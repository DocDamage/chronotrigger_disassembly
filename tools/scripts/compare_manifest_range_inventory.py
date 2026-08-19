#!/usr/bin/env python3
"""Prove source and range conservation across the complete baseline inventory."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.ctrepo.manifest_adapters import adapt_to_canonical, detect_schema_family
from tools.ctrepo.manifest_corrections import iter_manifest_corrections, load_manifest_corrections
from tools.ctrepo.manifest_discovery import discover_manifest_candidates


def _filename_pass(path: str) -> int | None:
    match = re.search(r"pass_?(\d+)", Path(path).name, flags=re.IGNORECASE)
    return int(match.group(1)) if match else None


def _read_baseline_blob(blob_id: str) -> Dict[str, Any]:
    raw = subprocess.check_output(["git", "cat-file", "-p", blob_id])
    return json.loads(raw.decode("utf-8-sig"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Strict full-baseline source and range conservation comparison")
    parser.add_argument("baseline_inventory", nargs="?", default="reports/remediation/corrective_baseline.json")
    parser.add_argument("canonical_manifests_dir", nargs="?", default="passes/manifests")
    parser.add_argument("--output-json", default="reports/remediation/range_conservation_report.json")
    parser.add_argument("--output-md", default="reports/remediation/range_conservation_report.md")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero on any unexplained source/range loss")
    args = parser.parse_args()

    baseline_path = Path(args.baseline_inventory)
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    baseline_sources = baseline.get("manifests", [])

    migration_path = Path(args.canonical_manifests_dir) / "manifest_migration_map.json"
    migration = json.loads(migration_path.read_text(encoding="utf-8"))
    migration_records = migration.get("migration_records", [])
    migration_index = {
        (record.get("original_source_path"), record.get("source_sha256")): record
        for record in migration_records
    }

    current_ranges: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    current_range_identities: set[Tuple[int, str, str]] = set()
    candidates = discover_manifest_candidates(args.canonical_manifests_dir)
    candidate_errors = [
        {"path": candidate.source_path, "error": candidate.error}
        for candidate in candidates if candidate.error
    ]
    for candidate in candidates:
        if candidate.manifest is None:
            continue
        for item in candidate.manifest.closed_ranges:
            current_range_identities.add((candidate.manifest.pass_number, item.range_str, item.label))
            current_ranges.setdefault((item.range_str, item.label), []).append({
                "pass_number": candidate.manifest.pass_number,
                "kind": item.kind,
                "verification_status": item.verification_status,
            })

    corrections = load_manifest_corrections()
    correction_index = {
        (
            correction["subject"]["pass_number"],
            correction["subject"]["range"],
            correction["subject"]["label"],
        ): correction
        for correction in iter_manifest_corrections(corrections)
    }

    missing_sources: List[Dict[str, Any]] = []
    missing_ranges: List[Dict[str, Any]] = []
    baseline_range_records: List[Dict[str, Any]] = []
    baseline_parse_errors: List[Dict[str, Any]] = []
    accounted_sources = 0

    for source in baseline_sources:
        source_key = (source["path"], source["sha256"])
        migration_record = migration_index.get(source_key)
        if migration_record is None:
            missing_sources.append(source)
            continue
        accounted_sources += 1

        data = _read_baseline_blob(source["blob_id"])
        try:
            manifest = adapt_to_canonical(
                data,
                source_path=source["path"],
                filename_pass=_filename_pass(source["path"]),
            )
        except ValueError as exc:
            # A range-less report may be archived/quarantined, but any source
            # claiming ranges must adapt successfully.
            family = detect_schema_family(data)
            if migration_record.get("range_count") == 0 and migration_record.get("canonical_pass") is None:
                baseline_parse_errors.append({
                    "source_path": source["path"],
                    "schema_family": family,
                    "disposition": migration_record.get("disposition"),
                    "non_range_artifact": True,
                    "diagnostic": str(exc),
                })
                continue
            baseline_parse_errors.append({
                "source_path": source["path"],
                "schema_family": family,
                "non_range_artifact": False,
                "error": str(exc),
            })
            continue

        for item in manifest.closed_ranges:
            key = (item.range_str, item.label)
            record = {
                "source_path": source["path"],
                "source_sha256": source["sha256"],
                "pass_number": manifest.pass_number,
                "range": item.range_str,
                "label": item.label,
            }
            matches = current_ranges.get(key, [])
            if matches:
                record["disposition"] = "represented"
                record["canonical_kinds"] = sorted({match["kind"] for match in matches})
            else:
                correction = correction_index.get((manifest.pass_number, item.range_str, item.label))
                updates = correction.get("updates", {}) if correction else {}
                corrected_identity = (
                    manifest.pass_number,
                    updates.get("range", item.range_str),
                    updates.get("label", item.label),
                )
                if correction and corrected_identity in current_range_identities:
                    record["disposition"] = "reviewed_correction"
                    record["correction_id"] = correction["correction_id"]
                    record["canonical_identity"] = {
                        "pass_number": corrected_identity[0],
                        "range": corrected_identity[1],
                        "label": corrected_identity[2],
                    }
                else:
                    record["disposition"] = "missing"
                    missing_ranges.append(record.copy())
            baseline_range_records.append(record)

    fatal_parse_errors = [entry for entry in baseline_parse_errors if not entry.get("non_range_artifact")]
    report = {
        "schema_version": 2,
        "baseline_commit": baseline.get("baseline_commit"),
        "total_baseline_sources": len(baseline_sources),
        "total_accounted_sources": accounted_sources,
        "missing_sources_count": len(missing_sources),
        "total_baseline_range_records": len(baseline_range_records),
        "total_canonical_range_records": sum(len(values) for values in current_ranges.values()),
        "missing_ranges_count": len(missing_ranges),
        "baseline_parse_errors_count": len(fatal_parse_errors),
        "non_range_artifacts_count": len(baseline_parse_errors) - len(fatal_parse_errors),
        "canonical_candidate_errors": candidate_errors,
        "missing_sources": missing_sources,
        "missing_ranges": missing_ranges,
        "baseline_parse_diagnostics": baseline_parse_errors,
        "range_records": baseline_range_records,
    }

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    output_md = Path(args.output_md)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(
        "\n".join([
            "# Manifest and Range Conservation Report",
            "",
            f"- Baseline sources: **{len(baseline_sources)}**",
            f"- Accounted source path/hash pairs: **{accounted_sources}**",
            f"- Baseline range records: **{len(baseline_range_records)}**",
            f"- Canonical range records: **{sum(len(values) for values in current_ranges.values())}**",
            f"- Missing sources: **{len(missing_sources)}**",
            f"- Missing ranges: **{len(missing_ranges)}**",
            f"- Range-bearing parse errors: **{len(fatal_parse_errors)}**",
            f"- Archived non-range artifacts: **{len(baseline_parse_errors) - len(fatal_parse_errors)}**",
            "",
            "Zero unexplained source or range loss." if not (missing_sources or missing_ranges or fatal_parse_errors or candidate_errors)
            else "Conservation failed; inspect the JSON report.",
        ]) + "\n",
        encoding="utf-8",
    )

    failed = bool(missing_sources or missing_ranges or fatal_parse_errors or candidate_errors)
    print(
        f"Conservation: {accounted_sources}/{len(baseline_sources)} sources, "
        f"{len(baseline_range_records)} baseline ranges, {len(missing_ranges)} missing"
    )
    return 1 if args.strict and failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
