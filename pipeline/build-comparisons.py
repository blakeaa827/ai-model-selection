"""Publish every active AA configuration alongside the strictly verified routing lane.

The comparison is an evidence inventory, not a source of executable requests.
Never infer a model revision, provider, effort setting, or task cost from a name.
"""
import json
import re
from pathlib import Path

ACQ = Path('run-artifacts/acquisition')
OUT = Path('run-artifacts/report')


def load(path):
    return json.loads(Path(path).read_text())


def normalize(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())


def build(records, catalog, report):
    known = {row['benchmark_source_url']: row for row in report['evaluated_configurations']}
    known.update({row['benchmark_source_url']: row for row in report.get('limited_free_configurations', [])})
    callable_rows = {row['configuration_id']: row for row in report['frontier'] + report.get('limited_free_configurations', [])}
    catalog_names = {}
    for model in catalog['data']:
        name = model['name'].split(': ', 1)[-1]
        name = re.sub(r' \((?:batch|free)\)$', '', name, flags=re.I)
        catalog_names.setdefault(normalize(name), []).append(model['id'])

    rows = []
    for record in records:
        release = record.get('release') or {}
        source = record.get('source_url', 'https://artificialanalysis.ai/models/' + record['slug'])
        match = known.get(source)
        pair = record.get('intelligenceIndexCostPerTask') or {}
        cost = (pair.get('cost') or {}).get('total')
        score = record.get('intelligenceIndex')
        fallback = 'fallback' in record.get('name', '').lower() or 'router' in record.get('name', '').lower()
        measured = not record.get('error') and not record.get('deprecated') and not record.get('intelligenceIndexIsEstimated') and isinstance(score, (int, float)) and isinstance(cost, (int, float))
        if record.get('error'):
            status = 'exact_record_retrieval_failed'
        elif record.get('deprecated'):
            status = 'deprecated'
        elif record.get('intelligenceIndexIsEstimated'):
            status = 'estimated_score'
        elif score is None or cost is None:
            status = 'missing_common_score_or_measured_task_cost'
        elif fallback:
            status = 'measured_multi_model_or_fallback_not_single_call'
        elif match and match.get('configuration_id') in callable_rows:
            status = 'verified_callable_frontier'
        elif match and match.get('eligible_for_frontier'):
            status = 'recorded_mapping_dominated_route_not_reverified'
        else:
            status = 'measured_route_or_configuration_unverified'
        row = {
            'AA_slug': record['slug'], 'AA_label': record.get('name'),
            'AA_release_slug': release.get('slug'), 'AA_release_name': release.get('name'),
            'reasoning_effort_as_measured': (record.get('effort') or {}).get('slug'),
            'is_reasoning_as_measured': record.get('isReasoning'),
            'intelligence_score': score, 'weighted_AA_task_cost_usd': cost,
            'benchmark_version': record.get('version'), 'source_url': source,
            'source_verified_at': record.get('verified_at'), 'score_is_estimated':record.get('intelligenceIndexIsEstimated'),
            'status': status, 'measured_pair': measured,
            'candidate_openrouter_ids_unverified': sorted(catalog_names.get(normalize(release.get('name', '')), [])),
            'verified_openrouter_model_id': match['openrouter_model_id'] if status == 'verified_callable_frontier' else None,
            'verified_configuration_id': match['configuration_id'] if status == 'verified_callable_frontier' else None,
            'request': callable_rows[match['configuration_id']]['request'] if status == 'verified_callable_frontier' else None,
        }
        if match and match.get('benchmark_cost_status') != 'complete_as_published':
            row['benchmark_cost_status'] = match.get('benchmark_cost_status')
            if match.get('benchmark_cost_status', '').startswith('provisional'):
                row['status'] = 'provisional_task_cost_not_actionable'
        pending = next((x for x in report.get('excluded_or_pending', []) if x.get('AA_model_slug') == record['slug']), None)
        if pending:
            row['routing_or_benchmark_caveat'] = pending.get('reason')
        if record.get('error'):
            row['retrieval_error'] = record['error']
        rows.append(row)

    # A score/cost pair is genuinely comparable on the index, even when its
    # OpenRouter revision or execution mode has not been established. Such a
    # row can challenge the claim of global coverage, but never becomes a route.
    standalone = [r for r in rows if r['measured_pair'] and r['status'] != 'measured_multi_model_or_fallback_not_single_call']
    for row in rows:
        if row not in standalone:
            row['AA_measurement_pareto'] = None
            row['cheaper_than_verified_selection_for_score'] = None
            continue
        row['AA_measurement_pareto'] = not any(
            other is not row and other['intelligence_score'] >= row['intelligence_score']
            and other['weighted_AA_task_cost_usd'] <= row['weighted_AA_task_cost_usd']
            and (other['intelligence_score'] > row['intelligence_score'] or other['weighted_AA_task_cost_usd'] < row['weighted_AA_task_cost_usd'])
            for other in standalone
        )
        eligible = [r for r in report['frontier'] if r['intelligence_score'] >= row['intelligence_score']]
        row['cheaper_than_verified_selection_for_score'] = (
            bool(eligible) and row['weighted_AA_task_cost_usd'] < min(r['benchmark_task_cost_usd'] for r in eligible)
        )
    rows.sort(key=lambda r: (r['intelligence_score'] is None, -(r['intelligence_score'] or 0), r['AA_slug']))
    challengers = [r for r in rows if r['AA_measurement_pareto'] and r['status'] == 'measured_route_or_configuration_unverified']
    non_callable = [r for r in rows if r['AA_measurement_pareto'] and r['status'] != 'verified_callable_frontier']
    return {
        'schema_version': '1.0.0', 'report_date': report['report_date'], 'checked_at': report['checked_at'],
        'index_version': report['benchmark']['version'], 'index_source': 'Artificial Analysis',
        'source_index_url': 'https://artificialanalysis.ai/models',
        'scope': 'All freshly acquired nondeprecated AA exact configurations, including missing and estimated results. The OpenRouter catalog has a separate complete inventory in coverage.json.',
        'cost_basis': 'AA measured weighted Intelligence Index task cost; not an OpenRouter invoice or provider token price.',
        'routing_policy': 'Only verified_callable_frontier rows carry a request. Candidate IDs are name-match discovery hints, not verified revisions or executable routes.',
        'counts': {'active_AA_records': len(rows), 'measured_pairs': sum(r['measured_pair'] for r in rows),
                   'single_configuration_measured_pairs': len(standalone), 'AA_measurement_pareto_count': sum(r['AA_measurement_pareto'] is True for r in rows),
                   'unverified_AA_pareto_challengers': len(challengers),
                   'non_callable_AA_measurement_frontier': len(non_callable),
                   'verified_callable_frontier': sum(r['status'] == 'verified_callable_frontier' for r in rows),
                   'OpenRouter_catalog_entries': len(catalog['data'])},
        'rows': rows,
    }


def main():
    report = load(OUT/'latest.json')
    acquired = load(ACQ/'workloads.json')
    comparison = build(acquired['active_exact_records'], load(ACQ/'catalog.json'), report)
    version = report['benchmark']['version']
    if any(row['benchmark_version'] != version for row in comparison['rows'] if not row.get('retrieval_error')):
        raise ValueError('Incompatible index versions in comprehensive comparison')
    if comparison['counts']['active_AA_records'] != len(acquired['active_exact_records']):
        raise ValueError('Incomplete exact configuration comparison')
    previous = load('comparisons.json') if Path('comparisons.json').exists() else {'rows':[]}
    prior = {r['AA_slug']:r for r in previous['rows']}
    updates = []
    for row in comparison['rows']:
        old = prior.get(row['AA_slug'])
        if old and not row.get('retrieval_error') and any(row[k] != old.get(k) for k in ('intelligence_score','weighted_AA_task_cost_usd')):
            updates.append({'AA_slug':row['AA_slug'],'label':row['AA_label'],'previous_score':old.get('intelligence_score'),
                            'score':row['intelligence_score'],'previous_AA_task_cost_usd':old.get('weighted_AA_task_cost_usd'),
                            'AA_task_cost_usd':row['weighted_AA_task_cost_usd'],'previous_retrieval_failed':bool(old.get('retrieval_error')),
                            'source_url':row['source_url'],'source_verified_at':row['source_verified_at']})
    comparison['changes_since_previous']={'previous_report_date':previous.get('report_date'),'measurement_updates':updates,
        'note':'Includes newly recovered source records and previously missing values; not every change represents a new evaluation. No older value is presented as freshly verified.'}
    report['changes_since_previous']['comparison_measurement_updates']=updates
    (OUT/'comparisons.json').write_text(json.dumps(comparison, ensure_ascii=False, separators=(',', ':'))+'\n')
    lines = [f"# All measured model configurations — {report['report_date']}", '',
             f"Source: [Artificial Analysis](https://artificialanalysis.ai/models), Intelligence Index v{version}. {comparison['counts']['active_AA_records']} active exact records; {comparison['counts']['measured_pairs']} measured score/cost pairs; {comparison['counts']['non_callable_AA_measurement_frontier']} non-callable points on the AA-only measurement frontier (including provisional costs and unavailable routes).", '',
             'This is the complete observed AA comparison, including models without a verified OpenRouter request. **Only** [latest.md](latest.md) contains executable, revision-pinned selections. A name match in the OpenRouter catalog does not verify the benchmarked revision, provider, mode or effort. Multi-model fallback systems and provisional pricing are not single-call routes. The index measures broad capability, not request success probability; the task cost is not an OpenRouter invoice.', '',
             '| AA configuration | Effort recorded by AA | Score | USD / AA task | Route status | AA measurement frontier | Source |',
             '|---|---|---:|---:|---|---|---|']
    for row in comparison['rows']:
        label = (row['AA_label'] or row['AA_slug']).replace('|', '\\|')
        score = str(row['intelligence_score']) if row['intelligence_score'] is not None else '—'
        cost = '$'+str(row['weighted_AA_task_cost_usd']) if row['weighted_AA_task_cost_usd'] is not None else '—'
        lines.append(f"| {label} | {row['reasoning_effort_as_measured'] or ('enabled / unlabeled' if row['is_reasoning_as_measured'] else 'none / unspecified')} | {score} | {cost} | {row['status']} | {'yes' if row['AA_measurement_pareto'] else '—' if row['AA_measurement_pareto'] is None else 'no'} | [AA]({row['source_url']}) |")
    (OUT/'comparisons.md').write_text('\n'.join(lines)+'\n')
    # Make the verified routing subset's limitations visible at its point of use.
    report['scope']['measured_comparison_file'] = 'comparisons.json'
    report['scope']['frontier_completeness'] = 'verified_routing_subset; not a global optimum over every measured AA configuration'
    report['coverage_inventory']['active_AA_exact_records'] = comparison['counts']['active_AA_records']
    report['coverage_inventory']['measured_score_task_cost_pairs'] = comparison['counts']['measured_pairs']
    report['coverage_inventory']['AA_only_unverified_pareto_challengers'] = comparison['counts']['unverified_AA_pareto_challengers']
    report['coverage_inventory']['AA_only_non_callable_frontier'] = comparison['counts']['non_callable_AA_measurement_frontier']
    content = json.dumps(report, indent=2, ensure_ascii=False)+'\n'
    (OUT/'latest.json').write_text(content)
    (OUT/'snapshots'/f"{report['report_date']}.json").write_text(content)
    print('Built comprehensive AA comparison:', comparison['counts'], flush=True)


if __name__ == '__main__':
    main()
