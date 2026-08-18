"""Unit tests for artifact validation and encoding normalization."""

import json
from tools.scripts.validate_repository_artifacts import detect_and_normalize_file

def test_detect_and_normalize_valid_utf8(tmp_path):
    f = tmp_path / "valid.json"
    f.write_text(json.dumps({"key": "value"}), encoding="utf-8")
    rec = detect_and_normalize_file(str(f), normalize=False)
    assert rec["status"] == "valid"
    assert rec["original_encoding"] == "utf-8"

def test_detect_and_normalize_utf8_bom(tmp_path):
    f = tmp_path / "bom.json"
    f.write_bytes(b"\xef\xbb\xbf" + json.dumps({"key": "value"}).encode("utf-8"))
    rec = detect_and_normalize_file(str(f), normalize=True)
    assert rec["status"] == "normalized"
    assert rec["original_encoding"] == "utf-8-sig"
    # Re-reading should be valid utf-8 without BOM
    new_raw = f.read_bytes()
    assert not new_raw.startswith(b"\xef\xbb\xbf")

def test_detect_and_rename_traceback(tmp_path):
    f = tmp_path / "failed.json"
    f.write_text("Traceback (most recent call last):\n  File a.py, line 1\nZeroDivisionError", encoding="utf-8")
    rec = detect_and_normalize_file(str(f), normalize=True)
    assert rec["status"] == "renamed"
    assert rec["new_path"].endswith(".log")
