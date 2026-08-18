"""Tests for repository policy, doctor subprocess semantics, and report provenance."""



from tools.ctrepo.provenance import create_provenance_header

def test_report_provenance_structure():
    header = create_provenance_header("test_generator.py")
    assert "source_commit" in header or "git_commit" in header
    assert "manifest_set_digest" in header
    assert "generated_at_utc" in header

def test_tracked_generated_xref_cache_policy():
    # Ensure raw xref caches are not in git tracking
    import subprocess
    res = subprocess.run(["git", "ls-files", "*raw_xref*"], capture_output=True, text=True)
    tracked_files = [l.strip() for l in res.stdout.splitlines() if l.strip()]
    # None of the tracked files should be generated cache copies under reports/ or repo_sync/seam_cache/
    for tf in tracked_files:
        assert not tf.startswith("reports/chrono_trigger_raw_xref")
        assert not tf.startswith("reports/seam_cache/")
