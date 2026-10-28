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

if __name__=='__main__':unittest.main()
