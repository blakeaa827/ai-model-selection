// Artificial Analysis official Free API: headline score AND measured weighted cost/task.
// A valid AA_API_KEY is required. Never substitute gateway token pricing.
import {mkdir,writeFile} from 'node:fs/promises';
const destination=process.argv[2]||'run-artifacts/aa-catalog.json';
if(!process.env.AA_API_KEY)throw Error('Missing AA_API_KEY');
const url='https://artificialanalysis.ai/api/v2/language/models/free';
let page=1,models=[],version=null;
for(;;){
 const response=await fetch(url+'?page='+page,{headers:{'x-api-key':process.env.AA_API_KEY,accept:'application/json'},signal:AbortSignal.timeout(45000)});
 if(!response.ok)throw Error('AA API HTTP '+response.status);
 const body=await response.json();
 if(!Array.isArray(body.data))throw Error('Unexpected AA response');
 if(version!==null&&version!==body.intelligence_index_version)throw Error('Inconsistent index version');
 version=body.intelligence_index_version;
 models.push(...body.data.map(m=>({
  id:m.id??m.slug??null,name:m.name??null,release_date:m.release_date??null,
  intelligence_score:m.evaluations?.artificial_analysis_intelligence_index??null,
  benchmark_task_cost_usd:m.artificial_analysis_intelligence_index_cost?.cost_per_task?.total_cost??null,
  model_creator:m.model_creator??null,
  status:'screening_only_requires_exact_reasoning_revision_and_patch_version_verification',
  raw:m
 })));
 const p=body.pagination;
 if(!p||!p.has_more)break;
 if(page>=100)throw Error('Pagination safety limit');
 page++;
}
await mkdir(destination.includes('/')?destination.slice(0,destination.lastIndexOf('/')):'.',{recursive:true});
await writeFile(destination,JSON.stringify({checked_at:new Date().toISOString(),source:url,index_version_major_minor:version,patch_version_verified:false,entries:models,actionable:false},null,2)+'\n');
console.log('AA records:',models.length,'with cost:',models.filter(x=>Number.isFinite(x.benchmark_task_cost_usd)).length);
