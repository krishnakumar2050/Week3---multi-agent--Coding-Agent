"""Judge contracts, graph ordering, failure retention, and PR artifacts."""

import json

import pytest
from pydantic import ValidationError

from coding_review.agents.evaluation_prompt import SYSTEM_PROMPT
from coding_review.agents.evaluator import Evaluation, make_evaluator
from coding_review.domain import Review
from coding_review.graph import build_graph
from coding_review.integrations.github import run_review
from coding_review.reporting.rendering import markdown


def judgment(**updates):
    answer = {
        "reasoning": "Step 1 — Independent findings: No evidenced defects.\nStep 2 — Review comparison: Review correctly abstained.\nStep 3 — Evaluation outcome: No demonstrated omissions; limited sample.",
        "criteria_scores": {
            "bug_accuracy": 5,
            "security": 5,
            "actionability": 4,
            "false_positives": 5,
        },
        "overall_verdict": "PASS",
        "summary": "The review appropriately reports no evidenced defects.",
    }
    answer.update(updates)
    return answer


class Backend:
    backend_name = "fireworks"

    def __init__(self, fail=False):
        self.fail = fail
        self.judge_messages = None
        self.reviews = 0

    def with_structured_output(self, schema):
        parent = self

        class Runner:
            execution_metadata = {"backend": "fireworks", "actual_model": "judge-test"}

            def invoke(self, messages):
                if schema is Evaluation:
                    assert parent.reviews == 3
                    parent.judge_messages = messages
                    if parent.fail:
                        raise RuntimeError("sensitive-secret")
                    return judgment()
                parent.reviews += 1
                return Review(findings=[], limitations=[])

        return Runner()


def test_evaluation_runs_once_after_aggregator(monkeypatch):
    monkeypatch.setenv("KEENABLE_ENABLED", "false")
    monkeypatch.setenv("KEENABLE_SECURITY_ENABLED", "false")
    model = Backend()
    updates = list(
        build_graph(model, evaluator=model, evaluation_context={"diffs": ["+pass"]}).stream(
            {"files": {"a.py": "pass"}, "results": []}
        )
    )
    names = [name for update in updates for name in update]
    assert names[-2:] == ["aggregator", "evaluator"]
    report = updates[-1]["evaluator"]["report"]
    assert set(report["evaluation"]) == {
        "reasoning",
        "criteria_scores",
        "overall_verdict",
        "summary",
    }
    assert report["evaluation_execution"]["status"] == "ok"
    assert len(report["evaluation_execution"]["prompt_sha256"]) == 64
    assert model.judge_messages[0] == ("system", SYSTEM_PROMPT)
    assert '"diffs": ["+pass"]' in model.judge_messages[1][1]
    assert '"agents"' in model.judge_messages[1][1]
    assert "Review performance evaluation" in markdown(report)


def test_judge_failure_keeps_report_without_fabricated_scores(monkeypatch):
    monkeypatch.setenv("KEENABLE_ENABLED", "false")
    monkeypatch.setenv("KEENABLE_SECURITY_ENABLED", "false")
    model = Backend(fail=True)
    report = build_graph(model, evaluator=model).invoke({"files": {"a.py": "pass"}, "results": []})[
        "report"
    ]
    assert report["status"] == "complete" and len(report["agents"]) == 3
    assert "evaluation" not in report
    assert report["evaluation_execution"]["status"] == "failed"
    assert "sensitive-secret" not in str(report)
    assert "Evaluation failed; no scores" in markdown(report)


@pytest.mark.parametrize("value", [0, 6, True, "5", 4.5])
def test_score_requires_strict_integer_range(value):
    answer = judgment()
    answer["criteria_scores"]["security"] = value
    with pytest.raises(ValidationError):
        Evaluation.model_validate(answer)


def test_inconsistent_pass_and_missing_sections_rejected():
    answer = judgment()
    answer["criteria_scores"]["false_positives"] = 3
    with pytest.raises(ValidationError):
        Evaluation.model_validate(answer)
    with pytest.raises(ValidationError):
        Evaluation.model_validate(
            judgment(reasoning="No analysis", overall_verdict="NEEDS_REVISION")
        )
    with pytest.raises(ValidationError):
        Evaluation.model_validate({**judgment(), "extra": "not allowed"})


def test_invalid_judgment_is_disclosed_without_leaking_response():
    class Invalid:
        def with_structured_output(self, schema):
            return self

        def invoke(self, messages):
            return {"reasoning": "secret-response"}

    result = make_evaluator(Invalid())({"files": {"a.py": "pass"}, "report": {"findings": []}})[
        "report"
    ]
    assert result["evaluation_execution"]["status"] == "failed"
    assert "secret-response" not in str(result)
    assert "evaluation" not in result


def test_pr_writes_exact_schema_artifact(monkeypatch, tmp_path):
    monkeypatch.setenv("KEENABLE_ENABLED", "false")
    monkeypatch.setenv("KEENABLE_SECURITY_ENABLED", "false")
    sha = "a" * 40

    class Client:
        repository = "owner/repo"
        evaluation_changes = [
            {"file": "a.py", "patch": "+pass", "patch_missing_or_truncated": False}
        ]

        def pull_request(self, number):
            return {
                "head": {"sha": sha, "repo": {"full_name": self.repository}},
                "title": "Change",
                "body": "Requirement",
            }

        def changed_source_paths(self, number, expected_sha):
            return {"a.py"}

        def source_snapshot(self, expected_sha, max_bytes, selected_paths=None):
            return {"a.py": "pass"}

    report = run_review(Client(), 1, sha, tmp_path, backend=Backend(), scope="changed")
    assert report["evaluation_execution"]["status"] == "ok"
    artifact = json.loads((tmp_path / "evaluation.json").read_text())
    assert Evaluation.model_validate(artifact).overall_verdict == "PASS"
    assert artifact == report["evaluation"]
    assert json.loads((tmp_path / "evaluation-status.json").read_text())["status"] == "ok"


def test_pr_entrypoint_fails_on_judge_execution_error(monkeypatch, tmp_path):
    from coding_review.integrations import github

    event = tmp_path / "event.json"
    event.write_text(json.dumps({"number": 1, "pull_request": {"head": {"sha": "a" * 40}}}))
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setattr("sys.argv", ["github", "review", "--output", str(tmp_path)])

    class Client:
        def __init__(self, *args):
            pass

        def close(self):
            pass

    monkeypatch.setattr(github, "GitHubClient", Client)
    monkeypatch.setattr(
        github,
        "run_review",
        lambda *args, **kwargs: {
            "status": "complete",
            "evaluation_execution": {"status": "failed"},
        },
    )
    with pytest.raises(SystemExit) as error:
        github.main()
    assert error.value.code == 2


def test_failed_pr_evaluation_removes_stale_scores(monkeypatch, tmp_path):
    monkeypatch.setenv("KEENABLE_ENABLED", "false")
    monkeypatch.setenv("KEENABLE_SECURITY_ENABLED", "false")
    (tmp_path / "evaluation.json").write_text(json.dumps(judgment()))
    sha = "a" * 40

    class Client:
        repository = "owner/repo"

        def pull_request(self, number):
            return {"head": {"sha": sha, "repo": {"full_name": self.repository}}}

        def source_snapshot(self, expected_sha, max_bytes):
            return {"a.py": "pass"}

    report = run_review(Client(), 1, sha, tmp_path, backend=Backend(fail=True))
    assert report["evaluation_execution"]["status"] == "failed"
    assert not (tmp_path / "evaluation.json").exists()
    assert json.loads((tmp_path / "evaluation-status.json").read_text())["status"] == "failed"
