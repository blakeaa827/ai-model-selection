import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {validateWorkloadSnapshot,selectWorkloadConfiguration,pareto,buildWorkloadSelection} from './select-workload.mjs';
// Synthetic scores and prices below are test fixtures, not real model results.
const checked=new Date().toISOString(),asOf=Date.parse(checked);
const p={id:'fixture',status:'ready',evaluation_slug:'fixture-benchmark',benchmark_name:'Synthetic test benchmark',benchmark_version:'test-1',methodology_version:'fixture-1',harness_id:'fixture-harness',score_unit:'percent',score_multiplier:100,cost_metric:'USD_per_fixture-benchmark_task',source_verified_at:checked,methodology_verified_at:checked,score_is_request_success_probability:false,required_parameters:['tools'],cost_basis:'Synthetic fixture only',frontier:[],limited_free_configurations:[],evaluated_configurations:[],recommendations:{floor:null,ceiling:null}};
function row(name,score,cost,context,image=false,free=false) {
  const mid='fixture/'+name;
  return {configuration_id:mid+'@low',model_name:'Synthetic '+name,openrouter_model_id:mid,openrouter_canonical_slug:mid+'-revision1',effort:'low',reasoning_control:{type:'effort',value:'low'},
    request:{model:mid,reasoning:{effort:'low'},provider:{only:['fixture'],require_parameters:true,allow_fallbacks:false}},api_endpoint:'https://openrouter.ai/api/v1/chat/completions',
    benchmark_source_url:'https://example.com/'+name,benchmark_verified_at:checked,openrouter_verified_at:checked,provider_documentation_verified_at:checked,
    endpoint_verification:{verified_at:checked,provider_tag:'fixture',quantization:'unknown',supported_parameters:['reasoning','reasoning_effort','tools']},
    context_window_tokens:context,input_modalities:image?['text','image']:['text'],eligible_for_frontier:true,benchmark_score_is_estimated:false,benchmark_cost_status:'complete_as_published',
    score,source_raw_score:score/100,score_unit:p.score_unit,benchmark_task_cost_usd:cost,benchmark_id:p.evaluation_slug,benchmark_version:p.benchmark_version,harness_id:p.harness_id,...(free?{requires_opt_in:true}:{})};
}
function intervals(rows) {
  return rows.map((r,i)=>({...r,minimum_score_exclusive:rows[i-1]?.score??null,maximum_score_inclusive:r.score,minimum_budget_inclusive:r.benchmark_task_cost_usd,maximum_budget_exclusive:rows[i+1]?.benchmark_task_cost_usd??null}));
}
p.evaluated_configurations=[row('a',20,.01,10000),row('b',30,.03,50000),row('c',25,.04,1000000,true),row('d',40,.1,1000000,true),row('free',10,0,10000,false,true)];
p.frontier=intervals(pareto(p.evaluated_configurations.filter(r=>!r.requires_opt_in)));
p.limited_free_configurations=intervals(p.evaluated_configurations.filter(r=>r.requires_opt_in));
for(const [role,index] of [['floor',0],['ceiling',1]]) {
  const r=p.frontier[index];p.recommendations[role]={configuration_id:r.configuration_id,score:r.score,benchmark_task_cost_usd:r.benchmark_task_cost_usd};
}
const fixture={schema_version:'1.0.0',checked_at:checked,freshness:{recommended_max_age_hours:48,on_stale:'reject_and_request_refresh'},general_intelligence_index_version:'fixture-1',profiles:[p],coding_agent_systems:{openrouter_actionable:false,request:null,systems:[]}};
validateWorkloadSnapshot(fixture,asOf);
function boundaries(d,profile) {
  const candidates=profile.evaluated_configurations.filter(r=>!r.requires_opt_in);
  for(const r of profile.frontier) {
    assert.equal(selectWorkloadConfiguration(d,profile.id,r.score).configuration_id,r.configuration_id);
    assert.equal(selectWorkloadConfiguration(d,profile.id,{max_task_cost_usd:r.benchmark_task_cost_usd}).configuration_id,r.configuration_id);
    if(r.minimum_score_exclusive!==null) {
      const middle=(r.minimum_score_exclusive+r.score)/2;
      const eligible=candidates.filter(x=>x.score>=middle).sort((a,b)=>a.benchmark_task_cost_usd-b.benchmark_task_cost_usd);
      assert.equal(selectWorkloadConfiguration(d,profile.id,middle).benchmark_task_cost_usd,eligible[0].benchmark_task_cost_usd);
      assert.equal(selectWorkloadConfiguration(d,profile.id,r.minimum_score_exclusive).score,r.minimum_score_exclusive);
    }
    if(r.maximum_budget_exclusive!==null)assert.equal(selectWorkloadConfiguration(d,profile.id,{max_task_cost_usd:r.maximum_budget_exclusive}).benchmark_task_cost_usd,r.maximum_budget_exclusive);
  }
  assert.throws(()=>selectWorkloadConfiguration(d,profile.id,profile.frontier.at(-1).score+1),/No eligible/);
  assert.throws(()=>selectWorkloadConfiguration(d,profile.id,'budget:0'),/No eligible/);
  if(profile.limited_free_configurations.length)assert.equal(selectWorkloadConfiguration(d,profile.id,'budget:0',{allow_limited_free:true}).benchmark_task_cost_usd,0);
}
boundaries(fixture,p);
// C is dominated globally; after a context/image constraint it is the cheapest fit.
assert.equal(selectWorkloadConfiguration(fixture,'fixture','score:25',{min_context_tokens:1000000}).request.model,'fixture/c');
assert.equal(selectWorkloadConfiguration(fixture,'fixture','budget:0.04',{input_modalities:['image']}).request.model,'fixture/c');
assert.throws(()=>selectWorkloadConfiguration(fixture,'unknown',20),/Unknown or pending/);
assert.throws(()=>selectWorkloadConfiguration(fixture,'fixture',20,{harness_id:'another-harness'}),/No eligible/);
assert.throws(()=>selectWorkloadConfiguration(fixture,'fixture',20,{benchmark_version:'another-version'}),/No eligible/);
assert.throws(()=>selectWorkloadConfiguration(fixture,'fixture',20,{maximum_latency_seconds:5}),/Unsupported workload constraint/);
assert.throws(()=>selectWorkloadConfiguration(fixture,'fixture','floor',{input_modalities:['image']}),/does not meet/);
assert.throws(()=>selectWorkloadConfiguration(fixture,'fixture','budget:NaN'),/Budget/);
assert.throws(()=>validateWorkloadSnapshot(fixture,asOf+49*3600000),/stale/);
for(const mutate of [
 d=>d.profiles[0].frontier[0].benchmark_version='wrong',
 d=>d.profiles[0].frontier[0].harness_id='wrong',
 d=>d.profiles[0].frontier[0].request.reasoning.effort=null,
 d=>d.profiles[0].frontier[0].request.provider.allow_fallbacks=true,
 d=>d.profiles[0].frontier[0].benchmark_task_cost_usd=.999,
 d=>d.profiles[0].frontier[0].benchmark_score_is_estimated=true,
 d=>d.profiles[0].frontier[0].benchmark_verified_at='2020-01-01T00:00:00Z',
 d=>d.profiles[0].frontier[0].model_name='Synthetic (Default Fallback)',
 d=>d.profiles[0].frontier.pop(),
 d=>d.profiles[0].status='pending_methodology_verification',
 d=>d.coding_agent_systems.request={model:'fixture/fake'}
]) {const d=structuredClone(fixture);mutate(d);assert.throws(()=>validateWorkloadSnapshot(d,asOf));}
if(process.argv[2]) {
  const d=JSON.parse(await readFile(process.argv[2],'utf8'));validateWorkloadSnapshot(d);
  for(const profile of d.profiles)if(profile.status==='ready')boundaries(d,profile);
}
// Live request construction is exercised with HTTP fixtures; no generation call.
const selected=p.evaluated_configurations.find(r=>r.openrouter_model_id==='fixture/b');
const catalog={data:[{id:selected.openrouter_model_id,canonical_slug:selected.openrouter_canonical_slug,reasoning:{supported_efforts:['low']},supported_parameters:['reasoning','tools'],context_length:50000,architecture:{input_modalities:['text']}}]};
const endpoint={data:{endpoints:[{model_id:selected.openrouter_model_id,name:selected.openrouter_canonical_slug,tag:'fixture',status:0,quantization:'unknown',supported_parameters:['reasoning','tools']}]}};
const oldFetch=globalThis.fetch;
globalThis.fetch=async url=>({ok:true,json:async()=>String(url).endsWith('/fixture.json')?fixture:String(url).endsWith('/models')?catalog:endpoint});
try {
  const result=await buildWorkloadSelection('https://example.com/fixture.json','fixture','score:30',{required_parameters:['tools']});
  assert.deepEqual(result.request,selected.request);
  endpoint.data.endpoints[0].status=1;
  await assert.rejects(()=>buildWorkloadSelection('https://example.com/fixture.json','fixture','score:30'),/unavailable/);
  endpoint.data.endpoints[0].status=0;catalog.data[0].canonical_slug+='-changed';
  await assert.rejects(()=>buildWorkloadSelection('https://example.com/fixture.json','fixture','score:30'),/revision changed/);
} finally {globalThis.fetch=oldFetch;}
console.log('PASS: workload score/budget boundaries, free opt-in, constrained dominance, unknown/pending/stale/version/harness/provisional rejection and strict live request construction');
