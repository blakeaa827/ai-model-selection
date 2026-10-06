# AI model selection

Daily capability-versus-cost guidance for tools calling OpenRouter. The report covers the requested OpenAI, Anthropic, xAI and Google families. It does not claim to rank the entire OpenRouter market.

## Stable files

- `latest.json`: machine-readable frontier, default floor, higher ceiling, exact callable IDs, supported effort settings, timestamps, sources and caveats.
- `latest.md`: readable progressive chart, including exact OpenRouter IDs.
- `snapshots/YYYY-MM-DD.json`: dated history; never silently rewrite history.
- `schema.json`: JSON Schema contract (version 1.0.0).
- `select-model.mjs`: dependency-free Node.js 22+ selector and live catalog check; it returns a request skeleton and never makes a paid inference call.

## Recommendation checked October 6, 2026

Default floor: `openai/gpt-6.1-sol`, `reasoning.effort: medium`, score 48, benchmark cost $0.21.

Ceiling before the sharp cost cliff: same model, `reasoning.effort: xhigh`, score 51, benchmark cost $0.39. Ceiling is advice, not a hard cap; a higher minimum score still selects the eligible row that meets it.

## Consume the data

Repository: [blakeaa827/ai-model-selection](https://github.com/blakeaa827/ai-model-selection), branch `main`. This repository is private; consumers need authenticated read access. Use the authenticated GitHub Contents API to retrieve `latest.json`. Re-fetch regularly and honor `checked_at`; do not just rely on a cached filename or commit time.

```sh
gh api -H 'Accept: application/vnd.github.raw+json' 'repos/blakeaa827/ai-model-selection/contents/latest.json?ref=main' > latest.json
node select-model.mjs latest.json floor
node select-model.mjs latest.json ceiling
node select-model.mjs latest.json 50
```

The Contents API endpoint is `https://api.github.com/repos/blakeaa827/ai-model-selection/contents/latest.json?ref=main`. Authenticate through your tool's GitHub integration. The selector's HTTPS-input option supports public JSON endpoints; for this private repository, retrieve the file through authenticated GitHub access first.

An optional third argument is a comma-separated list of required OpenRouter parameters, for example `tools,response_format`. The helper verifies the current catalog ID, unchanged canonical revision, exact supported effort and required parameters before returning the configuration. Network errors, stale data, unverified model revisions, unsupported effort and impossible thresholds stop selection; it never silently substitutes a different model.

The request fragment includes `provider.only` for the first-party provider, `require_parameters: true` and `allow_fallbacks: false`. This reduces variation from the benchmark environment. Use the returned `api_endpoint`: add `input` for Responses or `messages` for Chat Completions, plus a task-specific output budget. The selector checks the standard provider endpoint's current availability, revision and parameter support. Higher effort may need a large output budget; a small limit can truncate reasoning and change capability. Tool calling and vision need their own task checks.

## Cost and identity contract

Use `openrouter_model_id` in an API request. `openrouter_canonical_slug` records the observed catalog revision and is **not** assumed callable. Do not replace IDs with `latest` aliases or Pro/Batch variants without benchmarking that exact configuration.

`benchmark_task_cost_usd` is Artificial Analysis's weighted cost of its benchmark tasks, not an OpenRouter invoice estimate. Per-million-token catalog pricing is stored separately. Context size, cache use, tool fees, service tiers and actual token usage change real costs. Rounded score ties do not guarantee equal behavior. Added USD/index point is a descriptive heuristic rather than a claim that index points have equal practical utility.

## Daily publishing contract

1. Recheck independent benchmarks, their methodology version, official release/availability/pricing and OpenRouter's live catalog.
2. Admit only publicly available configurations with a comparable score/cost pair and verified ID/effort. Record pending or restricted models separately.
3. Recompute the lowest-cost frontier, marginal costs, floor and ceiling; preserve explicit capability requirements.
4. Validate `latest.json` against `schema.json`, and run live catalog verification. Compare the results with the previous report.
5. Publish `latest.json`, `latest.md` and a dated snapshot in one commit to the agreed repository and branch. Advance `checked_at` only after a successful check, even if recommendations are unchanged. Do not publish a freshly dated report after a failed verification.
6. Preserve unrelated repository files. Retain the last successful snapshot when a check fails and report the failure. Consumers reject reports older than 48 hours unless they deliberately implement a documented stale-data policy.

The existing AI Model Selection Chart task publishes to this repository. Credentials are supplied by the connected GitHub integration and never committed. Publication failures are reported separately from successful benchmark research.

## Sources

[Artificial Analysis model releases](https://artificialanalysis.ai/models/releases), [OpenRouter live model catalog](https://openrouter.ai/api/v1/models), [reasoning settings](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens), [provider routing](https://openrouter.ai/docs/guides/routing/provider-selection).


## October 4 verification notes

The frontier and recommendations are unchanged. `latest.json` now includes the complete candidate audit and first-party endpoint verification. The selector returns `api_endpoint` and validates live endpoint parameter support. For OpenAI reasoning/tool workflows use the Responses API and add `input`; for Claude Chat Completions add `messages`. Respect the exact effort and standard provider route. Gemini Flash pricing is promotional through December 31; Opus provider default effort differs from the gateway default, so explicit effort is required.
