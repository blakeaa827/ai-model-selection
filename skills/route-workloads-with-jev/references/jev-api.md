# Jev API and preparation contract

Sources checked October 26, 2026 UTC (October 25 in America/Chicago). Recheck live metadata before preparing/resolving. No paid-call smoke test was performed.

| Field | Verified value |
| --- | --- |
| Callable model | `typesafe/jev-1.14` |
| Canonical revision | `typesafe/jev-1.14-20261014` |
| Provider tag | `typesafe` |
| Response provider label | `TypeSafe` |
| API endpoint | `https://openrouter.ai/api/alpha/decisions` |
| Output modality | `decisions` |
| Reasoning effort | Not applicable; omit reasoning controls |
| Managed quantization | `unknown`; no third-party substitute |

Live sources:

- <https://openrouter.ai/api/v1/models?output_modalities=decisions>
- <https://openrouter.ai/api/v1/models/typesafe/jev-1.14/endpoints>

The helper records token pricing as metadata only. It does not turn token rates into AA task costs or a production invoice estimate. An unavailable or changed control revision fails. The endpoint remains under `/alpha/`; review schema changes rather than guessing compatibility.

## Private task file

The orchestrator constructs this envelope from the user request and application context. The user does not need to choose a benchmark or numerical target. Omit `target` (or use `"infer"`) for workload classification followed by task-capability inference:

```json
{
  "task": "Reconcile incoming CRM records and update the approved workflow.",
  "acceptance_criteria": ["Preserve existing IDs", "Validate updates before applying them"],
  "context": {"tools_available": ["CRM read", "CRM validated update"]},
  "constraints": {"required_parameters": ["tools"]}
}
```

Default target: `infer`. Advanced overrides: `score:<number>`, `budget:<USD per benchmark task>`, or explicitly chosen `floor`/`ceiling` value knees. Supported constraints: `allow_limited_free`, `required_parameters`, `min_context_tokens`, `input_modalities`, `harness_id`, `benchmark_version`. Separately enforce unsupported privacy, region, latency or other requirements.

`prepare` returns a bundle with task data, report hash, verified control metadata and an API request:

```json
{
  "model": "typesafe/jev-1.14",
  "state": {"task": "...", "acceptance_criteria": ["..."], "context": {}},
  "questions": {
    "workload": {
      "type": "choice",
      "instructions": "Choose a supported workload or uncertainty option.",
      "criteria": {"business_automation": "...", "unsupported": "..."}
    }
  },
  "provider": {"only": ["typesafe"], "require_parameters": true, "allow_fallbacks": false}
}
```

Actual criteria include all ready profiles, `unsupported`, `mixed` and `clarification_needed`. Send only `bundle.request`. Add authentication at runtime from the platform secret store or `OPENROUTER_API_KEY`; never serialize credentials. The helper performs no paid POST.

## Resolve

Pass the full Decisions response, including `model`, `provider` and `answers.workload`, without rewriting identity fields. The helper requires the canonical revision and TypeSafe label. Choice uses `.choice`, `.probabilities` and `.confidence`. The helper gates on selected probability and the top-to-second **difference**, not confidence. This is classification evidence, not worker success evidence. A supplied response is not cryptographically attested: output records `provided_response_not_attested`, or `simulated_fixture` when the input explicitly contains `test_fixture:true`. The verified scope is the report and live routing metadata, not the truth of a supplied classification.

Provide an explicit private classification policy:

```json
{"minimum_choice_probability": 0.8, "minimum_probability_margin": 0.2}
```

The values illustrate syntax only; evaluate them on labeled examples. No defaults are embedded. A tie, low margin, uncertain option, changed report or stale evidence blocks resolution. Reprepare after a report change. With an explicit target, `resolve` invokes the existing selector and verifies current metadata. With `infer` or no target, it returns a bound `capability_inference_required` bundle. Submit that bundle's request separately: questions in a single Jev call are independent, so capability inference must follow workload classification.

The second request uses a `minimum_capability` Choice over exact constrained measured anchors, plus `insufficient_evidence` and `no_adequate_candidate`. It includes the task, acceptance criteria, context, hard constraints, named benchmark/version/harness, limitations, exact worker settings and observed scores. It supplies no made-up difficulty-to-score mapping.

Resolve the full second response using `route.mjs resolve-requirements REPO REQUIREMENTS_BUNDLE_JSON REQUIREMENTS_RESPONSE_JSON POLICY_JSON [WORKLOADS_JSON]`. This rechecks report binding, anchors, control identity, probability/margin policy, freshness and the selected live worker route. It derives the minimum score from the chosen anchor and emits an unexecuted worker request plan.

`requirements_inference` records `inferred_minimum_score`, `anchor_configuration_id`, `status: "uncalibrated_task_estimate"`, `quality_target_verified: false` and worker success probability null. The plan sets `acceptance_verification_required: true`. This is a task-dependent model judgment, not a calibrated success prediction. The runtime must supply acceptance checks, spend limits and bounded escalation. Both Jev responses retain synthetic/provided-response provenance; neither is attested by this helper.

Noul returns `.noul` in `[0,1]`, with no separate confidence. Define one clear yes/no acceptance event per exact candidate. Score returns an expected ordinal position over supplied levels; it is not AA capability or inherently a probability.

## Primary documentation

- [OpenRouter Jev overview](https://openrouter.ai/docs/guides/community/jev)
- [Decisions API reference](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-request)
- [Tutorial and response fields](https://openrouter.ai/docs/guides/community/jev-tutorial) — historical examples still name 1.13; use the verified pin.
- [Catalog modality filters](https://openrouter.ai/docs/guides/overview/models)
- [TypeSafe confidence](https://docs.typesafe.ai/confidence)
- [Noul](https://docs.typesafe.ai/primitives/noul), [Choice](https://docs.typesafe.ai/primitives/choice), [Score](https://docs.typesafe.ai/primitives/score)
