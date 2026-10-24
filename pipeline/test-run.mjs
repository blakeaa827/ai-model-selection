// Offline regression for the coordinated pipeline. Requires no API keys or network.
// Tests the fail-closed contract: incomplete evidence cannot publish.
import {mkdtemp,writeFile,readFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
const dir=await mkdtemp(join(tmpdir(),'model-pipeline-'));
try{
 const path=join(dir,'invalid-evidence.json');
 await writeFile(path,JSON.stringify({methodology_version:'4.3.2',checked_at:new Date().toISOString(),
 configurations:[{configuration_id:'example',intelligence_score:50,benchmark_task_cost_usd:.2,
 evidence_kind:'release_screening_bounds'}]}));
 const result=spawnSync(process.execPath,['pipeline/run.mjs',path],{encoding:'utf8',timeout:20000});
 assert.equal(result.status,2,'unverified release bounds must fail');
 const status=JSON.parse(await readFile('run-artifacts/run-status.json','utf8'));
 assert.equal(status.publish_allowed,false);
 assert.equal(status.stages[0].name,'aa_evidence');
 assert.equal(status.stages[0].passed,false);
 console.log('PASS: invalid benchmark evidence fails closed without publication');
}finally{await rm(dir,{recursive:true,force:true});}
