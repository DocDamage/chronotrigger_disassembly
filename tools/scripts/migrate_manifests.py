#!/usr/bin/env python3
"""Migrate heterogeneous historical manifests into canonical passNNNN.json schema v2 manifests."""

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import time

from pathlib import Path
from typing import Dict, Any, List, Tuple

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.ctrepo.manifest_models import CanonicalManifest, ClosedRange
from tools.ctrepo.manifest_discovery import discover_manifest_candidates
from tools.ctrepo.manifest_validation import validate_manifest
from tools.ctrepo.range_adjudication import apply_adjudications, load_adjudications


def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def replace_with_retry(source: str, destination: str, attempts: int = 12) -> None:
    """Atomically replace a file, tolerating short-lived Windows reader locks."""
    for attempt in range(attempts):
        try:
            os.replace(source, destination)
            return
        except PermissionError:
            if attempt == attempts - 1:
                raise
            time.sleep(0.05 * (attempt + 1))

def _baseline_original_paths() -> Dict[str, str]:
    """Return baseline SHA-256 -> original repository path when available."""
    baseline_path = repo_root / "reports" / "remediation" / "corrective_baseline.json"
    if not baseline_path.exists():
        return {}
    data = json.loads(baseline_path.read_text(encoding="utf-8"))
    return {entry["sha256"]: entry["path"] for entry in data.get("manifests", [])}


def plan_migration(
    manifests_dir: str = "passes/manifests",
    adjudications_path: str = "tools/config/range_adjudications.json",
    apply_ownership_adjudications: bool = True,
    project_state_path: str = "tools/config/project_state.json",
) -> Tuple[Dict[int, CanonicalManifest], List[Dict[str, Any]]]:
    """Analyze all candidate source manifests and construct merged canonical manifests + migration ledger."""
    legacy_dir = os.path.join(manifests_dir, "legacy")
    
    # 1. Collect all candidates from legacy directory (or manifests_dir if legacy does not exist)
    all_candidates = []
    seen_source_keys = set()
    original_paths = _baseline_original_paths()

    source_dir = legacy_dir if os.path.exists(legacy_dir) and len(os.listdir(legacy_dir)) > 0 else manifests_dir

    for c in discover_manifest_candidates(manifests_dir=source_dir):
        if c.source_path and os.path.exists(c.source_path):
            file_hash = sha256_file(c.source_path)
            source_key = (os.path.normcase(os.path.abspath(c.source_path)), file_hash)
            if source_key not in seen_source_keys:
                seen_source_keys.add(source_key)
                all_candidates.append(c)

    # 2. Group candidates by pass number
    grouped_candidates: Dict[int, List[Any]] = {}
    scan_reports: List[Any] = []

    for c in all_candidates:
        if c.schema_family == "scan_report" or (c.error and "scan report" in c.error.lower()):
            scan_reports.append(c)
            continue
        if c.pass_number is not None:
            grouped_candidates.setdefault(c.pass_number, []).append(c)
        else:
            scan_reports.append(c)

    canonical_manifests: Dict[int, CanonicalManifest] = {}
    migration_records: List[Dict[str, Any]] = []

    for pass_num in sorted(grouped_candidates.keys()):
        cand_list = grouped_candidates[pass_num]
        
        merged_ranges: List[ClosedRange] = []
        seen_range_keys = set()
        merged_labels: List[str] = []
        merged_notes: List[str] = []
        sources: Dict[str, str] = {}
        legacy_meta: Dict[str, Any] = {}
        status = "accepted"
        live_seam = None
        
        for c in cand_list:
            if c.manifest is None:
                continue
            m = c.manifest
            if m.live_seam_after_pass:
                live_seam = m.live_seam_after_pass
            trust_rank = {"draft": 0, "reviewed": 1, "accepted": 2}
            if m.status in trust_rank and trust_rank[m.status] < trust_rank.get(status, 0):
                status = m.status
                
            fn_clean = os.path.basename(c.source_path)
            sources[f"source_{len(sources)+1}_{fn_clean}"] = c.source_path.replace("\\", "/")
            
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

        canonical_dest = f"pass{pass_num:04d}.json"
        
        # Build CanonicalManifest if ranges exist
        if merged_ranges:
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
                source_path=os.path.join(manifests_dir, canonical_dest).replace("\\", "/")
            )
            canonical_manifests[pass_num] = canon_m

        for c in cand_list:
            src_sha = sha256_file(c.source_path) if os.path.exists(c.source_path) else None
            disposition = "canonicalized" if len(cand_list) == 1 else "merged"
            if not merged_ranges:
                disposition = "scan_report_without_closed_ranges"

            migration_records.append({
                "original_source_path": original_paths.get(src_sha, c.source_path.replace("\\", "/")),
                "source_path": c.source_path.replace("\\", "/"),
                "source_filename": c.filename,
                "source_sha256": src_sha,
                "detected_schema": c.schema_family,
                "parsed_pass": pass_num,
                "canonical_target_filename": canonical_dest if merged_ranges else None,
                "canonical_pass": pass_num if merged_ranges else None,
                "range_count": len(c.manifest.closed_ranges) if c.manifest else 0,
                "disposition": disposition,
                "legacy_archived_path": c.source_path.replace("\\", "/")
            })

    for s in scan_reports:
        src_sha = sha256_file(s.source_path) if os.path.exists(s.source_path) else None
        migration_records.append({
            "original_source_path": original_paths.get(src_sha, s.source_path.replace("\\", "/")),
            "source_path": s.source_path.replace("\\", "/"),
            "source_filename": s.filename,
            "source_sha256": src_sha,
            "detected_schema": s.schema_family or "scan_report",
            "parsed_pass": s.pass_number,
            "canonical_target_filename": None,
            "canonical_pass": None,
            "range_count": 0,
            "disposition": "scan_report_without_closed_ranges",
            "legacy_archived_path": s.source_path.replace("\\", "/")
        })

    # Sort migration records deterministically by parsed_pass, source_path
    migration_records.sort(key=lambda x: (x["parsed_pass"] if x["parsed_pass"] is not None else 99999, x["source_path"]))

    if apply_ownership_adjudications:
        adjudications = load_adjudications(adjudications_path)
        apply_adjudications(canonical_manifests, adjudications, strict=True)
        state_path = Path(project_state_path)
        if state_path.exists():
            project_state = json.loads(state_path.read_text(encoding="utf-8"))
            latest_pass = int(project_state["latest_manifest_pass"])
            if latest_pass not in canonical_manifests:
                raise ValueError(f"Project state references missing pass {latest_pass}")
            canonical_manifests[latest_pass].live_seam_after_pass = project_state["live_seam"]

    return canonical_manifests, migration_records


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate historical pass manifests to canonical schema v2.")
    parser.add_argument("--manifests-dir", default="passes/manifests", help="Path to manifests directory")
    parser.add_argument("--staging-dir", default=None, help="Optional staging directory to output manifests to")
    parser.add_argument("--dry-run", action="store_true", help="Perform planning and analysis without modifying files")
    parser.add_argument("--apply", action="store_true", help="Execute the migration and write canonical files")
    parser.add_argument("--allow-corrective-apply", action="store_true", help="Override Phase 0 safety guard for Phase 3 apply")
    parser.add_argument("--adjudications", default="tools/config/range_adjudications.json", help="Durable ownership adjudication ledger")
    parser.add_argument("--skip-adjudications", action="store_true", help="Generate source-normalized manifests before ownership adjudication")
    parser.add_argument("--report", default="reports/remediation/manifest_migration_plan.json", help="Path to write migration JSON report")
    args = parser.parse_args()

    manifests_dir = args.manifests_dir
    print(f"Analyzing manifests in {manifests_dir}...")
    canon_manifests, mig_map = plan_migration(
        manifests_dir,
        adjudications_path=args.adjudications,
        apply_ownership_adjudications=not args.skip_adjudications,
    )

    report_payload = {
        "total_canonical_manifests": len(canon_manifests),
        "total_source_files": len(mig_map),
        "canonical_pass_min": min(canon_manifests.keys()) if canon_manifests else None,
        "canonical_pass_max": max(canon_manifests.keys()) if canon_manifests else None,
        "migration_records": mig_map
    }

    print(f"Planned {len(canon_manifests)} canonical manifests from {len(mig_map)} source files.")

    if args.report:
        os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(report_payload, f, indent=2)
        print(f"Saved migration report to {args.report}")

    if args.dry_run or not args.apply:
        print("Dry run completed. No files modified. Run with --apply to execute migration.")
        return 0

    # Phase 0 Freeze Guard: Prevent destructive apply until Phase 2 idempotency fix is explicitly enabled
    if not args.allow_corrective_apply:
        print("PHASE 0 SAFETY GUARD: 'migrate_manifests.py --apply' is currently FROZEN.")
        print("Use --dry-run or provide --allow-corrective-apply when executing Phase 3.")
        return 1

    target_out_dir = os.path.abspath(args.staging_dir or manifests_dir)
    print(f"Applying migration to {target_out_dir}...")

    # Always build and validate a complete temporary tree before replacing any
    # destination.  Production replacement keeps backups until every atomic
    # os.replace succeeds, then removes them.
    target_parent = os.path.dirname(target_out_dir)
    os.makedirs(target_parent, exist_ok=True)
    temp_dir = tempfile.mkdtemp(prefix="manifest-migration-", dir=target_parent)
    backup_dir = None
    try:
        for pass_num, canon_m in sorted(canon_manifests.items()):
            valid, errors = validate_manifest(canon_m, strict=True)
            if not valid:
                raise ValueError(f"Staged pass {pass_num} failed validation: {errors}")
            dest_filename = f"pass{pass_num:04d}.json"
            with open(os.path.join(temp_dir, dest_filename), "w", encoding="utf-8") as f:
                json.dump(canon_m.to_dict(), f, indent=2)

        with open(os.path.join(temp_dir, "manifest_migration_map.json"), "w", encoding="utf-8") as f:
            json.dump(report_payload, f, indent=2)

        expected = {f"pass{p:04d}.json" for p in canon_manifests}
        staged = {p.name for p in Path(temp_dir).glob("pass*.json")}
        if staged != expected:
            raise ValueError(f"Staged manifest set mismatch: expected {len(expected)}, found {len(staged)}")

        os.makedirs(target_out_dir, exist_ok=True)
        backup_dir = tempfile.mkdtemp(prefix="manifest-backup-", dir=target_parent)
        replaced: List[str] = []
        try:
            for filename in sorted(expected | {"manifest_migration_map.json"}):
                destination = os.path.join(target_out_dir, filename)
                if os.path.exists(destination):
                    shutil.copy2(destination, os.path.join(backup_dir, filename))
                replace_with_retry(os.path.join(temp_dir, filename), destination)
                replaced.append(filename)
        except Exception:
            for filename in replaced:
                backup = os.path.join(backup_dir, filename)
                destination = os.path.join(target_out_dir, filename)
                if os.path.exists(backup):
                    replace_with_retry(backup, destination)
                elif os.path.exists(destination):
                    os.remove(destination)
            raise

        print(f"Written {len(expected)} canonical manifests and manifest_migration_map.json")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
        if backup_dir:
            shutil.rmtree(backup_dir, ignore_errors=True)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
