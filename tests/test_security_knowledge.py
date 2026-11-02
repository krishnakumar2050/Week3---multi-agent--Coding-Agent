"""Security enrichment isolation, official sources, and graceful degradation."""

from types import SimpleNamespace

import pytest

from coding_review.agents.knowledge import enrich_security
from coding_review.agents.reviewer import make_reviewer
from coding_review.domain import Review
from coding_review.reporting.rendering import markdown


@pytest.fixture(autouse=True)
def enable_security(monkeypatch):
    monkeypatch.setenv("KEENABLE_SECURITY_ENABLED", "true")


class Search:
    def __init__(self):
        self.queries = []

    def search(self, query):
        self.queries.append(query)
        host = "cwe.mitre.org" if "cwe.mitre.org" in query else "mas.owasp.org"
        return [
            SimpleNamespace(
                title="Guidance", url=f"https://{host}/{len(self.queries)}/{i}", snippet="x" * 2000
            )
            for i in range(10)
        ]


def test_queries_are_generic_bounded_and_mobile_specific():
    client = Search()
    context, metadata = enrich_security({"private.swift": "secret-code"}, client)
    assert len(client.queries) == 3
    assert len(metadata["sources"]) == 6
    assert "OWASP MASVS" in metadata["frameworks"]
    assert all("private" not in q and "secret-code" not in q for q in client.queries)
    assert all(len(s["snippet"]) == 1200 for s in metadata["sources"])
    assert "UNTRUSTED" in context and "exact repository citation" in context


def test_security_rejects_unofficial_and_deceptive_urls():
    class Bad:
        def search(self, query):
            return [
                SimpleNamespace(title="t", url=url, snippet="s")
                for url in [
                    "https://owasp.org.attacker.example/x",
                    "http://owasp.org/x",
                    "https://attacker.example/x",
                    "https://user:password@owasp.org/x",
                ]
            ]

    context, metadata = enrich_security({"a.py": "pass"}, Bad())
    assert context == "" and metadata["status"] == "empty"


def test_failure_hides_provider_error():
    class Broken:
        def search(self, query):
            raise RuntimeError("secret-token")

    context, metadata = enrich_security({"a.py": "pass"}, Broken())
    assert context == "" and metadata["status"] == "failed"
    assert "secret-token" not in str(metadata)


def test_explicit_disable_skips_search(monkeypatch):
    monkeypatch.setenv("KEENABLE_SECURITY_ENABLED", "false")
    client = Search()
    _, metadata = enrich_security({}, client)
    assert metadata["status"] == "disabled" and client.queries == []


def test_security_enabled_by_default(monkeypatch):
    monkeypatch.delenv("KEENABLE_SECURITY_ENABLED")
    monkeypatch.delenv("KEENABLE_ENABLED", raising=False)
    client = Search()
    _, metadata = enrich_security({"a.py": "pass"}, client)
    assert metadata["status"] == "ok" and len(client.queries) == 2


def test_only_security_receives_security_guidance(monkeypatch):
    monkeypatch.setenv("KEENABLE_ENABLED", "false")
    monkeypatch.setattr(
        "coding_review.agents.reviewer.enrich_security",
        lambda files: (
            "SECURITY_REFERENCE",
            {"status": "ok", "sources": [], "frameworks": ["CWE Top 25:2025"]},
        ),
    )

    class Model:
        def with_structured_output(self, schema):
            return self

        def invoke(self, messages):
            self.messages = messages
            return Review(findings=[], limitations=[])

    for name in ["quality", "security", "tests"]:
        model = Model()
        result = make_reviewer(name, model)({"files": {"a.py": "pass"}})["results"][0]
        assert result.status == "ok"
        assert ("SECURITY_REFERENCE" in model.messages[1][1]) == (name == "security")


def test_security_failure_is_disclosed_and_rendered(monkeypatch):
    monkeypatch.setattr(
        "coding_review.agents.reviewer.enrich_security",
        lambda files: (
            "",
            {"status": "failed", "sources": [], "frameworks": ["OWASP Top 10:2025"]},
        ),
    )

    class Model:
        def with_structured_output(self, schema):
            return self

        def invoke(self, messages):
            return Review(findings=[], limitations=[])

    result = make_reviewer("security", Model())({"files": {"a.py": "pass"}})["results"][0]
    assert result.status == "ok"
    assert any("security review used source context only" in x for x in result.limitations)
    rendered = markdown(
        {
            "status": "complete",
            "coverage_note": "static",
            "counts": {},
            "agents": [result.model_dump()],
            "findings": [],
        }
    )
    assert "Security framework knowledge" in rendered
    assert "OWASP Top 10:2025" in rendered


def test_android_platform_enables_masvs_for_java(monkeypatch):
    monkeypatch.setenv("CODING_REVIEW_PLATFORM", "android")
    client = Search()
    _, metadata = enrich_security({"Note.java": "class Note {}"}, client)
    assert "OWASP MASVS" in metadata["frameworks"]
    assert len(client.queries) == 3
