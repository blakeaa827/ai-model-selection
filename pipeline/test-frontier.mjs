// Regression tests for pipeline/build-frontier.mjs. No network or paid calls.
import {mkdtemp,writeFile,readFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
const dir=await mkdtemp(join(tmpdir(),'frontier-test-'));
const stamp=new Date().toISOString();
const mk=(id,score,cost)=>({
 configuration_id:id,methodology_version:'4.3.2',intelligence_score:score,benchmark_task_cost_usd:cost,
 aa_source_url:'https://artificialanalysis.ai/models',aa_configuration_verified_at:stamp,
 openrouter_model_id:'test/'+id,canonical_revision:'test/'+id+'-revision',
 openrouter_verified_at:stamp,endpoint_verification:{verified_at:stamp},
 request:{model:'test/'+id,reasoning:{effort:'high'},provider:{only:['test'],require_parameters:true,allow_fallbacks:false}}
});
try {
 const input=join(dir,'input.json'),output=join(dir,'output.json');
 await writeFile(input,JSON.stringify({methodology_version:'4.3.2',checked_at:stamp,configurations:[
 mk('a',10,.01),mk('dominated',9,.02),mk('b',20,.04),mk('c',30,.10),
 {...mk('unverified',40,.001),openrouter_verified_at:null}
 ]}));
 const result=spawnSync(process.execPath,['pipeline/build-frontier.mjs',input,output],{encoding:'utf8'});
 assert.equal(result.status,0,result.stderr);
 const data=JSON.parse(await readFile(output,'utf8'));
 assert.deepEqual(data.frontier.map(x=>x.configuration_id),['a','b','c']);
 assert.equal(data.frontier[0].minimum_score_exclusive,null);
 assert.equal(data.frontier[1].minimum_score_exclusive,10);
 assert.equal(data.frontier[0].maximum_budget_exclusive,.04);
 assert.ok(Math.abs(data.frontier[1].marginal_from_previous.percentage_cost_increase-300)<1e-8);
 assert.ok(data.rejected.some(x=>x.id==='unverified'));
 await writeFile(input,JSON.stringify({methodology_version:'4.3.2',checked_at:stamp,configurations:[{...mk('stale',10,.01),openrouter_verified_at:'2026-01-01T00:00:00Z'}]}));
 const failure=spawnSync(process.execPath,['pipeline/build-frontier.mjs',input,output],{encoding:'utf8'});
 assert.equal(failure.status,2,'stale evidence must not produce a valid frontier');
 console.log('PASS: dominance, score/budget intervals, marginal costs, stale route rejection');
} finally {await rm(dir,{recursive:true,force:true});}
