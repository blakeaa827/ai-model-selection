// End-to-end fail-closed coordinator. Node 20+.
// Run: node pipeline/run.mjs verified-aa-configurations.json
// Never refresh published timestamps or overwrite last good report on failure.
import {mkdir,readFile,writeFile} from 'node:fs/promises';
import {spawnSync} from 'node:child_process';
const source=process.argv[2];
if(!source)throw Error('Provide a verified configuration-level AA evidence file');
const dir='run-artifacts';
await mkdir(dir,{recursive:true});
const stages=[];
async function execute(name,args){
 const run=spawnSync(process.execPath,args,{encoding:'utf8',timeout:180000});
 const item={name,exit_code:run.status,signal:run.signal,passed:run.status===0,at:new Date().toISOString(),
  stderr:(run.stderr||'').slice(-3000)};
 stages.push(item);await writeFile(dir+'/run-status.json',JSON.stringify({stages,publish_allowed:false},null,2)+'\n');
 if(!item.passed)throw Error(name+' failed; last published report preserved');
}
try{
 await execute('aa_evidence',['pipeline/verify-evidence.mjs',source,dir+'/evidence.json']);
 await execute('exact_routing',['pipeline/verify-route.mjs',dir+'/evidence.json',dir+'/routed.json']);
 const routed=JSON.parse(await readFile(dir+'/routed.json','utf8'));
 const eligible=routed.configurations.filter(r=>r.benchmark_audit?.status==='verified'&&r.routing_audit?.status==='verified');
 const rejected=routed.configurations.filter(r=>!eligible.includes(r));
 await writeFile(dir+'/routing-coverage.json',JSON.stringify({checked_at:new Date().toISOString(),eligible:eligible.length,rejected:rejected.map(r=>({id:r.configuration_id,benchmark:r.benchmark_audit,routing:r.routing_audit}))},null,2)+'\n');
 if(!eligible.length)throw Error('No eligible benchmark-route pairs');
 await writeFile(dir+'/eligible.json',JSON.stringify({...routed,configurations:eligible},null,2)+'\n');
 await execute('frontier',['pipeline/build-frontier.mjs',dir+'/eligible.json',dir+'/frontier-candidate.json']);
 await execute('assemble',['pipeline/assemble.mjs',dir+'/frontier-candidate.json','latest.json',dir+'/latest-candidate.json']);
 // Candidate only. Atomic publication requires separate complete source and schema checks.
 stages.push({name:'schema_selector_and_atomic_publish',passed:false,status:'not_integrated',at:new Date().toISOString()});
 await writeFile(dir+'/run-status.json',JSON.stringify({stages,publish_allowed:false},null,2)+'\n');
 console.error('Candidate generated, but publication intentionally blocked pending schema/selector and atomic GitHub integration.');
 process.exitCode=2;
}catch(error){
 await writeFile(dir+'/run-status.json',JSON.stringify({stages,publish_allowed:false,error:String(error)},null,2)+'\n');
 console.error(String(error));process.exitCode=2;
}
