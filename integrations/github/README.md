# Install automated multi-agent pull-request review

This integration runs the same three LangGraph specialists with MiniMax M3.1 Flash on Fireworks. The workflow reviews complete contents of changed supported-source files at the immutable PR head. It does not review unchanged or deleted files. Issues outside changed lines within those files can therefore appear in a PR report.

## Activation

1. Merge the integration pull request containing `.github/workflows/ai-code-review.yml` and the review engine under `.github/coding-review/`.
2. In the target repository, open **Settings → Secrets and variables → Actions → New repository secret**. Add `FIREWORKS_API_KEY` with your Fireworks key. Do not commit the key.
3. Open a same-repository pull request, push a new commit to one, reopen it, or mark a draft ready for review.

Because pull_request_target uses the trusted base workflow, the initial installation PR may not run this job at all. It activates after the workflow and engine reach the default branch. A missing Fireworks key produces an actionable Actions error; it does not fall back to another provider or claim a successful review.

The workflow also accepts `CODINGAGENT` as a repository-secret alias. `FIREWORKS_API_KEY` takes precedence. Secret values are never committed or displayed.

## Results

- **Multi-agent AI code review** appears in the PR's checks.
- One marked bot comment contains the prioritized report and is updated on new pushes.
- The Actions run retains full Markdown and JSON report artifacts for 14 days.
- Every report records the reviewed commit, source hash, per-agent results, and runtime model when returned by the provider.
- The job fails on an incomplete review; severity findings are advisory and do not by themselves fail the check.
- A 300,000-byte changed-source budget limits inference cost. Oversized snapshots fail explicitly; adjust the trusted integration entry point before enabling on a larger repository.

## Trust boundaries

The workflow uses `pull_request_target`, skips fork and Dependabot PRs, and uses a trusted default-branch checkout. The installed engine and dependency manifest come from the current trusted default branch, so adapter fixes apply to existing PRs too. Source at the PR head is retrieved as immutable GitHub blob data through the API; the integration never checks out, imports, installs dependencies from, or runs tests from PR code. The review backend has no tool loop.

The Fireworks key is scoped to the inference step. `GITHUB_TOKEN` receives `contents: read` and `pull-requests: write` for source retrieval and report publication. Only a marked comment belonging to `github-actions[bot]` can be replaced. Stale commit reports are not posted. User/model content is HTML-escaped and mention syntax is escaped before publication.

The pull_request_target workflow itself and its engine execute from the trusted base/default branch. PR workflow edits do not execute with review secrets. Protect the default branch and review changes under `.github/` as part of repository governance. This integration does not configure branch protection, GitHub account-wide hooks, or fork review approvals.

Fireworks API usage is billed to the Fireworks account. GitHub Actions usage and repository workflow policies also apply. The integration does not use ChatGPT Pro authentication in CI.

## Reuse in another repository

Copy the trusted review package, its `pyproject.toml` and README under `.github/coding-review/`, then copy the workflow into `.github/workflows/`. Add a Fireworks secret in each repository. The engine is deliberately vendored so a public repository need not fetch a private coding-agent repository using a long-lived token. Updates to the central local project must be explicitly copied into the installed engine.

## Android deployment

`CODING_REVIEW_PLATFORM=android` enables MASVS guidance for Java-only changes as
well as Kotlin. Quality and security Keenable enrichment are both enabled. The
optional `KEENABLE_API_KEY` repository secret is passed only to review. Set the
repository Actions variable `FIREWORKS_MODEL` to override the MiniMax default.
Docs-only and deletion-only PRs produce a skipped report without model calls.
Missing secrets and oversized changed snapshots fail explicitly. Tests are never
executed from PR contents. Concurrent runs on the same PR supersede older runs.

For a full repository audit, use the CLI's `--scope full` explicitly; the Python
`run_review` API keeps its previous full-snapshot default for compatibility.

## Performance judge on every PR review

A post-aggregation evaluator automatically scores each eligible source review.
The bot comment includes its verdict and four 1–5 scores; the Actions artifact
also includes exact-schema `evaluation.json` and provenance/status in
`evaluation-status.json`. `FIREWORKS_EVALUATOR_MODEL` is an optional repository
Actions variable; absent it, the reviewer model is reused in a separate request.
Verdicts are advisory. Invalid/failed judge output fails the workflow while
preserving the review. PRs without supported source skip both inference stages.
The prompt is versioned with a recorded hash; results remain model judgments.
