#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Stephan A. Davis

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from check_remote_sources import REPORT_VERSION, validate_url
from security_invariants import DOCUMENTED_INVARIANTS, validate_registry_policy

REQUIRED_STATIC = [
    "SKILL.md",
    "README.md",
    "GOVERNANCE.md",
    "PRIVACY-AND-DATA-MINIMIZATION.md",
    "ATTRIBUTION.md",
    "BRAND-AND-NAME-NOTICE.md",
    "SOURCE-MATERIAL-NOTICES.md",
    "RIGHTS-LICENSE-EDITION-MATRIX.md",
    "RIGHTS-LICENSE-EDITION-MATRIX.json",
    "REMOTE-SOURCE-REGISTRY.json",
    "OPTIONAL-SEMANTIC-REFERENCES.json",
    "OPTIONAL-SEMANTIC-REFERENCES.md",
    "REMOTE-SOURCE-UPDATE-CHECK.md",
    "SECURITY.md",
    "EMBEDDED-REFERENCES.json",
    "RELEASE-MANIFEST.json",
    "CHECKSUMS.sha256",
    "CHANGELOG.md",
    "LICENSE",
    "LICENSES/CC-BY-SA-4.0.txt",
    "LICENSES/MIT.txt",
    "LICENSES/README.md",
    "references/auren-core-specs_v2.4.yaml",
    "references/auren-core-specs_v2.4.yaml.txt",
    "references/auren-core-logic_v2.4.md",
    "references/README_v2.4.md",
    "references/Guidance4AIsystems_v2.4.txt",
    "references/runtime-contract.md",
    "references/integration-mode.md",
    "references/audit-mode.md",
    "references/update-report.schema.json",
    "evals/evals.json",
    "evals/description-trigger-evals.json",
    "evals/release-evidence.schema.json",
    "evals/RELEASE-EVIDENCE.md",
    "evals/gold-principles.md",
    "evals/source-update-cases.md",
    "examples/runtime-decision-preparation.md",
    "examples/runtime-overload.md",
    "examples/integration-architecture.md",
    "examples/audit-finding.md",
    "scripts/check_remote_sources.py",
    "scripts/security_invariants.py",
    "scripts/generate_checksums.py",
    "scripts/requirements.txt",
    "scripts/validate_package.py",
    "scripts/validate_evals.py",
    "scripts/validate_release_evidence.py",
    "scripts/tests/test_remote_source_checker.py",
    "scripts/tests/test_eval_inventory.py",
    "scripts/tests/test_package_validation.py",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(text: str) -> dict[str, Any]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md has no valid YAML frontmatter")
    parsed = yaml.safe_load(match.group(1))
    if not isinstance(parsed, dict):
        raise ValueError("SKILL.md frontmatter must be a mapping")
    return parsed


def validate(root: Path) -> tuple[list[str], list[str], dict[str, int]]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    stats = {"required_files": 0, "skill_md_lines": 0}

    if root.name != "auren-core":
        fail(errors, "Package directory must be named 'auren-core'")

    manifest_path = root / "RELEASE-MANIFEST.json"
    if not manifest_path.is_file():
        return [*errors, "Missing required file: RELEASE-MANIFEST.json"], warnings, stats

    try:
        release = load_json(manifest_path)
        skill_version = str(release["skill_version"])
        if release.get("validated_user_languages") != ["English", "German"]:
            fail(errors, "RELEASE-MANIFEST validated_user_languages must declare the validated English/German quality baseline")
        if release.get("language_behavior") != "respond_in_user_language_when_capable; validated_quality_baseline_en_de":
            fail(errors, "RELEASE-MANIFEST language_behavior must distinguish capability from validated language coverage")
        registry_version = str(release["remote_registry_version"])
        matrix_version = str(release["rights_matrix_version"])
        evidence_rel = str(release["evaluation"]["release_evidence_record"])
        schema_rel = str(release["evaluation"]["release_evidence_schema"])
    except Exception as exc:
        return [*errors, f"Release manifest invalid or incomplete: {exc}"], warnings, stats

    required = [*REQUIRED_STATIC, evidence_rel]
    required = list(dict.fromkeys(required))
    stats["required_files"] = len(required)
    for rel in required:
        if not (root / rel).is_file():
            fail(errors, f"Missing required file: {rel}")

    if errors:
        return errors, warnings, stats

    try:
        skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
        fm = parse_frontmatter(skill_text)
        if fm.get("name") != release.get("package_name"):
            fail(errors, "SKILL.md frontmatter name must match RELEASE-MANIFEST package_name")
        if not isinstance(fm.get("description"), str) or len(fm["description"]) < 80:
            fail(errors, "SKILL.md description is missing or too weak for activation")
        if str(fm.get("metadata", {}).get("version")) != skill_version:
            fail(errors, "SKILL.md metadata version must match RELEASE-MANIFEST")
        if str(fm.get("metadata", {}).get("core-specs-version")) != str(release.get("core_specs_version")):
            fail(errors, "SKILL.md Core Specs version must match RELEASE-MANIFEST")
        if str(fm.get("metadata", {}).get("ai-index-baseline")) != str(release.get("ai_index_baseline")):
            fail(errors, "SKILL.md AI Index baseline must match RELEASE-MANIFEST")
        if str(fm.get("metadata", {}).get("edition")) != str(release.get("edition")):
            fail(errors, "SKILL.md edition must match RELEASE-MANIFEST")
        description = fm.get("description", "").lower()
        for boundary in ("merely because auren is mentioned", "ordinary advice", "generic prompt review"):
            if boundary not in description:
                fail(errors, f"SKILL.md description lacks activation boundary: {boundary}")
        lines = skill_text.count("\n") + 1
        stats["skill_md_lines"] = lines
        if lines > 500:
            fail(errors, f"SKILL.md exceeds 500 lines: {lines}")
    except Exception as exc:
        fail(errors, f"SKILL.md invalid: {exc}")

    try:
        specs = yaml.safe_load((root / "references/auren-core-specs_v2.4.yaml").read_text(encoding="utf-8"))
        if str(specs["auren_core_spec"]["version"]) != str(release.get("core_specs_version")):
            fail(errors, "Embedded Core Specs version does not match RELEASE-MANIFEST")
        canonical = (root / "references/auren-core-specs_v2.4.yaml").read_bytes()
        mirror = (root / "references/auren-core-specs_v2.4.yaml.txt").read_bytes()
        if canonical != mirror:
            fail(errors, "Embedded Core Specs YAML and YAML-TXT must be bit-identical")
    except Exception as exc:
        fail(errors, f"Core Specs validation failed: {exc}")

    try:
        registry = load_json(root / "REMOTE-SOURCE-REGISTRY.json")
        if str(registry.get("registry_version")) != registry_version:
            fail(errors, "Remote registry version must match RELEASE-MANIFEST")
        sources = {s["source_id"]: s for s in registry["sources"]}
        ai = sources["ai_index"]
        if "baseline_local_file" in ai:
            fail(errors, "AI Index must not declare baseline_local_file")
        if ai.get("baseline_snapshot") is not False or ai.get("bundled") is not False:
            fail(errors, "AI Index must be non-bundled with baseline_snapshot false")
        if str(ai.get("baseline_version")) != str(release.get("ai_index_baseline")):
            fail(errors, "AI Index registry baseline must match RELEASE-MANIFEST")
        specs_entry = sources["core_specs"]
        if not specs_entry.get("mirror_urls") or "fallback_urls" in specs_entry:
            fail(errors, "Core Specs must use mirror_urls, not fallback_urls")
        if specs_entry.get("mirror_equivalence_required") is not True:
            fail(errors, "Core Specs mirror equivalence must be required")
        if sources["core_readme"].get("license_marker_required") is not True or sources["core_specs"].get("license_marker_required") is not True:
            fail(errors, "README and Core Specs must require license markers")
        if sources["core_logic"].get("license_marker_required") is not False or sources["guidance"].get("license_marker_required") is not False:
            fail(errors, "Logic and Guidance must not be treated as containing standalone license markers")
        policy_errors = validate_registry_policy(registry["default_policy"])
        for item in policy_errors:
            fail(errors, item)
        if registry["default_policy"].get("documented_invariants") != DOCUMENTED_INVARIANTS:
            fail(errors, "Remote registry documented_invariants must match enforced invariants exactly")
    except Exception as exc:
        fail(errors, f"Remote registry invalid: {exc}")

    try:
        update_schema = load_json(root / "references/update-report.schema.json")
        Draft202012Validator.check_schema(update_schema)
        schema_report_version = str(
            update_schema["properties"]["report_version"]["const"]
        )
        if schema_report_version != REPORT_VERSION:
            fail(
                errors,
                "Update-report schema report_version must match the checker REPORT_VERSION",
            )
        assurance = release.get("security_assurance", {})
        if str(assurance.get("update_report_schema_version")) != REPORT_VERSION:
            fail(
                errors,
                "Release manifest update-report schema version must match the checker REPORT_VERSION",
            )
        if assurance.get("update_report_full_schema_validation") is not True:
            fail(errors, "Release manifest must declare full update-report schema validation")
        if assurance.get("redirect_full_url_validation") is not True:
            fail(errors, "Release manifest must declare full URL validation for redirects")
        if assurance.get("allowed_https_ports") != DOCUMENTED_INVARIANTS.get("allowed_ports"):
            fail(errors, "Release manifest HTTPS ports must match enforced invariants exactly")
        if assurance.get("url_userinfo_rejected") is not True:
            fail(errors, "Release manifest must declare URL-userinfo rejection")
        if assurance.get("external_release_hash_boundary_documented") is not True:
            fail(errors, "Release manifest must declare the external release-hash trust boundary")
        if assurance.get("update_report_classification_regression_coverage") != 6:
            fail(errors, "Release manifest must declare six update-report classification regression branches")
    except Exception as exc:
        fail(errors, f"Update-report schema configuration invalid: {exc}")

    try:
        refs = load_json(root / "EMBEDDED-REFERENCES.json")
        if str(refs.get("package", {}).get("version")) != skill_version:
            fail(errors, "Embedded-reference package version must match RELEASE-MANIFEST")
        ai_ref = next(item for item in refs["references"] if item["reference_id"] == "AUR-005")
        if str(ai_ref.get("name", "").split()[-1].lstrip("v")) != str(release.get("ai_index_baseline")):
            fail(errors, "Embedded-reference AI Index baseline must match RELEASE-MANIFEST")
        for ref in refs["references"]:
            if ref.get("embedded"):
                path = root / ref["embedded_path"]
                if not path.is_file():
                    fail(errors, f"Embedded reference missing: {ref['embedded_path']}")
                    continue
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                if actual != ref.get("package_sha256"):
                    fail(errors, f"Embedded reference hash mismatch: {ref['reference_id']}")
    except Exception as exc:
        fail(errors, f"Embedded reference manifest invalid: {exc}")

    try:
        matrix = load_json(root / "RIGHTS-LICENSE-EDITION-MATRIX.json")
        if str(matrix.get("matrix_version")) != matrix_version:
            fail(errors, "Rights matrix version must match RELEASE-MANIFEST")
        if str(matrix.get("skill_version")) != skill_version:
            fail(errors, "Rights matrix skill version must match RELEASE-MANIFEST")
        if str(matrix.get("edition")) != str(release.get("edition")):
            fail(errors, "Rights matrix edition must match RELEASE-MANIFEST")
    except Exception as exc:
        fail(errors, f"Rights matrix invalid: {exc}")

    try:
        catalog_rel = str(release["optional_semantic_reference_catalog"])
        catalog_version = str(release["optional_semantic_reference_catalog_version"])
        catalog = load_json(root / catalog_rel)
        if str(catalog.get("catalog_version")) != catalog_version:
            fail(errors, "Optional semantic-reference catalog version must match RELEASE-MANIFEST")
        if str(catalog.get("skill_version")) != skill_version:
            fail(errors, "Optional semantic-reference catalog skill version must match RELEASE-MANIFEST")
        if str(catalog.get("edition")) != str(release.get("edition")):
            fail(errors, "Optional semantic-reference catalog edition must match RELEASE-MANIFEST")
        policy = catalog.get("policy", {})
        expected_false = (
            "automatic_fetch",
            "automatic_activation",
            "required_for_core_operation",
            "may_override_core",
            "package_license_applies",
            "crawl_discovered_links",
            "reconstruct_unpublished_methodology",
        )
        for field in expected_false:
            if policy.get(field) is not False:
                fail(errors, f"Optional semantic-reference policy must keep {field}=false")
        if policy.get("host_mediated_access_only") is not True:
            fail(errors, "Optional semantic-reference access must be host-mediated only")
        if policy.get("on_unavailable") != "continue_with_open_core":
            fail(errors, "Optional semantic references must degrade to the Open Core")
        refs_list = catalog.get("references", [])
        ids = [item.get("reference_id") for item in refs_list]
        if len(ids) != len(set(ids)):
            fail(errors, "Optional semantic-reference IDs must be unique")
        required_ids = {"AUR-009", "AUR-010", "AUR-011", "AUR-012", "AUR-015"}
        if set(ids) != required_ids:
            fail(errors, f"Optional semantic-reference catalog must contain exactly {sorted(required_ids)}")
        for item in refs_list:
            for field in ("bundled", "required_for_core_operation", "may_override_core", "package_license_applies"):
                if item.get(field) is not False:
                    fail(errors, f"Optional semantic reference {item.get('reference_id')} must keep {field}=false")
            try:
                validate_url(str(item["canonical_url"]), set(DOCUMENTED_INVARIANTS["allowed_hostnames"]))
            except Exception as exc:
                fail(errors, f"Optional semantic reference {item.get('reference_id')} has invalid canonical URL: {exc}")
        assurance = release.get("semantic_extension_assurance", {})
        if str(assurance.get("catalog_version")) != catalog_version:
            fail(errors, "Semantic-extension assurance catalog version must match RELEASE-MANIFEST")
        if assurance.get("optional_reference_count") != len(refs_list):
            fail(errors, "Semantic-extension assurance reference count must match catalog")
        for field in ("automatic_fetch", "required_for_core_operation", "may_override_core", "package_license_applies", "reconstruct_unpublished_methodology"):
            if assurance.get(field) is not False:
                fail(errors, f"Semantic-extension assurance must keep {field}=false")
        matrix_by_id = {item.get("id"): item for item in matrix.get("resources", [])}
        for rid in {"AUR-009", "AUR-010", "AUR-011", "AUR-012"}:
            row = matrix_by_id.get(rid, {})
            if row.get("embedded") is not False or row.get("cataloged") is not True:
                fail(errors, f"Rights matrix must mark {rid} as cataloged and non-embedded")
    except Exception as exc:
        fail(errors, f"Optional semantic-reference catalog invalid: {exc}")

    try:
        evaluation = release["evaluation"]
        if evaluation.get("bilingual_parity") is not True:
            fail(errors, "Release manifest must declare bilingual eval parity")
        if evaluation.get("description_trigger_suite") is not True:
            fail(errors, "Release manifest must declare description-trigger suite")
        if evaluation.get("full_trigger_class_bilingual_parity") is not True:
            fail(errors, "Release manifest must declare full bilingual parity for every trigger class")
        if evaluation.get("high_risk_path_bilingual_parity") is not True:
            fail(errors, "Release manifest must declare bilingual parity for high-risk paths")
        if evaluation.get("full_release_evidence_schema_validation") is not True:
            fail(errors, "Release manifest must declare full release-evidence JSON-Schema validation")
        if not (root / evidence_rel).is_file() or not (root / schema_rel).is_file():
            fail(errors, "Release-evidence paths declared by manifest must exist")
        evidence = load_json(root / evidence_rel)
        if str(evidence.get("release", {}).get("skill_version")) != skill_version:
            fail(errors, "Release-evidence skill version must match RELEASE-MANIFEST")
        if str(evidence.get("schema_version")) != str(evaluation.get("release_evidence_schema_version")):
            fail(errors, "Release-evidence schema version must match RELEASE-MANIFEST")
        package_runs = [
            run for run in evidence.get("evaluation_runs", [])
            if run.get("id") == "package-validation"
        ]
        if len(package_runs) != 1:
            fail(errors, "Release evidence must contain exactly one package-validation run")
        else:
            recorded_lines = package_runs[0].get("result", {}).get("skill_md_lines")
            if recorded_lines != stats.get("skill_md_lines"):
                fail(errors, "Release-evidence package-validation skill_md_lines must match the current SKILL.md artifact")

        def parse_evidence_time(value: Any, field_name: str) -> datetime | None:
            if not isinstance(value, str):
                fail(errors, f"Release-evidence {field_name} must be an RFC 3339 date-time string")
                return None
            try:
                parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                fail(errors, f"Release-evidence {field_name} is not a valid RFC 3339 date-time")
                return None
            if parsed.tzinfo is None:
                fail(errors, f"Release-evidence {field_name} must include a timezone")
                return None
            return parsed.astimezone(timezone.utc)

        generated_at = parse_evidence_time(evidence.get("generated_at"), "generated_at")
        executed_times = []
        for run in evidence.get("evaluation_runs", []):
            parsed = parse_evidence_time(run.get("executed_at"), f"evaluation run {run.get('id', '<unknown>')} executed_at")
            if parsed is not None:
                executed_times.append(parsed)
        if generated_at is not None and executed_times and generated_at < max(executed_times):
            fail(errors, "Release-evidence generated_at must be greater than or equal to every recorded evaluation run executed_at")
    except Exception as exc:
        fail(errors, f"Release manifest evaluation configuration invalid: {exc}")

    privacy = (root / "PRIVACY-AND-DATA-MINIMIZATION.md").read_text(encoding="utf-8")
    readme = (root / "README.md").read_text(encoding="utf-8")
    for phrase in ["never request passwords", "No user content is sent", "do not claim that a conversation is confidential"]:
        if phrase.lower() not in privacy.lower() and phrase.lower() not in readme.lower():
            fail(errors, f"Privacy rule missing concept: {phrase}")

    security_text = (root / "SECURITY.md").read_text(encoding="utf-8").lower()
    if "external release integrity reference" not in security_text or "release zip" not in security_text:
        fail(errors, "SECURITY.md must document the external release ZIP integrity-reference boundary")

    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## {skill_version} —" not in changelog:
        fail(errors, "CHANGELOG.md lacks the current release heading")

    prohibited_names = ["ai-index.txt", "ANALYSE_systemische-haltung-und-ethik.md", "SKILL-GOVERNANCE-REFERENCE-POLICY"]
    for path in root.rglob("*"):
        if path.is_file() and path.name in prohibited_names:
            fail(errors, f"Prohibited source embedded: {path.relative_to(root)}")

    for py in root.rglob("*.py"):
        text = py.read_text(encoding="utf-8")
        if "SPDX-License-Identifier: MIT" not in text:
            fail(errors, f"Python file lacks MIT SPDX header: {py.relative_to(root)}")

    checksum_path = root / "CHECKSUMS.sha256"
    if checksum_path.is_file():
        try:
            listed: set[str] = set()
            for line in checksum_path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                digest_value, rel = line.split("  ", 1)
                listed.add(rel)
                target = root / rel
                if not target.is_file():
                    fail(errors, f"Checksum target missing: {rel}")
                    continue
                actual = hashlib.sha256(target.read_bytes()).hexdigest()
                if actual != digest_value:
                    fail(errors, f"Checksum mismatch: {rel}")
            expected = {
                path.relative_to(root).as_posix()
                for path in root.rglob("*")
                if path.is_file() and path != checksum_path and "__pycache__" not in path.parts and path.suffix != ".pyc"
            }
            missing = sorted(expected - listed)
            extra = sorted(listed - expected)
            if missing:
                fail(errors, f"Files missing from checksum manifest: {missing}")
            if extra:
                fail(errors, f"Unexpected checksum entries: {extra}")
        except Exception as exc:
            fail(errors, f"Checksum manifest invalid: {exc}")

    return errors, warnings, stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the AUREN Core Skill package")
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    args = parser.parse_args()
    errors, warnings, stats = validate(args.root)

    if errors:
        print("VALIDATION FAILED")
        for item in errors:
            print(f"- ERROR: {item}")
        for item in warnings:
            print(f"- WARNING: {item}")
        return 1

    print("VALIDATION PASSED")
    print(f"- Required files: {stats['required_files']}")
    print(f"- SKILL.md lines: {stats['skill_md_lines']}")
    print(f"- Security invariants: {len(DOCUMENTED_INVARIANTS)} exact checks")
    print(f"- Warnings: {len(warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
