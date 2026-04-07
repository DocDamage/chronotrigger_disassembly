# Chrono Trigger Disassembly

Repo-native workspace for the ongoing Chrono Trigger (SNES, USA) ROM disassembly effort.

## Current live state
- working branch: `live-work-from-pass166`
- latest manifest-backed pass: `247`
- latest continuation note: `docs/sessions/chrono_trigger_session15_continue_notes_79.md`
- latest closed block: C3:B16F..C3:B1D0 (B100 region, score-6 cluster)
- current forward seam: `C3:B1D0..` (Bank C3 gap-filling ongoing)
- Session 20 completed 30 promotions in Bank C3 (passes 218-247), increasing C3 coverage from 10% to 17.6%
- effective closed-range snapshot: `tools/cache/closed_ranges_snapshot_v1.json` now carries 987+ closed ranges (85 manifest-backed + 900+ continuation)
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

## Current status (Session 20 Complete)

### Major Achievement: Bank C3 Expansion
Session 20 achieved the largest single-session mapping effort to date:
- **30 new promotions** in Bank C3 (passes 218-247)
- **Bank C3 coverage: 17.6%** (up from ~10%)
- **95 total ranges** now documented in C3
- **11.5KB** of code mapped in Bank C3

### Session 20 Summary
Targeted the largest remaining gaps in Bank C3:
- Filled 0528-08A1 gap (partially)
- Mapped high-density 1900-1C00 block
- Major progress in 2800-4C00 region (13 promotions)
- Partially filled 4CFF-A396 gap (6 promotions)
- Partially filled A3FF-C244 gap (5 promotions)

### Remaining Work
- Bank C3: Several large gaps remain (5600-80C4: 10.9KB, 8CFF-A396: 5.8KB)
- Bank C7: ~95% mapped, minor gaps remain
- Banks C0, C1, C2, C4-C6, CF: Largely unexplored

See detailed report: `docs/session_20_progress_report.md`

## Start here next session
- read the Session 20 progress report: `docs/session_20_progress_report.md`
- read the repo authority map: `docs/handoffs/chrono_trigger_repo_authority_map_2026-03-30.md`
- stay on `live-work-from-pass166`
- options for next work:
  1. Continue Bank C3 gap-filling (target 5600-80C4, 8CFF-A396, or small gaps)
  2. Switch to new bank (C0, C1, C2 recommended for fresh targets)
  3. Complete Bank C7 to 100% coverage
- promotion standard: score >= 6 + internal evidence (RTS/PHP/JSR) + regional context
- run `python tools/scripts/score_target_owner_backtrack_v1.py` for candidate identification
- run `build_call_anchor_report_v3.py` for caller validation when needed
