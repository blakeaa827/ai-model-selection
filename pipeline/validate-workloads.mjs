import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {validateWorkloadSnapshot,selectWorkloadConfiguration} from '../select-workload.mjs';
import {verifyCatalog,verifyEndpoint} from '../select-model.mjs';
const root=process.argv[2]||'run-artifacts/report';
const read=async path=>JSON.parse(await readFile(path,'utf8'));
const [d,a,g,catalog,eps,baseMetrics]=await Promise.all([read(root+'/workloads.json'),read('run-artifacts/acquisition/workloads.json'),read(root+'/latest.json'),read('run-artifacts/acquisition/catalog.json'),read('run-artifacts/acquisition/endpoints.json'),read('run-artifacts/acquisition/metrics.json')]);
validateWorkloadSnapshot(d);
const records=new Map([...a.active_exact_records,...baseMetrics].filter(r=>!r.error).map(r=>[r.source_url,r]));
let rows=0;
for(const p of d.profiles) {
  for(const r of p.evaluated_configurations) {
    const source=records.get(r.benchmark_source_url);
    assert(source&&!source.error,'Missing exact workload source');
    assert.equal(source.version,d.general_intelligence_index_version);
    assert.equal(source.intelligenceIndexIsEstimated,false);assert.equal(source.deprecated,false);
    assert(!/fallback/i.test(source.name),'Fallback system used as a single model');
    const ev=source.intelligenceIndexEvaluations.find(e=>e.slug===p.evaluation_slug);
    assert(ev&&Number.isFinite(ev.costPerTask),'Missing workload-specific measured cost');
    assert.equal(r.source_raw_score,ev.score);assert.equal(r.score,ev.score*p.score_multiplier);
    assert.equal(r.benchmark_task_cost_usd,ev.costPerTask,'General weighted cost or token prices substituted for workload task cost');
    if(r.effort!==null)assert((source.effort?.slug===r.effort)||(r.effort==='none'&&source.isReasoning===false),'Incorrect source effort');
    verifyCatalog(r,catalog,p.required_parameters);verifyEndpoint(r,eps[r.openrouter_model_id],p.required_parameters);
    rows++;
  }
  if(p.status==='ready') {
    for(const r of p.frontier) {
      assert.equal(selectWorkloadConfiguration(d,p.id,r.score).configuration_id,r.configuration_id);
      assert.equal(selectWorkloadConfiguration(d,p.id,{max_task_cost_usd:r.benchmark_task_cost_usd}).configuration_id,r.configuration_id);
    }
  }
}
assert.deepEqual(d,await read(root+'/workloads/snapshots/'+d.report_date+'.json'));
assert.equal(g.workload_selection.checked_at,d.checked_at);
assert.equal(g.report_date,d.report_date);
assert.equal(d.coverage.openrouter_model_count,catalog.data.length);
assert.equal(d.coverage.AA_configuration_count,a.configuration_index.length);
const sourceSystems=new Map(a.coding_agents.variants.map(r=>[r.id,r]));
for(const r of d.coding_agent_systems.systems) {
  const source=sourceSystems.get(r.configuration_id.split(':')[1]);assert(source);
  assert.equal(r.score,source.indexScore===null?null:source.indexScore*100);
  assert.equal(r.benchmark_task_cost_usd,source.mean.costUsd);
  assert.equal(r.request,null);assert.equal(r.openrouter_actionable,false);assert.equal(r.subscription_task_cost_usd,null);
}
assert.throws(()=>validateWorkloadSnapshot(d,Date.parse(d.checked_at)+49*3600000),/stale/);
console.log(`PASS: ${d.profiles.length} workload profiles, ${rows} exact evaluation score/cost pairs, live strict routing, complete candidate reconsideration, separate agent systems and matching snapshot`);
