// Checkpointed acquisition preflight. Does not publish or modify existing reports.
// Run: node pipeline/preflight.mjs
import {mkdir,writeFile,access} from 'node:fs/promises';
const directory='run-artifacts';
await mkdir(directory,{recursive:true});
const stages=[];
async function check(name,url,validate){
 try {
  const response=await fetch(url,{signal:AbortSignal.timeout(45000)});
  if(!response.ok)throw Error('HTTP '+response.status);
  const body=await response.text();
  const value=validate(body);
  stages.push({name,status:'passed',checked_at:new Date().toISOString(),...value});
 }catch(error){stages.push({name,status:'failed',error:String(error),checked_at:new Date().toISOString()});}
 await writeFile(directory+'/preflight.json',JSON.stringify({stages,publication_allowed:false},null,2)+'\n');
}
await check('openrouter_catalog','https://openrouter.ai/api/v1/models',body=>{
 const data=JSON.parse(body);if(!Array.isArray(data.data)||!data.data.length)throw Error('Empty catalog');
 return {entries:data.data.length};
});
await check('aa_release_registry','https://artificialanalysis.ai/models/releases',body=>{
 if(!body.includes('Artificial Analysis'))throw Error('Unexpected registry response');
 return {note:'Registry reachable; exact configuration score and task cost still require separate verification'};
});
try { await access('pipeline/acquire.py');await access('pipeline/validate-report.mjs');stages.push({name:'public_source_and_exact_routing_adapters',status:'passed',note:'Use node pipeline/refresh.mjs for acquisition, validation and publication'}); } catch(error) {stages.push({name:'public_source_and_exact_routing_adapters',status:'failed',error:String(error)});}
await writeFile(directory+'/preflight.json',JSON.stringify({stages,publication_allowed:false},null,2)+'\n');
if(stages.some(x=>x.status!=='passed')){console.error('Preflight incomplete: report publication blocked.');process.exitCode=2;}
