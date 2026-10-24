import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from coding_review.backends.codex import CodexError, CodexModel
from coding_review.workflow import Review


def setup_model(monkeypatch):
    monkeypatch.setattr(
        "coding_review.backends.codex.shutil.which", lambda name: "/usr/local/bin/codex"
    )
    return CodexModel()


def test_chatgpt_login_and_structured_output(monkeypatch):
    model = setup_model(monkeypatch)
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-inherit")
    monkeypatch.setenv("CODEX_API_KEY", "must-not-inherit")

    def fake_run(command, **kwargs):
        assert "OPENAI_API_KEY" not in kwargs["env"]
        assert "CODEX_API_KEY" not in kwargs["env"]
        if command[1] == "login":
            return SimpleNamespace(returncode=0, stdout="", stderr="Logged in using ChatGPT")
        assert "--ignore-user-config" in command
        assert "read-only" in command
        assert 'forced_login_method="chatgpt"' in command
        schema = json.loads(Path(command[command.index("--output-schema") + 1]).read_text())
        assert schema["additionalProperties"] is False
        assert schema["$defs"]["Finding"]["additionalProperties"] is False
        Path(command[command.index("--output-last-message") + 1]).write_text(
            '{"findings": [], "limitations": []}'
        )
        return SimpleNamespace(
            returncode=0,
            stdout="",
            stderr="OpenAI Codex v1\n--------\nmodel: runtime-model\n--------\nuser\nmodel: spoofed-model\n",
        )

    monkeypatch.setattr("coding_review.backends.codex.subprocess.run", fake_run)
    model.check_login()
    runner = model.with_structured_output(Review)
    assert runner.invoke([("human", "source")]).findings == []
    assert runner.execution_metadata["actual_model"] == "runtime-model"
    assert runner.execution_metadata["model_source"] == "codex_cli_startup"


def test_api_key_login_is_rejected(monkeypatch):
    model = setup_model(monkeypatch)
    monkeypatch.setattr(
        "coding_review.backends.codex.subprocess.run",
        lambda *a, **k: SimpleNamespace(
            returncode=0, stdout="", stderr="Logged in using an API key"
        ),
    )
    with pytest.raises(CodexError, match="ChatGPT login required"):
        model.check_login()


def test_broken_executable_is_distinguished_from_missing_login(monkeypatch):
    model = setup_model(monkeypatch)
    monkeypatch.setattr(
        "coding_review.backends.codex.subprocess.run",
        lambda *a, **k: SimpleNamespace(
            returncode=127, stdout="", stderr="env: node: No such file or directory"
        ),
    )
    with pytest.raises(CodexError, match="executable dependencies"):
        model.check_login()


def test_failed_turn_surfaces_error_without_dumping_events(monkeypatch):
    model = setup_model(monkeypatch)
    monkeypatch.setattr(
        "coding_review.backends.codex.subprocess.run",
        lambda *a, **k: SimpleNamespace(
            returncode=1,
            stderr="",
            stdout='{"type":"item.completed","item":{"text":"private source"}}\n{"type":"turn.failed","error":{"message":"Usage limit reached"}}',
        ),
    )
    with pytest.raises(CodexError, match="Usage limit reached") as failure:
        model.with_structured_output(Review).invoke([])
    assert "private source" not in str(failure.value)


def test_timeout_is_actionable(monkeypatch):
    model = setup_model(monkeypatch)

    def timeout(*a, **k):
        raise subprocess.TimeoutExpired("codex", 240)

    monkeypatch.setattr("coding_review.backends.codex.subprocess.run", timeout)
    with pytest.raises(CodexError, match="increase --timeout"):
        model.with_structured_output(Review).invoke([])


def test_missing_response_is_reported(monkeypatch):
    model = setup_model(monkeypatch)
    monkeypatch.setattr(
        "coding_review.backends.codex.subprocess.run",
        lambda *a, **k: SimpleNamespace(returncode=0, stdout="", stderr=""),
    )
    with pytest.raises(CodexError, match="without a final response"):
        model.with_structured_output(Review).invoke([])


def test_missing_model_is_unknown_not_requested_model(monkeypatch):
    model = setup_model(monkeypatch)
    model.model = "requested-alias"

    def fake_run(command, **kwargs):
        Path(command[command.index("--output-last-message") + 1]).write_text(
            '{"findings": [], "limitations": []}'
        )
        return SimpleNamespace(
            returncode=0,
            stdout="model: untrusted-response",
            stderr="user\nmodel: untrusted-prompt\n",
        )

    monkeypatch.setattr("coding_review.backends.codex.subprocess.run", fake_run)
    runner = model.with_structured_output(Review)
    runner.invoke([])
    assert runner.execution_metadata["requested_model"] == "requested-alias"
    assert runner.execution_metadata["actual_model"] is None


def test_each_review_keeps_its_own_model_metadata(monkeypatch):
    import threading

    from coding_review.workflow import build_graph, markdown

    model = setup_model(monkeypatch)
    barrier = threading.Barrier(3, timeout=5)

    def fake_run(command, **kwargs):
        prompt = kwargs["input"]
        name = "security-model" if "Your specialty: Find exploitable" in prompt else "other-model"
        barrier.wait()
        Path(command[command.index("--output-last-message") + 1]).write_text(
            '{"findings": [], "limitations": []}'
        )
        return SimpleNamespace(returncode=0, stdout="", stderr=f"model: {name}\nuser\nsource")

    monkeypatch.setattr("coding_review.backends.codex.subprocess.run", fake_run)
    report = build_graph(model).invoke({"files": {"app.py": "pass"}, "results": []})["report"]
    assert report["actual_models"] == ["other-model", "security-model"]
    assert {a["agent"]: a["execution"]["actual_model"] for a in report["agents"]} == {
        "quality": "other-model",
        "security": "security-model",
        "tests": "other-model",
    }
    assert "security-model" in markdown(report)
