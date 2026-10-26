---
name: route-workloads-with-jev
description: Route application or agent tasks through Jev and the daily ai-model-selection JSON charts. Use when choosing an economical OpenRouter worker, classifying a workload, preparing Jev decisions, configuring model routing, or evaluating routing outcomes. Enforce exact revisions, reasoning controls, benchmark units, freshness and provider constraints; keep Jev probabilities separate from benchmark scores.
---

# Route Workloads with Jev

Use Jev to classify a task and assess candidate suitability. Use deterministic code and the maintained charts to choose and verify the worker. Optimize within measured, verified candidates; do not claim global optimality or guaranteed success.

## Establish the task and policy

1. Capture the task, concrete acceptance criteria, relevant context and available tools.
2. Identify hard requirements: context, input modalities, tools, output schema, privacy, region, latency, output budget and permitted providers. Reject or separately enforce requirements the selector cannot represent; never silently ignore one.
3. Obtain an explicit application policy: a minimum **named workload benchmark score**, a **benchmark-task cost budget**, or a previously evaluated routing policy. Keep production spend limits separate. Do not invent a benchmark target from a task description, Jev probability or Intelligence Index score.
4. For subscriptions, use `latest.json.subscription_recommendations` conditionally on plan and surface. Keep subscription choices separate from API routes and task costs.

## Load the maintained contract

Use a trusted checkout of <https://github.com/blakeaa827/ai-model-selection>. Read its `README.md`, `select-workload.mjs` and the relevant profile in `workloads.json` as needed. Use `latest.json` with `select-model.mjs` only for an explicitly requested broad Intelligence Index comparison. Do not substitute the general chart for an unsupported workload.

Stable reports:

- <https://raw.githubusercontent.com/blakeaa827/ai-model-selection/main/workloads.json>
- <https://raw.githubusercontent.com/blakeaa827/ai-model-selection/main/latest.json>

Validate the snapshot and evidence dates with the repository's selector. Expired, pending, estimated, mismatched or unavailable configurations cannot be routed. Keep unrounded source values. Floors and ceilings describe value knees and need a workload quality target before becoming defaults.

## Classify with Jev when needed

Skip classification when the caller supplies an unambiguous supported workload. Split mixed work into independently verifiable stages.

Prepare a typed **Choice** request using the helper. It validates the report and verifies the pinned Jev revision/provider through the live **decision-output** catalog. The default OpenRouter catalog returns text-output models and is insufficient for checking Jev.

```sh
node /path/to/skill/scripts/route.mjs prepare /path/to/ai-model-selection /private/task.json /path/to/workloads.json > /private/jev-bundle.json
```

Read [references/jev-api.md](references/jev-api.md) for task input and API fields. Keep the bundle outside the public repository: it contains private task data. Submit only `bundle.request` to `bundle.api_endpoint` using authorized runtime credentials. The helper makes public metadata GETs and **never sends a paid model request**.

Choice confidence summarizes distribution concentration. Inspect the selected option's probability and margin over the runner-up. Use the application's tested classification thresholds; no universal threshold is supplied. Unsupported, mixed or unclear results need decomposition, context or review.

Resolve an actual response against the same report and explicit classification policy:

```sh
node /path/to/skill/scripts/route.mjs resolve /path/to/ai-model-selection /private/jev-bundle.json /private/jev-response.json /private/classification-policy.json /path/to/workloads.json
```

The helper rejects changed reports, unexpected Jev revisions/providers, malformed probabilities and insufficient margins, then calls the existing workload selector and checks live worker routing. The output is a **request plan**, not an executed task.

## Select the worker deterministically

Use `buildWorkloadSelection` or the CLI with the caller's explicit target and constraints. These example targets are benchmark units, not application success probabilities:

```sh
node select-workload.mjs workloads.json business_automation score:60 tools
node select-workload.mjs workloads.json coding_terminal budget:1 tools
node select-workload.mjs workloads.json long_context score:80 "" --min-context=128000
```

The selector filters **all evaluated configurations before recomputing dominance**. A general-chart loser can be useful for a specific workload or constraint. Enable the limited free lane only with explicit opt-in.

Copy the returned `api_endpoint` and complete `request` unchanged. Preserve `request.model`, exact tagged reasoning control, `provider.only`, `require_parameters=true` and `allow_fallbacks=false`. Do not send `effort:null`, invent efforts, switch endpoint families, use automatic aliases or substitute a provider/quantization. Add input/messages, tools and sufficient output capacity; preserve reasoning state across tool turns where required.

## Use candidate probabilities carefully

Read [references/routing-policy.md](references/routing-policy.md) before probability-based routing.

- Ask a separate **Noul** question for each exact candidate and clearly defined acceptance event. Supply task features, tools, revision, reasoning, harness and relevant observed outcomes.
- Label `.noul` as an **uncalibrated model estimate** until held-out outcomes validate it for the actual workload. It is not a benchmark score or demonstrated success rate. Noul has no separate `.confidence` field.
- Do not map `p=0.9` to Intelligence Index 90, 90% knowledge or a required benchmark target. Choice probability is not worker success probability. Score is an ordered-level estimate, not inherently a zero-to-one probability.
- With a validated calibration policy, choose the lowest expected total-cost candidate meeting its success target and hard requirements. Include routing, generation, tools, verification, retries and escalation. Match calibration evidence to exact configuration and workload.
- Without that evidence, use an explicit benchmark target/budget and keep candidate estimates advisory. State that probability-based production routing remains unvalidated.

Questions in one Jev call are independent. Separate classification from dependent candidate assessment. Avoid `typesafe/jev-router` when the requirement is to follow this repository's policy; it uses its own selection behavior.

## Verify, escalate and record

Verify worker output against acceptance checks: tests, schema, cited evidence, tool results or domain review as appropriate. Jev confidence alone does not satisfy an acceptance check or authorize external action.

Use bounded retries/escalation from application policy. Recheck eligibility for each new route; never silently substitute another model after failure. For unknown workloads, missing policy, stale evidence, unsupported requirements or failed live checks, return a precise blocked/needs-policy result and continue independent useful work where possible.

Return workload, report date/hash, benchmark/version/harness, configuration ID, exact request, score/cost and cost basis. Add Jev revision, classification probability/margin, calibration status, verification result and actual cost/latency when available; use null for unknowns. Keep redacted telemetry private. Never publish keys, private prompts or tool outputs.

## Install and maintain

Install this directory through each platform's supported skill mechanism. For platforms without skills, use this file as scoped company instructions and expose the selector as a tool. Keep helpers and references together. A repository file does not install itself companywide or provide credentials.

Keep changing rankings in the daily JSON, not this skill. Verify the pinned Jev control model/API on changes and fail until an intentional update passes checks. Retain MIT for original code/documentation and credit Artificial Analysis for benchmark evidence.
