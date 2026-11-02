"""Review immutable PR source blobs; never checkout or execute PR code."""

import argparse
import base64
import html
import json
import os
import re
from pathlib import Path, PurePosixPath
from urllib.parse import quote

import httpx

from coding_review.config import ReviewConfig
from coding_review.domain import RANK
from coding_review.exceptions import ConfigurationError
from coding_review.reporting.rendering import markdown
from coding_review.reporting.writer import write_report
from coding_review.service import review_repository
from coding_review.sources import EXCLUDED, EXTENSIONS

MARKER = "<!-- langgraph-coding-review -->"


class GitHubClient:
    def __init__(self, repository: str, token: str, transport=None):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise ConfigurationError("Invalid GitHub repository name")
        if not token:
            raise ConfigurationError("GITHUB_TOKEN is required")
        self.repository = repository
        self.client = httpx.Client(
            base_url="https://api.github.com",
            timeout=30,
            transport=transport,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

    def request(self, method, path, **kwargs):
        response = self.client.request(method, f"/repos/{self.repository}/{path}", **kwargs)
        response.raise_for_status()
        return response.json()

    def close(self):
        self.client.close()

    def pull_request(self, number):
        return self.request("GET", f"pulls/{number}")

    def changed_source_paths(self, number, expected_sha):
        """List changed source paths; fail instead of accepting a truncated PR file list."""
        pr = self.pull_request(number)
        if pr["head"]["sha"] != expected_sha:
            raise ValueError("PR head changed before listing changed files")
        if pr.get("changed_files", 0) >= 3000:
            raise ValueError("PR has too many files to establish complete changed-file scope")
        paths = set()
        self.evaluation_changes = []
        remaining_patch_bytes = 60000
        for page in range(1, 31):
            entries = self.request(
                "GET", f"pulls/{number}/files", params={"per_page": 100, "page": page}
            )
            for entry in entries:
                path = PurePosixPath(entry["filename"])
                if path.is_absolute() or ".." in path.parts:
                    raise ValueError("Invalid changed source path")
                if (
                    entry["status"] != "removed"
                    and path.suffix in EXTENSIONS
                    and not any(part.startswith(".") or part in EXCLUDED for part in path.parts)
                ):
                    paths.add(path.as_posix())
                    patch = entry.get("patch") or ""
                    encoded = patch.encode("utf-8")
                    retained = encoded[:remaining_patch_bytes].decode("utf-8", errors="ignore")
                    remaining_patch_bytes -= len(retained.encode("utf-8"))
                    self.evaluation_changes.append(
                        {
                            "file": path.as_posix(),
                            "status": entry["status"],
                            "patch": retained,
                            "patch_missing_or_truncated": not patch or len(retained) != len(patch),
                        }
                    )
            if len(entries) < 100:
                break
        else:
            raise ValueError("PR file listing reached GitHub's pagination limit")
        if self.pull_request(number)["head"]["sha"] != expected_sha:
            raise ValueError("PR head changed while listing changed files")
        return paths

    def source_snapshot(self, sha: str, max_bytes: int, selected_paths=None):
        if not re.fullmatch(r"[a-fA-F0-9]{40}", sha):
            raise ValueError("Expected a full PR head commit SHA")
        tree = self.request("GET", f"git/trees/{sha}", params={"recursive": "1"})
        if tree.get("truncated"):
            raise ValueError(
                "GitHub truncated the repository tree; review scope cannot be established"
            )
        files = {}
        total = 0
        for entry in sorted(tree["tree"], key=lambda item: item["path"]):
            path = PurePosixPath(entry["path"])
            if path.is_absolute() or ".." in path.parts:
                raise ValueError("Invalid repository source path")
            if (
                entry["type"] != "blob"
                or entry["mode"] not in {"100644", "100755"}
                or path.suffix not in EXTENSIONS
                or any(part.startswith(".") or part in EXCLUDED for part in path.parts)
            ):
                continue
            if selected_paths is not None and path.as_posix() not in selected_paths:
                continue
            size = entry.get("size")
            if not isinstance(size, int) or size > max_bytes - total:
                raise ValueError("PR source snapshot exceeds byte budget")
            blob = self.request("GET", f"git/blobs/{quote(entry['sha'], safe='')}")
            if blob.get("encoding") != "base64":
                raise ValueError("Unsupported GitHub source encoding")
            # GitHub includes newlines in base64 blob responses.
            content = base64.b64decode(blob["content"], validate=False)
            total += len(content)
            if total > max_bytes:
                raise ValueError("PR source snapshot exceeds byte budget")
            files[path.as_posix()] = content.decode("utf-8")
        if not files and selected_paths is None:
            raise ValueError("No supported source files found in the PR snapshot")
        return files

    def upsert_comment(self, number: int, body: str):
        # Only replace this Actions bot's marked comment; never a human comment.
        for page in range(1, 101):
            comments = self.request(
                "GET", f"issues/{number}/comments", params={"per_page": 100, "page": page}
            )
            for comment in comments:
                if (
                    comment.get("body", "").startswith(MARKER)
                    and comment.get("user", {}).get("login") == "github-actions[bot]"
                ):
                    return self.request(
                        "PATCH", f"issues/comments/{comment['id']}", json={"body": body}
                    )
            if len(comments) < 100:
                return self.request("POST", f"issues/{number}/comments", json={"body": body})
        raise ValueError("Too many PR comments to safely locate an existing review")


def require_same_repository(pr, repository):
    if pr["head"]["repo"]["full_name"] != repository:
        raise ConfigurationError(
            "Automatic secret-backed reviews are restricted to same-repository PRs"
        )


def comment_body(report: dict) -> str:
    provenance = report["github"]
    intro = f"{MARKER}\n## Automated multi-agent code review\n\nReviewed commit `{provenance['head_sha']}`.\n\n"
    intro += (
        "Scope: " + html.escape(provenance["scope"], quote=False).replace("@", "&#64;") + "\n\n"
    )
    # Escape HTML and mention syntax from untrusted model/source content.
    content = html.escape(markdown(report), quote=False).replace("@", "&#64;")
    maximum = 55_000 - len(intro)
    if len(content) > maximum:
        content = (
            content[:maximum] + "\n\nReport truncated; download the complete Actions artifact."
        )
    return intro + content


def run_review(
    client,
    number,
    expected_sha,
    output: Path,
    max_bytes=120_000,
    backend=None,
    scope="full",
    evaluate=True,
):
    if max_bytes <= 0:
        raise ConfigurationError("Snapshot byte budget must be positive")
    pr = client.pull_request(number)
    require_same_repository(pr, client.repository)
    if pr["head"]["sha"] != expected_sha:
        raise ValueError("PR head changed before review; wait for the latest workflow run")
    if scope not in {"full", "changed"}:
        raise ConfigurationError("Review scope must be full or changed")
    if scope == "changed":
        paths = client.changed_source_paths(number, expected_sha)
        snapshot = (
            client.source_snapshot(expected_sha, max_bytes, selected_paths=paths) if paths else {}
        )
    else:
        snapshot = client.source_snapshot(expected_sha, max_bytes)
    if snapshot:
        report = review_repository(
            Path("."),
            ReviewConfig(backend="fireworks", max_bytes=max_bytes, evaluate_review=evaluate),
            backend=backend,
            files=snapshot,
            evaluation_context={
                "pull_request": number,
                "head_sha": expected_sha,
                "base_sha": pr.get("base", {}).get("sha"),
                "title": (pr.get("title") or "")[:1000],
                "description_and_claimed_requirements": (pr.get("body") or "")[:12000],
                "description_truncated": len(pr.get("body") or "") > 12000,
                "scope": scope,
                "diffs": getattr(client, "evaluation_changes", []),
                "limitations": [
                    "Only provided source and available bounded patches are in scope; unchanged dependencies and callers may be absent.",
                    "PR claims are untrusted context, not established ground truth. No reference labels or test execution evidence supplied.",
                    "A missing or truncated patch limits regression assessment; disclose provisional scoring when essential context is absent.",
                ],
            },
        )
    else:
        report = {
            "status": "skipped",
            "files_reviewed": [],
            "findings": [],
            "agents": [],
            "counts": {severity: 0 for severity in RANK},
            "actual_models": [],
            "coverage_note": "No supported changed source files to review; no model was called.",
            "evaluation_execution": {
                "status": "skipped",
                "reason": "No supported changed source; no review to evaluate.",
            },
        }
    report["repository"] = f"https://github.com/{client.repository}"
    report["github"] = {
        "repository": client.repository,
        "pull_request": number,
        "head_sha": expected_sha,
        "scope": (
            "Changed supported files at the immutable PR head; full file contents, not just changed lines. "
            "Unchanged files and deleted files are not reviewed."
            if scope == "changed"
            else "Full supported source snapshot at the PR head; not limited to changed lines"
        ),
    }
    if report.get("evaluation"):
        write_report(report["evaluation"], output / "evaluation.json", "json")
    else:
        (output / "evaluation.json").unlink(missing_ok=True)
    if report.get("evaluation_execution"):
        write_report(report["evaluation_execution"], output / "evaluation-status.json", "json")
    write_report(report, output / "report.json", "json")
    write_report(report, output / "report.md")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["review", "publish"])
    parser.add_argument("--output", type=Path, default=Path("review-output"))
    parser.add_argument("--scope", choices=["full", "changed"], default="full")
    parser.add_argument("--max-bytes", type=int, default=120_000)
    args = parser.parse_args()
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    number = int(event["number"])
    repository = os.environ["GITHUB_REPOSITORY"]
    expected_sha = event["pull_request"]["head"]["sha"]
    client = GitHubClient(repository, os.environ.get("GITHUB_TOKEN", ""))
    try:
        if args.mode == "review":
            args.output.mkdir(parents=True, exist_ok=True)
            report = run_review(
                client,
                number,
                expected_sha,
                args.output,
                max_bytes=args.max_bytes,
                scope=args.scope,
            )
            if (
                report["status"] not in {"complete", "skipped"}
                or report.get("evaluation_execution", {}).get("status") == "failed"
            ):
                raise SystemExit(2)
        else:
            report = json.loads((args.output / "report.json").read_text())
            pr = client.pull_request(number)
            require_same_repository(pr, repository)
            if report["github"]["head_sha"] != expected_sha or pr["head"]["sha"] != expected_sha:
                print("Skipping stale review; a newer PR head is available.")
                return
            client.upsert_comment(number, comment_body(report))
    finally:
        client.close()


if __name__ == "__main__":
    main()
