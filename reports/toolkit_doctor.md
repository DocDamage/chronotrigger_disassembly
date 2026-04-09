# Toolkit Doctor

- overall health: **100.0%**
- passing checks: **8 / 8**

## Checks

- **python_script_compile_health**: ok
  {
    "script_count": 102,
    "failures": []
  }
- **legacy_entrypoints_upgraded**: ok
  {
    "required": [
      "tools/scripts/find_next_callable_lane.py",
      "tools/scripts/build_call_anchor_report.py",
      "tools/scripts/classify_c3_ranges.py",
      "tools/scripts/validate_labels.py",
      "tools/scripts/publish_pass_bundle.py",
      "tools/scripts/update_bank_progress.py"
    ],
    "missing": [],
    "stub_markers": []
  }
- **doc_script_references**: ok
  {
    "referenced_scripts": [
      "tools/scripts/build_call_anchor_report_v3.py",
      "tools/scripts/detect_data_patterns_v1.py",
      "tools/scripts/ensure_seam_cache_v1.py",
      "tools/scripts/find_local_code_islands_v2.py",
      "tools/scripts/render_seam_block_report_v1.py",
      "tools/scripts/run_c3_candidate_flow_v7.py",
      "tools/scripts/run_seam_block_v1.py",
      "tools/scripts/score_target_owner_backtrack_v1.py",
      "tools/scripts/seam_triage_utils_v1.py",
      "tools/scripts/snes_utils_hirom_v2.py",
      "tools/scripts/toolkit_doctor.py",
      "tools/scripts/update_bank_progress.py",
      "tools/scripts/validate_cross_bank_callers_v1.py"
    ],
    "missing": []
  }
- **low_bank_mapping**: ok
  {
    "samples": [
      {
        "address": "C3:0000",
        "offset": 196608
      },
      {
        "address": "C3:0557",
        "offset": 197975
      },
      {
        "address": "CF:F3DC",
        "offset": 1045468
      }
    ],
    "mismatches": []
  }
- **core_help_smoke**: ok
  {
    "smoke_targets": [
      "tools/scripts/find_next_callable_lane.py",
      "tools/scripts/build_call_anchor_report.py",
      "tools/scripts/classify_c3_ranges.py",
      "tools/scripts/validate_labels.py",
      "tools/scripts/publish_pass_bundle.py",
      "tools/scripts/update_bank_progress.py"
    ],
    "failures": []
  }
- **manifest_schema_smoke**: ok
  {
    "sample_manifests": [
      "passes/manifests/pass402.json",
      "passes/manifests/pass763.json"
    ],
    "failures": []
  }
- **branch_state_audit**: ok
  {
    "returncode": 0,
    "stdout_tail": [
      "latest manifest seam: C0:7F61-7F7A",
      "latest continuation note: chrono_trigger_session15_continue_notes_100.md",
      "note-backed live seam: (missing)",
      "effective live seam: C0:7F61-7F7A",
      "warnings found:",
      "  - missing manifest pass numbers: [282, 304, 305, 307, 312, 316, 322, 331, 335, 341, 357, 361, 384, 388, 392, 398, 400, 411, 412, 413, 425, 457, 478, 479, 484, 537]",
      "branch state audit ok"
    ],
    "stderr_tail": []
  }
- **duplicate_helper_drift**: ok
  {
    "targets": [
      "tools/scripts/detect_data_patterns_v1.py",
      "tools/scripts/validate_cross_bank_callers_v1.py",
      "tools/scripts/page_range_mixedness_v1.py",
      "tools/scripts/score_owner_boundary_risk_v1.py",
      "tools/scripts/find_local_code_islands_v1.py",
      "tools/scripts/score_raw_xref_context_v1.py",
      "tools/scripts/seam_triage_utils_v1.py"
    ],
    "offenders": []
  }
