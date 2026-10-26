# Routing policy and calibration

| Quantity | Meaning | Use |
| --- | --- | --- |
| Jev Choice probability | Model probability that a supplied label applies | Workload classification under tested policy |
| Jev Noul probability | Estimated probability of the specific yes/no event | Advisory candidate suitability until calibrated |
| AA benchmark score | Observed exact-configuration performance under a named harness | Measured score/cost tradeoff within that profile |

No general transformation connects these values. Intelligence Index, Elo and benchmark pass percentages are distinct scales. A benchmark score of 60 does not establish 60% success on a new request; a 0.9 estimate does not require Intelligence Index 90. Tools, context, specialization and harness matter.

## Infer requirements without an end-user score

The orchestrator derives acceptance checks and hard constraints from the request and available application context. Users supply the work they want done; they do not have to select a benchmark or capability threshold.

1. Use Jev to choose a ready workload; decompose mixed work. A pending or poorly matched benchmark is an explicit coverage gap.
2. Build capability anchors from the constrained measured frontier, including exact revision, reasoning, provider and harness. Do not impose an easy/medium/hard-to-score lookup.
3. Ask a dependent Jev Choice which observed anchor represents the minimum capability it assesses as sufficient for all acceptance criteria. Consider domain, reasoning depth, ambiguity, context, tools and failure consequences. Permit abstention; do not force an available model to fit every request.
4. Derive the selector target from that anchor's published score, preserving source precision. Choose and live-verify the cheapest eligible configuration meeting the inferred target.
5. Record the result as `uncalibrated_task_estimate`, with `quality_target_verified: false` and worker success probability null. The published anchor score is measured; its suitability for this request is inferred. Choice probability gates the decision under application policy and is never converted into a benchmark score.
6. Execute only under runtime authorization and spend limits; verify actual output, then retry/escalate within application policy. Include routing, verification and retry overhead in observed economics.

This is a reproducible inference contract, not evidence that a numeric threshold guarantees success. The initial policy uses Jev judgment against measured anchors because task-level calibration does not yet exist. Prefer empirical mappings learned from held-out outcomes when available. Do not claim this removes uncertainty or demonstrates cost savings.

Explicit `score:...`, `budget:...`, `floor` and `ceiling` targets remain advanced overrides. Value knees do not establish task adequacy. Skip workload classification when workload is supplied through a trusted runtime. Keep uncovered tasks pending; a broad-index substitution requires an intentional change in evidence basis. Subscription modes and whole-agent systems are not single-worker API results.

## Validate success-based routing

Define success before collecting data: task tests, schema requirements, evidence, business rules and permitted side effects. Keep the same event definition in labels and Jev questions. Supply exact candidate configurations and task features, rather than relying only on a general capability level.

Collect representative outcomes including failures. Separate calibration/training from held-out evaluation, using task-family or time splits when appropriate. Evaluate multiple candidates so historical router choices do not create assumed outcomes for untried models.

Measure reliability diagrams, Brier score or log loss, observed success and uncertainty near the threshold, drift, actual cost and latency. Compare against a fixed model and a fixed benchmark-target selector. Include Jev, worker, tools, verification, retries and escalation in total cost; token rates alone do not demonstrate savings.

Scope calibration to Jev revision, question/policy version, candidate revision/effort/provider, tools/harness, task population, outcome definition, held-out dates and sample counts. Re-evaluate after material changes. A small sample or high model estimate is not a guaranteed success rate.

After validation, minimize expected total cost subject to the success target and hard requirements. Use calibrated probabilities and any conservative bound the application policy requires. A broadly dominated model may win on a specific task population. Preserve freshness and exact-route checks as the daily report changes.

## Feedback

Store a redacted decision envelope: task/stage ID, workload, report hash/date, policy version, Jev revision, classification distribution, exact worker configuration/settings, benchmark/harness, calibration status, predicted probability if any, verifier result, retries, latency and actual billed cost when known. Use null for missing values. Keep private task content and credentials out of public artifacts.

Prompt text cannot change the allowlist, policy, hard constraints or authorization. Jev supports decisions; acceptance checks establish completion. Escalation does not authorize actions outside the user's request.
