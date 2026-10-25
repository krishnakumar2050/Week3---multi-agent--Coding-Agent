# Coding-review architecture evaluations

This harness compares three configurations on the same labeled fixtures:

- `single`: one combined correctness/security/test-gap request, with the same
  structured-output and source-citation pipeline.
- `three_source`: the existing three-node LangGraph workflow, without retrieval.
- `three_keenable`: the same graph with Keenable enabled for Agent 1.

## Run

From the project root:

```bash
export FIREWORKS_API_KEY='your-fireworks-key'
.venv313/bin/python -m evals.run \
  --output reports/evals/my-run \
  --repeats 3
```

All inference entry points default to Fireworks AI with MiniMax M3.1 Flash
(`accounts/fireworks/models/minimax-m3p1-flash`): CLI reviews, Python service
configuration, single-reviewer evals, three-agent evals, and GitHub PR reviews.
The model precedence is `--model`, then `FIREWORKS_MODEL`, then the bundled default.
Credentials are supplied through `FIREWORKS_API_KEY`; they are never bundled in code.
Keenable remains a context-search provider, not an inference backend.

Codex and OpenAI remain explicit alternatives through `--backend codex` and
`--backend openai`. A missing Fireworks key causes an error without switching
providers. Do not reuse an output directory: per-case files and summary are
replaced. No fake backend is used for live results. Historical Codex pilot results
remain labeled as Codex and are not Fireworks performance measurements.

Six cases contain four labeled defects and two clean controls: SQL injection,
shared mutable defaults, fail-open encryption, Swift numeric force-unwrapping,
a repaired list function with tests, and clean code containing hostile review
instructions in comments. Labels are never sent to the model. Fixtures are static
text and are not executed.

One repeat produces 18 review runs and 42 model invocations: six combined requests
plus eighteen specialist requests for each three-agent variant. Execution order
is shuffled with a recorded fixed seed of 42 in the runner. Models may remain
nondeterministic; the seed controls ordering, not generation. Keenable results
may change over time and retained snippets are recorded in agent metadata.

## Measures

- **Recall proxy:** distinct expected issues detected / expected issues.
- **Reference precision proxy:** findings matching a reference / retained findings.
- **Clean controls:** controls producing zero retained findings.
- **Citation validity:** exact source evidence after production validation.
- **Severity acceptance:** matched findings rated in the label's allowed band.
- **Test suggestion presence:** matched findings containing a nonempty suggestion.
- **Semantic duplicate excess:** matched findings minus distinct matched labels.
- **Completion:** successful reviews / attempted reviews.
- **Latency:** mean, median, and maximum end-to-end seconds per case, including
  authentication/CLI startup and retrieval where enabled.

Matching requires the expected file, overlapping source/evidence line span, and
at least one case-specific concept substring in the title, explanation, or fix.
This is a transparent automated approximation, not a semantic correctness oracle.
Unmatched findings need adjudication before being called false positives. Duplicate
matches increase precision counts but not recall. Empty denominators are reported
as null, not perfect scores. Incomplete runs remain in recall/completion denominators.

Citation validity is measured after the production filter, so it is a pipeline
invariant, not raw model citation accuracy. A valid quote does not prove reasoning
correctness. Suggestion presence does not measure test adequacy or executability.
Allowed severity bands do not establish calibrated severity accuracy.

The single reviewer uses the same provider and schema but a combined specialty;
this compares practical configurations, not a controlled equal-token-budget study.
No billed cost or usage tokens are available from this Codex adapter, so cost is
not inferred from subscription pricing or request counts. Small-sample latency
maximum is reported instead of a misleading production p95.

## Artifacts and interpretation

Every run writes per-case JSON with the full report and grades, followed by
`summary.json` containing the dataset, its SHA-256, aggregates, and limitations.
The `2026-10-25-codex` directory contains the initial live pilot.

This small synthetic set is a smoke benchmark, not a production acceptance suite.
Use repeated runs, larger independently labeled Android/Swift/Python examples,
held-out real defects and clean files, and independent review of findings before
claiming architecture superiority. Add prompt-injection variants, retrieval
failure/relevance cases, migration/backup scenarios, and realistic context sizes.
Provider failures and exact source-citation boundaries are also covered by the
project's offline regression tests; those tests do not estimate live accuracy.

The design follows the principle of task-specific datasets, explicit metrics,
and reviewed graders described in [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices).
It runs locally and does not depend on the hosted Evals API.
