# Bank C3 Mapping Progress Report

**Date:** 2026-04-08  
**Bank:** C3 (Game Logic Bank)  
**Current Coverage:** 19.65% (54 documented ranges)  
**Target Coverage:** 28%  
**Score-12 Location:** C3:2EA7 (HIGHEST IN C3!)

---

## Executive Summary

Bank C3 (the game logic bank) continues to show strong disassembly potential with **169 score-6+ backtrack candidates** and **30+ score-6+ code clusters** identified. The analysis reveals significant untapped function boundaries, particularly in the 3700-5200 region and the high-value score-12 cluster at C3:2EA7.

### Key Findings
- **169 score-6+ candidates** from owner backtrack analysis (all score-6)
- **30+ score-6+ clusters** from local island analysis
- **Highest cluster score: 13** at C3:4548..C3:459F
- **Score-12 cluster** at C3:2EA7..C3:2EBF (25 bytes, 4 calls, 12 returns)
- **46 existing candidate files** in `labels/c3_candidates/`

---

## Top Score-6+ Clusters (Prioritized)

| Rank | Range | Score | Width | Calls | Returns | Notes |
|------|-------|-------|-------|-------|---------|-------|
| 1 | C3:4548..C3:459F | 13 | 88 | 0 | 25 | **Highest score in C3** - Complex control flow |
| 2 | C3:2EA7..C3:2EBF | 12 | 25 | 4 | 12 | **HIGHEST IN C3** - ASCII-heavy, 4 calls |
| 3 | C3:4A2A..C3:4A53 | 11 | 42 | 5 | 8 | 5 callers, text-ASCII heavy |
| 4 | C3:19DB..C3:1A05 | 9 | 43 | 4 | - | High function density |
| 5 | C3:B979..C3:B9AC | 9 | 52 | 1 | - | Large function block |
| 6 | C3:87BA..C3:87E1 | 8 | 40 | 6 | - | 6 calls, high activity |
| 7 | C3:42C2..C3:42D4 | 8 | 19 | 1 | - | Compact function |
| 8 | C3:2B3A..C3:2B6E | 8 | 53 | 1 | - | 53 bytes, score-8 |
| 9 | C3:3779..C3:37A2 | 8 | 42 | 2 | - | Mid-bank function |

---

## Score-6+ Backtrack Candidates (Sample)

| Start | Target | Score | Distance | Start Byte | Range |
|-------|--------|-------|----------|------------|-------|
| C3:3705 | C3:3715 | 6 | 16 | 0B | C3:3705..C3:372D |
| C3:387B | C3:388B | 6 | 16 | 20 | C3:387B..C3:38A3 |
| C3:4010 | C3:4019 | 6 | 9 | A2 | C3:4010..C3:4031 |
| C3:4021 | C3:4028 | 6 | 7 | 22 | C3:4021..C3:4040 |
| C3:4B22 | C3:4B30 | 6 | 14 | C2 | C3:4B22..C3:4B48 |
| C3:4C43 | C3:4C50 | 6 | 13 | 08 | C3:4C43..C3:4C68 |
| C3:A3E2 | C3:A3EE | 6 | 12 | 20 | C3:A3E2..C3:A406 |
| C3:A3F1 | C3:A401 | 6 | 16 | 20 | C3:A3F1..C3:A419 |
| C3:AF42 | C3:AF48 | 6 | 6 | A0 | C3:AF42..C3:AF60 |

**Total: 169 score-6+ candidates awaiting triage**

---

## Major Gap Analysis

### Gap 1: C3:0000-01E3 (484 bytes)
- **Status:** branch_fed_control_pocket
- **Review Posture:** bad_start_or_dead_lane_reject
- **Clusters Found:** 
  - C3:01B3..C3:01C5 (score 5, 19 bytes)
  - C3:01D3..C3:01E3 (score 3, 17 bytes)
- **Score-6 Candidates:** Yes (at C3:01BA, C3:01A8, C3:01B4)
- **Recommendation:** Needs boundary review - 6 score-6+ candidates detected

### Gap 2: C3:0529-08A0 (879 bytes)
- **Status:** branch_fed_control_pocket
- **Review Posture:** bad_start_or_dead_lane_reject  
- **Clusters Found:**
  - C3:0594..C3:059B (score 5, 8 bytes)
- **Score-6 Candidates:** Yes (at C3:058A, C3:0540, C3:052A)
- **Recommendation:** Manual owner boundary review needed

### Gap 3: C3:2900-3058 (344 bytes)
- **Status:** branch_fed_control_pocket / text_ascii_heavy
- **Review Posture:** bad_start_or_dead_lane_reject / local_control_only
- **Key Cluster:** C3:2EA7..C3:2EBF (**score 12** - HIGHEST IN C3!)
- **Additional Clusters:**
  - C3:2B3A..C3:2B6E (score 8, 53 bytes)
  - C3:2AA5..C3:2ACC (score 7, 40 bytes)
  - C3:2CF8..C3:2D09 (score 7, 18 bytes)
  - C3:30B6..C3:30BE (score 6, 9 bytes)
- **Score-6 Candidates:** Yes (at C3:2E31, C3:307D, C3:3092, C3:3059, C3:306D)
- **Recommendation:** **HIGH PRIORITY** - Contains score-12 cluster, multiple score-6+ functions

---

## Page Family Distribution (Bank-wide)

| Page Range | Family | Posture | Priority |
|------------|--------|---------|----------|
| C3:0000-0FFF | branch_fed_control_pocket / mixed_command_data | Mostly reject | Low |
| C3:2000-2FFF | candidate_code_lane / branch_fed | Mixed | **High** (score-12 at 2EA7) |
| C3:3700-4300 | candidate_code_lane | Mixed | **High** (18 score-6+ candidates) |
| C3:4500-5200 | candidate_code_lane / mixed | Mixed | **High** (score-13 cluster) |
| C3:6000-6FFF | candidate_code_lane | Mixed | Medium |
| C3:8000-8FFF | candidate_code_lane / mixed | Mixed | Medium |
| C3:A000-AFFF | branch_fed_control_pocket | Mixed | Medium |
| C3:C000-CFFF | branch_fed_control_pocket | local_control | Medium |

---

## Recommended New Functions (18-22 targets)

Based on cluster scores and candidate density, recommended new function entries:

### Tier 1: Immediate (Score 8+)
1. **C3:4548** - Score 13 cluster (88 bytes, 25 returns)
2. **C3:2EA7** - Score 12 cluster (25 bytes, 4 calls)
3. **C3:4A2A** - Score 11 cluster (42 bytes, 5 calls)
4. **C3:19DB** - Score 9 cluster (43 bytes)
5. **C3:B979** - Score 9 cluster (52 bytes)
6. **C3:87BA** - Score 8 cluster (40 bytes, 6 calls)
7. **C3:42C2** - Score 8 cluster (19 bytes)
8. **C3:2B3A** - Score 8 cluster (53 bytes)
9. **C3:3779** - Score 8 cluster (42 bytes)

### Tier 2: High Value (Score 6-7)
10. C3:3705 - Score-6 backtrack candidate (high density)
11. C3:387B - Score-6 backtrack candidate
12. C3:4010 - Score-6 backtrack candidate
13. C3:4B22 - Score-6 backtrack candidate
14. C3:4C43 - Score-6 backtrack candidate
15. C3:A3E2 - Score-6 backtrack candidate
16. C3:A3F1 - Score-6 backtrack candidate
17. C3:AF42 - Score-6 backtrack candidate
18. C3:30B6 - Score 6 cluster (9 bytes)
19. C3:2AA5 - Score 7 cluster (40 bytes)
20. C3:ADB9 - Score 7 cluster (21 bytes)
21. C3:C2BA - Score 7 cluster (57 bytes)
22. C3:DFA6 - Score 7 cluster (36 bytes)

---

## Coverage Projection

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Documented Ranges | 54 | ~75 | +21 |
| Coverage | 19.65% | 28% | +8.35% |
| New Functions | 46 candidates | 64-68 | +18-22 |

**Estimated new coverage from 18-22 functions:** +2,000-2,800 bytes  
**Projected coverage increase:** 3-5%  
**Combined with boundary extensions:** Can reach 28% target

---

## Next Steps

1. **Immediate:** Create manifests for C3:2EA7 (score-12) and C3:4548 (score-13)
2. **Gap Filling:** Process C3:2900-3100 region (highest density of score-6+ clusters)
3. **Backtrack Triage:** Process remaining 169 score-6+ backtrack candidates
4. **Boundary Review:** Manual review of C3:3700-4300 region (18+ candidates)

---

## Tools Used

- `run_c3_candidate_flow_v7.py` - Comprehensive seam triage
- `score_target_owner_backtrack_v1.py` - Score-6+ candidate identification
- `find_local_code_islands_v2.py` - Cluster analysis
- `run_seam_block_v1.py` - Page family classification

---

*Report generated: 2026-04-08*  
*Bank C3: Game Logic Bank - Highest Coverage Potential*
