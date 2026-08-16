#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Stephan A. Davis

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "jsonschema is required. Install dependencies from scripts/requirements.txt"
    ) from exc

DEFAULT_SCHEMA = "evals/release-evidence.schema.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def format_json_path(path_parts: list[Any]) -> str:
    if not path_parts:
        return "$"
    result = "$"
    for part in path_parts:
        if isinstance(part, int):
            result += f"[{part}]"
        else:
            result += f".{part}"
    return result


def validate_documents(evidence: Any, schema: Any) -> list[str]:
    errors: list[str] = []
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        return [f"Invalid release-evidence schema: {exc.message}"]

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(evidence), key=lambda item: list(item.absolute_path)):
        location = format_json_path(list(error.absolute_path))
        errors.append(f"{location}: {error.message}")
    return errors


def validate_files(evidence_path: Path, schema_path: Path) -> list[str]:
    try:
        evidence = load_json(evidence_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot load release evidence {evidence_path}: {exc}"]
    try:
        schema = load_json(schema_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot load release-evidence schema {schema_path}: {exc}"]
    return validate_documents(evidence, schema)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an AUREN Core release-evidence record against its full JSON Schema"
    )
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    parser.add_argument("--evidence", help="Override the manifest-declared evidence record")
    parser.add_argument("--schema", help="Override the manifest-declared evidence schema")
    args = parser.parse_args()

    root = args.root.resolve()
    if args.evidence or args.schema:
        evidence_rel = args.evidence
        schema_rel = args.schema or DEFAULT_SCHEMA
        if not evidence_rel:
            raise SystemExit("--evidence is required when overriding manifest paths")
    else:
        try:
            manifest = load_json(root / "RELEASE-MANIFEST.json")
            evaluation = manifest["evaluation"]
            evidence_rel = evaluation["release_evidence_record"]
            schema_rel = evaluation.get("release_evidence_schema", DEFAULT_SCHEMA)
        except (OSError, json.JSONDecodeError, KeyError) as exc:
            raise SystemExit(f"Cannot resolve release-evidence paths from RELEASE-MANIFEST.json: {exc}") from exc
    evidence_path = root / evidence_rel
    schema_path = root / schema_rel
    errors = validate_files(evidence_path, schema_path)
    if errors:
        print("RELEASE-EVIDENCE SCHEMA VALIDATION FAILED")
        for error in errors:
            print(f"- ERROR: {error}")
        return 1

    print("RELEASE-EVIDENCE SCHEMA VALIDATION PASSED")
    print(f"- Evidence: {evidence_path.relative_to(root)}")
    print(f"- Schema: {schema_path.relative_to(root)}")
    print("- Draft: JSON Schema 2020-12")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
