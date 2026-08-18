"""Regression tests for manifest migration idempotency, multi-source merging, and conservation."""

import json

from tools.ctrepo.manifest_models import CanonicalManifest, ClosedRange

from tools.ctrepo.manifest_discovery import discover_manifest_candidates
from tools.ctrepo.manifest_validation import validate_manifest

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
