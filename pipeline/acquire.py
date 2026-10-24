"""Public original-source acquisition. No credentials or generation calls required."""
import concurrent.futures, datetime, json, re, urllib.request
from html.parser import HTMLParser
from pathlib import Path
OUT=Path('run-artifacts/acquisition')

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

def exact(slug):
    url='https://artificialanalysis.ai/models/'+slug
    try:
        raw,t=fetch(url)
        candidates=[o for o in embedded(raw) if o.get('slug')==slug and 'intelligenceIndexIsEstimated' in o]
        versions=set(re.findall(r'Intelligence Index v([0-9.]+)', raw))
        if not candidates or len(versions)!=1: raise ValueError('Exact record or common index version missing')
        a=candidates[0]
        return {**a,'source_url':url,'verified_at':t,'version':versions.pop()}
    except Exception as e: return {'slug':slug,'source_url':url,'error':str(e)}

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
    slugs={r['benchmark_source_url'].split('/')[-1] for r in base['evaluated_configurations'] if r.get('benchmark_source_url')}
    slugs|={r['benchmark_source_url'].split('/')[-1] for r in base.get('limited_free_configurations',[])}
    slugs|={r['AA_model_slug'] for r in base.get('excluded_or_pending',[]) if r.get('AA_model_slug')}
    slugs|={'step-5','north-mini-code','command-a-plus','k2-horizon-375b-a23b','ling-3-0-tiny','gemini-4-argon'}
    old_releases={r['AA_release_slug'] for r in json.loads(Path('coverage.json').read_text())['AA_release_screening']}
    # New single-configuration releases use their original registry href. No invented effort mapping.
    for r in reg.values():
        href=r.get('href','')
        if r['slug'] not in old_releases and href.startswith('/models/') and not href.startswith('/models/releases/'):
            slugs.add(href.split('/')[-1])
    ids={m['openrouter_model_id'] for m in base['models']}|{r['openrouter_model_id'] for r in base.get('limited_free_configurations',[])}
    urls={m['provider_documentation_url'] for m in base['models'] if m.get('provider_documentation_url')}
    urls|={m['provider_pricing_url'] for m in base['models'] if m.get('provider_pricing_url')}
    urls|={u for s in base['subscription_recommendations']['services'] for u in s['sources']}
    urls|={'https://openrouter.ai/docs/guides/best-practices/reasoning-tokens','https://openrouter.ai/docs/guides/routing/provider-selection','https://artificialanalysis.ai/articles/claude-haiku-5-5','https://artificialanalysis.ai/articles/claude-sonnet-5-5','https://artificialanalysis.ai/changelog','https://artificialanalysis.ai/methodology/intelligence-benchmarking','https://mimo.mi.com/docs/en-US/updates/model','https://platform.claude.com/docs/en/about-claude/pricing','https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback'}
    urls|={'https://ai.google.dev/gemini-api/docs/changelog','https://ai.google.dev/gemini-api/docs/latest-model','https://platform.kimi.ai/docs/guide/kimi-k3-1-pro-quickstart','https://www.kimi.ai/blog/kimi-k3-1-pro','https://platform.kimi.ai/docs/pricing/chat','https://artificialanalysis.ai/articles/kimi-k3-1-pro-launch-benchmarks'}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        metrics=list(pool.map(exact,sorted(slugs)))
        endpoints=dict(pool.map(endpoint,sorted(ids)))
        docs=list(pool.map(document,sorted(urls)))
    save('metrics',metrics);save('endpoints',endpoints);save('doc-checks',docs)
    required={r['benchmark_source_url'] for r in base['evaluated_configurations'] if r.get('eligible_for_frontier')}
    failures=[a for a in metrics if a.get('error') and a['source_url'] in required]
    if failures: raise ValueError('Required exact benchmark acquisition failed: '+str([a['slug'] for a in failures]))
    print(f"Acquired {len(catalog['data'])} gateway entries, {len(reg)} releases, {len(metrics)} exact records; document failures remain explicitly unverified",flush=True)
if __name__=='__main__': main()
