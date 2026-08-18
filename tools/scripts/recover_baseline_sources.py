#!/usr/bin/env python3
"""Recover omitted source manifests from baseline commit 253f2f6c into passes/manifests/legacy/."""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main():
    legacy_dir = "passes/manifests/legacy"
    os.makedirs(legacy_dir, exist_ok=True)

    with open("reports/remediation/corrective_baseline.json", "r", encoding="utf-8") as f:
        base_data = json.load(f)

    baseline_manifests = base_data["manifests"]
    print(f"Loaded {len(baseline_manifests)} manifests from corrective baseline.")

    recovered_count = 0
    verified_count = 0

    for m in baseline_manifests:
        orig_fn = os.path.basename(m["path"])
        expected_sha = m["sha256"]
        blob_id = m["blob_id"]

        # Check if already present in legacy_dir with matching hash
        target_path = os.path.join(legacy_dir, orig_fn)
        file_present = False
        if os.path.exists(target_path):
            with open(target_path, "rb") as f:
                if sha256_bytes(f.read()) == expected_sha:
                    file_present = True
                    verified_count += 1

        if not file_present:
            # If target_path exists with different hash (name collision between direct and suffixed), use a distinct name
            if os.path.exists(target_path):
                target_path = os.path.join(legacy_dir, f"{orig_fn[:-5]}_direct.json")
                if os.path.exists(target_path):
                    with open(target_path, "rb") as f:
                        if sha256_bytes(f.read()) == expected_sha:
                            file_present = True
                            verified_count += 1

            if not file_present:
                # Extract from git blob
                raw = subprocess.run(["git", "cat-file", "-p", blob_id], capture_output=True, check=True).stdout
                actual_sha = sha256_bytes(raw)
                assert actual_sha == expected_sha, f"SHA mismatch on recovery of {m['path']}: {actual_sha} != {expected_sha}"
                with open(target_path, "wb") as f:
                    f.write(raw)
                recovered_count += 1
                verified_count += 1

    print(f"Recovery complete: {recovered_count} files recovered from Git history, {verified_count} total baseline files verified in {legacy_dir}.")

if __name__ == "__main__":
    main()
