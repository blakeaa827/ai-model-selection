# Model selection chart — October 3, 2026

Recommended floor: **GPT-6.1 Sol / medium / 48 / $0.21**.
Recommended ceiling before the sharp cost cliff: **GPT-6.1 Sol / xhigh / 51 / $0.39**.

Artificial Analysis Intelligence Index v4.3.2. USD costs are weighted benchmark task averages, not OpenRouter prompt bills. Claude configurations use adaptive reasoning and default safety fallback.

| Minimum score | Model | OpenRouter model ID | Effort | Delivered score | USD/task | Added USD/point |
|---|---|---|---|---:|---:|---:|
| ≤22 | GPT-6 Luna | `openai/gpt-6-luna` | `low` | 22 | 0.0045 | — |
| 23–30 | GPT-6 Luna | `openai/gpt-6-luna` | `medium` | 30 | 0.02 | 0.001937 |
| 31–33 | GPT-6 Luna | `openai/gpt-6-luna` | `high` | 33 | 0.03 | 0.003333 |
| 34–35 | GPT-6 Luna | `openai/gpt-6-luna` | `xhigh` | 35 | 0.04 | 0.005 |
| 36–38 | GPT-6 Luna | `openai/gpt-6-luna` | `max` | 38 | 0.07 | 0.01 |
| 39–42 | GPT-6.1 Sol | `openai/gpt-6.1-sol` | `low` | 42 | 0.13 | 0.015 |
| 43–48 | GPT-6.1 Sol | `openai/gpt-6.1-sol` | `medium` | 48 | 0.21 | 0.013333 |
| 49–50 | GPT-6.1 Sol | `openai/gpt-6.1-sol` | `high` | 50 | 0.32 | 0.055 |
| 51 | GPT-6.1 Sol | `openai/gpt-6.1-sol` | `xhigh` | 51 | 0.39 | 0.07 |
| 52 | GPT-6.1 Sol | `openai/gpt-6.1-sol` | `max` | 52 | 0.72 | 0.33 |
| 53–54 | Claude Opus 5.5 | `anthropic/claude-opus-5.5` | `high` | 54 | 1.82 | 0.55 |
| 55–56 | Claude Opus 5.5 | `anthropic/claude-opus-5.5` | `xhigh` | 56 | 3.46 | 0.82 |
| 57–58 | Claude Opus 5.5 | `anthropic/claude-opus-5.5` | `max` | 58 | 5.98 | 1.26 |

Above 58: no eligible configuration in this comparison.

## Diminishing returns

At 48, medium-to-high costs $0.055 per added point versus $0.013333 for low-to-medium, a 4.125× increase. At 51, xhigh-to-max adds one point for $0.33 (+84.6% cost), a 4.714× marginal-price increase. These knees are recommendations; index intervals are not equal units of practical value.

## Calling OpenRouter

Use `openrouter_model_id` for `model` and the exact `effort` for `reasoning.effort`. The same slug can produce very different costs at different efforts. `provider.require_parameters: true` prevents routing to endpoints that ignore required parameters. No paid model-call verification was performed.

## Sources

- https://artificialanalysis.ai/models/releases/gpt-6-luna
- https://artificialanalysis.ai/models/releases/gpt-6-1-sol
- https://artificialanalysis.ai/models/releases/claude-opus-5-5
- https://openrouter.ai/api/v1/models
- https://openrouter.ai/docs/guides/best-practices/reasoning-tokens
- https://openrouter.ai/docs/guides/routing/provider-selection
- https://artificialanalysis.ai/models/releases/comparisons/gpt-6-1-sol-vs-gpt-6-astra
- https://artificialanalysis.ai/models/releases/claude-sonnet-5-5
- https://artificialanalysis.ai/models/releases/grok-4-7
- https://artificialanalysis.ai/models/releases/gemini-3-8-flash

