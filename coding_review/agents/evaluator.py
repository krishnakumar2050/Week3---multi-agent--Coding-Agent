"""Post-aggregation judge; failures remain visible without discarding the review."""

import hashlib
import json
from time import monotonic
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from coding_review.agents.context import source_prompt
from coding_review.agents.evaluation_prompt import PROMPT_VERSION, SYSTEM_PROMPT
from coding_review.domain import State
from coding_review.errors import diagnose


class CriteriaScores(BaseModel):
    model_config = ConfigDict(extra="forbid")
    bug_accuracy: int = Field(strict=True, ge=1, le=5)
    security: int = Field(strict=True, ge=1, le=5)
    actionability: int = Field(strict=True, ge=1, le=5)
    false_positives: int = Field(strict=True, ge=1, le=5)


class Evaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reasoning: str = Field(min_length=1)
    criteria_scores: CriteriaScores
    overall_verdict: Literal["PASS", "NEEDS_REVISION", "FAIL"]
    summary: str = Field(min_length=1)

    @model_validator(mode="after")
    def consistent_assessment(self):
        if not all(f"Step {n}" in self.reasoning for n in (1, 2, 3)):
            raise ValueError("Evaluation requires all three evidence-summary sections")
        if self.overall_verdict == "PASS" and min(self.criteria_scores.model_dump().values()) < 4:
            raise ValueError("PASS requires every score to be at least four")
        return self


def make_evaluator(model, context=None):
    def evaluate(state: State):
        started = monotonic()
        report = dict(state["report"])
        runner = None
        execution = {
            "status": "failed",
            "prompt_version": PROMPT_VERSION,
            "prompt_sha256": hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest(),
            "assessment_note": "Model-judged assessment, not measured precision/recall or proof of security.",
        }
        try:
            runner = model.with_structured_output(Evaluation)
            answer = runner.invoke(
                [
                    ("system", SYSTEM_PROMPT),
                    (
                        "human",
                        source_prompt(state["files"])
                        + "\nUNTRUSTED_EVALUATION_INPUT_JSON:\n"
                        + json.dumps(
                            {
                                "context": context
                                or {
                                    "limitations": [
                                        "No PR diff or requirements provided; assess provisionally."
                                    ]
                                },
                                "review": report,
                            },
                            ensure_ascii=False,
                        ),
                    ),
                ]
            )
            result = Evaluation.model_validate(answer)
            report["evaluation"] = result.model_dump()
            execution["status"] = "ok"
        except Exception as exc:
            execution["error"] = diagnose(
                exc, "evaluate_review", backend=getattr(model, "backend_name", "openai")
            )
        if execution.get("error", {}).get("validation_errors"):
            execution["error"]["hint"] = (
                "Model response does not match the Evaluation schema; check structured-output support."
            )
        execution.update(dict(getattr(runner, "execution_metadata", {})))
        execution["duration_seconds"] = round(monotonic() - started, 3)
        report["evaluation_execution"] = execution
        return {"report": report}

    return evaluate
