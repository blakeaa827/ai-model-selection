"""Assemble a fresh report from public, exact configuration evidence. Stages output only."""
import json,copy,datetime,re,os,shutil
from zoneinfo import ZoneInfo
from pathlib import Path
from collections import Counter
P=Path('.'); R=Path('run-artifacts/acquisition'); O=Path('run-artifacts/report'); (O/'snapshots').mkdir(parents=True,exist_ok=True)
shutil.copyfile(P/'README.md',O/'README.md')
d=json.load(open(P/'latest.json')); old=copy.deepcopy(d)
catalog=json.load(open(R/'catalog.json'));cat={m['id']:m for m in catalog['data']};ct=catalog['verified_at']
metrics=json.load(open(R/'metrics.json'));aa={a['source_url']:a for a in metrics}
errors=[a for a in metrics if a.get('error')];metrics=[a for a in metrics if not a.get('error')];aa={a['source_url']:a for a in metrics}
versions={a['version'] for a in metrics};assert len(versions)==1,'Incompatible benchmark versions';version=next(iter(versions))
eps=json.load(open(R/'endpoints.json')); docs=json.load(open(R/'doc-checks.json'))
checks={x['url']:{k:v for k,v in x.items() if k!='text'} for x in docs if x['status']=='opened_successfully'}
now=datetime.datetime.now(datetime.timezone.utc).isoformat();date=datetime.datetime.now(ZoneInfo('America/Chicago')).date().isoformat()
# Only external checks actually completed in this run may advance documentation timestamps.
override=Path('run-artifacts/source-check-overrides.json')
if override.exists():
 for r in json.loads(override.read_text()):
  stamp=datetime.datetime.fromisoformat(r['verified_at']);age=(datetime.datetime.now(datetime.timezone.utc)-stamp).total_seconds()
  assert 0<=age<=172800 and r['status']=='opened_successfully'
  checks[r['url']]=r
recovered=[u for u in checks if checks[u].get('retrieval')=='web original-source retrieval']
changed=[]
provisional_reason=next(r['exclusion_reasons'][0] for r in d['evaluated_configurations'] if r['openrouter_model_id']=='anthropic/claude-haiku-5.5')
for r in d['evaluated_configurations']:
 a=aa.get(r['benchmark_source_url'])
 if not a:
  r.update(eligible_for_frontier=False,exclusion_reasons=['Exact source retrieval failed; verification timestamp not advanced']);continue
 cost=(a.get('intelligenceIndexCostPerTask') or {}).get('cost',{}).get('total')
 prior=r.get('provisional_benchmark_task_cost_usd',r['benchmark_task_cost_usd'])
 if r['intelligence_score']!=a['intelligenceIndex'] or prior!=cost:changed.append({'configuration_id':r['configuration_id'],'previous_score':r['intelligence_score'],'score':a['intelligenceIndex'],'previous_task_cost_usd':prior,'task_cost_usd':cost,'cost_provisional':r.get('benchmark_cost_status','').startswith('provisional')})
 r.update(intelligence_score=a['intelligenceIndex'],benchmark_task_cost_usd=cost,benchmark_verified_at=a['verified_at'],benchmark_version=a['version'],benchmark_score_is_estimated=a['intelligenceIndexIsEstimated'],AA_model_label=a['name'])
 m=cat.get(r['openrouter_model_id'])
 if m and m['canonical_slug']==r['openrouter_canonical_slug']:r['openrouter_verified_at']=ct
 else:r.update(eligible_for_frontier=False,exclusion_reasons=['Live catalog missing or revision mismatch'])
 if a['deprecated'] or a['intelligenceIndexIsEstimated'] or cost is None:r.update(eligible_for_frontier=False,exclusion_reasons=['AA result deprecated, estimated or missing comparable task cost'])
 if r['openrouter_model_id']=='anthropic/claude-haiku-5.5':
  r.update(provisional_benchmark_task_cost_usd=cost,benchmark_task_cost_usd=None,eligible_for_frontier=False,benchmark_cost_status='provisional_incomplete_tiered_pricing',pareto_dominated=None)
def dominates(a,b):
 return a['intelligence_score']>=b['intelligence_score'] and a['benchmark_task_cost_usd']<=b['benchmark_task_cost_usd'] and (a['intelligence_score']>b['intelligence_score'] or a['benchmark_task_cost_usd']<b['benchmark_task_cost_usd'])
eligible=[r for r in d['evaluated_configurations'] if r.get('eligible_for_frontier') and r['benchmark_task_cost_usd'] is not None]
winning=[r for r in eligible if not any(dominates(x,r) for x in eligible if x is not r)]
templates={r['configuration_id']:r for r in old['frontier']}
assert all(r['configuration_id'] in templates for r in winning),'New winner requires complete request template verification'
def refresh_route(row):
 a=aa[row['benchmark_source_url']];m=cat[row['openrouter_model_id']];er=eps[row['openrouter_model_id']]
 assert m['canonical_slug']==row['openrouter_canonical_slug'] and (not m.get('expiration_date') or m['expiration_date']>date)
 ep=next(e for e in er['data']['endpoints'] if e['tag']==row['request']['provider']['only'][0])
 assert ep['status']==0 and row['openrouter_canonical_slug'] in ep['name']
 assert {'reasoning','tools'}<=set(ep['supported_parameters'])
 if row['effort'] is not None:assert row['effort'] in m['reasoning']['supported_efforts'] and 'reasoning_effort' in ep['supported_parameters']
 else:assert row['request']['reasoning']=={'enabled':True}
 prior=row['endpoint_verification'].get('quantization')
 if prior is not None:assert ep.get('quantization')==prior
 assert float(m['pricing']['prompt'])==float(ep['pricing']['prompt']) and float(m['pricing']['completion'])==float(ep['pricing']['completion'])
 row.update(intelligence_score=a['intelligenceIndex'],benchmark_task_cost_usd=a['intelligenceIndexCostPerTask']['cost']['total'],benchmark_verified_at=a['verified_at'],openrouter_verified_at=ct)
 row['endpoint_verification'].update(verified_at=er['verified_at'],status=ep['status'],supported_parameters=ep['supported_parameters'],standard_pricing_matches_catalog=True)
 u=row.get('reasoning_control',{}).get('source')
 if u in checks:row['reasoning_control']['documentation_verified_at']=checks[u]['verified_at']
 return row
front=sorted([refresh_route(copy.deepcopy(templates[r['configuration_id']])) for r in winning],key=lambda r:r['intelligence_score'])
for r in eligible:r['pareto_dominated']=any(dominates(x,r) for x in front)
for i,r in enumerate(front):
 prev=front[i-1] if i else None
 r.update(minimum_score_exclusive=prev['intelligence_score'] if prev else None,maximum_score_inclusive=r['intelligence_score'],minimum_budget_inclusive=r['benchmark_task_cost_usd'],maximum_budget_exclusive=front[i+1]['benchmark_task_cost_usd'] if i+1<len(front) else None)
 if prev:
  gain=r['intelligence_score']-prev['intelligence_score'];added=r['benchmark_task_cost_usd']-prev['benchmark_task_cost_usd'];rate=added/gain;pm=prev['marginal']
  r['marginal']={'previous_configuration_id':prev['configuration_id'],'score_gain':gain,'additional_cost_usd':added,'cost_increase_percent':100*added/prev['benchmark_task_cost_usd'],'additional_usd_per_index_point':rate,'versus_previous_marginal_multiple':rate/pm['additional_usd_per_index_point'] if pm else None}
  r.pop('minimum_score_inclusive',None)
 else:r['marginal']=None;r['minimum_score_inclusive']=0
d['frontier']=front;d['limited_free_configurations']=[refresh_route(r) for r in d['limited_free_configurations']]
for r in d['limited_free_configurations']:assert r['benchmark_task_cost_usd']==0 and float(cat[r['openrouter_model_id']]['pricing']['prompt'])==0
# Descriptive knees: a >=3x marginal-rate jump with >=50% added task cost.
# This is a visible workload-conditional heuristic, never an intelligence utility scale.
knees=[i-1 for i,r in enumerate(front) if i and r['marginal'].get('versus_previous_marginal_multiple') is not None and r['marginal']['versus_previous_marginal_multiple']>=3 and r['marginal']['cost_increase_percent']>=50]
if not knees: raise ValueError('No meaningful default knee found; review recommendations explicitly')
picks={'floor':knees[0],'ceiling':knees[1] if len(knees)>1 else knees[0]}
for role,index in picks.items():
 row=front[index];rec=copy.deepcopy(row);rec['confidence']='workload_conditional_frontier_heuristic; intervals not equal practical utility';rec['rationale']='Recomputed from all adjacent marginal steps; verify success rate on the intended workload.';d['recommendations'][role]=rec
 if role=='floor':rec['recommendation_method']='First >=3x adjacent marginal cost/point increase accompanied by >=50% higher task cost; descriptive heuristic, not a universal optimum.'
 else:rec['recommendation_method']='Configuration before the next such sharp cliff after the floor; optional escalation.'
d['breakpoints']=[{'after_configuration_id':front[i]['configuration_id'],'next_configuration_id':front[i+1]['configuration_id'],'kind':'value_knee' if j==0 else 'sharp_cost_cliff',**front[i+1]['marginal']} for j,i in enumerate(knees)]
for m in d['models']:
 cm=cat.get(m['openrouter_model_id'])
 if not cm or cm['canonical_slug']!=m['openrouter_canonical_slug']:
  m['availability']='unavailable or revision mismatch; previous documentation retained';continue
 m.update(verified_at=ct,supported_efforts=cm.get('reasoning',{}).get('supported_efforts'),catalog_default_effort=cm.get('reasoning',{}).get('default_effort'),openrouter_pricing_per_token=cm['pricing'])
 m['standard_short_context_prices_usd_per_million_tokens']={k:float(cm['pricing'][v])*1e6 for k,v in [('input','prompt'),('output','completion'),('cache_read','input_cache_read'),('cache_write','input_cache_write')] if v in cm['pricing']}
 for urlkey,timekey in [('provider_documentation_url','provider_documentation_verified_at'),('provider_pricing_url','provider_pricing_verified_at')]:
  if m.get(urlkey) in checks:m[timekey]=checks[m[urlkey]]['verified_at']
for r in d['excluded_or_pending']:
 if r.get('model')=='Claude Haiku 5.5':r['intelligence_score']=next(x['intelligence_score'] for x in d['evaluated_configurations'] if x['openrouter_model_id']==r['openrouter_model_id'] and x['effort']==r['effort'])
# Refresh existing pending catalog identity evidence without duplicating entries.
for row in d['excluded_or_pending']:
 cm=cat.get(row.get('openrouter_model_id'))
 if cm:
  if row.get('openrouter_canonical_slug') and row['openrouter_canonical_slug']!=cm['canonical_slug']:
   row['reason']='Catalog revision changed; benchmark correspondence must be reverified.'
  row['catalog_verified_at']=ct
  row['supported_efforts']=cm.get('reasoning',{}).get('supported_efforts')
d.update(report_date=date,checked_at=now)
d['benchmark']['verified_at']=max(a['verified_at'] for a in metrics)
d['benchmark']['version']=version
d['benchmark']['evaluation_run_date_note']=date+' is the source verification date; exact AA evaluation completion dates remain unpublished.'
d['scope']['benchmark_frontier_rechecked_date']=date
newids=sorted(set(cat)-{r['model_id'] for r in json.load(open(P/'coverage.json'))['catalog_models']})
removed=sorted({r['model_id'] for r in json.load(open(P/'coverage.json'))['catalog_models']}-set(cat))
previous_coverage=json.load(open(P/'coverage.json'));old_catalog={r['model_id']:r for r in previous_coverage['catalog_models']}
pricing_changes=[{'model_id':mid,'previous_per_token':old_catalog[mid]['openrouter_pricing_per_token'],'current_per_token':cat[mid]['pricing'],'basis':'gateway token prices, not measured AA task cost'} for mid in sorted(set(old_catalog)&set(cat)) if old_catalog[mid].get('openrouter_pricing_per_token') is not None and old_catalog[mid]['openrouter_pricing_per_token']!=cat[mid]['pricing']]
oldreg={r['AA_release_slug'] for r in previous_coverage['AA_release_screening']}
newreleases=sorted({r['slug'] for r in json.load(open(R/'registry.json'))['releases']}-oldreg)
frontier_changed=[(r['configuration_id'],r['intelligence_score'],r['benchmark_task_cost_usd']) for r in front]!=[(r['configuration_id'],r['intelligence_score'],r['benchmark_task_cost_usd']) for r in old['frontier']]
revision=old['changes_since_previous'].get('revision',0)+1 if old['report_date']==date else 1
summary=f"Refreshed {len(front)} paid configurations and {len(d['limited_free_configurations'])} opt-in free configurations. {len(changed)} numerical source revisions; {len(newids)} new and {len(removed)} absent gateway listings; {len(newreleases)} new AA releases since {old['report_date']}. New candidates require exact effort/revision correspondence before routing."
d['changes_since_previous']={'previous_report_date':old['report_date'],'previous_commit':os.environ.get('REPORT_PARENT_SHA') or None,'revision':revision,'benchmark_version_changed':version!=old['benchmark']['version'],'frontier_changed':frontier_changed,'frontier_membership_changed':{r['configuration_id'] for r in front}!={r['configuration_id'] for r in old['frontier']},'recommendations_changed':any(old['recommendations'][k]['configuration_id']!=d['recommendations'][k]['configuration_id'] for k in ('floor','ceiling')),'new_eligible_releases':[],'removed_actionable_configurations':[],'new_catalog_entries':newids,'removed_catalog_entries':removed,'new_AA_releases':newreleases,'revised_metrics':changed,'gateway_token_pricing_changes':pricing_changes,'summary':summary}
if old['report_date']==date:d['changes_since_previous']['same_day_revision_note']='Reverified same-day snapshot; previous version is preserved in Git history.'
# Keep new measured models separately until original-source controls and routing match.
for a in metrics:
 if (a.get('release',{}).get('slug') in newreleases or a['slug'] in {r.get('AA_model_slug') for r in old['excluded_or_pending']}) and a['source_url'] not in {r.get('benchmark_source_url') for r in d['evaluated_configurations']}:
  cost=(a.get('intelligenceIndexCostPerTask')or{}).get('cost',{}).get('total')
  row={'model':a['name'],'AA_release_slug':a.get('release',{}).get('slug'),'AA_model_slug':a['slug'],'intelligence_score':a['intelligenceIndex'],'benchmark_task_cost_usd':cost,'benchmark_verified_at':a['verified_at'],'benchmark_version':a['version'],'source_url':a['source_url'],'reason':'Measured original-source pair; exact benchmark reasoning control, revision and public provider-route correspondence not verified. No request or effort invented.'}
  if a['slug']=='kimi-k3-1-pro':row['reason']='AA publishes an unlabeled reasoning configuration, with no explicit effort in its exact record. Native default is max, but this is not proof of the effort used by AA. Gateway additionally advertises none despite official always-on thinking. Standard first-party MXFP4 route exists; benchmark effort/deployment correspondence remains pending. Current model task cost $2.1145052918767275 differs from launch article $1.98; current exact record takes precedence. Weights promised by November 4 are not yet available.'
  d['excluded_or_pending']=[r for r in d['excluded_or_pending'] if r.get('AA_model_slug')!=a['slug']];d['excluded_or_pending'].append(row)
# Complete inventory and optimistic release screening, with explicit special-case eligibility.
step=cat.get('stepfun/step-5-preview',{'id':'stepfun/step-5-preview'})
reg=json.load(open(R/'registry.json'));rt=reg['verified_at'];releases=reg['releases'];cov=json.load(open(P/'coverage.json'));oldcov={r['model_id']:r for r in cov['catalog_models']};ids={r['openrouter_model_id'] for r in front};known={r['openrouter_model_id'] for r in d['models']};freeids={r['openrouter_model_id'] for r in d['limited_free_configurations']}
norm=lambda s:re.sub('[^a-z0-9]','',s.lower())
inventory=[]
for m in catalog['data']:
 name=re.sub(r' \((free|batch)\)$','',m['name'].split(': ',1)[-1],flags=re.I);matches=[r['slug'] for r in releases if norm(r['name'])==norm(name)]
 status='verified_frontier_model' if m['id'] in ids else 'verified_limited_free_configuration' if m['id'] in freeids else 'model_verified_other_configurations' if m['id'] in known else 'candidate_name_match_unverified' if matches else 'pending_comparable_results_or_exact_identity_match'
 reason=None
 if m['id'].endswith(':batch'):status='pending_comparable_processing_tier_results';reason='No exact AA configuration score and measured weighted task cost for this processing tier.'
 if m.get('expiration_date') and m['expiration_date']<=date:status='retired_or_expired';reason='catalog expiration date reached'
 if m['id'].startswith('anthropic/claude-haiku-5.5'):status='pending_comparable_complete_task_cost';reason=provisional_reason
 if m['id']=='anthropic/claude-sonnet-5.5':status='prerelease_deployment_match_unverified';reason='AA structured-output bug reruns not confirmed; max fallback setting not blindly mapped'
 if m['id']==step['id']:status='routing_revision_effort_match_unverified';reason='Gateway revision versus existing AA model; named effort not matched'
 row={'model_id':m['id'],'canonical_slug':m.get('canonical_slug'),'name':m['name'],'status':status,'AA_candidate_name_matches':matches,'supported_efforts':m.get('reasoning',{}).get('supported_efforts'),'output_modalities':m.get('architecture',{}).get('output_modalities'),'expiration_date':m.get('expiration_date'),'openrouter_pricing_per_token':m.get('pricing'),'pricing_basis':'gateway token prices; not AA weighted task cost','reasoning_catalog':m.get('reasoning')}
 if reason:row['reason']=reason
 if m['id'].endswith(':free'):
  row['free_route_audit']={'requires_opt_in':True,'matching_zero_cost_AA_pair_and_first_party_route_verified':m['id'] in freeids,'reason':'Verified first-party thinking route, matching measured zero-cost basis' if m['id'] in freeids else 'Token-price zero is not a measured task-cost pair. Unmatched/unverified free route stays pending; North Mini Code zero-cost score is below Gemma.'}
 inventory.append(row)
checked={a.get('release',{}).get('slug') for a in metrics}
screen=[]
for r in releases:
 score=r.get('intelligenceIndex');cost=(r.get('costPerTaskRange')or{}).get('min');dom=next((f['configuration_id'] for f in front if score is not None and cost is not None and f['intelligence_score']>=score and f['benchmark_task_cost_usd']<=cost),None)
 status='deprecated' if r['isDeprecated'] else 'pending_comparable_metrics' if score is None or cost is None else 'dominated_even_at_optimistic_release_bounds' if dom else 'configuration_results_checked' if r['slug'] in checked else 'pending_routing_or_configuration_verification'
 if r['slug']=='claude-haiku-5-5':status='provisional_incomplete_tiered_cost'
 if r['slug']=='claude-sonnet-5-5':status='prerelease_deployment_match_unverified'
 if r['slug']=='gpt-6-sol-daybreak-blue':status='restricted_separate_harness_no_common_metrics'
 if r['slug']=='gemini-4-argon':status='restricted_unavailable_public_route'
 if r['slug']=='kimi-k3-1-pro':status='benchmark_effort_revision_correspondence_unverified'
 screen.append({'AA_release_slug':r['slug'],'name':r['name'],'creator':r['creator']['name'],'score_upper_bound':score,'task_cost_lower_bound_usd':cost,'status':status,'dominated_by':dom,'source_path':r['href']})
cov.update(report_date=date,catalog_verified_at=ct,AA_registry_verified_at=rt,catalog_models=inventory,AA_release_screening=screen)
cov['provenance']='All catalog identity/effort metadata inventoried at catalog_verified_at; all AA release bounds checked at AA_registry_verified_at. Exact routing and benchmark checks have separate row timestamps. Release maxima/minima are screening bounds, never measured pairs. Haiku cost bounds are explicitly provisional and excluded.'
d['coverage_inventory'].update(openrouter_model_count=len(inventory),AA_release_count=len(screen),paid_frontier_configuration_count=len(front),catalog_verified_at=ct,AA_registry_verified_at=rt,status_counts=dict(Counter(r['status'] for r in inventory)),limited_free_configuration_count=len(d['limited_free_configurations']),exact_AA_records_checked=len(metrics))
cov['removed_since_previous']=[{**oldcov[mid],'status':'unavailable_not_in_live_catalog','last_observed_catalog_date':old['report_date'],'absence_verified_at':ct} for mid in removed]
d['coverage_inventory']['status_counts']=dict(Counter(r['status'] for r in inventory))
d['coverage_inventory']['free_catalog_entries_audited']=sum(m['id'].endswith(':free') for m in catalog['data'])
sub=d['subscription_recommendations'];sub['last_verification_attempt_at']=now
for s in sub['services']:
 s['sources']=list(dict.fromkeys(s['sources']))
 s['source_checks']=[checks[u] for u in s['sources'] if u in checks]
 s['source_verification_complete']=len(s['source_checks'])==len(s['sources'])
 s['unverified_source_urls']=[u for u in s['sources'] if u not in checks]
 s['last_successful_source_check_at']=max((x['verified_at'] for x in s['source_checks']),default=s.get('verified_at'))
 if s['source_verification_complete']:s['verified_at']=s['last_successful_source_check_at']
 for r in s['recommendations']:r.update(intelligence_score=None,benchmark_task_cost_usd=None,account_access_verified=False)
 if s.get('first_party_API_credit') and s['first_party_API_credit']['source'] in checks:s['first_party_API_credit']['verified_at']=checks[s['first_party_API_credit']['source']]['verified_at']
# Resolve launch announcements against newer official lifecycle documentation.
google_changes=next((r.get('text','') for r in docs if r['url']=='https://ai.google.dev/gemini-api/docs/changelog' and r['status']=='opened_successfully'),'')
argon_ga='Gemini 4 Argon' in google_changes and 'October 13, 2026' in google_changes and 'generally available' in google_changes
if argon_ga and 'google/gemini-4-argon' in cat:
 for r in d['excluded_or_pending']:
  if 'Argon' in r.get('model','') or r.get('AA_release_slug')=='gemini-4-argon':r['reason']='API generally available October 13, 2026 and gateway revision 20261013 now listed. AA September 30 deployment-to-GA correspondence remains unverified; earlier AA high-effort score/cost is also dominated by Opus high. Do not claim the model is still restricted-only.'
 for r in cov['AA_release_screening']:
  if r['AA_release_slug']=='gemini-4-argon':r['status']='GA_revision_correspondence_unverified';r['official_GA_date']='2026-10-13'
 d['caveats']=[r for r in d['caveats'] if not ('Argon' in r and ('no public' in r or 'restricted' in r))]
 d['changes_since_previous']['availability_updates']=[{'model':'Gemini 4 Argon','official_GA_date':'2026-10-13','catalog_canonical_slug':cat['google/gemini-4-argon']['canonical_slug'],'source_url':'https://ai.google.dev/gemini-api/docs/changelog'}]
 for service in sub['services']:
  if service['service']=='Gemini' and 'Gemini 4 Argon API is GA as of October 13' not in service['limits_note']:service['limits_note']+=' Gemini 4 Argon API is GA as of October 13; consumer-plan and exact UI access remain conditional. Do not use the older Fairwind launch announcement as proof that current API access is restricted.'

d['source_checks']=list(checks.values())
d['source_checks']+=[{'url':a['source_url'],'verified_at':a['verified_at'],'status':'opened_successfully','retrieval':'public embedded exact numerical record'} for a in metrics]
d['source_checks']+=[{'url':e['source_url'],'verified_at':e['verified_at'],'status':'opened_successfully'} for e in eps.values()]
d['source_checks']+=[{'url':'https://openrouter.ai/api/v1/models','verified_at':ct,'status':'opened_successfully'},{'url':'https://artificialanalysis.ai/models/releases','verified_at':rt,'status':'opened_successfully'}]
d['sources']=sorted(set(d['sources'])|{r['url'] for r in d['source_checks']})
d['verification_limitations']={'raw_HTTP_failures_recovered_with_web':recovered,'unsuccessful_sources_not_advanced':[{'url':r['url'],'error':r['error']} for r in docs if r['status']=='failed' and r['url'] not in recovered],'no_paid_generation_calls':True,'account_access_not_verified':True,'benchmark_run_completion_dates_unpublished':True,'acquisition_errors':errors,'new_configuration_routing_requires_original_source_match':True}
assert front and len(inventory)==len(cat) and len(screen)==len(releases)
assert all(not r.get('error') for r in eps.values())
assert not any(r['openrouter_model_id']=='anthropic/claude-haiku-5.5' for r in front)
assert all(not any(dominates(x,r) for x in eligible) for r in front)
# Unknown configurations stay pending; they do not block an otherwise verified refresh.
for role,rec in d['recommendations'].items():
 row=next(r for r in front if r['configuration_id']==rec['configuration_id']);i=front.index(row)
 if i and i+1<len(front):
  following=front[i+1]['marginal'];prior=row['marginal']
  rec['rationale']=f"Workload-conditional {role}: next step adds {following['score_gain']:.6f} points for ${following['additional_cost_usd']:.6f} (+{following['cost_increase_percent']:.2f}%), ${following['additional_usd_per_index_point']:.6f}/point, {following['versus_previous_marginal_multiple']:.2f}x the preceding marginal rate. Compare actual success rate, latency and review effort before paying above it."
 if not any(r['configuration_id']==rec['configuration_id'] for r in front):raise ValueError('Recommendation no longer verified')
content=json.dumps(d,indent=2,ensure_ascii=False)+'\n'
(O/'latest.json').write_text(content);(O/'snapshots'/f'{date}.json').write_text(content)
(O/'coverage.json').write_text(json.dumps(cov,separators=(',',':'),ensure_ascii=False)+'\n')
print('Refreshed',len(front),'paid +',len(d['limited_free_configurations']),'opt-in free; catalog',len(inventory),'AA registry',len(screen),'changes',changed)
