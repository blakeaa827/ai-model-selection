# AI model selection — October 28, 2026

**Default API floor:** GPT-6.1 Terra / low — **29.217**, **$0.071338 per AA task**. **Optional ceiling:** GPT-6.1 Terra / medium — **38.115**, **$0.168805**.

## Changes since the last published report

Refreshed 13 paid configurations and 0 opt-in free configurations. 0 numerical source revisions; 0 new and 8 absent gateway listings; 1 new AA releases since 2026-10-28. New candidates require exact effort/revision correspondence before routing.

Previous report: 2026-10-28; common Intelligence Index v5.0. Frontier membership unchanged; floor and ceiling unchanged.

Reverified same-day snapshot; previous version is preserved in Git history.

9 gateway token-price changes are recorded in latest.json changes_since_previous.gateway_token_pricing_changes. These are separate from AA measured task costs; provider changes, promotions and time-of-day rates do not authorize repricing an AA configuration. Automatic/latest aliases are never actionable.

Benchmark source: [Artificial Analysis](https://artificialanalysis.ai/). Original project code and documentation: [MIT](LICENSE). See [DATA-SOURCES.md](DATA-SOURCES.md) for attribution and the deferred source-data rights review.


Screened **456 live gateway listings**, **517 AA releases**, **80 exact model records**, and **16 free listings**. Every listing is inventoried; this does not mean every model has comparable measurements.

New gateway listings: none. Removed listings: `openai/gpt-4-turbo`, `openai/o1`, `openai/o1-pro`, `openai/o3-mini`, `openai/o3-mini-high`, `openai/o4-mini`, `openai/o4-mini-high`, `qwen/qwen3-next-80b-a3b-thinking`. Absence from a gateway is not proof of provider-wide retirement.

Newly observed AA release entries: gemini-4-carbon. These can include a newly identified revision of an older release.

The Intelligence Index measures broad capability, not percentage knowledge or a request's probability of success. These costs are AA's weighted benchmark-task costs from observed token use and published prices, not guaranteed prompt prices, OpenRouter invoices or spending caps. Numerical precision is retained for lookup; close score differences are not proof of statistical significance.

## Minimum cost meeting a capability target

Intervals are continuous: the first lower bound is inclusive, later lower bounds are exclusive, and all upper bounds are inclusive. Round only for display, and use latest.json for machine selection.

| Minimum-score range | request.model | request.reasoning | Delivered score | USD / AA task |
|---|---|---|---:|---:|
| [0, 9.66610812336462] | `openai/gpt-6-luna` | `{"effort":"low"}` | 9.666 | $0.005115 |
| (9.66610812336462, 18.3042156192416] | `openai/gpt-6-luna` | `{"effort":"medium"}` | 18.304 | $0.042202 |
| (18.3042156192416, 29.2169280792131] | `openai/gpt-6.1-terra` | `{"effort":"low"}` | 29.217 | $0.071338 |
| (29.2169280792131, 34.502924431456] | `openai/gpt-6.1-sol` | `{"effort":"low"}` | 34.503 | $0.161474 |
| (34.502924431456, 38.1152076677975] | `openai/gpt-6.1-terra` | `{"effort":"medium"}` | 38.115 | $0.168805 |
| (38.1152076677975, 42.3344508712563] | `openai/gpt-6.1-terra` | `{"effort":"high"}` | 42.334 | $0.259280 |
| (42.3344508712563, 46.1468797067114] | `openai/gpt-6.1-sol` | `{"effort":"medium"}` | 46.147 | $0.359390 |
| (46.1468797067114, 50.2291231936536] | `openai/gpt-6.1-sol` | `{"effort":"high"}` | 50.229 | $0.590985 |
| (50.2291231936536, 52.308219253291] | `openai/gpt-6.1-sol` | `{"effort":"xhigh"}` | 52.308 | $0.763995 |
| (52.308219253291, 54.5087338138148] | `openai/gpt-6.1-sol` | `{"effort":"max"}` | 54.509 | $1.272063 |
| (54.5087338138148, 54.849838322506] | `openai/gpt-6-astra` | `{"effort":"high"}` | 54.850 | $3.238572 |
| (54.849838322506, 55.2557468569681] | `openai/gpt-6-astra` | `{"effort":"xhigh"}` | 55.256 | $3.658926 |
| (55.2557468569681, 56.8538559596797] | `openai/gpt-6-astra` | `{"effort":"max"}` | 56.854 | $6.244667 |

No eligible verified configuration meets a score above 56.8538559596797.

## Most capability within a benchmark-task budget

| Budget interval, USD / AA task | request.model | request.reasoning | Delivered score |
|---|---|---|---:|
| [0.005115255188520391, 0.042201836106537785) | `openai/gpt-6-luna` | `{"effort":"low"}` | 9.666 |
| [0.042201836106537785, 0.07133756205169729) | `openai/gpt-6-luna` | `{"effort":"medium"}` | 18.304 |
| [0.07133756205169729, 0.16147357831822573) | `openai/gpt-6.1-terra` | `{"effort":"low"}` | 29.217 |
| [0.16147357831822573, 0.16880458238389412) | `openai/gpt-6.1-sol` | `{"effort":"low"}` | 34.503 |
| [0.16880458238389412, 0.2592796466169722) | `openai/gpt-6.1-terra` | `{"effort":"medium"}` | 38.115 |
| [0.2592796466169722, 0.3593898648025732) | `openai/gpt-6.1-terra` | `{"effort":"high"}` | 42.334 |
| [0.3593898648025732, 0.5909853515780825) | `openai/gpt-6.1-sol` | `{"effort":"medium"}` | 46.147 |
| [0.5909853515780825, 0.7639949356156494) | `openai/gpt-6.1-sol` | `{"effort":"high"}` | 50.229 |
| [0.7639949356156494, 1.2720632679446995) | `openai/gpt-6.1-sol` | `{"effort":"xhigh"}` | 52.308 |
| [1.2720632679446995, 3.2385719685518306) | `openai/gpt-6.1-sol` | `{"effort":"max"}` | 54.509 |
| [3.2385719685518306, 3.6589264906126227) | `openai/gpt-6-astra` | `{"effort":"high"}` | 54.850 |
| [3.6589264906126227, 6.244666943602518) | `openai/gpt-6-astra` | `{"effort":"xhigh"}` | 55.256 |
| [6.244666943602518, ∞) | `openai/gpt-6-astra` | `{"effort":"max"}` | 56.854 |

## Exact revision and route contract

Every request uses `provider.require_parameters=true`, `provider.allow_fallbacks=false`, and exactly one verified provider tag. Standard endpoint prices and parameters are checked; a different revision, quantization, unsupported setting or stale report causes rejection. No generation calls or keys are embedded in these reports.

| Callable model | Canonical revision | provider.only | API surface |
|---|---|---|---|
| `openai/gpt-6-luna` | `openai/gpt-6-luna-20260922` | `openai` | `responses` |
| `openai/gpt-6.1-terra` | `openai/gpt-6.1-terra-20261026` | `openai` | `responses` |
| `openai/gpt-6.1-sol` | `openai/gpt-6.1-sol-20260929` | `openai` | `responses` |
| `openai/gpt-6-astra` | `openai/gpt-6-astra-20260903` | `openai` | `responses` |

MiMo uses `reasoning.enabled=true`, corresponding to native `thinking.type=enabled`; its metadata effort is null and is omitted from the actual request. Named non-none MiMo efforts do not define different thinking intensities. Preserve reasoning details across tool turns, omit unsupported sampling controls and allow sufficient output tokens. Provider token prices are recorded separately from AA measured task costs.

## Free lane: explicit opt-in


Other free listings remain pending unless the exact revision, reasoning state, first-party route and independently measured zero-cost basis match. A gateway token price of zero is not sufficient evidence of AA task cost zero.

## Marginal costs, floor and ceiling

Workload-conditional floor: next step adds 5.285996 points for $0.090136 (+126.35%), $0.017052/point, 6.39x the preceding marginal rate. Compare actual success rate, latency and review effort before paying above it.

Workload-conditional ceiling: next step adds 4.219243 points for $0.090475 (+53.60%), $0.021443/point, 10.57x the preceding marginal rate. Compare actual success rate, latency and review effort before paying above it.

The recommendation heuristic uses the first ≥3× rise in adjacent marginal dollars per point accompanied by ≥50% higher task cost as a candidate floor, and the next such cliff as an optional ceiling. All steps are evaluated. These are workload-conditional starting points, not universal optima. Index intervals need not have equal practical value. Smaller local bends and model-family transitions remain visible below.

| Upgrade to | Index point gain | Added USD/task | Cost increase | Added USD/point | Relative to previous marginal rate |
|---|---:|---:|---:|---:|---:|
| GPT-6 Luna / medium | 8.638107 | $0.037087 | 725.02% | $0.004293 | — |
| GPT-6.1 Terra / low | 10.912712 | $0.029136 | 69.04% | $0.002670 | 0.62× |
| GPT-6.1 Sol / low | 5.285996 | $0.090136 | 126.35% | $0.017052 | 6.39× |
| GPT-6.1 Terra / medium | 3.612283 | $0.007331 | 4.54% | $0.002029 | 0.12× |
| GPT-6.1 Terra / high | 4.219243 | $0.090475 | 53.60% | $0.021443 | 10.57× |
| GPT-6.1 Sol / medium | 3.812429 | $0.100110 | 38.61% | $0.026259 | 1.22× |
| GPT-6.1 Sol / high | 4.082243 | $0.231595 | 64.44% | $0.056732 | 2.16× |
| GPT-6.1 Sol / xhigh | 2.079096 | $0.173010 | 29.27% | $0.083214 | 1.47× |
| GPT-6.1 Sol / max | 2.200515 | $0.508068 | 66.50% | $0.230886 | 2.77× |
| GPT-6 Astra / high | 0.341105 | $1.966509 | 154.59% | $5.765121 | 24.97× |
| GPT-6 Astra / xhigh | 0.405909 | $0.420355 | 12.98% | $1.035589 | 0.18× |
| GPT-6 Astra / max | 1.598109 | $2.585740 | 70.67% | $1.618000 | 1.56× |

Pay above the ceiling when difficult debugging, architecture, research, avoidable failures or human review are worth the additional cost. For simple, repeatable work, select the cheapest model meeting a measured workload success target. Do not convert an evaluator's 0–1 success probability directly into this index.

![Measured cost versus capability](cost-curve.svg)

## Excluded or pending evidence

Haiku 5.5 costs remain provisional because AA's article still omits tiered pricing above 100K input tokens. Its prerelease refusal issue and Sonnet's structured-output reruns are not confirmed complete. Their measured scores are retained without assigning actionable request costs. Kimi K3.1 Pro has a measured pair, but AA's current record does not identify the effort used; its native default alone is insufficient proof. Current exact model cost also differs from the launch article. No guessed mapping is admitted.

| Model or configuration | Measured score if available | Task cost if complete | Exclusion / uncertainty |
|---|---:|---:|---|
| Gemini 4 Argon  | — | — | API generally available October 13, 2026 and gateway revision 20261013 now listed. AA September 30 deployment-to-GA correspondence remains unverified; earlier AA high-effort score/cost is also dominated by Opus high. Do not claim the model is still restricted-only. |
| Grok 4.7 medium | — | — | Supported by OpenRouter but no comparable published score/task-cost pair in current comparison. |
| Gemini 3.8 Flash low | — | — | Published score but missing benchmark task cost. |
| GPT-6.1 Sol Pro  | — | — | Listed by OpenRouter; standard Sol effort benchmarks do not establish Pro-mode score or task cost. |
| Anthropic: Claude Sonnet 5.5 (batch)  | — | — | Pro mode or Batch billing configuration lacks a verified comparable AA score/cost pair; standard results are not reused. |
| OpenAI: GPT-6 Luna Pro  | — | — | Pro mode or Batch billing configuration lacks a verified comparable AA score/cost pair; standard results are not reused. |
| OpenAI: GPT-6 Luna Pro (batch)  | — | — | Pro mode or Batch billing configuration lacks a verified comparable AA score/cost pair; standard results are not reused. |
| OpenAI: GPT-6 Luna (batch)  | — | — | Pro mode or Batch billing configuration lacks a verified comparable AA score/cost pair; standard results are not reused. |
| OpenAI: GPT-6 Sol Pro  | — | — | Pro mode or Batch billing configuration lacks a verified comparable AA score/cost pair; standard results are not reused. |
| OpenAI: GPT-6 Sol Pro (batch)  | — | — | Pro mode or Batch billing configuration lacks a verified comparable AA score/cost pair; standard results are not reused. |
| OpenAI: GPT-6 Sol (batch)  | — | — | Pro mode or Batch billing configuration lacks a verified comparable AA score/cost pair; standard results are not reused. |
| Anthropic: Claude Opus 5.5 (batch)  | — | — | Pro mode or Batch billing configuration lacks a verified comparable AA score/cost pair; standard results are not reused. |
| OpenAI: GPT-6 Astra (batch)  | — | — | Pro mode or Batch billing configuration lacks a verified comparable AA score/cost pair; standard results are not reused. |
| OpenAI: GPT-6 Astra Pro  | — | — | Pro mode or Batch billing configuration lacks a verified comparable AA score/cost pair; standard results are not reused. |
| OpenAI: GPT-6 Astra Pro (batch)  | — | — | Pro mode or Batch billing configuration lacks a verified comparable AA score/cost pair; standard results are not reused. |
| Mistral Large 4 Preview  | — | — | AA now reports score 38 and $1.13/task for a reasoning configuration, but does not identify the exact effort. It is also strictly dominated by GPT-6 Luna max at the same score for $0.07/task. Measured but non-actionable; excluded from routing. |
| Claude Sonnet 5.5  | — | — | Prerelease structured-output bug is disclosed by AA; no confirmed public-release rerun. All current pairs would also be cost-dominated. |
| Gemini 3.8 Flash Cyber  | — | — | Restricted Fairwind access; no verified callable OpenRouter ID or comparable task-cost pair. |
| Gemini 3.5 Flash-Lite / Gemini 3.1 Pro Preview  | — | — | Historical AA score/cost pairs are retained in evaluated_configurations, but exact effort labels are unverified. No defaults inferred. |
| Grok 4.6  | — | — | Artificial Analysis marks Grok 4.6 deprecated and recommends Grok 4.7. Measurements are retained for audit but excluded from actionable routing. |
| Claude Haiku 5.5 max | 36.2345435880142 | — | AA October 7 evaluator article explicitly says task costs are provisional and omit the 5x price tier above 100K input tokens. AutomationBench-AA prerelease safety over-refusal issue awaits rerun. Excluded until comparable complete task costs and deployment status are verified. |
| Claude Haiku 5.5 xhigh | 34.3387759486628 | — | AA October 7 evaluator article explicitly says task costs are provisional and omit the 5x price tier above 100K input tokens. AutomationBench-AA prerelease safety over-refusal issue awaits rerun. Excluded until comparable complete task costs and deployment status are verified. |
| Claude Haiku 5.5 high | 29.624315467743 | — | AA October 7 evaluator article explicitly says task costs are provisional and omit the 5x price tier above 100K input tokens. AutomationBench-AA prerelease safety over-refusal issue awaits rerun. Excluded until comparable complete task costs and deployment status are verified. |
| Claude Haiku 5.5 medium | 24.5513254343023 | — | AA October 7 evaluator article explicitly says task costs are provisional and omit the 5x price tier above 100K input tokens. AutomationBench-AA prerelease safety over-refusal issue awaits rerun. Excluded until comparable complete task costs and deployment status are verified. |
| Claude Haiku 5.5 low | 18.6180055310996 | — | AA October 7 evaluator article explicitly says task costs are provisional and omit the 5x price tier above 100K input tokens. AutomationBench-AA prerelease safety over-refusal issue awaits rerun. Excluded until comparable complete task costs and deployment status are verified. |
| Step 5 Preview  | — | — | New gateway listing; exact AA revision/effort correspondence and price basis unverified. Existing AA release result is dominated; no benchmark score assigned to low/medium/high routing. |
| GPT-6.1 Sol Batch  | — | — | New listing, same canonical revision as standard Sol but different processing tier. No independently measured batch weighted task costs; standard scores/costs not transferred. |
| GPT-6.1 Sol Pro Batch  | — | — | New batch listing; Pro mode and processing tier lack an exact common-index score/task-cost pair. Standard-mode benchmarks not transferred. |
| Ling 3.0 Flash Sante  | — | — | New paid gateway listing; no exact common-index score/task-cost pair in the current AA registry. Its former free listing is no longer in the live catalog. |
| GPT-6 Sol Daybreak Blue  | — | — | Restricted Daybreak-program access. Cyber Index evaluation is a different harness and cost basis, not the Intelligence Index; no common-index pair or public gateway route. |
| Gemma 4 31B (Reasoning, limited free route)  | — | — | Free route lacks a measured, non-estimated zero-cost pair on the current common index version. Prior-version result cannot be reused. |
| Claude Opus 5.5 (Max, Default Fallback) max | 58.4060336078904 | $10.036409719512749 | AA labels this configuration Default Fallback. A pinned single-model OpenRouter request does not reproduce the measured fallback system. |
| Claude Opus 5.5 (High, Default Fallback) high | 51.6859958227294 | $3.4646622820973185 | AA labels this configuration Default Fallback. A pinned single-model OpenRouter request does not reproduce the measured fallback system. |
| Claude Opus 5.5 (Low, Default Fallback) low | 34.502785007759 | $0.9755293224458845 | AA labels this configuration Default Fallback. A pinned single-model OpenRouter request does not reproduce the measured fallback system. |
| Claude Opus 5.5 (Medium, Default Fallback) medium | 48.0581024960691 | $2.4510894376611723 | AA labels this configuration Default Fallback. A pinned single-model OpenRouter request does not reproduce the measured fallback system. |
| Claude Opus 5.5 (Xhigh, Default Fallback) xhigh | 56.9947060170507 | $6.047194490848774 | AA labels this configuration Default Fallback. A pinned single-model OpenRouter request does not reproduce the measured fallback system. |
| Claude Sonnet 5.5 (Max, Default Fallback) max | 54.24133407109 | $10.020621343395753 | AA labels this configuration Default Fallback. A pinned single-model OpenRouter request does not reproduce the measured fallback system. |
| Claude Sonnet 5.5 (High, Default Fallback) high | 41.115109087048 | $1.6361294399784785 | AA labels this configuration Default Fallback. A pinned single-model OpenRouter request does not reproduce the measured fallback system. |
| Claude Sonnet 5.5 (Low, Default Fallback) low | 25.299704549789 | $0.5113424463897498 | AA labels this configuration Default Fallback. A pinned single-model OpenRouter request does not reproduce the measured fallback system. |
| Claude Sonnet 5.5 (Medium, Default Fallback) medium | 30.3195522148431 | $0.7806560352024481 | AA labels this configuration Default Fallback. A pinned single-model OpenRouter request does not reproduce the measured fallback system. |
| Claude Sonnet 5.5 (Xhigh, Default Fallback) xhigh | 49.5740327787242 | $4.091984916321919 | AA labels this configuration Default Fallback. A pinned single-model OpenRouter request does not reproduce the measured fallback system. |
| Agnes 2.5 Pro Beta  | — | — | AA score is estimated or measured weighted task cost is missing; not a comparable measured score/cost pair. Pending benchmarks; no actionable request or effort mapping. |
| Command A+  | 6.24120025576958 | $0 | Measured original-source pair; exact benchmark reasoning control, revision and public provider-route correspondence not verified. No request or effort invented. |
| DeepSeek V4.1 Flash 1017 (Max)  | 32.4896393532027 | $0.60210514783598 | Measured original-source pair; exact benchmark reasoning control, revision and public provider-route correspondence not verified. No request or effort invented. |
| Gemini 4 Carbon (High)  | 59.425738829526 | $7.755545745286556 | Measured original-source pair; exact benchmark reasoning control, revision and public provider-route correspondence not verified. No request or effort invented. |
| Gemma 4 31B (Reasoning)  | — | — | AA score is estimated or measured weighted task cost is missing; not a comparable measured score/cost pair. Pending benchmarks; no actionable request or effort mapping. |
| K2 Horizon 375B A23B  | 17.7702731734027 | $0 | Measured original-source pair; exact benchmark reasoning control, revision and public provider-route correspondence not verified. No request or effort invented. |
| Kimi K3.1 Pro  | 46.0026236744189 | $3.6812002895742055 | AA publishes an unlabeled reasoning configuration, with no explicit effort in its exact record. Native default is max, but this is not proof of the effort used by AA. Gateway additionally advertises none despite official always-on thinking. Standard first-party MXFP4 route exists; benchmark effort/deployment correspondence remains pending. Current model task cost $2.1145052918767275 differs from launch article $1.98; current exact record takes precedence. Weights promised by November 4 are not yet available. |
| LFM2.5-2.6B  | — | — | AA score is estimated or measured weighted task cost is missing; not a comparable measured score/cost pair. Pending benchmarks; no actionable request or effort mapping. |
| Ling 3.0 Tiny  | — | — | AA score is estimated or measured weighted task cost is missing; not a comparable measured score/cost pair. Pending benchmarks; no actionable request or effort mapping. |
| Ling 3.1 Flash 1019  | 29.470119369837 | $3.185145018337793 | Measured original-source pair; exact benchmark reasoning control, revision and public provider-route correspondence not verified. No request or effort invented. |
| MiniMax-M3.1-Flash  | 28.9095214290458 | $0.49097067348453205 | Measured original-source pair; exact benchmark reasoning control, revision and public provider-route correspondence not verified. No request or effort invented. |
| Muse Spark Open (Xhigh)  | 24.6815868992913 | $2.0176680435839316 | Measured original-source pair; exact benchmark reasoning control, revision and public provider-route correspondence not verified. No request or effort invented. |
| Muse Wonder (Max)  | 43.3248225998431 | $6.9520364786062245 | Measured original-source pair; exact benchmark reasoning control, revision and public provider-route correspondence not verified. No request or effort invented. |
| Muse Wonder Full (Max)  | 49.7272123627021 | — | AA score is estimated or measured weighted task cost is missing; not a comparable measured score/cost pair. Pending benchmarks; no actionable request or effort mapping. |
| Nemotron 3.5 Bolt 74B-A9B  | — | — | AA score is estimated or measured weighted task cost is missing; not a comparable measured score/cost pair. Pending benchmarks; no actionable request or effort mapping. |
| Nemotron 3.5 Bolt E4B 4GB (Reasoning)  | — | — | AA score is estimated or measured weighted task cost is missing; not a comparable measured score/cost pair. Pending benchmarks; no actionable request or effort mapping. |
| Nemotron 3.5 Super VL  | 13.6203422723141 | $0.5565160431921087 | Measured original-source pair; exact benchmark reasoning control, revision and public provider-route correspondence not verified. No request or effort invented. |
| North Mini Code  | — | — | AA score is estimated or measured weighted task cost is missing; not a comparable measured score/cost pair. Pending benchmarks; no actionable request or effort mapping. |
| Beam 1.0  | 17.7307282547205 | $0.28440671352465285 | Measured original-source pair; exact benchmark reasoning control, revision and public provider-route correspondence not verified. No request or effort invented. |
| Solar Pro 4  | — | — | AA score is estimated or measured weighted task cost is missing; not a comparable measured score/cost pair. Pending benchmarks; no actionable request or effort mapping. |

Gemini 4 Argon API became generally available October 13; the live gateway revision is now 20261013. The September 30 restricted-release benchmark is not silently attached to that GA revision. Its earlier high-effort pair is also dominated by Opus high. Introductory token prices expire November 30 according to Google's current guide; token rates are not substituted for measured task costs. The old Fairwind announcement is historical rollout context.

## Build through subscription services

Personal tiers and account menus are unknown. All subscription scores and task costs are null unless separately measured in the exact app/agent harness. UI Standard/Extended, Heavy/Deep Think and Ultra are not mapped to API efforts or single-model API scores.

| Service | Routine default | Escalation | Quota-saving choice | Source check complete |
|---|---|---|---|---|
| OpenAI | GPT-6.1 Sol; `{"reasoning_effort":"medium","ui_label":"Medium","speed":"Standard"}` | GPT-6.1 Sol; `{"reasoning_effort":"xhigh","ui_label":"Extra High","speed":"Standard"}` | GPT-6.1 Terra; `{"ui_or_cli_effort":null,"note":"Exact subscription effort labels not verified; no API effort or benchmark correspondence assumed."}` | False |
| Claude | Claude Sonnet 5.5; `{"effort":"high","ui_label":"High","thinking":"always_on_in_Claude"}` | Claude Opus 5.5; `{"effort":"xhigh","ui_label":"Extra high","thinking":"always_on"}` | Claude Haiku 5.5; `{"effort":"low","ui_label":"Low","thinking":"always_on_in_Claude"}` | False |
| Grok | Grok 4.7; `{"selection":"documented default model","effort":null,"ui_to_api_effort_mapping":"unverified","speed":"standard"}` | Grok account higher-reasoning mode; `{"selection":"only the higher-reasoning option actually exposed by the account","effort":null,"ui_to_api_effort_mapping":"unverified"}` | Grok 4.7 standard mode; `{"selection":"standard rather than Fast","effort":null,"ui_to_api_effort_mapping":"unverified"}` | True |
| Gemini | Gemini 3.8 Flash; `{"ui_thinking":"Standard where exposed","api_effort_mapping":null}` | Gemini 3.8 Flash with Extended thinking; `{"ui_thinking":"Extended where exposed","api_effort_mapping":null}` | Gemini Flash-Lite; `{"ui_thinking":"Standard where exposed","api_effort_mapping":null}` | True |

**OpenAI:** Work and Codex share allowances. Fast uses 2.5x included allowance relative to Standard. Included tasks vary by context, effort and tools; use account dashboard. API rates are separate.
Unverified this run: https://openai.com/index/introducing-gpt-6-1-terra/. Previous verification dates are retained.

**Claude:** Claude and Claude Code share plan limits; higher effort uses more quota. An ANTHROPIC_API_KEY can cause API billing instead of subscription usage. Personal tier not known. Eligible Max/Team can separately claim monthly Claude Platform API credits; first-party only, personal eligibility/claim status unknown.
Unverified this run: https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings, https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code, https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan, https://www.anthropic.com/claude-haiku-5-5, https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-and-team-plans. Previous verification dates are retained.

**Grok:** Consumer FAQ describes a shared weekly pool and paid extra usage. Bot launch docs describe its own usage pool, so keep Bot separate and check its dashboard; do not assume identical accounting. API credits are separate. Exact consumer reasoning control not verified.

**Gemini:** Models/thinking consume differing allowance. Generic Help still lists Gemini 3 families while September launch explicitly grants 3.8 Flash to Pro/Ultra; prefer launch for exact revision, Help for controls. Gemini 4 Argon is restricted Fairwind rollout, not assumed consumer subscription access. Gemini 4 Argon API is GA as of October 13; consumer-plan and exact UI access remain conditional. Do not use the older Fairwind launch announcement as proof that current API access is restricted. Gemini 4 Argon API is GA as of October 13; consumer-plan and exact UI access remain conditional. Do not use the older Fairwind launch announcement as proof that current API access is restricted.

Eligible Claude Max/Team users can claim first-party API credits; eligibility depends on exact plan, claim and linked Console organization. These credits do not pay OpenRouter invoices. No personal entitlement is assumed.

## Verification and freshness

Checked 2026-10-28T17:44:27.375098+00:00 (report date in America/Chicago). AA v5.0; exact evaluation completion dates remain unpublished. Catalog checked 2026-10-28T17:43:54.038860+00:00; registry checked 2026-10-28T17:43:54.190733+00:00. Each score, route and source has its own successful verification timestamp. Reports and actionable rows expire after 48 hours. Unsuccessful source checks are disclosed and not advanced.

Source sites, original configuration data and endpoint metadata are required inputs. New releases with unverified benchmark controls remain pending and do not inherit another revision's results. Release maxima and cost minima are optimistic screening bounds, never a fabricated configuration pair. See coverage.json for the entire inventory and latest.json for exact intervals and eligibility.

## Workload-specific routing

The new [workload charts](workloads.md) and [workload JSON](workloads.json) provide six independently measured score/cost frontiers, exact routing and separate candidate floors/ceilings. Use `select-workload.mjs` with an explicit workload. Complete coding-agent systems and pending profiles are separate; no benchmark score is converted directly into a Jev success probability.

AA now labels Opus 5.5 measurements as **Default Fallback**. Those multi-model measurements are excluded from the pinned single-model frontier. Astra configurations that become undominated are checked on the standard first-party route. The general floor and ceiling are recomputed from the retained configurations.

## Sources

- https://ai.google.dev/gemini-api/docs/changelog
- https://ai.google.dev/gemini-api/docs/latest-model
- https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash
- https://ai.google.dev/gemini-api/docs/pricing
- https://ai.google.dev/gemma/docs/capabilities/thinking
- https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v5
- https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra
- https://artificialanalysis.ai/articles/benchmarking-grok-4-7
- https://artificialanalysis.ai/articles/claude-haiku-5-5
- https://artificialanalysis.ai/articles/claude-opus-5-5
- https://artificialanalysis.ai/articles/claude-sonnet-5-5
- https://artificialanalysis.ai/articles/gemini-4-argon-google-top-three-labs
- https://artificialanalysis.ai/articles/gpt-6-1-sol-replaces-gpt-6-sol-after-just-7-days-with-near-astra-intelligence
- https://artificialanalysis.ai/articles/gpt-6-1-terra-pushes-the-cost-efficiency-frontier
- https://artificialanalysis.ai/articles/gpt-6-sol-and-luna-push-the-cost-efficiency-frontier
- https://artificialanalysis.ai/articles/harvey-lab-aa-v1-1
- https://artificialanalysis.ai/articles/kimi-k3-1-pro-launch-benchmarks
- https://artificialanalysis.ai/articles/trusted-access-models-cyber-index
- https://artificialanalysis.ai/changelog
- https://artificialanalysis.ai/methodology/intelligence-benchmarking
- https://artificialanalysis.ai/models
- https://artificialanalysis.ai/models/agnes-2-5-pro-beta
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
- https://artificialanalysis.ai/models/deepseek-v4-1-flash-1017
- https://artificialanalysis.ai/models/gemini-3-1-pro-preview
- https://artificialanalysis.ai/models/gemini-3-5-flash-lite
- https://artificialanalysis.ai/models/gemini-3-8-flash
- https://artificialanalysis.ai/models/gemini-3-8-flash-low
- https://artificialanalysis.ai/models/gemini-3-8-flash-medium
- https://artificialanalysis.ai/models/gemini-4-argon
- https://artificialanalysis.ai/models/gemini-4-carbon
- https://artificialanalysis.ai/models/gemma-4-31b
- https://artificialanalysis.ai/models/gpt-6-1-sol
- https://artificialanalysis.ai/models/gpt-6-1-sol-high
- https://artificialanalysis.ai/models/gpt-6-1-sol-low
- https://artificialanalysis.ai/models/gpt-6-1-sol-medium
- https://artificialanalysis.ai/models/gpt-6-1-sol-xhigh
- https://artificialanalysis.ai/models/gpt-6-1-terra
- https://artificialanalysis.ai/models/gpt-6-1-terra-high
- https://artificialanalysis.ai/models/gpt-6-1-terra-low
- https://artificialanalysis.ai/models/gpt-6-1-terra-medium
- https://artificialanalysis.ai/models/gpt-6-1-terra-non-reasoning
- https://artificialanalysis.ai/models/gpt-6-1-terra-xhigh
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
- https://artificialanalysis.ai/models/kimi-k3-1-pro
- https://artificialanalysis.ai/models/lfm2-5-2-6b
- https://artificialanalysis.ai/models/ling-3-0-tiny
- https://artificialanalysis.ai/models/ling-3-1-flash-1019
- https://artificialanalysis.ai/models/mimo-v2-6-flash
- https://artificialanalysis.ai/models/mimo-v2-6-pro
- https://artificialanalysis.ai/models/minimax-m3-1-flash
- https://artificialanalysis.ai/models/mistral-large-4
- https://artificialanalysis.ai/models/muse-spark-open
- https://artificialanalysis.ai/models/muse-wonder
- https://artificialanalysis.ai/models/muse-wonder-full
- https://artificialanalysis.ai/models/nemotron-3-5-bolt-74b-a9b
- https://artificialanalysis.ai/models/nemotron-3-5-bolt-e4b-4gb
- https://artificialanalysis.ai/models/nemotron-3-5-super-vl
- https://artificialanalysis.ai/models/north-mini-code
- https://artificialanalysis.ai/models/reflection-beam
- https://artificialanalysis.ai/models/releases
- https://artificialanalysis.ai/models/releases/claude-haiku-5-5
- https://artificialanalysis.ai/models/releases/claude-opus-5-5
- https://artificialanalysis.ai/models/releases/claude-sonnet-5-5
- https://artificialanalysis.ai/models/releases/comparisons/gpt-6-1-sol-vs-gpt-6-astra
- https://artificialanalysis.ai/models/releases/gemini-3-8-flash
- https://artificialanalysis.ai/models/releases/gpt-6-1-sol
- https://artificialanalysis.ai/models/releases/gpt-6-luna
- https://artificialanalysis.ai/models/releases/grok-4-7
- https://artificialanalysis.ai/models/solar-pro4
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
- https://developers.openai.com/api/docs/models/gpt-6.1-terra
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
- https://openai.com/index/introducing-gpt-6-1-terra/
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
- https://openrouter.ai/api/v1/models/openai/gpt-6.1-terra/endpoints
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
- https://platform.kimi.ai/docs/guide/kimi-k3-1-pro-quickstart
- https://platform.kimi.ai/docs/pricing/chat
- https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan
- https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code
- https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-and-team-plans
- https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings
- https://support.google.com/gemini/answer/16275805
- https://support.google.com/gemini/answer/16275805?gl=US&hl=en
- https://www.anthropic.com/claude-haiku-5-5
- https://www.anthropic.com/claude-opus-5-5
- https://www.anthropic.com/claude-sonnet-5-5
- https://www.kimi.ai/blog/kimi-k3-1-pro
- https://www.liquid.ai/blog/lfm2-5-2-6b
