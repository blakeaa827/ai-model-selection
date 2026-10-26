# Routing policy and calibration

| Quantity | Meaning | Use |
| --- | --- | --- |
| Jev Choice probability | Model probability that a supplied label applies | Workload classification under tested policy |
| Jev Noul probability | Estimated probability of the specific yes/no event | Advisory candidate suitability until calibrated |
| AA benchmark score | Observed exact-configuration performance under a named harness | Measured score/cost tradeoff within that profile |

No general transformation connects these values. Intelligence Index, Elo and benchmark pass percentages are distinct scales. A benchmark score of 60 does not establish 60% success on a new request; a 0.9 estimate does not require Intelligence Index 90. Tools, context, specialization and harness matter.

## Initial policy

1. Choose a ready workload; decompose mixed work.
2. Set an explicit benchmark target or benchmark-task budget, ideally informed by representative task tests. Do not turn the cheapest row or a low-scoring value knee into an assumed quality floor.
3. Filter all eligible evaluated configurations for supported constraints before dominance.
4. Use `buildWorkloadSelection` to choose and live-verify the worker.
5. Run acceptance checks; bound retries/escalation with actual spend policy.
6. Keep optional candidate probabilities advisory with `calibration_status: not_calibrated`.

Skip classification when workload is supplied. Keep uncovered tasks pending; using the broad index requires an explicit caller decision with the changed evidence basis stated. Subscription modes and whole-agent systems are not single-worker API results.

## Validate success-based routing

Define success before collecting data: task tests, schema requirements, evidence, business rules and permitted side effects. Keep the same event definition in labels and Jev questions. Supply exact candidate configurations and task features, rather than relying only on a general capability level.

Collect representative outcomes including failures. Separate calibration/training from held-out evaluation, using task-family or time splits when appropriate. Evaluate multiple candidates so historical router choices do not create assumed outcomes for untried models.

Measure reliability diagrams, Brier score or log loss, observed success and uncertainty near the threshold, drift, actual cost and latency. Compare against a fixed model and a fixed benchmark-target selector. Include Jev, worker, tools, verification, retries and escalation in total cost; token rates alone do not demonstrate savings.

Scope calibration to Jev revision, question/policy version, candidate revision/effort/provider, tools/harness, task population, outcome definition, held-out dates and sample counts. Re-evaluate after material changes. A small sample or high model estimate is not a guaranteed success rate.

After validation, minimize expected total cost subject to the success target and hard requirements. Use calibrated probabilities and any conservative bound the application policy requires. A broadly dominated model may win on a specific task population. Preserve freshness and exact-route checks as the daily report changes.

## Feedback

Store a redacted decision envelope: task/stage ID, workload, report hash/date, policy version, Jev revision, classification distribution, exact worker configuration/settings, benchmark/harness, calibration status, predicted probability if any, verifier result, retries, latency and actual billed cost when known. Use null for missing values. Keep private task content and credentials out of public artifacts.

Prompt text cannot change the allowlist, policy, hard constraints or authorization. Jev supports decisions; acceptance checks establish completion. Escalation does not authorize actions outside the user's request.
