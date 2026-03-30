# Chrono Trigger Disassembly

Repo-native workspace for the ongoing Chrono Trigger (SNES, USA) ROM disassembly effort.

## Current live state
- working branch: `live-work-from-pass166`
- latest manifest-backed pass: `191`
- latest continuation note: `docs/sessions/chrono_trigger_session15_continue_notes_54.md`
- latest closed block: `C6:CC00..C6:D5FF`
- current forward seam: `C6:D600..`
- note-backed continuation run closed `41` ten-page blocks from `C5:3B00` through `C6:D5FF` with `0` promotions
- effective closed-range snapshot: `tools/cache/closed_ranges_snapshot_v1.json` now refreshes from manifests plus session-15 continuation notes and currently carries `715` closed ranges (`65` manifest-backed + `650` note-backed page freezes)
- completion estimate: see latest handoff - coarse `%` metric is not reliable at current granularity
- source of truth: this GitHub repo, not chat exports or old toolkit zips
- continuation notes are the operative state-of-record from pass 191 onward, and their frozen pages now feed caller-context scoring through the seam snapshot layer (see `docs/sessions/chrono_trigger_session15_continue_notes_*.md`)

## What this repo contains
- `passes/manifests/` — machine-readable pass history
- `passes/disasm/` — per-pass disassembly notes
- `passes/labels/` — per-pass label notes
- `tools/` — repo-native toolkit scripts, config, and workflow docs
- `reports/` — generated bank progress, seam-block, anchor, and toolkit-status artifacts
- `repo_sync/` — earlier sync packets from the repo-first transition phase
- `disassembly/` — legacy disassembly-note mirror through pass `163` (historical)
- `labels/` — legacy label-note mirror through pass `163` (historical)
- `toolkits/` — archived toolkit zip bundles; not the active tooling tree
- `docs/handoffs/` — master handoff snapshots and resume checklists
- `docs/sessions/` — continuation notes and next-session starting documents
- `docs/reports/raw_seams/` — long-form seam-facing raw report markdown

## Authority map
If you need to know what is active vs historical vs archive-only, read:
- `docs/handoffs/chrono_trigger_repo_authority_map_2026-03-30.md`

If you need the short backlog of older note-backed near-miss pages worth revisiting only on new evidence, read:
- `docs/handoffs/chrono_trigger_revisit_backlog_from_session15_notes.md`

If you are browsing subdirectories directly, the local status guides now live in:
- `docs/handoffs/README.md`
- `docs/sessions/README.md`
- `docs/reports/README.md`
- `reports/README.md`
- `passes/README.md`

## Current workflow
1. treat the repo branch as canonical
2. identify the next honest seam
3. refresh the seam cache so the closed-range snapshot reflects manifests plus note-backed frozen pages
4. scan for tiny veneers / branch pads / return stubs
5. evaluate raw callers with bank-aware validation and caller-context scoring
6. only promote code when the local bytes and caller context both hold up
7. publish a canonical pass manifest only for manifest-backed work; otherwise publish the continuation note and report bundle

## Toolkit highlights
The active toolkit lives under `tools/`.

Key scripts now in use:
- `tools/scripts/ensure_seam_cache_v1.py` — refreshes the xref index and effective closed-range snapshot
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
The project has now pushed a long conservative seam run from `C5:3B00` through `C6:D5FF` without a single defensible owner/helper promotion.
That is not stalled work. It is strong negative evidence that this corridor is mixed command/data territory dominated by weak-only anchors, invalid companion targets, and dead/no-ingress pages.
The current job is still to preserve label quality, not to manufacture code out of hot mixed-content pages.
The high-priority tooling repair before the next block is now done: callers from already frozen note-backed pages no longer masquerade as unresolved weak support by default.

## Start here next session
- read the latest handoff in `docs/handoffs/` - currently `chrono_trigger_master_handoff_session16.md`
- read the repo authority map - `docs/handoffs/chrono_trigger_repo_authority_map_2026-03-30.md`
- read the latest continuation notes - currently `docs/sessions/chrono_trigger_session15_continue_notes_54.md`
- read the current resume checklist - `docs/handoffs/chrono_trigger_resume_checklist_c6_d600_dfff.md`
- read the short revisit backlog only if new caller-quality evidence appears - `docs/handoffs/chrono_trigger_revisit_backlog_from_session15_notes.md`
- stay on `live-work-from-pass166`
- run `python3 tools/scripts/audit_branch_state_v1.py` first to confirm the effective seam is still `C6:D600..`
- resume from `C6:D600..`
- run `run_seam_block_v1.py --start C6:D600 --pages 10` first; it now auto-refreshes `tools/cache/closed_ranges_snapshot_v1.json` from manifests plus continuation notes before scanning
- only run owner-backtrack and anchor reports for pages that the new block marks `manual_owner_boundary_review`
- write `docs/sessions/chrono_trigger_session15_continue_notes_55.md` after the block closes
- do not backfill manifests during seam work; the manifest layer is still frozen at pass `191`, but the seam snapshot now bridges the closed note-backed pages automatically
- promotion standard: caller quality + start-byte quality + local structure must all converge
