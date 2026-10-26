"""Render exact lookup tables and a repository-native SVG curve from the staged contract."""
import datetime,html,json,math,re
from pathlib import Path
P=Path('run-artifacts/report');d=json.loads((P/'latest.json').read_text());f=d['frontier'];c=d['coverage_inventory'];changes=d['changes_since_previous']
label=lambda r:r['model_name']+' / '+(r.get('effort') or 'thinking enabled')
control=lambda r:json.dumps(r['request']['reasoning'],separators=(',',':'))
when=datetime.date.fromisoformat(d['report_date']).strftime('%B %-d, %Y')
floor=d['recommendations']['floor'];ceiling=d['recommendations']['ceiling']
lines=[f'# AI model selection — {when}','',f"**Default API floor:** {label(floor)} — **{floor['intelligence_score']:.3f}**, **${floor['benchmark_task_cost_usd']:.6f} per AA task**. **Optional ceiling:** {label(ceiling)} — **{ceiling['intelligence_score']:.3f}**, **${ceiling['benchmark_task_cost_usd']:.6f}**.",'','## Changes since the last published report','',changes['summary'],'',f"Previous report: {changes['previous_report_date']}; common Intelligence Index v{d['benchmark']['version']}. Frontier membership {'changed' if changes['frontier_membership_changed'] else 'unchanged'}; floor and ceiling {'changed' if changes['recommendations_changed'] else 'unchanged'}.",'']
if changes.get('same_day_revision_note'):lines += [changes['same_day_revision_note'],'']
lines += ['Benchmark source: [Artificial Analysis](https://artificialanalysis.ai/). Original project code and documentation: [MIT](LICENSE). See [DATA-SOURCES.md](DATA-SOURCES.md) for attribution and the deferred source-data rights review.','']
for r in changes['revised_metrics']:
 lines.append(f"- `{r['configuration_id']}`: score {r['previous_score']} → {r['score']}; AA task cost ${r['previous_task_cost_usd']} → ${r['task_cost_usd']}. Provisional: {r['cost_provisional']}.")
lines += ['',f"Screened **{c['openrouter_model_count']} live gateway listings**, **{c['AA_release_count']} AA releases**, **{c['exact_AA_records_checked']} exact model records**, and **{c['free_catalog_entries_audited']} free listings**. Every listing is inventoried; this does not mean every model has comparable measurements.",'',f"New gateway listings: {', '.join('`'+x+'`' for x in changes['new_catalog_entries']) or 'none'}. Removed listings: {', '.join('`'+x+'`' for x in changes['removed_catalog_entries']) or 'none'}. Absence from a gateway is not proof of provider-wide retirement.",'',f"Newly observed AA release entries: {', '.join(changes['new_AA_releases']) or 'none'}. These can include a newly identified revision of an older release.",'',"The Intelligence Index measures broad capability, not percentage knowledge or a request's probability of success. These costs are AA's weighted benchmark-task costs from observed token use and published prices, not guaranteed prompt prices, OpenRouter invoices or spending caps. Numerical precision is retained for lookup; close score differences are not proof of statistical significance.",'','## Minimum cost meeting a capability target','',"Intervals are continuous: the first lower bound is inclusive, later lower bounds are exclusive, and all upper bounds are inclusive. Round only for display, and use latest.json for machine selection.",'','| Minimum-score range | request.model | request.reasoning | Delivered score | USD / AA task |','|---|---|---|---:|---:|']
for r in f:
 lo=r['minimum_score_exclusive'];hi=r['intelligence_score'];ran=f'[0, {hi}]' if lo is None else f'({lo}, {hi}]'
 lines.append(f"| {ran} | `{r['request']['model']}` | `{control(r)}` | {hi:.3f} | ${r['benchmark_task_cost_usd']:.6f} |")
lines += ['',f"No eligible verified configuration meets a score above {f[-1]['intelligence_score']}.",'','## Most capability within a benchmark-task budget','','| Budget interval, USD / AA task | request.model | request.reasoning | Delivered score |','|---|---|---|---:|']
for r in f:
 high=r['maximum_budget_exclusive'];ran=f"[{r['minimum_budget_inclusive']}, {high})" if high is not None else f"[{r['minimum_budget_inclusive']}, ∞)"
 lines.append(f"| {ran} | `{r['request']['model']}` | `{control(r)}` | {r['intelligence_score']:.3f} |")
lines += ['','## Exact revision and route contract','','Every request uses `provider.require_parameters=true`, `provider.allow_fallbacks=false`, and exactly one verified provider tag. Standard endpoint prices and parameters are checked; a different revision, quantization, unsupported setting or stale report causes rejection. No generation calls or keys are embedded in these reports.','','| Callable model | Canonical revision | provider.only | API surface |','|---|---|---|---|']
seen=set()
for r in f+d.get('limited_free_configurations',[]):
 if r['openrouter_model_id'] in seen:continue
 seen.add(r['openrouter_model_id']);lines.append(f"| `{r['request']['model']}` | `{r['openrouter_canonical_slug']}` | `{r['request']['provider']['only'][0]}` | `{r['api_endpoint'].split('/')[-1]}` |")
lines += ['',"MiMo uses `reasoning.enabled=true`, corresponding to native `thinking.type=enabled`; its metadata effort is null and is omitted from the actual request. Named non-none MiMo efforts do not define different thinking intensities. Preserve reasoning details across tool turns, omit unsupported sampling controls and allow sufficient output tokens. Provider token prices are recorded separately from AA measured task costs.",'','## Free lane: explicit opt-in','']
for r in d.get('limited_free_configurations',[]):
 lines += [f"- `{r['request']['model']}` with `{control(r)}`: score **{r['intelligence_score']}**, measured AA task cost **${r['benchmark_task_cost_usd']}**; pinned first-party provider `{r['request']['provider']['only'][0]}`. Requires `allow_limited_free:true` / `--allow-limited-free`. Rate limits and quota apply. Undisclosed managed quantization is recorded rather than replaced with a third-party route."]
lines += ['',"Other free listings remain pending unless the exact revision, reasoning state, first-party route and independently measured zero-cost basis match. A gateway token price of zero is not sufficient evidence of AA task cost zero.",'','## Marginal costs, floor and ceiling','',floor['rationale'],'',ceiling['rationale'],'',"The recommendation heuristic uses the first ≥3× rise in adjacent marginal dollars per point accompanied by ≥50% higher task cost as a candidate floor, and the next such cliff as an optional ceiling. All steps are evaluated. These are workload-conditional starting points, not universal optima. Index intervals need not have equal practical value. Smaller local bends and model-family transitions remain visible below.",'','| Upgrade to | Index point gain | Added USD/task | Cost increase | Added USD/point | Relative to previous marginal rate |','|---|---:|---:|---:|---:|---:|']
for r in f[1:]:
 m=r['marginal'];multiple=m['versus_previous_marginal_multiple'];mult='—' if multiple is None else f'{multiple:.2f}×'
 lines.append(f"| {label(r)} | {m['score_gain']:.6f} | ${m['additional_cost_usd']:.6f} | {m['cost_increase_percent']:.2f}% | ${m['additional_usd_per_index_point']:.6f} | {mult} |")
lines += ['',"Pay above the ceiling when difficult debugging, architecture, research, avoidable failures or human review are worth the additional cost. For simple, repeatable work, select the cheapest model meeting a measured workload success target. Do not convert an evaluator's 0–1 success probability directly into this index.",'','![Measured cost versus capability](cost-curve.svg)','','## Excluded or pending evidence','',"Haiku 5.5 costs remain provisional because AA's article still omits tiered pricing above 100K input tokens. Its prerelease refusal issue and Sonnet's structured-output reruns are not confirmed complete. Their measured scores are retained without assigning actionable request costs. Kimi K3.1 Pro has a measured pair, but AA's current record does not identify the effort used; its native default alone is insufficient proof. Current exact model cost also differs from the launch article. No guessed mapping is admitted.",'','| Model or configuration | Measured score if available | Task cost if complete | Exclusion / uncertainty |','|---|---:|---:|---|']
for r in d['excluded_or_pending']:
 name=r.get('model',r.get('configuration_id',r.get('openrouter_model_id','unknown')))
 score=r.get('intelligence_score');cost=r.get('benchmark_task_cost_usd');reason=r.get('reason','; '.join(r.get('exclusion_reasons',[]))).replace('|','/').replace('\n',' ')
 lines.append(f"| {name} {r.get('effort') or ''} | {score if score is not None else '—'} | {'$'+str(cost) if cost is not None else '—'} | {reason} |")
lines += ['',"Gemini 4 Argon API became generally available October 13; the live gateway revision is now 20261013. The September 30 restricted-release benchmark is not silently attached to that GA revision. Its earlier high-effort pair is also dominated by Opus high. Introductory token prices expire November 30 according to Google's current guide; token rates are not substituted for measured task costs. The old Fairwind announcement is historical rollout context.",'','## Build through subscription services','',"Personal tiers and account menus are unknown. All subscription scores and task costs are null unless separately measured in the exact app/agent harness. UI Standard/Extended, Heavy/Deep Think and Ultra are not mapped to API efforts or single-model API scores.",'','| Service | Routine default | Escalation | Quota-saving choice | Source check complete |','|---|---|---|---|---|']
for service in d['subscription_recommendations']['services']:
 rs={r['role']:r for r in service['recommendations']}
 def desc(role):
  r=rs[role];return r['model_label']+'; `'+json.dumps(r['control'],separators=(',',':'))+'`'
 lines.append(f"| {service['service']} | {desc('routine_default')} | {desc('escalation')} | {desc('quota_saving')} | {service.get('source_verification_complete',False)} |")
for service in d['subscription_recommendations']['services']:
 lines += ['',f"**{service['service']}:** {service['limits_note']}"]
 if service.get('unverified_source_urls'):lines += ['Unverified this run: '+', '.join(service['unverified_source_urls'])+'. Previous verification dates are retained.']
lines += ['',"Eligible Claude Max/Team users can claim first-party API credits; eligibility depends on exact plan, claim and linked Console organization. These credits do not pay OpenRouter invoices. No personal entitlement is assumed.",'','## Verification and freshness','',f"Checked {d['checked_at']} (report date in America/Chicago). AA v{d['benchmark']['version']}; exact evaluation completion dates remain unpublished. Catalog checked {c['catalog_verified_at']}; registry checked {c['AA_registry_verified_at']}. Each score, route and source has its own successful verification timestamp. Reports and actionable rows expire after 48 hours. Unsuccessful source checks are disclosed and not advanced.",'',"Source sites, original configuration data and endpoint metadata are required inputs. New releases with unverified benchmark controls remain pending and do not inherit another revision's results. Release maxima and cost minima are optimistic screening bounds, never a fabricated configuration pair. See coverage.json for the entire inventory and latest.json for exact intervals and eligibility.",'','## Sources','']
for u in d['sources']:lines.append('- '+u)
(P/'latest.md').write_text('\n'.join(lines)+'\n')
# Native vector chart: broad index vs logarithmic measured task cost; zero-cost lane is separate.
w,h=1000,620;x0,y0,x1,y1=90,100,930,500
low=min(r['intelligence_score'] for r in f)-1;high=max(r['intelligence_score'] for r in f)+2
minc=min(r['benchmark_task_cost_usd'] for r in f)*.8;maxc=max(r['benchmark_task_cost_usd'] for r in f)*1.2
xs=lambda s:x0+(s-low)/(high-low)*(x1-x0)
ys=lambda c:y1-(math.log10(c)-math.log10(minc))/(math.log10(maxc)-math.log10(minc))*(y1-y0)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="white"/><g font-family="sans-serif" fill="#172033"><text x="90" y="38" font-size="25">All-lab paid cost–capability frontier</text><text x="90" y="65" font-size="15">{when} · AA v{d["benchmark"]["version"]} · Log cost · Unverified and free lanes excluded</text>']
for score in range(math.ceil(low/10)*10,math.floor(high/10)*10+1,10):
 x=xs(score);svg.append(f'<path d="M{x},100 V500" stroke="#e5e9ef"/><text x="{x}" y="525" text-anchor="middle" font-size="14">{score}</text>')
for cost in [.005,.01,.03,.1,.3,1,3,6]:
 if minc<=cost<=maxc:
  y=ys(cost);svg.append(f'<path d="M90,{y} H930" stroke="#e5e9ef"/><text x="78" y="{y+5}" text-anchor="end" font-size="14">${cost}</text>')
svg += ['<text x="510" y="555" text-anchor="middle" font-size="16">Delivered Intelligence Index score</text><text x="15" y="305" transform="rotate(-90 15 305)" text-anchor="middle" font-size="16">USD per weighted benchmark task (log)</text>','<polyline points="'+' '.join('{},{}'.format(xs(r['intelligence_score']),ys(r['benchmark_task_cost_usd'])) for r in f)+'" fill="none" stroke="#4361ee" stroke-width="3"/>']
for r in f:
 x,y=xs(r['intelligence_score']),ys(r['benchmark_task_cost_usd']);color='#16845c' if r['configuration_id']==floor['configuration_id'] else '#c47707' if r['configuration_id']==ceiling['configuration_id'] else '#4361ee'
 svg.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{color}"><title>{html.escape(label(r))}: {r["intelligence_score"]:.3f}, ${r["benchmark_task_cost_usd"]:.6f}</title></circle>')
for r,title,offset in [(floor,'Floor: '+floor['model_name'],48),(ceiling,'Ceiling: '+ceiling['model_name'],-30)]:
 x,y=xs(r['intelligence_score']),ys(r['benchmark_task_cost_usd']);mode=r.get('effort') or 'thinking enabled';svg.append(f'<text x="{x-8}" y="{y+offset}" text-anchor="end" font-size="14"><tspan>{html.escape(title)}</tspan><tspan x="{x-8}" dy="18">{html.escape(mode)}</tspan></text>')
svg.append('<text x="90" y="592" font-size="14">Broad capability, not percentage knowledge. AA benchmark cost is not an invoice estimate.</text><text x="90" y="614" font-size="12">Benchmark source: Artificial Analysis (artificialanalysis.ai). Independently maintained selection chart.</text></g></svg>');(P/'cost-curve.svg').write_text(''.join(svg))
readme=(P/'README.md').read_text();start=readme.index('## October');end=readme.index('## Files and cost basis',start)
rec=f'''## {when} recommendation

API floor: **{label(floor)}**, score **{floor['intelligence_score']}**, **${floor['benchmark_task_cost_usd']}** per measured AA task. Optional ceiling: **{label(ceiling)}**, score **{ceiling['intelligence_score']}**, **${ceiling['benchmark_task_cost_usd']}**. Both are workload-conditional heuristics.

{changes['summary']}

Discovery screens {c['openrouter_model_count']} live OpenRouter entries and {c['AA_release_count']} AA releases across all labs. Only exact comparable benchmark/route pairs are actionable. See [latest.md](latest.md) for full threshold and budget tables, all marginal costs, source limitations and conditional subscription guidance. Kimi K3.1 Pro is pending an explicit AA effort match; Haiku's complete tiered task costs and Sonnet's prerelease reruns remain pending. Gemini 4 Argon API is now GA, with revision correspondence handled separately.

'''
readme=readme[:start]+rec+readme[end:]
marker='## Scheduled pipeline'
if marker in readme:readme=readme[:readme.index(marker)]
readme+='''## Scheduled pipeline

The existing workflow runs `node pipeline/refresh.mjs`: public AA exact-record and full release acquisition, live OpenRouter catalog and pinned endpoint checks, report assembly, rendering, schema/selector/evidence validation, and one atomic fast-forward publication. It uses the existing daily schedule; only verified evidence advances timestamps. An AA API key is optional for separate catalog diagnostics and is not required by the public-source report path. No generation API is called.

Run `node pipeline/refresh.mjs` locally to stage and validate `run-artifacts/report/`. `--publish` additionally requires the existing GitHub integration or the workflow's scoped `GITHUB_TOKEN`; credentials are never put in reports. `pipeline/publish.mjs` creates individual blobs, then a small tree, commit and non-force ref update, and verifies the remote contents. This avoids the earlier large inline tree request. On a concurrent update it stops safely; a fresh run rebuilds from current main.

The Dot monitor remains responsible for web research and reviewing new candidates, lifecycle changes and subscription UI correspondence. A newly listed model stays pending until its exact AA configuration, revision, reasoning control and route are verified. This is deliberate eligibility enforcement; supported effort names alone cannot supply missing benchmarks. Failed acquisition or validation preserves the last published report and produces diagnostic artifacts.
'''
(P/'README.md').write_text(readme)
print('Rendered complete score/budget lookup tables, all marginal steps, subscription track and SVG curve')
