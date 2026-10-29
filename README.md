# AI Model Selection — Cost vs Capability

[![Daily refresh](https://github.com/blakeaa827/ai-model-selection/actions/workflows/model-selection.yml/badge.svg)](https://github.com/blakeaa827/ai-model-selection/actions/workflows/model-selection.yml)
[![GitHub stars](https://img.shields.io/github/stars/blakeaa827/ai-model-selection?style=flat)](https://github.com/blakeaa827/ai-model-selection/stargazers)

**Find the cheapest verified AI model for a capability target—or the most capable model within a benchmark-task budget.**

A daily cost vs capability chart and machine-readable model selector across all labs listed on OpenRouter. Actionable configurations require matching Artificial Analysis measurements, exact model revisions, reasoning controls and verified provider routes. Unmeasured, estimated or mismatched candidates stay visible as pending.

- **For applications and agents:** exact OpenRouter model IDs, reasoning settings, provider pins and freshness checks.
- **For builders:** separate subscription guidance for Claude, ChatGPT/Codex, Grok and Gemini, conditional on plan and account access.
- **For evaluation:** the complete cost-capability frontier, minimum-score and budget intervals, marginal cost cliffs, source links and dated snapshots.

**Start here:** [Current chart](latest.md) · [Raw JSON](https://raw.githubusercontent.com/blakeaa827/ai-model-selection/main/latest.json) · [Selector examples](#select-an-api-configuration) · [Report a bug or request a feature](https://github.com/blakeaa827/ai-model-selection/issues/new/choose)

![AI model capability versus measured benchmark-task cost](cost-curve.svg)

The Intelligence Index measures broad benchmark capability, not a request's probability of success. AA weighted task costs are not OpenRouter invoice estimates. Every listed model is inventoried; not every model has comparable measurements. See the [methodology and limits](latest.md) before using the recommendations.

## October 29, 2026 recommendation

API floor: **GPT-6.1 Terra / low**, score **29.2169280792131**, **$0.07133756205169729** per measured AA task. Optional ceiling: **GPT-6.1 Terra / medium**, score **38.1152076677975**, **$0.16880458238389412**. Both are workload-conditional heuristics.

Refreshed 13 paid configurations and 0 opt-in free configurations. 0 numerical source revisions; 0 new and 0 absent gateway listings; 0 new AA releases since 2026-10-29. New candidates require exact effort/revision correspondence before routing.

Discovery screens 457 live OpenRouter entries and 517 AA releases across all labs. Only exact comparable benchmark/route pairs are actionable. See [latest.md](latest.md) for full threshold and budget tables, all marginal costs, source limitations and conditional subscription guidance. Kimi K3.1 Pro is pending an explicit AA effort match; Haiku's complete tiered task costs and Sonnet's prerelease reruns remain pending. Gemini 4 Argon API is now GA, with revision correspondence handled separately.

## Files and cost basis

**License:** Original project code and original documentation are licensed under [MIT](LICENSE). Benchmark source: [Artificial Analysis](https://artificialanalysis.ai/). MIT does not assert rights over third-party material; the source-data rights review remains deferred by the maintainer. See [DATA-SOURCES.md](DATA-SOURCES.md). The [workload-specific selector](docs/WORKLOADS.md) is included in the daily refresh.

- [latest.json](latest.json): stable machine-readable schema 1.1.0 contract, paid frontier, limited free lane, subscription guidance and source checks.
- [latest.md](latest.md): full dated report, exact score thresholds, budget examples, marginal costs and recommendations.
- [coverage.json](coverage.json): catalog inventory and AA release screening bounds with explicit pending statuses.
- [cost-curve.svg](cost-curve.svg): current paid cost-capability curve.
- [snapshots](snapshots): dated complete reports; same-day revisions remain in Git history.
- [schema.json](schema.json), [select-model.mjs](select-model.mjs) and [test-selector.mjs](test-selector.mjs): format, selector and validation checks.

The common comparison is **Artificial Analysis Intelligence Index v5.0** and **weighted USD per Intelligence Index task**. Broad capability is not percentage knowledge. AA cost is based on measured benchmark token usage and provider prices; it is not an OpenRouter invoice estimate, guaranteed prompt price or spending cap. Token rates are recorded separately. Underlying AA numerical precision drives dominance and selection; display values are rounded, and close score gaps may not be meaningful for your workload.

Subscription allowance consumption is a separate cost basis. A monthly plan does not establish cost per successful task. UI Extended, Expert, Heavy, Deep Think and Ultra are not assumed to map to API efforts; app tools, parallel agents, limits and model rollouts can change outcomes.

## Retrieve publicly

The repository is public. Other tools can read the stable raw JSON URL without GitHub credentials:

https://raw.githubusercontent.com/blakeaa827/ai-model-selection/main/latest.json

```sh
curl --fail --location https://raw.githubusercontent.com/blakeaa827/ai-model-selection/main/latest.json --output latest.json
```

The Contents API is also available for clients that need GitHub metadata:

`https://api.github.com/repos/blakeaa827/ai-model-selection/contents/latest.json?ref=main`

Public read access does not grant permission to publish changes. Daily commits continue to use the connected integration or the workflow's scoped `GITHUB_TOKEN`. OpenRouter generation calls still need your own API key; the report includes no credentials. Validate against schema.json and run the selector before routing.

## Workload-specific selection

Use [workloads.md](workloads.md) for independent cost-capability frontiers for terminal coding, business automation, professional work, long-context reasoning, PDF reasoning and academic reasoning. [workloads.json](workloads.json) is the stable machine-readable contract; [workloads.schema.json](workloads.schema.json) validates it. Each profile uses its own benchmark score, evaluation task cost, harness and candidate value knees. It never borrows the general index's task cost. All configurations are reconsidered per workload, including general-chart losers. Exact routing coverage remains incomplete.

```sh
node select-workload.mjs workloads.json business_automation score:60 tools
node select-workload.mjs workloads.json coding_terminal budget:1 tools
node select-workload.mjs workloads.json long_context score:80 "" --min-context=128000
node select-workload.mjs workloads.json long_context budget:0 "" --allow-limited-free
```

The workload selector filters all verified candidates for required parameters, context and input modalities before computing dominance. It rejects unknown workloads, stale evidence, changed revisions and unsupported constraints. Budget values are benchmark-task budgets, not production prompt caps. Candidate floors and ceilings describe cost knees; a workload quality target is needed before treating one as a deployment default. The existing general selector and subscription guidance remain available.

The same daily `pipeline/refresh.mjs` acquires active public AA configuration records, rebuilds each profile, refreshes complete coding-agent system comparisons, renders curves, validates schema/evidence and selector boundaries, then publishes all artifacts and dated workload snapshots atomically. Benchmark source: [Artificial Analysis](https://artificialanalysis.ai/); original project code and documentation use [MIT](LICENSE). The maintainer has deferred the source-data rights review; see [DATA-SOURCES.md](DATA-SOURCES.md). Pending research, extraction and other profiles are explicit. A [companion Jev routing skill](skills/route-workloads-with-jev/SKILL.md) prepares classification requests and verified worker selection. Calibrated request-success routing remains unimplemented; see the [router guidance](workloads.md#router-and-jev-integration).

## Company routing skill with Jev

Install or adapt [route-workloads-with-jev](skills/route-workloads-with-jev/SKILL.md) in your AI platform's skill/instruction system. Keep its helpers and references together and point it at a trusted checkout of this repository. It infers the workload and required capability from the task and acceptance criteria using two dependent Jev decisions. The second decision assesses exact measured configurations as capability anchors; the deterministic selector then prepares the cheapest verified worker meeting the inferred target. End users do not need to supply benchmark scores. Explicit score/budget targets remain advanced overrides.

The orchestrator derives acceptance criteria and hard constraints from the request and application context. The helper verifies the decision-output catalog, binds both decisions and capability anchors to a report hash, requires an application-level probability/margin policy and rejects stale reports, changed revisions/providers, uncertain classifications, unsupported constraints and insufficient capability evidence. An inferred target is labeled `uncalibrated_task_estimate`, with `quality_target_verified: false` and worker success probability null. It is an estimated requirement, not a measured task-success threshold. Known workloads can skip Jev. No command submits a paid model request; your platform supplies authorized runtime credentials and executes the request plan. A repository skill does not automatically install itself companywide.

```sh
node skills/route-workloads-with-jev/scripts/route.mjs prepare . /private/task.json workloads.json > /private/jev-bundle.json
# Submit only bundle.request to bundle.api_endpoint through your authorized runtime.
node skills/route-workloads-with-jev/scripts/route.mjs resolve . /private/jev-bundle.json /private/jev-response.json /private/classification-policy.json workloads.json > /private/requirements-bundle.json
# With no task target (or target: infer), submit the second bundle.request separately.
node skills/route-workloads-with-jev/scripts/route.mjs resolve-requirements . /private/requirements-bundle.json /private/requirements-response.json /private/classification-policy.json workloads.json
node test-jev-routing.mjs
```

See the [input/API contract](skills/route-workloads-with-jev/references/jev-api.md) and [routing policy](skills/route-workloads-with-jev/references/routing-policy.md). Keep task bundles, responses, credentials and telemetry outside this public repository. Choice probabilities classify workloads and assess a required-capability anchor; neither is a worker success probability. The target copies the selected anchor's observed workload score without converting probabilities into Intelligence Index points or inventing an easy/medium/hard score ladder. Require output acceptance checks and bounded escalation. Optional Noul estimates need held-out calibration before success-based routing. Calibrated production success prediction remains unimplemented.

## Select an API configuration

Requires Node 20+; uses public OpenRouter catalog/endpoint metadata and makes no paid generation call.

```sh
node select-model.mjs latest.json floor tools
node select-model.mjs latest.json ceiling tools
node select-model.mjs latest.json score:46 tools
node select-model.mjs latest.json budget:0.14 tools
node select-model.mjs latest.json budget:0 tools --allow-limited-free
```

Existing numeric minimum-score queries remain supported. `floor` and `ceiling` are suggested defaults, not hard capability limits. `budget:0.14` returns the highest observed index score whose **AA task cost** is at most $0.14. It does not constrain the price of a specific production request. Without explicit limited-free opt-in, budgets below the cheapest paid configuration fail.

Programmatic use:

```js
import {buildSelection} from './select-model.mjs';
const byScore = await buildSelection('latest.json', 46, ['tools']);
const byBudget = await buildSelection('latest.json', {max_task_cost_usd: 0.14}, ['tools']);
const freeOptIn = await buildSelection('latest.json', {max_task_cost_usd: 0}, ['tools'], {allow_limited_free: true});
// POST the returned request plus input/messages and an appropriate output budget
// to the returned api_endpoint. Add authentication only at request time.
```

Every retained row contains exact request.model and the supported reasoning control. Named efforts use request.reasoning.effort. MiMo and Gemma use reasoning.enabled=true; effort=null is descriptive metadata only, never sent in the request. Routing pins the exact standard provider tag, requires parameters, disables fallback, and verifies the canonical revision. Third-party quantization or a faster variant is not silently substituted. Preserve reasoning_details on tool turns where required, and provide enough output capacity for reasoning plus the answer.

The selector rechecks the selected live catalog entry and exact endpoint, including required parameters and recorded quantization. OpenAI tool calling uses the verified Responses endpoint. A removed route, mismatched revision, unsupported control/parameter or stale snapshot/row causes rejection. Explicitly ineligible, provisional-cost and estimated-score records are rejected even if mistakenly placed in the frontier. Reports expire for routing after 48 hours; source checks are not advanced without successful verification. No paid-generation smoke test is claimed.

Queries optimize the comparable broad index; they do not guarantee coding, vision, latency, privacy, context length or reliability for your particular task. Supply required parameters to detect incompatibility; failure does not automatically select a dominated model or a different revision. Add workload evaluations before choosing deployment defaults.

## Read subscription recommendations

Use `latest.json.subscription_recommendations.services` to show routine_default, escalation and quota_saving options, exact documented controls, plan eligibility and uncertainty. These records are guidance for the service's building UI/CLI, not OpenRouter requests. `personal_tier` remains null until Blake provides the exact tier. Do not turn subscription entries into production API routes or attach API task costs to them.

## Refresh and validation

The daily report now discovers all labs and keeps the API and subscription tracks distinct. It refreshes a common index version, all potentially competitive measured configurations, source documentation, canonical model IDs and endpoint controls. Release score maxima/cost minima are screening bounds, never invented score/cost pairs. Free and promotional token prices do not overwrite measured task costs.

Publish latest.json, latest.md, the dated snapshot and any changed contract/coverage/curve files together in one non-force fast-forward commit. Preserve unrelated files and history. Re-read a concurrent head before rebasing. Verify remote file contents after publishing. October 7 revision 2 expands scope and corrects rounded comparisons; its earlier same-day snapshot is preserved at commit a7a9b70b3bcdc1e3965165d20ca20b461e814f6f.

Run local selector checks:

```sh
node test-selector.mjs
```
## Feedback and contributions

Found a broken route, stale result, selector bug or missing feature? Use the [issue forms](https://github.com/blakeaa827/ai-model-selection/issues/new/choose). General questions are welcome through a blank issue. Include the report date or commit and reproducible evidence so changes can be verified.

See [CONTRIBUTING.md](CONTRIBUTING.md) for evidence requirements and local checks. Please exclude API keys, authorization headers and private prompts. Stars help you save this repository and signal interest; they are not a count of active users.

## Scheduled pipeline

The existing workflow runs `node pipeline/refresh.mjs`: public AA exact-record and full release acquisition, live OpenRouter catalog and pinned endpoint checks, report assembly, rendering, schema/selector/evidence validation, and one atomic fast-forward publication. It uses the existing daily schedule; only verified evidence advances timestamps. An AA API key is optional for separate catalog diagnostics and is not required by the public-source report path. No generation API is called.

Run `node pipeline/refresh.mjs` locally to stage and validate `run-artifacts/report/`. `--publish` additionally requires the existing GitHub integration or the workflow's scoped `GITHUB_TOKEN`; credentials are never put in reports. `pipeline/publish.mjs` creates individual blobs, then a small tree, commit and non-force ref update, and verifies the remote contents. This avoids the earlier large inline tree request. On a concurrent update it stops safely; a fresh run rebuilds from current main.

The Dot monitor remains responsible for web research and reviewing new candidates, lifecycle changes and subscription UI correspondence. A newly listed model stays pending until its exact AA configuration, revision, reasoning control and route are verified. This is deliberate eligibility enforcement; supported effort names alone cannot supply missing benchmarks. Failed acquisition or validation preserves the last published report and produces diagnostic artifacts.
