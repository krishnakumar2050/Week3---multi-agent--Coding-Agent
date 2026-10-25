"""Citation regression cases, including the PR #2 eval smoke fixture."""

import json

import pytest
from pydantic import ValidationError

from coding_review.agents.context import source_prompt
from coding_review.agents.evidence import resolve_evidence, verify_evidence
from coding_review.domain import Finding, Review
from coding_review.graph import build_graph

SOURCE = '''"""Intentionally defective review fixture, not used by the application."""


def calculate_user_expression(expression):
    """Evaluate a caller-supplied arithmetic expression."""
    return eval(expression)


def average_customer_balance(balances):
    """Return the average customer balance."""
    return sum(balances) / len(balances)
'''
PATH = "review_smoke_test_fixture.py"


def finding(line=6, evidence="    return eval(expression)", path=PATH):
    return Finding(
        severity="high",
        title="Unsafe eval",
        file=path,
        line=line,
        evidence=evidence,
        explanation="Caller input can execute code.",
        recommendation="Use an arithmetic parser.",
        suggested_test="Reject imports and calls.",
    )


def test_prompt_supplies_real_coordinates_and_exact_indentation():
    prompt = source_prompt({PATH: SOURCE})
    data = json.loads(prompt.split("SOURCE_LINES_JSON:\n", 1)[1])
    assert data[PATH][5] == {"line": 6, "text": "    return eval(expression)"}
    assert data[PATH][1] == {"line": 2, "text": ""}
    assert "never estimate" in prompt


@pytest.mark.parametrize(
    "line,evidence,method",
    [
        (6, "    return eval(expression)", "exact"),
        (99, "    return eval(expression)", "relocated_exact"),
        (99, "return eval(expression)", "normalized_indentation"),
    ],
)
def test_eval_citation_is_recovered_from_unique_source(line, evidence, method):
    original = finding(line=line, evidence=evidence)
    corrected, actual_method = resolve_evidence(original, {PATH: SOURCE})
    assert actual_method == method
    assert corrected.line == 6
    assert corrected.evidence == "    return eval(expression)"
    assert verify_evidence(corrected, {PATH: SOURCE})
    assert original.line == line  # No mutation of the model's original finding.


def test_multiline_common_margin_can_be_recovered():
    quote = 'def calculate_user_expression(expression):\n    """Evaluate a caller-supplied arithmetic expression."""\n    return eval(expression)'
    corrected, method = resolve_evidence(finding(99, quote), {PATH: SOURCE})
    assert corrected.line == 4
    assert verify_evidence(corrected, {PATH: SOURCE})


@pytest.mark.parametrize("evidence", ["eval(other_input)", "return exec(expression)", "", "  "])
def test_fabricated_or_empty_quotes_are_rejected(evidence):
    if not evidence:
        with pytest.raises(ValidationError):
            finding(99, evidence)
        return
    assert resolve_evidence(finding(99, evidence), {PATH: SOURCE})[0] is None


def test_wrong_file_is_not_resolved_by_searching_another_file():
    assert resolve_evidence(finding(path="wrong.py"), {PATH: SOURCE})[0] is None


def test_ambiguous_quotes_are_rejected_when_location_is_wrong():
    duplicated = SOURCE + SOURCE
    assert resolve_evidence(finding(99), {PATH: duplicated})[0] is None
    assert resolve_evidence(finding(99, "return eval(expression)"), {PATH: duplicated})[0] is None
    assert resolve_evidence(finding(6), {PATH: duplicated})[1] == "exact"


def test_literal_whitespace_and_relative_indentation_are_not_rewritten():
    code = 'def example():\n    return "a b"\n'
    assert resolve_evidence(finding(99, 'return "ab"'), {PATH: code})[0] is None
    malformed = 'def example():\nreturn "a b"'
    assert resolve_evidence(finding(99, malformed), {PATH: code})[0] is None


def test_graph_preserves_eval_finding_and_audits_corrections():
    class Model:
        def with_structured_output(self, schema):
            return self

        def invoke(self, messages):
            return Review(findings=[finding(99, "return eval(expression)")], limitations=[])

    report = build_graph(Model()).invoke({"files": {PATH: SOURCE}, "results": []})["report"]
    assert report["status"] == "complete"
    assert report["findings"][0]["line"] == 6
    assert report["findings"][0]["agents"] == ["quality", "security", "tests"]
    assert all(
        a["execution"]["citation_corrections"][0]["original_line"] == 99 for a in report["agents"]
    )
