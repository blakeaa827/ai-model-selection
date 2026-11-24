"""Offline regression for AA index version and measurement evidence."""
import json
import unittest
from unittest.mock import patch
from acquire import exact, data_manifests, normalize_configuration_index, configuration_models

REQUIRED=['aa-briefcase','automationbench-aa','terminalbench-4-0',
    'frontiercode-2-0','omniscience','gdp-pdf','hle-diamond',
    'critpt-v2-hard','terminal-bench-science']

class VersionLabels(unittest.TestCase):
    def record(self, labels):
        row={'slug':'fixture','intelligenceIndexIsEstimated':False}
        body=' '.join('Intelligence Index v'+v for v in labels)
        body+='<script>self.__next_f.push('+json.dumps([1,'0:'+json.dumps(row)+'\n'])+')</script>'
        with patch('acquire.fetch',return_value=(body,'2026-10-28T00:00:00+00:00')):
            return exact('fixture')
    def test_equivalent_major_labels(self):
        self.assertEqual(self.record(['5','5.0'])['version'],'5.0')
    def test_actual_mixed_versions_rejected(self):
        self.assertIn('error',self.record(['4.3.2','5.0']))
    def test_legacy_minor_patch_preserved(self):
        self.assertEqual(self.record(['4.3.2'])['version'],'4.3.2')

class MissingEstimationFlag(unittest.TestCase):
    def record(self, complete):
        slugs=['aa-briefcase','automationbench-aa','terminalbench-4-0',
            'frontiercode-2-0','omniscience','gdp-pdf','hle-diamond',
            'critpt-v2-hard','terminal-bench-science']
        row={'id':'fixture-id','slug':'fixture','release':{},'isReasoning':True,
            'intelligenceIndex':25,'intelligenceIndexCostPerTask':{'cost':{'total':1}},
            'intelligenceIndexEvaluations':[{'slug':s,'score':0.5,'costPerTask':1,'outputTokensPerTask':100} for s in slugs[:9 if complete else 8]]}
        body='Intelligence Index v5.0<script>self.__next_f.push('+json.dumps([1,'0:'+json.dumps(row)+'\n'])+')</script>'
        with patch('acquire.fetch',return_value=(body,'2026-11-03T00:00:00+00:00')):
            return exact('fixture')
    def test_complete_original_evaluations_establish_measurement(self):
        r=self.record(True)
        self.assertIs(r['intelligenceIndexIsEstimated'],False)
        self.assertIs(r['estimation_status_provenance']['source_flag_present'],False)
    def test_incomplete_evidence_does_not_silently_become_measured(self):
        failed=self.record(False)
        self.assertIn('incomplete original evaluation evidence',failed['error'])
        self.assertEqual(failed['parsed_index_versions'],['5.0'])

class IndexV501(unittest.TestCase):
    def page(self, labels, row):
        body=' '.join('Intelligence Index v'+v for v in labels)
        body+='<script>self.__next_f.push('+json.dumps([1,'0:'+json.dumps(row)+'\n'])+')</script>'
        with patch('acquire.fetch',return_value=(body,'2026-11-24T00:00:00+00:00')):
            return exact('fixture')
    def current(self, **overrides):
        row={'id':'fixture-id','slug':'fixture','name':'Fixture','release':{},'isReasoning':True,
            'intelligenceIndex':25,'intelligenceIndexCostPerTask':{'cost':{'total':1},
                'evaluations':[{'slug':s,'weightedCostPerTask':0.1} for s in REQUIRED]},
            'intelligenceIndexOutputTokensPerTask':{'reasoning':40,'answer':60,'output':100},
            'briefcaseBreakdown':{'overall':{'elo':1500}},'automationBenchPartialScore':0.4,
            'terminalBench40':0.3,'frontierCode20':0.2,'omniscience':-3.5,'gdpPdfAllPass':0.2,
            'hleDiamond':0.2,'critptAgenticHard':0.3,'terminalBenchScience':0.1}
        row.update(overrides)
        return row
    def test_patch_version_is_preserved(self):
        r=self.page(['5.0.1'],self.current())
        self.assertEqual(r['version'],'5.0.1')
        self.assertIs(r['intelligenceIndexIsEstimated'],False)
        self.assertIs(r['estimation_status_provenance']['source_flag_present'],False)
        self.assertEqual(r['estimation_status_provenance']['index_version'],'5.0.1')
        self.assertIn('v5_0_1',r['estimation_status_provenance']['basis'])
        self.assertNotIn('intelligenceIndexEvaluations',r)
    def test_sentence_period_is_not_a_second_version(self):
        r=self.page(['5.0.1.'],self.current())
        self.assertEqual(r['version'],'5.0.1')
    def test_major_badge_beside_patch_is_rejected(self):
        failed=self.page(['5','5.0.1'],self.current())
        self.assertIn('Exact record or common index version missing',failed['error'])
        self.assertEqual(failed['parsed_index_versions'],['5.0','5.0.1'])
    def test_new_shape_is_not_accepted_as_v5_0(self):
        failed=self.page(['5.0'],self.current())
        self.assertIn('incomplete original evaluation evidence',failed['error'])
    def test_unapproved_version_fails_closed(self):
        row=self.current()
        row['intelligenceIndexEvaluations']=[{'slug':s,'score':0.5,'costPerTask':1,'outputTokensPerTask':100} for s in REQUIRED]
        failed=self.page(['5.2'],row)
        self.assertIn('unapproved index version',failed['error'])
        self.assertEqual(failed['parsed_index_versions'],['5.2'])
    def test_legacy_records_keep_their_real_version(self):
        row={'id':'fixture-id','slug':'fixture','release':{},'isReasoning':True,
            'intelligenceIndex':25,'intelligenceIndexCostPerTask':{'cost':{'total':1}},
            'intelligenceIndexEvaluations':[{'slug':s,'score':0.5,'costPerTask':1,'outputTokensPerTask':100} for s in REQUIRED]}
        r=self.page(['5.0.1'],row)
        self.assertEqual(r['version'],'5.0.1')
        self.assertIs(r['intelligenceIndexIsEstimated'],False)
        self.assertEqual(r['estimation_status_provenance']['basis'],'complete_nine_original_evaluation_score_cost_token_records')
    def test_missing_constituent_score_or_cost_or_tokens_fails(self):
        missing_score=self.current();missing_score['critptAgenticHard']=None
        missing_cost=self.current();missing_cost['intelligenceIndexCostPerTask']['evaluations']=missing_cost['intelligenceIndexCostPerTask']['evaluations'][:-1]
        missing_tokens=self.current();missing_tokens['intelligenceIndexOutputTokensPerTask']={'reasoning':1}
        for row in (missing_score,missing_cost,missing_tokens):
            self.assertIn('incomplete original evaluation evidence',self.page(['5.0.1'],row)['error'])
    def test_name_only_row_is_not_a_measured_record(self):
        failed=self.page(['5.0.1'],{'slug':'fixture','name':'Fixture','intelligenceIndex':25,'creator':{},'releaseDate':'2026-11-04'})
        self.assertIn('Exact record or common index version missing',failed['error'])
        self.assertEqual(failed['parsed_index_versions'],['5.0.1'])
    def test_score_without_task_cost_stays_unmeasured(self):
        row=self.current(intelligenceIndexCostPerTask={'evaluations':[{'slug':s,'weightedCostPerTask':0.1} for s in REQUIRED]})
        r=self.page(['5.0.1'],row)
        self.assertNotIn('error',r)
        self.assertIsNone(r['intelligenceIndexIsEstimated'])

class ConfigurationInventory(unittest.TestCase):
    def rows(self, n=100, release='rel'):
        return [{'slug':'m%d'%i,'name':'Model %d'%i,'release':{'slug':release}} for i in range(n)]
    def test_release_object_is_normalized(self):
        index=normalize_configuration_index(self.rows())
        self.assertEqual(len(index),100)
        self.assertEqual(index[0]['releaseSlug'],'rel')
    def test_legacy_release_slug_is_preserved(self):
        rows=[{'slug':'m%d'%i,'releaseSlug':'old'} for i in range(100)]
        self.assertEqual(normalize_configuration_index(rows)[0]['releaseSlug'],'old')
    def test_short_duplicate_or_slugless_inventory_is_rejected(self):
        self.assertIsNone(normalize_configuration_index(self.rows(99)))
        duplicated=self.rows();duplicated[1]['slug']=duplicated[0]['slug']
        self.assertIsNone(normalize_configuration_index(duplicated))
        missing=self.rows();missing[0].pop('release')
        self.assertIsNone(normalize_configuration_index(missing))
    def test_only_a_models_payload_is_an_inventory(self):
        self.assertEqual(len(configuration_models({'models':self.rows()})),100)
        self.assertIsNone(configuration_models([{'slug':'m'}]))
        self.assertIsNone(configuration_models({'models':self.rows(20)}))
    def test_manifests_require_one_key_per_path(self):
        key='a'*64
        records=[{'path':'/data/'+'ab'*8+'.txt','key':key},{'path':'/nav','key':'nope'}]
        self.assertEqual(data_manifests(records),[{'path':'/data/'+'ab'*8+'.txt','key':key}])
        records.append({'path':'/data/'+'ab'*8+'.txt','key':'b'*64})
        self.assertRaises(ValueError,data_manifests,records)

if __name__=='__main__':unittest.main()
