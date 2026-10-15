"""Validate planning JSON, schema definitions, references and checkpoint coverage."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
planning = ROOT / 'planning'
documents = {p.name: json.loads(p.read_text()) for p in planning.glob('*.json')}
for name, document in documents.items():
    if name.endswith('.schema.json'):
        Draft202012Validator.check_schema(document)


def check_refs(value):
    if isinstance(value, dict):
        reference = value.get('$ref', '')
        if reference and not reference.startswith(('#', 'http:', 'https:')):
            filename, _, fragment = reference.partition('#')
            target = documents[filename]
            for segment in fragment.strip('/').split('/'):
                if segment:
                    target = target[segment.replace('~1', '/').replace('~0', '~')]
        for child in value.values():
            check_refs(child)
    elif isinstance(value, list):
        for child in value:
            check_refs(child)


for document in documents.values():
    check_refs(document)
plan = documents['workflow_plan.json']
steps = plan['workflow']
assert [s['step'] for s in steps] == ['intake'] + [str(n) for n in range(9)]
for step in steps:
    checkpoint = step['checkpoint']
    assert checkpoint['required'] and checkpoint['quality_checks']
    assert checkpoint['human_approval_required'] == (step['step'] == '1')
assert plan['plan_version'] == plan['change_history'][-1]['version']
assert plan['commit_text'] == plan['change_history'][-1]['commit_text']
print(f'Validated {len(documents)} JSON files, schema definitions, external schema references and all {len(steps)} stage checkpoint declarations.')
