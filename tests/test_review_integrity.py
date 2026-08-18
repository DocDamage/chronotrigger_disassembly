"""Regression tests for review status fidelity, confidence normalization, and gap validation."""

from tools.ctrepo.manifest_adapters import adapt_to_canonical


def test_pending_final_review_remains_pending():
    # Pass 1228 legacy promotion schema
    doc = {
        "pass_number": 1228,
        "function_range": "C3:CB00..C3:CB46",
        "label": "sound_command_dispatch",
        "confidence": "medium",
        "verification_status": "pending_final_review"
    }
    m = adapt_to_canonical(doc, "promotions", source_path="pass1228.json")
    assert len(m.closed_ranges) == 1
    cr = m.closed_ranges[0]
    # pending_final_review must map to pending, NOT reviewed
    assert cr.verification_status == "pending"
    assert cr.confidence == "medium"

def test_missing_verification_status_does_not_default_to_reviewed():
    doc = {
        "pass": 500,
        "ranges": [{"range": "C0:1000..C0:1010", "label": "test_fn"}]
    }
    m = adapt_to_canonical(doc, "canonical_v1", source_path="pass0500.json")
    cr = m.closed_ranges[0]
    assert cr.verification_status in ("pending", "draft", None)
    assert cr.verification_status != "reviewed"

def test_numeric_score_does_not_raise_source_confidence():
    # Score 6 must not convert into high confidence automatically
    doc = {
        "pass": 1010,
        "range": "C3:1627..C3:1642",
        "label": "ct_c3_1627",
        "confidence": 6
    }
    m = adapt_to_canonical(doc, "single_function", source_path="pass1010.json")
    cr = m.closed_ranges[0]
    # Score is preserved in evidence, confidence is conservative
    assert cr.evidence.get("score") == 6 or cr.confidence in ("medium", "score-6", "pending")
    assert cr.confidence != "high"
