# Toolkit Smoke Test

- Latest pass: **150**
- Health score: **100.0%**
- Inspect target used: `C2:F2F3..C2:F360`
- Parent-dir harness: `(cleaned automatically; staged via symlink)`

## Cases
- **root_doctor**: ok
  - cwd: `/mnt/data/ctpass150_toolkit_v6_7_release_work`
  - cmd: `["python3", "scripts/ct_toolkit_doctor.py", "--root", ".", "--rom", "Chrono Trigger (USA).sfc", "--output-json", "reports/ct_toolkit_doctor.json", "--output-md", "reports/ct_toolkit_doctor.md"]`
  - stdout tail: `["/mnt/data/ctpass150_toolkit_v6_7_release_work/reports/ct_toolkit_doctor.json", "/mnt/data/ctpass150_toolkit_v6_7_release_work/reports/ct_toolkit_doctor.md"]`
- **root_build_manifest**: ok
  - cwd: `/mnt/data/ctpass150_toolkit_v6_7_release_work`
  - cmd: `["python3", "scripts/ct_generate_build_manifest.py", "--root", ".", "--output-json", "build/rebuild/build_manifest.json", "--output-md", "build/rebuild/build_manifest.md"]`
  - stdout tail: `["/mnt/data/ctpass150_toolkit_v6_7_release_work/build/rebuild/build_manifest.json", "/mnt/data/ctpass150_toolkit_v6_7_release_work/build/rebuild/build_manifest.md"]`
- **root_session_packet**: ok
  - cwd: `/mnt/data/ctpass150_toolkit_v6_7_release_work`
  - cmd: `["python3", "scripts/ct_generate_session_packet.py", "--root", ".", "--rom", "Chrono Trigger (USA).sfc", "--db", "data/ct_label_db.sqlite", "--xref-json", "data/ct_hot_xref_cache.json", "--state-json", "state/current_state.json", "--output-json", "reports/session/current_session_packet.json", "--output-md", "reports/session/current_session_packet.md"]`
  - stdout tail: `["/mnt/data/ctpass150_toolkit_v6_7_release_work/reports/session/current_session_packet.json", "/mnt/data/ctpass150_toolkit_v6_7_release_work/reports/session/current_session_packet.md"]`
- **root_inspect_target**: ok
  - cwd: `/mnt/data/ctpass150_toolkit_v6_7_release_work`
  - cmd: `["python3", "scripts/ct_inspect_target.py", "C2:F2F3..C2:F360", "--root", ".", "--rom", "Chrono Trigger (USA).sfc"]`
  - stdout tail: `["- none", "", "NEARBY LABELS:", "- pass 150 [strong] C2:F2E2..C2:F2F2 :: ct_c2_7d00_table_selector_helper_returning_y_pointer_and_constant_cc0b", "- pass 150 [strong] C2:F2DC..C2:F2E1 :: ct_c2_indexed_local_wrapper_selecting_7d00_pointer_then_tail_jumping_into_ef65", "- pass 150 [strong] C2:F2CC..C2:F2DB :: ct_c2_two_decimal_byte_to_binary_helper_combining_y_y_plus_1_into_a", "", "XREFS:", "- no cached hot-xref targets inside span", "", "NOTE MENTIONS:", "- chrono_trigger_labels_pass150.md"]`
- **parent_doctor_autodetect**: ok
  - cwd: `/tmp/ct_smoke_parent_4apu1vz8`
  - cmd: `["python3", "workspace/scripts/ct_toolkit_doctor.py", "--root", ".", "--rom", "Chrono Trigger (USA).sfc", "--output-json", "reports/ct_toolkit_doctor.json", "--output-md", "reports/ct_toolkit_doctor.md"]`
  - stdout tail: `["/tmp/ct_smoke_parent_4apu1vz8/workspace/reports/ct_toolkit_doctor.json", "/tmp/ct_smoke_parent_4apu1vz8/workspace/reports/ct_toolkit_doctor.md"]`
- **parent_session_packet_autodetect**: ok
  - cwd: `/tmp/ct_smoke_parent_4apu1vz8`
  - cmd: `["python3", "workspace/scripts/ct_generate_session_packet.py", "--root", ".", "--rom", "Chrono Trigger (USA).sfc", "--db", "data/ct_label_db.sqlite", "--xref-json", "data/ct_hot_xref_cache.json", "--state-json", "state/current_state.json", "--output-json", "reports/session/current_session_packet.json", "--output-md", "reports/session/current_session_packet.md"]`
  - stdout tail: `["/tmp/ct_smoke_parent_4apu1vz8/workspace/reports/session/current_session_packet.json", "/tmp/ct_smoke_parent_4apu1vz8/workspace/reports/session/current_session_packet.md"]`
- **parent_inspect_target_autodetect**: ok
  - cwd: `/tmp/ct_smoke_parent_4apu1vz8`
  - cmd: `["python3", "workspace/scripts/ct_inspect_target.py", "C2:F2F3..C2:F360", "--root", ".", "--rom", "Chrono Trigger (USA).sfc"]`
  - stdout tail: `["- none", "", "NEARBY LABELS:", "- pass 150 [strong] C2:F2E2..C2:F2F2 :: ct_c2_7d00_table_selector_helper_returning_y_pointer_and_constant_cc0b", "- pass 150 [strong] C2:F2DC..C2:F2E1 :: ct_c2_indexed_local_wrapper_selecting_7d00_pointer_then_tail_jumping_into_ef65", "- pass 150 [strong] C2:F2CC..C2:F2DB :: ct_c2_two_decimal_byte_to_binary_helper_combining_y_y_plus_1_into_a", "", "XREFS:", "- no cached hot-xref targets inside span", "", "NOTE MENTIONS:", "- chrono_trigger_labels_pass150.md"]`
