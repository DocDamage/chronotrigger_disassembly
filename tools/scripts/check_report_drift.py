#!/usr/bin/env python3
"""Check report drift: ensure reports match freshly generated outputs from canonical manifests."""

import json
import os
import subprocess
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

def main() -> int:
    print("Checking report drift across generated reports...")
    
    # 1. Regenerate coverage report
    ret_cov = subprocess.run([sys.executable, "tools/scripts/generate_coverage.py", "--strict"], capture_output=True, text=True)
    if ret_cov.returncode != 0:
        print(f"Error regenerating coverage report:\n{ret_cov.stderr}")
        return 1

    # 2. Check coverage.json validity and metrics presence
    cov_path = "reports/coverage.json"
    if not os.path.exists(cov_path):
        print(f"Missing {cov_path}")
        return 1

    with open(cov_path, "r", encoding="utf-8") as f:
        cov_data = json.load(f)
        assert "provenance" in cov_data, "Missing provenance in coverage.json"
        assert "metrics" in cov_data, "Missing metrics in coverage.json"
        assert cov_data["metrics"]["total_canonical_manifests_count"] == 961, "Mismatch in canonical manifests count"

    # 3. Regenerate toolkit doctor
    ret_doc = subprocess.run([sys.executable, "tools/scripts/toolkit_doctor.py", "--strict"], capture_output=True, text=True)
    if ret_doc.returncode != 0:
        print(f"Error running toolkit doctor:\n{ret_doc.stderr}")
        return 1

    # 4. Check range ownership report
    ret_own = subprocess.run([sys.executable, "tools/scripts/validate_range_ownership.py", "--output-json", "reports/range_ownership_report.json"], capture_output=True, text=True)
    if ret_own.returncode != 0:
        print(f"Error running range ownership report:\n{ret_own.stderr}")
        return 1

    print("Report drift check PASSED: all generated reports match current canonical state.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
