import httpx
import pytest
from openai import APIConnectionError, APITimeoutError, BadRequestError, RateLimitError
from pydantic import ValidationError

from coding_review.errors import diagnose
from coding_review.workflow import Review, build_graph, markdown


def provider_error(cls, status, code, message):
    body = {
        "code": code,
        "message": message,
        "type": "invalid_request_error",
        "param": "response_format",
    }
    response = httpx.Response(
        status,
        request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"),
        headers={"x-request-id": "req_test"},
    )
    return cls(message, response=response, body=body)


def test_quota_error_explains_billing_and_redacts_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "private-value")
    exc = provider_error(
        RateLimitError, 429, "insufficient_quota", "quota exhausted private-value sk-test-key"
    )
    detail = diagnose(exc, "provider_request_or_parsing")
    assert detail["code"] == "insufficient_quota"
    assert detail["status_code"] == 429
    assert detail["request_id"] == "req_test"
    assert "billing" in detail["hint"]
    assert "private-value" not in str(detail)
    assert "sk-test-key" not in str(detail)


def test_schema_rejection_is_visible_in_graph_and_markdown():
    class BrokenModel:
        def with_structured_output(self, schema):
            return self

        def invoke(self, messages):
            raise provider_error(
                BadRequestError, 400, "invalid_json_schema", "Invalid schema for response_format"
            )

    report = build_graph(BrokenModel()).invoke({"files": {"app.py": "pass"}, "results": []})[
        "report"
    ]
    assert report["status"] == "incomplete"
    assert all(a["error"]["code"] == "invalid_json_schema" for a in report["agents"])
    assert "Invalid schema for response_format" in markdown(report)


def test_validation_diagnostics_do_not_include_raw_response():
    with pytest.raises(ValidationError) as failure:
        Review.model_validate({"findings": "private source content", "limitations": []})
    detail = diagnose(failure.value, "validate_response")
    assert detail["validation_errors"] == [{"location": ["findings"], "type": "list_type"}]
    assert "private source content" not in str(detail)


def test_timeout_and_connection_have_distinct_hints():
    request = httpx.Request("POST", "https://api.openai.com")
    assert "timed out" in diagnose(APITimeoutError(request=request), "request")["hint"]
    assert "TLS" in diagnose(APIConnectionError(request=request), "request")["hint"]
