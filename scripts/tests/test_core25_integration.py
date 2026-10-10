# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Stephan A. Davis

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]

def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"scripts/{name}.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

checker = module('check_remote_sources')
package = module('validate_package')
evals = module('validate_evals')

class Core25IntegrationTests(unittest.TestCase):
    def test_pinned_manual_source_never_uses_network(self):
        registry = json.loads((ROOT / 'REMOTE-SOURCE-REGISTRY.json').read_text())
        source = next(s for s in registry['sources'] if s['source_id'] == 'core_logic')
        with patch.object(checker, 'fetch') as fetch:
            result = checker.check_source(source, registry['default_policy'], None)
        fetch.assert_not_called()
        self.assertEqual(result['classification'], 'fetch_unavailable')
        self.assertFalse(result['automatic_activation'])

    def test_current_source_readme_header_version_is_detected(self):
        text = (ROOT / 'references/README_v2.5.md').read_text()
        self.assertEqual(checker.extract_version('core_readme', text), '2.5')

    def test_removed_process_consent_block_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'auren-core'
            shutil.copytree(ROOT, target)
            path = target / 'references/auren-core-specs_v2.5.yaml'
            data = package.yaml.safe_load(path.read_text())
            del data['auren_core_spec']['systemic_method_layer']['observation_consent']
            path.write_text(package.yaml.safe_dump(data))
            errors, _, _ = package.validate(target)
            self.assertTrue(any('observation-consent block missing' in error for error in errors))

    def test_superseded_runtime_source_selection_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'auren-core'
            shutil.copytree(ROOT, target)
            path = target / 'SKILL.md'
            path.write_text(path.read_text().replace('references/auren-core-specs_v2.5.yaml', 'references/auren-core-specs_v2.4.yaml'))
            errors, _, _ = package.validate(target)
            self.assertTrue(any('operational source hierarchy' in error for error in errors))

    def test_divergent_resonance_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'auren-core'
            shutil.copytree(ROOT, target)
            path = target / 'OPTIONAL-SEMANTIC-REFERENCES.json'
            data = json.loads(path.read_text())
            row = next(x for x in data['references'] if x['reference_id'] == 'AUR-025')
            row['canonical_url'] = 'https://stephanadavis.de/perspektivensystemik/'
            path.write_text(json.dumps(data))
            errors, _, _ = package.validate(target)
            self.assertTrue(any('Resonanzkreis catalog must match' in error for error in errors))

    def test_missing_calibration_language_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'auren-core'
            shutil.copytree(ROOT, target)
            path = target / 'evals/evals.json'
            data = json.loads(path.read_text())
            data['cases'] = [x for x in data['cases'] if x['id'] != 'core25-ambiguous-compound-assent-de']
            path.write_text(json.dumps(data))
            errors = evals.validate(target)
            self.assertTrue(any('calibration group must have exact English/German parity: ambiguous-compound-assent' in error for error in errors))

    def test_unresolved_upstream_rule_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'auren-core'
            shutil.copytree(ROOT, target)
            path = target / 'evals/core-specs-v2.5/scenarios_v2.5.yaml'
            data = evals.yaml.safe_load(path.read_text())
            data['scenarios'][0]['rule_refs'] = ['missing.nonexistent.rule']
            path.write_text(evals.yaml.safe_dump(data))
            self.assertTrue(any('rule reference invalid' in error for error in evals.validate(target)))

if __name__ == '__main__':
    unittest.main()
