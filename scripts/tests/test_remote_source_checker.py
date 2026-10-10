# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Stephan A. Davis

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
import urllib.error
import urllib.request
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("checker", ROOT / "scripts/check_remote_sources.py")
checker = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(checker)


class SourceCheckerTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads((ROOT / "REMOTE-SOURCE-REGISTRY.json").read_text(encoding="utf-8"))
        self.policy = self.registry["default_policy"]
        self.sources = {s["source_id"]: s for s in self.registry["sources"]}
        self.allowed = set(checker.ALLOWED_HOSTNAMES)

    def _write_complete_fixtures(self, directory: Path) -> None:
        (directory / "ai_index.bin").write_bytes(f'Version: "{self.sources["ai_index"]["baseline_version"]}"\n'.encode())
        (directory / "core_readme.bin").write_bytes(
            (ROOT / self.sources["core_readme"]["package_local_file"]).read_bytes()
        )
        (directory / "core_logic.bin").write_bytes(
            (ROOT / self.sources["core_logic"]["package_local_file"]).read_bytes()
        )
        specs = (ROOT / self.sources["core_specs"]["package_local_file"]).read_bytes()
        (directory / "core_specs.bin").write_bytes(specs)
        (directory / "core_specs.mirror1.bin").write_bytes(specs)
        (directory / "guidance.bin").write_bytes(
            (ROOT / self.sources["guidance"]["package_local_file"]).read_bytes()
        )


    def _validate_report(self, registry: dict, directory: Path) -> dict:
        report = checker.build_report(
            registry, directory, checked_at="2026-08-15T15:30:00+00:00"
        )
        schema = json.loads(
            (ROOT / "references/update-report.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(schema)
        errors = sorted(
            Draft202012Validator(
                schema, format_checker=FormatChecker()
            ).iter_errors(report),
            key=lambda item: list(item.absolute_path),
        )
        self.assertEqual([error.message for error in errors], [])
        return report

    def _single_source_registry(self, source_id: str) -> dict:
        registry = copy.deepcopy(self.registry)
        registry["sources"] = [copy.deepcopy(self.sources[source_id])]
        return registry

    def test_ai_index_has_no_local_snapshot(self):
        source = self.sources["ai_index"]
        self.assertFalse(source["bundled"])
        self.assertFalse(source["baseline_snapshot"])
        self.assertNotIn("baseline_local_file", source)

    def test_core_specs_mirror_is_always_checked(self):
        source = self.sources["core_specs"]
        self.assertTrue(source["mirror_equivalence_required"])
        self.assertEqual(len(source["mirror_urls"]), 1)
        self.assertNotIn("fallback_urls", source)

    def test_mirror_divergence_blocks_adoption(self):
        source = self.sources["core_specs"]
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            base = (ROOT / self.sources["core_specs"]["package_local_file"]).read_bytes()
            (directory / "core_specs.bin").write_bytes(base)
            (directory / "core_specs.mirror1.bin").write_bytes(base + b"\n# divergence\n")
            result = checker.check_source(source, self.policy, directory)
            self.assertEqual(result["classification"], "mirror_divergence")
            self.assertFalse(result["automatic_activation"])

    def test_no_change_fixture(self):
        source = self.sources["core_readme"]
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            (directory / "core_readme.bin").write_bytes((ROOT / self.sources["core_readme"]["package_local_file"]).read_bytes())
            result = checker.check_source(source, self.policy, directory)
            self.assertEqual(result["classification"], "no_change")

    def test_validate_url_accepts_exact_allowlisted_https_url(self):
        checker.validate_url("https://stephanadavis.de/ai-index.txt", self.allowed)

    def test_validate_url_accepts_explicit_standard_https_port(self):
        checker.validate_url("https://stephanadavis.de:443/ai-index.txt", self.allowed)

    def test_validate_url_blocks_http(self):
        with self.assertRaisesRegex(ValueError, "HTTPS"):
            checker.validate_url("http://stephanadavis.de/ai-index.txt", self.allowed)

    def test_validate_url_blocks_unallowlisted_hostname(self):
        with self.assertRaisesRegex(ValueError, "allowlisted"):
            checker.validate_url("https://evil.com/ai-index.txt", self.allowed)

    def test_validate_url_blocks_subdomain(self):
        with self.assertRaisesRegex(ValueError, "allowlisted"):
            checker.validate_url("https://sub.stephanadavis.de/ai-index.txt", self.allowed)

    def test_validate_url_blocks_query_string(self):
        with self.assertRaisesRegex(ValueError, "Query strings"):
            checker.validate_url("https://stephanadavis.de/ai-index.txt?x=1", self.allowed)

    def test_validate_url_blocks_fragment(self):
        with self.assertRaisesRegex(ValueError, "fragments"):
            checker.validate_url("https://stephanadavis.de/ai-index.txt#x", self.allowed)

    def test_validate_url_blocks_nonstandard_https_port(self):
        with self.assertRaisesRegex(ValueError, "port 443"):
            checker.validate_url("https://stephanadavis.de:444/ai-index.txt", self.allowed)


    def test_validate_url_blocks_userinfo(self):
        with self.assertRaisesRegex(ValueError, "credentials"):
            checker.validate_url("https://user:password@stephanadavis.de/ai-index.txt", self.allowed)

    def test_redirect_handler_blocks_userinfo(self):
        handler = checker.SameHostRedirectHandler(self.allowed)
        request = urllib.request.Request("https://stephanadavis.de/start")
        with self.assertRaises(urllib.error.HTTPError):
            handler.redirect_request(
                request, None, 302, "Found", {},
                "https://user:password@stephanadavis.de/next",
            )

    def test_registry_userinfo_policy_extension_is_rejected(self):
        altered = copy.deepcopy(self.policy)
        altered["documented_invariants"]["url_userinfo_allowed"] = True
        errors = checker.validate_registry_policy(altered)
        self.assertTrue(any("documented_invariants" in item for item in errors))

    def test_redirect_handler_allows_same_host_https_redirect(self):
        handler = checker.SameHostRedirectHandler(self.allowed)
        request = urllib.request.Request("https://stephanadavis.de/start")
        redirected = handler.redirect_request(
            request, None, 302, "Found", {}, "https://stephanadavis.de/next"
        )
        self.assertIsInstance(redirected, urllib.request.Request)
        self.assertEqual(redirected.full_url, "https://stephanadavis.de/next")

    def test_redirect_handler_allows_explicit_standard_https_port(self):
        handler = checker.SameHostRedirectHandler(self.allowed)
        request = urllib.request.Request("https://stephanadavis.de/start")
        redirected = handler.redirect_request(
            request, None, 302, "Found", {}, "https://stephanadavis.de:443/next"
        )
        self.assertIsInstance(redirected, urllib.request.Request)
        self.assertEqual(redirected.full_url, "https://stephanadavis.de:443/next")

    def test_redirect_handler_blocks_cross_domain_redirect(self):
        handler = checker.SameHostRedirectHandler(self.allowed)
        request = urllib.request.Request("https://stephanadavis.de/start")
        with self.assertRaises(urllib.error.HTTPError):
            handler.redirect_request(request, None, 302, "Found", {}, "https://evil.com/next")

    def test_redirect_handler_blocks_non_https_redirect(self):
        handler = checker.SameHostRedirectHandler(self.allowed)
        request = urllib.request.Request("https://stephanadavis.de/start")
        with self.assertRaises(urllib.error.HTTPError):
            handler.redirect_request(
                request, None, 302, "Found", {}, "http://stephanadavis.de/next"
            )

    def test_redirect_handler_blocks_query_string(self):
        handler = checker.SameHostRedirectHandler(self.allowed)
        request = urllib.request.Request("https://stephanadavis.de/start")
        with self.assertRaises(urllib.error.HTTPError):
            handler.redirect_request(
                request, None, 302, "Found", {}, "https://stephanadavis.de/next?x=1"
            )

    def test_redirect_handler_blocks_fragment(self):
        handler = checker.SameHostRedirectHandler(self.allowed)
        request = urllib.request.Request("https://stephanadavis.de/start")
        with self.assertRaises(urllib.error.HTTPError):
            handler.redirect_request(
                request, None, 302, "Found", {}, "https://stephanadavis.de/next#fragment"
            )

    def test_redirect_handler_blocks_nonstandard_https_port(self):
        handler = checker.SameHostRedirectHandler(self.allowed)
        request = urllib.request.Request("https://stephanadavis.de/start")
        with self.assertRaises(urllib.error.HTTPError):
            handler.redirect_request(
                request, None, 302, "Found", {}, "https://stephanadavis.de:444/next"
            )

    def test_registry_documented_invariants_match_enforced_behavior(self):
        self.assertEqual(self.policy["documented_invariants"], checker.DOCUMENTED_INVARIANTS)
        self.assertEqual(checker.validate_registry_policy(self.policy), [])

    def test_registry_allowlist_extension_is_rejected(self):
        altered = copy.deepcopy(self.policy)
        altered["documented_invariants"]["allowed_hostnames"].append("evil.com")
        errors = checker.validate_registry_policy(altered)
        self.assertTrue(any("documented_invariants" in item for item in errors))

    def test_registry_port_extension_is_rejected(self):
        altered = copy.deepcopy(self.policy)
        altered["documented_invariants"]["allowed_ports"].append(444)
        errors = checker.validate_registry_policy(altered)
        self.assertTrue(any("documented_invariants" in item for item in errors))


    def test_generated_report_branch_no_change_validates(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            (directory / "core_readme.bin").write_bytes((ROOT / self.sources["core_readme"]["package_local_file"]).read_bytes())
            report = self._validate_report(self._single_source_registry("core_readme"), directory)
            self.assertEqual(report["sources"][0]["classification"], "no_change")

    def test_generated_report_branch_operational_compatible_change_validates(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            data = (ROOT / self.sources["core_logic"]["package_local_file"]).read_bytes() + b"\n<!-- synthetic compatible change -->\n"
            (directory / "core_logic.bin").write_bytes(data)
            report = self._validate_report(self._single_source_registry("core_logic"), directory)
            self.assertEqual(report["sources"][0]["classification"], "operational_compatible_change")

    def test_generated_report_branch_fetch_unavailable_validates(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            report = self._validate_report(self._single_source_registry("core_readme"), directory)
            self.assertEqual(report["sources"][0]["classification"], "fetch_unavailable")

    def test_generated_report_branch_mirror_divergence_validates(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            base = (ROOT / self.sources["core_specs"]["package_local_file"]).read_bytes()
            (directory / "core_specs.bin").write_bytes(base)
            (directory / "core_specs.mirror1.bin").write_bytes(base + b"\n# synthetic divergence\n")
            report = self._validate_report(self._single_source_registry("core_specs"), directory)
            self.assertEqual(report["sources"][0]["classification"], "mirror_divergence")

    def test_generated_report_branch_invalid_source_validates(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            (directory / "core_specs.bin").write_bytes(b"not: [valid\n")
            (directory / "core_specs.mirror1.bin").write_bytes(b"not: [valid\n")
            report = self._validate_report(self._single_source_registry("core_specs"), directory)
            self.assertEqual(report["sources"][0]["classification"], "invalid_source")

    def test_generated_report_branch_license_or_rights_change_validates(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source = copy.deepcopy(self.sources["core_readme"])
            source["baseline_sha256_normalized"] = "0" * 64
            registry = copy.deepcopy(self.registry)
            registry["sources"] = [source]
            data = b"# AUREN Core Specs & Logic (v2.5)\nVersion: 2.5\nNo license marker here.\n"
            (directory / "core_readme.bin").write_bytes(data)
            report = self._validate_report(registry, directory)
            self.assertEqual(report["sources"][0]["classification"], "license_or_rights_change")

    def test_generated_update_report_validates_against_full_schema(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            self._write_complete_fixtures(directory)
            report = checker.build_report(
                self.registry,
                directory,
                checked_at="2026-08-06T14:55:00+00:00",
            )
            schema = json.loads(
                (ROOT / "references/update-report.schema.json").read_text(encoding="utf-8")
            )
            Draft202012Validator.check_schema(schema)
            errors = sorted(
                Draft202012Validator(
                    schema, format_checker=FormatChecker()
                ).iter_errors(report),
                key=lambda item: list(item.absolute_path),
            )
            self.assertEqual([error.message for error in errors], [])
            self.assertEqual(report["report_version"], checker.REPORT_VERSION)


if __name__ == "__main__":
    unittest.main()
