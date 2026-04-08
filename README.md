# Chrono Trigger Disassembly

Repo-native workspace for the ongoing Chrono Trigger (SNES, USA) ROM disassembly effort.

## Current live state
- working branch: `live-work-from-pass166`
- latest manifest-backed pass: `763`
- latest continuation-note snapshot: `docs/sessions/chrono_trigger_session15_continue_notes_100.md` (historical C7 summary through pass 217)
- latest closed block: CF:F3DC..CF:F404 (Bank CF, score-8 cluster)
- current forward seam: `CF:D000..` (Bank CF mapping ongoing)
- **Session 23 completed 30 promotions in Bank C0 (passes 277-306)**, increasing C0 coverage from 0 to 55 documented ranges
- **Session 24 completed 42 promotions in Bank C0 (passes 307-348)**, increasing C0 coverage from 55 to 97 documented ranges
- **Agent Swarm Session (passes 555-578)** added 24 new manifests across Banks C0, C1, C2, C3, C5
- **Agent Swarm Session 2 (passes 579-603)** added 25 new manifests, deep scans of C5, C1 hubs, C0 continuation
- **Agent Swarm Session 3 (passes 604-620)** added 17 new manifests, C3:5000 major discovery, C1:8000 hub, C0:9000 continuation
- **Agent Swarm Session 4 (passes 621-640)** added 20 new manifests, C1 dispatch table, C2 cross-bank hub, C4 initial mapping
- **Agent Swarm Session 5 (passes 641-658)** added 18 new manifests, C4 deep scan, C6 initial mapping, C1 dispatch completion
- **Agent Swarm Session 6 (passes 659-676)** added 18 new manifests, C6:D400 highest density, C4 cross-bank, C1 dispatch progress
- **Agent Swarm Session 7 (passes 677-697)** added 21 new manifests, C6:D800 RTL, C4:4000, C0:0000, C1 dispatch COMPLETE
- **Agent Swarm Session 8 (passes 698-715)** added 18 new manifests, C4:9000-FFFF, CF bank initial, C3 gaps, C5 deep scan
- **Agent Swarm Session 9 (passes 716-733)** added 18 new manifests, CF:E000-F000 major region, C6:E000-FFFF completion, C3:6000 completion
- **Agent Swarm Session 10 (passes 734-763)** added 30 new manifests, CF:F000-FFFF highest density, C4:4000-5000, **D1 bank discovered!**
- **C1:8C3E Dispatch Hub COMPLETE**: All 42 handler functions documented (C1:8E00-9800)
- effective closed-range snapshot: `tools/cache/closed_ranges_snapshot_v1.json` now carries 1081+ closed ranges (181 manifest-backed + 900 continuation)
- completion estimate: see latest handoff - coarse `%` metric is not reliable at current granularity
- source of truth: this GitHub repo, not chat exports or old toolkit zips
- continuation notes remain important historical context for the earlier C7 seam, and their frozen pages still feed caller-context scoring through the seam snapshot layer

## What this repo contains
- `passes/manifests/` — machine-readable pass history (763 manifests)
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
- `tools/generate_coverage_report_v2.py` — coverage statistics with overlap handling
- `tools/scripts/detect_data_patterns_v1.py` — identifies data vs code structures
- `tools/scripts/validate_cross_bank_callers_v1.py` — validates cross-bank caller integrity

## Why the toolkit changed
Recent `C3` work exposed three recurring problems:
- fake cross-bank same-bank anchors
- over-trusting callers that still live in unresolved mixed-content regions
- missing tiny executable splinters buried inside noisy seams

The newer flow is designed to stop those mistakes before they turn into bad labels.

## Current status (Agent Swarm Session 10 Complete)

### Major Achievement: Bank CF and D1 Discovery
Session 10 achieved major breakthroughs in Bank CF (highest density region) and discovered Bank D1:
- **30 new promotions** across Banks CF, C4, C3, and **D1**
- **Bank CF: 31 documented ranges, 1.62% coverage** (F000-FFFF: 19 score-6+ clusters)
- **Bank D1: 5 documented ranges, 0.65% coverage** (NEW BANK! 394 code islands found)
- **C1:8C3E Dispatch Hub 100% COMPLETE** - all 42 handlers documented

### Session 10 Summary
Systematically mapped highest-density regions:
- **CF:F000-FFFF**: 19 score-6+ clusters including CF:F3DC-F404 (score-8, highest confidence)
- **CF:E000-F000**: 3 score-6+ clusters (E000-E0FF identified as data, excluded)
- **C4:4000-5000**: 3 score-6 clusters (41BA, 481E, 4ABB)
- **C3 gaps**: 5 gap fills (0000-01E3, 0529-08A0, 6000-6FFF)
- **D1 discovery**: 5 score-6/7 clusters including D1:0509-053C (near C4 caller)

### Cross-Bank Connectivity Verified
- **D1 → C4:C0C0 callers**: D1:0236, D1:04BF, D1:35E1 (all verified JSL)
- **C2:8000-8004**: 5 verified cross-bank callers (JSL hub)
- **C4:C0C0**: Jump vector table with callers from multiple banks

### Cumulative Progress (Session 10)
| Bank | Ranges | Coverage | Status |
|------|--------|----------|--------|
| C0 | 215 | 17.25% | Active |
| C1 | 24 | 1.70% | Dispatch complete |
| C2 | 10 | 1.35% | Cross-bank hub mapped |
| C3 | 50 | 19.46% | Gap filling 90%+ |
| C4 | 37 | 1.80% | Deep scan active |
| C5 | 13 | 1.69% | Deep scan active |
| C6 | 15 | 0.50% | D400-D800 mapped |
| C7 | 23 | 2.16% | 95% mapped |
| **CF** | **31** | **1.62%** | **Major discovery** |
| **D1** | **5** | **0.65%** | **NEW BANK!** |
| **Total** | **423** | **4.82%** | **763 manifests** |

### Toolkit Updates (Session 10)
- `generate_coverage_report_v2.py`: Fixed overlapping range handling (prevents negative coverage)
- `detect_data_patterns_v1.py`: Identifies data vs code (C6:CC00-D000 = data structure)
- `validate_cross_bank_callers_v1.py`: Detects fake cross-bank misidentifications

### Remaining Work
- **Bank CF**: Continue D000-E000 region (12 score-6+ clusters pending)
- **Bank D1**: Expand mapping (90+ score-5+ islands identified)
- **Bank C5**: Systematic deep scan (~40 pages)
- **Banks D2-D9**: Exploration for more code banks
- **Bank C3**: Final gap completion (target 28% coverage)

See detailed reports:
- `AGENT_SWARM_SESSION_10_SUMMARY.md`
- `C1_8C3E_DISPATCH_COMPLETION_REPORT.md`
- `C3_GAP_ANALYSIS_FINAL_REPORT.md`

## Start here next session
- read the Session 10 summary: `AGENT_SWARM_SESSION_10_SUMMARY.md`
- read the repo authority map: `docs/handoffs/chrono_trigger_repo_authority_map_2026-03-30.md`
- stay on `live-work-from-pass166`
- options for next work:
  1. **Bank CF**: Complete D000-E000 region (high priority - major code bank)
  2. **Bank D1**: Expand initial mapping (90+ islands waiting)
  3. **Bank C5**: Systematic deep scan (major unexplored bank)
  4. **Banks D2-D9**: Find more code banks
  5. **Bank C3**: Final gap completion
- promotion standard: score >= 6 + internal evidence (RTS/PHP/JSR) + regional context
- run `python tools/scripts/score_target_owner_backtrack_v1.py` for candidate identification
- run `tools/generate_coverage_report_v2.py` for coverage statistics
