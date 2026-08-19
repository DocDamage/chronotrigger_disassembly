"""Apply reviewed factual corrections after legacy migration and ownership adjudication."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .manifest_models import CanonicalManifest, ClosedRange


REPO_ROOT = Path(__file__).resolve().parents[2]


def load_manifest_corrections(path: str | Path | None = None) -> Dict[str, Any]:
    target = Path(path) if path else REPO_ROOT / "tools" / "config" / "manifest_corrections.json"
    return json.loads(target.read_text(encoding="utf-8"))


def _selection_subjects(selection: Dict[str, Any], manifests=None) -> List[Dict[str, Any]]:
    """Resolve an exact-count batch against canonical identities without changing them."""
    records: List[Dict[str, Any]] = []
    if manifests is None:
        for path in sorted((REPO_ROOT / "passes" / "manifests").glob("pass[0-9][0-9][0-9][0-9].json")):
            document = json.loads(path.read_text(encoding="utf-8"))
            pass_number = document["pass_number"]
            for item in document.get("closed_ranges", []):
                records.append({"pass_number": pass_number, "item": item})
    else:
        for pass_number, manifest in manifests.items():
            for item in manifest.closed_ranges:
                records.append({"pass_number": pass_number, "item": item})

    bank = selection.get("bank")
    include_kinds = set(selection.get("kinds", []))
    exclude_kinds = set(selection.get("exclude_kinds", []))
    subjects: List[Dict[str, Any]] = []
    for record in records:
        item = record["item"]
        range_text = item["range"] if isinstance(item, dict) else item.range_str
        kind = item["kind"] if isinstance(item, dict) else item.kind
        label = item["label"] if isinstance(item, dict) else item.label
        if bank and not range_text.startswith(f"{bank}:"):
            continue
        if include_kinds and kind not in include_kinds:
            continue
        if kind in exclude_kinds:
            continue
        subjects.append({"pass_number": record["pass_number"], "range": range_text, "label": label})
    subjects.sort(key=lambda item: (item["pass_number"], item["range"], item["label"]))
    expected_count = selection.get("expected_count")
    if expected_count is not None and len(subjects) != expected_count:
        raise ValueError(
            f"manifest correction selector expected {expected_count} subjects but matched {len(subjects)}: {selection}"
        )
    return subjects


def iter_manifest_corrections(registry: Dict[str, Any], manifests=None):
    """Yield ordinary corrections plus expanded, template-driven correction batches."""
    yield from registry.get("corrections", [])
    for batch in registry.get("bulk_corrections", []):
        template = batch.get("updates", {})
        subjects = batch.get("subjects")
        if subjects is None:
            subjects = _selection_subjects(batch["selection"], manifests=manifests)
        for index, subject in enumerate(subjects, start=1):
            updates = dict(template)
            suffix = updates.pop("label_suffix", None)
            if suffix:
                bank, start = subject["range"].split("..", 1)[0].split(":", 1)
                updates["label"] = f"ct_{bank.lower()}_{start.lower()}_{suffix}"
            yield {
                "correction_id": f"{batch['correction_id']}_{index:03d}",
                "subject": subject,
                "reason": batch["reason"],
                "evidence": batch["evidence"],
                "updates": updates,
            }


def _range_key(pass_number: int, item: ClosedRange) -> Tuple[int, str, str]:
    return pass_number, item.range_str, item.label


def apply_manifest_corrections(
    manifests: Dict[int, CanonicalManifest],
    registry: Dict[str, Any],
    strict: bool = True,
) -> List[str]:
    index = {
        _range_key(pass_number, item): (manifest, item)
        for pass_number, manifest in manifests.items()
        for item in manifest.closed_ranges
    }
    diagnostics: List[str] = []
    for correction in iter_manifest_corrections(registry, manifests=manifests):
        identity = correction.get("subject", {})
        key = (
            identity.get("pass_number"),
            identity.get("range"),
            identity.get("label"),
        )
        match = index.get(key)
        if match is None:
            diagnostics.append(f"missing manifest correction subject: {key}")
            continue
        manifest, item = match
        updates = correction.get("updates", {})
        old_label = item.label
        for field in (
            "kind",
            "label",
            "confidence",
            "verification_status",
            "parent_range",
            "parent_label",
            "evidence",
        ):
            if field in updates:
                setattr(item, field, updates[field])
        if item.label != old_label:
            manifest.new_labels = [item.label if label == old_label else label for label in manifest.new_labels]
            index.pop(key, None)
            index[_range_key(manifest.pass_number, item)] = (manifest, item)
    if diagnostics and strict:
        raise ValueError("Invalid manifest correction ledger: " + "; ".join(diagnostics))
    return diagnostics
