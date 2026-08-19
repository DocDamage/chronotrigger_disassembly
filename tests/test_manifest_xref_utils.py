from __future__ import annotations

import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "tools" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from manifest_xref_utils import ClosedRange, anchor_strength, classify_caller_context, classify_kind


def test_canonical_code_kinds_are_executable() -> None:
    assert classify_kind("code_owner") == "code"
    assert classify_kind("code_helper") == "code"
    assert classify_kind("data") == "data"
    assert classify_kind("superseded") == "unknown"


def test_only_reviewed_code_is_a_strong_anchor() -> None:
    pending = ClosedRange(0xC3, 0x8000, 0x80FF, "code_owner", "pending", "high", 1)
    reviewed = ClosedRange(
        0xC3, 0x8100, 0x81FF, "code_owner", "reviewed", "high", 2, "reviewed"
    )
    ranges = [pending, reviewed]

    pending_context = classify_caller_context(ranges, "C3:8001")
    reviewed_context = classify_caller_context(ranges, "C3:8101")

    assert pending_context["caller_status"] == "pending_code"
    assert anchor_strength("valid", pending_context["caller_status"]) == "weak"
    assert reviewed_context["caller_status"] == "resolved_code"
    assert anchor_strength("valid", reviewed_context["caller_status"]) == "strong"
