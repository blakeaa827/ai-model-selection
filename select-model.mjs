import { readFile } from "node:fs/promises";
import { pathToFileURL } from "node:url";

async function getJson(url) {
  const response = await fetch(url, { signal: AbortSignal.timeout(20000), cache: "no-store" });
  if (!response.ok) throw new Error(`HTTP ${response.status} fetching ${url}`);
  return response.json();
}

export async function loadSnapshot(source) {
  return /^https:\/\//.test(source) ? getJson(source) : JSON.parse(await readFile(source, "utf8"));
}

export function validateSnapshot(data, now = Date.now()) {
  if (!["1.0.0", "1.1.0"].includes(data.schema_version)) throw new Error("Unsupported schema version");
  if (data.benchmark?.cost_metric !== "weighted_USD_per_Intelligence_Index_task") throw new Error("Incompatible cost metric");
  const checked = Date.parse(data.checked_at);
  if (!Number.isFinite(checked) || checked > now + 300000) throw new Error("Invalid check timestamp");
  const maxAge = data.freshness?.recommended_max_age_hours;
  if (!(Number.isFinite(maxAge) && maxAge > 0)) throw new Error("Invalid freshness policy");
  if (now - checked > maxAge * 3600000) throw new Error("Model selection report is stale; refresh before routing");
  if (!Array.isArray(data.frontier) || !data.frontier.length) throw new Error("Empty frontier");
  let previous = null;
  const ids = new Set();
  for (const row of data.frontier) {
    const evidence = data.evaluated_configurations?.find(r => r.configuration_id === row.configuration_id);
    for (const record of [row, evidence].filter(Boolean)) {
      if (record.eligible_for_frontier === false || record.benchmark_score_is_estimated === true ||
          record.benchmark_mode === "multi_model_fallback" || /fallback/i.test(record.AA_model_label ?? "") ||
          (record.benchmark_cost_status && record.benchmark_cost_status !== "complete_as_published")) {
        throw new Error("Configuration benchmark eligibility is unverified or provisional");
      }
    }
    if (!Number.isFinite(row.intelligence_score) || !Number.isFinite(row.benchmark_task_cost_usd) || row.benchmark_task_cost_usd < 0) throw new Error("Invalid score or cost");
    if (ids.has(row.configuration_id)) throw new Error("Duplicate configuration");
    ids.add(row.configuration_id);
    const reasoning = row.request?.reasoning;
    const enabledControl = row.reasoning_control?.type === "enabled";
    const controlKey = enabledControl ? `thinking-${reasoning?.enabled ? "enabled" : "disabled"}` : row.effort;
    if (row.configuration_id !== `${row.openrouter_model_id}@${controlKey}` || row.request?.model !== row.openrouter_model_id ||
        (enabledControl ? (row.effort !== null || typeof reasoning?.enabled !== "boolean" ||
          reasoning.enabled !== row.reasoning_control.value || "effort" in reasoning) :
          (!row.effort || reasoning?.effort !== row.effort || "enabled" in reasoning))) throw new Error("Request does not match benchmark configuration");
    if (row.request.provider?.require_parameters !== true || row.request.provider?.allow_fallbacks !== false ||
        !Array.isArray(row.request.provider?.only) || row.request.provider.only.length !== 1) throw new Error("Strict provider routing is required");
    for (const value of [row.openrouter_verified_at, row.benchmark_verified_at ?? data.checked_at,
      row.endpoint_verification?.verified_at ?? row.openrouter_verified_at]) {
      const verified = Date.parse(value);
      if (!Number.isFinite(verified) || verified > now + 300000 || now - verified > maxAge * 3600000) throw new Error("Configuration verification is stale or invalid");
    }
    if (row.maximum_score_inclusive !== row.intelligence_score ||
        row.minimum_score_exclusive !== (previous?.intelligence_score ?? null)) throw new Error("Non-contiguous capability ranges");
    if (previous && (row.intelligence_score <= previous.intelligence_score || row.benchmark_task_cost_usd <= previous.benchmark_task_cost_usd)) throw new Error("Frontier is not ordered by increasing capability and cost");
    if (data.schema_version === "1.1.0" && (row.minimum_budget_inclusive !== row.benchmark_task_cost_usd ||
        row.maximum_budget_exclusive !== (data.frontier[data.frontier.indexOf(row) + 1]?.benchmark_task_cost_usd ?? null))) throw new Error("Non-contiguous budget ranges");
    previous = row;
  }
  for (const role of ["floor", "ceiling"]) {
    const recommendation = data.recommendations?.[role];
    const row = data.frontier.find(r => r.configuration_id === recommendation?.configuration_id);
    if (!row || row.openrouter_model_id !== recommendation.openrouter_model_id ||
        row.effort !== recommendation.effort || row.intelligence_score !== recommendation.intelligence_score ||
        row.benchmark_task_cost_usd !== recommendation.benchmark_task_cost_usd ||
        JSON.stringify(row.request) !== JSON.stringify(recommendation.request)) throw new Error(`Invalid ${role} recommendation`);
  }
  if (data.limited_free_configurations?.length) {
    const merged = withLimitedFree(data);
    validateSnapshot({...merged, limited_free_configurations: []}, now);
    if (data.limited_free_configurations.some(r => r.benchmark_task_cost_usd !== 0 || r.requires_opt_in !== true)) throw new Error("Invalid limited free lane");
  }
  return data;
}

function withLimitedFree(data) {
  const rows = [...(data.limited_free_configurations ?? []), ...data.frontier];
  const frontier = rows.filter(a => !rows.some(b => b !== a && b.intelligence_score >= a.intelligence_score &&
    b.benchmark_task_cost_usd <= a.benchmark_task_cost_usd)).sort((a,b) => a.intelligence_score - b.intelligence_score);
  return {...data, frontier: frontier.map((r,i) => ({...r,
    minimum_score_exclusive: frontier[i-1]?.intelligence_score ?? null,
    maximum_score_inclusive: r.intelligence_score,
    minimum_budget_inclusive: r.benchmark_task_cost_usd,
    maximum_budget_exclusive: frontier[i+1]?.benchmark_task_cost_usd ?? null}))};
}

export function selectConfiguration(data, target = "floor", options = {}) {
  if (options.allow_limited_free === true) data = withLimitedFree(data);
  if (target === "floor" || target === "ceiling") {
    return data.frontier.find(r => r.configuration_id === data.recommendations[target].configuration_id);
  }
  if (typeof target === "string" && target.startsWith("budget:")) target = {max_task_cost_usd: Number(target.slice(7))};
  if (typeof target === "object" && target !== null) {
    const keys = Object.keys(target);
    if (keys.length !== 1 || keys[0] !== "max_task_cost_usd" || !Number.isFinite(target.max_task_cost_usd) || target.max_task_cost_usd < 0) throw new Error("Budget must be a nonnegative finite benchmark task cost");
    const rows = data.frontier.filter(r => r.benchmark_task_cost_usd <= target.max_task_cost_usd);
    if (!rows.length) throw new Error("No eligible configuration fits the requested budget");
    return rows.at(-1);
  }
  if (typeof target === "string" && target.startsWith("score:")) target = target.slice(6);
  if ((typeof target !== "number" && (typeof target !== "string" || !target.trim())) ||
      !Number.isFinite(Number(target)) || Number(target) < 0) throw new Error("Target must be floor, ceiling, or a nonnegative minimum score");
  const row = data.frontier.find(r => r.intelligence_score >= Number(target));
  if (!row) throw new Error("No eligible configuration meets the requested minimum score");
  return row;
}

export function verifyCatalog(row, catalog, requiredParameters = []) {
  if (!Array.isArray(catalog?.data)) throw new Error("Invalid OpenRouter catalog response");
  const model = catalog.data.find(m => m.id === row.openrouter_model_id);
  if (!model) throw new Error("Recommended model is no longer listed by OpenRouter");
  if (model.canonical_slug !== row.openrouter_canonical_slug) throw new Error("Catalog model revision changed; re-evaluate before routing");
  if (model.expiration_date && Date.parse(model.expiration_date) <= Date.now()) throw new Error("Model is expired");
  if (row.reasoning_control?.type === "enabled") {
    if (!model.reasoning || !row.reasoning_control.verified_native_setting ||
        (row.request.reasoning.enabled === false && model.reasoning.mandatory)) throw new Error("Exact thinking control is not verified");
  } else {
    const efforts = model.reasoning?.supported_efforts;
    if (!Array.isArray(efforts) || !efforts.includes(row.effort)) throw new Error("Exact reasoning effort is not verified");
  }
  for (const parameter of ["reasoning", ...requiredParameters]) {
    if (!model.supported_parameters?.includes(parameter)) throw new Error(`Required parameter unsupported: ${parameter}`);
  }
  return model;
}

export function verifyEndpoint(row, metadata, requiredParameters = []) {
  const tag = row.request.provider.only[0];
  const endpoint = metadata?.data?.endpoints?.find(e => e.tag === tag);
  if (!endpoint || endpoint.status !== 0 || endpoint.model_id !== row.openrouter_model_id) throw new Error("Standard provider endpoint is unavailable");
  if (!endpoint.name?.includes(row.openrouter_canonical_slug)) throw new Error("Provider endpoint revision does not match the benchmark configuration");
  if (row.endpoint_verification?.quantization && endpoint.quantization !== row.endpoint_verification.quantization) throw new Error("Provider quantization changed; re-evaluate before routing");
  for (const parameter of ["reasoning", ...requiredParameters]) {
    if (!endpoint.supported_parameters?.includes(parameter)) throw new Error(`Required endpoint parameter unsupported: ${parameter}`);
  }
  if (requiredParameters.includes("tools") && row.openrouter_model_id.startsWith("openai/") &&
      row.api_endpoint !== "https://openrouter.ai/api/v1/responses") throw new Error("OpenAI tool calling requires the verified Responses endpoint");
  return endpoint;
}

export async function buildSelection(source, target = "floor", requiredParameters = [], options = {}) {
  const data = validateSnapshot(await loadSnapshot(source));
  const row = selectConfiguration(data, target, options);
  verifyCatalog(row, await getJson("https://openrouter.ai/api/v1/models"), requiredParameters);
  verifyEndpoint(row, await getJson(`https://openrouter.ai/api/v1/models/${row.openrouter_model_id}/endpoints`), requiredParameters);
  return {
    checked_at: data.checked_at,
    configuration_id: row.configuration_id,
    intelligence_score: row.intelligence_score,
    benchmark_task_cost_usd: row.benchmark_task_cost_usd,
    api_endpoint: row.api_endpoint,
    request: row.request,
    note: "Add input for Responses or messages for Chat Completions, plus task-specific output limits; this is not an invoice estimate."
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    const [source = "latest.json", target = "floor", parameters = "", optIn = ""] = process.argv.slice(2);
    if (optIn && optIn !== "--allow-limited-free") throw new Error("Unknown option");
    console.log(JSON.stringify(await buildSelection(source, target, parameters.split(",").filter(Boolean), {allow_limited_free: optIn === "--allow-limited-free"}), null, 2));
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}

