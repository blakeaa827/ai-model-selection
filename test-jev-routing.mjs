import assert from 'node:assert/strict';
import {readFile,mkdtemp,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {CONTROL,verifyDecisionRoute,prepareRouting,readWorkloadAnswer,resolveRouting} from './skills/route-workloads-with-jev/scripts/route.mjs';
import {selectWorkloadConfiguration} from './select-workload.mjs';

const source=resolve(process.argv[2]??'workloads.json');
const data=JSON.parse(await readFile(source,'utf8'));
const now=Date.parse(data.checked_at)+1000;
const catalog={data:[{id:CONTROL.model,canonical_slug:CONTROL.canonical_slug,architecture:{output_modalities:['decisions']},pricing:{prompt:'0.000000042',completion:'0'}}]};
const endpoints={data:{id:CONTROL.model,endpoints:[{tag:'typesafe',provider_name:'TypeSafe',model_id:CONTROL.model,status:0,name:`TypeSafe | ${CONTROL.canonical_slug}`,quantization:'unknown'}]}};
let gets=0;
const fetcher=async(url,options)=>{
  assert.equal(options.method,undefined,'tests may not submit paid requests');gets++;
  assert.ok([CONTROL.catalog_url,CONTROL.endpoints_url].includes(url));
  return {ok:true,json:async()=>structuredClone(url===CONTROL.catalog_url?catalog:endpoints)};
};
const options={fetcher,now};
const task={task:'Reconcile CRM records using the approved business workflow.',acceptance_criteria:['Preserve IDs','Validate updates'],target:'score:60',constraints:{required_parameters:['tools']}};
const bundle=await prepareRouting('.',source,task,options);
assert.equal(bundle.request.model,CONTROL.model);
assert.equal(bundle.request.reasoning,undefined);
assert.deepEqual(bundle.request.provider,{only:['typesafe'],require_parameters:true,allow_fallbacks:false});
assert.deepEqual(Object.keys(bundle.request.questions.workload.criteria).sort(),[...data.profiles.filter(p=>p.status==='ready').map(p=>p.id),'unsupported','mixed','clarification_needed'].sort());
assert.equal(bundle.control.paid_call_tested,false);
assert.equal(bundle.control.managed_quantization,'unknown');
const responseFor=(choice,p=0.9)=>{
  const keys=Object.keys(bundle.request.questions.workload.criteria);
  return {model:CONTROL.canonical_slug,provider:'TypeSafe',answers:{workload:{type:'choice',choice,confidence:0.99,
    probabilities:Object.fromEntries(keys.map(k=>[k,k===choice?p:(1-p)/(keys.length-1)]))}}};
};
const response=responseFor('business_automation');
const policy={minimum_choice_probability:0.8,minimum_probability_margin:0.2};
assert.equal(readWorkloadAnswer(response,bundle,policy).worker_success_probability,null);
assert.equal(readWorkloadAnswer(response,bundle,policy).calibration_status,'not_calibrated');
assert.equal(readWorkloadAnswer(response,bundle,policy).input_provenance,'provided_response_not_attested');
assert.equal(readWorkloadAnswer({...response,test_fixture:true},bundle,policy).input_provenance,'simulated_fixture');
assert.throws(()=>readWorkloadAnswer(response,bundle,{}),/explicit classification/);
assert.throws(()=>readWorkloadAnswer(responseFor('business_automation',0.55),bundle,policy),/does not meet/,'confidence must not override a low selected probability');
for(const choice of ['unsupported','mixed','clarification_needed'])assert.throws(()=>readWorkloadAnswer(responseFor(choice),bundle,policy),/needs decomposition/);
for(const change of [r=>{r.model='typesafe/jev-latest';},r=>{r.provider='Other';},r=>{r.answers.workload.probabilities.business_automation=1.1;},r=>{r.answers.workload.probabilities.invented_model=0;},r=>{r.answers.workload.type='score';}]) {
  const broken=structuredClone(response);change(broken);assert.throws(()=>readWorkloadAnswer(broken,bundle,policy));
}
const tie=structuredClone(response);
Object.keys(tie.answers.workload.probabilities).forEach(k=>{tie.answers.workload.probabilities[k]=0;});
tie.answers.workload.probabilities.business_automation=0.5;tie.answers.workload.probabilities.professional_work=0.5;
assert.throws(()=>readWorkloadAnswer(tie,bundle,{minimum_choice_probability:0.1,minimum_probability_margin:0}),/does not meet/);
for(const mutate of [c=>{c.data[0].canonical_slug='changed';},c=>{c.data[0].architecture.output_modalities=['text'];},c=>{c.data[0].expiration_date='2020-01-01';}]) {
  const broken=structuredClone(catalog);mutate(broken);assert.throws(()=>verifyDecisionRoute(broken,endpoints,now));
}
const unavailable=structuredClone(endpoints);unavailable.data.endpoints[0].status=1;
assert.throws(()=>verifyDecisionRoute(catalog,unavailable,now),/unavailable/);
await assert.rejects(prepareRouting('.',source,{...task,target:'probability:0.9'},options),/explicit benchmark/);
await assert.rejects(prepareRouting('.',source,{...task,constraints:{region:'EU'}},options),/Unsupported constraint/);
await assert.rejects(prepareRouting('.',source,task,{...options,now:now+49*3600000}),/stale/);
let selected=0;
const buildSelection=async(givenSource,workload,target,constraints)=>{
  selected++;assert.equal(givenSource,source);assert.equal(workload,'business_automation');assert.equal(target,task.target);assert.deepEqual(constraints,task.constraints);
  const row=selectWorkloadConfiguration(data,workload,target,constraints);
  return {checked_at:data.checked_at,configuration_id:row.configuration_id,request:row.request,score:row.score,benchmark_task_cost_usd:row.benchmark_task_cost_usd,api_endpoint:row.api_endpoint};
};
const result=await resolveRouting('.',source,bundle,response,policy,{...options,buildSelection});
assert.equal(selected,1);assert.equal(result.executed,false);
assert.deepEqual(result.selection.request,selectWorkloadConfiguration(data,'business_automation','score:60',task.constraints).request);
const changed=structuredClone(bundle);changed.request.provider.allow_fallbacks=true;
await assert.rejects(resolveRouting('.',source,changed,response,policy,{...options,buildSelection}),/request identity/);
const directory=await mkdtemp(join(tmpdir(),'jev-routing-test-'));
try {
  const newSource=join(directory,'workloads.json');
  await writeFile(newSource,JSON.stringify({...data,report_date:'different-report'}));
  await assert.rejects(resolveRouting('.',newSource,bundle,response,policy,{...options,buildSelection}),/Report changed/);
} finally {await rm(directory,{recursive:true,force:true});}
assert.equal(selected,1,'invalid resolutions must not reach worker selection');
await assert.rejects(resolveRouting('.',source,bundle,response,policy,{...options,buildSelection:async()=>({...result.selection,request:{model:'invented-worker'}})}),/differs from the bound report/);
assert.ok(gets>=4);
console.log('Jev routing checks passed: decision modality/revision/provider, task policy, probability/margin, uncertainty, report binding, freshness and exact selector handoff; no paid calls.');
