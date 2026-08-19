#!/usr/bin/env python3
"""Measure whether canonical mapping evidence is ready for source reconstruction."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.ctrepo.manifest_discovery import discover_manifest_candidates


ACTIVE_KINDS = {"code_owner", "code_helper", "wrapper", "veneer", "data", "text_marker", "tail_fragment"}
EXECUTABLE_KINDS = {"code_owner", "code_helper", "wrapper", "veneer", "tail_fragment"}
FINAL_VERIFICATION = {"reviewed", "accepted"}


def audit(manifests_dir: str | Path, candidate_ledger: str | Path) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    discovery_errors: list[dict[str, str]] = []
    for candidate in discover_manifest_candidates(manifests_dir):
        if candidate.error or candidate.manifest is None:
            discovery_errors.append({"path": candidate.source_path, "error": candidate.error or "missing manifest"})
            continue
        manifest = candidate.manifest
        for item in manifest.closed_ranges:
            if item.kind not in ACTIVE_KINDS:
                continue
            records.append({
                "pass_number": manifest.pass_number,
                "range": item.range_str,
                "bank": item.bank,
                "kind": item.kind,
                "label": item.label,
                "verification_status": item.verification_status or "pending",
                "has_structured_evidence": bool(item.evidence),
                "has_source_provenance": bool(manifest.sources),
            })

    ledger = json.loads(Path(candidate_ledger).read_text(encoding="utf-8"))
    dispositions = Counter(item["disposition"] for item in ledger.get("candidates", []))
    deferred = [item for item in ledger.get("candidates", []) if item["disposition"] == "deferred"]
    unresolved = [record for record in records if record["verification_status"] not in FINAL_VERIFICATION]
    missing_evidence = [record for record in records if not record["has_structured_evidence"]]
    missing_provenance = [record for record in records if not record["has_source_provenance"]]

    by_bank: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        bucket = by_bank[record["bank"]]
        bucket["active"] += 1
        if record["kind"] in EXECUTABLE_KINDS:
            bucket["executable"] += 1
        if record["verification_status"] not in FINAL_VERIFICATION:
            bucket["unresolved_verification"] += 1
        if not record["has_structured_evidence"]:
            bucket["missing_evidence"] += 1

    blockers = {
        "discovery_errors": len(discovery_errors),
        "unresolved_active_ranges": len(unresolved),
        "active_ranges_missing_evidence": len(missing_evidence),
        "active_ranges_missing_source_provenance": len(missing_provenance),
        "deferred_candidates": len(deferred),
    }
    ready = not any(blockers.values())
    return {
        "schema_version": 1,
        "ready_for_disassembly": ready,
        "active_range_count": len(records),
        "executable_range_count": sum(record["kind"] in EXECUTABLE_KINDS for record in records),
        "reviewed_or_accepted_range_count": len(records) - len(unresolved),
        "candidate_disposition_counts": dict(sorted(dispositions.items())),
        "blockers": blockers,
        "banks": {bank: dict(counts) for bank, counts in sorted(by_bank.items())},
        "deferred_candidates": deferred,
        "unresolved_active_ranges": unresolved,
        "missing_evidence_ranges": missing_evidence,
        "missing_provenance_ranges": missing_provenance,
        "discovery_errors": discovery_errors,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Pre-disassembly readiness audit",
        "",
        f"- Ready for disassembly: **{'YES' if report['ready_for_disassembly'] else 'NO'}**",
        f"- Active canonical ranges: **{report['active_range_count']}**",
        f"- Executable canonical ranges: **{report['executable_range_count']}**",
        f"- Reviewed or accepted ranges: **{report['reviewed_or_accepted_range_count']}**",
        "",
        "## Blocking counts",
        "",
    ]
    for name, count in report["blockers"].items():
        lines.append(f"- {name.replace('_', ' ').title()}: **{count}**")
    lines.extend(["", "## Bank summary", "", "| Bank | Active | Executable | Unresolved verification | Missing evidence |", "|---|---:|---:|---:|---:|"])
    for bank, counts in report["banks"].items():
        lines.append(
            f"| {bank} | {counts.get('active', 0)} | {counts.get('executable', 0)} | "
            f"{counts.get('unresolved_verification', 0)} | {counts.get('missing_evidence', 0)} |"
        )
    lines.extend(["", "Deferred candidates remain explicit blockers until accepted, rejected, or otherwise resolved.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit evidence required before actual disassembly begins.")
    parser.add_argument("--manifests-dir", default="passes/manifests")
    parser.add_argument("--candidate-ledger", default="tools/config/candidate_dispositions.json")
    parser.add_argument("--output-json", default="reports/pre_disassembly_readiness.json")
    parser.add_argument("--output-md", default="reports/pre_disassembly_readiness.md")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero while readiness blockers remain")
    args = parser.parse_args()

    report = audit(args.manifests_dir, args.candidate_ledger)
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")
    print(
        f"Pre-disassembly readiness: {'READY' if report['ready_for_disassembly'] else 'BLOCKED'} "
        f"({report['reviewed_or_accepted_range_count']}/{report['active_range_count']} active ranges reviewed)"
    )
    return 1 if args.strict and not report["ready_for_disassembly"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
