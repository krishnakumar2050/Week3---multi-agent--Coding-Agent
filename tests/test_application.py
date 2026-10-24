"""Application and integration boundaries with no provider credentials."""

import io
import json
from contextlib import redirect_stderr, redirect_stdout
from types import SimpleNamespace

import pytest

from coding_review.cli import main
from coding_review.config import ReviewConfig
from coding_review.domain import AgentResult, Review
from coding_review.exceptions import ConfigurationError
from coding_review.reporting.aggregation import orchestrate
from coding_review.reporting.writer import write_report
from coding_review.service import review_repository
from coding_review.sources import load_files


class FakeBackend:
    def with_structured_output(self, schema):
        # A separate runner per agent is essential for metadata isolation.
        class Runner:
            execution_metadata = {
                "backend": "codex",
                "actual_model": "test-model",
                "model_source": "test",
                "requested_model": None,
            }

            def invoke(self, messages):
                return Review(findings=[], limitations=[])

        return Runner()


@pytest.mark.parametrize(
    "options",
    [
        {"timeout": 0},
        {"timeout": float("nan")},
        {"timeout": float("inf")},
        {"max_bytes": -1},
        {"max_concurrency": 0},
        {"max_concurrency": 4},
        {"backend": "unsupported"},
        {"model": " "},
    ],
)
def test_invalid_configuration_is_rejected(options):
    with pytest.raises(ConfigurationError):
        ReviewConfig(**options)


def test_source_exclusion_and_nested_symlinks(tmp_path):
    (tmp_path / "app.py").write_text("pass\n")
    (tmp_path / "generated").mkdir()
    (tmp_path / "generated" / "large.py").write_text("x" * 1000)
    (tmp_path / "external").symlink_to(tmp_path / "generated", target_is_directory=True)
    assert load_files(tmp_path, 10, ("generated/*",)) == {"app.py": "pass\n"}


def test_service_records_snapshot_identity_and_run_metadata(tmp_path, caplog):
    caplog.set_level("INFO", logger="coding_review")
    config = ReviewConfig(max_concurrency=1)
    first = review_repository(tmp_path, config, FakeBackend(), files={"app.py": "private source"})
    second = review_repository(tmp_path, config, FakeBackend(), files={"app.py": "changed source"})
    same = review_repository(tmp_path, config, FakeBackend(), files={"app.py": "private source"})
    assert first["status"] == "complete"
    assert first["model"] == "test-model"
    assert first["snapshot_sha256"] == same["snapshot_sha256"]
    assert first["snapshot_sha256"] != second["snapshot_sha256"]
    assert first["run_id"] != same["run_id"]
    assert first["schema_version"] == "1.0"
    assert "private source" not in caplog.text
    assert "agent_finished" in caplog.text


def test_missing_reviewer_cannot_be_masked_by_duplicate_result():
    results = [AgentResult(agent=name, status="ok") for name in ("quality", "quality", "tests")]
    assert orchestrate({"files": {}, "results": results})["report"]["status"] == "incomplete"


def test_atomic_write_preserves_previous_report_on_failure(tmp_path, monkeypatch):
    destination = tmp_path / "report.json"
    destination.write_text("previous")

    def fail(*args):
        raise OSError("simulated replace failure")

    monkeypatch.setattr("coding_review.reporting.writer.os.replace", fail)
    with pytest.raises(OSError):
        write_report({"status": "complete"}, destination, "json")
    assert destination.read_text() == "previous"
    assert list(tmp_path.glob(".review-*.tmp")) == []


def test_json_and_markdown_report_round_trip(tmp_path):
    report = review_repository(tmp_path, ReviewConfig(), FakeBackend(), files={"app.py": "pass"})
    write_report(report, tmp_path / "report.json", "json")
    write_report(report, tmp_path / "report.md")
    assert json.loads((tmp_path / "report.json").read_text())["run_id"] == report["run_id"]
    rendered = (tmp_path / "report.md").read_text()
    assert report["snapshot_sha256"] in rendered
    assert "test-model" in rendered


def test_cli_snapshot_only_never_initializes_backend(tmp_path, monkeypatch):
    (tmp_path / "app.py").write_text("pass")

    def fail(*args):
        pytest.fail("snapshot-only must not initialize a backend")

    monkeypatch.setattr("coding_review.service.create_backend", fail)
    output = io.StringIO()
    with redirect_stdout(output):
        main([str(tmp_path), "--snapshot-only"])
    assert "app.py" in output.getvalue()


def test_cli_complete_and_incomplete_exit_codes(tmp_path, monkeypatch):
    (tmp_path / "app.py").write_text("pass")
    monkeypatch.setattr("coding_review.service.create_backend", lambda config: FakeBackend())
    output = tmp_path / "report.json"
    main([str(tmp_path), "--format", "json", "--output", str(output)])
    assert json.loads(output.read_text())["status"] == "complete"

    class Broken(FakeBackend):
        def with_structured_output(self, schema):
            raise RuntimeError("private diagnostic")

    monkeypatch.setattr("coding_review.service.create_backend", lambda config: Broken())
    stderr = io.StringIO()
    with redirect_stderr(stderr), pytest.raises(SystemExit) as failure:
        main([str(tmp_path), "--format", "json", "--output", str(output)])
    assert failure.value.code == 2
    assert json.loads(output.read_text())["status"] == "incomplete"
    assert "private diagnostic" not in stderr.getvalue()


def test_cli_rejects_overwriting_source_before_model_call(tmp_path, monkeypatch):
    source = tmp_path / "app.py"
    source.write_text("pass")
    monkeypatch.setattr(
        "coding_review.service.create_backend",
        lambda config: pytest.fail("backend should not be called"),
    )
    with pytest.raises(SystemExit) as failure:
        main([str(tmp_path), "--output", str(source)])
    assert failure.value.code == 2
    assert source.read_text() == "pass"


def test_api_backend_records_runtime_model_and_propagates_parsing_errors():
    from coding_review.backends.openai import OpenAIBackend

    class Client:
        def with_structured_output(self, schema, include_raw):
            assert include_raw is True
            return self

        def invoke(self, messages):
            return {
                "raw": SimpleNamespace(response_metadata={"model_name": "resolved-api-model"}),
                "parsed": Review(findings=[], limitations=[]),
                "parsing_error": None,
            }

    runner = OpenAIBackend("alias", 10, Client()).with_structured_output(Review)
    runner.invoke([])
    assert runner.execution_metadata["actual_model"] == "resolved-api-model"
    assert runner.execution_metadata["requested_model"] == "alias"


def test_api_parsing_error_keeps_model_provenance():
    from coding_review.backends.openai import OpenAIBackend

    class Client:
        def with_structured_output(self, schema, include_raw):
            return self

        def invoke(self, messages):
            return {
                "raw": SimpleNamespace(response_metadata={"model_name": "resolved"}),
                "parsed": None,
                "parsing_error": ValueError("invalid output"),
            }

    runner = OpenAIBackend("alias", 10, Client()).with_structured_output(Review)
    with pytest.raises(ValueError, match="invalid output"):
        runner.invoke([])
    assert runner.execution_metadata["actual_model"] == "resolved"


def test_backend_factory_does_not_silently_fall_back_to_api(monkeypatch):
    from coding_review.backends.factory import create_backend
    from coding_review.exceptions import CodexError

    monkeypatch.setenv("OPENAI_API_KEY", "unused-key")

    def fail(self):
        raise CodexError("ChatGPT login required")

    monkeypatch.setattr("coding_review.backends.codex.CodexModel.check_login", fail)
    monkeypatch.setattr("coding_review.backends.codex.shutil.which", lambda name: "/test/codex")
    with pytest.raises(CodexError):
        create_backend(ReviewConfig(backend="codex"))


def test_atomic_writer_rejects_symlink_destination(tmp_path):
    target = tmp_path / "target.json"
    target.write_text("original")
    link = tmp_path / "report.json"
    link.symlink_to(target)
    with pytest.raises(ValueError, match="symlink"):
        write_report({}, link, "json")
    assert target.read_text() == "original"
