#!/usr/bin/env python3
"""Validate migration, gap, and waiver registries strictly."""

from __future__ import annotations

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.ctrepo.policy_validation import validate_all_policy_registries


def main() -> int:
    errors = validate_all_policy_registries()
    if errors:
        print("Policy registry errors:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Policy registries: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
