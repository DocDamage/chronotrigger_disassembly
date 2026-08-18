#!/usr/bin/env python3
"""Inventory tracked binary archives before current-tree removal."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT = ROOT / "reports" / "remediation" / "binary_archive_disposition.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    tracked = subprocess.check_output(["git", "ls-files", "*.zip"], cwd=ROOT, text=True).splitlines()
    records = []
    for relative in sorted(tracked):
        path = ROOT / relative
        if not path.exists():
            continue
        records.append({
            "path": relative.replace("\\", "/"),
            "size_bytes": path.stat().st_size,
            "sha256": sha256(path),
            "disposition": "remove_from_current_tree_recoverable_from_git_history",
            "recovery_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "external_publication_authorized": False,
        })
    payload = {
        "schema_version": 1,
        "tracked_archive_count_before_cleanup": len(records),
        "total_size_bytes": sum(record["size_bytes"] for record in records),
        "records": records,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Inventoried {len(records)} tracked ZIP archives ({payload['total_size_bytes']} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
