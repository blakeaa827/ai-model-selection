// Regression-safe frontier and explicit missing-data handling.
// Execute: node pipeline/test-frontier.mjs
// Publication remains gated by full schema, selector, endpoint and source checks.
import {readFile,writeFile} from 'node:fs/promises';
const [input,output]=process.argv.slice(2);
if(!input||!output)throw Error('Usage: node pipeline/build-frontier.mjs verified.json output.json');
const src=JSON.parse(await readFile(input,'utf8'));
if(!src.methodology_version||!Array.isArray(src.configurations))throw Error('Invalid evidence');
const checked=Date.parse(src.checked_at);
if(!Number.isFinite(checked)||checked>Date.now()+300000||Date.now()-checked>48*3600000)throw Error('Stale evidence');
const rejected=[],valid=[];
for(const r of src.configurations){
 const reasons=[];
 if(r.methodology_version!==src.methodology_version)reasons.push('methodology_mismatch');
 if(!Number.isFinite(r.intelligence_score)||!Number.isFinite(r.benchmark_task_cost_usd)||r.benchmark_task_cost_usd<0)reasons.push('missing_measured_pair');
 if(r.score_estimated||r.cost_provisional)reasons.push('provisional');
 if(!r.aa_source_url||!r.aa_configuration_verified_at)reasons.push('missing_source');
 if(!r.openrouter_model_id||r.request?.model!==r.openrouter_model_id||!r.canonical_revision)reasons.push('routing_identity');
 if(!r.openrouter_verified_at||!r.endpoint_verification?.verified_at)reasons.push('endpoint_unverified');
 if(r.request?.provider?.require_parameters!==true||r.request?.provider?.allow_fallbacks!==false||r.request?.provider?.only?.length!==1)reasons.push('unsafe_provider');
 const control=r.request?.reasoning;
 if(!control||!((typeof control.enabled==='boolean'&&!('effort' in control))||(typeof control.effort==='string'&&!('enabled' in control))))reasons.push('reasoning_invalid');
 for(const stamp of [r.aa_configuration_verified_at,r.openrouter_verified_at,r.endpoint_verification?.verified_at]){
  const time=Date.parse(stamp);
  if(!Number.isFinite(time)||time>Date.now()+300000||Date.now()-time>48*3600000)reasons.push('stale_verification');
 }
 if(r.limited_free||r.restricted||r.retired)reasons.push('not_paid_default');
 if(reasons.length)rejected.push({id:r.configuration_id??r.openrouter_model_id??'unknown',reasons:[...new Set(reasons)]});
 else valid.push(r);
}
const frontier=valid.filter(a=>!valid.some(b=>a!==b&&b.intelligence_score>=a.intelligence_score&&b.benchmark_task_cost_usd<=a.benchmark_task_cost_usd&&(b.intelligence_score>a.intelligence_score||b.benchmark_task_cost_usd<a.benchmark_task_cost_usd))).sort((a,b)=>a.intelligence_score-b.intelligence_score||a.benchmark_task_cost_usd-b.benchmark_task_cost_usd);
const unique=frontier.filter((r,i)=>!i||r.intelligence_score!==frontier[i-1].intelligence_score||r.benchmark_task_cost_usd!==frontier[i-1].benchmark_task_cost_usd);
const rows=unique.map((r,i)=>{
 const prev=unique[i-1],next=unique[i+1];
 return {...r,minimum_score_exclusive:prev?.intelligence_score??null,maximum_score_inclusive:r.intelligence_score,minimum_budget_inclusive:r.benchmark_task_cost_usd,maximum_budget_exclusive:next?.benchmark_task_cost_usd??null,marginal_from_previous:prev?{score_gain:r.intelligence_score-prev.intelligence_score,added_usd:r.benchmark_task_cost_usd-prev.benchmark_task_cost_usd,percentage_cost_increase:prev.benchmark_task_cost_usd===0?null:100*(r.benchmark_task_cost_usd-prev.benchmark_task_cost_usd)/prev.benchmark_task_cost_usd,usd_per_additional_index_point:(r.benchmark_task_cost_usd-prev.benchmark_task_cost_usd)/(r.intelligence_score-prev.intelligence_score)}:null};
});
await writeFile(output,JSON.stringify({methodology_version:src.methodology_version,checked_at:src.checked_at,status:rows.length?'computed_not_published':'no_verified_frontier',frontier:rows,rejected},null,2)+'\n');
if(!rows.length)process.exitCode=2;
