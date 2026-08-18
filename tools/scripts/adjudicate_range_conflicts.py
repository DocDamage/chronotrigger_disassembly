#!/usr/bin/env python3
"""Build durable deterministic ownership decisions without fabricating waivers."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.ctrepo.manifest_models import CanonicalManifest, ClosedRange
from tools.ctrepo.range_adjudication import apply_adjudications, iter_manifest_ranges
from tools.ctrepo.range_model import RangeConflict, detect_range_conflicts
from tools.scripts.migrate_manifests import plan_migration


CONFIDENCE_RANK = {
    "low": 0, "score-4": 1, "medium": 2, "score-5": 2,
    "medium-high": 3, "score-6": 3, "high": 4, "reviewed": 5,
}
STATUS_RANK = {"pending": 0, "draft": 0, "reviewed": 2, "accepted": 3}
KIND_RANK = {
    "tail_fragment": 0, "text_marker": 1, "data": 2,
    "code_helper": 3, "wrapper": 3, "veneer": 3, "code_owner": 4,
}


def _identity(pass_number: int, item: ClosedRange) -> Dict[str, Any]:
    return {"pass_number": pass_number, "range": item.range_str, "label": item.label}


def _decision_id(action: str, subject: Dict[str, Any], other: Dict[str, Any]) -> str:
    raw = json.dumps([action, subject, other], sort_keys=True).encode("utf-8")
    return "adj_" + hashlib.sha256(raw).hexdigest()[:20]


def _conflict_id(conflict: RangeConflict) -> str:
    identities = sorted(
        [_identity(conflict.left_pass, conflict.left_range), _identity(conflict.right_pass, conflict.right_range)],
        key=lambda item: (item["pass_number"], item["range"], item["label"]),
    )
    raw = json.dumps(
        [conflict.relationship, conflict.overlap_range_str, identities],
        sort_keys=True,
    ).encode("utf-8")
    return "conf_" + hashlib.sha256(raw).hexdigest()[:20]


def _rank(pass_number: int, item: ClosedRange) -> Tuple[int, int, int, int, int]:
    """Rank ownership evidence; earlier pass is only the final tie-break."""
    return (
        STATUS_RANK.get(item.verification_status or "pending", 0),
        CONFIDENCE_RANK.get(item.confidence, 0),
        1 if item.evidence else 0,
        KIND_RANK.get(item.kind, 0),
        -pass_number,
    )


def _locate(conflict: RangeConflict) -> Tuple[Tuple[int, ClosedRange], Tuple[int, ClosedRange]]:
    return (conflict.left_pass, conflict.left_range), (conflict.right_pass, conflict.right_range)


def _manifest_evidence(manifests: Dict[int, CanonicalManifest], passes: List[int]) -> List[str]:
    evidence: List[str] = []
    for pass_number in passes:
        canonical = f"passes/manifests/pass{pass_number:04d}.json"
        if canonical not in evidence:
            evidence.append(canonical)
        for source in sorted(manifests[pass_number].sources.values()):
            if source not in evidence:
                evidence.append(source)
    return evidence


def _supersede(conflict: RangeConflict, manifests: Dict[int, CanonicalManifest]) -> Dict[str, Any]:
    left, right = _locate(conflict)
    winner, loser = (left, right) if _rank(*left) >= _rank(*right) else (right, left)
    winner_pass, winner_range = winner
    loser_pass, loser_range = loser
    winner_rank = list(_rank(*winner))
    loser_rank = list(_rank(*loser))
    subject = _identity(loser_pass, loser_range)
    winner_data = _identity(winner_pass, winner_range)
    return {
        "decision_id": _decision_id("supersede", subject, winner_data),
        "action": "supersede",
        "relationship": conflict.relationship,
        "subject": subject,
        "winner": winner_data,
        "reason_code": "deterministic_ownership_precedence",
        "rationale": (
            "The overlapping bytes cannot have two active owners. The winner has the higher "
            "verification, confidence, evidence, and kind rank; pass number is only the "
            "final tie-break. The original weaker claim remains as superseded provenance, "
            "and any non-overlapping bytes are emitted as active residual fragments."
        ),
        "coverage_treatment": "winner_owns_overlap_subject_retains_non_overlapping_residuals",
        "rank": {"winner": winner_rank, "subject": loser_rank},
        "evidence": _manifest_evidence(manifests, [winner_pass, loser_pass]),
    }


def build_adjudications(
    manifests: Dict[int, CanonicalManifest],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    decisions: List[Dict[str, Any]] = []
    initial_conflicts = detect_range_conflicts(list(iter_manifest_ranges(manifests)))
    initial_candidates = [
        {
            "conflict_id": _conflict_id(c),
            "relationship": c.relationship,
            "overlap_range": c.overlap_range_str,
            "left": {
                **_identity(c.left_pass, c.left_range),
                "kind": c.left_range.kind,
                "confidence": c.left_range.confidence,
                "verification_status": c.left_range.verification_status,
            },
            "right": {
                **_identity(c.right_pass, c.right_range),
                "kind": c.right_range.kind,
                "confidence": c.right_range.confidence,
                "verification_status": c.right_range.verification_status,
            },
            "evidence": _manifest_evidence(manifests, [c.left_pass, c.right_pass]),
        }
        for c in initial_conflicts
    ]
    for conflict in sorted(
        initial_conflicts,
        key=lambda c: (c.bank, c.overlap_start, c.overlap_end, c.left_pass, c.right_pass, c.relationship),
    ):
        decisions.append(_supersede(conflict, manifests))
    return decisions, initial_candidates


def main() -> int:
    parser = argparse.ArgumentParser(description="Build durable deterministic range adjudications")
    parser.add_argument("--output", default="tools/config/range_adjudications.json")
    parser.add_argument("--candidates", default="reports/remediation/range_conflict_candidates.json")
    args = parser.parse_args()

    manifests, _ = plan_migration(apply_ownership_adjudications=False)
    decisions, candidates = build_adjudications(manifests)
    validation_manifests, _ = plan_migration(apply_ownership_adjudications=False)
    apply_adjudications(validation_manifests, {"decisions": decisions}, strict=True)
    remaining = detect_range_conflicts(list(iter_manifest_ranges(validation_manifests)))
    if remaining:
        print(f"Adjudication failed: {len(remaining)} conflicts remain")
        return 1

    source_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    ledger = {
        "$schema": "tools/config/schemas/range_adjudications.schema.json",
        "schema_version": 1,
        "policy_version": "deterministic-interval-ownership-v2",
        "source_commit": source_commit,
        "description": "Durable ownership decisions applied by canonical manifest migration",
        "decision_count": len(decisions),
        "decisions": decisions,
    }
    candidate_report = {
        "schema_version": 2,
        "source_commit": source_commit,
        "generated_status": "candidate_input_only",
        "total_conflicts": len(candidates),
        "candidates": candidates,
        "resolution_summary": {
            "decisions": len(decisions),
            "remaining_active_conflicts": 0,
            "by_relationship": {
                relationship: sum(1 for candidate in candidates if candidate["relationship"] == relationship)
                for relationship in sorted({candidate["relationship"] for candidate in candidates})
            },
        },
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    candidate_path = Path(args.candidates)
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text(json.dumps(candidate_report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(decisions)} durable decisions from {len(candidates)} raw conflicts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
