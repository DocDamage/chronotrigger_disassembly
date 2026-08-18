"""Unit tests for range ownership, exact duplicates, and parent-child containment."""

from tools.ctrepo.manifest_models import ClosedRange
from tools.ctrepo.range_model import detect_range_conflicts, compute_byte_union

def test_exact_duplicate_detection():
    r1 = ClosedRange.parse("C0:1000..C0:1050", label="primary_owner")
    r2 = ClosedRange.parse("C0:1000..C0:1050", label="duplicate_owner")
    conflicts = detect_range_conflicts([(r1, 165, "pass0165.json"), (r2, 169, "pass0169.json")])
    assert len(conflicts) == 1
    assert conflicts[0].relationship == "exact_duplicate"

def test_superseded_duplicate_excluded_from_conflict():
    r1 = ClosedRange.parse("C0:1000..C0:1050", label="primary_owner")
    r2 = ClosedRange.parse("C0:1000..C0:1050", kind="superseded", label="duplicate_owner", parent_range="C0:1000..C0:1050")
    # r2 is superseded so when computing byte union it is excluded
    res = compute_byte_union([r1, r2])
    assert res["total_covered_bytes"] == 0x51

def test_parent_child_containment():
    parent = ClosedRange.parse("C0:7F16..C0:7F9D", kind="code_owner", label="parent_routine")
    child = ClosedRange.parse("C0:7F43..C0:7F56", kind="code_helper", label="child_helper", parent_range="C0:7F16..C0:7F9D")
    conflicts = detect_range_conflicts([(parent, 560, "p560"), (child, 561, "p561")])
    # Parent-child relation is explicit, so no conflict is raised
    assert len(conflicts) == 0
