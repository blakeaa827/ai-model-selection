# AI model selection — October 6, 2026

Verified 2026-10-06T14:14:16Z. Artificial Analysis Intelligence Index **v4.3.2**. AA revised six non-frontier task costs and now marks Grok 4.6 deprecated; the actionable frontier, floor and ceiling are unchanged since October 5. October 6 is the verification date, not a claimed evaluation completion date.

**Recommended floor:** `openai/gpt-6.1-sol`, `reasoning.effort: "medium"`, score **48**, **$0.21** per weighted benchmark task. The next step raises marginal cost from $0.013333 to $0.055 per index point (**4.125×**).

**Optional ceiling before the sharp cliff:** `openai/gpt-6.1-sol`, `reasoning.effort: "xhigh"`, score **51**, **$0.39**. The next point costs $0.33 instead of $0.07 (**4.714×**), for an **84.62%** cost increase.

These are general defaults, not universally optimal knees. For narrow easy tasks, use cheaper Luna configurations once your success checks pass. Pay above the ceiling for verified improvements in complex reasoning, difficult debugging, long agent workflows or professional deliverables when avoided failure/review costs justify the premium.

## Exact progressive selection table

Choose the row whose interval contains your minimum required score. `(a, b]` means greater than a through b inclusive; ranges are continuous, including fractional thresholds. Costs are **AA weighted USD per Intelligence Index task**, not token prices or OpenRouter invoice estimates.

| Minimum score interval | request.model | request.reasoning.effort | Delivered score | USD/task |
|---|---|---|---:|---:|
| [0, 22] | `openai/gpt-6-luna` | `low` | 22 | $0.0045 |
| (22, 30] | `openai/gpt-6-luna` | `medium` | 30 | $0.02 |
| (30, 33] | `openai/gpt-6-luna` | `high` | 33 | $0.03 |
| (33, 35] | `openai/gpt-6-luna` | `xhigh` | 35 | $0.04 |
| (35, 38] | `openai/gpt-6-luna` | `max` | 38 | $0.07 |
| (38, 42] | `openai/gpt-6.1-sol` | `low` | 42 | $0.13 |
| (42, 48] | `openai/gpt-6.1-sol` | `medium` | 48 | $0.21 |
| (48, 50] | `openai/gpt-6.1-sol` | `high` | 50 | $0.32 |
| (50, 51] | `openai/gpt-6.1-sol` | `xhigh` | 51 | $0.39 |
| (51, 52] | `openai/gpt-6.1-sol` | `max` | 52 | $0.72 |
| (52, 54] | `anthropic/claude-opus-5.5` | `high` | 54 | $1.82 |
| (54, 56] | `anthropic/claude-opus-5.5` | `xhigh` | 56 | $3.46 |
| (56, 58] | `anthropic/claude-opus-5.5` | `max` | 58 | $5.98 |

Above 58: no eligible verified configuration in this scope.

All rows require `provider.require_parameters: true`, `provider.allow_fallbacks: false`, and `provider.only: ["openai"]` or `["anthropic"]`, respectively. Standard first-party endpoints were inspected; tier endpoints require opt-in and are not used. Canonical revision identifiers and supported efforts are stored per row/model in `latest.json`. OpenAI tool requests use `https://openrouter.ai/api/v1/responses` with `input`; Claude can use `https://openrouter.ai/api/v1/chat/completions` with `messages`. No paid generation was performed.

## Marginal cost of every adjacent retained step

| Destination model / effort | Δ score | Added USD/task | Cost increase | Added USD/index point |
|---|---:|---:|---:|---:|
| `openai/gpt-6-luna` / `medium` | +8 | $0.0155 | 344.44% | $0.0019375 |
| `openai/gpt-6-luna` / `high` | +3 | $0.01 | 50.00% | $0.00333333 |
| `openai/gpt-6-luna` / `xhigh` | +2 | $0.01 | 33.33% | $0.005 |
| `openai/gpt-6-luna` / `max` | +3 | $0.03 | 75.00% | $0.01 |
| `openai/gpt-6.1-sol` / `low` | +4 | $0.06 | 85.71% | $0.015 |
| `openai/gpt-6.1-sol` / `medium` | +6 | $0.08 | 61.54% | $0.0133333 |
| `openai/gpt-6.1-sol` / `high` | +2 | $0.11 | 52.38% | $0.055 |
| `openai/gpt-6.1-sol` / `xhigh` | +1 | $0.07 | 21.88% | $0.07 |
| `openai/gpt-6.1-sol` / `max` | +1 | $0.33 | 84.62% | $0.33 |
| `anthropic/claude-opus-5.5` / `high` | +2 | $1.1 | 152.78% | $0.55 |
| `anthropic/claude-opus-5.5` / `xhigh` | +2 | $1.64 | 90.11% | $0.82 |
| `anthropic/claude-opus-5.5` / `max` | +2 | $2.52 | 72.83% | $1.26 |

The early Luna increments rise from $0.0019375 to $0.01 per point; medium→max within Luna increases marginal cost 1.72×, 1.5× and 2× across successive steps. The Luna→Sol transition is $0.015/point, then Sol medium improves this to $0.013333/point. The first strong high-capability knee is therefore at Sol medium; the next marginal step is 4.125× dearer. The family jump from Sol max to Opus high adds 2 points for $1.10 (**152.78%** more cost; $0.55/point). Later Opus increments rise to $0.82 and $1.26/point. From the recommended ceiling to Opus high is **4.67×** the price for 3 points; Opus max is **15.33×** the price for 7 points.

Dollars per index point are descriptive: index intervals need not have equal practical utility, and an index percentage change is not a percentage increase in intelligence. No cost/score ratio or meaningful zero-intelligence baseline is assumed.

## Cost versus delivered capability

![Cost versus Intelligence Index score; logarithmic USD axis](cost-curve.svg)

The connected points are measured configurations, not claims about intermediate efforts. The vertical cost axis is logarithmic to keep the full frontier visible.

## Coverage, exclusions and uncertainty

- Fresh AA model pages were retrieved for all published configurations of GPT-6 Astra/Sol/Luna, GPT-6.1 Sol, Claude Opus/Sonnet 5.5, Grok 4.7/4.6 and Gemini 3.8 Flash, plus historical Gemini Pro/Flash-Lite results. All retrieved pairs use v4.3.2. The full audit is in `evaluated_configurations`. Astra, original Sol and Grok are dominated on this cost-capability objective.
- October 6 source changes outside the frontier: Gemini 3.1 Pro Preview task cost rose from $0.67 to $1.30; Gemini 3.5 Flash-Lite rose from $0.12 to $0.19; Grok 4.6 low/medium/xhigh/high-default fell from $0.48/$1.50/$2.32/$1.86 to $0.38/$1.14/$1.75/$1.48. Scores did not change. AA now marks Grok 4.6 deprecated and recommends Grok 4.7, so all Grok 4.6 configurations are non-actionable.
- Haiku 5.5 remains forthcoming. Grok 4.7 medium lacks a comparable pair; Gemini 3.8 Flash low has score 33 but no published task cost. Pro, Batch and speed-tier results are not substituted for standard-mode benchmarks.
- Gemini 4 Argon (announced September 30) remains restricted to Fairwind users. Its $1.99 task cost is promotional; AA reports $3.98 without that discount. The public Gemini 3.8 Flash token promotion expires December 31. Flash Cyber also has restricted access and no eligible pair.
- Sonnet measurements came from a prerelease deployment affected by a structured-output bug; AA has not confirmed reruns in the opened article. Excluded as unverified deployment equivalence; existing results are also dominated.
- AA marks SciCode and CritPt under review. Sol/Luna image encoding was fixed September 25; post-fix evaluation completion dates are not exposed. Current model tables take precedence over dated articles and stale search snippets.
- OpenRouter reports Opus default effort as high; Anthropic documents medium. Explicit efforts preserve each benchmarked setting. Anthropic model safety fallback (enabled in AA) is separate from gateway provider fallback.
- No actionable frontier-model retirement found; Grok 4.6 is newly marked deprecated and excluded. Google restricts Gemini 2.5 to existing users; OpenRouter lists October 20 expiration metadata for older 2.5 entries. Those policies are not interchangeable, and older 2.5 entries are excluded from this chart.

The index measures broad capability, **not percentage knowledge**. Benchmark task costs use observed token consumption and published provider prices. Individual prompts, tool calls, context length, retries and OpenRouter fees can produce different bills. Reject reports older than 48 hours, changed canonical revisions, unsupported efforts or missing required endpoint parameters; never silently substitute a model.

## Sources

- [https://artificialanalysis.ai/models/releases/gpt-6-luna](https://artificialanalysis.ai/models/releases/gpt-6-luna)
- [https://artificialanalysis.ai/models/releases/gpt-6-1-sol](https://artificialanalysis.ai/models/releases/gpt-6-1-sol)
- [https://artificialanalysis.ai/models/releases/claude-opus-5-5](https://artificialanalysis.ai/models/releases/claude-opus-5-5)
- [https://openrouter.ai/api/v1/models](https://openrouter.ai/api/v1/models)
- [https://openrouter.ai/docs/guides/best-practices/reasoning-tokens](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens)
- [https://openrouter.ai/docs/guides/routing/provider-selection](https://openrouter.ai/docs/guides/routing/provider-selection)
- [https://artificialanalysis.ai/models/releases/comparisons/gpt-6-1-sol-vs-gpt-6-astra](https://artificialanalysis.ai/models/releases/comparisons/gpt-6-1-sol-vs-gpt-6-astra)
- [https://artificialanalysis.ai/models/releases/claude-sonnet-5-5](https://artificialanalysis.ai/models/releases/claude-sonnet-5-5)
- [https://artificialanalysis.ai/models/releases/grok-4-7](https://artificialanalysis.ai/models/releases/grok-4-7)
- [https://artificialanalysis.ai/models/releases/gemini-3-8-flash](https://artificialanalysis.ai/models/releases/gemini-3-8-flash)
- [https://artificialanalysis.ai/models](https://artificialanalysis.ai/models)
- [https://artificialanalysis.ai/models/releases](https://artificialanalysis.ai/models/releases)
- [https://artificialanalysis.ai/methodology/intelligence-benchmarking](https://artificialanalysis.ai/methodology/intelligence-benchmarking)
- [https://developers.openai.com/api/docs/changelog](https://developers.openai.com/api/docs/changelog)
- [https://developers.openai.com/api/docs/deprecations](https://developers.openai.com/api/docs/deprecations)
- [https://www.anthropic.com/claude-opus-5-5](https://www.anthropic.com/claude-opus-5-5)
- [https://www.anthropic.com/claude-sonnet-5-5](https://www.anthropic.com/claude-sonnet-5-5)
- [https://platform.claude.com/docs/en/build-with-claude/effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [https://docs.x.ai/developers/release-notes](https://docs.x.ai/developers/release-notes)
- [https://ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [https://ai.google.dev/gemini-api/docs/changelog](https://ai.google.dev/gemini-api/docs/changelog)
- [https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash)
- [https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/)
- [https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/)
- [https://artificialanalysis.ai/articles/gemini-4-argon-google-top-three-labs](https://artificialanalysis.ai/articles/gemini-4-argon-google-top-three-labs)
- [https://artificialanalysis.ai/articles/claude-sonnet-5-5](https://artificialanalysis.ai/articles/claude-sonnet-5-5)
- [https://artificialanalysis.ai/articles/gpt-6-sol-and-luna-push-the-cost-efficiency-frontier](https://artificialanalysis.ai/articles/gpt-6-sol-and-luna-push-the-cost-efficiency-frontier)
- [https://artificialanalysis.ai/articles/gpt-6-1-sol-replaces-gpt-6-sol-after-just-7-days-with-near-astra-intelligence](https://artificialanalysis.ai/articles/gpt-6-1-sol-replaces-gpt-6-sol-after-just-7-days-with-near-astra-intelligence)
- [https://artificialanalysis.ai/articles/claude-opus-5-5](https://artificialanalysis.ai/articles/claude-opus-5-5)
- [https://artificialanalysis.ai/articles/benchmarking-grok-4-7](https://artificialanalysis.ai/articles/benchmarking-grok-4-7)
- [https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra](https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra)
- [https://openrouter.ai/docs/api_reference/responses/overview](https://openrouter.ai/docs/api_reference/responses/overview)
- [https://artificialanalysis.ai/models/claude-opus-5-5](https://artificialanalysis.ai/models/claude-opus-5-5)
- [https://artificialanalysis.ai/models/claude-opus-5-5-high](https://artificialanalysis.ai/models/claude-opus-5-5-high)
- [https://artificialanalysis.ai/models/claude-opus-5-5-low](https://artificialanalysis.ai/models/claude-opus-5-5-low)
- [https://artificialanalysis.ai/models/claude-opus-5-5-medium](https://artificialanalysis.ai/models/claude-opus-5-5-medium)
- [https://artificialanalysis.ai/models/claude-opus-5-5-xhigh](https://artificialanalysis.ai/models/claude-opus-5-5-xhigh)
- [https://artificialanalysis.ai/models/claude-sonnet-5-5](https://artificialanalysis.ai/models/claude-sonnet-5-5)
- [https://artificialanalysis.ai/models/claude-sonnet-5-5-high](https://artificialanalysis.ai/models/claude-sonnet-5-5-high)
- [https://artificialanalysis.ai/models/claude-sonnet-5-5-low](https://artificialanalysis.ai/models/claude-sonnet-5-5-low)
- [https://artificialanalysis.ai/models/claude-sonnet-5-5-medium](https://artificialanalysis.ai/models/claude-sonnet-5-5-medium)
- [https://artificialanalysis.ai/models/claude-sonnet-5-5-xhigh](https://artificialanalysis.ai/models/claude-sonnet-5-5-xhigh)
- [https://artificialanalysis.ai/models/gemini-3-1-pro-preview](https://artificialanalysis.ai/models/gemini-3-1-pro-preview)
- [https://artificialanalysis.ai/models/gemini-3-5-flash-lite](https://artificialanalysis.ai/models/gemini-3-5-flash-lite)
- [https://artificialanalysis.ai/models/gemini-3-8-flash](https://artificialanalysis.ai/models/gemini-3-8-flash)
- [https://artificialanalysis.ai/models/gemini-3-8-flash-low](https://artificialanalysis.ai/models/gemini-3-8-flash-low)
- [https://artificialanalysis.ai/models/gemini-3-8-flash-medium](https://artificialanalysis.ai/models/gemini-3-8-flash-medium)
- [https://artificialanalysis.ai/models/gpt-6-1-sol](https://artificialanalysis.ai/models/gpt-6-1-sol)
- [https://artificialanalysis.ai/models/gpt-6-1-sol-high](https://artificialanalysis.ai/models/gpt-6-1-sol-high)
- [https://artificialanalysis.ai/models/gpt-6-1-sol-low](https://artificialanalysis.ai/models/gpt-6-1-sol-low)
- [https://artificialanalysis.ai/models/gpt-6-1-sol-medium](https://artificialanalysis.ai/models/gpt-6-1-sol-medium)
- [https://artificialanalysis.ai/models/gpt-6-1-sol-xhigh](https://artificialanalysis.ai/models/gpt-6-1-sol-xhigh)
- [https://artificialanalysis.ai/models/gpt-6-astra](https://artificialanalysis.ai/models/gpt-6-astra)
- [https://artificialanalysis.ai/models/gpt-6-astra-high](https://artificialanalysis.ai/models/gpt-6-astra-high)
- [https://artificialanalysis.ai/models/gpt-6-astra-low](https://artificialanalysis.ai/models/gpt-6-astra-low)
- [https://artificialanalysis.ai/models/gpt-6-astra-medium](https://artificialanalysis.ai/models/gpt-6-astra-medium)
- [https://artificialanalysis.ai/models/gpt-6-astra-xhigh](https://artificialanalysis.ai/models/gpt-6-astra-xhigh)
- [https://artificialanalysis.ai/models/gpt-6-luna](https://artificialanalysis.ai/models/gpt-6-luna)
- [https://artificialanalysis.ai/models/gpt-6-luna-high](https://artificialanalysis.ai/models/gpt-6-luna-high)
- [https://artificialanalysis.ai/models/gpt-6-luna-low](https://artificialanalysis.ai/models/gpt-6-luna-low)
- [https://artificialanalysis.ai/models/gpt-6-luna-medium](https://artificialanalysis.ai/models/gpt-6-luna-medium)
- [https://artificialanalysis.ai/models/gpt-6-luna-non-reasoning](https://artificialanalysis.ai/models/gpt-6-luna-non-reasoning)
- [https://artificialanalysis.ai/models/gpt-6-luna-xhigh](https://artificialanalysis.ai/models/gpt-6-luna-xhigh)
- [https://artificialanalysis.ai/models/gpt-6-sol](https://artificialanalysis.ai/models/gpt-6-sol)
- [https://artificialanalysis.ai/models/gpt-6-sol-high](https://artificialanalysis.ai/models/gpt-6-sol-high)
- [https://artificialanalysis.ai/models/gpt-6-sol-low](https://artificialanalysis.ai/models/gpt-6-sol-low)
- [https://artificialanalysis.ai/models/gpt-6-sol-medium](https://artificialanalysis.ai/models/gpt-6-sol-medium)
- [https://artificialanalysis.ai/models/gpt-6-sol-non-reasoning](https://artificialanalysis.ai/models/gpt-6-sol-non-reasoning)
- [https://artificialanalysis.ai/models/gpt-6-sol-xhigh](https://artificialanalysis.ai/models/gpt-6-sol-xhigh)
- [https://artificialanalysis.ai/models/grok-4-6](https://artificialanalysis.ai/models/grok-4-6)
- [https://artificialanalysis.ai/models/grok-4-6-low](https://artificialanalysis.ai/models/grok-4-6-low)
- [https://artificialanalysis.ai/models/grok-4-6-medium](https://artificialanalysis.ai/models/grok-4-6-medium)
- [https://artificialanalysis.ai/models/grok-4-6-xhigh](https://artificialanalysis.ai/models/grok-4-6-xhigh)
- [https://artificialanalysis.ai/models/grok-4-7](https://artificialanalysis.ai/models/grok-4-7)
- [https://artificialanalysis.ai/models/grok-4-7-high](https://artificialanalysis.ai/models/grok-4-7-high)
- [https://artificialanalysis.ai/models/grok-4-7-low](https://artificialanalysis.ai/models/grok-4-7-low)
- [https://openrouter.ai/api/v1/models/openai/gpt-6-luna/endpoints](https://openrouter.ai/api/v1/models/openai/gpt-6-luna/endpoints)
- [https://openrouter.ai/api/v1/models/openai/gpt-6.1-sol/endpoints](https://openrouter.ai/api/v1/models/openai/gpt-6.1-sol/endpoints)
- [https://openrouter.ai/api/v1/models/anthropic/claude-opus-5.5/endpoints](https://openrouter.ai/api/v1/models/anthropic/claude-opus-5.5/endpoints)
- [https://developers.openai.com/api/docs/models/gpt-6-luna](https://developers.openai.com/api/docs/models/gpt-6-luna)
- [https://developers.openai.com/api/docs/models/gpt-6.1-sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
- [https://developers.openai.com/api/docs/models/gpt-6-sol](https://developers.openai.com/api/docs/models/gpt-6-sol)
- [https://developers.openai.com/api/docs/models/gpt-6-astra](https://developers.openai.com/api/docs/models/gpt-6-astra)
