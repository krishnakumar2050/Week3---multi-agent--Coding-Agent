"""Knowledge enrichment boundaries and failure behavior."""

from types import SimpleNamespace

from coding_review.agents.knowledge import enrich_quality
from coding_review.agents.reviewer import make_reviewer
from coding_review.domain import Review


class Search:
    def __init__(self):
        self.queries = []

    def search(self, query):
        self.queries.append(query)
        return [
            SimpleNamespace(title="Guidance", url="https://docs.python.org/3/", snippet="x" * 4000)
        ]


def test_disabled_does_not_search(monkeypatch):
    monkeypatch.delenv("KEENABLE_ENABLED", raising=False)
    client = Search()
    context, metadata = enrich_quality({"a.py": "secret"}, client)
    assert not context and metadata["status"] == "disabled"
    assert not client.queries


def test_bounded_generic_queries(monkeypatch):
    monkeypatch.setenv("KEENABLE_ENABLED", "true")
    client = Search()
    context, metadata = enrich_quality({"private_name.py": "secret", "a.ts": "secret"}, client)
    assert metadata["status"] == "ok"
    assert len(client.queries) == 2
    assert all("secret" not in q and "private_name" not in q for q in client.queries)
    assert all(len(s["snippet"]) == 1200 for s in metadata["sources"])
    assert "UNTRUSTED" in context and "exact repository citation" in context


def test_search_failure_redacts_provider_message(monkeypatch):
    monkeypatch.setenv("KEENABLE_ENABLED", "1")

    class Broken:
        def search(self, query):
            raise RuntimeError("secret-token")

    context, metadata = enrich_quality({"a.py": "x"}, Broken())
    assert not context and metadata["status"] == "failed"
    assert "secret-token" not in str(metadata)


def test_bad_urls_and_result_budget(monkeypatch):
    monkeypatch.setenv("KEENABLE_ENABLED", "yes")

    class Many:
        def search(self, query):
            return [
                SimpleNamespace(title="t", url=u, snippet="s")
                for u in ["javascript:alert(1)", "https://user:pass@example.com/"]
                + ["https://docs.python.org/3/"] * 20
            ]

    _, metadata = enrich_quality({"a.py": "x"}, Many())
    assert len(metadata["sources"]) == 6


def test_only_quality_receives_enrichment(monkeypatch):
    calls = []

    def enrich(files):
        calls.append(files)
        return "EXTERNAL_GUIDANCE", {"status": "ok", "sources": []}

    monkeypatch.setattr("coding_review.agents.reviewer.enrich_quality", enrich)

    class Model:
        def with_structured_output(self, schema):
            return self

        def invoke(self, messages):
            self.messages = messages
            return Review(findings=[], limitations=[])

    for name in ("quality", "security", "tests"):
        model = Model()
        result = make_reviewer(name, model)({"files": {"a.py": "pass"}})["results"][0]
        assert result.status == "ok"
        assert ("EXTERNAL_GUIDANCE" in model.messages[1][1]) == (name == "quality")
    assert len(calls) == 1


def test_swift_language_query(monkeypatch):
    monkeypatch.setenv("KEENABLE_ENABLED", "true")
    client = Search()
    _, metadata = enrich_quality({"App.swift": "import UIKit"}, client)
    assert metadata["status"] == "ok"
    assert len(client.queries) == 1 and client.queries[0].startswith("Swift ")
