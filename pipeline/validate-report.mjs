// Validate actual staged evidence and strict routing; no model generation or invoices.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFile,writeFile} from 'node:fs/promises';
import {validateSnapshot,selectConfiguration,verifyCatalog,verifyEndpoint} from '../select-model.mjs';
import {reportFiles} from './report-files.mjs';
const root=process.argv[2]||'run-artifacts/report';
const read=async p=>JSON.parse(await readFile(p,'utf8'));
const d=await read(root+'/latest.json');
validateSnapshot(d);
const [catalog,eps,metrics,coverage]=await Promise.all(['catalog','endpoints','metrics'].map(p=>read('run-artifacts/acquisition/'+p+'.json')).concat(read(root+'/coverage.json')));
for(const row of [...d.frontier,...d.limited_free_configurations]){
 verifyCatalog(row,catalog,['tools']);verifyEndpoint(row,eps[row.openrouter_model_id],['tools']);
 const a=metrics.find(x=>x.source_url===row.benchmark_source_url);
 assert(a&&!a.error,'Missing exact original source');
 assert.equal(a.version,d.benchmark.version);assert.equal(a.intelligenceIndexIsEstimated,false);assert.equal(a.deprecated,false);
 assert.equal(row.intelligence_score,a.intelligenceIndex);assert.equal(row.benchmark_task_cost_usd,a.intelligenceIndexCostPerTask?.cost?.total);
}
const eligible=d.evaluated_configurations.filter(r=>r.eligible_for_frontier&&r.benchmark_task_cost_usd!==null);
for(const row of d.frontier){
 assert(!eligible.some(x=>x.intelligence_score>=row.intelligence_score&&x.benchmark_task_cost_usd<=row.benchmark_task_cost_usd&&(x.intelligence_score>row.intelligence_score||x.benchmark_task_cost_usd<row.benchmark_task_cost_usd)),'Dominated retained configuration');
 assert.equal(selectConfiguration(d,row.intelligence_score).configuration_id,row.configuration_id);
 assert.equal(selectConfiguration(d,{max_task_cost_usd:row.benchmark_task_cost_usd}).configuration_id,row.configuration_id);
 if(row.minimum_score_exclusive!==null)assert.equal(selectConfiguration(d,row.minimum_score_exclusive).intelligence_score,row.minimum_score_exclusive);
 if(row.maximum_budget_exclusive!==null)assert.equal(selectConfiguration(d,{max_task_cost_usd:row.maximum_budget_exclusive}).benchmark_task_cost_usd,row.maximum_budget_exclusive);
}
assert.deepEqual(new Set(coverage.catalog_models.map(x=>x.model_id)),new Set(catalog.data.map(x=>x.id)));
assert.equal(coverage.catalog_models.length,d.coverage_inventory.openrouter_model_count);
assert.equal(coverage.AA_release_screening.length,d.coverage_inventory.AA_release_count);
assert.deepEqual(d,await read(root+'/snapshots/'+d.report_date+'.json'));
assert.throws(()=>validateSnapshot(d,Date.parse(d.checked_at)+49*3600000),/stale/);
assert.throws(()=>selectConfiguration(d,{max_task_cost_usd:0}),/No eligible/);
for(const free of d.limited_free_configurations)assert.equal(selectConfiguration(d,{max_task_cost_usd:0},{allow_limited_free:true}).benchmark_task_cost_usd,0);
const bad=structuredClone(d);bad.frontier[0].request.reasoning={effort:null};assert.throws(()=>validateSnapshot(bad));
const unchecked=structuredClone(d);unchecked.frontier[0].eligible_for_frontier=false;assert.throws(()=>validateSnapshot(unchecked),/eligibility/);
const fileHashes={};
for(const path of reportFiles(d))fileHashes[path]=createHash('sha256').update(await readFile(root+'/'+path)).digest('hex');
await writeFile('run-artifacts/validation.json',JSON.stringify({file_hashes_sha256:fileHashes,status:'passed',checked_at:new Date().toISOString(),actionable_configurations:d.frontier.length+d.limited_free_configurations.length,catalog_entries:catalog.data.length,AA_releases:coverage.AA_release_screening.length,no_generation_calls:true},null,2)+'\n');
console.log('PASS: exact current-source pairs, live catalog/endpoints, Pareto dominance, score/budget boundaries, free opt-in, stale/ineligible rejection, full inventory and matching snapshot');
