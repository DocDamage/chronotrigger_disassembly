"""Unit tests for manifest models and range parsing."""

import pytest
from tools.ctrepo.manifest_models import ClosedRange, CanonicalManifest

def test_closed_range_parse_valid():
    r = ClosedRange.parse("C0:1000..C0:1050", kind="code_owner", label="test_func")
    assert r.bank == "C0"
    assert r.start_addr == 0x1000
    assert r.end_addr == 0x1050
    assert r.byte_count == 0x51
    assert r.range_str == "C0:1000..C0:1050"
    assert r.label == "test_func"

def test_closed_range_parse_hyphen():
    r = ClosedRange.parse("C3:2000-C3:2020", kind="code_helper", label="helper_func")
    assert r.bank == "C3"
    assert r.start_addr == 0x2000
    assert r.end_addr == 0x2020
    assert r.range_str == "C3:2000..C3:2020"

def test_closed_range_invalid_cross_bank():
    with pytest.raises(ValueError, match="Cross-bank"):
        ClosedRange.parse("C0:1000..C1:1000")

def test_closed_range_reversed():
    with pytest.raises(ValueError, match="Reversed"):
        ClosedRange.parse("C0:2000..C0:1000")

def test_canonical_manifest_to_dict():
    cr = ClosedRange.parse("C0:1000..C0:1020", label="my_func")
    m = CanonicalManifest(pass_number=100, closed_ranges=[cr])
    d = m.to_dict()
    assert d["schema_version"] == 2
    assert d["pass_number"] == 100
    assert len(d["closed_ranges"]) == 1
    assert d["closed_ranges"][0]["range"] == "C0:1000..C0:1020"
