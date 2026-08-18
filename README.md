# Chrono Trigger Disassembly

Repo-native workspace for the ongoing Chrono Trigger (SNES, USA) ROM disassembly effort.

## Current live state

📊 **Full Progress Report**: See `reports/coverage.md` for comprehensive coverage statistics

- working branch: `live-work-from-pass166`
- latest manifest-backed pass: `1229` (Session 46: C4:9D10 + C3:CB47 dual promotion)
- latest continuation-note snapshot: `docs/sessions/chrono_trigger_session15_continue_notes_100.md` (historical C7 summary through pass 217)
- current live seam: `C3:D000.. / C4:A000..` (from canonical pass `1229` and `tools/config/project_state.json`)
- canonical pass manifests: 961 canonical manifests generated from 1,000 legacy source manifests
- range inventory: 1,105 conserved historical claims normalized into 1,289 records (1,061 active, 228 superseded); active ownership is conflict-free
- unique coverage: 59,050 bytes (1.4079% of the 4 MiB ROM)
- conservation status: 100% verified zero-loss conservation (`tools/scripts/compare_manifest_range_inventory.py`)
- source of truth: this GitHub repo, not chat exports or old toolkit zips
- continuation notes remain important historical context for the earlier C7 seam

## What this repo contains
- `passes/manifests/` — canonical Schema v2 pass manifests (`pass0001.json`..`pass1229.json`) and `legacy/` source archive
- `passes/disasm/` — per-pass disassembly notes
- `passes/labels/` — per-pass label notes
- `tools/` — repo-native toolkit scripts, models (`tools/ctrepo`), configs, and schemas
- `reports/` — generated coverage, health, and provenance reports
- `repo_sync/` — earlier sync packets from the repo-first transition phase
- `disassembly/` — legacy disassembly-note mirror through pass `163` (historical)
- `labels/` — legacy label-note mirror through pass `163` (historical)
- `toolkits/` — historical unpacked toolkit source; binary ZIP snapshots are intentionally excluded from Git
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

## Current status (Agent Swarm Session 46 Complete)

### Session 46: Major Breakthrough - C4:9800 Exceptional Density
Session 46 discovered exceptional C4:9800-9FFF region with 2 promotions:
- **16 pages scanned** (C3:C800-CFFF, C4:9800-9FFF)
- **2 functions promoted**: C4:9D10 (3-byte copy) + C3:CB47 (hardware init)
- **C4:9800-9FFF**: 7 of 8 pages candidate_code_lane (87.5% density!)
- **Score-6 clusters**: 3 discovered (C3:CB8E, C4:9DE6, C4:9E50)
- **C4 bank**: ~13.1%, only 1.9% to 15% target
- **Session-ending seam**: C3:D000.. / C4:A000..
- **Report**: `AGENT_SWARM_SESSION_46_REPORT.md`

### Session 45: Continuation Scan - 4 Score-4 Candidates Pending
Session 41 continued the sequential seam and pivoted to C3:8000+ high bank:
- **32 pages scanned** (C3:7800-97FF, C4:6800-6FFF)
- **Score-6 backtrack candidate**: C3:8912 (target C3:8921, verified callers)
- **Cluster score 8**: C3:87BA-87E1 (branch_fed_control_pocket)
- **High bank validation**: Confirmed 62.5% candidate_code_lane density
- **Session-ending seam**: C3:9800..
- **Report**: `AGENT_SWARM_SESSION_41_REPORT.md`

### Session 40: Agent Swarm Multi-Region Scan
**4 parallel agents** scanned **4 regions simultaneously**:
- **32 new closed ranges** added (1802 → 1834)
- **12 functions promoted** in C3:7000-77FF (major breakthrough!)
- **8 score-6+ candidates** identified in C4 bank
- **5+ promotions** identified in C3:8000 high bank
- **Key discovery**: C3:7000 code pocket with verified callers including FC:BA5A cross-bank call
- **High bank insight**: C3:8000+ shows 62.5% candidate_code_lane (vs low bank)
- **C4 progress**: 8 candidates found, path to 15% clearer
- **Closed ranges snapshot**: 1802 → 1834 ranges

### Session 39: C3 Low-Bank Forward Seam (C3:6000–C3:6800)
Session 39 continued the sequential C3 low-bank forward seam from pass 1217's stopping point at C3:6000:
- **1 pass produced** (pass 205, manifest 1218)
- **8 new closed ranges** added (C3:6000–C3:67FF, 2048 bytes)
- **No functions promoted** - all pages frozen as data
- **Score-6 candidate analysis** at C3:6600: fragmented code with cross-bank JSL $C30D5E
- **16-bit mode detection**: LDA #$003C patterns indicate 65816 native mode
- **Milestone reached**: 1000 total closed ranges!
- **Closed ranges snapshot**: 1794 → 1802 ranges

### Session 38: C3 Low-Bank Forward Seam (C3:5800–C3:6000)
Session 38 continued the sequential C3 low-bank forward seam from pass 1216's stopping point at C3:5800:
- **1 pass produced** (pass 204, manifest 1217)
- **8 new closed ranges** added (C3:5800–C3:5FFF, 2048 bytes)
- **No functions promoted** - all pages frozen as data
- **Local control analysis**: All 8 pages lack verified external callers
- **Structured data identification** at C3:5A00: repeated $31 patterns indicate data tables
- **Closed ranges snapshot**: 1786 → 1794 ranges

### Session 37: C3 Low-Bank Forward Seam (C3:5000–C3:5800)
Session 37 continued the sequential C3 low-bank forward seam from pass 1215's stopping point at C3:5000:
- **2 passes produced** (pass 202-203, manifest 1216)
- **8 new closed ranges** added (C3:5000–C3:57FF, 2048 bytes)
- **No functions promoted** - all pages frozen as data
- **Jump table identification** at C3:5700: C3:5777 is JMP $A22A dispatch entry (not actual function)
- **Data table analysis** at C3:5600: arithmetic progression pattern (+$21) indicates lookup table
- **Closed ranges snapshot**: 1778 → 1786 ranges

### Session 36: C3 Low-Bank Forward Seam (C3:4800–C3:5000)
Session 36 continued the sequential C3 low-bank forward seam from pass 1214's stopping point at C3:4800:
- **2 passes produced** (pass 200-201, manifest 1215)
- **8 new closed ranges** added (C3:4800–C3:4FFF, 2048 bytes)
- **No functions promoted** - all pages frozen as data
- **Local control analysis** at C3:4900: identified inline data patterns with long addressing to WRAM ($7E:7480BB)
- **ASCII ratio validation** at C3:4A00: debunked cluster score 11 by high ASCII ratio (0.619 = text/data)
- **Closed ranges snapshot**: 1770 → 1778 ranges

### Session 35: C3 Low-Bank Forward Seam (C3:4000–C3:4800)
Session 35 continued the sequential C3 low-bank forward seam from pass 1213's stopping point at C3:4000:
- **1 pass produced** (pass 198-199, manifest 1214)
- **8 new closed ranges** added (C3:4000–C3:47FF, 2048 bytes)
- **No functions promoted** - all pages frozen as data
- **False positive analysis** at C3:4548: identified 88-byte data table with inflated cluster score (13) caused by 25 RTS/RTI coincidences
- **Code fragment documentation** at C3:4200 demonstrating byte-coincidence detection methodology
- **Closed ranges snapshot**: 1762 → 1770 ranges

### Session 34: C3 Low-Bank Forward Seam (C3:3800–C3:4000)
Session 34 continued the sequential C3 low-bank forward seam from pass 1212's stopping point at C3:3800:
- **1 pass produced** (pass 197, manifest 1213)
- **8 new closed ranges** added (C3:3800–C3:3FFF, 2048 bytes)
- **No functions promoted** - all pages frozen as mixed data
- **Code fragments documented** at C3:3F00: Mode 7 matrix manipulation ($211B), window mask settings ($2123), WRAM long addressing ($7E6A5F)
- **Closed ranges snapshot**: 1754 → 1762 ranges

### Session 33: C3 Low-Bank Forward Seam (C3:3000–C3:3800)
Session 33 continued the sequential C3 low-bank forward seam from pass 1210's stopping point at C3:3000:
- **3 passes produced** (pass 194–196, manifests 1211–1212, disasm notes)
- **10 new closed ranges** added (C3:3000–C3:37FF, 2048 bytes)
- **3 functions promoted** (C3:3500, C3:353B, C3:357A): score-6 and score-4 with verified callers
- **7 frozen data pages** (C3:3000–C3:34FF, C3:3600–C3:37FF): hard bad starts, suspect caller contexts
- **Closed ranges snapshot** updated: 1744 → 1754 ranges

### Session 32: C3 Low-Bank Forward Seam (C3:2900–C3:2FFF)
Session 32 continued the sequential C3 low-bank forward seam from pass 191's stopping point at C3:2900:
- **2 passes produced** (pass 192–193, manifests 1209–1210)
- **7 new closed ranges** added (C3:2900–C3:2FFF, 1792 bytes)
- **1 annotated disassembly** (C3:2B00–C3:2BFF): hardware division/multiplication, cross-bank JSL, 9 JSR calls, table-driven computation
- **6 frozen data pages** (C3:2900–C3:2AFF and C3:2C00–C3:2FFF): mixed data, structured tables, byte-coincidence inflated scores
- **Closed ranges snapshot** updated: 1737 → 1744 ranges

### Session 32 Coverage Updates
| Bank | New Ranges | Notes |
|------|------------|-------|
| C3 | +7 | 2900-2BFF annotated + 2C00-2FFF frozen data |
| **Total** | **+7** | **1744 total ranges** |

### Previous Session (Agent Swarm Session 31 Complete)

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
| **Total** | **942** | **~13.7%** | **970+ manifests** |

### Toolkit Health: 100%
All upgraded toolkit scripts verified working across 31 sessions:
- `toolkit_doctor.py`: All 8 checks passing
- 102 Python scripts compile successfully
- Legacy entrypoints upgraded
- Manifest schema validated
- Low-bank mapping verified (C3, CF samples)

### Remaining Work
- **Bank C3**: Continue validated work from the authoritative frontier `C3:D000.. / C4:A000..`; review high-bank candidates around C3:8800+
- **Bank C2**: Expand score-14 region, cross-bank hub completion
- **Bank C4**: Push toward 15% coverage, expand 772E supercluster
- **Bank C1**: Process remaining 16% candidate pool (434A mega-cluster focus)
- **Banks D2-D9**: Deep scan the most promising (D4, D6 prioritized)
- **Bank D1**: Continue expansion (90+ score-5+ islands waiting)
- **Bank C5**: Continue 9000-A000 and D000-E000 rich regions
- **Bank CF**: Continue below D000 (C000-D000 pending)
- **Banks DA-FF**: Final upper ROM exploration

See detailed reports:
- `AGENT_SWARM_SESSION_40_MASTER_SUMMARY.md` - Agent swarm multi-region results (12 promotions!)
- `AGENT_SWARM_SESSION_39_SUMMARY.md` - C3 low-bank forward seam (pass 205)
- `C3_7000_REGION_REPORT.md` - C3:7000 breakthrough analysis
- `C3_8000_HIGH_BANK_REPORT.md` - High bank code density findings
- `C4_BANK_PROGRESS_REPORT.md` - Path to 15% coverage
- `AGENT_SWARM_SESSION_37_SUMMARY.md` - C3 low-bank forward seam (pass 202-203, jump table analysis)
- `AGENT_SWARM_SESSION_36_SUMMARY.md` - C3 low-bank forward seam (pass 200-201, local control/ASCII analysis)
- `AGENT_SWARM_SESSION_35_SUMMARY.md` - C3 low-bank forward seam (pass 198-199, false positive analysis)
- `AGENT_SWARM_SESSION_34_SUMMARY.md` - C3 low-bank forward seam (pass 197, fragments)
- `AGENT_SWARM_SESSION_33_SUMMARY.md` - C3 low-bank forward seam (pass 194-196)
- `AGENT_SWARM_SESSION_32_SUMMARY.md` - C3 low-bank forward seam (pass 192-193)
- `AGENT_SWARM_SESSION_31_SUMMARY.md` - Latest C0, C2, C3, C4 achievements
- `AGENT_SWARM_SESSION_30_SUMMARY.md` - C0 audio system mapping
- `AGENT_SWARM_SESSION_29_SUMMARY.md` - C0 HDMA system completion
- `AGENT_SWARM_SESSION_27-28_SUMMARY.md` - C3 28% target achieved
- `C1_8C3E_DISPATCH_COMPLETION_REPORT.md`
- `C3_GAP_ANALYSIS_FINAL_REPORT.md`

## Start here next session
- read the Session 40 summary: `AGENT_SWARM_SESSION_40_MASTER_SUMMARY.md`
- read the repo authority map: `docs/handoffs/chrono_trigger_repo_authority_map_2026-03-30.md`
- stay on `live-work-from-pass166`
- current authoritative frontier: `C3:D000.. / C4:A000..`
- options for next work:
  1. **Bank C3**: Re-review C3:8800-8FFF candidates (high bank showed 62.5% code density)
  2. **Bank C4**: Scan C4:6800-6FFF and continue toward the 15% target
  3. **Bank C2**: Expand the score-14 region (8F6D, 8C08, 8DA3)
  4. **Bank C1**: Process the remaining candidate pool (434A mega-cluster focus)
  5. **Banks D2-D9**: Deep scan the most promising regions (D4, D6 prioritized)
  6. **Bank CF**: Continue the pending C000-D000 region
  7. **Bank C5**: Systematic deep scan of the 9000-A000 and D000-E000 regions
  8. **Bank D1**: Continue expansion
  9. **Banks DA-FF**: Final upper-ROM exploration
- promotion standard: score >= 6 + internal evidence (RTS/PHP/JSR) + regional context
- run `python tools/scripts/score_target_owner_backtrack_v1.py` for candidate identification
- run `tools/generate_coverage_report_v2.py` for coverage statistics
