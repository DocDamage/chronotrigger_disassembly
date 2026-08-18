# Bank D1 Mapping Expansion Report

**Date:** 2026-04-08  
**Session:** Bank D1 Comprehensive Analysis  
**ROM:** Chrono Trigger (USA).sfc

## Executive Summary

This report documents the expansion of Bank D1 mapping through systematic analysis of high-density regions. **19 new function ranges** with score-6+ confidence have been identified, along with **4 cross-bank caller targets** and **90+ score-5+ islands** awaiting documentation.

---

## 1. Score-6+ Candidates Found

### Previously Documented (5 ranges)
| Range | Score | Width | Notes |
|-------|-------|-------|-------|
| D1:0509-053C | 7 | 52 bytes | Near C4 caller |
| D1:0E59-0E7B | 7 | 35 bytes | - |
| D1:3A8F-3AE2 | 7 | 84 bytes | 8 branches |
| D1:F8F1-F971 | 7 | 129 bytes | - |
| D1:FA67-FAE7 | 6 | 129 bytes | - |

### Newly Identified Score-6+ Clusters (19 ranges)

#### Region D1:F000-FFFF (High-Density Upper Bank)
| Range | Cluster Score | Width | Calls | Branches | Returns |
|-------|--------------|-------|-------|----------|---------|
| D1:F661..D1:F69B | 8 | 59 bytes | 1 | 5 | 3 |
| D1:F43A..D1:F452 | 6 | 25 bytes | 2 | 4 | 1 |
| D1:FBF3..D1:FC0B | 6 | 25 bytes | 1 | 2 | 1 |
| D1:FC1F..D1:FC37 | 6 | 25 bytes | 1 | 2 | 1 |
| D1:FC51..D1:FC69 | 6 | 25 bytes | 1 | 2 | 1 |
| D1:FC7D..D1:FC95 | 6 | 25 bytes | 1 | 2 | 1 |
| D1:FCAF..D1:FCC7 | 6 | 25 bytes | 1 | 2 | 1 |
| D1:FD23..D1:FD3B | 6 | 25 bytes | 1 | 2 | 1 |
| D1:F2E2..D1:F2F4 | 6 | 19 bytes | 1 | 2 | 1 |
| D1:FE3A..D1:FE4B | 6 | 18 bytes | 1 | 2 | 1 |
| D1:FCE5..D1:FCF3 | 6 | 15 bytes | 1 | 2 | 1 |

#### Region D1:0000-1000 (Near C4 Callers)
| Range | Cluster Score | Width | Calls | Branches | Returns |
|-------|--------------|-------|-------|----------|---------|
| D1:0D28..D1:0D42 | 12 | 27 bytes | 1 | 1 | 8 |
| D1:0E59..D1:0E86 | 9 | 46 bytes | 4 | 1 | 5 |
| D1:0350..D1:0374 | 8 | 37 bytes | 1 | 8 | 4 |
| D1:050D..D1:0527 | 8 | 27 bytes | 1 | 5 | 2 |
| D1:0A14..D1:0A28 | 8 | 21 bytes | 1 | 2 | 3 |

#### Region D1:B000-F000
| Range | Cluster Score | Width | Calls | Branches | Returns |
|-------|--------------|-------|-------|----------|---------|
| D1:E721..D1:E763 | 8 | 67 bytes | 4 | 0 | 7 |
| D1:E90F..D1:E930 | 8 | 34 bytes | 7 | 2 | 5 |
| D1:B04C..D1:B064 | 7 | 25 bytes | 1 | 3 | 1 |
| D1:EBE7..D1:EBFE | 7 | 24 bytes | 3 | 1 | 1 |

---

## 2. Cross-Bank Caller Verification

### Confirmed Cross-Bank Callers to D1

| Target | Caller | Type | Status |
|--------|--------|------|--------|
| D1:0002 | C4:206D | JSL | Valid |
| D1:0002 | C4:6751 | JSL | Valid |
| D1:0236 | C4:C0C0 | JSL | **Verified** |
| D1:04BF | C4:C0C0 | JSL | **Verified** |
| D1:35E1 | C4:C0C0 | JSL | **Verified** |
| D1:0058 | E7:A408 | JML | Valid |
| D1:001D | E1:DA1C | JSL | Valid |
| D1:00D7 | E1:4543 | JSL | Valid |

**Note:** C4:C0C0 is a known cross-bank dispatcher that calls multiple D1 targets.

---

## 3. Recommended New Manifests

### Priority 1: Score-7+ Clusters (Immediate Documentation)
```
D1:0D28..D1:0D42  (cluster_score: 12, 8 returns)
D1:0E59..D1:0E86  (cluster_score: 9, 4 calls)
D1:E721..D1:E763  (cluster_score: 8, 67 bytes)
D1:E90F..D1:E930  (cluster_score: 8, 7 calls)
D1:F661..D1:F69B  (cluster_score: 8, 59 bytes)
D1:0350..D1:0374  (cluster_score: 8, 8 branches)
D1:050D..D1:0527  (cluster_score: 8, 5 branches)
D1:0A14..D1:0A28  (cluster_score: 8, 3 returns)
```

### Priority 2: Score-6 Clusters (Documentation Ready)
```
D1:F43A..D1:F452
D1:FBF3..D1:FC0B
D1:FC1F..D1:FC37
D1:FC51..D1:FC69
D1:FC7D..D1:FC95
D1:FCAF..D1:FCC7
D1:FD23..D1:FD3B
D1:B04C..D1:B064
D1:EBE7..D1:EBFE
```

### Priority 3: Score-5 Islands (Candidate Review)
Over 90 score-5+ islands identified across all regions awaiting review.

---

## 4. D1 Coverage Improvement

### Analysis Summary by Region

| Region | Islands | Clusters | Score-6+ | Status |
|--------|---------|----------|----------|--------|
| D1:0000-1000 | 93 | 57 | 5 clusters | High-density code |
| D1:1000-4000 | 188 | 104 | Multiple | Code-heavy |
| D1:8000-B000 | 57 | 55 | 1 cluster | Moderate density |
| D1:B000-F000 | 106 | 74 | 3 clusters | High-density |
| D1:F000-FFFF | 61 | 45 | 11 clusters | Already partially mapped |

### Key Discoveries

1. **D1:0D28-0D42** - Exceptional cluster with 8 returns (cluster_score: 12)
2. **D1:0E59-0E86** - Extended cluster with 4 cross-references
3. **D1:E721-E763** - 67-byte cluster with 4 calls and 7 returns
4. **D1:E90F-E930** - Hot area with 7 calls, indicating heavy usage

### Cross-Bank Connectivity
- **C4 bank** has JSL/JML calls to D1:0002, D1:0236, D1:04BF, D1:35E1
- **E1 bank** has JSL calls to D1:001D, D1:00D7
- **E7 bank** has JML to D1:0058

---

## 5. High-Value Backtrack Candidates

Based on backtrack analysis, these entry points show strong function prologue signatures:

| Candidate | Target | Score | Start Byte | Class |
|-----------|--------|-------|------------|-------|
| D1:01D4 | D1:01D8 | 6 | 08 (PHP) | clean_start |
| D1:0394 | D1:0395 | 6 | 08 (PHP) | clean_start |
| D1:0683 | D1:0688 | 6 | 08 (PHP) | clean_start |
| D1:0809 | D1:080D | 6 | 20 (JSR) | clean_start |
| D1:093D | D1:0949 | 6 | 20 (JSR) | clean_start |
| D1:F077 | D1:F07E | 6 | 20 (JSR) | clean_start |
| D1:F0F9 | D1:F108 | 6 | 20 (JSR) | clean_start |
| D1:F551 | D1:F559 | 6 | C2 (REP) | clean_start |

---

## 6. Next Steps

1. **Create manifests** for Priority 1 (score-7+) clusters
2. **Verify boundaries** of high-confidence clusters with manual inspection
3. **Document cross-bank callers** with full call graph
4. **Analyze** D1:1000-4000 region more deeply (188 islands found)
5. **Resolve** overlapping candidate ranges through boundary analysis

---

## Appendix: Methodology

Tools used:
- `find_local_code_islands_v2.py` - Return-anchored code island detection
- `score_target_owner_backtrack_v1.py` - Entry point scoring
- `scan_range_entry_callers_v2.py` - Cross-reference analysis
- `validate_cross_bank_callers_v1.py` - Caller verification

Scoring criteria:
- Returns: +3 points
- Calls: +2 points
- Branches: +1 point
- Stack operations: +1 point
- Barriers (STP, etc.): -2 points each
- ASCII ratio > 30%: -2 points
- Data misread patterns: -2 points each
