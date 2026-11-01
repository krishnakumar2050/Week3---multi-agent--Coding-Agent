"""Fan-in agent: synthesize verified specialist outputs without another provider call."""

from coding_review.agents.prompts import SPECIALTIES
from coding_review.domain import State
from coding_review.reporting.aggregation import orchestrate


def aggregate_results(state: State):
    """Run after the join barrier and preserve the full specialist audit trail."""
    update = orchestrate(state)
    report = update["report"]
    results = state["results"]
    completed = sorted({r.agent for r in results if r.status == "ok"})
    missing = sorted(set(SPECIALTIES) - {r.agent for r in results})
    failed = sorted({r.agent for r in results if r.status == "failed"})
    findings = report["findings"]
    priorities = [
        {
            "file": finding["file"],
            "line": finding["line"],
            "title": finding["title"],
            "severity": finding["severity"],
            "recommendation": finding["recommendation"],
            "agents": finding["agents"],
        }
        for finding in findings[:5]
    ]
    summary = (
        f"{len(completed)}/{len(SPECIALTIES)} specialists succeeded; "
        f"{len(findings)} verified finding(s)."
    )
    if findings:
        summary += f" Highest reported severity: {findings[0]['severity']}."
    if report["status"] != "complete":
        summary += " Review is incomplete; resolve review gaps before relying on the results."
    report["synthesis"] = {
        "summary": summary,
        "priorities": priorities,
        "shared_findings": sum(len(f["agents"]) > 1 for f in findings),
        "completed_agents": completed,
        "failed_agents": failed,
        "missing_agents": missing,
        "limitations": sorted({item for r in results for item in r.limitations}),
    }
    return update
