# Release Audit

- Latest pass: **142**
- Toolkit version: **v6.3**
- Health score: **83.3%**
- Zip audited: `/mnt/data/ct_toolkit_upgrade_work/ct_disasm_toolkit_v6_3_pass142_toolkit_release_refresh.zip`

## Checks
- **workspace_state_present**: ok
  - details: `{"latest_pass": 142, "toolkit_version": "v6.3"}`
- **workspace_smoke_sync**: needs work
  - details: `{"smoke_latest_pass": 139, "state_latest_pass": 142, "inspect_target": "C2:DE98..C2:DF76"}`
- **workspace_session_packet_sync**: ok
  - details: `{"packet_latest_pass": 142, "state_latest_pass": 142, "target_count": 12}`
- **workspace_doctor_present**: ok
  - details: `{"doctor_health_percent": 100.0, "warning_count": 1}`
- **workspace_release_manifest_sync**: ok
  - details: `{"manifest_latest_pass": 142, "state_latest_pass": 142, "manifest_root_name": "ct_pass142_toolkit_v6_3_release_work", "expected_root_name": "ct_pass142_toolkit_v6_3_release_work"}`
- **zip_single_top_root**: ok
  - details: `{"top_roots": ["ct_pass142_toolkit_v6_3_release_work"]}`
- **zip_root_name_sync**: ok
  - details: `{"zip_root_name": "ct_pass142_toolkit_v6_3_release_work", "expected_root_name": "ct_pass142_toolkit_v6_3_release_work"}`
- **zip_required_release_files_present**: ok
  - details: `{"missing_files": []}`
- **zip_state_latest_pass_sync**: ok
  - details: `{"zip_state_latest_pass": 142, "expected_latest_pass": 142}`
- **zip_smoke_latest_pass_sync**: needs work
  - details: `{"zip_smoke_latest_pass": 139, "expected_latest_pass": 142, "inspect_target": "C2:DE98..C2:DF76"}`
- **zip_session_packet_latest_pass_sync**: ok
  - details: `{"zip_packet_latest_pass": 142, "expected_latest_pass": 142, "target_count": 12}`
- **zip_release_manifest_sync**: ok
  - details: `{"zip_manifest_latest_pass": 142, "expected_latest_pass": 142, "zip_manifest_root_name": "ct_pass142_toolkit_v6_3_release_work", "expected_root_name": "ct_pass142_toolkit_v6_3_release_work"}`

## Warnings
- workspace_smoke_sync
- zip_smoke_latest_pass_sync
