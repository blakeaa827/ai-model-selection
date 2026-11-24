"""Discover every public AA configuration; collect exact active records, never infer routes."""
import concurrent.futures, hashlib, json, re, subprocess
from pathlib import Path
from acquire import fetch, embedded, exact, document, data_manifests, normalize_configuration_index, configuration_models

OUT = Path('run-artifacts/acquisition')

DECRYPT = r'''
import {createDecipheriv, createHash} from 'node:crypto';
import {gunzipSync} from 'node:zlib';
const manifests = JSON.parse(await new Response(process.stdin).text());
const out = [];
for (const item of manifests) {
  const response = await fetch('https://artificialanalysis.ai' + item.path);
  if (!response.ok) throw new Error('page data HTTP ' + response.status);
  const buf = Buffer.from(await response.arrayBuffer());
  const key = Buffer.from(item.key, 'hex');
  if (key.length !== 32 || buf.length < 17) throw new Error('page data key or body');
  const iv = createHash('sha256').update(key).digest().subarray(0, 12);
  const decipher = createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(buf.subarray(buf.length - 16));
  const plain = Buffer.concat([decipher.update(buf.subarray(0, buf.length - 16)), decipher.final()]);
  out.push(JSON.parse(gunzipSync(plain).toString('utf8')));
}
process.stdout.write(JSON.stringify(out));
'''

def open_page_data(manifests):
    # The models index now ships its configuration list as a public AES-GCM
    # blob. The key is on the same page the browser uses. This is not an API
    # credential, and a blob that does not decrypt is not an inventory.
    if not manifests: return []
    proc = subprocess.run(['node', '--input-type=module', '-e', DECRYPT], input=json.dumps(manifests), text=True, capture_output=True, timeout=60)
    if proc.returncode != 0: raise ValueError('AA page data could not be opened: ' + proc.stderr[-400:])
    return json.loads(proc.stdout)

def configuration_index(raw):
    objects = embedded(raw)
    inline = [x['models'] for x in objects if isinstance(x.get('models'), list) and isinstance(x.get('releases'), list)]
    if len(inline) > 1: raise ValueError('AA public configuration inventory is ambiguous')
    if inline:
        index = normalize_configuration_index(inline[0])
    else:
        opened = open_page_data(data_manifests(objects))
        inventories = [models for payload in opened if (models := configuration_models(payload))]
        if len(inventories) != 1: raise ValueError('AA public configuration inventory is empty, truncated or duplicated')
        index = inventories[0]
    if not index: raise ValueError('AA public configuration inventory is empty, truncated or duplicated')
    return index

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    config = json.loads(Path('pipeline/workload-profiles.json').read_text())
    raw, checked = fetch('https://artificialanalysis.ai/models')
    index = configuration_index(raw)
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
