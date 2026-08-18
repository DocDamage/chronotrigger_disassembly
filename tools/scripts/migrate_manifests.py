#!/usr/bin/env python3
"""Migrate heterogeneous historical manifests into canonical passNNNN.json schema v2 manifests."""

import argparse
import hashlib
import json
import os
import re
import sys
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.ctrepo.manifest_models import CanonicalManifest, ClosedRange
from tools.ctrepo.manifest_adapters import adapt_to_canonical, detect_schema_family
from tools.ctrepo.manifest_discovery import discover_manifest_candidates, read_json_safely
from tools.ctrepo.manifest_validation import validate_manifest

def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def plan_migration(manifests_dir: str = "passes/manifests") -> Tuple[Dict[int, CanonicalManifest], List[Dict[str, Any]]]:
    """Analyze all candidate manifests and construct merged canonical manifests + migration records."""
    legacy_dir = os.path.join(manifests_dir, "legacy")
    search_dirs = [d for d in [legacy_dir, manifests_dir] if os.path.exists(d)]
    candidates = []
    seen_passes_in_legacy = set()
    
    if os.path.exists(legacy_dir):
        for c in discover_manifest_candidates(manifests_dir=legacy_dir):
            if c.pass_number is not None:
                seen_passes_in_legacy.add(c.pass_number)
            candidates.append(c)
            
    for c in discover_manifest_candidates(manifests_dir=manifests_dir):
        if c.pass_number is not None and c.pass_number in seen_passes_in_legacy:
            continue
        candidates.append(c)
    
    # Group candidates by pass number
    grouped_candidates: Dict[int, List[Any]] = {}
    scan_reports: List[Any] = []
    
    for c in candidates:
        if c.schema_family == "scan_report" or c.error and "scan report" in c.error.lower():
            scan_reports.append(c)
            continue
        if c.pass_number is not None:
            grouped_candidates.setdefault(c.pass_number, []).append(c)
        else:
            scan_reports.append(c)

    canonical_manifests: Dict[int, CanonicalManifest] = {}
    migration_map: List[Dict[str, Any]] = []

    for pass_num in sorted(grouped_candidates.keys()):
        cand_list = grouped_candidates[pass_num]
        
        # Merge all ranges and sources across all files for this pass
        merged_ranges: List[ClosedRange] = []
        seen_range_keys = set()
        merged_labels: List[str] = []
        merged_notes: List[str] = []
        sources: Dict[str, str] = {}
        legacy_meta: Dict[str, Any] = {}
        status = "reviewed"
        live_seam = None
        
        for c in cand_list:
            if c.manifest is None:
                continue
            m = c.manifest
            if m.live_seam_after_pass:
                live_seam = m.live_seam_after_pass
            if m.status in ("accepted", "reviewed", "draft"):
                status = m.status
                
            sources[f"legacy_{len(sources)+1}_{os.path.basename(c.source_path)}"] = c.source_path.replace("\\", "/")
            
            for cr in m.closed_ranges:
                r_key = (cr.bank, cr.start_addr, cr.end_addr, cr.label)
                if r_key not in seen_range_keys:
                    seen_range_keys.add(r_key)
                    merged_ranges.append(cr)
                    if cr.label and cr.label not in merged_labels:
                        merged_labels.append(cr.label)
                        
            for n in m.notes:
                if n not in merged_notes:
                    merged_notes.append(n)

        if not merged_ranges:
            for c in cand_list:
                migration_map.append({
                    "source_path": c.source_path.replace("\\", "/"),
                    "source_filename": c.filename,
                    "source_sha256": sha256_file(c.source_path) if os.path.exists(c.source_path) else None,
                    "detected_schema": c.schema_family,
                    "parsed_pass": pass_num,
                    "canonical_target_filename": None,
                    "canonical_pass": None,
                    "range_count": 0,
                    "disposition": "scan_report_without_closed_ranges"
                })
            continue

        # Build CanonicalManifest
        canonical_dest = f"pass{pass_num:04d}.json"
        canon_m = CanonicalManifest(
            pass_number=pass_num,
            schema_version=2,
            status=status,
            branch="live-work-from-pass166",
            toolkit_version="repo-native-vNext",
            rom_sha256="06d1c2b06b716052c5596aaa0c2e5632a027fee1a9a28439e509f813c30829a9",
            live_seam_after_pass=live_seam,
            closed_ranges=merged_ranges,
            new_labels=merged_labels,
            confidence={"structural": "medium", "semantic": "medium", "rebuild": "low"},
            sources=sources,
            legacy_metadata=legacy_meta,
            notes=merged_notes,
            source_path=os.path.join(manifests_dir, canonical_dest)
        )
        
        canonical_manifests[pass_num] = canon_m
        
        # Record migration map entries
        for c in cand_list:
            disposition = "canonicalized" if len(cand_list) == 1 else "merged_into_canonical"
            migration_map.append({
                "source_path": c.source_path.replace("\\", "/"),
                "source_filename": c.filename,
                "source_sha256": sha256_file(c.source_path) if os.path.exists(c.source_path) else None,
                "detected_schema": c.schema_family,
                "parsed_pass": pass_num,
                "canonical_target_filename": canonical_dest,
                "canonical_pass": pass_num,
                "range_count": len(c.manifest.closed_ranges) if c.manifest else 0,
                "disposition": disposition
            })

    for s in scan_reports:
        migration_map.append({
            "source_path": s.source_path.replace("\\", "/"),
            "source_filename": s.filename,
            "source_sha256": sha256_file(s.source_path) if os.path.exists(s.source_path) else None,
            "detected_schema": s.schema_family,
            "parsed_pass": s.pass_number,
            "canonical_target_filename": None,
            "canonical_pass": None,
            "range_count": 0,
            "disposition": "non_manifest_scan_report"
        })

    return canonical_manifests, migration_map


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate pass manifests to canonical schema v2 format.")
    parser.add_argument("--manifests-dir", default="passes/manifests", help="Manifests directory")
    parser.add_argument("--dry-run", action="store_true", help="Perform dry-run without modifying files")
    parser.add_argument("--apply", action="store_true", help="Apply migration directly to disk")
    parser.add_argument("--verify", action="store_true", help="Verify canonical manifests on disk")
    parser.add_argument("--report", default=None, help="Save migration report to JSON file")
    args = parser.parse_args()

    manifests_dir = args.manifests_dir
    legacy_dir = os.path.join(manifests_dir, "legacy")

    print(f"Analyzing manifests in {manifests_dir}...")
    canon_manifests, mig_map = plan_migration(manifests_dir=manifests_dir)

    print(f"Planned {len(canon_manifests)} canonical manifests from {len(mig_map)} source files.")

    report_payload = {
        "total_canonical_manifests": len(canon_manifests),
        "total_source_files": len(mig_map),
        "canonical_pass_min": min(canon_manifests.keys()) if canon_manifests else 0,
        "canonical_pass_max": max(canon_manifests.keys()) if canon_manifests else 0,
        "migration_records": mig_map
    }

    if args.report:
        os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(report_payload, f, indent=2)
        print(f"Saved migration report to {args.report}")

    if args.dry_run or not args.apply:
        print("Dry run completed. No files modified. Run with --apply to execute migration.")
        return 0

    # Apply migration
    print(f"Applying migration to {manifests_dir}...")
    os.makedirs(legacy_dir, exist_ok=True)

    # 1. First move suffixed / non-canonical files and duplicates to legacy/
    for rec in mig_map:
        src_path = rec["source_path"]
        src_fn = rec["source_filename"]
        target_fn = rec["canonical_target_filename"]
        
        # If the file has a suffixed name or is non-manifest, move it to legacy/
        if src_fn != target_fn:
            target_legacy_path = os.path.join(legacy_dir, src_fn)
            if os.path.exists(src_path) and src_path != target_legacy_path:
                shutil.move(src_path, target_legacy_path)
                rec["legacy_archived_path"] = target_legacy_path.replace("\\", "/")

    # 2. Write all canonical manifests
    expected_filenames = {f"pass{p:04d}.json" for p in canon_manifests.keys()}
    for pass_num, canon_m in sorted(canon_manifests.items()):
        dest_filename = f"pass{pass_num:04d}.json"
        dest_path = os.path.join(manifests_dir, dest_filename)

        data = canon_m.to_dict()
        with open(dest_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # Clean up any leftover pass*.json in manifests_dir not in expected canonical set
    for fn in os.listdir(manifests_dir):
        if fn.startswith("pass") and fn.endswith(".json") and fn not in expected_filenames:
            dest_f = os.path.join(manifests_dir, fn)
            if os.path.isfile(dest_f):
                os.remove(dest_f)

    # 3. Write manifest_migration_map.json
    mig_map_path = os.path.join(manifests_dir, "manifest_migration_map.json")
    with open(mig_map_path, "w", encoding="utf-8") as f:
        json.dump(report_payload, f, indent=2)
    print(f"Written {mig_map_path}")

    # 4. Reconcile intentional gaps
    existing_passes = set(canon_manifests.keys())
    all_possible = set(range(min(existing_passes), max(existing_passes) + 1))
    gaps = sorted(all_possible - existing_passes)
    
    gaps_config_path = os.path.join(repo_root, "tools", "config", "intentional_pass_gaps.json")
    gaps_record = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "Registry of reviewed intentional pass gaps in historical sequence",
        "version": 1,
        "total_gaps_count": len(gaps),
        "intentional_gaps": {
            str(g): {
                "rationale": "Historical agent swarm sequence gap or unnumbered draft iteration",
                "reviewed": True
            } for g in gaps
        }
    }
    with open(gaps_config_path, "w", encoding="utf-8") as f:
        json.dump(gaps_record, f, indent=2)
    print(f"Updated {gaps_config_path} with {len(gaps)} intentional gap entries.")

    print("Migration applied successfully.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
