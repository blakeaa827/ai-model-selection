"""Missing optional AA display metadata must not crash or invent a model pin."""
import importlib.util
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('builder',Path(__file__).with_name('build-workloads.py'))
builder=importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

class AgentMetadata(unittest.TestCase):
    def test_missing_or_invalid_display_stays_pending(self):
        for display in [None,{},[],{'model':None},{'model':''}]:
            with self.subTest(display=display):
                self.assertEqual(builder.agent_model_metadata({'display':display}),
                                 (None,['missing_tested_model_metadata']))
        self.assertEqual(builder.agent_model_metadata({'displayLabel':'Vibe - guessed model'}),
                         (None,['missing_tested_model_metadata']))
    def test_original_label_is_preserved(self):
        self.assertEqual(builder.agent_model_metadata({'display':{'model':'Exact source label'}}),
                         ('Exact source label',[]))

if __name__=='__main__':unittest.main()
