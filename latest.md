# AI model selection — October 9, 2026

**Recommended API floor:** MiMo-V2.6-Pro / thinking enabled, score **46.324**, **$0.133223** per AA task. **Optional ceiling:** GPT-6.1 Sol / xhigh, score **51.038**, **$0.392861**. Both remain unchanged.

## Changes since October 8

- The 15 paid configurations, opt-in Gemma free route, recommended floor and ceiling are unchanged. Every actionable score/cost and route was refreshed against current sources.
- Haiku low's measured score changed from 29.4494981304947 to 29.4523685891139 (+0.0028704586192). Its task cost is still provisional and omits the >100K input tier. No completed pricing correction or refusal-issue rerun was found; all five Haiku efforts remain excluded from actionable cost routing. The small score edit is not evidence of a significant capability change or a completed rerun.
- Three newly observed gateway listings: openai/gpt-6.1-sol:batch, openai/gpt-6.1-sol-pro:batch, inclusionai/ling-3.0-flash-sante. Batch processing and Pro mode cannot inherit standard task-cost or score pairs. Sante lacks an exact comparable pair. Gateway listing dates are not official model release dates.
- Two previous gateway listings are no longer present: inclusionai/ling-3.0-flash-sante:free and baidu/ernie-4.5-vl-424b-a47b. They were not on the actionable frontier. The coverage inventory records their absence rather than inferring an official model retirement.
- AA adds GPT-6 Sol Daybreak Blue to its release registry. Access is restricted; its published Cyber Index result uses a separate harness and cost basis, with no common Intelligence Index pair. It remains outside this chart.
- Harvey LAB-AA v1.1 adds hallucination checks to a separate legal evaluation. The common Intelligence Index remains v4.3.2; no incompatible Cyber or legal results are mixed into it.
- Coverage: 469 live gateway entries, 503 AA releases, 59 exact AA records and 15 free catalog entries audited. Screening every listing does not establish measured coverage for every configuration. Subscription recommendations remain conditional and unchanged.

[AA release registry](https://artificialanalysis.ai/models/releases) · [Live gateway catalog](https://openrouter.ai/api/v1/models) · [Daybreak evaluator article](https://artificialanalysis.ai/articles/trusted-access-models-cyber-index) · [Harvey LAB-AA update](https://artificialanalysis.ai/articles/harvey-lab-aa-v1-1) · [Haiku cost disclosure](https://artificialanalysis.ai/articles/claude-haiku-5-5)

The Intelligence Index measures broad capability, not percentage knowledge. Costs are AA’s weighted benchmark-task costs based on observed token use and published prices, not a forecast for an individual prompt or an OpenRouter invoice. Use underlying numerical values for lookup; close score differences are not established statistical advantages. AA does not publish exact per-configuration evaluation completion dates. SciCode and CritPt remain under review.

## Minimum cost for a capability target

Thresholds below are continuous: lower bounds are exclusive except the first row, and upper bounds inclusive. Request controls and pinned first-party providers are verified. No eligible configuration exceeds the highest observed score. Exact costs and score/budget intervals are in latest.json.

| Minimum-score range | request.model | request.reasoning | Delivered score | USD / AA task |
|---|---|---|---:|---:|
| [0, 21.5261980080866] | `openai/gpt-6-luna` | `effort=low` | 21.526 | $0.004517 |
| (21.5261980080866, 29.9251773515762] | `openai/gpt-6-luna` | `effort=medium` | 29.925 | $0.017477 |
| (29.9251773515762, 32.9282054150837] | `openai/gpt-6-luna` | `effort=high` | 32.928 | $0.029032 |
| (32.9282054150837, 34.5587320217785] | `openai/gpt-6-luna` | `effort=xhigh` | 34.559 | $0.042184 |
| (34.5587320217785, 37.8843590141754] | `xiaomi/mimo-v2.6-flash` | `enabled=true` | 37.884 | $0.062315 |
| (37.8843590141754, 38.1245186869738] | `openai/gpt-6-luna` | `effort=max` | 38.125 | $0.067823 |
| (38.1245186869738, 42.0835618555848] | `openai/gpt-6.1-sol` | `effort=low` | 42.084 | $0.130752 |
| (42.0835618555848, 46.3242065310383] | `xiaomi/mimo-v2.6-pro` | `enabled=true` | 46.324 | $0.133223 |
| (46.3242065310383, 47.7833271274065] | `openai/gpt-6.1-sol` | `effort=medium` | 47.783 | $0.213701 |
| (47.7833271274065, 50.2377777519769] | `openai/gpt-6.1-sol` | `effort=high` | 50.238 | $0.319144 |
| (50.2377777519769, 51.0377679093761] | `openai/gpt-6.1-sol` | `effort=xhigh` | 51.038 | $0.392861 |
| (51.0377679093761, 51.8332597011541] | `openai/gpt-6.1-sol` | `effort=max` | 51.833 | $0.724167 |
| (51.8332597011541, 53.5831959822067] | `anthropic/claude-opus-5.5` | `effort=high` | 53.583 | $1.822505 |
| (53.5831959822067, 55.9873505840139] | `anthropic/claude-opus-5.5` | `effort=xhigh` | 55.987 | $3.459110 |
| (55.9873505840139, 57.6223698102963] | `anthropic/claude-opus-5.5` | `effort=max` | 57.622 | $5.982012 |

Every paid request sets provider.require_parameters=true, provider.allow_fallbacks=false, and exactly one verified provider tag: openai, anthropic or xiaomi/fp8. Callable IDs above are paired with exact canonical revision slugs in latest.json; the selector checks the live revision before returning a request. OpenAI tool calls use Responses; Xiaomi and Anthropic use Chat Completions. Metadata checks succeeded; no paid generation calls were made.

For MiMo, reasoning.enabled=true maps to native thinking.type=enabled. Effort is null in metadata and omitted from the request. Official docs say named non-none efforts all enable identical thinking, so they are not additional capability configurations. Preserve reasoning_details through tool turns, leave sampling at provider defaults and allocate sufficient output tokens. Official release September 22 versus AA/catalog September 21 is recorded. Official cache writes are currently limited-time free, with no verified expiry; refresh AA costs when pricing changes.

## Most capability within a benchmark-task budget

These budgets refer to AA’s benchmark-task average, not an invoice cap. Intervals are lower-inclusive and upper-exclusive.

| Example budget | Best observed choice | Score | USD / AA task |
|---:|---|---:|---:|
| $0.010 | GPT-6 Luna / low | 21.526 | $0.004517 |
| $0.030 | GPT-6 Luna / high | 32.928 | $0.029032 |
| $0.070 | GPT-6 Luna / max | 38.125 | $0.067823 |
| $0.125 | GPT-6 Luna / max | 38.125 | $0.067823 |
| $0.140 | MiMo-V2.6-Pro / thinking enabled | 46.324 | $0.133223 |
| $0.250 | GPT-6.1 Sol / medium | 47.783 | $0.213701 |
| $0.400 | GPT-6.1 Sol / xhigh | 51.038 | $0.392861 |
| $1.000 | GPT-6.1 Sol / max | 51.833 | $0.724167 |
| $2.000 | Claude Opus 5.5 / high | 53.583 | $1.822505 |
| $4.000 | Claude Opus 5.5 / xhigh | 55.987 | $3.459110 |
| $6.000 | Claude Opus 5.5 / max | 57.622 | $5.982012 |

**Limited free opt-in:** request.model=google/gemma-4-31b-it:free, request.reasoning.enabled=true, provider.only=[google-ai-studio], require_parameters=true, allow_fallbacks=false. Delivered score 14.6689500745828, independently measured task cost $0. Both AA’s zero-cost basis and the current first-party free gateway endpoint were rechecked. Managed quantization is undisclosed and recorded; third-party substitutes are rejected. Rate limits and account quota remain conditional. Only explicit allow_limited_free:true / --allow-limited-free enables this lane. The route covers targets [0,14.6689500745828] and budgets [0,0.004516607569410252); default paid selection remains available.

All free catalog entries were screened. North Mini Code’s verified AA zero-cost score 9.914628 is below Gemma; Command A+ has a paid gateway candidate despite AA’s free first-party basis. K2 Horizon’s zero-cost score 30.501530 has no matching public gateway listing, and Ling Tiny also lacks one. Other free aliases cannot inherit zero task costs from token prices. No new eligible free route found.

## Diminishing returns and recommended defaults

High-capability default candidate: upgrading Sol low to MiMo Pro adds 4.240645 points for $0.002471/task (+1.89%). The next upgrade, Sol medium, adds 1.459121 points for $0.080478 (+60.41%): $0.055155 per point, 94.64x the preceding marginal cost. MiMo Pro costs 37.66% less than Sol medium while delivering 1.459121 fewer index points. Validate coding reliability, latency, locale and tools on the application workload.

Optional higher-capability ceiling before Sol max: xhigh to max adds 0.795492 points for $0.331306 (+84.33%), or $0.416479/point, 4.5197x the preceding marginal rate. Higher-priced Opus can still be worthwhile when failures or human review cost more than model calls.

The whole frontier matters: Luna high to xhigh is an early local bend (about 2.10x the preceding marginal dollars per point), but the next MiMo Flash step improves that rate. MiMo Flash to Luna max costs $0.005508 for only 0.240160 points (about 3.79x the preceding rate). Those bends are followed by the strong value jump from Sol low to MiMo Pro. For simple extraction or repeatable edits, choose the cheapest model that meets your measured success target; the recommended floor is a conditional default for more demanding work.

| Upgrade to | Point gain | Added USD/task | Cost increase | Added USD/point | Versus previous marginal rate |
|---|---:|---:|---:|---:|---:|
| GPT-6 Luna / medium | 8.398979 | $0.012960 | 286.95% | $0.001543 | — |
| GPT-6 Luna / high | 3.003028 | $0.011555 | 66.11% | $0.003848 | 2.49x |
| GPT-6 Luna / xhigh | 1.630527 | $0.013152 | 45.30% | $0.008066 | 2.10x |
| MiMo-V2.6-Flash / thinking enabled | 3.325627 | $0.020131 | 47.72% | $0.006053 | 0.75x |
| GPT-6 Luna / max | 0.240160 | $0.005508 | 8.84% | $0.022936 | 3.79x |
| GPT-6.1 Sol / low | 3.959043 | $0.062929 | 92.78% | $0.015895 | 0.69x |
| MiMo-V2.6-Pro / thinking enabled | 4.240645 | $0.002471 | 1.89% | $0.000583 | 0.04x |
| GPT-6.1 Sol / medium | 1.459121 | $0.080478 | 60.41% | $0.055155 | 94.64x |
| GPT-6.1 Sol / high | 2.454451 | $0.105444 | 49.34% | $0.042960 | 0.78x |
| GPT-6.1 Sol / xhigh | 0.799990 | $0.073717 | 23.10% | $0.092147 | 2.14x |
| GPT-6.1 Sol / max | 0.795492 | $0.331306 | 84.33% | $0.416479 | 4.52x |
| Claude Opus 5.5 / high | 1.749936 | $1.098338 | 151.67% | $0.627644 | 1.51x |
| Claude Opus 5.5 / xhigh | 2.404155 | $1.636605 | 89.80% | $0.680741 | 1.08x |
| Claude Opus 5.5 / max | 1.635019 | $2.522902 | 72.93% | $1.543041 | 2.27x |

| Breakpoint | Why it matters |
|---|---|
| xiaomi/mimo-v2.6-pro@thinking-enabled → openai/gpt-6.1-sol@medium | +1.459121 points for $0.080478 (+60.41%); $0.055155/point |
| openai/gpt-6.1-sol@xhigh → openai/gpt-6.1-sol@max | +0.795492 points for $0.331306 (+84.33%); $0.416479/point |
| openai/gpt-6.1-sol@max → anthropic/claude-opus-5.5@high | +1.749936 points for $1.098338 (+151.67%); $0.627644/point |
| anthropic/claude-opus-5.5@xhigh → anthropic/claude-opus-5.5@max | +1.635019 points for $2.522902 (+72.93%); $1.543041/point |

Dollars per index point is a descriptive heuristic; equal index intervals need not have equal practical value. There is no universal knee without a workload, success target and budget. Pay above the ceiling when harder debugging, architecture, research or expensive human review makes a higher success rate worth the extra call cost. Never equate an index percentage change with a percentage increase in intelligence.

![Cost versus capability](cost-curve.svg)

## Haiku: measured scores, provisional costs excluded

Callable ID anthropic/claude-haiku-5.5; canonical anthropic/claude-haiku-5.5-20261007; supported efforts low/medium/high/xhigh/max, default medium. Official release October 7. Short-context token prices are $0.10 input/$0.50 output per million; above 100K input tokens they rise to $0.50/$2.50. These token prices are separate from AA task cost.

| Model ID | reasoning.effort | Measured score | Provisional USD/task — NOT actionable |
|---|---|---:|---:|
| `anthropic/claude-haiku-5.5` | `low` | 29.452 | $0.024459 |
| `anthropic/claude-haiku-5.5` | `medium` | 34.465 | $0.047031 |
| `anthropic/claude-haiku-5.5` | `high` | 37.824 | $0.079427 |
| `anthropic/claude-haiku-5.5` | `xhigh` | 41.249 | $0.123786 |
| `anthropic/claude-haiku-5.5` | `max` | 43.395 | $0.212770 |

AA says its costs omit the long-context price tier; no completed pricing correction or prerelease refusal-issue rerun was found. latest.json sets benchmark_task_cost_usd=null and eligible_for_frontier=false, preserving the published provisional number in a separately named field. Current AA labels omit Default Fallback; official docs confirm Haiku has no server-side fallback. The earlier xhigh frontier inclusion is a corrected eligibility error, not a model capability regression.

## Why Luna remains while Haiku costs are pending

Haiku can be stronger at higher effort without being cheaper at every capability threshold. Short-context standard token rates match Luna ($0.10 input/$0.50 output per million), but observed token use differs. These comparisons use measured scores and separately flagged provisional Haiku costs; they do not authorize Haiku routing.

| Luna choice | Score | USD/task | Haiku choice | Score | Provisional USD/task |
|---|---:|---:|---|---:|---:|
| medium | 29.925 | $0.017477 | low | 29.452 | $0.024459 |
| xhigh | 34.559 | $0.042184 | medium | 34.465 | $0.047031 |
| max | 38.125 | $0.067823 | high | 37.824 | $0.079427 |

Luna provides slightly higher measured broad-index scores at lower task costs for these particular comparisons, even before completing Haiku's tiered cost correction. Haiku xhigh remains an interesting candidate at score 41.249 and provisional $0.123786, but cannot yet be certified as the cheapest exact route. Workload-specific quality, latency and cost per successful completion can favor a model outside the broad-index frontier. A routing evaluator's success probability is conditional on task, model and effort; it is not a direct conversion to an Intelligence Index threshold. No evaluator or task-specific success mapping has been calibrated in this report.

## Other excluded or pending results

| Model / configuration | Current finding |
|---|---|
| Sonnet 5.5 all five efforts | Updated task costs below; prerelease structured-output bug rerun and deployment equivalence unconfirmed. |
| Step 5 Preview | Gateway revision 20261008, named efforts low/medium/high; AA September 18 effort and pricing correspondence remains unverified. |
| Gemini 4 Argon | Restricted Fairwind rollout, no matching public OpenRouter route; promotional cost not a general entitlement. |
| Grok 4.7 medium | Supported setting, no complete comparable score/task-cost pair found. |
| Gemini 3.8 Flash low | Score 33.4548106699132, task cost missing. |
| Sol 6.1 Batch and Sol 6.1 Pro Batch | Newly observed listings; no exact common-version pair measured for the processing tier/Pro mode. Standard costs are not halved and relabeled. |
| Ling 3.0 Flash Sante | Paid listing newly observed; no exact AA pair. Its previous free listing is absent. Official launch date remains unverified. |
| GPT-6 Sol Daybreak Blue | Restricted access; Cyber Index results and costs are not the common Intelligence Index. |
| Other Pro, Batch, Fast/Ultraspeed variants | No transfer of standard-mode score/cost pairs. |
| Mistral Large 4 Preview | Public preview, weights forthcoming, 50% launch discount for two weeks; AA measured standard pair dominated. Context metadata differs across sources. |
| Legacy Gemini 2.5 | Restricted access/expiration policies differ by platform; excluded. |

Sonnet’s score/cost entries below are measured on the disclosed prerelease deployment and are not approved routing configurations.

| Effort | Score | Current AA USD/task — prerelease deployment |
|---|---:|---:|
| low | 35.868 | $0.345161 |
| medium | 40.839 | $0.483264 |
| high | 46.753 | $0.884450 |
| xhigh | 51.896 | $2.012035 |
| max | 56.000 | $5.460853 |

Sonnet costs are unchanged since October 8; they retain the earlier cache-price reduction. Its disclosed prerelease structured-output reruns remain unconfirmed.

## Building through subscriptions

Personal subscription tiers and model menus remain unknown. These are conditional starting recommendations; API benchmark scores and task costs are null for unmeasured app/agent harnesses. Included allowance is not assumed to mean zero cost per successful task.

| Service / surface | Routine default | Escalation | Quota-saving choice |
|---|---|---|---|
| OpenAI | GPT-6.1 Sol; {"reasoning_effort":"medium","ui_label":"Medium","speed":"Standard"} | GPT-6.1 Sol; {"reasoning_effort":"xhigh","ui_label":"Extra High","speed":"Standard"} | GPT-6 Luna; {"reasoning_effort":"high","ui_label":"High","speed":"Standard"} |
| Claude | Claude Sonnet 5.5; {"effort":"high","ui_label":"High","thinking":"always_on_in_Claude"} | Claude Opus 5.5; {"effort":"xhigh","ui_label":"Extra high","thinking":"always_on"} | Claude Haiku 5.5; {"effort":"low","ui_label":"Low","thinking":"always_on_in_Claude"} |
| Grok | Grok 4.7; {"selection":"documented default model","effort":null,"ui_to_api_effort_mapping":"unverified","speed":"standard"} | Grok account higher-reasoning mode; {"selection":"only the higher-reasoning option actually exposed by the account","effort":null,"ui_to_api_effort_mapping":"unverified"} | Grok 4.7 standard mode; {"selection":"standard rather than Fast","effort":null,"ui_to_api_effort_mapping":"unverified"} |
| Gemini | Gemini 3.8 Flash; {"ui_thinking":"Standard where exposed","api_effort_mapping":null} | Gemini 3.8 Flash with Extended thinking; {"ui_thinking":"Extended where exposed","api_effort_mapping":null} | Gemini Flash-Lite; {"ui_thinking":"Standard where exposed","api_effort_mapping":null} |

**OpenAI access and limits:** Plus, Pro, Business, Enterprise or Edu launch access; client/rollout dependent; Enterprise/Edu admin must enable. Not Chat; Free/Go excluded at launch. Work and Codex share allowances. Fast uses 2.5x included allowance relative to Standard. Included tasks vary by context, effort and tools; use account dashboard. API rates are separate.


**Claude access and limits:** Pro/Max subscription login covers Claude Code; use /model to check exact account access. Team/Enterprise policy may restrict model or effort. Claude and Claude Code share plan limits; higher effort uses more quota. An ANTHROPIC_API_KEY can cause API billing instead of subscription usage. Personal tier not known. Eligible Max/Team can separately claim monthly Claude Platform API credits; first-party only, personal eligibility/claim status unknown.


**Grok access and limits:** Available in Grok Build; included allowance depends on exact account/plan. Consumer FAQ describes a shared weekly pool and paid extra usage. Bot launch docs describe its own usage pool, so keep Bot separate and check its dashboard; do not assume identical accounting. API credits are separate. Exact consumer reasoning control not verified.


**Gemini access and limits:** Official launch: Gemini app for Google AI Pro/Ultra; model availability differs by surface, region and account. Models/thinking consume differing allowance. Generic Help still lists Gemini 3 families while September launch explicitly grants 3.8 Flash to Pro/Ultra; prefer launch for exact revision, Help for controls. Gemini 4 Argon is restricted Fairwind rollout, not assumed consumer subscription access.


Use the project-connected GPT-6.1 Sol medium or Sonnet high harness for routine building; escalate inside the same service when a difficult step stalls. OpenAI Ultra, Grok Heavy and Gemini Deep Think are separate multi-agent/parallel modes and cannot inherit single-model API scores. Gemini UI Standard/Extended is not mapped to an API effort without evidence. Argon is not assumed included in a normal consumer subscription.

**Claude API credits, conditional on plan:** Max 5x $100/month; Max 20x $200/month; Team $20/Standard seat or $100/Premium seat, pooled up to $500/month. Requires an active eligible plan, seven days on plan and claiming/linking a Console organization. Free/Pro/Enterprise excluded. Credits pay the first-party Claude Platform, not OpenRouter. No personal claim status or per-task zero-cost entitlement is inferred.

## Verification and machine-readable contract

Source verification date: October 9, 2026; catalog checked 2026-10-09T14:13:49.431674+00:00; AA release registry checked 2026-10-09T14:13:50.563077+00:00. Per-configuration score/cost and endpoint timestamps are retained in latest.json. Each successfully checked source advances only its associated timestamp. Some raw HTTP sources failed; original-source web retrieval recovered them, and unrecovered checks remain disclosed. AA evaluation completion dates are unavailable.

Schema 1.1.0 is unchanged. latest.json supplies exact paid and opt-in score/budget intervals, request skeletons, recommendations, all marginal steps, subscription guidance, exclusions, source checks and coverage counts. coverage.json inventories every catalog entry and AA release. Release maxima/minima only screen potential winners; they never become configuration score/cost pairs. Model/revision/effort matches remain incomplete outside verified configurations. Reports and rows expire after 48 hours; live catalog/endpoint revision, provider, quantization and parameter checks reject mismatches rather than silently substituting. Selector tests cover both paid and opt-in boundaries, freshness, provisional/estimated benchmark eligibility and revision/parameter mismatch rejection. Fresh catalog and endpoint data also pass for all 16 actionable configurations; no paid generation smoke test is claimed.

## Sources

- https://ai.google.dev/gemini-api/docs/changelog
- https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash
- https://ai.google.dev/gemini-api/docs/pricing
- https://ai.google.dev/gemma/docs/capabilities/thinking
- https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra
- https://artificialanalysis.ai/articles/benchmarking-grok-4-7
- https://artificialanalysis.ai/articles/claude-haiku-5-5
- https://artificialanalysis.ai/articles/claude-opus-5-5
- https://artificialanalysis.ai/articles/claude-sonnet-5-5
- https://artificialanalysis.ai/articles/gemini-4-argon-google-top-three-labs
- https://artificialanalysis.ai/articles/gpt-6-1-sol-replaces-gpt-6-sol-after-just-7-days-with-near-astra-intelligence
- https://artificialanalysis.ai/articles/gpt-6-sol-and-luna-push-the-cost-efficiency-frontier
- https://artificialanalysis.ai/articles/harvey-lab-aa-v1-1
- https://artificialanalysis.ai/articles/trusted-access-models-cyber-index
- https://artificialanalysis.ai/changelog
- https://artificialanalysis.ai/methodology/intelligence-benchmarking
- https://artificialanalysis.ai/models
- https://artificialanalysis.ai/models/claude-haiku-5-5
- https://artificialanalysis.ai/models/claude-haiku-5-5-high
- https://artificialanalysis.ai/models/claude-haiku-5-5-low
- https://artificialanalysis.ai/models/claude-haiku-5-5-medium
- https://artificialanalysis.ai/models/claude-haiku-5-5-xhigh
- https://artificialanalysis.ai/models/claude-opus-5-5
- https://artificialanalysis.ai/models/claude-opus-5-5-high
- https://artificialanalysis.ai/models/claude-opus-5-5-low
- https://artificialanalysis.ai/models/claude-opus-5-5-medium
- https://artificialanalysis.ai/models/claude-opus-5-5-xhigh
- https://artificialanalysis.ai/models/claude-sonnet-5-5
- https://artificialanalysis.ai/models/claude-sonnet-5-5-high
- https://artificialanalysis.ai/models/claude-sonnet-5-5-low
- https://artificialanalysis.ai/models/claude-sonnet-5-5-medium
- https://artificialanalysis.ai/models/claude-sonnet-5-5-xhigh
- https://artificialanalysis.ai/models/command-a-plus
- https://artificialanalysis.ai/models/gemini-3-1-pro-preview
- https://artificialanalysis.ai/models/gemini-3-5-flash-lite
- https://artificialanalysis.ai/models/gemini-3-8-flash
- https://artificialanalysis.ai/models/gemini-3-8-flash-low
- https://artificialanalysis.ai/models/gemini-3-8-flash-medium
- https://artificialanalysis.ai/models/gemini-4-argon
- https://artificialanalysis.ai/models/gemma-4-31b
- https://artificialanalysis.ai/models/gpt-6-1-sol
- https://artificialanalysis.ai/models/gpt-6-1-sol-high
- https://artificialanalysis.ai/models/gpt-6-1-sol-low
- https://artificialanalysis.ai/models/gpt-6-1-sol-medium
- https://artificialanalysis.ai/models/gpt-6-1-sol-xhigh
- https://artificialanalysis.ai/models/gpt-6-astra
- https://artificialanalysis.ai/models/gpt-6-astra-high
- https://artificialanalysis.ai/models/gpt-6-astra-low
- https://artificialanalysis.ai/models/gpt-6-astra-medium
- https://artificialanalysis.ai/models/gpt-6-astra-xhigh
- https://artificialanalysis.ai/models/gpt-6-luna
- https://artificialanalysis.ai/models/gpt-6-luna-high
- https://artificialanalysis.ai/models/gpt-6-luna-low
- https://artificialanalysis.ai/models/gpt-6-luna-medium
- https://artificialanalysis.ai/models/gpt-6-luna-non-reasoning
- https://artificialanalysis.ai/models/gpt-6-luna-xhigh
- https://artificialanalysis.ai/models/gpt-6-sol
- https://artificialanalysis.ai/models/gpt-6-sol-high
- https://artificialanalysis.ai/models/gpt-6-sol-low
- https://artificialanalysis.ai/models/gpt-6-sol-medium
- https://artificialanalysis.ai/models/gpt-6-sol-non-reasoning
- https://artificialanalysis.ai/models/gpt-6-sol-xhigh
- https://artificialanalysis.ai/models/grok-4-6
- https://artificialanalysis.ai/models/grok-4-6-low
- https://artificialanalysis.ai/models/grok-4-6-medium
- https://artificialanalysis.ai/models/grok-4-6-xhigh
- https://artificialanalysis.ai/models/grok-4-7
- https://artificialanalysis.ai/models/grok-4-7-high
- https://artificialanalysis.ai/models/grok-4-7-low
- https://artificialanalysis.ai/models/k2-horizon-375b-a23b
- https://artificialanalysis.ai/models/ling-3-0-tiny
- https://artificialanalysis.ai/models/mimo-v2-6-flash
- https://artificialanalysis.ai/models/mimo-v2-6-pro
- https://artificialanalysis.ai/models/mistral-large-4
- https://artificialanalysis.ai/models/north-mini-code
- https://artificialanalysis.ai/models/releases
- https://artificialanalysis.ai/models/releases/claude-haiku-5-5
- https://artificialanalysis.ai/models/releases/claude-opus-5-5
- https://artificialanalysis.ai/models/releases/claude-sonnet-5-5
- https://artificialanalysis.ai/models/releases/comparisons/gpt-6-1-sol-vs-gpt-6-astra
- https://artificialanalysis.ai/models/releases/gemini-3-8-flash
- https://artificialanalysis.ai/models/releases/gpt-6-1-sol
- https://artificialanalysis.ai/models/releases/gpt-6-luna
- https://artificialanalysis.ai/models/releases/grok-4-7
- https://artificialanalysis.ai/models/step-5
- https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/
- https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/
- https://blog.google/innovation-and-ai/technology/ai/google-ai-updates-september-2026/
- https://developers.openai.com/api/docs/changelog
- https://developers.openai.com/api/docs/deprecations
- https://developers.openai.com/api/docs/guides/batch
- https://developers.openai.com/api/docs/models/gpt-6-astra
- https://developers.openai.com/api/docs/models/gpt-6-luna
- https://developers.openai.com/api/docs/models/gpt-6-sol
- https://developers.openai.com/api/docs/models/gpt-6.1-sol
- https://docs.mistral.ai/models/mistral-large-4-0
- https://docs.mistral.ai/resources/changelogs
- https://docs.x.ai/developers/grok-4-7
- https://docs.x.ai/developers/release-notes
- https://docs.x.ai/grok/faq
- https://learn.chatgpt.com/docs/models
- https://learn.chatgpt.com/docs/pricing
- https://mimo.mi.com/docs/en-US/api/chat
- https://mimo.mi.com/docs/en-US/api/chat/responses
- https://mimo.mi.com/docs/en-US/news/latest/v2-6
- https://mimo.mi.com/docs/en-US/price/pay-as-you-go
- https://mimo.mi.com/docs/en-US/updates/model
- https://openrouter.ai/api/v1/models
- https://openrouter.ai/api/v1/models/anthropic/claude-haiku-5.5/endpoints
- https://openrouter.ai/api/v1/models/anthropic/claude-opus-5.5/endpoints
- https://openrouter.ai/api/v1/models/anthropic/claude-sonnet-5.5/endpoints
- https://openrouter.ai/api/v1/models/google/gemini-3.1-pro-preview/endpoints
- https://openrouter.ai/api/v1/models/google/gemini-3.5-flash-lite/endpoints
- https://openrouter.ai/api/v1/models/google/gemini-3.8-flash/endpoints
- https://openrouter.ai/api/v1/models/google/gemma-4-31b-it:free/endpoints
- https://openrouter.ai/api/v1/models/mistralai/mistral-large-4-0/endpoints
- https://openrouter.ai/api/v1/models/openai/gpt-6-astra/endpoints
- https://openrouter.ai/api/v1/models/openai/gpt-6-luna/endpoints
- https://openrouter.ai/api/v1/models/openai/gpt-6-sol/endpoints
- https://openrouter.ai/api/v1/models/openai/gpt-6.1-sol/endpoints
- https://openrouter.ai/api/v1/models/stepfun/step-5-preview/endpoints
- https://openrouter.ai/api/v1/models/x-ai/grok-4.6/endpoints
- https://openrouter.ai/api/v1/models/x-ai/grok-4.7/endpoints
- https://openrouter.ai/api/v1/models/xiaomi/mimo-v2.6-flash/endpoints
- https://openrouter.ai/api/v1/models/xiaomi/mimo-v2.6-pro/endpoints
- https://openrouter.ai/docs/api_reference/responses/overview
- https://openrouter.ai/docs/guides/best-practices/reasoning-tokens
- https://openrouter.ai/docs/guides/routing/provider-selection
- https://openrouter.ai/google/gemma-4-31b-it:free
- https://platform.claude.com/docs/en/about-claude/pricing
- https://platform.claude.com/docs/en/build-with-claude/effort
- https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback
- https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan
- https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code
- https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-and-team-plans
- https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings
- https://support.google.com/gemini/answer/16275805
- https://support.google.com/gemini/answer/16275805?gl=US&hl=en
- https://www.anthropic.com/claude-haiku-5-5
- https://www.anthropic.com/claude-opus-5-5
- https://www.anthropic.com/claude-sonnet-5-5
