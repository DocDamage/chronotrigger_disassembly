from __future__ import annotations

import subprocess
import sys
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools" / "scripts"))

from tools.scripts.run_seam_block_v1 import compact_result  # noqa: E402


def test_seam_analysis_entrypoints_load() -> None:
    scripts = (
        "score_raw_xref_context_v3.py",
        "score_target_owner_backtrack_v1.py",
    )

    for script in scripts:
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "scripts" / script), "--help"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr


def test_primary_seam_block_pipeline_runs(tmp_path: Path) -> None:
    rom = tmp_path / "fixture.sfc"
    rom.write_bytes(bytes(0x50000))
    manifests = tmp_path / "manifests"
    sessions = tmp_path / "sessions"
    cache = tmp_path / "cache"
    manifests.mkdir()
    sessions.mkdir()

    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "tools" / "scripts" / "run_seam_block_v1.py"),
            "--rom",
            str(rom),
            "--start",
            "C3:0000",
            "--pages",
            "1",
            "--manifests-dir",
            str(manifests),
            "--sessions-dir",
            str(sessions),
            "--cache-dir",
            str(cache),
            "--json",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["pages_requested"] == 1
    assert payload["pages"][0]["range"] == "C3:0000..C3:00FF"


def test_compact_seam_result_filters_noise() -> None:
    payload = {
        "start": "D4:0000",
        "pages_requested": 2,
        "page_family_counts": {"mixed": 2},
        "review_posture_counts": {"manual": 2},
        "pages": [
            {
                "range": "D4:0000..D4:00FF",
                "page_family": "mixed",
                "review_posture": "manual",
                "best_targets": [
                    {"target": "D4:0040", "best_strength": "weak", "hit_count": 4},
                    {"target": "D4:0041", "best_strength": "weak", "hit_count": 1},
                ],
                "top_backtracks": [{"candidate_start": "D4:0037", "score": 6}],
                "local_clusters": [{"range": "D4:0036..D4:004E", "cluster_score": 7}],
            },
            {
                "range": "D4:0100..D4:01FF",
                "page_family": "mixed",
                "review_posture": "manual",
                "best_targets": [],
                "top_backtracks": [{"candidate_start": "D4:0117", "score": 4}],
                "local_clusters": [],
            },
        ],
    }

    compact = compact_result(payload, minimum_score=6)

    assert compact["review_pages"] == 1
    assert compact["candidate_count"] == 1
    assert compact["cluster_count"] == 1
    assert [item["target"] for item in compact["pages"][0]["targets"]] == ["D4:0040"]
