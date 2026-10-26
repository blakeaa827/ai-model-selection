"""Discover every public AA configuration; collect exact active records, never infer routes."""
import concurrent.futures, hashlib, json, re
from pathlib import Path
from acquire import fetch, embedded, exact, document

OUT = Path('run-artifacts/acquisition')

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    config = json.loads(Path('pipeline/workload-profiles.json').read_text())
    raw, checked = fetch('https://artificialanalysis.ai/models')
    objects = embedded(raw)
    index = next(x for x in objects if isinstance(x.get('models'), list) and isinstance(x.get('releases'), list))['models']
    if len(index) < 100 or len({x['slug'] for x in index}) != len(index):
        raise ValueError('AA public configuration inventory is empty, truncated or duplicated')
    registry = {r['slug']: r for r in json.loads((OUT/'registry.json').read_text())['releases']}
    existing = {r['slug']: r for r in json.loads((OUT/'metrics.json').read_text()) if not r.get('error')}
    active = [x for x in index if not registry.get(x['releaseSlug'], {}).get('isDeprecated', False)]
    missing = sorted({x['slug'] for x in active} - set(existing))
    print(f'Workload discovery: {len(index)} AA configurations; {len(active)} nondeprecated; {len(missing)} additional exact records', flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        fresh = list(pool.map(exact, missing))
    for r in fresh:
        existing[r['slug']] = r
    records = [existing[x['slug']] for x in active]
    urls = {config['methodology_url']} | {'https://artificialanalysis.ai/evaluations/'+p['evaluation_slug'] for p in config['profiles']}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        checks = list(pool.map(document, sorted(urls)))
    coding_url = 'https://artificialanalysis.ai/agents/coding-agents'
    try:
        coding_raw, coding_checked = fetch(coding_url)
        variants = {x['id']: x for x in embedded(coding_raw) if x.get('agentName') and isinstance(x.get('evals'), list) and 'indexScore' in x}
        versions = set(re.findall(r'Coding Agent Index v([0-9]+\.[0-9]+)', coding_raw))
        if not variants or len(versions) != 1:
            raise ValueError('Coding Agent Index version or exact variants missing')
        method = document('https://artificialanalysis.ai/methodology/coding-agents-benchmarking')
        coding = {'source_url':coding_url, 'verified_at':coding_checked, 'version':versions.pop(), 'variants':list(variants.values()), 'methodology_check':method}
    except Exception as error:
        coding = {'source_url':coding_url, 'error':str(error), 'variants':[]}
    result = {'configuration_index_url':'https://artificialanalysis.ai/models', 'configuration_index_verified_at':checked,
              'configuration_index_sha256':hashlib.sha256(raw.encode()).hexdigest(), 'configuration_index':index,
              'active_exact_records':records, 'document_checks':checks, 'coding_agents':coding}
    (OUT/'workloads.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(f'Acquired {sum(not r.get("error") for r in records)} workload model records and {len(coding["variants"])} distinct coding-agent systems', flush=True)

if __name__ == '__main__':
    main()
