# Chrono Trigger Workspace Report

## Current top-of-stack
- Latest pass: **161**
- Current live seam: **C3:0077..C3:01E3**
- Completion estimate: **~70.2%**
- Completion source: **`reports/completion/ct_completion_score.json`**
- State/score sync ok: **yes**
- Toolkit version: **v6.7**
- Toolkit health score: **100.0%**

## Label database
- Total label rows: **1310**
- Strong: **992**
- Provisional: **150**
- Alias: **42**
- Caution: **57**
- Runtime evidence rows: **0**
- Runtime linked labels: **0**

## Coverage worksheets
- Master C1 global opcode worksheet rows: **170**
- Selector-control worksheet rows: **83**
- Service-7 wrapper worksheet rows: **8**

## Xref cache
- Hot targets cached: **33**

## Generated artifacts
- `reports/ct_completion_score.md`
- `reports/completion/ct_consistency_report.md`
- `reports/completion/ct_score_history.md`
- `reports/ct_toolkit_doctor.md`
- `reports/code_data_score.md`
- `reports/runtime/runtime_capture_plan.md`
- `reports/runtime/runtime_label_links.md`
- `reports/ct_unresolved_dashboard.md`
- `reports/ct_seam_priority.md`
- `reports/ct_dispatch_family_report.md`
- `reports/ct_apu_packet_summary.md`
- `reports/ct_runtime_validation.md`
- `reports/ct_source_state.md`
- `reports/ct_rebuild_diff_report.md`
- `build/rebuild/build_manifest.md`

## Immediate next work
1. Read `notes/next_session_start_here.md` and stay on that seam before going broad.
2. Use `reports/runtime/runtime_capture_plan.md` and the templates under `traces/templates/` before capturing emulator evidence.
3. Use `reports/ct_toolkit_doctor.md` if the toolkit itself starts feeling suspect.
4. Use `reports/ct_seam_priority.md` when multiple seams look equally tempting.
5. Use `build/rebuild/assemble_stub.sh` as the starter wiring point when you begin a real assembler loop.

## Score history snapshot
- pass 142: **~69.9%**
- pass 143: **~70.0%** (Δ +0.1)
- pass 145: **~70.2%** (Δ +0.2)
- pass 150: **~70.6%** (Δ +0.4)
- pass 161: **~70.2%** (Δ -0.4)

## Sync warnings
- none

## Still required for full disassembly
- Complete bank-by-bank code/data separation across the untouched ROM banks
- Finish decompressor grammar / format work
- Freeze subsystem ownership boundaries across banks
- Build a rebuildable source tree and validate against ROM fingerprints
