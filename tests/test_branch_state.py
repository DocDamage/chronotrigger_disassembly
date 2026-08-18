"""Unit tests for branch state audit and session handling."""

import json
from tools.scripts.audit_branch_state_v1 import main
from unittest.mock import patch

def test_audit_branch_state_empty_sessions(tmp_path):
    # Setup temporary empty directories
    manifests_dir = tmp_path / "manifests"
    manifests_dir.mkdir()
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()

    # Create a minimal manifest
    m1 = manifests_dir / "pass0100.json"
    m1.write_text(json.dumps({
        "schema_version": 2,
        "pass_number": 100,
        "status": "reviewed",
        "branch": "test",
        "live_seam_after_pass": "C0:1000..",
        "closed_ranges": [{"range": "C0:1000..C0:1020", "kind": "code_owner", "label": "f1"}]
    }), encoding="utf-8")

    test_args = [
        "audit_branch_state_v1.py",
        "--manifests-dir", str(manifests_dir),
        "--sessions-dir", str(sessions_dir),
        "--bank-progress", str(tmp_path / "nonexistent.json"),
        "--generated-progress", str(tmp_path / "nonexistent_gen.json")
    ]

    with patch("sys.argv", test_args):
        # Should not raise exception even with empty sessions dir and missing progress files
        exit_code = main()
        assert exit_code == 0
