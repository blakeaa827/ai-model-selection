// Verify exact OpenRouter catalog identity and provider endpoint, no paid generation.
import {readFile,writeFile} from 'node:fs/promises';
const [evidencePath,outPath]=process.argv.slice(2);
if(!evidencePath||!outPath)throw Error('Usage: node pipeline/verify-route.mjs evidence.json verified.json');
const evidence=JSON.parse(await readFile(evidencePath,'utf8'));
const now=new Date().toISOString();
async function get(url){const r=await fetch(url,{signal:AbortSignal.timeout(30000)});if(!r.ok)throw Error('HTTP '+r.status+' '+url);return r.json();}
const catalog=await get('https://openrouter.ai/api/v1/models');
if(!Array.isArray(catalog.data))throw Error('Unexpected catalog');
const byId=new Map(catalog.data.map(m=>[m.id,m]));
const output=[];
for(const item of evidence.configurations){
 const row={...item};const issues=[];const model=byId.get(item.openrouter_model_id);
 if(!model)issues.push('model_absent');
 else {
  if(model.canonical_slug!==item.canonical_revision)issues.push('revision_mismatch');
  if(model.expiration_date&&model.expiration_date<=Math.floor(Date.now()/1000))issues.push('expired');
  const control=item.request?.reasoning;
  if(!control||typeof control!=='object')issues.push('missing_reasoning');
  else if('effort'in control){
   if(!model.reasoning?.supported_efforts?.includes(control.effort))issues.push('effort_unsupported');
   if(!model.supported_parameters?.includes('reasoning')&&!model.supported_parameters?.includes('reasoning_effort'))issues.push('reasoning_parameter_unsupported');
  } else if('enabled'in control){
   if(typeof control.enabled!=='boolean'||!model.supported_parameters?.includes('reasoning'))issues.push('enabled_unsupported');
  }else issues.push('unknown_reasoning_control');
  if(item.request?.provider?.require_parameters!==true||item.request?.provider?.allow_fallbacks!==false||item.request?.provider?.only?.length!==1)issues.push('unsafe_routing');
  if(!issues.length){
   try{
    const url='https://openrouter.ai/api/v1/models/'+encodeURIComponent(model.canonical_slug)+'/endpoints';
    const endpoints=await get(url);
    const candidates=Array.isArray(endpoints.data?.endpoints)?endpoints.data.endpoints:[];
    const requested=item.request.provider.only[0];
    const match=candidates.find(x=>x.tag===requested);
    if(!match)issues.push('provider_endpoint_not_matched');
    else {
     const supported=match.supported_parameters;
     if(!Array.isArray(supported))issues.push('endpoint_parameters_unverified');
     else if(!supported.includes('reasoning')&&!supported.includes('reasoning_effort'))issues.push('endpoint_reasoning_unverified');
     if(item.quantization&&match.quantization!==item.quantization)issues.push('quantization_mismatch');
     if(!issues.length)row.endpoint_verification={verified_at:now,provider_tag:requested,quantization:match.quantization??null};
    }
   }catch(error){issues.push('endpoint_fetch_failed:'+String(error));}
  }
 }
 row.routing_audit={status:issues.length?'rejected':'verified',reasons:issues};
 if(!issues.length){row.openrouter_verified_at=now;row.canonical_revision=model.canonical_slug;}
 output.push(row);
}
await writeFile(outPath,JSON.stringify({...evidence,configurations:output,route_audit_at:now},null,2)+'\n');
if(!output.some(x=>x.routing_audit.status==='verified'&&x.benchmark_audit?.status==='verified')){console.error('No fully verified benchmark-route pairs');process.exitCode=2;}
