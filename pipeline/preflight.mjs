// Checkpointed acquisition preflight. Does not publish or modify existing reports.
// Run: node pipeline/preflight.mjs
import {mkdir,writeFile} from 'node:fs/promises';
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
stages.push({name:'aa_configuration_evidence',status:'blocked',reason:'No verified configuration-level AA source adapter installed'});
stages.push({name:'openrouter_exact_routing',status:'blocked',reason:'No exact revision/endpoint/effort verification adapter installed'});
await writeFile(directory+'/preflight.json',JSON.stringify({stages,publication_allowed:false},null,2)+'\n');
if(stages.some(x=>x.status!=='passed')){console.error('Preflight incomplete: report publication blocked.');process.exitCode=2;}
