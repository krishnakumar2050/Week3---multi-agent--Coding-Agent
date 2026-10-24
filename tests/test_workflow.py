import threading

from coding_review.cli import load_files
from coding_review.workflow import Finding, Review, build_graph, markdown


class FakeModel:
    def __init__(self, fail=None, invalid=False):
        self.fail = fail
        self.invalid = invalid
        self.barrier = threading.Barrier(3, timeout=5)

    def with_structured_output(self, schema):
        return self

    def invoke(self, messages):
        self.barrier.wait()  # Fails if the graph does not run all three in parallel.
        prompt = messages[0][1]
        if self.fail and self.fail in prompt:
            raise RuntimeError("sensitive provider error")
        security = "exploitable security" in prompt
        return Review(
            findings=[
                Finding(
                    severity="high" if security else "medium",
                    title="Unsafe operation",
                    file="app.py",
                    line=99 if self.invalid else 1,
                    evidence="eval(user_input)",
                    explanation="Untrusted input can execute code.",
                    recommendation="Parse allowed values.",
                    suggested_test="Assert malicious input is rejected.",
                )
            ],
            limitations=["Only supplied files reviewed."],
        )


def run(model):
    return build_graph(model).invoke({"files": {"app.py": "eval(user_input)\n"}, "results": []})[
        "report"
    ]


def test_parallel_join_deduplication_and_severity():
    report = run(FakeModel())
    assert report["status"] == "complete"
    assert len(report["agents"]) == 3
    assert len(report["findings"]) == 1
    assert report["findings"][0]["severity"] == "high"
    assert report["findings"][0]["agents"] == ["quality", "security", "tests"]
    assert report["counts"]["high"] == 1
    assert "[HIGH]" in markdown(report)


def test_failure_returns_partial_report_without_exception_content():
    report = run(FakeModel(fail="exploitable security"))
    assert report["status"] == "incomplete"
    assert len(report["findings"]) == 1
    assert "sensitive provider error" not in str(report)


def test_invalid_evidence_is_discarded():
    report = run(FakeModel(invalid=True))
    assert report["findings"] == []
    assert all("Discarded" in agent["limitations"][-1] for agent in report["agents"])


def test_snapshot_excludes_secrets_symlinks_and_generated_files(tmp_path):
    (tmp_path / "app.py").write_text("pass\n")
    (tmp_path / ".env").write_text("SECRET=value")
    (tmp_path / "linked.py").symlink_to(tmp_path / "app.py")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "lib.js").write_text("ignored")
    assert load_files(tmp_path) == {"app.py": "pass\n"}


def test_snapshot_budget_fails_explicitly(tmp_path):
    import pytest

    (tmp_path / "app.py").write_text("pass\n")
    with pytest.raises(ValueError, match="budget"):
        load_files(tmp_path, max_bytes=1)
