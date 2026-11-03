"""Offline regression for the AA v5/v5.0 display-label transition."""
import json
import unittest
from unittest.mock import patch
from acquire import exact

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
        self.assertIn('error',self.record(False))

if __name__=='__main__':unittest.main()
