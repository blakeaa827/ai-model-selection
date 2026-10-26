# Contributing

Questions, bug reports, feature requests and benchmark or routing corrections are welcome.

## Open an issue

Use the [issue chooser](https://github.com/blakeaa827/ai-model-selection/issues/new/choose) to select a bug report, feature request or data correction. Use a blank issue for general questions.

For a bug, include the report date or commit, the command or request configuration, expected behavior, actual behavior and a minimal reproduction. Remove credentials and private inputs from logs.

For model or benchmark corrections, include original source URLs, the exact model revision and reasoning setting, benchmark methodology/version, score and measured weighted task cost. Clearly distinguish an estimate, provider claim, token rate, provisional cost or different evaluation harness from a comparable measured configuration.

## Propose changes

1. Fork the repository and make a focused change on a branch.
2. Keep related report, schema and selector changes consistent.
3. Run `node test-selector.mjs` when changing selection or request construction. Add a focused regression case for a demonstrated bug.
4. Open a pull request explaining the behavior changed, evidence and verification.

The maintained report entry point is `node pipeline/refresh.mjs`. It fetches public benchmark and route metadata and stages validated files under `run-artifacts/report/`; it makes no paid model-generation call. Publishing is reserved for authorized maintainers and the existing workflow.

## Keep evidence and routing exact

- Never infer a model's benchmark score from its family, a different revision, an app mode or an effort label alone.
- Never replace measured AA task cost with a provider's token price.
- Keep estimated scores, provisional costs and unverified routes out of actionable selection.
- Preserve the paid frontier and the explicit-opt-in limited-free lane.
- Preserve historical snapshots and source precision. Refresh a common methodology version before comparing results.
- Reject stale or mismatched requests; do not silently substitute a different provider or configuration.
- Treat subscription recommendations separately from API costs and benchmarks.

## Credentials and private data

Do not include API keys, passwords, tokens, authorization headers, account data or private prompts in issues, pull requests or files. Public benchmark evidence and a synthetic reproduction are sufficient for most reports.

Third-party benchmark data and model materials remain subject to their original sources' terms; source attribution does not transfer ownership.
