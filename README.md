# AI model selection

Daily model guidance for Blake and his tools, with two separate tracks:

- **Applications:** all-lab OpenRouter discovery, minimum measured task cost meeting a capability target, or highest observed capability within a benchmark-task budget.
- **Building:** recommendations within Claude, OpenAI Work/Codex, Grok and Gemini subscriptions, conditional on plan/client/account access and included allowances.

## October 24, 2026 recommendation

API floor: **MiMo-V2.6-Pro / thinking enabled**, score **46.3242065310383**, **$0.13322318937213493** per measured AA task. Optional ceiling: **GPT-6.1 Sol / xhigh**, score **51.0377679093761**, **$0.39286117158850653**. Both are workload-conditional heuristics.

Refreshed 15 paid configurations and 1 opt-in free configurations. 0 numerical source revisions; 0 new and 0 absent gateway listings; 0 new AA releases since 2026-10-24. New candidates require exact effort/revision correspondence before routing.

Discovery screens 469 live OpenRouter entries and 515 AA releases across all labs. Only exact comparable benchmark/route pairs are actionable. See [latest.md](latest.md) for full threshold and budget tables, all marginal costs, source limitations and conditional subscription guidance. Kimi K3.1 Pro is pending an explicit AA effort match; Haiku's complete tiered task costs and Sonnet's prerelease reruns remain pending. Gemini 4 Argon API is now GA, with revision correspondence handled separately.

## Files and cost basis

- [latest.json](latest.json): stable machine-readable schema 1.1.0 contract, paid frontier, limited free lane, subscription guidance and source checks.
- [latest.md](latest.md): full dated report, exact score thresholds, budget examples, marginal costs and recommendations.
- [coverage.json](coverage.json): catalog inventory and AA release screening bounds with explicit pending statuses.
- [cost-curve.svg](cost-curve.svg): current paid cost-capability curve.
- [snapshots](snapshots): dated complete reports; same-day revisions remain in Git history.
- [schema.json](schema.json), [select-model.mjs](select-model.mjs) and [test-selector.mjs](test-selector.mjs): format, selector and validation checks.

The common comparison is **Artificial Analysis Intelligence Index v4.3.2** and **weighted USD per Intelligence Index task**. Broad capability is not percentage knowledge. AA cost is based on measured benchmark token usage and provider prices; it is not an OpenRouter invoice estimate, guaranteed prompt price or spending cap. Token rates are recorded separately. Underlying AA numerical precision drives dominance and selection; display values are rounded, and close score gaps may not be meaningful for your workload.

Subscription allowance consumption is a separate cost basis. A monthly plan does not establish cost per successful task. UI Extended, Expert, Heavy, Deep Think and Ultra are not assumed to map to API efforts; app tools, parallel agents, limits and model rollouts can change outcomes.

## Retrieve privately

Other tools need GitHub read access. Stable authenticated Contents endpoint:

`https://api.github.com/repos/blakeaa827/ai-model-selection/contents/latest.json?ref=main`

Using an already authenticated GitHub CLI:

```sh
gh api repos/blakeaa827/ai-model-selection/contents/latest.json?ref=main --jq '.content' | base64 --decode > latest.json
```

A checkout or authenticated raw retrieval can also supply latest.json. Never put credentials in report files. Validate against schema.json and run the selector before routing.

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
## Scheduled pipeline

The existing workflow runs `node pipeline/refresh.mjs`: public AA exact-record and full release acquisition, live OpenRouter catalog and pinned endpoint checks, report assembly, rendering, schema/selector/evidence validation, and one atomic fast-forward publication. It uses the existing daily schedule; only verified evidence advances timestamps. An AA API key is optional for separate catalog diagnostics and is not required by the public-source report path. No generation API is called.

Run `node pipeline/refresh.mjs` locally to stage and validate `run-artifacts/report/`. `--publish` additionally requires the existing GitHub integration or the workflow's scoped `GITHUB_TOKEN`; credentials are never put in reports. `pipeline/publish.mjs` creates individual blobs, then a small tree, commit and non-force ref update, and verifies the remote contents. This avoids the earlier large inline tree request. On a concurrent update it stops safely; a fresh run rebuilds from current main.

The Dot monitor remains responsible for web research and reviewing new candidates, lifecycle changes and subscription UI correspondence. A newly listed model stays pending until its exact AA configuration, revision, reasoning control and route are verified. This is deliberate eligibility enforcement; supported effort names alone cannot supply missing benchmarks. Failed acquisition or validation preserves the last published report and produces diagnostic artifacts.
