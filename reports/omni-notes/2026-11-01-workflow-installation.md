# Omni-Notes automatic review installation

Repository: https://github.com/krishnakumar2050/Omni-Notes-sample

Integration PR #2 was merged into develop: https://github.com/krishnakumar2050/Omni-Notes-sample/pull/2

Deployment commit: `6892b4f8f45c5313a80982c22b1daf9538f860ef`.

## Live verification

Verification PR: https://github.com/krishnakumar2050/Omni-Notes-sample/pull/3

The PR-opened event automatically started the multi-agent workflow:
https://github.com/krishnakumar2050/Omni-Notes-sample/actions/runs/41302286673

Trusted checkout, Python setup, and vendored engine installation succeeded.
The inference step failed because neither FIREWORKS_API_KEY nor CODINGAGENT was
available as a repository Actions secret. No agent calls or model findings were
produced by this Actions run. Add FIREWORKS_API_KEY at repository Settings >
Secrets and variables > Actions, then rerun the failed job. The value itself is
not stored in this project or report. macOS Keychain is not accessible from CI.

## Behavior

Opening, updating, reopening, and marking same-repository PRs ready triggers
three parallel Fireworks specialists and an aggregator. Draft, fork, and
Dependabot PRs are skipped. PR source is fetched as immutable blobs and never
executed. The workflow and engine run from trusted default-branch code under
pull_request_target. It reviews complete changed supported files, omitting
unchanged/deleted files, with a 300,000-byte budget. No-supported-source PRs are
reported as skipped. Stale results are not published. Successful/partial runs
with reports publish a bot comment and retain Markdown/JSON artifacts for 14 days.
Keenable enrichment is enabled for quality and security; an Android platform hint
enables MASVS guidance for Java-only changes. Optional KEENABLE_API_KEY secret
and FIREWORKS_MODEL Actions variable are supported.

## Validation

163 tests passed with external searches disabled; lint and diff checks passed.
Added checks cover changed-file filtering, head races, pagination limits,
no-source skips, report scope, and Android Java MASVS context. The earlier
sample PR #1 was already closed before installation and was not reopened.
