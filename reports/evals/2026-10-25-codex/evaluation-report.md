# Multi-agent architecture evaluation — live pilot

## Finding

**All three configurations detected all four seeded defects and passed both clean controls. This pilot shows no measured detection advantage from three specialists or Keenable on these simple cases.** The main observed architecture issue was duplicate output: the multi-agent variants retained 11–12 findings for four distinct issues, compared with four findings from the combined single reviewer.

This is a small smoke benchmark, not a production accuracy estimate or proof that the configurations are equivalent. More difficult, held-out real-world cases and repeated runs are needed.

## Live results

| Metric | Single combined reviewer | Three agents, source only | Three agents + Keenable |
| --- | --- | --- | --- |
| Review runs | 6 | 6 | 6 |
| Completion rate | 100% | 100% | 100% |
| Seeded issues detected | 4/4 | 4/4 | 4/4 |
| Recall proxy | 100% | 100% | 100% |
| Reference precision proxy | 100% | 100% | 100% |
| Clean controls passed | 2/2 | 2/2 | 2/2 |
| Retained citation validity | 100% | 100% | 100% |
| Allowed severity-band rate | 100% | 100% | 100% |
| Test-suggestion presence | 100% | 100% | 100% |
| Retained findings | 4 | 11 | 12 |
| Duplicate findings beyond unique labels | 0 | 7 | 8 |
| Mean latency (seconds) | 10.68 | 11.01 | 11.32 |
| Median latency (seconds) | 10.83 | 11.38 | 11.67 |
| Maximum latency (seconds) | 16.96 | 15.38 | 17.04 |

Single: six model invocations. Each three-agent variant: eighteen model invocations. Total: 42. All 42 reported actual model `gpt-6.1-sol`. Keenable succeeded on all six enabled reviews. No unverified findings were discarded in this pilot.

## Design

- Six independently specified synthetic fixtures: SQL injection, shared mutable defaults, fail-open encryption, Swift force-unwrapped numeric parsing, a repaired function with tests, and clean code containing hostile review instructions.
- Four reference defects total; two controls have no expected findings. Ground-truth labels are not included in prompts.
- Three practical configurations use the same provider and structured schema/citation pipeline. The single reviewer uses one combined specialty; the three-agent variants use the existing LangGraph graph.
- One repeat per case/configuration: 18 end-to-end reviews. Execution order shuffled with seed 42. This controls order only, not model generation.
- Backend: existing signed-in Codex CLI. Results are not a MiniMax/Fireworks benchmark.
- No hosted Evals API or LLM judge was used. Deterministic reference graders run locally. Raw findings were additionally inspected for relevance, concrete failure scenarios, and test suggestions, without an independent adjudicator.
- Dataset SHA-256: `210c407162e497b1a04d6d8133e23109ebc918090c53bc51566d7e65f8f62123`.

## What the measures mean

**Recall proxy:** a reference is detected when a finding overlaps its file/line span and contains at least one reference concept substring. Duplicate findings count only once toward recall.

**Reference precision proxy:** reference-matched findings divided by retained findings. This is a lexical/location approximation; it is not independent semantic grading. Unmatched output would require adjudication before calling it false positive.

**Citation validity:** checked after production citation filtering. It measures retained-output validity, not raw model citation accuracy or correctness of reasoning.

**Test-suggestion presence:** every matched finding supplied a nonempty suggested test. Presence does not prove the test is adequate, compilable, or executable; suggested tests were not run.

**Severity:** all matched findings fell within a broad predeclared high/medium band. Different agents rated the Swift crash differently, so a perfect band score does not establish severity calibration.

**Latency:** end-to-end wall time includes CLI/authentication setup, graph execution, and retrieval when enabled. Mean latency was approximately 3.1% higher for the source-only graph and 6.0% higher for the enriched graph than the single reviewer in this run. These small differences are subject to network/provider noise and cannot establish a stable ordering. No production p95 is inferred from six observations.

**Cost:** billed cost and token usage are unavailable from this adapter and were not measured. Three requests per review are more calls, but are not a monetary-cost measurement.

## Observations and recommended changes

1. **Improve issue consolidation.** Exact file/line/title deduplication retains differently worded findings about the same defect. Duplicate excess was 7/11 (63.6%) for source-only and 8/12 (66.7%) for enrichment. Prefer a validated issue-identity/consolidation layer that retains contributing agents and distinct fixes.
2. **Make the benchmark harder before choosing architecture.** Add independently labeled Android migrations, backup/restore failures, lifecycle problems, cross-file authentication defects, and clean counterparts. Include external BaseNote-style cases where the correct response is uncertainty rather than an invented defect.
3. **Evaluate Keenable relevance separately.** Successful retrieval proves integration availability. This pilot did not demonstrate quality lift. Test framework-specific anti-patterns, outdated/irrelevant sources, hostile snippets, no results, and timeouts; measure grounding and latency alongside recall.
4. **Grade test quality, not just presence.** Score setup/input/assertion specificity against labels, then compile or run generated tests in an isolated environment where practical.
5. **Repeat and independently adjudicate.** Run at least several repeats across a larger held-out set. Review disagreement and unmatched findings with an independent reviewer; report confidence intervals and task/language slices.
6. **Add release gates only after calibration.** Completion, citation-filter integrity, clean-control behavior, and severity agreement can become gates once the dataset and graders reflect production risk. A 100% score on four simple defects is insufficient.

## Per-case trace index

| Case | Single | Three/source | Three/Keenable |
| --- | --- | --- | --- |
| sql_injection | [1 findings; 16.96s](single-sql_injection-0.json) | [2 findings; 13.05s](three_source-sql_injection-0.json) | [3 findings; 11.82s](three_keenable-sql_injection-0.json) |
| mutable_default | [1 findings; 13.26s](single-mutable_default-0.json) | [3 findings; 15.38s](three_source-mutable_default-0.json) | [3 findings; 17.04s](three_keenable-mutable_default-0.json) |
| fail_open_encryption | [1 findings; 8.64s](single-fail_open_encryption-0.json) | [3 findings; 11.27s](three_source-fail_open_encryption-0.json) | [3 findings; 11.53s](three_keenable-fail_open_encryption-0.json) |
| swift_amount_crash | [1 findings; 13.02s](single-swift_amount_crash-0.json) | [3 findings; 11.50s](three_source-swift_amount_crash-0.json) | [3 findings; 11.93s](three_keenable-swift_amount_crash-0.json) |
| fixed_mutable_control | [0 findings; 7.07s](single-fixed_mutable_control-0.json) | [0 findings; 7.68s](three_source-fixed_mutable_control-0.json) | [0 findings; 8.47s](three_keenable-fixed_mutable_control-0.json) |
| injection_clean_control | [0 findings; 5.11s](single-injection_clean_control-0.json) | [0 findings; 7.19s](three_source-injection_clean_control-0.json) | [0 findings; 7.15s](three_keenable-injection_clean_control-0.json) |

## Reproduce and extend

From the coding-agent project root:

```bash
.venv313/bin/python -m evals.run \
  --output reports/evals/repeated-benchmark \
  --backend codex \
  --codex-executable "/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex" \
  --repeats 3
```

Use a new output directory for each experiment. Three repeats request 54 reviews and 126 model invocations. To benchmark MiniMax, select `--backend fireworks` with Fireworks credentials in the invoking process.

The project regression suite passes **139 tests**, including checks of the eval grader. Those offline tests verify behavior and failure handling; they are not the live accuracy benchmark.

- [Machine-readable summary and labels](summary.json)
- [Harness and methodology](../../../evals/README.md)
- [Official evaluation-design reference](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
