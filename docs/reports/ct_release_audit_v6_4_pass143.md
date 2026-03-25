# Release Audit

- Latest pass: **143**
- Toolkit version: **v6.4**
- Health score: **100.0%**
- Zip audited: `/mnt/data/ct_disasm_toolkit_v6_4_pass143_continued.zip`

## Checks
- **workspace_state_present**: ok
  - details: `{"latest_pass": 143, "toolkit_version": "v6.4"}`
- **workspace_smoke_sync**: ok
  - details: `{"smoke_latest_pass": 143, "state_latest_pass": 143, "inspect_target": "C2:E60B..C2:E760"}`
- **workspace_session_packet_sync**: ok
  - details: `{"packet_latest_pass": 143, "state_latest_pass": 143, "target_count": 12}`
- **workspace_doctor_present**: ok
  - details: `{"doctor_health_percent": 100.0, "warning_count": 1}`
- **workspace_release_manifest_sync**: ok
  - details: `{"manifest_latest_pass": 143, "state_latest_pass": 143, "manifest_root_name": "ct_pass143_toolkit_v6_4_release_work", "expected_root_name": "ct_pass143_toolkit_v6_4_release_work"}`
- **zip_single_top_root**: ok
  - details: `{"top_roots": ["ct_pass143_toolkit_v6_4_release_work"]}`
- **zip_root_name_sync**: ok
  - details: `{"zip_root_name": "ct_pass143_toolkit_v6_4_release_work", "expected_root_name": "ct_pass143_toolkit_v6_4_release_work"}`
- **zip_required_release_files_present**: ok
  - details: `{"missing_files": []}`
- **zip_state_latest_pass_sync**: ok
  - details: `{"zip_state_latest_pass": 143, "expected_latest_pass": 143}`
- **zip_smoke_latest_pass_sync**: ok
  - details: `{"zip_smoke_latest_pass": 143, "expected_latest_pass": 143, "inspect_target": "C2:E60B..C2:E760"}`
- **zip_session_packet_latest_pass_sync**: ok
  - details: `{"zip_packet_latest_pass": 143, "expected_latest_pass": 143, "target_count": 12}`
- **zip_release_manifest_sync**: ok
  - details: `{"zip_manifest_latest_pass": 143, "expected_latest_pass": 143, "zip_manifest_root_name": "ct_pass143_toolkit_v6_4_release_work", "expected_root_name": "ct_pass143_toolkit_v6_4_release_work"}`
