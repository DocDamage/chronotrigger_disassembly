# Bank CF:A000-FFFF Analysis Summary

## Task Completed
Analysis of Bank CF:A000-FFFF (24KB continuous high-density code region) completed successfully.

## Files Created

### Report
- `CF_A000_FFFF_ANALYSIS_REPORT.md` - Detailed analysis with 17 new manifest recommendations

### New Manifests (17 files)
| Pass | Range | Score | Description |
|------|-------|-------|-------------|
| 724 | CF:D3B0..CF:D3EA | 8 | Score-8 handler, D300 region |
| 725 | CF:DB00..CF:DB2A | 8 | Score-8 handler, DB00 region |
| 726 | CF:F606..CF:F635 | 8 | Score-8 handler, F600 region |
| 727 | CF:F010..CF:F037 | 6 | JSR prologue handler |
| 728 | CF:F18A..CF:F1A3 | 6 | PHP prologue handler |
| 729 | CF:FD99..CF:FDB6 | 6 | LDA# prologue, 4 callers |
| 730 | CF:C396..CF:C3C6 | 7 | Score-7 cluster, 9 branches |
| 731 | CF:CD30..CF:CD6A | 7 | Score-7 cluster, 5 returns |
| 732 | CF:D5A7..CF:D5D6 | 7 | Score-7 cluster, 4 children |
| 733 | CF:F3DC..CF:F3FD | 7 | Score-7 cluster, F300 region |
| 734 | CF:F5A1..CF:F5B9 | 7 | Score-7 handler, PHY op |
| 735 | CF:F700..CF:F724 | 7 | Score-7 cluster, 5 branches |
| 736 | CF:F7B5..CF:F7CD | 7 | Score-7 handler, PHY op |
| 737 | CF:F99C..CF:F9B4 | 7 | Score-7 handler, PHA op |
| 738 | CF:E91E..CF:F026 | 6 | JSR prologue handler |
| 739 | CF:EAC3..CF:EADD | 6 | JSR prologue handler |
| 740 | CF:ED0A..CF:ED30 | 6 | LDX# prologue handler |

## Key Findings

### Score-6+ Candidates Found: 27
- 12 with JSR/PHP/JSL prologues (strong function entry signals)
- 15 with LDA#/LDX#/LDY#/REP prologues
- 3 new score-8 clusters identified
- 8 score-7 clusters identified

### Existing Documentation (Preserved)
- CF:A16E..CF:A1A7 (pass711, score-9) ✓
- CF:D284..CF:D2BE (pass712, score-8) ✓
- CF:D41E..CF:D47A (pass710, score-10) ✓

### Coverage Improvement
| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Documented ranges | 3 | 20 | +17 |
| Coverage | 0.32% | ~2.1% | +1.78% |

### Cross-Bank References (20+)
Bank CF functions are called from:
- C1 bank (7 references) - System functions
- C4 bank (1 reference) - Graphics
- C7 bank (1 reference) - Audio
- C8/C9/CA banks (4 references) - Game logic
- CF internal (100+ references)

This indicates Bank CF contains important shared utility functions used across the game.

### Page Family Distribution (96 pages)
- text_ascii_heavy: 68 pages (71%) - Code-heavy
- mixed_command_data: 20 pages (21%) - Mixed code/data
- candidate_code_lane: 4 pages (4%) - High-confidence code
- branch_fed_control_pocket: 3 pages (3%) - Control flow
- dead_zero_field: 1 page (1%) - Data region (E000)

### Regions of Interest
| Region | Status | Key Findings |
|--------|--------|--------------|
| A000-AFFF | Partial | A16E-A1A7 documented, more candidates |
| B000-BFFF | New | 4 score-5 clusters, 3 score-4 candidates |
| C000-CFFF | New | C396 score-7 cluster, C0B0 score-6 candidate |
| D000-DFFF | Partial | D284-D2BE, D41E-D47A documented, D3B0, DB00 new |
| E000-EFFF | New | E000-E0FF is data, E700-EFFF code-heavy |
| F000-FFFF | New | F606 score-8, 6 score-7 clusters, 8 score-6+ candidates |

## Recommendations

### Phase 1 (Completed)
✅ Documented 17 high-value ranges (score-6+)

### Phase 2 (Next Steps)
- Scan remaining score-4/5 candidates for promotion
- Focus on F000-FFFF region (highest density)
- Investigate cross-bank caller targets

### Phase 3 (Future)
- Full disassembly of documented regions
- Trace function call graphs
- Identify data tables vs code

## Tools Used
- `run_seam_block_v1.py` - 96-page seam block scanning
- `score_target_owner_backtrack_v1.py` - Entry point backtracking
- `find_local_code_islands_v2.py` - Code island detection

## Analysis Date
2026-04-08
