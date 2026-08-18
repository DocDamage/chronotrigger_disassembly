#!/usr/bin/env python3
"""Fail when prohibited ROMs, generated caches, or ZIP archives are tracked."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent


def main() -> int:
    tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
    errors = []
    for path in tracked:
        lower = path.lower()
        if lower.endswith((".sfc", ".smc")):
            errors.append(f"commercial ROM path is tracked: {path}")
        if lower.endswith(".zip"):
            errors.append(f"binary archive is tracked: {path}")
        if "raw_xref_index" in lower and lower.endswith(".json"):
            errors.append(f"generated raw xref cache is tracked: {path}")
    if errors:
        print("Binary/cache policy errors:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Binary/cache policy: current tracked tree is clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
