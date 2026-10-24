// Turn a fully verified frontier into a schema 1.1.0 candidate without altering publication.
// Reuses the existing report's non-routing metadata only; all routing rows must be newly verified.
// node pipeline/assemble.mjs run-artifacts/frontier-candidate.json latest.json run-artifacts/latest-candidate.json
import {readFile,writeFile} from 'node:fs/promises';
import {validateSnapshot} from '../select-model.mjs';
const [frontierPath,previousPath,outputPath]=process.argv.slice(2);
if(!frontierPath||!previousPath||!outputPath)throw Error('Usage: node pipeline/assemble.mjs frontier.json previous.json output.json');
const calculated=JSON.parse(await readFile(frontierPath,'utf8'));
const previous=JSON.parse(await readFile(previousPath,'utf8'));
if(!calculated.frontier?.length)throw Error('No verified frontier');
const checked=Date.parse(calculated.checked_at);
if(!Number.isFinite(checked)||Date.now()-checked>48*3600000)throw Error('Candidate stale');
const frontier=calculated.frontier.map(r=>{
 if(!r.routing_audit||r.routing_audit.status!=='verified'||r.benchmark_audit?.status!=='verified')throw Error('Missing verification');
 if(!r.openrouter_canonical_slug||!r.endpoint_verification?.verified_at)throw Error('Missing canonical route metadata');
 return r;
});
const pick=(target)=>frontier.find(r=>r.configuration_id===target);
const floor=pick(process.env.FLOOR_CONFIGURATION_ID);
const ceiling=pick(process.env.CEILING_CONFIGURATION_ID);
if(!floor||!ceiling)throw Error('Explicit verified FLOOR_CONFIGURATION_ID and CEILING_CONFIGURATION_ID required; no invented recommendation');
const report={...previous,report_date:calculated.checked_at.slice(0,10),checked_at:calculated.checked_at,
 benchmark:{...previous.benchmark,version:calculated.methodology_version,verified_at:calculated.checked_at},
 recommendations:{floor:{...floor,rationale:'Selected from verified frontier; workload-dependent recommendation'},ceiling:{...ceiling,rationale:'Optional escalation; workload-dependent recommendation'}},
 frontier,models:frontier.map(r=>r.configuration_id),
 sources:[...new Set(frontier.flatMap(r=>[r.aa_source_url,r.openrouter_source_url].filter(Boolean)))]};
validateSnapshot(report);
await writeFile(outputPath,JSON.stringify(report,null,2)+'\n');
console.log('Validated candidate; publication remains separate');
