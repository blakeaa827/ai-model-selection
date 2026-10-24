// Artificial Analysis model catalog screening adapter (Node 20+).
// Requires an API key supplied at runtime through the AA_API_KEY environment variable.
// No secrets are written to the output.
import {mkdir,writeFile} from 'node:fs/promises';
const destination=process.argv[2]||'run-artifacts/aa-catalog.json';
if(!process.env.AA_API_KEY)throw Error('Missing AA_API_KEY environment variable');
const response=await fetch('https://artificialanalysis.ai/api/v2/language/models',{
 headers:{'x-api-key':process.env.AA_API_KEY,accept:'application/json'},
 signal:AbortSignal.timeout(45000)
});
if(!response.ok)throw Error('Artificial Analysis API returned HTTP '+response.status);
const data=await response.json();
if(!Array.isArray(data.data))throw Error('Unexpected response format');
const models=data.data.map(m=>({
 id:m.id??null,name:m.name??null,
 score:m.evaluations?.artificial_analysis_intelligence_index??null,
 benchmark_task_cost_usd:null,
 status:'pending_exact_configuration_and_measured_task_cost'
}));
await mkdir(destination.includes('/')?destination.slice(0,destination.lastIndexOf('/')):'.',{recursive:true});
await writeFile(destination,JSON.stringify({checked_at:new Date().toISOString(),source:'https://artificialanalysis.ai/api/v2/language/models',models,actionable:false},null,2)+'\n');
console.log('Screened '+models.length+' AA models; configuration-level verification remains required.');
