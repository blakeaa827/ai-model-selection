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
  if (data.schema_version !== "1.0.0") throw new Error("Unsupported schema version");
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
    if (!Number.isFinite(row.intelligence_score) || !Number.isFinite(row.benchmark_task_cost_usd) || row.benchmark_task_cost_usd < 0) throw new Error("Invalid score or cost");
    if (ids.has(row.configuration_id)) throw new Error("Duplicate configuration");
    ids.add(row.configuration_id);
    if (row.configuration_id !== `${row.openrouter_model_id}@${row.effort}` ||
        row.request?.model !== row.openrouter_model_id || row.request?.reasoning?.effort !== row.effort) throw new Error("Request does not match benchmark configuration");
    if (row.maximum_score_inclusive !== row.intelligence_score ||
        row.minimum_score_exclusive !== (previous?.intelligence_score ?? null)) throw new Error("Non-contiguous capability ranges");
    if (previous && (row.intelligence_score <= previous.intelligence_score || row.benchmark_task_cost_usd <= previous.benchmark_task_cost_usd)) throw new Error("Frontier is not ordered by increasing capability and cost");
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
  return data;
}

export function selectConfiguration(data, target = "floor") {
  if (target === "floor" || target === "ceiling") {
    return data.frontier.find(r => r.configuration_id === data.recommendations[target].configuration_id);
  }
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
  const efforts = model.reasoning?.supported_efforts;
  if (!Array.isArray(efforts) || !efforts.includes(row.effort)) throw new Error("Exact reasoning effort is not verified");
  for (const parameter of ["reasoning", ...requiredParameters]) {
    if (!model.supported_parameters?.includes(parameter)) throw new Error(`Required parameter unsupported: ${parameter}`);
  }
  return model;
}

export async function buildSelection(source, target = "floor", requiredParameters = []) {
  const data = validateSnapshot(await loadSnapshot(source));
  const row = selectConfiguration(data, target);
  verifyCatalog(row, await getJson("https://openrouter.ai/api/v1/models"), requiredParameters);
  return {
    checked_at: data.checked_at,
    configuration_id: row.configuration_id,
    intelligence_score: row.intelligence_score,
    benchmark_task_cost_usd: row.benchmark_task_cost_usd,
    request: row.request,
    note: "Add messages and task-specific output limits; this is not an invoice estimate."
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    const [source = "latest.json", target = "floor", parameters = ""] = process.argv.slice(2);
    console.log(JSON.stringify(await buildSelection(source, target, parameters.split(",").filter(Boolean)), null, 2));
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}

