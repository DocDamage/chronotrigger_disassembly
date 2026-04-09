# Chrono Trigger Disassembly

Repo-native workspace for the ongoing Chrono Trigger (SNES, USA) ROM disassembly effort.

## Current live state
- working branch: `live-work-from-pass166`
- latest manifest-backed pass: `965`
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
- **Agent Swarm Session 11 (passes 764-805)** added 42 new manifests, CF:D000-E000 complete, **D2-D9 banks discovered!**, C5 score-9 cluster, D1 expansion
- **Agent Swarm Session 12 (passes 806-833)** added 28 new manifests, D6 deep scan (22 score-6+), D4 expansion (20+ score-6+), C5:9000 region, D1:1000 region
- **C1:8C3E Dispatch Hub COMPLETE**: All 42 handler functions documented (C1:8E00-9800)
- **C3:30% TARGET ACHIEVED**: 30.5% coverage with dual superclusters (4548 score-13, 4A2A score-11)
- **C0:30% TARGET EXCEEDED**: 31.90% coverage with complete audio and HDMA systems
- **C4:10% TARGET ACHIEVED**: 12.2% coverage, C4:772E score-10 supercluster
- **C2:8% TARGET ACHIEVED**: 8.0% coverage, three score-14 functions discovered
- effective closed-range snapshot: `tools/cache/closed_ranges_snapshot_v1.json` now carries 1200+ closed ranges (280 manifest-backed + 920 continuation)
- completion estimate: see latest handoff - coarse `%` metric is not reliable at current granularity
- source of truth: this GitHub repo, not chat exports or old toolkit zips
- continuation notes remain important historical context for the earlier C7 seam, and their frozen pages still feed caller-context scoring through the seam snapshot layer

## What this repo contains
- `passes/manifests/` — machine-readable pass history (965 manifests)
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
- `tools/scripts/toolkit_doctor.py` — repo-native audit for compile health, low-bank mapping, and CLI compatibility entrypoints
- `tools/generate_coverage_report_v2.py` — coverage statistics with overlap handling
- `tools/scripts/detect_data_patterns_v1.py` — identifies data vs code structures
- `tools/scripts/validate_cross_bank_callers_v1.py` — validates cross-bank caller integrity

## Why the toolkit changed
Recent `C3` work exposed three recurring problems:
- fake cross-bank same-bank anchors
- over-trusting callers that still live in unresolved mixed-content regions
- missing tiny executable splinters buried inside noisy seams

The newer flow is designed to stop those mistakes before they turn into bad labels.

## Current status (Agent Swarm Session 31 Complete)

### Major Achievement: 31 Agent Swarm Sessions Complete - C0 Exceeds 30%!
Session 31 achieved the **30% target for Bank C0** and major discoveries across all active banks:
- **84 new promotions** across C0, C1, C2, C3, C4 (pass1000-1009, pass1115-1126, pass1200-1208, pass1500-1519, pass0758-0769)
- **Bank C0: 31.90% coverage** - TARGET EXCEEDED (18 new functions, complete audio/HDMA systems)
- **Bank C2: 8.0% coverage** - Three score-14 functions discovered (8F6D, 8C08, 8DA3)
- **Bank C3: 30.5% coverage** - Dual superclusters (4548 score-13, 4A2A score-11)
- **Bank C4: 12.2% coverage** - C4:772E score-10 supercluster documented
- **Bank C1: 7.6% coverage** - Mega-cluster at 434A (score-17), 84% candidate pool processed

### Session 31 Coverage Updates
| Bank | New Ranges | Coverage Change |
|------|------------|-----------------|
| C0 | +31 | 28.02% → 31.90% (TARGET EXCEEDED!) |
| C2 | +12 | 6.8% → 8.0% |
| C3 | +20 | 28.8% → 30.5% (30% ACHIEVED!) |
| C4 | +12 | 9.57% → 12.2% (10% ACHIEVED!) |
| C1 | +9 | 6.8% → 7.6% |
| **Total** | **+84** | **10.5% → 13.68%** |

### Previous Session (Agent Swarm Session 11 Complete)

### Major Achievement: Banks D2-D9 Discovered!
Session 11 achieved the biggest bank discovery yet - **8 new code banks (D2-D9)**:
- **42 new promotions** across CF, D1, C5, C4, and **D2-D9**
- **Bank CF: 2.14% coverage** (D000-E000 now complete with 12 new functions)
- **Bank D1: Expanded** (19 score-6+ candidates, 505 islands, 335 clusters)
- **Banks D2-D9: ALL CODE BANKS!** (D6 has 49 cross-bank callers - highest)
- **Bank C5: Score-9 cluster found** (C5:9BC1 - highest in bank)

### Session 11 Summary
Systematically mapped priority regions:
- **CF:D000-E000**: 12 new functions including CF:DAF0-DB2A (score-8)
- **D1 expansion**: 19 score-6+ including D1:0D28-0D42 (score-12 EXCEPTIONAL)
- **C5 deep scan**: 15 new functions including C5:9BC1 (score-9, highest in C5)
- **D2-D9 discovery**: All 8 banks are CODE banks! D4:45BB (score-9), D6:68FB (score-8)
- **C4:8000-9000**: 16 new ranges, C4:8010 hub confirmed

### Cross-Bank Connectivity Verified
- **D1 → C4:C0C0 callers**: D1:0236, D1:04BF, D1:35E1 (all verified JSL)
- **C4:8010 hub**: 22 fake cross-bank callers filtered, internal callers verified
- **D6**: 49 cross-bank callers (highest count) - called from C4, C6, C7, CA
- **D4**: 36 cross-bank callers - major new hub potential

### Cumulative Progress (Session 31)
| Bank | Ranges | Coverage | Status |
|------|--------|----------|--------|
| C0 | 308 | 31.90% | TARGET EXCEEDED! |
| C1 | 89 | 7.60% | Mega-cluster mapped |
| C2 | 75 | 8.00% | Score-14 discovered |
| C3 | 285 | 30.50% | Dual superclusters |
| C4 | 146 | 12.20% | Score-10 supercluster |
| C5 | 28 | 4.10% | Score-9 discovered |
| C6 | 15 | 0.50% | D400-D800 mapped |
| C7 | 23 | 2.16% | 95% mapped |
| CF | 43 | 2.14% | D000-FFFF complete |
| D1 | 24 | 2.05% | 505 islands found |
| D2 | 1 | 0.04% | New bank |
| D3 | 1 | 0.04% | New bank |
| D4 | 5 | 0.20% | New bank |
| D6 | 5 | 0.20% | New bank |
| D7 | 1 | 0.04% | New bank |
| D8 | 1 | 0.04% | New bank |
| D9 | 1 | 0.04% | New bank |
| **Total** | **935** | **13.68%** | **920+ manifests** |

### Toolkit Health: 100%
All upgraded toolkit scripts verified working across 31 sessions:
- `toolkit_doctor.py`: All 8 checks passing
- 102 Python scripts compile successfully
- Legacy entrypoints upgraded
- Manifest schema validated
- Low-bank mapping verified (C3, CF samples)

### Remaining Work
- **Bank C3**: Solidify 30% → 35% coverage, expand dual superclusters
- **Bank C2**: Expand score-14 region, cross-bank hub completion
- **Bank C4**: Push toward 15% coverage, expand 772E supercluster
- **Bank C1**: Process remaining 16% candidate pool (434A mega-cluster focus)
- **Banks D2-D9**: Deep scan the most promising (D4, D6 prioritized)
- **Bank D1**: Continue expansion (90+ score-5+ islands waiting)
- **Bank C5**: Continue 9000-A000 and D000-E000 rich regions
- **Bank CF**: Continue below D000 (C000-D000 pending)
- **Banks DA-FF**: Final upper ROM exploration

See detailed reports:
- `AGENT_SWARM_SESSION_31_SUMMARY.md` - Latest C0, C2, C3, C4 achievements
- `AGENT_SWARM_SESSION_30_SUMMARY.md` - C0 audio system mapping
- `AGENT_SWARM_SESSION_29_SUMMARY.md` - C0 HDMA system completion
- `AGENT_SWARM_SESSION_27-28_SUMMARY.md` - C3 28% target achieved
- `C1_8C3E_DISPATCH_COMPLETION_REPORT.md`
- `C3_GAP_ANALYSIS_FINAL_REPORT.md`

## Start here next session
- read the Session 31 summary: `AGENT_SWARM_SESSION_31_SUMMARY.md`
- read the repo authority map: `docs/handoffs/chrono_trigger_repo_authority_map_2026-03-30.md`
- stay on `live-work-from-pass166`
- options for next work:
  1. **Bank C3**: Solidify 30% → 35% coverage (dual superclusters expansion)
  2. **Bank C2**: Expand score-14 region (8F6D, 8C08, 8DA3)
  3. **Bank C4**: Push toward 15% coverage (772E supercluster)
  4. **Bank C1**: Process remaining candidate pool (434A mega-cluster focus)
  5. **Banks D2-D9**: Deep scan the most promising (D4, D6 prioritized)
  6. **Bank CF**: Complete D000-E000 region
  7. **Bank C5**: Systematic deep scan
  8. **Bank D1**: Continue expansion
  9. **Banks DA-FF**: Final upper ROM exploration
- promotion standard: score >= 6 + internal evidence (RTS/PHP/JSR) + regional context
- run `python tools/scripts/score_target_owner_backtrack_v1.py` for candidate identification
- run `tools/generate_coverage_report_v2.py` for coverage statistics
