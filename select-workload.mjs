import {readFile} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
import {loadSnapshot,verifyCatalog,verifyEndpoint} from './select-model.mjs';

const finite=Number.isFinite;
const fail=message=>{throw Error(message);};
function timestamp(value,data,now) {
  const t=Date.parse(value),hours=data.freshness?.recommended_max_age_hours;
  if(!finite(t)||t>now+300000||!finite(hours)||hours<=0||now-t>hours*3600000)fail('Workload evidence is stale or has an invalid verification timestamp');
}
export function pareto(rows) {
  const sorted=[...rows].sort((a,b)=>a.score-b.score||a.benchmark_task_cost_usd-b.benchmark_task_cost_usd||a.configuration_id.localeCompare(b.configuration_id));
  return sorted.filter((a,i)=>!sorted.some((b,j)=>j!==i&&b.score>=a.score&&b.benchmark_task_cost_usd<=a.benchmark_task_cost_usd&&
    (b.score>a.score||b.benchmark_task_cost_usd<a.benchmark_task_cost_usd||j<i)));
}
function validateRow(row,profile,data,now) {
  if(!finite(row.score)||!finite(row.source_raw_score)||!finite(row.benchmark_task_cost_usd)||row.benchmark_task_cost_usd<0)fail('Missing measured workload score or cost');
  if(row.score!==row.source_raw_score*profile.score_multiplier||row.score_unit!==profile.score_unit)fail('Workload score scale mismatch');
  if(row.benchmark_id!==profile.evaluation_slug||row.benchmark_version!==profile.benchmark_version||row.harness_id!==profile.harness_id)fail('Workload benchmark version or harness mismatch');
  if(row.eligible_for_frontier!==true||row.benchmark_score_is_estimated!==false||row.benchmark_cost_status!=='complete_as_published'||/fallback/i.test(row.model_name??''))fail('Workload configuration is ineligible, estimated, provisional or uses fallback');
  if(row.request?.model!==row.openrouter_model_id||!row.openrouter_canonical_slug)fail('Workload request identity mismatch');
  const reasoning=row.request.reasoning;
  if(row.reasoning_control?.type==='enabled') {
    if(row.effort!==null||!row.reasoning_control.verified_native_setting||typeof reasoning?.enabled!=='boolean'||reasoning.enabled!==row.reasoning_control.value||'effort' in reasoning)fail('Workload native reasoning control mismatch');
  } else if(typeof row.effort!=='string'||reasoning?.effort!==row.effort||'enabled' in reasoning)fail('Workload effort mismatch');
  const key=row.effort??`thinking-${reasoning.enabled?'enabled':'disabled'}`;
  if(row.configuration_id!==`${row.openrouter_model_id}@${key}`)fail('Workload configuration ID mismatch');
  const provider=row.request.provider;
  if(provider?.require_parameters!==true||provider?.allow_fallbacks!==false||provider?.only?.length!==1||provider.only[0]!==row.endpoint_verification?.provider_tag)fail('Workload route must pin one standard provider with parameters required and no fallback');
  for(const value of [row.benchmark_verified_at,row.openrouter_verified_at,row.endpoint_verification.verified_at,row.provider_documentation_verified_at])timestamp(value,data,now);
  const evidence=profile.evaluated_configurations.find(x=>x.configuration_id===row.configuration_id);
  if(!evidence||['score','source_raw_score','benchmark_task_cost_usd','benchmark_id','benchmark_version','harness_id','openrouter_canonical_slug'].some(k=>row[k]!==evidence[k])||JSON.stringify(row.request)!==JSON.stringify(evidence.request))fail('Workload row does not match its evaluated configuration');
}
export function validateWorkloadSnapshot(data,now=Date.now()) {
  if(data.schema_version!=='1.0.0'||!Array.isArray(data.profiles))fail('Unsupported workload report schema');
  timestamp(data.checked_at,data,now);
  const names=new Set();
  for(const profile of data.profiles) {
    if(names.has(profile.id))fail('Duplicate workload ID');names.add(profile.id);
    if(profile.cost_metric!==`USD_per_${profile.evaluation_slug}_task`)fail('Workload cost metric mismatch');
    if(profile.score_is_request_success_probability!==false)fail('Benchmark score is not a request success probability');
    if(profile.status!=='ready') {
      if(profile.frontier.length||profile.limited_free_configurations.length)fail('Pending workload cannot have actionable rows');
      continue;
    }
    if(profile.methodology_version!==data.general_intelligence_index_version)fail('Workload methodology version mismatch');
    timestamp(profile.source_verified_at,data,now);timestamp(profile.methodology_verified_at,data,now);
    const ids=new Set();
    for(const row of profile.evaluated_configurations) {
      if(ids.has(row.configuration_id))fail('Duplicate evaluated workload configuration');ids.add(row.configuration_id);
      validateRow(row,profile,data,now);
    }
    for(const [rows,isFree] of [[profile.frontier,false],[profile.limited_free_configurations,true]]) {
      let previous=null;
      for(let i=0;i<rows.length;i++) {
        const row=rows[i];validateRow(row,profile,data,now);
        if(isFree?(row.benchmark_task_cost_usd!==0||row.requires_opt_in!==true):row.benchmark_task_cost_usd<=0)fail('Invalid paid/free workload lane');
        if(row.minimum_score_exclusive!==(previous?.score??null)||row.maximum_score_inclusive!==row.score||row.minimum_budget_inclusive!==row.benchmark_task_cost_usd||row.maximum_budget_exclusive!==(rows[i+1]?.benchmark_task_cost_usd??null))fail('Workload score/budget intervals are not contiguous');
        if(previous&&(row.score<=previous.score||row.benchmark_task_cost_usd<=previous.benchmark_task_cost_usd))fail('Workload frontier ordering mismatch');
        previous=row;
      }
      const candidates=profile.evaluated_configurations.filter(r=>isFree?r.requires_opt_in===true:r.requires_opt_in!==true);
      if(JSON.stringify(pareto(candidates).map(r=>r.configuration_id))!==JSON.stringify(rows.map(r=>r.configuration_id)))fail('Workload frontier misses a winner or retains a dominated configuration');
    }
    for(const role of ['floor','ceiling']) {
      const rec=profile.recommendations[role];if(!rec)continue;
      const row=profile.frontier.find(r=>r.configuration_id===rec.configuration_id);
      if(!row||row.score!==rec.score||row.benchmark_task_cost_usd!==rec.benchmark_task_cost_usd)fail('Workload recommendation mismatch');
    }
  }
  if(data.coding_agent_systems?.openrouter_actionable!==false||data.coding_agent_systems?.request!==null||data.coding_agent_systems?.systems?.some(r=>r.request!==null||r.openrouter_actionable!==false||r.subscription_task_cost_usd!==null))fail('Agent systems cannot masquerade as standalone OpenRouter models or subscription task prices');
  return data;
}
function constrained(row,profile,options) {
  if(options.harness_id&&options.harness_id!==profile.harness_id)return false;
  if(options.benchmark_version&&options.benchmark_version!==profile.benchmark_version)return false;
  if(options.min_context_tokens!==undefined&&(!finite(row.context_window_tokens)||row.context_window_tokens<options.min_context_tokens))return false;
  const params=[...profile.required_parameters,...(options.required_parameters??[])];
  if(params.some(p=>!row.endpoint_verification.supported_parameters.includes(p)))return false;
  if((options.input_modalities??[]).some(m=>!row.input_modalities.includes(m)))return false;
  return true;
}
export function selectWorkloadConfiguration(data,workload,target='floor',options={}) {
  const allowed=new Set(['allow_limited_free','required_parameters','min_context_tokens','input_modalities','harness_id','benchmark_version']);
  if(Object.keys(options).some(k=>!allowed.has(k)))fail('Unsupported workload constraint; unknown constraints are never ignored');
  if(options.min_context_tokens!==undefined&&(!finite(options.min_context_tokens)||options.min_context_tokens<0))fail('Invalid minimum context constraint');
  const profile=data.profiles.find(p=>p.id===workload);
  if(!profile||profile.status!=='ready')fail('Unknown or pending workload; no general-model substitution');
  // Filter every eligible configuration before computing dominance. A globally
  // dominated model can win once a context, modality or tool constraint applies.
  const rows=pareto(profile.evaluated_configurations.filter(r=>(r.requires_opt_in!==true||options.allow_limited_free===true)&&constrained(r,profile,options)));
  if(target==='floor'||target==='ceiling') {
    const rec=profile.recommendations[target];
    if(!rec)fail('No clear workload value knee; specify a benchmark score or task-cost budget');
    return rows.find(r=>r.configuration_id===rec.configuration_id)??fail('Workload recommendation does not meet the required constraints');
  }
  if(typeof target==='string'&&target.startsWith('budget:'))target={max_task_cost_usd:Number(target.slice(7))};
  if(typeof target==='object'&&target!==null) {
    if(Object.keys(target).length!==1||!finite(target.max_task_cost_usd)||target.max_task_cost_usd<0)fail('Budget must be a nonnegative finite benchmark-task cost');
    return rows.filter(r=>r.benchmark_task_cost_usd<=target.max_task_cost_usd).at(-1)??fail('No eligible workload configuration fits the budget');
  }
  if(typeof target==='string'&&target.startsWith('score:'))target=target.slice(6);
  if((typeof target!=='number'&&(typeof target!=='string'||!target.trim()))||!finite(Number(target)))fail('Invalid workload benchmark score');
  return rows.find(r=>r.score>=Number(target))??fail('No eligible workload configuration meets the score and constraints');
}
async function getJson(url) {
  const r=await fetch(url,{signal:AbortSignal.timeout(20000),cache:'no-store'});
  if(!r.ok)fail(`HTTP ${r.status} fetching workload route metadata`);
  return r.json();
}
export async function buildWorkloadSelection(source,workload,target='floor',options={}) {
  const data=validateWorkloadSnapshot(await loadSnapshot(source));
  const profile=data.profiles.find(p=>p.id===workload);
  const row=selectWorkloadConfiguration(data,workload,target,options);
  const params=[...new Set([...profile.required_parameters,...(options.required_parameters??[])])];
  const catalog=await getJson('https://openrouter.ai/api/v1/models');
  const live=verifyCatalog(row,catalog,params);
  if(options.min_context_tokens!==undefined&&live.context_length<options.min_context_tokens)fail('Live context window no longer meets the workload requirement');
  if((options.input_modalities??[]).some(m=>!live.architecture?.input_modalities?.includes(m)))fail('Live input modality no longer meets the workload requirement');
  const ep=await getJson(`https://openrouter.ai/api/v1/models/${row.openrouter_model_id}/endpoints`);
  verifyEndpoint(row,ep,params);
  return {checked_at:data.checked_at,workload:profile.id,benchmark:profile.benchmark_name,benchmark_version:profile.benchmark_version,harness_id:profile.harness_id,
    configuration_id:row.configuration_id,score:row.score,score_unit:profile.score_unit,benchmark_task_cost_usd:row.benchmark_task_cost_usd,
    cost_basis:profile.cost_basis,api_endpoint:row.api_endpoint,request:row.request,
    note:'Benchmark-specific evidence, not a calibrated task success probability or prompt spending cap. Add messages/input, tools and sufficient output budget; preserve reasoning across turns.'};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href) {
  try {
    const [source='workloads.json',workload,target='floor',parameters='',...flags]=process.argv.slice(2);
    const options={required_parameters:parameters.split(',').filter(Boolean)};
    for(const flag of flags) {
      if(flag==='--allow-limited-free')options.allow_limited_free=true;
      else if(flag.startsWith('--min-context='))options.min_context_tokens=Number(flag.slice(14));
      else if(flag.startsWith('--harness='))options.harness_id=flag.slice(10);
      else if(flag.startsWith('--benchmark-version='))options.benchmark_version=flag.slice(20);
      else if(flag.startsWith('--input='))options.input_modalities=flag.slice(8).split(',').filter(Boolean);
      else fail('Unknown workload selector option');
    }
    console.log(JSON.stringify(await buildWorkloadSelection(source,workload,target,options),null,2));
  } catch(error) {console.error(error.message);process.exitCode=1;}
}
