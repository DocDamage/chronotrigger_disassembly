"""Regression tests for manifest migration idempotency, multi-source merging, and conservation."""

import json
from pathlib import Path

from tools.ctrepo.manifest_models import CanonicalManifest, ClosedRange
from tools.ctrepo.manifest_discovery import discover_manifest_candidates
from tools.ctrepo.manifest_validation import validate_manifest
from tools.ctrepo.range_adjudication import apply_adjudications
from tools.scripts.migrate_manifests import plan_migration

def test_migration_merges_same_pass_sources_instead_of_skipping_current_manifest(tmp_path):
    # Pass 1000 direct file with range A
    p1 = tmp_path / "pass1000.json"
    p1.write_text(json.dumps({
        "pass": 1000,
        "range": "C0:3D52..C0:3DA8",
        "label": "ct_c0_3d52",
        "status": "draft"
    }), encoding="utf-8")

    # Pass 1000 suffixed file with range B
    p2 = tmp_path / "pass1000_c3_session28.json"
    p2.write_text(json.dumps({
        "pass": 1000,
        "targets": [{"addr": "C3:6641", "coverage_bytes": 9, "label": "ct_c3_6641"}],
        "status": "draft"
    }), encoding="utf-8")

    candidates = discover_manifest_candidates(manifests_dir=str(tmp_path))
    assert len(candidates) == 2
    
    # Both candidates must have pass 1000
    passes = [c.pass_number for c in candidates]
    assert passes == [1000, 1000]

    # Adaptation of both must yield valid ranges
    m1 = candidates[0].manifest
    m2 = candidates[1].manifest
    assert len(m1.closed_ranges) == 1
    assert len(m2.closed_ranges) == 1
    assert m1.closed_ranges[0].range_str == "C0:3D52..C0:3DA8"
    assert m2.closed_ranges[0].range_str == "C3:6641..C3:6649"

def test_filename_pass_must_equal_content_pass():
    # A file named pass0100.json claiming pass 200 must fail validation
    m = CanonicalManifest(
        pass_number=200,
        source_path="passes/manifests/pass0100.json",
        closed_ranges=[ClosedRange.parse("C0:1000..C0:1010")]
    )
    is_valid, errs = validate_manifest(m, strict=True)
    assert not is_valid
    assert any("mismatch" in e.lower() or "does not match" in e.lower() for e in errs)


def test_missing_verification_is_pending_not_reviewed():
    item = ClosedRange.parse("C0:1000..C0:1010")
    assert item.verification_status == "pending"


def test_unknown_range_kind_is_rejected():
    try:
        ClosedRange.parse("C0:1000..C0:1010", kind="invented_kind")
    except ValueError as exc:
        assert "Unknown range kind" in str(exc)
    else:
        raise AssertionError("unknown range kind was silently accepted")


def test_migration_plan_is_idempotent_for_same_sources(tmp_path):
    legacy = tmp_path / "legacy"
    legacy.mkdir()
    (legacy / "pass1000.json").write_text(json.dumps({
        "pass": 1000,
        "range": "C0:3D52..C0:3DA8",
        "label": "ct_c0_3d52",
        "status": "draft",
    }), encoding="utf-8")
    (legacy / "pass1000_extra.json").write_text(json.dumps({
        "pass": 1000,
        "targets": [{"addr": "C3:6641", "coverage_bytes": 9, "label": "ct_c3_6641"}],
        "status": "reviewed",
    }), encoding="utf-8")

    first_manifests, first_ledger = plan_migration(
        str(tmp_path), apply_ownership_adjudications=False
    )
    second_manifests, second_ledger = plan_migration(
        str(tmp_path), apply_ownership_adjudications=False
    )

    assert {key: value.to_dict() for key, value in first_manifests.items()} == {
        key: value.to_dict() for key, value in second_manifests.items()
    }
    assert first_ledger == second_ledger
    assert first_manifests[1000].status == "draft"
    assert len(first_ledger) == 2


def test_adjudication_replay_marks_loser_without_dropping_claim():
    loser = ClosedRange.parse("C0:1000..C0:1010", label="loser")
    winner = ClosedRange.parse("C0:1008..C0:1020", label="winner")
    manifests = {
        1: CanonicalManifest(pass_number=1, closed_ranges=[loser]),
        2: CanonicalManifest(pass_number=2, closed_ranges=[winner]),
    }
    ledger = {
        "decisions": [{
            "decision_id": "adj_test",
            "action": "supersede",
            "subject": {"pass_number": 1, "range": loser.range_str, "label": loser.label},
            "winner": {"pass_number": 2, "range": winner.range_str, "label": winner.label},
        }]
    }

    apply_adjudications(manifests, ledger)

    assert len(manifests[1].closed_ranges) == 2
    assert loser.kind == "superseded"
    assert loser.parent_range == winner.range_str
    assert loser.legacy_metadata["ownership_adjudication_ids"] == ["adj_test"]
    residuals = [item for item in manifests[1].closed_ranges if item.kind != "superseded"]
    assert [item.range_str for item in residuals] == ["C0:1000..C0:1007"]


def test_committed_canonical_manifests_are_reproducible_from_legacy_sources():
    root = Path(__file__).resolve().parent.parent
    planned, _ = plan_migration()
    committed_paths = sorted((root / "passes" / "manifests").glob("pass[0-9][0-9][0-9][0-9].json"))
    assert len(planned) == len(committed_paths)
    for path in committed_paths:
        pass_number = int(path.stem[4:])
        assert json.loads(path.read_text(encoding="utf-8")) == planned[pass_number].to_dict()
