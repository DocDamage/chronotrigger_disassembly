# Chrono Trigger Disassembly

Repo-native workspace for the ongoing Chrono Trigger (SNES, USA) ROM disassembly effort.

## Current live state
- working branch: `live-work-from-pass166`
- latest manifest-backed pass: `191`
- current forward seam: `C5:6300..`
- completion estimate: see latest handoff — coarse `%` metric is not reliable at current granularity
- source of truth: this GitHub repo, not chat exports or old toolkit zips
- continuation notes are the operative state-of-record from pass 191 onward (see `docs/sessions/chrono_trigger_session15_continue_notes_*.md`)

## What this repo contains
- `passes/manifests/` — machine-readable pass history
- `passes/disasm/` — per-pass disassembly notes
- `passes/labels/` — per-pass label notes
- `tools/` — repo-native toolkit scripts, config, and workflow docs
- `reports/` — generated bank progress, seam-block, anchor, and toolkit-status artifacts
- `repo_sync/` — earlier sync packets from the repo-first transition phase
- `docs/handoffs/` — master handoff snapshots and resume checklists
- `docs/sessions/` — continuation notes and next-session starting documents
- `docs/reports/raw_seams/` — long-form seam-facing raw report markdown

## Current workflow
1. treat the repo branch as canonical
2. identify the next honest seam
3. scan for tiny veneers / branch pads / return stubs
4. evaluate raw callers with bank-aware validation and caller-context scoring
5. only promote code when the local bytes and caller context both hold up
6. publish the pass manifest, disasm note, and label note to the branch

## Toolkit highlights
The active toolkit lives under `tools/`.

Key scripts now in use:
- `tools/scripts/run_seam_block_v1.py` — 10-page block scanner (primary seam workflow)
- `tools/scripts/render_seam_block_report_v1.py` — renders block JSON to Markdown
- `tools/scripts/run_c3_candidate_flow_v7.py` — per-page candidate triage
- `tools/scripts/score_target_owner_backtrack_v1.py` — backtrack scorer for owner candidates
- `tools/scripts/find_local_code_islands_v2.py` — return-anchored local island finder
- `tools/scripts/seam_triage_utils_v1.py` — shared opcode classification utilities
- `tools/scripts/build_call_anchor_report_v3.py`
- `tools/scripts/snes_utils_hirom_v2.py`

## Why the toolkit changed
Recent `C3` work exposed three recurring problems:
- fake cross-bank same-bank anchors
- over-trusting callers that still live in unresolved mixed-content regions
- missing tiny executable splinters buried inside noisy seams

The newer flow is designed to stop those mistakes before they turn into bad labels.

## Current no-BS status
The project is still moving forward, but the current high-bank `C3` lane is mixed-content heavy.
A lot of forward progress since pass 171 has come from refusing fake monolithic code claims and instead peeling out only the executable pieces that survive structural and caller-context checks.

## Start here next session
- read the latest handoff in `docs/handoffs/` — currently `chrono_trigger_master_handoff_session15.md`
- read the latest continuation notes — currently `docs/sessions/chrono_trigger_session15_continue_notes_17.md`
- stay on `live-work-from-pass166`
- resume from `C5:6300..`
- run `run_seam_block_v1.py --start C5:6300 --pages 10` first, then anchor reports for any `manual_owner_boundary_review` pages
- promotion standard: caller quality + start-byte quality + local structure must all converge
