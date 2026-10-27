# Workload-specific model selection — 2026-10-27

Benchmark source: [Artificial Analysis](https://artificialanalysis.ai/). Original project code and documentation: [MIT](LICENSE). See [DATA-SOURCES.md](DATA-SOURCES.md) for attribution and the deferred data-rights review.

Each profile has its own benchmark score, measured evaluation task cost, harness and Pareto frontier. Scores and budgets are meaningful only within that profile. The general Intelligence Index remains in [latest.md](latest.md).

Screened **715 public AA configurations** and **463 OpenRouter entries**; acquired **272 active exact records**. Exact routing correspondence is incomplete. These are the best observed verified pairs, not proof of global optimality. All eligible configurations are reconsidered per workload, including those dominated in the general chart.

**Floor and ceiling are candidate value knees, not validated deployment defaults.** A cheap model scoring poorly can have an early cost knee. Supply a workload quality target or use a score/budget query; no application success threshold or calibrated Jev predictor has been supplied. Close score gaps may reflect evaluation noise. Dollars per score point are descriptive, and Elo/benchmark intervals need not have equal practical value.

Source checks completed at 2026-10-27T14:14:38.974439+00:00. Routing evidence expires after 48 hours. Missing or mismatched configurations fail without a substitute.

![Workload cost versus capability curves](workloads/cost-curves.svg)

## Candidate floor and ceiling by workload

| Workload | Benchmark and score unit | Candidate floor | Optional ceiling |
|---|---|---|---|
| [Coding and terminal execution](#coding-terminal) | Terminal-Bench 4.0; pass_at_1_percent | `openai/gpt-6.1-terra / {"effort":"low"}`; 15.152; $0.106601/task | `openai/gpt-6.1-terra / {"effort":"medium"}`; 32.323; $0.275657/task |
| [Business workflow automation](#business-automation) | AutomationBench-AA AA-II-4.3.2; guardrail_adjusted_objective_completion_percent | `xiaomi/mimo-v2.6-flash / {"enabled":true}`; 64.052; $0.016656/task | `openai/gpt-6.1-sol / {"effort":"xhigh"}`; 66.574; $0.250558/task |
| [Documents, spreadsheets and professional work](#professional-work) | GDPval-AA 2.1; elo | `openai/gpt-6-luna / {"effort":"medium"}`; 1270.950; $0.016936/task | `xiaomi/mimo-v2.6-flash / {"enabled":true}`; 1615.210; $0.073176/task |
| [Long-document reasoning](#long-context) | AA-LCR 1.1; pass_at_1_percent | `openai/gpt-6-luna / {"effort":"max"}`; 83.333; $0.010188/task | `openai/gpt-6-luna / {"effort":"max"}`; 83.333; $0.010188/task |
| [Reasoning over professional PDFs](#document-reasoning) | GDP.pdf (AA implementation) AA-II-4.3.2; all_criteria_pass_percent | `openai/gpt-6-luna / {"effort":"max"}`; 22.800; $0.028547/task | `openai/gpt-6.1-sol / {"effort":"high"}`; 32.000; $0.349401/task |
| [Advanced academic reasoning](#academic-reasoning) | Humanity's Last Exam (AA text subset) May-2025-text-2158/AA-II-4.3.2; pass_at_1_percent | `openai/gpt-6-luna / {"effort":"low"}`; 20.250; $0.000522/task | `openai/gpt-6.1-terra / {"effort":"low"}`; 35.820; $0.002952/task |

## coding-terminal

**Coding and terminal execution** — [Terminal-Bench](https://artificialanalysis.ai/evaluations/terminalbench-4-0), version `4.0`; score unit `pass_at_1_percent`; status `ready`.

Harness `aa-mini-swe-agent-terminalbench-4.0`: AA mini-swe-agent; 66 tasks, three repeats, 500-step limit, full transcript, upstream task timeouts.

Terminal execution is not the same as repository implementation, code review or an IDE coding agent.

AA evaluation-specific costPerTask from observed contestant token use and published prices; excludes unreported tools, judges, infrastructure and supervision. Not Intelligence Index weighted cost or an OpenRouter invoice estimate.

Verified candidates: 28; paid frontier: 13. Incomplete routing matches are retained as pending in workloads.json.

### Minimum cost for a minimum benchmark score

| Minimum-score interval | request.model | request.reasoning | Score | USD / this benchmark task |
|---|---|---|---:|---:|
| (−∞, 0] | `openai/gpt-6-luna` | `{"effort":"low"}` | 0.000 | $0.005448 |
| (0, 1.51515151515152] | `openai/gpt-6-luna` | `{"effort":"none"}` | 1.515 | $0.044621 |
| (1.51515151515152, 2.52525252525253] | `openai/gpt-6-luna` | `{"effort":"medium"}` | 2.525 | $0.071565 |
| (2.52525252525253, 15.151515151515198] | `openai/gpt-6.1-terra` | `{"effort":"low"}` | 15.152 | $0.106601 |
| (15.151515151515198, 22.727272727272698] | `xiaomi/mimo-v2.6-flash` | `{"enabled":true}` | 22.727 | $0.230158 |
| (22.727272727272698, 32.3232323232323] | `openai/gpt-6.1-terra` | `{"effort":"medium"}` | 32.323 | $0.275657 |
| (32.3232323232323, 41.9191919191919] | `openai/gpt-6.1-terra` | `{"effort":"high"}` | 41.919 | $0.437542 |
| (41.9191919191919, 47.979797979798] | `openai/gpt-6.1-sol` | `{"effort":"medium"}` | 47.980 | $0.613755 |
| (47.979797979798, 51.5151515151515] | `openai/gpt-6.1-sol` | `{"effort":"high"}` | 51.515 | $0.828177 |
| (51.5151515151515, 54.040404040404] | `openai/gpt-6.1-sol` | `{"effort":"xhigh"}` | 54.040 | $1.025949 |
| (54.040404040404, 55.5555555555556] | `openai/gpt-6.1-terra` | `{"effort":"max"}` | 55.556 | $1.485313 |
| (55.5555555555556, 56.0606060606061] | `openai/gpt-6.1-sol` | `{"effort":"max"}` | 56.061 | $1.822763 |
| (56.0606060606061, 59.5959595959596] | `openai/gpt-6-astra` | `{"effort":"xhigh"}` | 59.596 | $5.855483 |

The first lower bound is unbounded for lookup only; it does not give score zero a practical meaning. No verified configuration satisfies a score above the last row.

### Maximum score within a benchmark-task budget

| Budget interval, USD | request.model | request.reasoning | Score |
|---|---|---|---:|
| [0.005448337009257049, 0.0446207812657598) | `openai/gpt-6-luna` | `{"effort":"low"}` | 0.000 |
| [0.0446207812657598, 0.07156543103673528) | `openai/gpt-6-luna` | `{"effort":"none"}` | 1.515 |
| [0.07156543103673528, 0.1066009786508095) | `openai/gpt-6-luna` | `{"effort":"medium"}` | 2.525 |
| [0.1066009786508095, 0.23015839490323023) | `openai/gpt-6.1-terra` | `{"effort":"low"}` | 15.152 |
| [0.23015839490323023, 0.275657091680196) | `xiaomi/mimo-v2.6-flash` | `{"enabled":true}` | 22.727 |
| [0.275657091680196, 0.4375420474275898) | `openai/gpt-6.1-terra` | `{"effort":"medium"}` | 32.323 |
| [0.4375420474275898, 0.6137554705459501) | `openai/gpt-6.1-terra` | `{"effort":"high"}` | 41.919 |
| [0.6137554705459501, 0.8281767981765117) | `openai/gpt-6.1-sol` | `{"effort":"medium"}` | 47.980 |
| [0.8281767981765117, 1.0259491542428139) | `openai/gpt-6.1-sol` | `{"effort":"high"}` | 51.515 |
| [1.0259491542428139, 1.4853125323157166) | `openai/gpt-6.1-sol` | `{"effort":"xhigh"}` | 54.040 |
| [1.4853125323157166, 1.8227634618325743) | `openai/gpt-6.1-terra` | `{"effort":"max"}` | 55.556 |
| [1.8227634618325743, 5.855482520522051) | `openai/gpt-6.1-sol` | `{"effort":"max"}` | 56.061 |
| [5.855482520522051, ∞) | `openai/gpt-6-astra` | `{"effort":"xhigh"}` | 59.596 |

### Marginal upgrades

| Upgrade to | Score gain | Added USD/task | Cost increase | USD / added score point | Marginal rate multiple |
|---|---:|---:|---:|---:|---:|
| `openai/gpt-6-luna / {"effort":"none"}` | 1.515152 | $0.039172 | 718.98% | $0.025854 | — |
| `openai/gpt-6-luna / {"effort":"medium"}` | 1.010101 | $0.026945 | 60.39% | $0.026675 | 1.03× |
| `openai/gpt-6.1-terra / {"effort":"low"}` | 12.626263 | $0.035036 | 48.96% | $0.002775 | 0.10× |
| `xiaomi/mimo-v2.6-flash / {"enabled":true}` | 7.575758 | $0.123557 | 115.91% | $0.016310 | 5.88× |
| `openai/gpt-6.1-terra / {"effort":"medium"}` | 9.595960 | $0.045499 | 19.77% | $0.004741 | 0.29× |
| `openai/gpt-6.1-terra / {"effort":"high"}` | 9.595960 | $0.161885 | 58.73% | $0.016870 | 3.56× |
| `openai/gpt-6.1-sol / {"effort":"medium"}` | 6.060606 | $0.176213 | 40.27% | $0.029075 | 1.72× |
| `openai/gpt-6.1-sol / {"effort":"high"}` | 3.535354 | $0.214421 | 34.94% | $0.060651 | 2.09× |
| `openai/gpt-6.1-sol / {"effort":"xhigh"}` | 2.525253 | $0.197772 | 23.88% | $0.078318 | 1.29× |
| `openai/gpt-6.1-terra / {"effort":"max"}` | 1.515152 | $0.459363 | 44.77% | $0.303180 | 3.87× |
| `openai/gpt-6.1-sol / {"effort":"max"}` | 0.505051 | $0.337451 | 22.72% | $0.668153 | 2.20× |
| `openai/gpt-6-astra / {"effort":"xhigh"}` | 3.535354 | $4.032719 | 221.24% | $1.140683 | 1.71× |

**Candidate floor:** The next step adds 7.5757575757575 score points for $0.12355741625242073 (115.9064558470472%); marginal cost rises 5.877716807961248x. Conditional on this benchmark, workload and verified subset; not a universal default.

**Candidate ceiling:** The next step adds 9.595959595959606 score points for $0.1618849557473938 (58.72693307495419%); marginal cost rises 3.558013024877448x. Conditional on this benchmark, workload and verified subset; not a universal default.

### Explicit-opt-in free lane

- `google/gemma-4-31b-it:free / {"enabled":true}`: 0.000 `pass_at_1_percent`, $0.000000/task, first-party `google-ai-studio`. Rate limits and quota apply; use `--allow-limited-free` explicitly.

Pending reasons: multi_model_or_fallback_configuration: 10, exact_revision_effort_provider_route_not_verified: 69, original_configuration_eligibility_not_verified: 10, missing_comparable_score_or_evaluation_task_cost: 154, nonstandard_pricing_tier: 1, deprecated_or_estimated: 10.

## business-automation

**Business workflow automation** — [AutomationBench-AA](https://artificialanalysis.ai/evaluations/automationbench-aa), version `AA-II-4.3.2`; score unit `guardrail_adjusted_objective_completion_percent`; status `ready`.

Harness `aa-automationbench-ii-4.3.2`: AA simulated SaaS REST workflow environment; 657 tasks; guardrail-violating tasks score zero.

The headline score measures objective completion, not the percentage of fully completed workflows or a request's success probability.

AA evaluation-specific costPerTask from observed contestant token use and published prices; excludes unreported tools, judges, infrastructure and supervision. Not Intelligence Index weighted cost or an OpenRouter invoice estimate.

Verified candidates: 28; paid frontier: 8. Incomplete routing matches are retained as pending in workloads.json.

### Minimum cost for a minimum benchmark score

| Minimum-score interval | request.model | request.reasoning | Score | USD / this benchmark task |
|---|---|---|---:|---:|
| (−∞, 12.049187272690505] | `openai/gpt-6-luna` | `{"effort":"low"}` | 12.049 | $0.005878 |
| (12.049187272690505, 40.46136879135791] | `openai/gpt-6-luna` | `{"effort":"medium"}` | 40.461 | $0.016571 |
| (40.46136879135791, 64.05168250285656] | `xiaomi/mimo-v2.6-flash` | `{"enabled":true}` | 64.052 | $0.016656 |
| (64.05168250285656, 64.49523732184466] | `openai/gpt-6.1-sol` | `{"effort":"high"}` | 64.495 | $0.225781 |
| (64.49523732184466, 66.57372141364344] | `openai/gpt-6.1-sol` | `{"effort":"xhigh"}` | 66.574 | $0.250558 |
| (66.57372141364344, 66.6122174975011] | `openai/gpt-6-astra` | `{"effort":"high"}` | 66.612 | $1.295185 |
| (66.6122174975011, 67.17778020215393] | `openai/gpt-6-astra` | `{"effort":"xhigh"}` | 67.178 | $1.406389 |
| (67.17778020215393, 68.49174806688876] | `openai/gpt-6-astra` | `{"effort":"max"}` | 68.492 | $1.595592 |

The first lower bound is unbounded for lookup only; it does not give score zero a practical meaning. No verified configuration satisfies a score above the last row.

### Maximum score within a benchmark-task budget

| Budget interval, USD | request.model | request.reasoning | Score |
|---|---|---|---:|
| [0.005878499065985337, 0.01657116888405385) | `openai/gpt-6-luna` | `{"effort":"low"}` | 12.049 |
| [0.01657116888405385, 0.016656378652840892) | `openai/gpt-6-luna` | `{"effort":"medium"}` | 40.461 |
| [0.016656378652840892, 0.22578054709230252) | `xiaomi/mimo-v2.6-flash` | `{"enabled":true}` | 64.052 |
| [0.22578054709230252, 0.2505578926118788) | `openai/gpt-6.1-sol` | `{"effort":"high"}` | 64.495 |
| [0.2505578926118788, 1.2951847697570744) | `openai/gpt-6.1-sol` | `{"effort":"xhigh"}` | 66.574 |
| [1.2951847697570744, 1.406388714811355) | `openai/gpt-6-astra` | `{"effort":"high"}` | 66.612 |
| [1.406388714811355, 1.5955923111377626) | `openai/gpt-6-astra` | `{"effort":"xhigh"}` | 67.178 |
| [1.5955923111377626, ∞) | `openai/gpt-6-astra` | `{"effort":"max"}` | 68.492 |

### Marginal upgrades

| Upgrade to | Score gain | Added USD/task | Cost increase | USD / added score point | Marginal rate multiple |
|---|---:|---:|---:|---:|---:|
| `openai/gpt-6-luna / {"effort":"medium"}` | 28.412182 | $0.010693 | 181.89% | $0.000376 | — |
| `xiaomi/mimo-v2.6-flash / {"enabled":true}` | 23.590314 | $0.000085 | 0.51% | $0.000004 | 0.01× |
| `openai/gpt-6.1-sol / {"effort":"high"}` | 0.443555 | $0.209124 | 1255.52% | $0.471473 | 130527.27× |
| `openai/gpt-6.1-sol / {"effort":"xhigh"}` | 2.078484 | $0.024777 | 10.97% | $0.011921 | 0.03× |
| `openai/gpt-6-astra / {"effort":"high"}` | 0.038496 | $1.044627 | 416.92% | $27.135926 | 2276.34× |
| `openai/gpt-6-astra / {"effort":"xhigh"}` | 0.565563 | $0.111204 | 8.59% | $0.196625 | 0.01× |
| `openai/gpt-6-astra / {"effort":"max"}` | 1.313968 | $0.189204 | 13.45% | $0.143994 | 0.73× |

**Candidate floor:** The next step adds 0.44355481898809046 score points for $0.20912416843946163 (1255.520019075657%); marginal cost rises 130527.26992091053x. Conditional on this benchmark, workload and verified subset; not a universal default.

**Candidate ceiling:** The next step adds 0.03849608385766601 score points for $1.0446268771451956 (416.92036369548816%); marginal cost rises 2276.3370739038987x. Conditional on this benchmark, workload and verified subset; not a universal default.

### Explicit-opt-in free lane

- `google/gemma-4-31b-it:free / {"enabled":true}`: 4.933 `guardrail_adjusted_objective_completion_percent`, $0.000000/task, first-party `google-ai-studio`. Rate limits and quota apply; use `--allow-limited-free` explicitly.

Pending reasons: multi_model_or_fallback_configuration: 10, exact_revision_effort_provider_route_not_verified: 69, original_configuration_eligibility_not_verified: 10, missing_comparable_score_or_evaluation_task_cost: 154, nonstandard_pricing_tier: 1, deprecated_or_estimated: 10.

## professional-work

**Documents, spreadsheets and professional work** — [GDPval-AA](https://artificialanalysis.ai/evaluations/gdpval-aa), version `2.1`; score unit `elo`; status `ready`.

Harness `aa-stirrup-gdpval-2.1`: AA Stirrup with code execution, browsing and file outputs; 220 tasks; Crowd-BT Elo anchored to DeepSeek V4.1 Flash max at 1600.

Elo is a relative quality rating, not a percentage or an absolute success target. Benchmark contestant-token cost excludes infrastructure, supervision and external tool charges unless included by the source.

AA evaluation-specific costPerTask from observed contestant token use and published prices; excludes unreported tools, judges, infrastructure and supervision. Not Intelligence Index weighted cost or an OpenRouter invoice estimate.

Verified candidates: 28; paid frontier: 9. Incomplete routing matches are retained as pending in workloads.json.

### Minimum cost for a minimum benchmark score

| Minimum-score interval | request.model | request.reasoning | Score | USD / this benchmark task |
|---|---|---|---:|---:|
| (−∞, 1040.9] | `openai/gpt-6-luna` | `{"effort":"low"}` | 1040.900 | $0.003793 |
| (1040.9, 1052.09] | `openai/gpt-6-luna` | `{"effort":"none"}` | 1052.090 | $0.007881 |
| (1052.09, 1270.95] | `openai/gpt-6-luna` | `{"effort":"medium"}` | 1270.950 | $0.016936 |
| (1270.95, 1352.33] | `openai/gpt-6-luna` | `{"effort":"high"}` | 1352.330 | $0.031902 |
| (1352.33, 1373.25] | `openai/gpt-6-luna` | `{"effort":"xhigh"}` | 1373.250 | $0.045715 |
| (1373.25, 1615.21] | `xiaomi/mimo-v2.6-flash` | `{"enabled":true}` | 1615.210 | $0.073176 |
| (1615.21, 1691.26] | `xiaomi/mimo-v2.6-pro` | `{"enabled":true}` | 1691.260 | $0.161217 |
| (1691.26, 1716.55] | `x-ai/grok-4.7` | `{"effort":"high"}` | 1716.550 | $4.517006 |
| (1716.55, 1721.59] | `x-ai/grok-4.7` | `{"effort":"xhigh"}` | 1721.590 | $5.572227 |

The first lower bound is unbounded for lookup only; it does not give score zero a practical meaning. No verified configuration satisfies a score above the last row.

### Maximum score within a benchmark-task budget

| Budget interval, USD | request.model | request.reasoning | Score |
|---|---|---|---:|
| [0.0037933271240714194, 0.007880583970193037) | `openai/gpt-6-luna` | `{"effort":"low"}` | 1040.900 |
| [0.007880583970193037, 0.01693611899300757) | `openai/gpt-6-luna` | `{"effort":"none"}` | 1052.090 |
| [0.01693611899300757, 0.03190170403500649) | `openai/gpt-6-luna` | `{"effort":"medium"}` | 1270.950 |
| [0.03190170403500649, 0.04571538846185774) | `openai/gpt-6-luna` | `{"effort":"high"}` | 1352.330 |
| [0.04571538846185774, 0.07317641347585718) | `openai/gpt-6-luna` | `{"effort":"xhigh"}` | 1373.250 |
| [0.07317641347585718, 0.16121702931689816) | `xiaomi/mimo-v2.6-flash` | `{"enabled":true}` | 1615.210 |
| [0.16121702931689816, 4.517006141396162) | `xiaomi/mimo-v2.6-pro` | `{"enabled":true}` | 1691.260 |
| [4.517006141396162, 5.572226716663576) | `x-ai/grok-4.7` | `{"effort":"high"}` | 1716.550 |
| [5.572226716663576, ∞) | `x-ai/grok-4.7` | `{"effort":"xhigh"}` | 1721.590 |

### Marginal upgrades

| Upgrade to | Score gain | Added USD/task | Cost increase | USD / added score point | Marginal rate multiple |
|---|---:|---:|---:|---:|---:|
| `openai/gpt-6-luna / {"effort":"none"}` | 11.190000 | $0.004087 | 107.75% | $0.000365 | — |
| `openai/gpt-6-luna / {"effort":"medium"}` | 218.860000 | $0.009056 | 114.91% | $0.000041 | 0.11× |
| `openai/gpt-6-luna / {"effort":"high"}` | 81.380000 | $0.014966 | 88.36% | $0.000184 | 4.44× |
| `openai/gpt-6-luna / {"effort":"xhigh"}` | 20.920000 | $0.013814 | 43.30% | $0.000660 | 3.59× |
| `xiaomi/mimo-v2.6-flash / {"enabled":true}` | 241.960000 | $0.027461 | 60.07% | $0.000113 | 0.17× |
| `xiaomi/mimo-v2.6-pro / {"enabled":true}` | 76.050000 | $0.088041 | 120.31% | $0.001158 | 10.20× |
| `x-ai/grok-4.7 / {"effort":"high"}` | 25.290000 | $4.355789 | 2701.82% | $0.172234 | 148.78× |
| `x-ai/grok-4.7 / {"effort":"xhigh"}` | 5.040000 | $1.055221 | 23.36% | $0.209369 | 1.22× |

**Candidate floor:** The next step adds 81.37999999999988 score points for $0.014965585041998918 (88.36490253863813%); marginal cost rises 4.4445550934221485x. Conditional on this benchmark, workload and verified subset; not a universal default.

**Candidate ceiling:** The next step adds 76.04999999999995 score points for $0.08804061584104098 (120.31283259063781%); marginal cost rises 10.200246931902083x. Conditional on this benchmark, workload and verified subset; not a universal default.

### Explicit-opt-in free lane

- `google/gemma-4-31b-it:free / {"enabled":true}`: 618.720 `elo`, $0.000000/task, first-party `google-ai-studio`. Rate limits and quota apply; use `--allow-limited-free` explicitly.

Pending reasons: multi_model_or_fallback_configuration: 10, exact_revision_effort_provider_route_not_verified: 69, original_configuration_eligibility_not_verified: 10, missing_comparable_score_or_evaluation_task_cost: 154, nonstandard_pricing_tier: 1, deprecated_or_estimated: 10.

## long-context

**Long-document reasoning** — [AA-LCR](https://artificialanalysis.ai/evaluations/artificial-analysis-long-context-reasoning), version `1.1`; score unit `pass_at_1_percent`; status `ready`.

Harness `aa-lcr-1.1`: AA-LCR v1.1; 100 text questions, three repeats; approximately 100K-token supplied contexts; equality-checker grading.

Applies to supplied long text, not live retrieval, arbitrary context lengths or all PDF input formats.

AA evaluation-specific costPerTask from observed contestant token use and published prices; excludes unreported tools, judges, infrastructure and supervision. Not Intelligence Index weighted cost or an OpenRouter invoice estimate.

Verified candidates: 28; paid frontier: 7. Incomplete routing matches are retained as pending in workloads.json.

### Minimum cost for a minimum benchmark score

| Minimum-score interval | request.model | request.reasoning | Score | USD / this benchmark task |
|---|---|---|---:|---:|
| (−∞, 39.6666666666667] | `openai/gpt-6-luna` | `{"effort":"none"}` | 39.667 | $0.009465 |
| (39.6666666666667, 74.0] | `openai/gpt-6-luna` | `{"effort":"low"}` | 74.000 | $0.009561 |
| (74.0, 78.3333333333333] | `openai/gpt-6-luna` | `{"effort":"medium"}` | 78.333 | $0.009635 |
| (78.3333333333333, 79.3333333333333] | `openai/gpt-6-luna` | `{"effort":"high"}` | 79.333 | $0.009704 |
| (79.3333333333333, 80.0] | `openai/gpt-6-luna` | `{"effort":"xhigh"}` | 80.000 | $0.009817 |
| (80.0, 83.3333333333333] | `openai/gpt-6-luna` | `{"effort":"max"}` | 83.333 | $0.010188 |
| (83.3333333333333, 86.3333333333333] | `xiaomi/mimo-v2.6-pro` | `{"enabled":true}` | 86.333 | $0.047379 |

The first lower bound is unbounded for lookup only; it does not give score zero a practical meaning. No verified configuration satisfies a score above the last row.

### Maximum score within a benchmark-task budget

| Budget interval, USD | request.model | request.reasoning | Score |
|---|---|---|---:|
| [0.009465072000000001, 0.009561002000000002) | `openai/gpt-6-luna` | `{"effort":"none"}` | 39.667 |
| [0.009561002000000002, 0.009635487000000002) | `openai/gpt-6-luna` | `{"effort":"low"}` | 74.000 |
| [0.009635487000000002, 0.009703947000000003) | `openai/gpt-6-luna` | `{"effort":"medium"}` | 78.333 |
| [0.009703947000000003, 0.009817157000000002) | `openai/gpt-6-luna` | `{"effort":"high"}` | 79.333 |
| [0.009817157000000002, 0.010187532000000001) | `openai/gpt-6-luna` | `{"effort":"xhigh"}` | 80.000 |
| [0.010187532000000001, 0.047379438749999996) | `openai/gpt-6-luna` | `{"effort":"max"}` | 83.333 |
| [0.047379438749999996, ∞) | `xiaomi/mimo-v2.6-pro` | `{"enabled":true}` | 86.333 |

### Marginal upgrades

| Upgrade to | Score gain | Added USD/task | Cost increase | USD / added score point | Marginal rate multiple |
|---|---:|---:|---:|---:|---:|
| `openai/gpt-6-luna / {"effort":"low"}` | 34.333333 | $0.000096 | 1.01% | $0.000003 | — |
| `openai/gpt-6-luna / {"effort":"medium"}` | 4.333333 | $0.000074 | 0.78% | $0.000017 | 6.15× |
| `openai/gpt-6-luna / {"effort":"high"}` | 1.000000 | $0.000068 | 0.71% | $0.000068 | 3.98× |
| `openai/gpt-6-luna / {"effort":"xhigh"}` | 0.666667 | $0.000113 | 1.17% | $0.000170 | 2.48× |
| `openai/gpt-6-luna / {"effort":"max"}` | 3.333333 | $0.000370 | 3.77% | $0.000111 | 0.65× |
| `xiaomi/mimo-v2.6-pro / {"enabled":true}` | 3.000000 | $0.037192 | 365.07% | $0.012397 | 111.57× |

**Candidate floor:** The next step adds 3.0 score points for $0.037191906749999996 (365.07278455665215%); marginal cost rises 111.57432557092949x. Conditional on this benchmark, workload and verified subset; not a universal default.

**Candidate ceiling:** The next step adds 3.0 score points for $0.037191906749999996 (365.07278455665215%); marginal cost rises 111.57432557092949x. Conditional on this benchmark, workload and verified subset; not a universal default.

### Explicit-opt-in free lane

- `google/gemma-4-31b-it:free / {"enabled":true}`: 69.667 `pass_at_1_percent`, $0.000000/task, first-party `google-ai-studio`. Rate limits and quota apply; use `--allow-limited-free` explicitly.

Pending reasons: multi_model_or_fallback_configuration: 10, exact_revision_effort_provider_route_not_verified: 69, original_configuration_eligibility_not_verified: 10, missing_comparable_score_or_evaluation_task_cost: 154, nonstandard_pricing_tier: 1, deprecated_or_estimated: 10.

## document-reasoning

**Reasoning over professional PDFs** — [GDP.pdf (AA implementation)](https://artificialanalysis.ai/evaluations/gdp-pdf), version `AA-II-4.3.2`; score unit `all_criteria_pass_percent`; status `ready`.

Harness `aa-gdp-pdf-ii-4.3.2`: AA LiteParse/OCR text, plus page images for image-capable models; 100 tasks, five repeats; all-criteria-pass grading.

AA and Surge use different input preparation and judges. Cost excludes document preparation, OCR and judge calls. Page-image capability must be checked for an image-dependent application.

AA evaluation-specific costPerTask from observed contestant token use and published prices; excludes unreported tools, judges, infrastructure and supervision. Not Intelligence Index weighted cost or an OpenRouter invoice estimate.

Verified candidates: 28; paid frontier: 13. Incomplete routing matches are retained as pending in workloads.json.

### Minimum cost for a minimum benchmark score

| Minimum-score interval | request.model | request.reasoning | Score | USD / this benchmark task |
|---|---|---|---:|---:|
| (−∞, 5.800000000000001] | `openai/gpt-6-luna` | `{"effort":"none"}` | 5.800 | $0.016515 |
| (5.800000000000001, 9.0] | `openai/gpt-6-luna` | `{"effort":"low"}` | 9.000 | $0.016602 |
| (9.0, 13.8] | `openai/gpt-6-luna` | `{"effort":"medium"}` | 13.800 | $0.017432 |
| (13.8, 18.2] | `openai/gpt-6-luna` | `{"effort":"high"}` | 18.200 | $0.018825 |
| (18.2, 18.6] | `openai/gpt-6-luna` | `{"effort":"xhigh"}` | 18.600 | $0.020664 |
| (18.6, 19.2] | `xiaomi/mimo-v2.6-pro` | `{"enabled":true}` | 19.200 | $0.024022 |
| (19.2, 22.8] | `openai/gpt-6-luna` | `{"effort":"max"}` | 22.800 | $0.028547 |
| (22.8, 25.6] | `openai/gpt-6.1-terra` | `{"effort":"low"}` | 25.600 | $0.164403 |
| (25.6, 28.4] | `openai/gpt-6.1-terra` | `{"effort":"medium"}` | 28.400 | $0.166710 |
| (28.4, 28.599999999999998] | `openai/gpt-6.1-terra` | `{"effort":"max"}` | 28.600 | $0.235180 |
| (28.599999999999998, 30.0] | `openai/gpt-6.1-sol` | `{"effort":"medium"}` | 30.000 | $0.337478 |
| (30.0, 32.0] | `openai/gpt-6.1-sol` | `{"effort":"high"}` | 32.000 | $0.349401 |
| (32.0, 32.2] | `openai/gpt-6-astra` | `{"effort":"xhigh"}` | 32.200 | $1.912723 |

The first lower bound is unbounded for lookup only; it does not give score zero a practical meaning. No verified configuration satisfies a score above the last row.

### Maximum score within a benchmark-task budget

| Budget interval, USD | request.model | request.reasoning | Score |
|---|---|---|---:|
| [0.016514747, 0.016602051000000003) | `openai/gpt-6-luna` | `{"effort":"none"}` | 5.800 |
| [0.016602051000000003, 0.017431547000000002) | `openai/gpt-6-luna` | `{"effort":"low"}` | 9.000 |
| [0.017431547000000002, 0.018825166) | `openai/gpt-6-luna` | `{"effort":"medium"}` | 13.800 |
| [0.018825166, 0.020663617) | `openai/gpt-6-luna` | `{"effort":"high"}` | 18.200 |
| [0.020663617, 0.02402207025) | `openai/gpt-6-luna` | `{"effort":"xhigh"}` | 18.600 |
| [0.02402207025, 0.028547064) | `xiaomi/mimo-v2.6-pro` | `{"enabled":true}` | 19.200 |
| [0.028547064, 0.16440301999999998) | `openai/gpt-6-luna` | `{"effort":"max"}` | 22.800 |
| [0.16440301999999998, 0.16670952) | `openai/gpt-6.1-terra` | `{"effort":"low"}` | 25.600 |
| [0.16670952, 0.23517992) | `openai/gpt-6.1-terra` | `{"effort":"medium"}` | 28.400 |
| [0.23517992, 0.33747823999999993) | `openai/gpt-6.1-terra` | `{"effort":"max"}` | 28.600 |
| [0.33747823999999993, 0.34940143999999995) | `openai/gpt-6.1-sol` | `{"effort":"medium"}` | 30.000 |
| [0.34940143999999995, 1.9127230999999998) | `openai/gpt-6.1-sol` | `{"effort":"high"}` | 32.000 |
| [1.9127230999999998, ∞) | `openai/gpt-6-astra` | `{"effort":"xhigh"}` | 32.200 |

### Marginal upgrades

| Upgrade to | Score gain | Added USD/task | Cost increase | USD / added score point | Marginal rate multiple |
|---|---:|---:|---:|---:|---:|
| `openai/gpt-6-luna / {"effort":"low"}` | 3.200000 | $0.000087 | 0.53% | $0.000027 | — |
| `openai/gpt-6-luna / {"effort":"medium"}` | 4.800000 | $0.000829 | 5.00% | $0.000173 | 6.33× |
| `openai/gpt-6-luna / {"effort":"high"}` | 4.400000 | $0.001394 | 7.99% | $0.000317 | 1.83× |
| `openai/gpt-6-luna / {"effort":"xhigh"}` | 0.400000 | $0.001838 | 9.77% | $0.004596 | 14.51× |
| `xiaomi/mimo-v2.6-pro / {"enabled":true}` | 0.600000 | $0.003358 | 16.25% | $0.005597 | 1.22× |
| `openai/gpt-6-luna / {"effort":"max"}` | 3.600000 | $0.004525 | 18.84% | $0.001257 | 0.22× |
| `openai/gpt-6.1-terra / {"effort":"low"}` | 2.800000 | $0.135856 | 475.90% | $0.048520 | 38.60× |
| `openai/gpt-6.1-terra / {"effort":"medium"}` | 2.800000 | $0.002307 | 1.40% | $0.000824 | 0.02× |
| `openai/gpt-6.1-terra / {"effort":"max"}` | 0.200000 | $0.068470 | 41.07% | $0.342352 | 415.60× |
| `openai/gpt-6.1-sol / {"effort":"medium"}` | 1.400000 | $0.102298 | 43.50% | $0.073070 | 0.21× |
| `openai/gpt-6.1-sol / {"effort":"high"}` | 2.000000 | $0.011923 | 3.53% | $0.005962 | 0.08× |
| `openai/gpt-6-astra / {"effort":"xhigh"}` | 0.200000 | $1.563322 | 447.43% | $7.816608 | 1311.16× |

**Candidate floor:** The next step adds 2.8000000000000007 score points for $0.13585595599999997 (475.9016759131516%); marginal cost rises 38.60158777646298x. Conditional on this benchmark, workload and verified subset; not a universal default.

**Candidate ceiling:** The next step adds 0.20000000000000284 score points for $1.5633216599999997 (447.42851088421384%); marginal cost rises 1311.159470611895x. Conditional on this benchmark, workload and verified subset; not a universal default.

### Explicit-opt-in free lane

- `google/gemma-4-31b-it:free / {"enabled":true}`: 6.000 `all_criteria_pass_percent`, $0.000000/task, first-party `google-ai-studio`. Rate limits and quota apply; use `--allow-limited-free` explicitly.

Pending reasons: multi_model_or_fallback_configuration: 10, exact_revision_effort_provider_route_not_verified: 69, original_configuration_eligibility_not_verified: 10, missing_comparable_score_or_evaluation_task_cost: 154, nonstandard_pricing_tier: 1, deprecated_or_estimated: 10.

## academic-reasoning

**Advanced academic reasoning** — [Humanity's Last Exam (AA text subset)](https://artificialanalysis.ai/evaluations/humanitys-last-exam), version `May-2025-text-2158/AA-II-4.3.2`; score unit `pass_at_1_percent`; status `ready`.

Harness `aa-hle-text-2158-ii-4.3.2`: AA 2,158-question text-only May 2025 subset; one repeat; no browsing or code tools; equality-checker grading.

Includes mathematics, science and humanities. It is not a direct measure of research-agent performance or a calibrated probability for a new question.

AA evaluation-specific costPerTask from observed contestant token use and published prices; excludes unreported tools, judges, infrastructure and supervision. Not Intelligence Index weighted cost or an OpenRouter invoice estimate.

Verified candidates: 28; paid frontier: 14. Incomplete routing matches are retained as pending in workloads.json.

### Minimum cost for a minimum benchmark score

| Minimum-score interval | request.model | request.reasoning | Score | USD / this benchmark task |
|---|---|---|---:|---:|
| (−∞, 8.57275254865616] | `openai/gpt-6-luna` | `{"effort":"none"}` | 8.573 | $0.000150 |
| (8.57275254865616, 20.2502316960148] | `openai/gpt-6-luna` | `{"effort":"low"}` | 20.250 | $0.000522 |
| (20.2502316960148, 21.1306765523633] | `openai/gpt-6.1-terra` | `{"effort":"none"}` | 21.131 | $0.001002 |
| (21.1306765523633, 28.2669138090825] | `openai/gpt-6-luna` | `{"effort":"medium"}` | 28.267 | $0.001615 |
| (28.2669138090825, 35.820203892493005] | `openai/gpt-6.1-terra` | `{"effort":"low"}` | 35.820 | $0.002952 |
| (35.820203892493005, 40.2224281742354] | `openai/gpt-6.1-terra` | `{"effort":"medium"}` | 40.222 | $0.007151 |
| (40.2224281742354, 47.3586654309546] | `openai/gpt-6.1-sol` | `{"effort":"low"}` | 47.359 | $0.007308 |
| (47.3586654309546, 49.8609823911029] | `openai/gpt-6.1-sol` | `{"effort":"medium"}` | 49.861 | $0.012619 |
| (49.8609823911029, 51.390176088971295] | `openai/gpt-6.1-sol` | `{"effort":"high"}` | 51.390 | $0.026634 |
| (51.390176088971295, 52.6413345690454] | `openai/gpt-6.1-sol` | `{"effort":"xhigh"}` | 52.641 | $0.042817 |
| (52.6413345690454, 52.919369786839695] | `openai/gpt-6.1-sol` | `{"effort":"max"}` | 52.919 | $0.077574 |
| (52.919369786839695, 53.058387395736794] | `openai/gpt-6-astra` | `{"effort":"high"}` | 53.058 | $0.161848 |
| (53.058387395736794, 54.587581093605195] | `openai/gpt-6-astra` | `{"effort":"xhigh"}` | 54.588 | $0.253223 |
| (54.587581093605195, 54.6802594995366] | `openai/gpt-6-astra` | `{"effort":"max"}` | 54.680 | $0.378077 |

The first lower bound is unbounded for lookup only; it does not give score zero a practical meaning. No verified configuration satisfies a score above the last row.

### Maximum score within a benchmark-task budget

| Budget interval, USD | request.model | request.reasoning | Score |
|---|---|---|---:|
| [0.00014989606116774793, 0.0005215371640407784) | `openai/gpt-6-luna` | `{"effort":"none"}` | 8.573 |
| [0.0005215371640407784, 0.0010019518072289157) | `openai/gpt-6-luna` | `{"effort":"low"}` | 20.250 |
| [0.0010019518072289157, 0.0016150941612604265) | `openai/gpt-6.1-terra` | `{"effort":"none"}` | 21.131 |
| [0.0016150941612604265, 0.0029517942539388324) | `openai/gpt-6-luna` | `{"effort":"medium"}` | 28.267 |
| [0.0029517942539388324, 0.007150781742354031) | `openai/gpt-6.1-terra` | `{"effort":"low"}` | 35.820 |
| [0.007150781742354031, 0.0073080926784059325) | `openai/gpt-6.1-terra` | `{"effort":"medium"}` | 40.222 |
| [0.0073080926784059325, 0.01261928359592215) | `openai/gpt-6.1-sol` | `{"effort":"low"}` | 47.359 |
| [0.01261928359592215, 0.02663372752548656) | `openai/gpt-6.1-sol` | `{"effort":"medium"}` | 49.861 |
| [0.02663372752548656, 0.04281734198331789) | `openai/gpt-6.1-sol` | `{"effort":"high"}` | 51.390 |
| [0.04281734198331789, 0.07757399165894348) | `openai/gpt-6.1-sol` | `{"effort":"xhigh"}` | 52.641 |
| [0.07757399165894348, 0.1618475764596849) | `openai/gpt-6.1-sol` | `{"effort":"max"}` | 52.919 |
| [0.1618475764596849, 0.25322250695088044) | `openai/gpt-6-astra` | `{"effort":"high"}` | 53.058 |
| [0.25322250695088044, 0.3780767979610751) | `openai/gpt-6-astra` | `{"effort":"xhigh"}` | 54.588 |
| [0.3780767979610751, ∞) | `openai/gpt-6-astra` | `{"effort":"max"}` | 54.680 |

### Marginal upgrades

| Upgrade to | Score gain | Added USD/task | Cost increase | USD / added score point | Marginal rate multiple |
|---|---:|---:|---:|---:|---:|
| `openai/gpt-6-luna / {"effort":"low"}` | 11.677479 | $0.000372 | 247.93% | $0.000032 | — |
| `openai/gpt-6.1-terra / {"effort":"none"}` | 0.880445 | $0.000480 | 92.12% | $0.000546 | 17.15× |
| `openai/gpt-6-luna / {"effort":"medium"}` | 7.136237 | $0.000613 | 61.19% | $0.000086 | 0.16× |
| `openai/gpt-6.1-terra / {"effort":"low"}` | 7.553290 | $0.001337 | 82.76% | $0.000177 | 2.06× |
| `openai/gpt-6.1-terra / {"effort":"medium"}` | 4.402224 | $0.004199 | 142.25% | $0.000954 | 5.39× |
| `openai/gpt-6.1-sol / {"effort":"low"}` | 7.136237 | $0.000157 | 2.20% | $0.000022 | 0.02× |
| `openai/gpt-6.1-sol / {"effort":"medium"}` | 2.502317 | $0.005311 | 72.68% | $0.002123 | 96.29× |
| `openai/gpt-6.1-sol / {"effort":"high"}` | 1.529194 | $0.014014 | 111.06% | $0.009165 | 4.32× |
| `openai/gpt-6.1-sol / {"effort":"xhigh"}` | 1.251158 | $0.016184 | 60.76% | $0.012935 | 1.41× |
| `openai/gpt-6.1-sol / {"effort":"max"}` | 0.278035 | $0.034757 | 81.17% | $0.125008 | 9.66× |
| `openai/gpt-6-astra / {"effort":"high"}` | 0.139018 | $0.084274 | 108.64% | $0.606208 | 4.85× |
| `openai/gpt-6-astra / {"effort":"xhigh"}` | 1.529194 | $0.091375 | 56.46% | $0.059754 | 0.10× |
| `openai/gpt-6-astra / {"effort":"max"}` | 0.092678 | $0.124854 | 49.31% | $1.347178 | 22.55× |

**Candidate floor:** The next step adds 0.8804448563485003 score points for $0.00048041464318813727 (92.11513125276996%); marginal cost rises 17.14507684507814x. Conditional on this benchmark, workload and verified subset; not a universal default.

**Candidate ceiling:** The next step adds 4.4022242817423916 score points for $0.004198987488415198 (142.2520381565256%); marginal cost rises 5.389824218773145x. Conditional on this benchmark, workload and verified subset; not a universal default.

### Explicit-opt-in free lane

- `google/gemma-4-31b-it:free / {"enabled":true}`: 23.633 `pass_at_1_percent`, $0.000000/task, first-party `google-ai-studio`. Rate limits and quota apply; use `--allow-limited-free` explicitly.

Pending reasons: multi_model_or_fallback_configuration: 10, exact_revision_effort_provider_route_not_verified: 69, original_configuration_eligibility_not_verified: 10, missing_comparable_score_or_evaluation_task_cost: 154, nonstandard_pricing_tier: 1, deprecated_or_estimated: 10.

## Exact API routing

Every actionable row pins one standard provider, uses `require_parameters:true` and `allow_fallbacks:false`, and carries exact canonical revision, reasoning control, source timestamps and endpoint parameters. Missing revisions, controls or freshness are rejected. Provider token prices are separate from the task-cost measurements. No automatic/latest aliases or fallback-system scores are used.

| Callable model | Canonical revision | provider.only | API surface |
|---|---|---|---|
| `openai/gpt-6-luna` | `openai/gpt-6-luna-20260922` | `openai` | `https://openrouter.ai/api/v1/responses` |
| `openai/gpt-6.1-terra` | `openai/gpt-6.1-terra-20261026` | `openai` | `https://openrouter.ai/api/v1/responses` |
| `xiaomi/mimo-v2.6-flash` | `xiaomi/mimo-v2.6-flash-20260921` | `xiaomi/fp8` | `https://openrouter.ai/api/v1/chat/completions` |
| `openai/gpt-6.1-sol` | `openai/gpt-6.1-sol-20260929` | `openai` | `https://openrouter.ai/api/v1/responses` |
| `openai/gpt-6-astra` | `openai/gpt-6-astra-20260903` | `openai` | `https://openrouter.ai/api/v1/responses` |
| `google/gemma-4-31b-it:free` | `google/gemma-4-31b-it-20260402` | `google-ai-studio` | `https://openrouter.ai/api/v1/chat/completions` |
| `xiaomi/mimo-v2.6-pro` | `xiaomi/mimo-v2.6-pro-20260921` | `xiaomi/fp8` | `https://openrouter.ai/api/v1/chat/completions` |
| `x-ai/grok-4.7` | `x-ai/grok-4.7-20260916` | `xai` | `https://openrouter.ai/api/v1/chat/completions` |

## Complete coding-agent systems

These are separate model-plus-agent evaluations from the AA Coding Agent Index. They are useful evidence when building with a coding service, conditional on exact client version, settings and account access. API task costs below are for the tested system; subscription cost per prompt remains null. They do not authorize a standalone OpenRouter request. Fallback counts and tested harness versions are retained in workloads.json.

| Tested agent/system | Coding Agent Index score | API USD / agent task | Fallback attempts |
|---|---:|---:|---:|
| Codex - GPT-6 Luna (max) ({'reasoning_effort': 'max'}) | 31.126 | $0.159156 | 0 |
| Codex - GPT-6.1 Terra (low) | 34.857 | $0.198820 | 0 |
| DeepSeek Harness - DeepSeek V4.1 Flash 1017 ({'reasoning_effort': 'max'}) | 46.305 | $0.296275 | 0 |
| Codex - DeepSeek V4.1 Flash ({'reasoning_effort': 'max'}) | 47.300 | $0.386194 | 0 |
| Codex - GPT-6.1 Terra (xhigh) | 48.224 | $0.690844 | 0 |
| Codex - GPT-6.1 Sol (max) | 54.128 | $1.504639 | 0 |
| Codex - GPT-6 Astra (max) | 54.664 | $7.036158 | 0 |
| Devin Fusion CLI - Claude Opus 5.5 Max + GPT-6 Luna High | 61.512 | $7.997688 | 0 |
| Claude Code - Opus 5.5 (max) | 61.653 | $11.422720 | 76 |

Coding Agent Index version `2.0`; [original results](https://artificialanalysis.ai/agents/coding-agents) and [methodology](https://artificialanalysis.ai/methodology/coding-agents-benchmarking). Systems with missing cost, unverified tiered costs or unavailable access are listed separately in workloads.json. A tested fallback chain stays part of that system; it is never silently represented as one model.

## Pending workload profiles

| Workload | Candidate evidence | Missing requirement |
|---|---|---|
| Repository implementation and bug fixes | FrontierCode v1.1 | Separate common-harness configuration-level score and task-cost extraction remains required. Coding-agent system results are reported separately, never borrowed as API model scores. |
| Scientific coding | SciCode | The maintained general report flags SciCode as under review. Resolve the evaluation warning before enabling a dedicated routing frontier. |
| Physics reasoning | CritPt | The maintained general report flags CritPt as under review. Resolve the evaluation warning before enabling a dedicated routing frontier. |
| Live web research and retrieval | Cross-model research evaluation | AA Search Index holds the answer model fixed to compare search providers. It cannot establish a cross-model research frontier. Matching model-plus-search evaluations and all tool charges are required. |
| Structured extraction and classification | Application-specific held-out tasks | Requires representative labeled examples, schema validation and measured attempts, retries and tool costs. No production task data or calibrated Jev predictions have been supplied. |

## Router and Jev integration

The selector accepts a workload plus a benchmark score or benchmark-task budget. It filters every verified candidate before recomputing dominance for required parameters, input modality and context length. An unknown workload or unsupported constraint is rejected. A removed live endpoint is rejected rather than replaced with another model.

```sh
node select-workload.mjs workloads.json business_automation score:60 tools
node select-workload.mjs workloads.json coding_terminal budget:1 tools
node select-workload.mjs workloads.json long_context score:80 "" --min-context=128000
node select-workload.mjs workloads.json long_context budget:0 "" --allow-limited-free
```

```js
import {buildWorkloadSelection} from './select-workload.mjs';
const selected = await buildWorkloadSelection('workloads.json', 'business_automation',
  {max_task_cost_usd: 0.05}, {required_parameters: ['tools']});
// Send selected.request with task input, tools and sufficient output budget.
```

Jev is not integrated or calibrated by this refresh. A future predictor should estimate success for the task, workload, model revision, reasoning setting and execution setup, and be calibrated on held-out accepted outcomes. No benchmark-to-probability conversion is valid by assumption. Track attempted cost, retries, tools, verification, acceptance and latency without publishing private task content. Production evaluation runs and generation charges require a separate configured evaluation service; this public-data pipeline makes no paid calls.

## Sources

- https://artificialanalysis.ai/agents/coding-agents
- https://artificialanalysis.ai/evaluations/artificial-analysis-long-context-reasoning
- https://artificialanalysis.ai/evaluations/automationbench-aa
- https://artificialanalysis.ai/evaluations/gdp-pdf
- https://artificialanalysis.ai/evaluations/gdpval-aa
- https://artificialanalysis.ai/evaluations/humanitys-last-exam
- https://artificialanalysis.ai/evaluations/terminalbench-4-0
- https://artificialanalysis.ai/methodology/coding-agents-benchmarking
- https://artificialanalysis.ai/methodology/intelligence-benchmarking
