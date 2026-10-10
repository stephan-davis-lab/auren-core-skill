# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Stephan A. Davis

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("validate_evals", ROOT / "scripts/validate_evals.py")
validate_evals = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validate_evals)

SCHEMA_SPEC = importlib.util.spec_from_file_location(
    "validate_release_evidence", ROOT / "scripts/validate_release_evidence.py"
)
validate_release_evidence = importlib.util.module_from_spec(SCHEMA_SPEC)
assert SCHEMA_SPEC.loader is not None
SCHEMA_SPEC.loader.exec_module(validate_release_evidence)


class EvalInventoryTests(unittest.TestCase):
    def setUp(self):
        self.version, self.evidence_path, self.schema_path, self.schema_version = (
            validate_evals.release_config(ROOT)
        )

    def test_eval_inventory_is_valid(self):
        self.assertEqual(validate_evals.validate(ROOT), [])

    def test_inventory_versions_follow_release_manifest(self):
        main = validate_evals.load_json(ROOT / "evals/evals.json")
        triggers = validate_evals.load_json(ROOT / "evals/description-trigger-evals.json")
        self.assertEqual(main["skill_version"], self.version)
        self.assertEqual(triggers["skill_version"], self.version)

    def test_behavioral_evidence_does_not_claim_unrun_hosts(self):
        evidence = validate_evals.load_json(self.evidence_path)
        behavioral = evidence["behavioral_model_evidence"]
        if behavioral["status"] == "not_run":
            self.assertEqual(behavioral["hosts"], [])
        else:
            self.assertTrue(behavioral["hosts"])
            for host in behavioral["hosts"]:
                self.assertEqual(host["cases_run"], host["passed"] + host["failed"] + host["manual_reviewed"])
                self.assertTrue((ROOT / host["evidence_reference"]).is_file())

    def test_every_trigger_class_has_exact_bilingual_parity(self):
        triggers = validate_evals.load_json(ROOT / "evals/description-trigger-evals.json")
        classes = {}
        for case in triggers["cases"]:
            classes.setdefault(case["trigger_class"], set()).add(case["language"])
        self.assertEqual(set(classes), validate_evals.REQUIRED_TRIGGER_CLASSES)
        for languages in classes.values():
            self.assertEqual(languages, {"en", "de"})

    def test_every_high_risk_path_has_exact_bilingual_parity(self):
        main = validate_evals.load_json(ROOT / "evals/evals.json")
        groups = {}
        for case in main["cases"]:
            group = case.get("risk_parity_group")
            if group:
                groups.setdefault(group, set()).add(case["language"])
        self.assertEqual(set(groups), validate_evals.REQUIRED_RISK_PARITY_GROUPS)
        for languages in groups.values():
            self.assertEqual(languages, {"en", "de"})

    def test_release_evidence_passes_complete_json_schema_validation(self):
        evidence = validate_evals.load_json(self.evidence_path)
        schema = validate_evals.load_json(self.schema_path)
        self.assertEqual(validate_release_evidence.validate_documents(evidence, schema), [])

    def test_release_evidence_schema_rejects_missing_required_field(self):
        evidence = validate_evals.load_json(self.evidence_path)
        schema = validate_evals.load_json(self.schema_path)
        invalid = copy.deepcopy(evidence)
        del invalid["release"]["release_scope"]
        errors = validate_release_evidence.validate_documents(invalid, schema)
        self.assertTrue(any("release_scope" in error for error in errors))

    def test_release_evidence_schema_rejects_unknown_field(self):
        evidence = validate_evals.load_json(self.evidence_path)
        schema = validate_evals.load_json(self.schema_path)
        invalid = copy.deepcopy(evidence)
        invalid["release"]["untracked_claim"] = True
        errors = validate_release_evidence.validate_documents(invalid, schema)
        self.assertTrue(any("Additional properties" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
