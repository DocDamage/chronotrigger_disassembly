"""Unit tests for manifest discovery."""

from tools.ctrepo.manifest_discovery import (
    discover_manifest_candidates,
    extract_pass_from_filename,
    is_canonical_filename
)

def test_filename_helpers():
    assert extract_pass_from_filename("pass0100.json") == 100
    assert extract_pass_from_filename("pass1229_c3_cb47.json") == 1229
    assert extract_pass_from_filename("not_a_pass.json") is None

    assert is_canonical_filename("pass0100.json") is True
    assert is_canonical_filename("pass1229.json") is True
    assert is_canonical_filename("pass1229_c3_cb47.json") is False

def test_discover_fixtures():
    fixtures_dir = "tests/fixtures/manifest_audit"
    results = discover_manifest_candidates(manifests_dir=fixtures_dir)
    assert len(results) > 0
    # Check that pass 1000-era fixtures are discovered
    passes = [r.pass_number for r in results if r.pass_number is not None]
    assert 100 in passes
    assert 1001 in passes
    assert 1004 in passes
