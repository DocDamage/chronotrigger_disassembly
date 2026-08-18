#!/usr/bin/env python3
"""Audit trust fidelity and account for historical pass-number gaps factually."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.ctrepo.manifest_adapters import adapt_to_canonical
from tools.ctrepo.manifest_discovery import iter_canonical_manifests


BASELINE_PATH = Path("reports/remediation/corrective_baseline.json")
BASELINE_COMMIT = "c00ebe6f8e2d81f9c724c79215ac7643a5c1b353"


def _filename_pass(path: str) -> int | None:
    match = re.search(r"pass_?(\d+)", Path(path).name, flags=re.IGNORECASE)
    return int(match.group(1)) if match else None


def _baseline_manifest(entry: Dict[str, Any]):
    raw = subprocess.check_output(["git", "cat-file", "-p", entry["blob_id"]])
    data = json.loads(raw.decode("utf-8-sig"))
    return adapt_to_canonical(data, source_path=entry["path"], filename_pass=_filename_pass(entry["path"]))


def main() -> int:
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    canonical = list(iter_canonical_manifests())
    canonical_ranges: Dict[Tuple[int, str, str], List[Any]] = {}
    for manifest in canonical:
        for item in manifest.closed_ranges:
            canonical_ranges.setdefault((manifest.pass_number, item.range_str, item.label), []).append(item)

    trust_records: List[Dict[str, Any]] = []
    unexplained_promotions: List[Dict[str, Any]] = []
    baseline_passes = set()
    non_range_sources: List[str] = []
    for entry in baseline.get("manifests", []):
        try:
            manifest = _baseline_manifest(entry)
        except ValueError:
            non_range_sources.append(entry["path"])
            continue
        baseline_passes.add(manifest.pass_number)
        for source_item in manifest.closed_ranges:
            matches = canonical_ranges.get((manifest.pass_number, source_item.range_str, source_item.label), [])
            for canonical_item in matches[:1]:
                record = {
                    "source_path": entry["path"],
                    "pass_number": manifest.pass_number,
                    "range": source_item.range_str,
                    "label": source_item.label,
                    "source_verification_status": source_item.verification_status,
                    "canonical_verification_status": canonical_item.verification_status,
                    "source_confidence": source_item.confidence,
                    "canonical_confidence": canonical_item.confidence,
                }
                promoted = (
                    source_item.verification_status != canonical_item.verification_status
                    or source_item.confidence != canonical_item.confidence
                )
                record["trust_changed"] = promoted
                trust_records.append(record)
                if promoted:
                    unexplained_promotions.append(record)

    trust_report = {
        "schema_version": 2,
        "baseline_commit": baseline.get("baseline_commit"),
        "total_source_range_records_audited": len(trust_records),
        "unexplained_promotions_count": len(unexplained_promotions),
        "non_range_sources": non_range_sources,
        "unexplained_promotions": unexplained_promotions,
        "records": trust_records,
    }
    trust_path = Path("reports/remediation/trust_delta_report.json")
    trust_path.write_text(json.dumps(trust_report, indent=2) + "\n", encoding="utf-8")

    canonical_passes = {manifest.pass_number for manifest in canonical}
    gap_numbers = sorted(set(range(min(canonical_passes), max(canonical_passes) + 1)) - canonical_passes)
    gaps: Dict[str, Dict[str, Any]] = {}
    ordered_passes = sorted(canonical_passes)
    for gap in gap_numbers:
        lower = max(number for number in ordered_passes if number < gap)
        upper = min(number for number in ordered_passes if number > gap)
        status = "baseline_absent" if gap not in baseline_passes else "investigation_needed"
        gaps[str(gap)] = {
            "pass_number": gap,
            "status": status,
            "reason_code": "no_baseline_manifest" if status == "baseline_absent" else "baseline_identity_mismatch",
            "rationale": (
                f"No source manifest with pass identity {gap} exists in the immutable "
                f"{BASELINE_COMMIT[:8]} baseline inventory; adjacent canonical passes are {lower} and {upper}."
            ),
            "evidence": [
                "reports/remediation/corrective_baseline.json",
                f"passes/manifests/pass{lower:04d}.json",
                f"passes/manifests/pass{upper:04d}.json",
            ],
            "evidence_commit": BASELINE_COMMIT,
            "generated_by": "reconcile_trust_and_gaps.py",
            "revalidation_required": False,
        }

    gap_record = {
        "$schema": "schemas/intentional_pass_gaps.schema.json",
        "schema_version": 3,
        "description": "Factual accounting of pass identities absent from the immutable baseline; no human intent is inferred.",
        "total_gaps_count": len(gaps),
        "intentional_gaps": gaps,
    }
    gap_path = Path("tools/config/intentional_pass_gaps.json")
    gap_path.write_text(json.dumps(gap_record, indent=2) + "\n", encoding="utf-8")

    print(
        f"Trust audit: {len(trust_records)} ranges, {len(unexplained_promotions)} changes; "
        f"gap accounting: {len(gaps)} baseline-absence records"
    )
    return 1 if unexplained_promotions or any(item["status"] == "investigation_needed" for item in gaps.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
