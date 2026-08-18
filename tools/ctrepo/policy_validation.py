"""Schema and semantic validation for repository policy registries."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List

import jsonschema


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMA_DIR = REPO_ROOT / "tools" / "config" / "schemas"


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _schema_errors(document: Dict[str, Any], schema_name: str) -> List[str]:
    schema = _load(SCHEMA_DIR / schema_name)
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    return [f"{error.json_path}: {error.message}" for error in validator.iter_errors(document)]


def _commit_exists(commit: str) -> bool:
    if not commit:
        return False
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=REPO_ROOT,
        capture_output=True,
    )
    return result.returncode == 0


def validate_gap_registry(path: Path | None = None) -> List[str]:
    target = path or REPO_ROOT / "tools" / "config" / "intentional_pass_gaps.json"
    document = _load(target)
    errors = _schema_errors(document, "intentional_pass_gaps.schema.json")
    entries = document.get("intentional_gaps", {})
    if document.get("total_gaps_count") != len(entries):
        errors.append("total_gaps_count does not equal registry entry count")
    for key, entry in entries.items():
        if str(entry.get("pass_number")) != key:
            errors.append(f"gap key {key} does not match pass_number {entry.get('pass_number')}")
        if entry.get("status") != "baseline_absent":
            errors.append(f"gap {key} is not fully accounted: {entry.get('status')}")
        if not _commit_exists(entry.get("evidence_commit", "")):
            errors.append(f"gap {key} evidence_commit is not a reachable commit")
        for evidence in entry.get("evidence", []):
            if not (REPO_ROOT / evidence).exists():
                errors.append(f"gap {key} evidence path does not exist: {evidence}")
    return errors


def validate_waiver_registry(path: Path | None = None) -> List[str]:
    target = path or REPO_ROOT / "tools" / "config" / "range_overlap_waivers.json"
    document = _load(target)
    errors = _schema_errors(document, "range_overlap_waivers.schema.json")
    waivers = document.get("waivers", [])
    if document.get("total_waivers_count") != len(waivers):
        errors.append("total_waivers_count does not equal waiver entry count")
    for waiver in waivers:
        conflict_id = waiver.get("conflict_id", "<unknown>")
        if not _commit_exists(waiver.get("review_commit", "")):
            errors.append(f"waiver {conflict_id} review_commit is not reachable")
        for evidence in waiver.get("evidence", []):
            if not (REPO_ROOT / evidence).exists():
                errors.append(f"waiver {conflict_id} evidence path does not exist: {evidence}")
    return errors


def validate_migration_ledger(path: Path | None = None) -> List[str]:
    target = path or REPO_ROOT / "passes" / "manifests" / "manifest_migration_map.json"
    document = _load(target)
    errors = _schema_errors(document, "manifest_migration_ledger.schema.json")
    records = document.get("migration_records", [])
    if document.get("total_source_files") != len(records):
        errors.append("total_source_files does not equal migration record count")
    source_keys = [
        (record.get("original_source_path"), record.get("source_sha256"))
        for record in records
    ]
    if len(source_keys) != len(set(source_keys)):
        errors.append("migration ledger contains duplicate original path/hash identities")
    return errors


def validate_range_adjudications(path: Path | None = None) -> List[str]:
    target = path or REPO_ROOT / "tools" / "config" / "range_adjudications.json"
    document = _load(target)
    errors = _schema_errors(document, "range_adjudications.schema.json")
    decisions = document.get("decisions", [])
    if document.get("decision_count") != len(decisions):
        errors.append("decision_count does not equal adjudication entry count")
    decision_ids = [decision.get("decision_id") for decision in decisions]
    if len(decision_ids) != len(set(decision_ids)):
        errors.append("range adjudication decision IDs are not unique")
    if not _commit_exists(document.get("source_commit", "")):
        errors.append("range adjudication source_commit is not reachable")
    canonical_identities = set()
    for manifest_path in (REPO_ROOT / "passes" / "manifests").glob("pass[0-9][0-9][0-9][0-9].json"):
        manifest = _load(manifest_path)
        pass_number = manifest.get("pass_number")
        for item in manifest.get("closed_ranges", []):
            canonical_identities.add((pass_number, item.get("range"), item.get("label")))
    for decision in decisions:
        decision_id = decision.get("decision_id", "<unknown>")
        for role in ("subject", "winner"):
            identity = decision.get(role, {})
            key = (identity.get("pass_number"), identity.get("range"), identity.get("label"))
            if key not in canonical_identities:
                errors.append(f"adjudication {decision_id} {role} is absent from canonical manifests: {key}")
        rank = decision.get("rank", {})
        if rank.get("winner", []) < rank.get("subject", []):
            errors.append(f"adjudication {decision_id} winner rank is lower than subject rank")
        for evidence in decision.get("evidence", []):
            if not (REPO_ROOT / evidence).exists():
                errors.append(f"adjudication {decision_id} evidence path does not exist: {evidence}")
    return errors


def validate_project_state(path: Path | None = None) -> List[str]:
    target = path or REPO_ROOT / "tools" / "config" / "project_state.json"
    document = _load(target)
    errors = _schema_errors(document, "project_state.schema.json")
    for evidence in document.get("evidence", []):
        if not (REPO_ROOT / evidence).exists():
            errors.append(f"project-state evidence path does not exist: {evidence}")
    pass_number = document.get("latest_manifest_pass")
    if isinstance(pass_number, int):
        manifest_path = REPO_ROOT / "passes" / "manifests" / f"pass{pass_number:04d}.json"
        if not manifest_path.exists():
            errors.append(f"project state latest manifest does not exist: {manifest_path}")
        else:
            manifest = _load(manifest_path)
            if manifest.get("live_seam_after_pass") != document.get("live_seam"):
                errors.append("project-state seam does not match latest canonical manifest")
    return errors


def validate_report_provenance(provenance: Dict[str, Any]) -> List[str]:
    return _schema_errors(provenance, "report_provenance.schema.json")


def validate_all_policy_registries() -> List[str]:
    errors: List[str] = []
    for name, validator in (
        ("gaps", validate_gap_registry),
        ("waivers", validate_waiver_registry),
        ("migration", validate_migration_ledger),
        ("range_adjudications", validate_range_adjudications),
        ("project_state", validate_project_state),
    ):
        try:
            errors.extend(f"{name}: {error}" for error in validator())
        except Exception as exc:
            errors.append(f"{name}: {exc}")
    return errors
