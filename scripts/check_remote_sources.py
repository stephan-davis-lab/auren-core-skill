#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Stephan A. Davis

"""Allowlisted, privacy-preserving AUREN Core remote source checker."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from security_invariants import (
    ALLOWED_HOSTNAMES,
    ALLOWED_PORTS,
    DOCUMENTED_INVARIANTS,
    REQUEST_METHOD,
    validate_registry_policy,
)

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install scripts/requirements.txt") from exc

REPORT_VERSION = "1.1"
USER_AGENT = "AUREN-Core-Source-Checker/1.2.5"


def normalize(data: bytes) -> bytes:
    text = data.decode("utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n"
    return text.encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class SameHostRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, allowed_hostnames: set[str]):
        super().__init__()
        self.allowed_hostnames = allowed_hostnames

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        try:
            validate_url(newurl, self.allowed_hostnames)
        except ValueError as exc:
            raise urllib.error.HTTPError(
                newurl, code, f"Redirect target blocked: {exc}", headers, fp
            ) from exc
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def validate_url(
    url: str,
    allowed_hostnames: set[str],
    allowed_ports: frozenset[int] = ALLOWED_PORTS,
) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("Only HTTPS URLs are allowed")
    if parsed.hostname not in allowed_hostnames:
        raise ValueError("Hostname is not allowlisted")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("URL credentials are not allowed")
    try:
        port = parsed.port
    except ValueError as exc:
        raise ValueError("URL contains an invalid port") from exc
    if port is not None and port not in allowed_ports:
        raise ValueError("Only the standard HTTPS port 443 is allowed")
    if parsed.query or parsed.fragment:
        raise ValueError("Query strings and fragments are not allowed")


def fetch(url: str, allowed_hostnames: set[str], timeout: int, max_bytes: int) -> bytes:
    validate_url(url, allowed_hostnames)
    request = urllib.request.Request(url, method=REQUEST_METHOD, headers={"User-Agent": USER_AGENT, "Accept": "text/plain, text/markdown, application/yaml, */*;q=0.1"})
    context = ssl.create_default_context()
    # urllib's opener does not accept a context directly for all handlers; install HTTPS handler.
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=context), SameHostRedirectHandler(allowed_hostnames))
    with opener.open(request, timeout=timeout) as response:
        data = response.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise ValueError(f"Source exceeds max_bytes={max_bytes}")
        return data


def load_fixture(source_dir: Path, source_id: str, index: int) -> bytes:
    candidates = [
        source_dir / f"{source_id}.bin" if index == 0 else source_dir / f"{source_id}.mirror{index}.bin",
        source_dir / f"{source_id}.txt" if index == 0 else source_dir / f"{source_id}.mirror{index}.txt",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.read_bytes()
    raise FileNotFoundError(f"No fixture found for {source_id} index {index}")


def extract_version(source_id: str, text: str) -> str | None:
    if source_id == "core_specs":
        try:
            parsed = yaml.safe_load(text)
            return str(parsed["auren_core_spec"]["version"])
        except Exception:
            return None
    if source_id == "guidance":
        try:
            parsed = yaml.safe_load(text)
            return str(parsed["orientation_framework"]["version"])
        except Exception:
            return None
    patterns = [
        r'^Version:\s*["\']?([^"\'\s]+)',
        r'\(v([0-9]+(?:\.[0-9]+)+)\)',
        r'\bVersion:\s*([0-9]+(?:\.[0-9]+)+)',
        r'^#\s*AUREN Core Specs.*?[—–-]\s*v([0-9]+(?:\.[0-9]+)+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def extract_license(source_id: str, text: str) -> str | None:
    if source_id == "core_specs":
        try:
            parsed = yaml.safe_load(text)
            return str(parsed["auren_core_spec"]["license"]["type"])
        except Exception:
            return None
    if re.search(r"CC\s+BY-SA\s+4\.0", text, re.IGNORECASE):
        return "CC BY-SA 4.0"
    return None


def validate_structured(source_id: str, text: str) -> tuple[bool, str | None]:
    if source_id not in {"core_specs", "guidance"}:
        return True, None
    try:
        parsed = yaml.safe_load(text)
        if not isinstance(parsed, dict):
            return False, "YAML root is not a mapping"
        expected = "auren_core_spec" if source_id == "core_specs" else "orientation_framework"
        if expected not in parsed:
            return False, f"Missing YAML root key: {expected}"
        return True, None
    except Exception as exc:
        return False, f"YAML validation failed: {type(exc).__name__}: {str(exc)[:180]}"


def classify(source: dict[str, Any], remote_version: str | None, remote_norm_hash: str, remote_license: str | None) -> tuple[str, str, list[str]]:
    expected_license = source.get("expected_license", "")
    if source.get("license_marker_required", False) and expected_license == "CC BY-SA 4.0" and remote_license != "CC BY-SA 4.0":
        return "license_or_rights_change", "Block adoption and perform a rights review.", ["license_scope_review"]

    if remote_norm_hash == source.get("baseline_sha256_normalized"):
        return "no_change", "No adoption action required.", []

    sid = source["source_id"]
    baseline_version = str(source.get("baseline_version"))
    version_changed = remote_version is not None and remote_version != baseline_version

    if sid == "ai_index":
        return "semantic_context_update", "Review relevant semantic changes; do not change operational behavior automatically.", []
    if sid == "core_readme":
        return "documentation_update", "Review semantics and package documentation before adoption.", ["documentation_consistency"]
    if sid == "core_logic":
        classification = "operational_breaking_change" if version_changed else "operational_compatible_change"
        return classification, "Review diff, YAML consistency, rights, and regression evals before a new release.", ["yaml_logic_consistency", "runtime_regression", "safety_regression"]
    if sid == "core_specs":
        classification = "operational_breaking_change" if version_changed else "ambiguous_change"
        return classification, "Block runtime adoption; prepare a reviewed release with full regression evals.", ["schema_validation", "mode_priority_regression", "crisis_regression", "dependency_regression", "privacy_regression"]
    if sid == "guidance":
        return "documentation_update", "Review orientation-policy changes before package adoption.", ["guidance_consistency", "human_responsibility_regression"]
    return "ambiguous_change", "Review manually.", ["manual_review"]


def check_source(source: dict[str, Any], policy: dict[str, Any], source_dir: Path | None) -> dict[str, Any]:
    sid = source["source_id"]
    urls = [source["canonical_url"], *source.get("mirror_urls", [])]
    allowed_hostnames = set(ALLOWED_HOSTNAMES)
    fetched: list[dict[str, Any]] = []

    for index, url in enumerate(urls):
        try:
            if source_dir is None and source.get("retrieval_policy") == "manual_host_review_only":
                raise ValueError("Manual-only pinned reference outside the fixed checker allowlist; no network request made")
            data = load_fixture(source_dir, sid, index) if source_dir else fetch(url, allowed_hostnames, int(policy["timeout_seconds"]), int(policy["max_bytes"]))
            norm = normalize(data)
            text = norm.decode("utf-8")
            valid, error = validate_structured(sid, text)
            fetched.append({
                "url": url,
                "status": "success" if valid else "invalid",
                "bytes": len(data),
                "sha256": digest(data),
                "sha256_normalized": digest(norm),
                "version": extract_version(sid, text),
                "license": extract_license(sid, text),
                "validation_error": error,
                "_text": text,
            })
        except Exception as exc:
            fetched.append({
                "url": url,
                "status": "unavailable",
                "error": f"{type(exc).__name__}: {str(exc)[:220]}",
            })

    public_fetched = [{k: v for k, v in item.items() if not k.startswith("_")} for item in fetched]
    canonical = fetched[0]
    result: dict[str, Any] = {
        "source_id": sid,
        "role": source["role"],
        "fetch_status": canonical["status"],
        "baseline": {
            "version": source.get("baseline_version"),
            "sha256": source.get("baseline_sha256"),
            "sha256_normalized": source.get("baseline_sha256_normalized"),
        },
        "retrievals": public_fetched,
        "automatic_activation": False,
    }

    if canonical["status"] == "unavailable":
        result.update(classification="fetch_unavailable", operational_impact="unknown", license_impact="unknown", required_evals=[], recommendation="Keep the embedded approved source active and do not claim currentness.")
        return result
    if canonical["status"] == "invalid":
        result.update(classification="invalid_source", operational_impact="blocked", license_impact="unknown", required_evals=[], recommendation="Block adoption and inspect the source manually.")
        return result

    if source.get("mirror_equivalence_required"):
        if any(item["status"] != "success" for item in fetched[1:]):
            result.update(classification="fetch_unavailable", operational_impact="blocked", license_impact="unknown", required_evals=[], recommendation="Mirror verification is required; block adoption until every mirror is available.")
            return result
        hashes = {item["sha256_normalized"] for item in fetched}
        if len(hashes) != 1:
            result.update(classification="mirror_divergence", operational_impact="blocked", license_impact="unknown", required_evals=["mirror_equivalence"], recommendation="Block adoption. Reconcile canonical YAML and YAML-TXT.")
            return result

    classification, recommendation, required_evals = classify(source, canonical.get("version"), canonical["sha256_normalized"], canonical.get("license"))
    operational_impact = "none" if classification in {"no_change", "metadata_only", "semantic_context_update", "documentation_update"} else "review_required"
    license_impact = "review_required" if classification == "license_or_rights_change" else "none_detected"
    result.update(
        remote={
            "version": canonical.get("version"),
            "sha256": canonical["sha256"],
            "sha256_normalized": canonical["sha256_normalized"],
            "license": canonical.get("license"),
        },
        classification=classification,
        operational_impact=operational_impact,
        license_impact=license_impact,
        required_evals=required_evals,
        recommendation=recommendation,
    )
    return result


def build_report(
    registry: dict[str, Any],
    source_dir: Path | None = None,
    checked_at: str | None = None,
) -> dict[str, Any]:
    """Build the same complete report structure used by the command-line checker."""

    policy = registry["default_policy"]
    policy_errors = validate_registry_policy(policy)
    if policy_errors:
        raise ValueError("; ".join(policy_errors))

    return {
        "report_version": REPORT_VERSION,
        "checked_at": checked_at
        or dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "registry_version": registry["registry_version"],
        "automatic_activation": False,
        "privacy": {
            "user_content_sent": False,
            "request_method": DOCUMENTED_INVARIANTS["request_method"],
            "crawl_discovered_links": DOCUMENTED_INVARIANTS["crawl_discovered_links"],
        },
        "sources": [
            check_source(source, policy, source_dir) for source in registry["sources"]
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=Path("REMOTE-SOURCE-REGISTRY.json"))
    parser.add_argument("--output", type=Path, default=Path("source-update-report.json"))
    parser.add_argument("--source-dir", type=Path, help="Offline fixture directory; never used in normal remote checks.")
    args = parser.parse_args()

    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    try:
        report = build_report(registry, args.source_dir)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
