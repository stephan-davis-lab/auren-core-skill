#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Stephan A. Davis

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_release_evidence import validate_files as validate_evidence_files

REQUIRED_TRIGGER_CLASSES = {
    "casual_mention",
    "ordinary_advice",
    "reflective_complexity",
    "technical_execution",
    "decision_delegation",
    "explicit_integration",
    "explicit_audit",
    "generic_prompt_review",
    "generic_architecture",
    "host_safety_priority",
}

REQUIRED_RISK_PARITY_GROUPS = {
    "overload_stabilization",
    "high_risk_medical_referral",
    "privacy_minimize_identifiers",
    "privacy_no_confidentiality_claim",
    "certainty_loop",
    "no_forced_positivity",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def release_config(root: Path) -> tuple[str, Path, Path, str]:
    manifest = load_json(root / "RELEASE-MANIFEST.json")
    evaluation = manifest["evaluation"]
    return (
        str(manifest["skill_version"]),
        root / evaluation["release_evidence_record"],
        root / evaluation["release_evidence_schema"],
        str(evaluation["release_evidence_schema_version"]),
    )


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = root / "RELEASE-MANIFEST.json"
    main_path = root / "evals/evals.json"
    trigger_path = root / "evals/description-trigger-evals.json"

    for path in (manifest_path, main_path, trigger_path):
        if not path.is_file():
            errors.append(f"Missing evaluation file: {path.relative_to(root)}")
    if errors:
        return errors

    try:
        version, evidence_path, schema_path, expected_schema_version = release_config(root)
    except Exception as exc:
        return [f"Cannot resolve evaluation release configuration: {exc}"]

    for path in (evidence_path, schema_path):
        if not path.is_file():
            errors.append(f"Missing evaluation file: {path.relative_to(root)}")
    if errors:
        return errors

    main = load_json(main_path)
    triggers = load_json(trigger_path)
    evidence = load_json(evidence_path)
    schema = load_json(schema_path)

    if main.get("skill_version") != version:
        errors.append("Primary eval inventory version mismatch")
    if triggers.get("skill_version") != version:
        errors.append("Description-trigger inventory version mismatch")
    if evidence.get("release", {}).get("skill_version") != version:
        errors.append("Release-evidence version mismatch")
    if evidence.get("schema_version") != expected_schema_version:
        errors.append(
            f"Release-evidence schema_version must be {expected_schema_version}"
        )
    if schema.get("title") != "AUREN Core Release Evidence":
        errors.append("Release-evidence schema title mismatch")

    schema_errors = validate_evidence_files(evidence_path, schema_path)
    errors.extend(f"Release-evidence schema validation: {item}" for item in schema_errors)

    cases = main.get("cases", [])
    ids = [case.get("id") for case in cases]
    if len(ids) != len(set(ids)):
        errors.append("Primary eval case IDs must be unique")
    for case in cases:
        for field in ("id", "mode", "activation", "language", "prompt", "expected", "must_not"):
            if field not in case:
                errors.append(f"Primary eval {case.get('id', '<unknown>')} missing {field}")
        if case.get("language") not in {"en", "de"}:
            errors.append(f"Primary eval {case.get('id')} has invalid language")
        if not case.get("expected") or not case.get("must_not"):
            errors.append(f"Primary eval {case.get('id')} needs expected and must_not criteria")

    for mode in ("runtime", "integration", "audit"):
        languages = {case.get("language") for case in cases if case.get("mode") == mode}
        if not {"en", "de"}.issubset(languages):
            errors.append(f"Missing English/German parity for mode: {mode}")
    crisis_languages = {
        case.get("language")
        for case in cases
        if "crisis" in str(case.get("activation", "")) or "crisis" in str(case.get("id", ""))
    }
    if not {"en", "de"}.issubset(crisis_languages):
        errors.append("Missing English/German crisis parity")
    nonactivation_languages = {
        case.get("language") for case in cases if case.get("activation") == "should_not_activate"
    }
    if not {"en", "de"}.issubset(nonactivation_languages):
        errors.append("Missing English/German nonactivation parity")

    risk_groups = {case.get("risk_parity_group") for case in cases if case.get("risk_parity_group")}
    missing_risk_groups = REQUIRED_RISK_PARITY_GROUPS - risk_groups
    unexpected_risk_groups = risk_groups - REQUIRED_RISK_PARITY_GROUPS
    if missing_risk_groups:
        errors.append(f"Missing risk parity groups: {sorted(missing_risk_groups)}")
    if unexpected_risk_groups:
        errors.append(f"Unexpected risk parity groups: {sorted(unexpected_risk_groups)}")
    for group in sorted(REQUIRED_RISK_PARITY_GROUPS):
        languages = {
            case.get("language")
            for case in cases
            if case.get("risk_parity_group") == group
        }
        if languages != {"en", "de"}:
            errors.append(
                f"Risk path must have exact English/German parity: {group}; found {sorted(languages)}"
            )

    trigger_cases = triggers.get("cases", [])
    trigger_ids = [case.get("id") for case in trigger_cases]
    if len(trigger_ids) != len(set(trigger_ids)):
        errors.append("Description-trigger case IDs must be unique")
    classes = {case.get("trigger_class") for case in trigger_cases}
    missing_classes = REQUIRED_TRIGGER_CLASSES - classes
    unexpected_classes = classes - REQUIRED_TRIGGER_CLASSES
    if missing_classes:
        errors.append(f"Missing trigger classes: {sorted(missing_classes)}")
    if unexpected_classes:
        errors.append(f"Unexpected trigger classes: {sorted(unexpected_classes)}")

    for case in trigger_cases:
        for field in (
            "id",
            "language",
            "trigger_class",
            "prompt",
            "expected_activation",
            "expected_mode",
            "rationale",
            "must_not",
        ):
            if field not in case:
                errors.append(f"Description-trigger eval {case.get('id', '<unknown>')} missing {field}")
        if case.get("language") not in {"en", "de"}:
            errors.append(f"Description-trigger eval {case.get('id')} has invalid language")
        if not case.get("must_not"):
            errors.append(f"Description-trigger eval {case.get('id')} needs must_not criteria")

    for trigger_class in sorted(REQUIRED_TRIGGER_CLASSES):
        languages = {
            case.get("language")
            for case in trigger_cases
            if case.get("trigger_class") == trigger_class
        }
        if languages != {"en", "de"}:
            errors.append(
                f"Trigger class must have exactly English/German coverage: {trigger_class}; found {sorted(languages)}"
            )

    behavioral = evidence.get("behavioral_model_evidence", {})
    if behavioral.get("status") == "not_run" and behavioral.get("hosts"):
        errors.append("Behavioral evidence marked not_run must not list executed hosts")
    if evidence.get("release", {}).get("evidence_status") not in {"complete", "partial", "draft"}:
        errors.append("Invalid release evidence status")

    run_ids = [item.get("id") for item in evidence.get("evaluation_runs", [])]
    if len(run_ids) != len(set(run_ids)):
        errors.append("Release-evidence evaluation run IDs must be unique")
    if "release-evidence-schema-validation" not in run_ids:
        errors.append("Release evidence must record full JSON-Schema validation")
    if "security-invariant-regression" not in run_ids:
        errors.append("Release evidence must record security-invariant regression testing")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate AUREN Core evaluation inventories and release evidence"
    )
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.root.resolve()
    errors = validate(root)
    if errors:
        print("EVAL VALIDATION FAILED")
        for error in errors:
            print(f"- ERROR: {error}")
        return 1
    main_inventory = load_json(root / "evals/evals.json")
    trigger_inventory = load_json(root / "evals/description-trigger-evals.json")
    print("EVAL VALIDATION PASSED")
    print(f"- Primary eval cases: {len(main_inventory['cases'])}")
    print(f"- Description-trigger cases: {len(trigger_inventory['cases'])}")
    print("- Primary bilingual parity: Runtime, Integration, Audit, crisis, nonactivation")
    print(f"- High-risk paths with full English/German parity: {len(REQUIRED_RISK_PARITY_GROUPS)}")
    print(f"- Trigger classes with full English/German parity: {len(REQUIRED_TRIGGER_CLASSES)}")
    print("- Release evidence: full JSON Schema 2020-12 validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
