# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Stephan A. Davis

from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("validate_package", ROOT / "scripts/validate_package.py")
validate_package = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validate_package)


class PackageValidationTests(unittest.TestCase):
    def test_current_package_is_valid(self):
        errors, warnings, _ = validate_package.validate(ROOT)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_validator_rejects_registry_allowlist_extension(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "auren-core"
            shutil.copytree(ROOT, copied)
            registry_path = copied / "REMOTE-SOURCE-REGISTRY.json"
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            registry["default_policy"]["documented_invariants"]["allowed_hostnames"].append(
                "evil.com"
            )
            registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
            errors, _, _ = validate_package.validate(copied)
            self.assertTrue(any("documented_invariants" in item for item in errors))

    def test_validator_rejects_registry_port_extension(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "auren-core"
            shutil.copytree(ROOT, copied)
            registry_path = copied / "REMOTE-SOURCE-REGISTRY.json"
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            registry["default_policy"]["documented_invariants"]["allowed_ports"].append(444)
            registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
            errors, _, _ = validate_package.validate(copied)
            self.assertTrue(any("documented_invariants" in item for item in errors))

    def test_validator_rejects_skill_version_divergence(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "auren-core"
            shutil.copytree(ROOT, copied)
            skill_path = copied / "SKILL.md"
            skill_path.write_text(
                skill_path.read_text(encoding="utf-8").replace(
                    'version: "1.2.5"', 'version: "9.9.9"', 1
                ),
                encoding="utf-8",
            )
            errors, _, _ = validate_package.validate(copied)
            self.assertTrue(any("SKILL.md metadata version" in item for item in errors))

    def test_validator_rejects_update_report_schema_version_divergence(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "auren-core"
            shutil.copytree(ROOT, copied)
            schema_path = copied / "references/update-report.schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["properties"]["report_version"]["const"] = "9.9"
            schema_path.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
            errors, _, _ = validate_package.validate(copied)
            self.assertTrue(any("Update-report schema report_version" in item for item in errors))

    def test_validator_rejects_optional_catalog_required_dependency(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "auren-core"
            shutil.copytree(ROOT, copied)
            path = copied / "OPTIONAL-SEMANTIC-REFERENCES.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["policy"]["required_for_core_operation"] = True
            path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            errors, _, _ = validate_package.validate(copied)
            self.assertTrue(any("required_for_core_operation=false" in item for item in errors))

    def test_validator_rejects_optional_catalog_license_inheritance(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "auren-core"
            shutil.copytree(ROOT, copied)
            path = copied / "OPTIONAL-SEMANTIC-REFERENCES.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["references"][0]["package_license_applies"] = True
            path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            errors, _, _ = validate_package.validate(copied)
            self.assertTrue(any("package_license_applies=false" in item for item in errors))

    def test_validator_rejects_optional_catalog_nonstandard_url(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "auren-core"
            shutil.copytree(ROOT, copied)
            path = copied / "OPTIONAL-SEMANTIC-REFERENCES.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["references"][0]["canonical_url"] = "https://stephanadavis.de:444/perspektivensystemik/"
            path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            errors, _, _ = validate_package.validate(copied)
            self.assertTrue(any("invalid canonical URL" in item for item in errors))

    def test_validator_rejects_optional_catalog_edition_divergence(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "auren-core"
            shutil.copytree(ROOT, copied)
            path = copied / "OPTIONAL-SEMANTIC-REFERENCES.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["edition"] = "wrong-edition"
            path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            errors, _, _ = validate_package.validate(copied)
            self.assertTrue(any("catalog edition" in item for item in errors))

    def test_validator_rejects_optional_catalog_missing_required_reference(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "auren-core"
            shutil.copytree(ROOT, copied)
            path = copied / "OPTIONAL-SEMANTIC-REFERENCES.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["references"] = data["references"][:-1]
            path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            errors, _, _ = validate_package.validate(copied)
            self.assertTrue(any("must contain exactly" in item for item in errors))

    def test_validator_rejects_language_validation_semantics_divergence(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "auren-core"
            shutil.copytree(ROOT, copied)
            manifest_path = copied / "RELEASE-MANIFEST.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["validated_user_languages"] = ["English"]
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            errors, _, _ = validate_package.validate(copied)
            self.assertTrue(any("validated_user_languages" in item for item in errors))

    def test_validator_rejects_release_evidence_skill_line_drift(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "auren-core"
            shutil.copytree(ROOT, copied)
            manifest = json.loads((copied / "RELEASE-MANIFEST.json").read_text(encoding="utf-8"))
            evidence_path = copied / manifest["evaluation"]["release_evidence_record"]
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            run = next(item for item in evidence["evaluation_runs"] if item["id"] == "package-validation")
            run["result"]["skill_md_lines"] += 1
            evidence_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
            errors, _, _ = validate_package.validate(copied)
            self.assertTrue(any("skill_md_lines" in item for item in errors))

    def test_validator_rejects_release_evidence_generated_at_before_runs(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "auren-core"
            shutil.copytree(ROOT, copied)
            manifest = json.loads((copied / "RELEASE-MANIFEST.json").read_text(encoding="utf-8"))
            evidence_path = copied / manifest["evaluation"]["release_evidence_record"]
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            evidence["generated_at"] = "2000-01-01T00:00:00Z"
            evidence_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
            errors, _, _ = validate_package.validate(copied)
            self.assertTrue(any("generated_at" in item and "executed_at" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
