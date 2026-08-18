"""Apply explicit range-ownership adjudications to canonical manifests.

Adjudications are durable inputs to migration.  They are intentionally separate
from generated conflict candidates so rerunning migration cannot erase reviewed
ownership decisions or turn generated suggestions into approvals.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from .manifest_models import CanonicalManifest, ClosedRange


DEFAULT_ADJUDICATIONS_PATH = Path("tools/config/range_adjudications.json")


def range_key(pass_number: int, item: ClosedRange) -> Tuple[int, str, str]:
    return pass_number, item.range_str, item.label


def load_adjudications(path: Path | str = DEFAULT_ADJUDICATIONS_PATH) -> Dict[str, Any]:
    target = Path(path)
    if not target.exists():
        return {"schema_version": 1, "policy_version": "none", "decisions": []}
    return json.loads(target.read_text(encoding="utf-8"))


def apply_adjudications(
    manifests: Dict[int, CanonicalManifest],
    adjudications: Dict[str, Any],
    strict: bool = True,
) -> List[str]:
    """Apply durable decisions and return diagnostics.

    Each decision identifies ranges by pass, canonical interval, and label.  This
    avoids accidentally applying a decision to a later range that merely reuses
    an address.
    """
    index: Dict[Tuple[int, str, str], ClosedRange] = {}
    for pass_number, manifest in manifests.items():
        for item in manifest.closed_ranges:
            index[range_key(pass_number, item)] = item

    diagnostics: List[str] = []
    supersede_groups: Dict[Tuple[int, str, str], List[Dict[str, Any]]] = {}

    # Apply structural helper links first. A later supersession may preserve
    # only the non-overlapping residual bytes of the linked claim.
    for decision in adjudications.get("decisions", []):
        action = decision.get("action")
        subject_data = decision.get("subject", {})
        subject_key = (
            subject_data.get("pass_number"),
            subject_data.get("range"),
            subject_data.get("label"),
        )
        subject = index.get(subject_key)
        if subject is None:
            diagnostics.append(f"missing adjudication subject: {subject_key}")
            continue

        if action == "supersede":
            supersede_groups.setdefault(subject_key, []).append(decision)
        elif action == "link_helper":
            parent = decision.get("parent", {})
            subject.kind = "code_helper"
            subject.parent_range = parent.get("range")
            subject.parent_label = parent.get("label")
            subject.legacy_metadata = dict(subject.legacy_metadata)
            subject.legacy_metadata["ownership_adjudication_id"] = decision.get("decision_id")
        else:
            diagnostics.append(f"unknown adjudication action '{action}' for {subject_key}")

    # A partial overlap does not invalidate the non-overlapping bytes in the
    # weaker historical claim. Preserve the original claim as superseded and
    # emit deterministic active residual fragments after subtracting every
    # winning interval. Exact duplicates and fully-contained losers naturally
    # produce no residual fragments.
    for subject_key, decisions in supersede_groups.items():
        subject = index[subject_key]
        original_kind = subject.kind
        original_parent_range = subject.parent_range
        original_parent_label = subject.parent_label
        residuals = [(subject.start_addr, subject.end_addr)]
        winner_records = []

        for decision in decisions:
            winner_data = decision.get("winner", {})
            winner_key = (
                winner_data.get("pass_number"),
                winner_data.get("range"),
                winner_data.get("label"),
            )
            winner = index.get(winner_key)
            if winner is None:
                diagnostics.append(f"missing adjudication winner: {winner_key}")
                continue
            if winner.bank != subject.bank:
                diagnostics.append(f"cross-bank adjudication for {subject_key}: {winner_key}")
                continue
            winner_records.append(winner_data)
            next_residuals = []
            for start, end in residuals:
                overlap_start = max(start, winner.start_addr)
                overlap_end = min(end, winner.end_addr)
                if overlap_start > overlap_end:
                    next_residuals.append((start, end))
                    continue
                if start < overlap_start:
                    next_residuals.append((start, overlap_start - 1))
                if overlap_end < end:
                    next_residuals.append((overlap_end + 1, end))
            residuals = next_residuals

        decision_ids = [decision.get("decision_id") for decision in decisions]
        subject.kind = "superseded"
        subject.parent_range = winner_records[0].get("range") if winner_records else None
        subject.parent_label = winner_records[0].get("label") if winner_records else None
        subject.legacy_metadata = dict(subject.legacy_metadata)
        subject.legacy_metadata["ownership_adjudication_ids"] = decision_ids

        pass_number = int(subject_key[0])
        manifest = manifests[pass_number]
        for start, end in residuals:
            residual_meta = deepcopy(subject.legacy_metadata)
            residual_meta.update({
                "residual_of": subject.range_str,
                "ownership_adjudication_ids": decision_ids,
                "coverage_treatment": "active_non_overlapping_residual",
            })
            residual = ClosedRange.parse(
                f"{subject.bank}:{start:04X}..{subject.bank}:{end:04X}",
                kind=original_kind,
                label=f"{subject.label}__residual_{start:04x}_{end:04x}",
                confidence=subject.confidence,
                verification_status=subject.verification_status,
                parent_range=original_parent_range,
                parent_label=original_parent_label,
                evidence=deepcopy(subject.evidence),
                legacy_metadata=residual_meta,
            )
            manifest.closed_ranges.append(residual)
            if residual.label not in manifest.new_labels:
                manifest.new_labels.append(residual.label)

    if diagnostics and strict:
        raise ValueError("Invalid range adjudication ledger: " + "; ".join(diagnostics))
    return diagnostics


def iter_manifest_ranges(
    manifests: Dict[int, CanonicalManifest],
) -> Iterable[Tuple[ClosedRange, int, str]]:
    for pass_number, manifest in sorted(manifests.items()):
        source = manifest.source_path or f"passes/manifests/pass{pass_number:04d}.json"
        for item in manifest.closed_ranges:
            yield item, pass_number, source
