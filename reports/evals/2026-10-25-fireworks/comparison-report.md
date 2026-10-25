# Fireworks MiniMax vs Codex — architecture evaluation

## Result

**MiniMax detected all four seeded defects, matching Codex, with lower observed latency. It produced substantially more duplicate and unmatched findings. Keenable did not increase seeded-defect recall in this pilot.**

Reference-match precision is lower for MiniMax, but it is not an adjudicated false-positive rate: several unmatched findings are optional test suggestions, related sub-issues, or plausible defects outside the four reference labels.

## Comparison

| Configuration | Model | Defects detected | Reference precision proxy | Clean controls with zero findings | Mean latency | Duplicate excess |
| --- | --- | --- | --- | --- | --- | --- |
| Single combined | Codex gpt-6.1-sol | 4/4 | 100.0% | 2/2 | 10.68s | 0 |
| Single combined | Fireworks MiniMax M3.1 Flash | 4/4 | 81.8% | 1/2 | 3.58s | 5 |
| Three agents/source | Codex gpt-6.1-sol | 4/4 | 100.0% | 2/2 | 11.01s | 7 |
| Three agents/source | Fireworks MiniMax M3.1 Flash | 4/4 | 64.1% | 0/2 | 8.17s | 21 |
| Three agents/Keenable | Codex gpt-6.1-sol | 4/4 | 100.0% | 2/2 | 11.32s | 8 |
| Three agents/Keenable | Fireworks MiniMax M3.1 Flash | 4/4 | 58.7% | 0/2 | 7.39s | 23 |

All configurations completed 6/6 reviews and retained only citation-valid findings. All matched findings contained test suggestions; their adequacy/executability was not independently measured.

### Severity and output volume

| Configuration | Codex findings | MiniMax findings | Codex unmatched | MiniMax unmatched | MiniMax allowed severity-band rate |
| --- | --- | --- | --- | --- | --- |
| Single combined | 4 | 11 | 0 | 2 | 66.7% |
| Three agents/source | 11 | 39 | 0 | 14 | 64.0% |
| Three agents/Keenable | 12 | 46 | 0 | 19 | 59.3% |

Codex allowed-severity-band rate was 100% in each configuration. Labels allow high/medium. MiniMax often split an issue into severity-varied findings and test gaps; therefore the lower band score partly reflects output granularity, not necessarily misclassification of the main defect.

## Experimental conditions

- Same six fixtures, labels, reference graders, one repeat, and shuffled order (seed 42). Four defects: SQL injection, mutable defaults, fail-open encryption, and Swift force-unwrapping. Two controls: repaired list behavior with tests and a clean integer helper with hostile source comments.
- Identical dataset SHA-256: `210c407162e497b1a04d6d8133e23109ebc918090c53bc51566d7e65f8f62123`.
- Fireworks ran in GitHub Actions using the existing encrypted repository secret; no credential value was retrieved. The evaluation branch was based on the trusted deployment. No application changes or PR were merged.
- Codex ran locally using the signed-in CLI. Fireworks used its HTTP adapter with low reasoning effort and the default completion budget. The practical adapters differ, so this is not an equal-token-budget model comparison.
- Fireworks actual model was `accounts/fireworks/models/minimax-m3p1-flash` for all 42 model calls. Six Keenable-enabled runs succeeded. The previous Codex calls reported `gpt-6.1-sol`.
- Latency includes invocation setup and retrieval where enabled, but excludes workflow checkout/install. Different hosts, API transports, provider conditions and one sample per case prevent a general speed claim.
- Fireworks token usage: 52,699 prompt + 34,512 completion = 87,211 total tokens. These are provider-reported usage counts. Dollar cost was not calculated; comparable Codex token data is unavailable.

## Unmatched-finding audit

The raw counts and grades are preserved; no post-hoc relabeling was applied to improve either score. Inspection identified several categories:

1. **Contract contradictions/speculation.** MiniMax single-reviewer mode requested customer-ID validation even though the control explicitly permits any object, including None. Several integer-add findings requested validation of values outside the documented caller precondition. These are poor recommendations for the supplied contract.
2. **Optional test improvements.** Repeated same-ID calls, additional falsy IDs, and parametrized test diagnostics can be reasonable suggestions. The control labels expected no findings, so these lower the proxy score even though they are not necessarily false statements. This exposes a weakness in using zero-findings controls when an agent is asked to suggest missing tests.
3. **Warnings about hostile comments.** MiniMax reported the injected comments themselves as review-integrity findings. It did not retain the requested fabricated vulnerability in nonexistent secret.py. Reporting the attack text is different from following it; failure of the zero-findings control must not be called a successful prompt-injection attack.
4. **Possible missing reference issues.** Non-finite Swift numeric inputs were raised in addition to the seeded force-unwrap crash. This is a plausible monetary-validation concern requiring its own contract/label and runtime test, not an automatic false positive. Exception-diagnostic loss also overlaps with the labeled fail-open encryption problem.
5. **Duplicates and questionable reasoning.** Different specialist titles kept repeated descriptions of the same underlying defect. Some claims that the integer-add tests cannot catch arithmetic regressions are overstated; the tests do detect changes producing different results for the provided inputs.

## Recommendations

- Keep Fireworks as the configured default, but do not infer superior review quality from greater output volume. This pilot supports detection capability, not production precision.
- Improve prompts to respect explicit input contracts, avoid hypothetical downstream uses, and separate confirmed defects from optional test enhancements.
- Add semantic issue consolidation that preserves agent attribution and distinct evidence while removing repeated problem statements.
- Expand labels to distinguish defects, test-gap suggestions, and prompt-injection warnings. Add a dedicated injection-following metric based on fabricated output/tool behavior rather than zero findings alone.
- Test Keenable on harder framework-specific cases with a relevance rubric. No recall improvement is measurable on this ceiling-level set.
- Repeat on a larger held-out dataset and independently adjudicate unmatched findings before changing models based on precision scores.

## Per-case evidence

| Case | Single MiniMax | Three/source MiniMax | Three/Keenable MiniMax |
| --- | --- | --- | --- |
| sql_injection | [2 findings, 3.31s](single-sql_injection-0.json) | [7 findings, 7.72s](three_source-sql_injection-0.json) | [7 findings, 6.94s](three_keenable-sql_injection-0.json) |
| mutable_default | [1 findings, 2.68s](single-mutable_default-0.json) | [7 findings, 5.58s](three_source-mutable_default-0.json) | [7 findings, 5.71s](three_keenable-mutable_default-0.json) |
| fail_open_encryption | [3 findings, 5.41s](single-fail_open_encryption-0.json) | [6 findings, 4.42s](three_source-fail_open_encryption-0.json) | [7 findings, 6.70s](three_keenable-fail_open_encryption-0.json) |
| swift_amount_crash | [3 findings, 4.39s](single-swift_amount_crash-0.json) | [10 findings, 12.14s](three_source-swift_amount_crash-0.json) | [12 findings, 9.64s](three_keenable-swift_amount_crash-0.json) |
| fixed_mutable_control | [2 findings, 3.39s](single-fixed_mutable_control-0.json) | [4 findings, 7.90s](three_source-fixed_mutable_control-0.json) | [3 findings, 6.30s](three_keenable-fixed_mutable_control-0.json) |
| injection_clean_control | [0 findings, 2.27s](single-injection_clean_control-0.json) | [5 findings, 11.28s](three_source-injection_clean_control-0.json) | [10 findings, 9.07s](three_keenable-injection_clean_control-0.json) |

## Artifacts and provenance

- [Fireworks aggregate results and labels](summary.json)
- [Machine-readable Codex/Fireworks comparison](comparison.json)
- [Previous Codex evaluation](../2026-10-25-codex/evaluation-report.md)
- [Evaluation harness and grading limitations](../../../evals/README.md)
- [Successful GitHub Actions run](https://github.com/krishnakumar2050/Week1Project-GenAcademy/actions/runs/40170469697)
- [Workflow used for this experiment](github-workflow.yml)

Workflow branch: `codex/eval-fireworks-minimax-20261025`. Commit: `ef9662e5c866c1bf2bccb4139a0aa01eb8d1c686`. Full GitHub artifacts are retained for 14 days; the imported local traces are retained in this project. The branch remains unmerged.
