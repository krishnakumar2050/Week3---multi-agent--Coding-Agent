# Omni-Notes sample PR evaluation

PR: https://github.com/krishnakumar2050/Omni-Notes-sample/pull/1

Reviewed head: `008d504115cd81d91774948003004b2c37f20f8e`

## Outcome

All three specialist agents completed, using Fireworks `accounts/fireworks/models/minimax-m3p1-flash`. Elapsed workflow time: 11.158 seconds. Both independently reproduced seeded defects were detected by all three specialists: path traversal at NoteExportPreview.java:19 and empty-list division by zero at line 29. Each agent proposed regression tests for both.

This is an isolated fixture in the Android repository, not a vulnerability assessment of the shipping Android application. The fixture is outside Android source sets and is not called by the app. Only the exact PR-head Java files were sent to the reviewers; the ground-truth README and PR description were excluded. The run used the current local application, not GitHub Actions. No multi-agent workflow is installed on the repository default branch, and no Actions runs were observed for this head.

## Measurements

| Check | Observed result |
| --- | --- |
| Seeded defect detection | 2/2 cases; tiny sample, not general recall |
| Specialist completion | 3/3 |
| Retained findings | 13 |
| Exact source citations | 13/13; proves source location, not reasoning correctness |
| Model severity counts | 1 critical, 2 high, 5 medium, 4 low, 1 info; uncalibrated |
| Quality Keenable retrieval | Successful |
| Security Keenable retrieval | Successful; four official sources across two queries |
| Test-gap web retrieval | None, by design |
| Workflow latency | 11.158 seconds |
| Semantic duplicates | Six findings describe the two seeded defects; four excess copies within those groups |
| Aggregator shared-finding count | 0, despite the cross-agent semantic overlap |

## Independent validation

The exact PR-head Java sources compiled using the installed Java 8 JDK. Three happy-path checks passed. The separate FixtureProbe.java reproduced path traversal using synthetic temporary files and reproduced ArithmeticException for an empty note list. These checks were executed by the evaluation harness after review; the specialist agents themselves performed static analysis only. No Android build or instrumentation suite was run.

## Performance gaps

1. **Semantic aggregation:** exact-title deduplication retains three versions of each seeded issue. The synthesis prioritizes repeated reports rather than distinct root causes.
2. **Severity and reachability:** the quality reviewer labeled fixture traversal critical. No production caller or exported Android component is connected, so catastrophic shipping impact is not established. Security language claiming attacker exfiltration exceeds the supplied call-site evidence, despite limitations elsewhere.
3. **Framework validation:** the security reviewer called A04:2025 Insecure Design, but the official 2025 list identifies A04 as Cryptographic Failures and A06 as Insecure Design. Its limitation also conflated A06 with dependencies; Software Supply Chain Failures is A03. Retrieved guidance did not prevent these identifier errors. See https://top10.owasp.org/2025/ .
4. **Android context detection:** the two Java files did not trigger MASVS retrieval because the current mobile heuristic recognizes Swift/Kotlin extensions, not Java Android paths. It retrieved OWASP/CWE guidance only.
5. **Unsupported claims:** the test reviewer reported integer truncation using a 6/2 example that is exactly 3, and returned contradictory claims about JVM exit status for uncaught AssertionError. These should be rejected or corrected before presenting the report as actionable defects.
6. **Precision remains unmeasured:** null-input contracts, generic missing tests, and alleged error-message disclosure require adjudication. Findings beyond the two seeded cases are not automatically false positives, and no overall precision score is claimed.

## Recommended next work

Add semantic issue grouping with preserved provenance, validate framework identifiers against a pinned taxonomy, carry platform metadata for Android Java, calibrate severity to demonstrated reachability, and introduce fixed controls plus repeated runs before comparing model quality. Keep exact-citation checks, but do not equate them with factual correctness.

## Artifacts

- [Raw review](review-report.md)
- [Structured review and provenance](review-report.json)
- [Machine-readable evaluation summary](evaluation-summary.json)
- [Reviewed source](NoteExportPreview.java)
- [Happy-path checks](NoteExportPreviewTest.java)
- [Independent probe](FixtureProbe.java)
