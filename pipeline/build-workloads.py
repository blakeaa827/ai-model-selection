"""Separate measured cost-capability frontiers. No cross-benchmark cost borrowing."""
import copy, datetime, json, math, re
from collections import Counter
from pathlib import Path

R=Path('run-artifacts/acquisition'); O=Path('run-artifacts/report')
load=lambda p:json.loads(Path(p).read_text())
save=lambda p,x:Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

def frontier(rows):
    unique={}
    for r in sorted(rows,key=lambda x:x['configuration_id']):
        key=(r['score'],r['benchmark_task_cost_usd'])
        unique.setdefault(key,r)
    rows=list(unique.values())
    kept=sorted([copy.deepcopy(a) for a in rows if not any(b['score']>=a['score'] and b['benchmark_task_cost_usd']<=a['benchmark_task_cost_usd'] and (b['score']>a['score'] or b['benchmark_task_cost_usd']<a['benchmark_task_cost_usd']) for b in rows)],key=lambda r:r['score'])
    for i,r in enumerate(kept):
        p=kept[i-1] if i else None
        r.update(minimum_score_exclusive=p['score'] if p else None,maximum_score_inclusive=r['score'],minimum_budget_inclusive=r['benchmark_task_cost_usd'],maximum_budget_exclusive=kept[i+1]['benchmark_task_cost_usd'] if i+1<len(kept) else None,marginal=None)
        if p:
            gain=r['score']-p['score']; added=r['benchmark_task_cost_usd']-p['benchmark_task_cost_usd']; rate=added/gain
            previous_rate=(p.get('marginal') or {}).get('additional_usd_per_score_point')
            r['marginal']={'previous_configuration_id':p['configuration_id'],'score_gain':gain,'additional_cost_usd':added,'cost_increase_percent':100*added/p['benchmark_task_cost_usd'] if p['benchmark_task_cost_usd'] else None,'additional_usd_per_score_point':rate,'versus_previous_marginal_multiple':rate/previous_rate if previous_rate else None}
    return kept

def recommendations(rows):
    knees=[]
    for i,r in enumerate(rows):
        m=r.get('marginal') or {}
        if (m.get('versus_previous_marginal_multiple') or 0)>=3 and (m.get('cost_increase_percent') or 0)>=50:
            knees.append(i-1)
    result={'floor':None,'ceiling':None,'status':'no_clear_value_knee','method':'First >=3x adjacent marginal dollars/score-point jump with >=50% task-cost increase; next such cliff defines the optional ceiling. Descriptive only; benchmark intervals need not have equal practical value. No raw cost/score ratios.'}
    if knees:
        result['status']='conditional_heuristic'
        for role,index in [('floor',knees[0]),('ceiling',knees[1] if len(knees)>1 else knees[0])]:
            r=rows[index];n=rows[index+1]['marginal']
            result[role]={'configuration_id':r['configuration_id'],'score':r['score'],'benchmark_task_cost_usd':r['benchmark_task_cost_usd'],'rationale':f"The next step adds {n['score_gain']} score points for ${n['additional_cost_usd']} ({n['cost_increase_percent']}%); marginal cost rises {n['versus_previous_marginal_multiple']}x. Conditional on this benchmark, workload and verified subset; not a universal default."}
    return result,[{'after_configuration_id':rows[i]['configuration_id'],'next_configuration_id':rows[i+1]['configuration_id'],'kind':'value_knee' if j==0 else 'cost_cliff',**rows[i+1]['marginal']} for j,i in enumerate(knees)]

def route(r,a,general,catalog,eps,checks):
    mid=r['openrouter_model_id'];model=catalog.get(mid)
    if not model or model['canonical_slug']!=r['openrouter_canonical_slug']:raise ValueError('catalog_revision_mismatch')
    if a.get('deprecated') or a.get('intelligenceIndexIsEstimated'):raise ValueError('deprecated_or_estimated')
    if 'fallback' in a['name'].lower() or 'router' in a['name'].lower():raise ValueError('multi_model_or_fallback_configuration')
    if not r.get('eligible_for_frontier',True):raise ValueError('original_configuration_eligibility_not_verified')
    if r.get('benchmark_cost_status','complete_as_published')!='complete_as_published':raise ValueError('provisional_task_cost')
    policy=next((m for m in general['models'] if m['openrouter_model_id']==mid),None)
    if not policy or policy.get('provider_documentation_url') not in checks:raise ValueError('provider_control_documentation_not_reverified')
    template=next((x for x in general['frontier']+general.get('limited_free_configurations',[]) if x['openrouter_model_id']==mid),None)
    tag=template['request']['provider']['only'][0] if template else {'openai':'openai','anthropic':'anthropic','google':'google-ai-studio','x-ai':'xai','xiaomi':'xiaomi/fp8'}.get(mid.split('/')[0])
    er=eps.get(mid,{})
    ep=next((e for e in er.get('data',{}).get('endpoints',[]) if e['tag']==tag),None)
    if not ep or ep['status']!=0 or ep['model_id']!=mid or model['canonical_slug'] not in ep['name']:raise ValueError('standard_endpoint_revision_unverified')
    if model.get('expiration_date') and model['expiration_date']<=general['report_date']:raise ValueError('expired')
    effort=r.get('effort')
    rc=(template or {}).get('reasoning_control') or r.get('reasoning_control')
    if effort is not None:
        exact_effort=(a.get('effort') or {}).get('slug')==effort or (effort=='none' and a.get('isReasoning') is False)
        if not exact_effort or effort not in model.get('reasoning',{}).get('supported_efforts',[]):raise ValueError('benchmark_effort_mismatch')
        if 'reasoning_effort' not in ep['supported_parameters']:raise ValueError('endpoint_effort_unsupported')
        reasoning={'effort':effort}
    elif rc and rc.get('type')=='enabled' and rc.get('verified_native_setting'):
        if rc.get('source') not in checks:raise ValueError('native_control_source_not_reverified')
        reasoning={'enabled':rc['value']}
    else:raise ValueError('native_reasoning_control_unverified')
    if 'reasoning' not in ep['supported_parameters']:raise ValueError('endpoint_reasoning_unsupported')
    prior_quant=(template or {}).get('endpoint_verification',{}).get('quantization')
    if prior_quant not in (None,'unknown') and ep.get('quantization')!=prior_quant:raise ValueError('quantization_mismatch')
    if float(ep['pricing']['prompt'])!=float(model['pricing']['prompt']) or float(ep['pricing']['completion'])!=float(model['pricing']['completion']):raise ValueError('nonstandard_pricing_tier')
    return {'configuration_id':r['configuration_id'],'model_name':a['name'],'openrouter_model_id':mid,'openrouter_canonical_slug':model['canonical_slug'],'effort':effort,
            'reasoning_control':rc if effort is None else {'type':'effort','value':effort},'request':{'model':mid,'reasoning':reasoning,'provider':{'only':[tag],'require_parameters':True,'allow_fallbacks':False}},
            'api_endpoint':'https://openrouter.ai/api/v1/responses' if mid.startswith('openai/') else 'https://openrouter.ai/api/v1/chat/completions',
            'benchmark_source_url':a['source_url'],'benchmark_verified_at':a['verified_at'],'openrouter_verified_at':general['coverage_inventory']['catalog_verified_at'],
            'endpoint_verification':{'verified_at':er['verified_at'],'metadata_url':er['source_url'],'provider_tag':tag,'quantization':ep.get('quantization'),'status':ep['status'],'supported_parameters':ep['supported_parameters']},
            'provider_documentation_verified_at':checks[policy['provider_documentation_url']]['verified_at'],
            'context_window_tokens':model.get('context_length'),'input_modalities':model.get('architecture',{}).get('input_modalities',[]),
            'configuration_settings':(template or {}).get('configuration_settings',{'sampling':'AA/provider defaults; no invented temperature or top_p','output_budget':'Preserve sufficient reasoning plus answer budget and reasoning details across tool turns.'}),
            'api_call_tested':False,'eligible_for_frontier':True,'benchmark_score_is_estimated':False,'benchmark_cost_status':'complete_as_published'}

def main():
    cfg=load('pipeline/workload-profiles.json'); general=load(O/'latest.json'); acq=load(R/'workloads.json')
    cat={m['id']:m for m in load(R/'catalog.json')['data']}; eps=load(R/'endpoints.json')
    metrics={a['slug']:a for a in acq['active_exact_records'] if not a.get('error')}
    # Exact records explicitly acquired by the general lane also include free routes.
    metrics.update({a['slug']:a for a in load(R/'metrics.json') if not a.get('error')})
    checks={r['url']:r for r in general['source_checks'] if r.get('status')=='opened_successfully'}
    checks.update({r['url']:r for r in acq['document_checks'] if r['status']=='opened_successfully'})
    mappings={r['benchmark_source_url'].split('/')[-1]:r for r in general['evaluated_configurations']+general.get('limited_free_configurations',[])}
    profiles=[]
    for p in cfg['profiles']:
        source='https://artificialanalysis.ai/evaluations/'+p['evaluation_slug'];doc=checks.get(source)
        version_ok=general['benchmark']['version']==cfg['intelligence_methodology_version']
        method=checks.get(cfg['methodology_url'],{})
        verified_doc=bool(doc and p['page_signature'] in doc.get('text','') and ('Intelligence Index v'+cfg['intelligence_methodology_version']) in method.get('text',''))
        profile={**p,'status':'ready' if version_ok and verified_doc else 'pending_methodology_verification','source_url':source,
                 'methodology_version':general['benchmark']['version'],'methodology_url':cfg['methodology_url'],
                 'methodology_verified_at':checks.get(cfg['methodology_url'],{}).get('verified_at'),
                 'source_verified_at':doc.get('verified_at') if doc else None,'cost_metric':'USD_per_'+p['evaluation_slug']+'_task',
                 'cost_basis':'AA evaluation-specific costPerTask from observed contestant token use and published prices; excludes unreported tools, judges, infrastructure and supervision. Not Intelligence Index weighted cost or an OpenRouter invoice estimate.',
                 'score_is_request_success_probability':False,'coverage_status':'all_public_configurations_screened_routing_verification_incomplete',
                 'frontier':[],'limited_free_configurations':[],'evaluated_configurations':[],'breakpoints':[],'recommendations':{'floor':None,'ceiling':None,'status':'pending'},'pending_candidates':[]}
        paid=[];free=[]
        for slug,a in metrics.items():
            ev=next((v for v in a.get('intelligenceIndexEvaluations',[]) if v['slug']==p['evaluation_slug']),None)
            if not ev or not isinstance(ev.get('score'),(int,float)) or not isinstance(ev.get('costPerTask'),(int,float)):
                profile['pending_candidates'].append({'AA_slug':slug,'status':'missing_comparable_score_or_evaluation_task_cost'});continue
            pending={'AA_slug':slug,'model_name':a['name'],'source_url':a['source_url'],'verified_at':a['verified_at'],'score':ev['score']*p['score_multiplier'],'source_raw_score':ev['score'],'benchmark_task_cost_usd':ev['costPerTask']}
            r=mappings.get(slug)
            if not r:
                profile['pending_candidates'].append({**pending,'status':'exact_revision_effort_provider_route_not_verified'});continue
            try:
                if profile['status']!='ready':raise ValueError('profile_methodology_unverified')
                if a['version']!=cfg['intelligence_methodology_version']:raise ValueError('methodology_version_mismatch')
                row=route(r,a,general,cat,eps,checks)
                if not set(p['required_parameters'])<=set(row['endpoint_verification']['supported_parameters']):raise ValueError('required_workload_parameters_unsupported')
                row.update(score=ev['score']*p['score_multiplier'],source_raw_score=ev['score'],score_unit=p['score_unit'],benchmark_task_cost_usd=ev['costPerTask'],
                           benchmark_id=p['evaluation_slug'],benchmark_version=p['benchmark_version'],harness_id=p['harness_id'],
                           benchmark_output_tokens_per_task=ev.get('outputTokensPerTask'),benchmark_time_per_task_seconds=ev.get('timePerTask'),
                           time_basis='AA source estimate from token usage and model performance; not measured production wall time or p95 latency')
                if row['benchmark_task_cost_usd']<0:raise ValueError('negative_cost')
                if row['benchmark_task_cost_usd']==0:
                    if not r.get('requires_opt_in'):raise ValueError('zero_cost_not_verified_limited_free_lane')
                    row.update(requires_opt_in=True,route_limitations=r.get('route_limitations','First-party free route; rate limits and quota; managed quantization may be unknown.'))
                    free.append(row)
                else:paid.append(row)
                profile['evaluated_configurations'].append(copy.deepcopy(row))
            except (ValueError,KeyError) as error:
                profile['pending_candidates'].append({**pending,'status':str(error)})
        profile['frontier']=frontier(paid);profile['limited_free_configurations']=frontier(free)
        if profile['frontier']:
            profile['recommendations'],profile['breakpoints']=recommendations(profile['frontier'])
        elif profile['status']=='ready':profile['status']='pending_verified_pairs'
        profile['coverage']={'source_records_screened':len(metrics),'eligible_configurations':len(paid)+len(free),'paid_frontier_count':len(profile['frontier']),'pending_status_counts':dict(Counter(x['status'] for x in profile['pending_candidates']))}
        ids={r['configuration_id'] for r in profile['frontier']+profile['limited_free_configurations']}
        for r in profile['evaluated_configurations']:r['pareto_dominated']=r['configuration_id'] not in ids
        profiles.append(profile)
    coding=acq['coding_agents']; systems=[]
    for r in coding['variants']:
        score=r.get('indexScore');cost=r.get('mean',{}).get('costUsd')
        reasons=[]
        if score is None or cost is None:reasons.append('missing_measured_score_or_cost')
        if r.get('hasTieredPricing'):reasons.append('tiered_cost_completeness_requires_verification')
        if r.get('isUnavailable'):reasons.append('unavailable')
        systems.append({'configuration_id':'aa-coding-agent:'+r['id'],'label':r['displayLabel'],'agent':r['agentName'],'model_label':r['display']['model'],
                        'score':score*100 if score is not None else None,'source_raw_score':score,'benchmark_task_cost_usd':cost,
                        'harness_versions':r.get('versions'),'fallback_attempts':r.get('safety',{}).get('fallbackAttemptCount'),
                        'refusal_rate':r.get('safety',{}).get('rate'),'agent_wall_time_seconds':r.get('mean',{}).get('agentWallTimeSec'),
                        'benchmark_version':coding.get('version'),'source_url':coding['source_url'],'verified_at':coding.get('verified_at'),
                        'request':None,'openrouter_actionable':False,'subscription_task_cost_usd':None,
                        'status':'measured_agent_system' if not reasons else 'pending','reasons':reasons})
    system_frontier=frontier([r for r in systems if r['status']=='measured_agent_system'])
    codemethod=coding.get('methodology_check',{})
    if codemethod.get('status')!='opened_successfully':system_frontier=[]
    previous=load('workloads.json') if Path('workloads.json').exists() else None
    previous_profiles={p['id']:p for p in previous['profiles']} if previous else {}
    signature=lambda p:[(r['configuration_id'],r['score'],r['benchmark_task_cost_usd']) for r in p.get('frontier',[])]
    changed_profiles=[p['id'] for p in profiles if signature(p)!=signature(previous_profiles.get(p['id'],{}))]
    result={'schema_version':'1.0.0','report_date':general['report_date'],'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'freshness':copy.deepcopy(general['freshness']),'general_report':'latest.json','general_intelligence_index_version':general['benchmark']['version'],
            'selection_policy':{'scope':'Best observed among exact verified configurations, not proof of global optimality. All catalog entries and AA configurations are inventoried; routing correspondence is incomplete.',
                                'unknown_workload':'reject; explicit general-lane selection remains available','unverified_or_stale':'reject_without_substitution',
                                'capability_scores':'Benchmark-specific; no direct conversion between benchmarks, Elo, general index or Jev probabilities.',
                                'free_routes':'Separate explicit-opt-in lane; never default production routing.'},
            'coverage':{'openrouter_model_count':len(cat),'AA_configuration_count':len(acq['configuration_index']),'active_exact_records_checked':len(acq['active_exact_records']),
                        'configuration_index_verified_at':acq['configuration_index_verified_at'],'catalog_verified_at':general['coverage_inventory']['catalog_verified_at'],
                        'incomplete_exact_record_retrievals':[{'AA_slug':r['slug'],'error':r['error']} for r in acq['active_exact_records'] if r.get('error')]},
            'profiles':profiles,'pending_profiles':cfg['pending_profiles'],
            'coding_agent_systems':{'benchmark':'AA Coding Agent Index','version':coding.get('version'),'verified_at':coding.get('verified_at'),
                                    'source_url':coding['source_url'],'methodology_url':'https://artificialanalysis.ai/methodology/coding-agents-benchmarking',
                                    'methodology_verified_at':codemethod.get('verified_at'),'status':'measured_system_comparisons' if system_frontier else 'pending',
                                    'cost_basis':'Published pay-per-token API cost for each complete tested agent system. Not subscription consumption or a standalone OpenRouter model request.',
                                    'frontier':system_frontier,'systems':systems,'request':None,'openrouter_actionable':False},
            'jev':{'status':'not_integrated_not_calibrated','predicted_success_probability':None,
                   'guidance':'Use workload, task features and exact candidate configuration to estimate success. Calibrate against held-out observed outcomes; never convert benchmark score directly to probability. No Jev calls or production evaluations run by this public-data refresh.'},
            'changes_since_previous':{'previous_report_date':previous.get('report_date') if previous else None,'initial_workload_release':previous is None,
                                      'changed_profiles':changed_profiles},
            'source_checks':[{'url':r['url'],'verified_at':r['verified_at'],'status':r['status']} for r in acq['document_checks'] if r['status']=='opened_successfully'],
            'no_paid_generation_calls':True}
    save(O/'workloads.json',result)
    coverage=load(O/'coverage.json')
    coverage['workload_coverage']={'file':'workloads.json','AA_configuration_count':len(acq['configuration_index']),'active_exact_records_checked':len(acq['active_exact_records']),'configuration_index_verified_at':acq['configuration_index_verified_at'],'note':'All public configuration names screened; exact active records acquired. Each workload evaluates all verified mappings, including configurations dominated in the general chart. Unknown mappings remain pending.'}
    for model in coverage['catalog_models']:
        model['workloads']={p['id']:('verified_workload_configuration' if any(r['openrouter_model_id']==model['model_id'] for r in p['evaluated_configurations']) else 'pending_exact_workload_benchmark_or_route') for p in profiles}
    save(O/'coverage.json',coverage)
    (O/'workloads/snapshots').mkdir(parents=True,exist_ok=True)
    save(O/'workloads/snapshots'/f"{result['report_date']}.json",result)
    general['workload_selection']={'file':'workloads.json','report':'workloads.md','schema':'workloads.schema.json','selector':'select-workload.mjs','schema_version':'1.0.0','checked_at':result['checked_at'],
                                   'ready_profiles':[p['id'] for p in profiles if p['status']=='ready'],'pending_profiles':[p['id'] for p in cfg['pending_profiles']],
                                   'routing_coverage':'partial_exact_configuration_verification; all catalog entries screened','Jev_status':'not_integrated_not_calibrated'}
    save(O/'latest.json',general);save(O/'snapshots'/f"{general['report_date']}.json",general)
    print('Built independent workload frontiers:',{p['id']:len(p['frontier']) for p in profiles},flush=True)

if __name__=='__main__':main()
