"""Regression checks: complete evidence comparison never manufactures a route."""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('comparisons', Path(__file__).with_name('build-comparisons.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Comparisons(unittest.TestCase):
    def test_all_records_retained_without_invented_requests(self):
        def record(slug, score, cost, name=None):
            return {'slug':slug,'name':name or slug,'release':{'slug':slug,'name':slug},
                    'intelligenceIndex':score,'intelligenceIndexCostPerTask':{'cost':{'total':cost}} if cost is not None else None,
                    'version':'5.0','intelligenceIndexIsEstimated':False,'deprecated':False,
                    'source_url':'https://artificialanalysis.ai/models/'+slug,'verified_at':'2026-10-29T00:00:00Z'}
        records=[record('incumbent',30,.2),record('challenger',31,.1),record('missing',None,None),
                 record('fallback',40,.05,'Fallback router')]
        catalog={'data':[{'id':'lab/challenger','name':'Lab: challenger'}]}
        baseline={'report_date':'2026-10-29','checked_at':'2026-10-29T00:00:00Z',
                  'benchmark':{'version':'5.0'},
                  'frontier':[{'configuration_id':'incumbent@high','intelligence_score':30,'benchmark_task_cost_usd':.2,'request':{'model':'lab/incumbent'}}],
                  'limited_free_configurations':[],
                  'evaluated_configurations':[{'configuration_id':'incumbent@high','benchmark_source_url':records[0]['source_url'],
                                               'openrouter_model_id':'lab/incumbent','request':{'model':'lab/incumbent'}}]}
        result=module.build(records,catalog,baseline)
        rows={r['AA_slug']:r for r in result['rows']}
        self.assertEqual(result['counts']['active_AA_records'],4)
        self.assertEqual(rows['challenger']['status'],'measured_route_or_configuration_unverified')
        self.assertIsNone(rows['challenger']['request'])
        self.assertTrue(rows['challenger']['AA_measurement_pareto'])
        self.assertTrue(rows['challenger']['cheaper_than_verified_selection_for_score'] is False)  # no incumbent reaches 31
        self.assertIsNone(rows['missing']['weighted_AA_task_cost_usd'])
        self.assertIsNone(rows['fallback']['AA_measurement_pareto'])
        self.assertEqual(rows['incumbent']['request']['model'],'lab/incumbent')


if __name__ == '__main__':
    unittest.main()
