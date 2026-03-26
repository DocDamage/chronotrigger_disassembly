# Release Audit

- Latest pass: **161**
- Toolkit version: **v6.8**
- Health score: **100.0%**
- Zip audited: `/mnt/data/ct_disasm_toolkit_v6_8_pass161_upgraded.zip`

## Checks
- **workspace_state_present**: ok
  - details: `{"latest_pass": 161, "toolkit_version": "v6.8"}`
- **workspace_smoke_sync**: ok
  - details: `{"smoke_latest_pass": 161, "state_latest_pass": 161, "inspect_target": "C3:0077..C3:01E3"}`
- **workspace_session_packet_sync**: ok
  - details: `{"packet_latest_pass": 161, "state_latest_pass": 161, "target_count": 1}`
- **workspace_doctor_present**: ok
  - details: `{"doctor_health_percent": 100.0, "warning_count": 0}`
- **workspace_release_manifest_sync**: ok
  - details: `{"manifest_latest_pass": 161, "state_latest_pass": 161, "manifest_root_name": "ct_pass161_toolkit_v6_8_release_work", "expected_root_name": "ct_pass161_toolkit_v6_8_release_work"}`
- **zip_single_top_root**: ok
  - details: `{"top_roots": ["ct_pass161_toolkit_v6_8_release_work"]}`
- **zip_root_name_sync**: ok
  - details: `{"zip_root_name": "ct_pass161_toolkit_v6_8_release_work", "expected_root_name": "ct_pass161_toolkit_v6_8_release_work"}`
- **zip_required_release_files_present**: ok
  - details: `{"missing_files": []}`
- **zip_state_latest_pass_sync**: ok
  - details: `{"zip_state_latest_pass": 161, "expected_latest_pass": 161}`
- **zip_smoke_latest_pass_sync**: ok
  - details: `{"zip_smoke_latest_pass": 161, "expected_latest_pass": 161, "inspect_target": "C3:0077..C3:01E3"}`
- **zip_session_packet_latest_pass_sync**: ok
  - details: `{"zip_packet_latest_pass": 161, "expected_latest_pass": 161, "target_count": 1}`
- **zip_release_manifest_sync**: ok
  - details: `{"zip_manifest_latest_pass": 161, "expected_latest_pass": 161, "zip_manifest_root_name": "ct_pass161_toolkit_v6_8_release_work", "expected_root_name": "ct_pass161_toolkit_v6_8_release_work"}`
