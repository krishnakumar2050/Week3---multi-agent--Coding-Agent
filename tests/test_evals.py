"""Reference graders must expose misses, duplicates, and unmatched findings."""

from evals.dataset import CASES
from evals.scoring import aggregate, score


def finding(**overrides):
    item = {
        "file": "app.py",
        "line": 1,
        "severity": "medium",
        "title": "Shared mutable default",
        "evidence": "def record_customer(customer_id, customer_ids=[]):",
        "explanation": "A shared default leaks state across calls.",
        "recommendation": "Use a fresh list.",
        "suggested_test": "Call twice; assert independent lists.",
    }
    item.update(overrides)
    return item


def report(findings, status="complete"):
    return {"findings": findings, "status": status, "duration_seconds": 1.0}


def test_grader_scores_duplicates_and_misses():
    case = next(c for c in CASES if c["id"] == "mutable_default")
    result = score(case, report([finding(), finding()]))
    assert result["detected"] == 1 and result["matched"] == 2
    assert result["semantic_duplicate_excess"] == 1
    assert result["valid_citations"] == 2
    missing = score(case, report([], "incomplete"))
    assert missing["detected"] == 0 and not missing["complete"]
    combined = aggregate([result, missing])
    assert combined["recall_proxy"] == 0.5 and combined["completion_rate"] == 0.5


def test_grader_rejects_wrong_file_or_wrong_concept():
    case = next(c for c in CASES if c["id"] == "mutable_default")
    bad = finding(file="absent.py")
    result = score(case, report([bad]))
    assert result["matched"] == 0 and result["valid_citations"] == 0
    result = score(
        case, report([finding(title="Style", explanation="Rename", recommendation="Shorten")])
    )
    assert result["matched"] == 0


def test_clean_controls_do_not_claim_vacuous_precision():
    case = next(c for c in CASES if not c["expected"])
    result = score(case, report([]))
    summary = aggregate([result])
    assert summary["reference_precision_proxy"] is None
    assert summary["citation_validity"] is None
    assert summary["clean_controls_passed"] == 1
    assert score(case, report([finding()]))["clean_control_pass"] is False


def test_dataset_labels_reference_real_lines():
    for case in CASES:
        for label in case["expected"]:
            assert label["start"] >= 1
            assert label["end"] <= len(case["files"][label["file"]].splitlines())


def test_all_entry_points_default_to_fireworks():
    from coding_review.cli import build_parser as review_parser
    from coding_review.config import DEFAULT_BACKEND, ReviewConfig
    from evals.run import build_parser as eval_parser

    assert DEFAULT_BACKEND == "fireworks"
    assert ReviewConfig().backend == "fireworks"
    assert review_parser().parse_args(["examples"]).backend == "fireworks"
    assert eval_parser().parse_args(["--output", "results"]).backend == "fireworks"
    assert (
        eval_parser().parse_args(["--output", "results", "--backend", "codex"]).backend == "codex"
    )
