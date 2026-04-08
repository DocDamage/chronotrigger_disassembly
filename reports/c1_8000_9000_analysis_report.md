# Bank C1:8000-9000 Analysis Report

## Executive Summary
- **Region**: C1:8000-9000 (16 pages, 4KB)
- **Bank C1 Coverage**: Previously 1.29%, this region significantly expands documented ranges
- **Primary Finding**: Dense code region with 16 score-6+ candidates and major hub connections

---

## Score-6+ Candidates Found

### Backtrack Score-6 Candidates (16 total)
| Address | Target | Score | Start Byte | Notes |
|---------|--------|-------|------------|-------|
| C1:8398 | C1:83A5 | 6 | 8B (PHB) | Near high-activity zone |
| C1:882D | C1:883D | 6 | 8B (PHB) | Adjacent to score-6 cluster |
| C1:8853 | C1:8862 | 6 | 20 (JSR) | Code lane candidate |
| C1:8940 | C1:894C | 6 | 20 (JSR) | Precedes 89AD hub caller |
| C1:8959 | C1:895B | 6 | 20 (JSR) | Dual candidate |
| C1:89A6 | C1:89AD | 6 | A9 (LDA#) | **Major hub caller** (13 refs) |
| C1:89A6 | C1:89AE | 6 | A9 (LDA#) | Shared candidate |
| C1:8BAC | C1:8BAD | 6 | 20 (JSR) | Before score-7 cluster |
| C1:8BAC | C1:8BB8 | 6 | 20 (JSR) | Dual candidate |
| C1:8C27 | C1:8C28 | 6 | 0B (PHD) | Precedes score-7 cluster |
| C1:8C30 | C1:8C3E | 6 | 20 (JSR) | **Major hub** target (42 refs) |
| C1:8C9D | C1:8CAD | 6 | C2 (REP) | Mode-setting prologue |
| C1:8C9E | C1:8CAE | 6 | 20 (JSR) | Dual candidate |
| C1:8CEF | C1:8CF8 | 6 | 08 (PHP) | Stack operation prologue |
| C1:8E9B | C1:8EA6 | 6 | 08 (PHP) | Near score-8 cluster |
| C1:8F02 | C1:8F10 | 6 | 20 (JSR) | Post-score-8 region |

### High-Score Local Clusters
| Range | Score | Width | Calls | Returns | Notes |
|-------|-------|-------|-------|---------|-------|
| **C1:8E95..C1:8EAA** | **8** | 22 | 1 | 2 | **Highest score** - no direct callers |
| **C1:8C2F..C1:8C3D** | **7** | 15 | 1 | 1 | Adjacent to 8C3E hub |
| C1:83DE..C1:83EE | 6 | 17 | 2 | 1 | Early region cluster |
| C1:8824..C1:883C | 6 | 25 | 4 | 1 | Code lane cluster |
| C1:8963..C1:8974 | 6 | 18 | 1 | 1 | Post-89AD region |
| C1:8D21..C1:8D35 | 6 | 21 | 1 | 1 | Between hub zones |

---

## Hub Connection Analysis

### C1:4AEB Hub Function
- **Type**: Major internal hub
- **Call Count**: 30 total (27 valid weak anchors)
- **Callers in C1:8000-9000 region**:
  - C1:851F, C1:8660, C1:86F4 (early region)
  - C1:88B1, C1:88D8 (mid region)
  - **C1:89AD** (major caller - 13 callers to it, then it calls hub)
  - C1:89F1, C1:8A3D, C1:8A89, C1:8AB2 (post-89AD)
  - C1:8B23, C1:8BF4 (late 8B region)
  - C1:8E2D (8E region)

### C1:8C3E Sub-Hub Function
- **Type**: Regional sub-hub within C1:8C00-9800
- **Call Count**: 42 (all weak anchors from unresolved callers)
- **Callers**: All in C1:8E00-9800 range
- **Pattern**: Each caller is 0x30-0x80 bytes apart (dispatch table-like)

### C1:89AD Regional Hub
- **Type**: Mid-tier hub
- **Call Count**: 13 callers
- **Notable**: Calls C1:4AEB hub internally
- **Distribution**: Callers spread across C1:83D1 to C1:F060

### C1:8E78 Jump Target
- **Type**: Multi-entry point
- **Call Count**: 5 JMP callers
- **Pattern**: All JMP from C1:8D3B-8DCF range (jump table)

---

## Page Classification Summary

| Page Family | Count | Description |
|-------------|-------|-------------|
| mixed_command_data | 13 | Primary code/data intermixing |
| branch_fed_control_pocket | 2 | Branch-heavy control flow |
| candidate_code_lane | 1 | Clean code lane (C1:8800) |

| Review Posture | Count |
|----------------|-------|
| manual_owner_boundary_review | 9 |
| bad_start_or_dead_lane_reject | 6 |
| mixed_lane_continue | 1 |

---

## Recommended New Manifests (12 Functions)

### Priority 1: Major Hubs
1. **C1:8C3E..C1:8C56** - Sub-hub with 42 callers
2. **C1:89AD..C1:89C6** - Regional hub (13 callers)
3. **C1:8E95..C1:8EAA** - Score-8 cluster (investigate internal callers)

### Priority 2: High-Activity Zones
4. **C1:8C2F..C1:8C3D** - Score-7 cluster (adjacent to 8C3E)
5. **C1:8824..C1:883C** - Score-6 cluster (4 calls, 1 ret)
6. **C1:8D21..C1:8D35** - Score-6 cluster

### Priority 3: Entry Points with Prologue
7. **C1:8398..C1:83BD** - PHB prologue (score-6)
8. **C1:882D..C1:8855** - PHB prologue near cluster
9. **C1:8C27..C1:8C40** - PHD prologue (precedes score-7)
10. **C1:8CEF..C1:8D10** - PHP prologue

### Priority 4: Supporting Functions
11. **C1:8E78..C1:8E90** - Multi-JMP target (5 entries)
12. **C1:8C9D..C1:8CC6** - REP prologue pair

---

## Regional Code Density Assessment

### Density Metrics
- **Total Pages**: 16 (C1:8000-9000)
- **Pages with Code Candidates**: 15/16 (94%)
- **Score-6+ Candidates**: 16
- **High-Score Clusters**: 6 (score >= 5)
- **Major Hub Functions**: 3 (C1:4AEB external, C1:8C3E, C1:89AD)

### Code Organization Pattern
```
C1:8000-8300: Mixed utility functions
C1:8300-8800: Control flow pockets with data
C1:8800-8C00: Candidate code lanes
C1:8C00-8E00: **Major hub zone** (8C3E, 8C2F)
C1:8E00-9000: **High-density code** (8E95 score-8 cluster)
C1:9000-9800: Sub-hub dispatchers (42 callers to 8C3E)
```

### Key Findings
1. **C1:8C3E is a major sub-hub** called by 42 different locations in 9000-9800
2. **C1:89AD connects to C1:4AEB hub** - serves as regional dispatcher
3. **C1:8E95 score-8 cluster** has no direct external callers - internal function
4. **Dispatch table pattern** observed at C1:8E78 (5 JMP entries)
5. **High prologue density** (PHB/PHD/PHP/REP) suggests well-formed functions

---

## Connection to C1:4AEB Hub

The C1:4AEB hub receives calls from **7 distinct locations** within the analyzed region:
- C1:89AD is the most significant (serves 13 callers before calling hub)
- Distribution shows the hub serves code across the entire 8000-9000 range

**Recommendation**: Document C1:89AD as a "preprocessor" function that prepares arguments before calling C1:4AEB.

---

*Generated: 2026-04-08*
*Analysis Tools: run_seam_block_v1.py, score_target_owner_backtrack_v1.py, build_call_anchor_report_v3.py*
