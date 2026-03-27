# Chrono Trigger Disassembly

Repo-native workspace for the ongoing Chrono Trigger (SNES, USA) ROM disassembly effort.

## Current live state
- working branch: `live-work-from-pass166`
- latest completed pass: `181`
- current forward seam: `C3:1C00..`
- completion estimate: `~73.6%`
- source of truth: this GitHub repo, not chat exports or old toolkit zips

## What this repo contains
- `passes/manifests/` — machine-readable pass history
- `passes/disasm/` — per-pass disassembly notes
- `passes/labels/` — per-pass label notes
- `tools/` — repo-native toolkit scripts, config, and workflow docs
- `reports/` — bank progress, audits, and toolkit-status notes
- `repo_sync/` — earlier sync packets from the repo-first transition phase
- `handoffs/` — master handoff snapshots for the next session

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
- `tools/scripts/build_call_anchor_report_v3.py`
- `tools/scripts/scan_range_entry_callers_v2.py`
- `tools/scripts/detect_tiny_veneers_v1.py`
- `tools/scripts/run_c3_candidate_flow_v1.py`
- `tools/scripts/emit_bank_c3_progress_v1.py`
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
- read the latest handoff in `handoffs/`
- stay on `live-work-from-pass166`
- resume from `C3:1C00..`
- use the upgraded xref/anchor workflow before claiming new owners/helpers
