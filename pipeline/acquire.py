"""Public original-source acquisition. No credentials or generation calls required."""
import concurrent.futures, datetime, json, re, urllib.request
from html.parser import HTMLParser
from pathlib import Path
OUT=Path('run-artifacts/acquisition')
REQUIRED_EVALUATIONS=('aa-briefcase','automationbench-aa','terminalbench-4-0',
    'frontiercode-2-0','omniscience','gdp-pdf','hle-diamond',
    'critpt-v2-hard','terminal-bench-science')
# Constituent scores published on the v5.0.1 model object. These are the
# original evaluation scores, not index weights and not task costs.
V501_SCORE_PATHS={
    'aa-briefcase':('briefcaseBreakdown','overall','elo'),
    'automationbench-aa':('automationBenchPartialScore',),
    'terminalbench-4-0':('terminalBench40',),
    'frontiercode-2-0':('frontierCode20',),
    'omniscience':('omniscience',),
    'gdp-pdf':('gdpPdfAllPass',),
    'hle-diamond':('hleDiamond',),
    'critpt-v2-hard':('critptAgenticHard',),
    'terminal-bench-science':('terminalBenchScience',),
}

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def fetch(url):
    with urllib.request.urlopen(url, timeout=35) as r: text=r.read().decode()
    return text, now()
def embedded(raw):
    chunks=[]
    for m in re.finditer(r'self\.__next_f\.push\((\[.*?\])\)</script>', raw):
        try:
            item=json.loads(m[1])
            if len(item)>1 and isinstance(item[1],str): chunks.append(item[1])
        except (ValueError,IndexError): pass
    records=[]
    def walk(o):
        if isinstance(o,dict):
            records.append(o)
            for v in o.values(): walk(v)
        elif isinstance(o,list):
            for v in o: walk(v)
    for line in ''.join(chunks).splitlines():
        try: walk(json.loads(line.split(':',1)[1]))
        except (ValueError,IndexError): pass
    return records

def numeric(value):
    return isinstance(value,(int,float)) and not isinstance(value,bool)
def release_slug_of(row):
    if isinstance(row.get('releaseSlug'), str) and row['releaseSlug']: return row['releaseSlug']
    release=row.get('release')
    if isinstance(release, dict) and isinstance(release.get('slug'), str) and release['slug']: return release['slug']
    return None
def data_manifests(records):
    found={}
    for record in records:
        path,key=record.get('path'),record.get('key')
        if not (isinstance(path,str) and isinstance(key,str) and re.fullmatch(r'/data/[0-9a-f]{16,}\.txt', path) and re.fullmatch(r'[0-9a-f]{64}', key)): continue
        if path in found and found[path]!=key: raise ValueError('AA page data manifest is ambiguous')
        found[path]=key
    return [{'path':path,'key':key} for path,key in found.items()]
def normalize_configuration_index(rows):
    # A short, duplicated, or slug-less list is not the public configuration inventory.
    if not isinstance(rows, list) or len(rows)<100: return None
    slim=[]; seen=set()
    for row in rows:
        slug=row.get('slug') if isinstance(row, dict) else None
        release=release_slug_of(row) if isinstance(row, dict) else None
        if not isinstance(slug, str) or not release or slug in seen: return None
        seen.add(slug)
        slim.append({'slug':slug,'name':row.get('name'),'releaseSlug':release,'deprecated':row.get('deprecated')})
    return slim
def configuration_models(payload):
    return normalize_configuration_index(payload.get('models')) if isinstance(payload, dict) else None
def dig(obj, path):
    for key in path:
        if not isinstance(obj, dict) or key not in obj: return None
        obj=obj[key]
    return obj
def index_versions(raw):
    # "v5" and "v5.0" are equivalent display labels. "v5.0.1" is the CritPt v2
    # regrade and stays its own version. A sentence period is not part of it.
    # A page that announces more than one version fails closed.
    return {v if '.' in v else v+'.0' for v in re.findall(r'Intelligence Index v([0-9]+(?:\.[0-9]+)*)', raw)}
def original_model(record, slug):
    if record.get('slug')!=slug: return False
    if 'intelligenceIndexIsEstimated' in record: return True
    # Name-only index rows carry slug and intelligenceIndex. They are not the
    # original model object and cannot establish a measured result.
    if not isinstance(record.get('release'), dict) or not {'id','isReasoning'}<=set(record): return False
    return 'intelligenceIndexEvaluations' in record or isinstance(record.get('intelligenceIndexCostPerTask'), dict)
def legacy_evaluation_complete(record):
    rows=record.get('intelligenceIndexEvaluations')
    if not isinstance(rows, list): return False
    evaluations={row.get('slug'):row for row in rows if isinstance(row, dict)}
    return set(REQUIRED_EVALUATIONS)<=set(evaluations) and all(
        numeric(evaluations[slug].get('score')) and numeric(evaluations[slug].get('costPerTask')) and numeric(evaluations[slug].get('outputTokensPerTask'))
        for slug in REQUIRED_EVALUATIONS)
def v501_evaluation_complete(record):
    cost=record.get('intelligenceIndexCostPerTask')
    rows=cost.get('evaluations') if isinstance(cost, dict) else None
    if not isinstance(rows, list): return False
    evaluations={row.get('slug'):row for row in rows if isinstance(row, dict)}
    tokens=record.get('intelligenceIndexOutputTokensPerTask')
    return set(REQUIRED_EVALUATIONS)<=set(evaluations) and isinstance(tokens, dict) and numeric(tokens.get('output')) and all(
        numeric(evaluations[slug].get('weightedCostPerTask')) and numeric(dig(record, V501_SCORE_PATHS[slug]))
        for slug in REQUIRED_EVALUATIONS)
# Missing intelligenceIndexIsEstimated may count as measured only for an
# explicit methodology whose published evidence is complete. v5.0.1 is not
# accepted by pretending it is v5.0. Any other version fails closed.
MEASURED_WITHOUT_FLAG={
    '5.0':legacy_evaluation_complete,
    '5.0.1':lambda record: legacy_evaluation_complete(record) or v501_evaluation_complete(record),
}
def exact(slug):
    url='https://artificialanalysis.ai/models/'+slug
    versions=set()
    try:
        raw,t=fetch(url)
        versions=index_versions(raw)
        candidates=[o for o in embedded(raw) if original_model(o, slug)]
        if len(candidates)!=1 or len(versions)!=1: raise ValueError('Exact record or common index version missing')
        a=candidates[0]
        version=next(iter(versions))
        # AA removed its legacy estimation flag in November, then stopped
        # embedding intelligenceIndexEvaluations when it published v5.0.1.
        # A missing flag is never itself a measured result.
        if 'intelligenceIndexIsEstimated' not in a:
            cost_record=a.get('intelligenceIndexCostPerTask') if isinstance(a.get('intelligenceIndexCostPerTask'), dict) else {}
            cost=(cost_record.get('cost') or {}).get('total') if isinstance(cost_record.get('cost'), dict) else None
            pair=numeric(a.get('intelligenceIndex')) and numeric(cost)
            checker=MEASURED_WITHOUT_FLAG.get(version)
            complete=bool(checker and checker(a))
            if pair and not complete:
                if version not in MEASURED_WITHOUT_FLAG: raise ValueError('Missing estimation flag and unapproved index version')
                raise ValueError('Missing estimation flag and incomplete original evaluation evidence')
            if pair and complete and legacy_evaluation_complete(a): basis='complete_nine_original_evaluation_score_cost_token_records'
            elif pair and complete: basis='complete_v5_0_1_constituent_scores_weighted_costs_and_index_output_tokens'
            else: basis='unknown_no_comparable_measured_pair'
            a={**a,'intelligenceIndexIsEstimated':False if pair and complete else None,
                'estimation_status_provenance':{'source_flag_present':False,'index_version':version,'basis':basis}}
        return {**a,'source_url':url,'verified_at':t,'version':version}
    except Exception as e: return {'slug':slug,'source_url':url,'error':str(e),'parsed_index_versions':sorted(versions)}

def endpoint(mid):
    url='https://openrouter.ai/api/v1/models/'+mid+'/endpoints'
    try:
        raw,t=fetch(url);return mid,{'verified_at':t,'source_url':url,**json.loads(raw)}
    except Exception as e: return mid,{'source_url':url,'error':str(e)}

class VisibleText(HTMLParser):
    def __init__(self): super().__init__();self.parts=[];self.skip=0
    def handle_starttag(self,t,a):
        if t in ('script','style'): self.skip+=1
    def handle_endtag(self,t):
        if t in ('script','style'): self.skip=max(0,self.skip-1)
    def handle_data(self,t):
        if not self.skip: self.parts.append(t)
def document(url):
    try:
        raw,t=fetch(url);p=VisibleText();p.feed(raw);text=re.sub(r'\s+',' ',' '.join(p.parts))
        if len(text)<200: raise ValueError('Insufficient source text')
        return {'url':url,'verified_at':t,'status':'opened_successfully','text':text}
    except Exception as e: return {'url':url,'status':'failed','error':str(e)}

def save(name,data): (OUT/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    base=json.loads(Path('latest.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        fa=pool.submit(fetch,'https://artificialanalysis.ai/models/releases')
        fc=pool.submit(fetch,'https://openrouter.ai/api/v1/models')
        raw,rt=fa.result();reg={a['slug']:a for a in embedded(raw) if all(k in a for k in ('slug','creator','releaseDate','costPerTaskRange'))}
        raw,ct=fc.result();catalog={'verified_at':ct,**json.loads(raw)}
    if not reg or not catalog.get('data'): raise ValueError('Empty public discovery sources')
    save('registry',{'verified_at':rt,'releases':list(reg.values())});save('catalog',catalog)
    # The default catalog is text-only. Inventory every output modality and
    # decisions separately without treating these models as text benchmarks.
    for label,query in [('all-output-catalog','all'),('decision-catalog','decisions')]:
        url='https://openrouter.ai/api/v1/models?output_modalities='+query
        try:
            raw,verified=fetch(url);save(label,{'source_url':url,'verified_at':verified,**json.loads(raw)})
        except Exception as error:save(label,{'source_url':url,'error':str(error)})
    slugs={r['benchmark_source_url'].split('/')[-1] for r in base['evaluated_configurations'] if r.get('benchmark_source_url')}
    slugs|={r['benchmark_source_url'].split('/')[-1] for r in base.get('limited_free_configurations',[])}
    slugs|={r['AA_model_slug'] for r in base.get('excluded_or_pending',[]) if r.get('AA_model_slug')}
    slugs|={'step-5','north-mini-code','command-a-plus','k2-horizon-375b-a23b','ling-3-0-tiny','gemini-4-argon'}
    templates_path=Path('pipeline/additional-request-templates.json')
    templates=json.loads(templates_path.read_text()) if templates_path.exists() else []
    slugs|={r['benchmark_source_url'].split('/')[-1] for r in templates}
    old_releases={r['AA_release_slug'] for r in json.loads(Path('coverage.json').read_text())['AA_release_screening']}
    old_ids={r['model_id'] for r in json.loads(Path('coverage.json').read_text())['catalog_models']}
    normalize=lambda name: re.sub(r'[^a-z0-9]', '', name.lower())
    newly_listed_names={normalize(m['name'].split(':',1)[-1]) for m in catalog['data'] if m['id'] not in old_ids}
    # A newly observed gateway listing can refer to an older AA release.
    # Name matching discovers evidence only; it never authorizes routing.
    for r in reg.values():
        href=r.get('href','')
        if normalize(r['name']) in newly_listed_names and href.startswith('/models/') and not href.startswith('/models/releases/'):
            slugs.add(href.split('/')[-1])
    # New single-configuration releases use their original registry href. No invented effort mapping.
    for r in reg.values():
        href=r.get('href','')
        if r['slug'] not in old_releases and href.startswith('/models/') and not href.startswith('/models/releases/'):
            slugs.add(href.split('/')[-1])
    ids={m['openrouter_model_id'] for m in base['models']}|{r['openrouter_model_id'] for r in base.get('limited_free_configurations',[])}
    ids|={r['openrouter_model_id'] for r in templates}
    urls={m['provider_documentation_url'] for m in base['models'] if m.get('provider_documentation_url')}
    urls|={m['provider_pricing_url'] for m in base['models'] if m.get('provider_pricing_url')}
    policies_path=Path('pipeline/additional-model-policies.json')
    policies=json.loads(policies_path.read_text()) if policies_path.exists() else []
    urls|={r['provider_documentation_url'] for r in policies}
    urls|={u for s in base['subscription_recommendations']['services'] for u in s['sources']}
    urls|={'https://openrouter.ai/docs/guides/best-practices/reasoning-tokens','https://openrouter.ai/docs/guides/routing/provider-selection','https://artificialanalysis.ai/articles/claude-haiku-5-5','https://artificialanalysis.ai/articles/claude-sonnet-5-5','https://artificialanalysis.ai/changelog','https://artificialanalysis.ai/methodology/intelligence-benchmarking','https://mimo.mi.com/docs/en-US/updates/model','https://platform.claude.com/docs/en/about-claude/pricing','https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback'}
    urls|={'https://ai.google.dev/gemini-api/docs/changelog','https://ai.google.dev/gemini-api/docs/latest-model','https://platform.kimi.ai/docs/guide/kimi-k3-1-pro-quickstart','https://www.kimi.ai/blog/kimi-k3-1-pro','https://platform.kimi.ai/docs/pricing/chat','https://artificialanalysis.ai/articles/kimi-k3-1-pro-launch-benchmarks'}
    urls|={'https://openai.com/index/introducing-gpt-6-1-terra/','https://artificialanalysis.ai/articles/gpt-6-1-terra-pushes-the-cost-efficiency-frontier'}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        metrics=list(pool.map(exact,sorted(slugs)))
        endpoints=dict(pool.map(endpoint,sorted(ids)))
        docs=list(pool.map(document,sorted(urls)))
    save('metrics',metrics);save('endpoints',endpoints);save('doc-checks',docs)
    required={r['benchmark_source_url'] for r in base['evaluated_configurations'] if r.get('eligible_for_frontier')}
    failures=[a for a in metrics if a.get('error') and a['source_url'] in required]
    failure_path=OUT/'required-failures.json'
    if failures:
        details=[{'slug':a['slug'],'source_url':a['source_url'],'error':a['error'],'parsed_index_versions':a.get('parsed_index_versions')} for a in failures]
        failure_path.write_text(json.dumps(details,indent=2)+'\n')
        kinds=sorted({(a['error'],tuple(a.get('parsed_index_versions') or ())) for a in failures})
        raise ValueError('Required exact benchmark acquisition failed: '+str([a['slug'] for a in failures])+'; error_versions='+str(kinds))
    elif failure_path.exists(): failure_path.unlink()
    print(f"Acquired {len(catalog['data'])} gateway entries, {len(reg)} releases, {len(metrics)} exact records; document failures remain explicitly unverified",flush=True)
if __name__=='__main__': main()
