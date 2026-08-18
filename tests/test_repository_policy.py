"""Tests for repository policy, doctor subprocess semantics, and report provenance."""

import subprocess
import sys

from tools.ctrepo.policy_validation import validate_all_policy_registries
from tools.ctrepo.provenance import calculate_generator_source_digest, create_provenance_header
from tools.scripts.check_report_drift import _semantic_markdown
from tools.scripts.toolkit_doctor import stable_pytest_summary
from tools.scripts.validate_repository_artifacts import parse_structured_text


def test_report_provenance_structure():
    header = create_provenance_header("test_generator.py")
    assert "source_commit" in header or "git_commit" in header
    assert "manifest_set_digest" in header
    assert "generated_at_utc" in header
    assert header["generation_command"].startswith("python ")


def test_generator_source_digest_ignores_checkout_line_endings(tmp_path):
    lf_source = tmp_path / "lf.py"
    crlf_source = tmp_path / "crlf.py"
    lf_source.write_bytes(b"print('one')\nprint('two')\n")
    crlf_source.write_bytes(b"print('one')\r\nprint('two')\r\n")
    assert calculate_generator_source_digest(lf_source) == calculate_generator_source_digest(crlf_source)


def test_semantic_markdown_ignores_provenance_only_lines():
    first = "# Report\n\n- **Generated**: `first`\n- **Source Commit**: `aaa`\n- **Metric**: 1\n"
    second = "# Report\r\n\r\n- **Generated**: `second`\r\n- **Source Commit**: `bbb`\r\n- **Metric**: 1\r\n"
    assert _semantic_markdown(first) == _semantic_markdown(second)


def test_policy_registries_and_evidence_are_valid():
    assert validate_all_policy_registries() == []


def test_doctor_pytest_summary_drops_nondeterministic_timing():
    assert stable_pytest_summary("35 passed in 6.29s\n") == "35 passed"


def test_artifact_validator_accepts_multi_document_yaml():
    assert parse_structured_text("a: 1\n---\nb: 2\n", "fixture.yaml") == [
        {"a": 1},
        {"b": 2},
    ]


def test_tracked_generated_xref_cache_policy():
    result = subprocess.run(["git", "ls-files", "*raw_xref*"], capture_output=True, text=True)
    tracked_files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    for tracked_file in tracked_files:
        assert not tracked_file.startswith("reports/chrono_trigger_raw_xref")
        assert not tracked_file.startswith("reports/seam_cache/")


def test_no_prohibited_binary_archives_or_roms_are_tracked():
    result = subprocess.run(
        [sys.executable, "tools/scripts/validate_binary_policy.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
