// Configuration-level AA evidence gate. Release-level bounds are not actionable.
import {readFile,writeFile} from 'node:fs/promises';
const [input,output]=process.argv.slice(2);
if(!input||!output)throw Error('Usage: node pipeline/verify-evidence.mjs raw.json verified.json');
const raw=JSON.parse(await readFile(input,'utf8'));
if(!raw.methodology_version||!raw.checked_at||!Array.isArray(raw.configurations))throw Error('Missing methodology, date or configurations');
const rows=raw.configurations.map(r=>{
 const reasons=[];
 if(r.methodology_version!==raw.methodology_version)reasons.push('index_version_mismatch');
 if(!Number.isFinite(r.intelligence_score)||!Number.isFinite(r.benchmark_task_cost_usd)||r.benchmark_task_cost_usd<0)reasons.push('missing_measured_pair');
 if(r.evidence_kind!=='configuration_level_original_source')reasons.push('release_bounds_not_actionable');
 if(r.score_estimated||r.cost_provisional)reasons.push('provisional');
 if(!r.aa_source_url?.startsWith('https://artificialanalysis.ai/'))reasons.push('source_unverified');
 if(!r.reasoning_control||!r.configuration_id)reasons.push('identity_unverified');
 const date=Date.parse(r.aa_configuration_verified_at);
 if(!Number.isFinite(date)||Date.now()-date>48*3600000||date>Date.now()+300000)reasons.push('stale_benchmark');
 return {...r,benchmark_audit:{status:reasons.length?'rejected':'verified',reasons}};
});
await writeFile(output,JSON.stringify({...raw,configurations:rows},null,2)+'\n');
if(rows.some(x=>x.benchmark_audit.status==='rejected'))process.exitCode=2;
