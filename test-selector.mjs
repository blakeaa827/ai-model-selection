import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {validateSnapshot, selectConfiguration, verifyCatalog, verifyEndpoint, buildSelection} from './select-model.mjs';
const reportPath=process.argv[2]||new URL('./latest.json',import.meta.url).pathname;
const data = JSON.parse(await readFile(reportPath,'utf8'));
const asOf = Date.parse(data.checked_at);
validateSnapshot(data, asOf);
for (const row of data.frontier) {
 assert.equal(selectConfiguration(data,row.intelligence_score).configuration_id,row.configuration_id);
 assert.equal(selectConfiguration(data,{max_task_cost_usd:row.benchmark_task_cost_usd}).configuration_id,row.configuration_id);
 if (row.minimum_score_exclusive !== null) {
  assert.equal(selectConfiguration(data,(row.minimum_score_exclusive+row.intelligence_score)/2).configuration_id,row.configuration_id);
 }
 if (row.maximum_budget_exclusive !== null) {
  assert.equal(selectConfiguration(data,{max_task_cost_usd:(row.minimum_budget_inclusive+row.maximum_budget_exclusive)/2}).configuration_id,row.configuration_id);
 }
}
const budgetRow=data.frontier[Math.min(2,data.frontier.length-1)];
assert.equal(selectConfiguration(data,`budget:${budgetRow.benchmark_task_cost_usd}`).configuration_id,budgetRow.configuration_id);
assert.equal(selectConfiguration(data,`score:${budgetRow.intelligence_score}`).configuration_id,budgetRow.configuration_id);
assert.throws(()=>selectConfiguration(data,{max_task_cost_usd:0}),/No eligible/);
assert.throws(()=>selectConfiguration(data,{max_task_cost_usd:-1}),/Budget/);
assert.throws(()=>selectConfiguration(data,'budget:NaN'),/Budget/);
assert.throws(()=>selectConfiguration(data,data.frontier.at(-1).intelligence_score+1),/No eligible/);
const free=data.limited_free_configurations[0];
if(free){
assert.equal(selectConfiguration(data,'budget:0',{allow_limited_free:true}).configuration_id,free.configuration_id);
assert.equal(selectConfiguration(data,free.intelligence_score,{allow_limited_free:true}).configuration_id,free.configuration_id);
const above=data.frontier.find(r=>r.intelligence_score>free.intelligence_score);
if(above)assert.equal(selectConfiguration(data,free.intelligence_score+.0001,{allow_limited_free:true}).configuration_id,above.configuration_id);
}else assert.throws(()=>selectConfiguration(data,'budget:0',{allow_limited_free:true}),/No eligible/);
assert.throws(()=>validateSnapshot(data,asOf+49*3600000),/stale/);
const stale=structuredClone(data);stale.frontier[0].openrouter_verified_at='2026-10-01T00:00:00Z';
assert.throws(()=>validateSnapshot(stale,asOf),/stale/);
if(free){const staleFree=structuredClone(data);staleFree.limited_free_configurations[0].openrouter_verified_at='2026-10-01T00:00:00Z';
assert.throws(()=>validateSnapshot(staleFree,asOf),/stale/);
}
const invalid=structuredClone(data);invalid.frontier[0].request.reasoning.effort=null;
assert.throws(()=>validateSnapshot(invalid,asOf),/configuration/);
const ineligible=structuredClone(data);ineligible.frontier[0].eligible_for_frontier=false;
assert.throws(()=>validateSnapshot(ineligible,asOf),/eligibility/);
const provisional=structuredClone(data);
provisional.evaluated_configurations.find(r=>r.configuration_id===provisional.frontier[0].configuration_id).benchmark_cost_status='provisional_incomplete_tiered_pricing';
assert.throws(()=>validateSnapshot(provisional,asOf),/provisional/);
const estimated=structuredClone(data);estimated.frontier[0].benchmark_score_is_estimated=true;
assert.throws(()=>validateSnapshot(estimated,asOf),/eligibility/);
// Mock metadata isolates contract rejection from transient public HTTP failures.
const row=data.frontier[0];
const catalog={data:[{id:row.openrouter_model_id,canonical_slug:row.openrouter_canonical_slug,reasoning:{mandatory:false,supported_efforts:[row.effort]},supported_parameters:['reasoning','tools']}]};
const endpoint={data:{endpoints:[{model_id:row.openrouter_model_id,name:'Verified | '+row.openrouter_canonical_slug,tag:row.request.provider.only[0],status:0,quantization:row.endpoint_verification.quantization,supported_parameters:['reasoning','tools']}]}};
verifyCatalog(row,catalog,['tools']);verifyEndpoint(row,endpoint,['tools']);
const changed=structuredClone(catalog);changed.data[0].canonical_slug+='-changed';
assert.throws(()=>verifyCatalog(row,changed),/revision changed/);
const wrongQuant=structuredClone(endpoint);wrongQuant.data.endpoints[0].quantization='fp4';
assert.throws(()=>verifyEndpoint(row,wrongQuant),/quantization changed/);
const missing=structuredClone(endpoint);missing.data.endpoints[0].supported_parameters=['reasoning'];
assert.throws(()=>verifyEndpoint(row,missing,['tools']),/unsupported/);
const unavailable=structuredClone(endpoint);unavailable.data.endpoints[0].status=1;
assert.throws(()=>verifyEndpoint(row,unavailable),/unavailable/);
// End-to-end public-data selection, with clock and HTTP mocked; no generation call.
const priorFetch=globalThis.fetch;const priorNow=Date.now;
Date.now=()=>asOf;
globalThis.fetch=async url=>({ok:true,json:async()=>String(url).endsWith('/models')?catalog:endpoint});
try {
 const result=await buildSelection(reportPath,`budget:${row.benchmark_task_cost_usd}`,['tools']);
 assert.equal(result.request.model,row.request.model);assert.deepEqual(result.request.reasoning,row.request.reasoning);
 assert.equal(result.api_endpoint,row.api_endpoint);
} finally {globalThis.fetch=priorFetch;Date.now=priorNow;}
console.log('Passed: all score/budget boundaries, free opt-in, freshness, native reasoning, provisional/estimated benchmark rejection, revision/quantization/parameter rejection, request construction.');
