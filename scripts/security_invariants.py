#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Stephan A. Davis

"""Shared, non-configurable security invariants for remote source checks."""

from __future__ import annotations

from typing import Any

DOCUMENTED_INVARIANTS: dict[str, Any] = {
    "https_only": True,
    "allowed_hostnames": ["stephanadavis.de"],
    "allowed_ports": [443],
    "url_userinfo_allowed": False,
    "follow_cross_domain_redirects": False,
    "request_method": "GET",
    "request_body": None,
    "crawl_discovered_links": False,
    "hash_algorithm": "sha256",
    "normalization": [
        "strip_utf8_bom",
        "normalize_line_endings_to_lf",
        "ensure_single_final_newline",
    ],
}

ALLOWED_HOSTNAMES = frozenset(DOCUMENTED_INVARIANTS["allowed_hostnames"])
ALLOWED_PORTS = frozenset(DOCUMENTED_INVARIANTS["allowed_ports"])
REQUEST_METHOD = DOCUMENTED_INVARIANTS["request_method"]


def validate_registry_policy(policy: dict[str, Any]) -> list[str]:
    """Return errors when registry documentation diverges from enforced behavior."""

    errors: list[str] = []
    if policy.get("user_content_in_requests") is not False:
        errors.append("Registry must prohibit user content in requests")
    if policy.get("user_content_in_logs") is not False:
        errors.append("Registry must prohibit user content in logs")
    if policy.get("documented_invariants") != DOCUMENTED_INVARIANTS:
        errors.append(
            "Registry documented_invariants must exactly match the checker-enforced security invariants"
        )
    return errors
