"""GitHub automation behavior without network, secrets, or model calls."""

import base64
import json

import httpx
import pytest

from coding_review.domain import Review
from coding_review.exceptions import ConfigurationError
from coding_review.integrations.github import MARKER, GitHubClient, comment_body, run_review

SHA = "a" * 40


def tree_entry(path, content="pass", mode="100644"):
    return {
        "path": path,
        "type": "blob",
        "mode": mode,
        "size": len(content.encode()),
        "sha": path.replace("/", "-"),
    }


def test_snapshot_fetches_only_source_blobs_not_symlinks_or_hidden_files():
    paths = [
        tree_entry("app.py"),
        tree_entry("tests/test_app.py"),
        tree_entry(".env.py"),
        tree_entry(".github/coding-review/runner.py"),
        tree_entry("linked.py", mode="120000"),
        tree_entry("node_modules/a.js"),
    ]
    requested = []

    def transport(request):
        requested.append(request.url.path)
        if "/git/trees/" in request.url.path:
            return httpx.Response(200, json={"tree": paths, "truncated": False})
        assert "/git/blobs/" in request.url.path
        return httpx.Response(
            200, json={"encoding": "base64", "content": base64.b64encode(b"pass").decode()}
        )

    client = GitHubClient("owner/repo", "fake-token", transport=httpx.MockTransport(transport))
    try:
        assert client.source_snapshot(SHA, 100) == {"app.py": "pass", "tests/test_app.py": "pass"}
        assert len(requested) == 3
    finally:
        client.close()


@pytest.mark.parametrize(
    "tree,match",
    [
        ({"truncated": True}, "truncated"),
        ({"tree": [tree_entry("large.py", "x" * 101)]}, "byte budget"),
        ({"tree": [tree_entry("../app.py")]}, "Invalid"),
    ],
)
def test_incomplete_or_unsafe_snapshots_fail_explicitly(tree, match):
    client = GitHubClient(
        "owner/repo",
        "fake-token",
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json=tree)),
    )
    try:
        with pytest.raises(ValueError, match=match):
            client.source_snapshot(SHA, 100)
    finally:
        client.close()


def test_actual_blob_bytes_are_checked_even_if_tree_size_is_wrong():
    def transport(request):
        if "/git/trees/" in request.url.path:
            return httpx.Response(200, json={"tree": [tree_entry("app.py")]})
        return httpx.Response(
            200, json={"encoding": "base64", "content": base64.b64encode(b"x" * 101).decode()}
        )

    client = GitHubClient("owner/repo", "fake-token", transport=httpx.MockTransport(transport))
    try:
        with pytest.raises(ValueError, match="byte budget"):
            client.source_snapshot(SHA, 100)
    finally:
        client.close()


def test_only_actions_bot_marked_comment_is_updated():
    calls = []

    def transport(request):
        calls.append((request.method, request.url.path))
        if request.method == "GET":
            return httpx.Response(
                200,
                json=[
                    {"id": 1, "body": MARKER, "user": {"login": "human"}},
                    {"id": 2, "body": MARKER, "user": {"login": "github-actions[bot]"}},
                ],
            )
        assert json.loads(request.content)["body"] == "new report"
        return httpx.Response(200, json={"id": 2})

    client = GitHubClient("owner/repo", "fake-token", transport=httpx.MockTransport(transport))
    try:
        client.upsert_comment(3, "new report")
        assert calls[-1] == ("PATCH", "/repos/owner/repo/issues/comments/2")
    finally:
        client.close()


def test_new_comment_is_created_when_no_marked_bot_comment_exists():
    calls = []

    def transport(request):
        calls.append(request.method)
        return httpx.Response(200, json=[] if request.method == "GET" else {"id": 3})

    client = GitHubClient("owner/repo", "fake-token", transport=httpx.MockTransport(transport))
    try:
        client.upsert_comment(3, "report")
        assert calls == ["GET", "POST"]
    finally:
        client.close()


class FakeBackend:
    def with_structured_output(self, schema):
        return self

    def invoke(self, messages):
        return Review(findings=[], limitations=["<b>untrusted</b> @someone"])


class FakeClient:
    repository = "owner/repo"

    def pull_request(self, number):
        return {"head": {"sha": SHA, "repo": {"full_name": self.repository}}}

    def source_snapshot(self, sha, max_bytes):
        return {"app.py": "pass"}


def test_review_outputs_commit_provenance_and_escaped_comment(tmp_path):
    report = run_review(FakeClient(), 3, SHA, tmp_path, backend=FakeBackend())
    assert json.loads((tmp_path / "report.json").read_text())["github"]["head_sha"] == SHA
    assert (tmp_path / "report.md").exists()
    body = comment_body(report)
    assert body.startswith(MARKER)
    assert "@someone" not in body
    assert "<b>" not in body
    assert "&lt;b&gt;" in body


def test_fork_and_stale_commits_are_rejected_before_snapshot(tmp_path):
    class Fork(FakeClient):
        def pull_request(self, number):
            return {"head": {"sha": SHA, "repo": {"full_name": "untrusted/fork"}}}

    with pytest.raises(ConfigurationError, match="same-repository"):
        run_review(Fork(), 3, SHA, tmp_path, backend=FakeBackend())
    with pytest.raises(ValueError, match="head changed"):
        run_review(FakeClient(), 3, "b" * 40, tmp_path, backend=FakeBackend())


def test_changed_snapshot_ignores_large_unchanged_files():
    def transport(request):
        if "/git/trees/" in request.url.path:
            return httpx.Response(
                200,
                json={"tree": [tree_entry("large.java", "x" * 1000), tree_entry("changed.java")]},
            )
        assert request.url.path.endswith("changed.java")
        return httpx.Response(200, json={"encoding": "base64", "content": "cGFzcw=="})

    client = GitHubClient("owner/repo", "fake", transport=httpx.MockTransport(transport))
    try:
        assert client.source_snapshot(SHA, 100, {"changed.java"}) == {"changed.java": "pass"}
    finally:
        client.close()


def test_changed_paths_filter_and_head_race():
    heads = [SHA, SHA]

    def transport(request):
        if request.url.path.endswith("/files"):
            return httpx.Response(
                200,
                json=[
                    {"filename": "app.java", "status": "modified"},
                    {"filename": "renamed.kt", "status": "renamed"},
                    {"filename": "gone.java", "status": "removed"},
                    {"filename": "README.md", "status": "modified"},
                    {"filename": ".github/engine.py", "status": "added"},
                ],
            )
        return httpx.Response(200, json={"head": {"sha": heads.pop(0)}, "changed_files": 5})

    client = GitHubClient("owner/repo", "fake", transport=httpx.MockTransport(transport))
    try:
        assert client.changed_source_paths(1, SHA) == {"app.java", "renamed.kt"}
        heads[:] = [SHA, "b" * 40]
        with pytest.raises(ValueError, match="head changed"):
            client.changed_source_paths(1, SHA)
    finally:
        client.close()


def test_changed_paths_reject_api_limit():
    client = GitHubClient(
        "owner/repo",
        "fake",
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json={"head": {"sha": SHA}, "changed_files": 3000})
        ),
    )
    try:
        with pytest.raises(ValueError, match="too many files"):
            client.changed_source_paths(1, SHA)
    finally:
        client.close()


def test_docs_only_review_skips_models_and_reports_scope(tmp_path):
    class Docs(FakeClient):
        def changed_source_paths(self, number, sha):
            return set()

        def source_snapshot(self, *args, **kwargs):
            pytest.fail("No source blobs should be read")

    report = run_review(Docs(), 3, SHA, tmp_path, scope="changed")
    assert report["status"] == "skipped"
    assert report["agents"] == []
    assert "Changed supported files" in comment_body(report)
    assert "no model was called" in report["coverage_note"]


def test_changed_review_passes_immutable_paths(tmp_path):
    class Changed(FakeClient):
        def changed_source_paths(self, number, sha):
            assert sha == SHA
            return {"app.py"}

        def source_snapshot(self, sha, max_bytes, selected_paths=None):
            assert selected_paths == {"app.py"} and sha == SHA
            return {"app.py": "pass"}

    report = run_review(Changed(), 3, SHA, tmp_path, backend=FakeBackend(), scope="changed")
    assert report["status"] == "complete"
    assert "Unchanged files and deleted files are not reviewed" in report["github"]["scope"]
