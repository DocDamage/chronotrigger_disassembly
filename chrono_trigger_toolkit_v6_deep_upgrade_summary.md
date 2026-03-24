# Chrono Trigger Toolkit v6 Deep Upgrade Summary

This was a toolkit-upgrade pass, not a new disassembly pass. The live ROM-analysis state remains anchored at **pass 106**.

## What was upgraded

### 1) Workspace/state consistency
- Added a stronger state sync path so the toolkit now refreshes both:
  - `state/current_state.json`
  - `state/workspace_config.json`
- The synced state now carries:
  - latest pass
  - live seam
  - canonical completion score source
  - toolkit version
  - workspace root name
  - sync timestamp

### 2) Runtime evidence lane
- Added/standardized runtime trace intake assets:
  - `traces/imported/README.md`
  - `traces/templates/runtime_trace_template.csv`
  - `traces/templates/runtime_trace_template.json`
  - `notes/emulator_capture_quickstart.md`
- Added `scripts/ct_trace_normalize.py` so messy raw trace text can be normalized before import.
- Added live-seam-aware capture planning via:
  - `scripts/ct_runtime_capture_plan.py`
  - `reports/runtime/runtime_capture_plan.md`
  - `reports/runtime/runtime_capture_plan.json`

### 3) Score/report discipline
- Added score history tracking via:
  - `scripts/ct_score_history.py`
  - `state/score_history.json`
  - `reports/completion/ct_score_history.md`
  - `reports/completion/ct_score_history.json`
- Canonical completion source remains:
  - `reports/completion/ct_completion_score.json`
- This reduces handoff drift and percentage confusion between passes.

### 4) Toolkit self-audit
- Added `scripts/ct_toolkit_doctor.py`
- Added generated audit outputs:
  - `reports/ct_toolkit_doctor.md`
  - `reports/ct_toolkit_doctor.json`
- Current toolkit doctor result after upgrade: **100.0% health score**

### 5) Seam prioritization
- Added `scripts/ct_prioritize_seams.py`
- Added:
  - `reports/ct_seam_priority.md`
  - `reports/ct_seam_priority.json`
- This gives ranked next-work candidates instead of only a single handwritten seam note.

### 6) Rebuild lane hardening
- Added/strengthened rebuild assets:
  - `build/rebuild/README.md`
  - `build/rebuild/assemble_stub.sh`
  - `build/rebuild/build_manifest.json`
  - `build/rebuild/build_manifest.md`
- Added `scripts/ct_generate_build_manifest.py`
- Added improved rebuild diff reporting via `scripts/ct_rebuild_diff.py`

### 7) Source/rebuild visibility
- Improved source-state reporting through `scripts/ct_source_state_report.py`
- Improved workspace summary generation through `scripts/ct_make_report.py`
- Improved resume/bootstrap path through `scripts/ct_resume_workspace.py`

### 8) Broken script repair
- Fixed `scripts/ct_label_diff.py`, which was shipped in a broken Python state.

### 9) Workspace hygiene
- Rebuilt the toolkit under a clean root that matches the live project state:
  - `ct_pass106_toolkit_v6_work`
- This replaces the old misleading root naming mismatch.

## Important current outputs
- Toolkit doctor: `reports/ct_toolkit_doctor.md`
- Runtime capture plan: `reports/runtime/runtime_capture_plan.md`
- Seam priority: `reports/ct_seam_priority.md`
- Workspace report: `reports/ct_workspace_report.md`
- Completion score: `reports/completion/ct_completion_score.json`
- Score history: `reports/completion/ct_score_history.md`
- Rebuild diff report: `reports/ct_rebuild_diff_report.md`

## Current known truths after the upgrade
- Latest disassembly pass: **106**
- Canonical completion estimate: **~68.9%**
- Toolkit doctor health: **100.0%**
- Rebuild mode: **starter**
- Runtime evidence rows currently linked: **0**

## What this upgrade does NOT magically solve
- It does **not** create runtime evidence by itself; traces still need to be captured/imported.
- It does **not** produce a real rebuilt ROM yet; rebuild remains in starter mode until a real assembler path is wired in and exercised.
- It does **not** finish the disassembly; it makes the toolkit materially better at continuing it.

## Best next disassembly seam after this toolkit upgrade
Stay on the already-isolated live seam:
- **`FD:C1EE..C2C0`**

Specifically freeze:
- what pointer/table family it seeds
- how it finalizes or materializes `7E:0128`
- whether `0153` and `0126` are true mode/state bytes or only local builder selectors in this family
