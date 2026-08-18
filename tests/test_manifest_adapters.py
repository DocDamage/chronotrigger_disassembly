"""Unit tests for legacy manifest adapters."""

from tools.ctrepo.manifest_adapters import adapt_to_canonical, detect_schema_family

def test_detect_schema_family():
    assert detect_schema_family({"schema_version": 2, "closed_ranges": []}) == "canonical_v2"
    assert detect_schema_family({"closed_ranges": []}) == "canonical_v1"
    assert detect_schema_family({"targets": []}) == "legacy_targets"
    assert detect_schema_family({"promotions": []}) == "promotions"
    assert detect_schema_family({"function_range": "C0:1000..C0:1020"}) == "single_function"
    assert detect_schema_family({"scanned_pages": []}) == "scan_report"

def test_adapt_legacy_targets():
    raw = {
        "pass": 500,
        "targets": [
            {"start_address": "C1:4000", "end_address": "C1:4050", "name": "c1_func", "type": "function"}
        ]
    }
    m = adapt_to_canonical(raw)
    assert m.pass_number == 500
    assert m.schema_version == 2
    assert len(m.closed_ranges) == 1
    assert m.closed_ranges[0].range_str == "C1:4000..C1:4050"
    assert m.closed_ranges[0].label == "c1_func"
    assert m.closed_ranges[0].kind == "code_owner"

def test_adapt_promotions():
    raw = {
        "pass_number": 1229,
        "promotions": [
            {
                "function_range": "C3:CB47..C3:CB64",
                "name": "ct_c3_cb47_php_prologue",
                "score": 6,
                "verification_status": "reviewed",
                "evidence": {"callers": ["C3:28E9"]}
            }
        ]
    }
    m = adapt_to_canonical(raw)
    assert m.pass_number == 1229
    assert len(m.closed_ranges) == 1
    assert m.closed_ranges[0].range_str == "C3:CB47..C3:CB64"
    assert m.closed_ranges[0].label == "ct_c3_cb47_php_prologue"
    assert m.closed_ranges[0].evidence.get("callers") == ["C3:28E9"]
