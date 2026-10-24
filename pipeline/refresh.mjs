// Scheduled end-to-end refresh; acquisition failures preserve last published files.
import {mkdir,writeFile} from 'node:fs/promises';
import {spawnSync} from 'node:child_process';
import {baseline,head,publish} from './publish.mjs';
const shouldPublish=process.argv.includes('--publish');
const reuse=process.argv.includes('--reuse-acquisition');
await mkdir('run-artifacts',{recursive:true});
const stages=[];
async function run(name,program,args){
 const result=spawnSync(program,args,{stdio:'inherit',timeout:12*60*1000,env:process.env});
 const stage={name,passed:result.status===0,exit_code:result.status,signal:result.signal,checked_at:new Date().toISOString()};
 stages.push(stage);await writeFile('run-artifacts/refresh-status.json',JSON.stringify({stages,publish_allowed:false},null,2)+'\n');
 if(!stage.passed)throw Error(name+' failed; last published report preserved');
}
try{
 for(let attempt=0;attempt<3;attempt++){
  let parent=process.env.REPORT_PARENT_SHA;
  if(shouldPublish){const current=await head();parent=current.sha;await baseline(parent);process.env.REPORT_PARENT_SHA=parent;}
  if(!reuse||attempt)await run('public_original_source_acquisition','python3',['pipeline/acquire.py']);
  await run('assemble_verified_report','python3',['pipeline/build-report.py']);
  await run('render_tables_and_curve','python3',['pipeline/render-report.py']);
  await run('validate_exact_source_and_routing',process.execPath,['pipeline/validate-report.mjs']);
  await run('schema_validation','python3',['pipeline/validate-schema.py']);
  await run('selector_regression',process.execPath,['test-selector.mjs']);
  if(!shouldPublish){console.log('Fresh staged report validated; publication not requested');break;}
  try{await publish('run-artifacts/report',parent);break;}
  catch(error){if(String(error).includes('CONCURRENT_MAIN_CHANGED')&&attempt<2){console.log('Main changed; rebuilding against fresh main and preserving unrelated history');continue;}throw error;}
 }
 await writeFile('run-artifacts/refresh-status.json',JSON.stringify({stages,status:shouldPublish?'published_and_verified':'validated_candidate',publish_allowed:true},null,2)+'\n');
}catch(error){
 await writeFile('run-artifacts/refresh-status.json',JSON.stringify({stages,status:'failed_preserving_last_published_report',publish_allowed:false,error:String(error)},null,2)+'\n');
 console.error(String(error));process.exitCode=1;
}
