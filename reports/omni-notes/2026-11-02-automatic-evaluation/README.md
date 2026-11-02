# Automatic PR review performance evaluation

Deployed through [PR #4](https://github.com/krishnakumar2050/Omni-Notes-sample/pull/4), merged into develop at 7bb06f73b6453f7591b2d68cf350c19912faec05.

Verified on [PR #5](https://github.com/krishnakumar2050/Omni-Notes-sample/pull/5).
The [Actions run](https://github.com/krishnakumar2050/Omni-Notes-sample/actions/runs/41431869766) succeeded, including review, evaluation, bot-comment publication, and artifact upload.

[Published assessment](https://github.com/krishnakumar2050/Omni-Notes-sample/pull/5#issuecomment-6575279663): NEEDS_REVISION.
Scores: bug accuracy 3/5, security 5/5, actionability 3/5, false positives 3/5.
The judge flagged severity inflation and an unsupported overflow claim. These are model judgments, not independently measured quality metrics.

## Architecture

Source snapshot -> parallel quality/security/test-gap agents -> aggregator -> performance evaluator -> Markdown/JSON reports and PR comment.

The judge uses the versioned system prompt in coding_review/agents/evaluation_prompt.py and the exact requested four-key schema. All eligible source PR reviews enable it; no-source PRs explicitly skip. Execution failure preserves the review and fails the workflow. Verdicts remain advisory. Set FIREWORKS_EVALUATOR_MODEL as an Actions variable to choose another judge model; absent it, a separate request reuses the reviewer model.

## Saved artifacts

- [Exact-schema judgment](evaluation.json)
- [Judge execution/provenance](evaluation-status.json)
- [Full report](report.md)
- [Structured report](report.json)

All four files were downloaded from the successful Actions artifact. The exact judgment schema, execution status, report/judgment equality, and reviewed commit were validated locally. The local suite passed 176 tests; lint and diff checks passed.
