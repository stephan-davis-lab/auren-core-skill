#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Stephan A. Davis

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic SHA-256 checksums for an AUREN Core package.")
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    parser.add_argument("--output", default="CHECKSUMS.sha256")
    args = parser.parse_args()
    root = args.root.resolve()
    output = root / args.output
    rows = []
    for path in sorted(
        p for p in root.rglob("*")
        if p.is_file() and p != output and "__pycache__" not in p.parts and p.suffix != ".pyc"
    ):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {path.relative_to(root).as_posix()}")
    output.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"Wrote {output} with {len(rows)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
