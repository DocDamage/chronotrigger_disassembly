# Chrono Trigger Disassembly

Repo-native workspace for the ongoing Chrono Trigger (SNES, USA) ROM disassembly effort.

## Current live state
- working branch: `live-work-from-pass166`
- latest manifest-backed pass: `306`
- latest continuation-note snapshot: `docs/sessions/chrono_trigger_session15_continue_notes_100.md` (historical C7 summary through pass 217)
- latest closed block: C0:77DB..C0:77E3 (Bank C0, score-6 cluster)
- current forward seam: `C0:7800..` (Bank C0 mapping ongoing)
- **Session 23 completed 30 promotions in Bank C0 (passes 277-306)**, increasing C0 coverage from 0 to 55 documented ranges
- Session 20 completed 30 promotions in Bank C3 (passes 218-247), increasing C3 coverage from 10% to 17.6%
- effective closed-range snapshot: `tools/cache/closed_ranges_snapshot_v1.json` now carries 1081+ closed ranges (181 manifest-backed + 900 continuation)
- completion estimate: see latest handoff - coarse `%` metric is not reliable at current granularity
- source of truth: this GitHub repo, not chat exports or old toolkit zips
- continuation notes remain important historical context for the earlier C7 seam, and their frozen pages still feed caller-context scoring through the seam snapshot layer

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

## Current status (Session 23 Complete)

### Major Achievement: Bank C0 Discovery and Mapping
Session 23 achieved the first comprehensive mapping of Bank C0:
- **30 new promotions** in Bank C0 (passes 277-306)
- **Bank C0: 55 documented ranges** (first-ever mapping of this bank)
- Rich code regions identified from 4000-7700 with strong RTS/JSR patterns

### Session 23 Summary
Systematically mapped Bank C0 score-6 clusters:
- Page 4000 region: C0:407C-408E, C0:4098-40B3
- Page 4600 region: C0:4612-4670
- Page 5200-5C00 region: C0:520E-5280, C0:5406-5470, C0:5A77-5A90, C0:5C8D-5CC6
- Page 6000-6400 region: C0:6070-607D, C0:629B-62CA, C0:639D-63E5
- Page 6600-6F00 region: C0:67D7-67E2, C0:6896-68A4, C0:6986-698A, C0:6E1E-6EF0, C0:6F08-6F5D
- Page 7000-7700 region: C0:70E7-70E8, C0:7162-716F, C0:749B-77E3

### Cumulative Progress
| Bank | Ranges | Status |
|------|--------|--------|
| C0 | 55 | Actively mapping |
| C3 | 99 | 17.6% coverage |
| C7 | 27 | ~95% mapped |
| **Total** | **181** | 144 manifests |

### Remaining Work
- Bank C0: Continue mapping 7800-FFFF region (upper half largely unexplored)
- Bank C3: Several large gaps remain (5600-80C4: 10.9KB, 8CFF-A396: 5.8KB)
- Bank C7: ~95% mapped, minor gaps remain
- Banks C1, C2, C4-C6, CF: Largely unexplored

See detailed report: `docs/session_23_progress_report.md`

## Start here next session
- read the Session 23 progress report: `docs/session_23_progress_report.md`
- read the repo authority map: `docs/handoffs/chrono_trigger_repo_authority_map_2026-03-30.md`
- stay on `live-work-from-pass166`
- options for next work:
  1. Continue Bank C0 mapping (target 7800-FFFF region)
  2. Return to Bank C3 gap-filling (target 5600-80C4, 8CFF-A396)
  3. Switch to new bank (C1, C2, C4-C6 recommended for fresh targets)
  4. Complete Bank C7 to 100% coverage
- promotion standard: score >= 6 + internal evidence (RTS/PHP/JSR) + regional context
- run `python tools/scripts/score_target_owner_backtrack_v1.py` for candidate identification
- run `build_call_anchor_report_v3.py` for caller validation when needed
