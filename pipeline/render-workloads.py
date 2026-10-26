"""Readable workload lookup tables and exact-data SVG panels."""
import html,json,math,re
from pathlib import Path
P=Path('run-artifacts/report');d=json.loads((P/'workloads.json').read_text())
control=lambda r:json.dumps(r['request']['reasoning'],separators=(',',':'))
name=lambda r:r['request']['model']+' / '+control(r)
money=lambda value:f'${value:.6f}'
lines=[f"# Workload-specific model selection — {d['report_date']}",'',
 'Benchmark source: [Artificial Analysis](https://artificialanalysis.ai/). Original project code and documentation: [MIT](LICENSE). See [DATA-SOURCES.md](DATA-SOURCES.md) for attribution and the deferred data-rights review.','',
 'Each profile has its own benchmark score, measured evaluation task cost, harness and Pareto frontier. Scores and budgets are meaningful only within that profile. The general Intelligence Index remains in [latest.md](latest.md).',
 '',f"Screened **{d['coverage']['AA_configuration_count']} public AA configurations** and **{d['coverage']['openrouter_model_count']} OpenRouter entries**; acquired **{d['coverage']['active_exact_records_checked']} active exact records**. Exact routing correspondence is incomplete. These are the best observed verified pairs, not proof of global optimality. All eligible configurations are reconsidered per workload, including those dominated in the general chart.",'',
 '**Floor and ceiling are candidate value knees, not validated deployment defaults.** A cheap model scoring poorly can have an early cost knee. Supply a workload quality target or use a score/budget query; no application success threshold or calibrated Jev predictor has been supplied. Close score gaps may reflect evaluation noise. Dollars per score point are descriptive, and Elo/benchmark intervals need not have equal practical value.',
 '',f"Source checks completed at {d['checked_at']}. Routing evidence expires after {d['freshness']['recommended_max_age_hours']} hours. Missing or mismatched configurations fail without a substitute.",'',
 '![Workload cost versus capability curves](workloads/cost-curves.svg)','','## Candidate floor and ceiling by workload','','| Workload | Benchmark and score unit | Candidate floor | Optional ceiling |','|---|---|---|---|']
for p in d['profiles']:
 def pick(role):
  rec=p['recommendations'][role]
  if not rec:return 'No clear knee; supply a score or budget'
  r=next(x for x in p['frontier'] if x['configuration_id']==rec['configuration_id'])
  return f"`{name(r)}`; {r['score']:.3f}; {money(r['benchmark_task_cost_usd'])}/task"
 lines.append(f"| [{p['name']}](#{p['id'].replace('_','-')}) | {p['benchmark_name']} {p['benchmark_version']}; {p['score_unit']} | {pick('floor')} | {pick('ceiling')} |")
for p in d['profiles']:
 lines+=['',f"## {p['id'].replace('_','-')}",'',f"**{p['name']}** — [{p['benchmark_name']}]({p['source_url']}), version `{p['benchmark_version']}`; score unit `{p['score_unit']}`; status `{p['status']}`.",'',f"Harness `{p['harness_id']}`: {p['harness']}.",'',p['limits'],'',p['cost_basis'],'',f"Verified candidates: {p['coverage']['eligible_configurations']}; paid frontier: {len(p['frontier'])}. Incomplete routing matches are retained as pending in workloads.json.",'','### Minimum cost for a minimum benchmark score','','| Minimum-score interval | request.model | request.reasoning | Score | USD / this benchmark task |','|---|---|---|---:|---:|']
 for r in p['frontier']:
  lo=r['minimum_score_exclusive'];ran=f"(−∞, {r['score']}]" if lo is None else f"({lo}, {r['score']}]"
  lines.append(f"| {ran} | `{r['request']['model']}` | `{control(r)}` | {r['score']:.3f} | {money(r['benchmark_task_cost_usd'])} |")
 lines+=['','The first lower bound is unbounded for lookup only; it does not give score zero a practical meaning. No verified configuration satisfies a score above the last row.','','### Maximum score within a benchmark-task budget','','| Budget interval, USD | request.model | request.reasoning | Score |','|---|---|---|---:|']
 for r in p['frontier']:
  high=r['maximum_budget_exclusive'];ran=f"[{r['minimum_budget_inclusive']}, {high})" if high is not None else f"[{r['minimum_budget_inclusive']}, ∞)"
  lines.append(f"| {ran} | `{r['request']['model']}` | `{control(r)}` | {r['score']:.3f} |")
 lines+=['','### Marginal upgrades','','| Upgrade to | Score gain | Added USD/task | Cost increase | USD / added score point | Marginal rate multiple |','|---|---:|---:|---:|---:|---:|']
 for r in p['frontier'][1:]:
  m=r['marginal'];multiple=m['versus_previous_marginal_multiple']
  lines.append(f"| `{name(r)}` | {m['score_gain']:.6f} | {money(m['additional_cost_usd'])} | {m['cost_increase_percent']:.2f}% | {money(m['additional_usd_per_score_point'])} | {f'{multiple:.2f}×' if multiple is not None else '—'} |")
 for role in ['floor','ceiling']:
  rec=p['recommendations'][role]
  if rec:lines+=['',f"**Candidate {role}:** {rec['rationale']}"]
 if p['limited_free_configurations']:
  lines+=['','### Explicit-opt-in free lane','']
  for r in p['limited_free_configurations']:lines.append(f"- `{name(r)}`: {r['score']:.3f} `{p['score_unit']}`, {money(r['benchmark_task_cost_usd'])}/task, first-party `{r['request']['provider']['only'][0]}`. Rate limits and quota apply; use `--allow-limited-free` explicitly.")
 lines+=['','Pending reasons: '+', '.join(f"{k}: {v}" for k,v in p['coverage']['pending_status_counts'].items())+'.']
lines+=['','## Exact API routing','','Every actionable row pins one standard provider, uses `require_parameters:true` and `allow_fallbacks:false`, and carries exact canonical revision, reasoning control, source timestamps and endpoint parameters. Missing revisions, controls or freshness are rejected. Provider token prices are separate from the task-cost measurements. No automatic/latest aliases or fallback-system scores are used.','','| Callable model | Canonical revision | provider.only | API surface |','|---|---|---|---|']
seen=set()
for p in d['profiles']:
 for r in p['frontier']+p['limited_free_configurations']:
  if r['openrouter_model_id'] in seen:continue
  seen.add(r['openrouter_model_id']);lines.append(f"| `{r['request']['model']}` | `{r['openrouter_canonical_slug']}` | `{r['request']['provider']['only'][0]}` | `{r['api_endpoint']}` |")
lines+=['','## Complete coding-agent systems','','These are separate model-plus-agent evaluations from the AA Coding Agent Index. They are useful evidence when building with a coding service, conditional on exact client version, settings and account access. API task costs below are for the tested system; subscription cost per prompt remains null. They do not authorize a standalone OpenRouter request. Fallback counts and tested harness versions are retained in workloads.json.','','| Tested agent/system | Coding Agent Index score | API USD / agent task | Fallback attempts |','|---|---:|---:|---:|']
for r in d['coding_agent_systems']['frontier']:lines.append(f"| {r['label'].replace('|','/')} | {r['score']:.3f} | {money(r['benchmark_task_cost_usd'])} | {r['fallback_attempts']} |")
lines+=['',f"Coding Agent Index version `{d['coding_agent_systems']['version']}`; [original results]({d['coding_agent_systems']['source_url']}) and [methodology]({d['coding_agent_systems']['methodology_url']}). Systems with missing cost, unverified tiered costs or unavailable access are listed separately in workloads.json. A tested fallback chain stays part of that system; it is never silently represented as one model.",'','## Pending workload profiles','','| Workload | Candidate evidence | Missing requirement |','|---|---|---|']
for p in d['pending_profiles']:lines.append(f"| {p['name']} | {p['benchmark']} | {p['reason']} |")
lines+=['','## Router and Jev integration','','The selector accepts a workload plus a benchmark score or benchmark-task budget. It filters every verified candidate before recomputing dominance for required parameters, input modality and context length. An unknown workload or unsupported constraint is rejected. A removed live endpoint is rejected rather than replaced with another model.','','```sh','node select-workload.mjs workloads.json business_automation score:60 tools','node select-workload.mjs workloads.json coding_terminal budget:1 tools','node select-workload.mjs workloads.json long_context score:80 "" --min-context=128000','node select-workload.mjs workloads.json long_context budget:0 "" --allow-limited-free','```','','```js',"import {buildWorkloadSelection} from './select-workload.mjs';","const selected = await buildWorkloadSelection('workloads.json', 'business_automation',",'  {max_task_cost_usd: 0.05}, {required_parameters: [\'tools\']});','// Send selected.request with task input, tools and sufficient output budget.','```','','Jev is not integrated or calibrated by this refresh. A future predictor should estimate success for the task, workload, model revision, reasoning setting and execution setup, and be calibrated on held-out accepted outcomes. No benchmark-to-probability conversion is valid by assumption. Track attempted cost, retries, tools, verification, acceptance and latency without publishing private task content. Production evaluation runs and generation charges require a separate configured evaluation service; this public-data pipeline makes no paid calls.','','## Sources','']
for u in sorted({p['source_url'] for p in d['profiles']}|{p['methodology_url'] for p in d['profiles']}|{d['coding_agent_systems']['source_url'],d['coding_agent_systems']['methodology_url']}):lines.append('- '+u)
(P/'workloads.md').write_text('\n'.join(lines)+'\n')
# Separate log-cost panels; score scales are deliberately not shared.
W,H=1320,1185;svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="#ffffff"/><g font-family="sans-serif" fill="#19283d"><text x="45" y="36" font-size="25">Cost and capability by workload</text><text x="45" y="62" font-size="14">{d["report_date"]} · Evaluation-specific USD/task (log scale) · Verified paid configurations only</text>']
for index,p in enumerate(d['profiles']):
 col=index%2;row=index//2;left=45+col*650;top=90+row*350;f=p['frontier']
 svg.append(f'<text x="{left}" y="{top+15}" font-size="18">{html.escape(p["name"])}</text>')
 if not f:
  svg.append(f'<text x="{left}" y="{top+60}" font-size="15">Pending comparable evidence</text>');continue
 x0=left+65;x1=left+590;y0=top+45;y1=top+250
 xmin=min(r['score'] for r in f);xmax=max(r['score'] for r in f);pad=max((xmax-xmin)*.04,.1);xmin-=pad;xmax+=pad
 if p['score_unit']!='elo':xmin=max(0,xmin);xmax=min(100,xmax)
 ymin=min(r['benchmark_task_cost_usd'] for r in f)*.75;ymax=max(r['benchmark_task_cost_usd'] for r in f)*1.35
 if ymax<=ymin:ymax=ymin*2
 xs=lambda s:x0+(s-xmin)/(xmax-xmin)*(x1-x0)
 ys=lambda c:y1-(math.log10(c)-math.log10(ymin))/(math.log10(ymax)-math.log10(ymin))*(y1-y0)
 for step in range(5):
  s=xmin+(xmax-xmin)*step/4;x=xs(s)
  svg.append(f'<path d="M{x},{y0} V{y1}" stroke="#e5eaf1"/><text x="{x}" y="{y1+20}" text-anchor="middle" font-size="11">{s:.1f}</text>')
 for step in range(4):
  cost=10**(math.log10(ymin)+(math.log10(ymax)-math.log10(ymin))*step/3);y=ys(cost)
  svg.append(f'<path d="M{x0},{y} H{x1}" stroke="#e5eaf1"/><text x="{x0-8}" y="{y+4}" text-anchor="end" font-size="11">${cost:.3g}</text>')
 points=' '.join(f"{xs(r['score'])},{ys(r['benchmark_task_cost_usd'])}" for r in f)
 svg.append(f'<polyline points="{points}" fill="none" stroke="#4562d8" stroke-width="2.5"/>')
 for r in f:
  role=next((role for role in ['floor','ceiling'] if (p['recommendations'].get(role) or {}).get('configuration_id')==r['configuration_id']),None)
  color={'floor':'#14815d','ceiling':'#ba7415'}.get(role,'#4562d8')
  svg.append(f'<circle cx="{xs(r["score"])}" cy="{ys(r["benchmark_task_cost_usd"])}" r="4.5" fill="{color}"><title>{html.escape(name(r))}: {r["score"]}, ${r["benchmark_task_cost_usd"]}</title></circle>')
 axis_label={'elo':'Benchmark Elo','pass_at_1_percent':'Pass@1 (%)','guardrail_adjusted_objective_completion_percent':'Objectives completed, guardrail-adjusted (%)','all_criteria_pass_percent':'All criteria passed (%)'}.get(p['score_unit'],p['score_unit'])
 svg.append(f'<text x="{(x0+x1)/2}" y="{y1+41}" text-anchor="middle" font-size="12">{html.escape(axis_label)}</text>')
 rec=p['recommendations'].get('floor');note='No clear value knee' if not rec else 'Value knee: '+rec['configuration_id']
 svg.append(f'<text x="{left}" y="{y1+66}" font-size="12">{html.escape(note)}</text>')
svg.append('<text x="45" y="1140" font-size="13">Green: candidate floor · Amber: optional ceiling · Each panel has its own score scale · Benchmarks are not request success probabilities</text><text x="45" y="1166" font-size="12">Benchmark source: Artificial Analysis (artificialanalysis.ai). Independently maintained selection charts.</text></g></svg>')
(P/'workloads').mkdir(exist_ok=True);(P/'workloads/cost-curves.svg').write_text(''.join(svg))
section='''## Workload-specific selection

Use [workloads.md](workloads.md) for independent cost-capability frontiers for terminal coding, business automation, professional work, long-context reasoning, PDF reasoning and academic reasoning. [workloads.json](workloads.json) is the stable machine-readable contract; [workloads.schema.json](workloads.schema.json) validates it. Each profile uses its own benchmark score, evaluation task cost, harness and candidate value knees. It never borrows the general index's task cost. All configurations are reconsidered per workload, including general-chart losers. Exact routing coverage remains incomplete.

```sh
node select-workload.mjs workloads.json business_automation score:60 tools
node select-workload.mjs workloads.json coding_terminal budget:1 tools
node select-workload.mjs workloads.json long_context score:80 "" --min-context=128000
node select-workload.mjs workloads.json long_context budget:0 "" --allow-limited-free
```

The workload selector filters all verified candidates for required parameters, context and input modalities before computing dominance. It rejects unknown workloads, stale evidence, changed revisions and unsupported constraints. Budget values are benchmark-task budgets, not production prompt caps. Candidate floors and ceilings describe cost knees; a workload quality target is needed before treating one as a deployment default. The existing general selector and subscription guidance remain available.

The same daily `pipeline/refresh.mjs` acquires active public AA configuration records, rebuilds each profile, refreshes complete coding-agent system comparisons, renders curves, validates schema/evidence and selector boundaries, then publishes all artifacts and dated workload snapshots atomically. Benchmark source: [Artificial Analysis](https://artificialanalysis.ai/); original project code and documentation use [MIT](LICENSE). The maintainer has deferred the source-data rights review; see [DATA-SOURCES.md](DATA-SOURCES.md). Pending research, extraction and other profiles are explicit. A [companion Jev routing skill](skills/route-workloads-with-jev/SKILL.md) prepares classification requests and verified worker selection. Calibrated request-success routing remains unimplemented; see the [router guidance](workloads.md#router-and-jev-integration).

'''
readme=(P/'README.md').read_text()
if '## Workload-specific selection' in readme:readme=re.sub(r'## Workload-specific selection\n.*?(?=\n## |\Z)',section.rstrip()+'\n',readme,flags=re.S)
else:readme=readme.replace('## Select an API configuration',section+'## Select an API configuration',1)
(P/'README.md').write_text(readme)
general=(P/'latest.md').read_text();notice='## Workload-specific routing\n\nThe new [workload charts](workloads.md) and [workload JSON](workloads.json) provide six independently measured score/cost frontiers, exact routing and separate candidate floors/ceilings. Use `select-workload.mjs` with an explicit workload. Complete coding-agent systems and pending profiles are separate; no benchmark score is converted directly into a Jev success probability.\n\nAA now labels Opus 5.5 measurements as **Default Fallback**. Those multi-model measurements are excluded from the pinned single-model frontier. Astra configurations that become undominated are checked on the standard first-party route. The general floor and ceiling are recomputed from the retained configurations.\n\n'
general=general.replace('## Sources\n',notice+'## Sources\n',1);(P/'latest.md').write_text(general)
print('Rendered six workload tables, marginal costs, coding-agent systems and separate SVG panels')
