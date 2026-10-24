// Deterministic, fail-closed frontier builder. Node 20+.
// Input is independently verified configuration-level evidence, NOT release bounds.
// node pipeline/build-frontier.mjs verified-configurations.json output.json
import {readFile,writeFile} from 'node:fs/promises';
const [input,output]=process.argv.slice(2);
if(!input||!output)throw Error('Usage: node pipeline/build-frontier.mjs verified-configurations.json output.json');
const source=JSON.parse(await readFile(input,'utf8'));
if(!source.methodology_version||!Array.isArray(source.configurations))throw Error('Missing methodology/version or configurations');
const checked=Date.parse(source.checked_at);
if(!Number.isFinite(checked)||Date.now()-checked>48*3600000||checked>Date.now()+300000)throw Error('Evidence stale or invalid');
const rejected=[],eligible=[];
for(const row of source.configurations){
 const reasons=[];
 if(row.methodology_version!==source.methodology_version)reasons.push('methodology_mismatch');
 if(!Number.isFinite(row.intelligence_score)||!Number.isFinite(row.benchmark_task_cost_usd)||row.benchmark_task_cost_usd<0)reasons.push('missing_measured_pair');
 if(row.score_estimated||row.cost_provisional)reasons.push('provisional_measurement');
 if(!row.aa_source_url||!row.aa_configuration_verified_at)reasons.push('missing_original_source');
 if(!row.openrouter_model_id||row.request?.model!==row.openrouter_model_id)reasons.push('missing_exact_route');
 if(!row.canonical_revision||!row.openrouter_verified_at||!row.endpoint_verification?.verified_at)reasons.push('unverified_revision_or_endpoint');
 if(row.request?.provider?.require_parameters!==true||row.request?.provider?.allow_fallbacks!==false||row.request?.provider?.only?.length!==1)reasons.push('unsafe_provider_routing');
 const control=row.request?.reasoning;
 if(!control||!(typeof control.enabled==='boolean'&&!('effort'in control)||typeof control.effort==='string'&&!('enabled'in control)))reasons.push('invalid_reasoning_control');
 for(const stamp of [row.aa_configuration_verified_at,row.openrouter_verified_at,row.endpoint_verification?.verified_at]){
  const date=Date.parse(stamp);
  if(!Number.isFinite(date)||Date.now()-date>48*3600000||date>Date.now()+300000)reasons.push('stale_verification');
 }
 if(row.limited_free||row.restricted||row.retired)reasons.push('non_default_lane');
 if(reasons.length)rejected.push({id:row.configuration_id??row.openrouter_model_id??'unknown',reasons:[...new Set(reasons)]});
 else eligible.push(row);
}
eligible.sort((a,b)=>a.intelligence_score-b.intelligence_score||a.benchmark_task_cost_usd-b.benchmark_task_cost_usd);
const frontier=[];
for(const candidate of eligible){
 if(eligible.some(other=>other!==candidate&&other.intelligence_score>=candidate.intelligence_score&&other.benchmark_task_cost_usd<=candidate.benchmark_task_cost_usd&&(other.intelligence_score>candidate.intelligence_score||other.benchmark_task_cost_usd<candidate.benchmark_task_cost_usd)))continue;
 if(frontier.some(x=>x.intelligence_score===candidate.intelligence_score&&x.benchmark_task_cost_usd===candidate.benchmark_task_cost_usd))continue;
 frontier.push(candidate);
}
frontier.sort((a,b)=>a.intelligence_score-b.intelligence_score);
const result=frontier.map((row,i)=>{
 const previous=frontier[i-1],next=frontier[i+1];
 const delta=previous?{score_gain:row.intelligence_score-previous.intelligence_score,added_usd:row.benchmark_task_cost_usd-previous.benchmark_task_cost_usd,percentage_cost_increase:100*(row.benchmark_task_cost_usd-previous.benchmark_task_cost_usd)/previous.benchmark_task_cost_usd,usd_per_additional_index_point:(row.benchmark_task_cost_usd-previous.benchmark_task_cost_usd)/(row.intelligence_score-previous.intelligence_score)}:null;
 return {...row,minimum_score_exclusive:previous?.intelligence_score??null,maximum_score_inclusive:row.intelligence_score,minimum_budget_inclusive:row.benchmark_task_cost_usd,maximum_budget_exclusive:next?.benchmark_task_cost_usd??null,marginal_from_previous:delta};
});
await writeFile(output,JSON.stringify({methodology_version:source.methodology_version,checked_at:source.checked_at,status:result.length?'computed_not_published':'no_verified_frontier',frontier:result,rejected},null,2)+'\n');
if(!result.length){console.error('No eligible configurations; publication blocked');process.exitCode=2;}
