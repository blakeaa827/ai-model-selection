# Workload-specific daily selection

The implementation adds independently computed cost-capability frontiers for:

- Terminal coding: Terminal-Bench 4.0 with AA's mini-swe-agent setup.
- Business automation: AutomationBench-AA objective completion with guardrail handling.
- Professional work: GDPval-AA v2.1 with Stirrup and its Elo scale.
- Long context: AA-LCR v1.1.
- PDF reasoning: the AA implementation of GDP.pdf.
- Academic reasoning: the AA text-only Humanity's Last Exam subset.

Every profile uses its own observed evaluation `costPerTask`, not the Intelligence Index weighted task cost. Every verified candidate is reconsidered, including configurations dominated in the general chart. A model can therefore be on one workload frontier and off another. Exact model revisions, native reasoning controls, pinned standard provider routes, methodology, harness and source freshness remain required. Missing evidence stays pending.

## Rollout status

The feature is **enabled for daily publication** by the maintainer's October 25, 2026 instruction. Original project code and documentation use the [MIT license](../LICENSE). Benchmark measurements are credited to [Artificial Analysis](https://artificialanalysis.ai/). The source-data rights review is deferred, and source redistribution permission has not been independently verified; see [DATA-SOURCES.md](../DATA-SOURCES.md). The existing daily schedule is preserved.

Generated files are `workloads.json`, `workloads.md`, `workloads/cost-curves.svg` and `workloads/snapshots/YYYY-MM-DD.json`. The general report links to them. They are validated and published atomically with the general report, coverage inventory, README and snapshot. Each benchmark uses its own measured score and task cost.

## Selector contract

`select-workload.mjs` supports minimum-score and benchmark-task-budget queries. Scores are benchmark-specific: percentage metrics and Elo remain distinct, with no conversion into general intelligence or probability of a new request succeeding.

After retrieving the current dataset:

```sh
node select-workload.mjs workloads.json business_automation score:60 tools
node select-workload.mjs workloads.json coding_terminal budget:1 tools
node select-workload.mjs workloads.json long_context score:80 "" --min-context=128000
node select-workload.mjs workloads.json long_context budget:0 "" --allow-limited-free
```

```js
import {buildWorkloadSelection} from '../select-workload.mjs';
const selected = await buildWorkloadSelection('workloads.json', 'business_automation',
  {max_task_cost_usd: 0.05}, {required_parameters: ['tools']});
// Use selected.api_endpoint and selected.request with input, tools and output budget.
```

Programmatic constraints include `required_parameters`, `min_context_tokens`, `input_modalities`, `harness_id` and `benchmark_version`. Candidates are filtered before Pareto dominance is recomputed. A model dominated overall can still be the cheapest compatible choice after these constraints. Unknown constraints, pending workloads, stale evidence, changed revisions and unavailable endpoints are rejected without substitution.

Free routes remain an explicit-opt-in lane. Benchmark-task budgets do not cap the price of individual production requests. Candidate floors and ceilings identify cost knees only; an acceptable workload quality target is required before adopting a deployment default.

## Agent systems and subscriptions

AA Coding Agent Index results are kept as separate model-plus-agent system comparisons, including tested client versions and fallback counts. Their API costs are not subscription prompt costs, and those systems are never represented as a standalone OpenRouter model call. Individual implementation, research/search and extraction profiles stay pending when matching cost or execution evidence is missing.

## Jev

No Jev calls, success-probability calibration or paid evaluation runs are implemented. The future calibration layer should condition on task features and each exact candidate configuration, then compare predicted probabilities with held-out accepted results. Track cost including retries, tools and verification, along with acceptance and latency, without making private tasks public. Do not map a Jev probability directly onto a benchmark score.

## Validation and review

```sh
node test-workload-selector.mjs
```

Synthetic tests cover score/budget boundaries, free opt-in, constraint-dependent dominance, stale/version/harness/parameter rejection and strict request construction. For an already acquired, authorized local evidence bundle, offline review can run:

```sh
node pipeline/refresh.mjs --reuse-acquisition --include-workloads
```

The review flag cannot publish and cannot initiate workload acquisition. Normal daily execution runs `node pipeline/refresh.mjs --publish`; rollout state is recorded in `pipeline/workload-rollout.json`. Source acquisition, schema, exact-configuration, endpoint and selector validation must pass before publication. A failed check preserves the last published report. MIT licensing and attribution do not assert third-party redistribution permission.
