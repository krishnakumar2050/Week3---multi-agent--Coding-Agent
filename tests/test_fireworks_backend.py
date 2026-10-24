"""Exercise the real SDK request/response boundary without network access."""

import io
import json
from contextlib import redirect_stderr

import httpx
import pytest
from openai import OpenAI
from pydantic import ValidationError

from coding_review.backends.factory import create_backend
from coding_review.backends.fireworks import (
    DEFAULT_FIREWORKS_MODEL,
    FIREWORKS_BASE_URL,
    FireworksBackend,
)
from coding_review.cli import build_parser, main
from coding_review.config import ReviewConfig
from coding_review.domain import Review
from coding_review.errors import diagnose
from coding_review.exceptions import ConfigurationError, ProviderResponseError
from coding_review.graph import build_graph


def backend_for(transport):
    client = OpenAI(
        api_key="test-fireworks-key",
        base_url=FIREWORKS_BASE_URL,
        max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(transport)),
    )
    return FireworksBackend(api_key="test-fireworks-key", client=client)


def completion(
    content='{"findings": [], "limitations": []}', finish_reason="stop", model="resolved-minimax"
):
    return {
        "id": "test-completion",
        "object": "chat.completion",
        "created": 0,
        "model": model,
        "choices": [
            {
                "index": 0,
                "finish_reason": finish_reason,
                "message": {"role": "assistant", "content": content},
            }
        ],
    }


def test_request_schema_roles_endpoint_and_runtime_model():
    def transport(request):
        assert str(request.url) == FIREWORKS_BASE_URL + "/chat/completions"
        assert request.headers["authorization"] == "Bearer test-fireworks-key"
        body = json.loads(request.content)
        assert body["model"] == DEFAULT_FIREWORKS_MODEL
        assert body["messages"][-1] == {"role": "user", "content": "source snapshot"}
        assert "JSON" in body["messages"][0]["content"]
        assert body["response_format"]["type"] == "json_schema"
        assert "Finding" in body["response_format"]["json_schema"]["schema"]["$defs"]
        assert body["max_tokens"] == 8192
        return httpx.Response(200, json=completion())

    backend = backend_for(transport)
    runner = backend.with_structured_output(Review)
    assert runner.invoke([("human", "source snapshot")]).findings == []
    assert runner.execution_metadata["backend"] == "fireworks"
    assert runner.execution_metadata["actual_model"] == "resolved-minimax"
    assert runner.execution_metadata["requested_model"] == DEFAULT_FIREWORKS_MODEL


@pytest.mark.parametrize(
    "content,reason,error",
    [
        ("{", "length", ProviderResponseError),
        ("", "stop", ProviderResponseError),
        ("{}", "content_filter", ProviderResponseError),
        ("{", "stop", ValidationError),
        ('{"findings": "invalid", "limitations": []}', "stop", ValidationError),
    ],
)
def test_invalid_or_truncated_outputs_are_not_success(content, reason, error):
    backend = backend_for(lambda request: httpx.Response(200, json=completion(content, reason)))
    with pytest.raises(error):
        backend.with_structured_output(Review).invoke([])


def test_provider_auth_error_reports_fireworks_variable():
    def transport(request):
        return httpx.Response(
            401, json={"error": {"message": "Invalid API key", "code": "invalid_api_key"}}
        )

    report = build_graph(backend_for(transport)).invoke(
        {"files": {"app.py": "pass"}, "results": []}
    )["report"]
    assert report["status"] == "incomplete"
    assert all("FIREWORKS_API_KEY" in a["error"]["hint"] for a in report["agents"])
    assert "test-fireworks-key" not in str(report)


def test_absent_model_metadata_does_not_fall_back_to_requested_model():
    backend = backend_for(lambda request: httpx.Response(200, json=completion(model=None)))
    runner = backend.with_structured_output(Review)
    runner.invoke([])
    assert runner.execution_metadata["actual_model"] is None


def test_fireworks_is_default_and_ignores_other_provider_settings(monkeypatch):
    monkeypatch.setenv("FIREWORKS_API_KEY", "fireworks-only")
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-use")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://wrong.example")
    monkeypatch.setenv("REVIEW_MODEL", "wrong-model")
    monkeypatch.delenv("FIREWORKS_MODEL", raising=False)
    assert build_parser().parse_args(["examples"]).backend == "fireworks"
    backend = create_backend(ReviewConfig())
    assert backend.model == DEFAULT_FIREWORKS_MODEL
    assert backend.client.api_key == "fireworks-only"
    assert str(backend.client.base_url).rstrip("/") == FIREWORKS_BASE_URL


def test_model_override_precedence(monkeypatch):
    monkeypatch.setenv("FIREWORKS_API_KEY", "test-key")
    monkeypatch.setenv("FIREWORKS_MODEL", "environment-deployment")
    assert create_backend(ReviewConfig()).model == "environment-deployment"
    assert create_backend(ReviewConfig(model="explicit-deployment")).model == "explicit-deployment"


def test_missing_key_fails_clearly_without_fallback(tmp_path, monkeypatch):
    monkeypatch.delenv("FIREWORKS_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-use")
    with pytest.raises(ConfigurationError, match="FIREWORKS_API_KEY"):
        create_backend(ReviewConfig())
    (tmp_path / "app.py").write_text("pass")
    stderr = io.StringIO()
    with redirect_stderr(stderr), pytest.raises(SystemExit) as failure:
        main([str(tmp_path), "--output", str(tmp_path / "report.md")])
    assert failure.value.code == 2
    assert "FIREWORKS_API_KEY" in stderr.getvalue()
    assert not (tmp_path / "report.md").exists()


def test_known_response_error_is_actionable_without_raw_output():
    detail = diagnose(
        ProviderResponseError("Fireworks returned no response choices."),
        "request",
        backend="fireworks",
    )
    assert "no response choices" in detail["message"]
