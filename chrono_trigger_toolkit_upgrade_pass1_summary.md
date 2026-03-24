# Chrono Trigger Toolkit Upgrade — Focused Pass 1

## Scope
- consistency lock between pass/seam/score state
- runtime evidence linking to labels and banks
- stronger fake-code-bait detection in code/data scoring
- starter rebuild lane improvements

## Files added
- `scripts/ct_sync_handoff_state.py`
- `scripts/ct_runtime_link_report.py`
- `notes/v5_1_toolkit_upgrade.md`
- `build/rebuild/README.md`
- `build/rebuild/assemble_stub.sh`

## Files upgraded
- `scripts/ct_resume_workspace.py`
- `scripts/ct_apply_pass_to_source.py`
- `scripts/ct_completion_score.py`
- `scripts/ct_runtime_validate.py`
- `scripts/ct_score_code_data.py`
- `scripts/ct_rebuild_diff.py`
- `scripts/ct_make_report.py`
- `scripts/ct_generate_unresolved_dashboard.py`
- `scripts/ct_generate_bank_dossiers.py`
- `README.md`
- `tool_manifest.md`

## Expected impact
- completion percent now has one canonical source
- runtime evidence can promote exact label targets and bank pressure immediately
- WRAM banks stop showing up as fake code winners in the code/data report
- rebuild report now distinguishes starter readiness from bare scaffold status
