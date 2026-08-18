"""Unit tests for range ownership and collision detection."""

from tools.ctrepo.manifest_models import ClosedRange
from tools.ctrepo.range_model import detect_range_conflicts, compute_byte_union

def test_detect_exact_duplicate():
    r1 = ClosedRange.parse("C0:1000..C0:1050", label="f1")
    r2 = ClosedRange.parse("C0:1000..C0:1050", label="f2")
    conflicts = detect_range_conflicts([(r1, 100, "p1"), (r2, 101, "p2")])
    assert len(conflicts) == 1
    assert conflicts[0].relationship == "exact_duplicate"

def test_detect_partial_overlap():
    r1 = ClosedRange.parse("C0:1000..C0:1050", label="f1")
    r2 = ClosedRange.parse("C0:1040..C0:1080", label="f2")
    conflicts = detect_range_conflicts([(r1, 100, "p1"), (r2, 101, "p2")])
    assert len(conflicts) == 1
    assert conflicts[0].relationship == "partial_overlap"
    assert conflicts[0].overlap_range_str == "C0:1040..C0:1050"

def test_detect_containment_helper():
    r1 = ClosedRange.parse("C0:1000..C0:1050", kind="code_owner", label="parent")
    r2 = ClosedRange.parse("C0:1010..C0:1020", kind="code_helper", label="child", parent_range="C0:1000..C0:1050")
    # If parent_range is specified, it should not trigger an error conflict
    conflicts = detect_range_conflicts([(r1, 100, "p1"), (r2, 101, "p2")])
    assert len(conflicts) == 0

def test_compute_byte_union():
    r1 = ClosedRange.parse("C0:1000..C0:1050") # 81 bytes
    r2 = ClosedRange.parse("C0:1040..C0:1080") # extends to 1080 -> 129 bytes
    r3 = ClosedRange.parse("C1:2000..C1:2010") # 17 bytes
    res = compute_byte_union([r1, r2, r3])
    assert res["bank_covered_bytes"]["C0"] == 0x81  # 129 bytes
    assert res["bank_covered_bytes"]["C1"] == 0x11  # 17 bytes
    assert res["total_covered_bytes"] == 0x81 + 0x11
