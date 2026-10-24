"""Validate the maintained JSON Schema and ensure the SVG is parseable."""
import json,sys
from pathlib import Path
from xml.etree import ElementTree
# Local isolated dependency location; GitHub workflow installs the same pinned package.
sys.path.insert(0,str(Path('run-artifacts/validation-deps').absolute()))
from jsonschema import Draft202012Validator
schema=json.loads(Path('schema.json').read_text());Draft202012Validator.check_schema(schema)
report=json.loads(Path('run-artifacts/report/latest.json').read_text());Draft202012Validator(schema).validate(report)
ElementTree.parse('run-artifacts/report/cost-curve.svg')
print('PASS: JSON Schema 2020-12 contract and parseable SVG')
