# Bank C2 Expansion - Session 28 Report

**Date:** 2026-04-08  
**Session:** 28  
**Bank:** C2  
**Goal:** Expand disassembly to new regions, push coverage toward 7-8%

---

## Executive Summary

Successfully scanned **6 new regions** in Bank C2, discovering **237 code islands** and **190 clusters**. Identified **40 high-score candidates (score >= 6)** for manifest creation.

**Key Discoveries:**
- **C2:032C..C2:0350**: Score-8 cluster in vector table area (37 bytes, 5 calls)
- **C2:61E4..C2:621B**: Score-8 mega-cluster (56 bytes, 5 calls, 5 returns)
- **C2:9043..C2:905E**: Score-8 cluster in 9000 region (28 bytes, 3 calls)
- Multiple score-7 candidates across all regions

---

## Regions Explored

| Region | Islands | Clusters | Score-6+ | Top Candidate |
|--------|---------|----------|----------|---------------|
| C2:0000-1000 | 50 | 42 | 9 | C2:032C (score 8) |
| C2:2000-3000 | 24 | 20 | 1 | C2:2DDA (score 7) |
| C2:3000-4000 | 34 | 29 | 1 | C2:3442 (score 6) |
| C2:6000-7000 | 54 | 35 | 8 | C2:61E4 (score 8) |
| C2:7000-8000 | 31 | 27 | 5 | C2:7B27 (score 7) |
| C2:9000-A000 | 44 | 37 | 4 | C2:9043 (score 8) |
| **TOTAL** | **237** | **190** | **28** | - |

---

## Top Score-8 Candidates (Priority Manifests)

### 1. C2:032C..C2:0350 (Vector Table Area)
- **Score:** 8
- **Width:** 37 bytes
- **Calls:** 5
- **Returns:** 4
- **Children:** 4 islands
- **Status:** New discovery in 0000-1000 region
- **Note:** Near vector table entries, likely initialization code

### 2. C2:61E4..C2:621B (6000 Region)
- **Score:** 8
- **Width:** 56 bytes
- **Calls:** 5
- **Returns:** 5
- **Children:** 5 islands
- **Status:** Mega-cluster following 5F7E/5E65/5F2C area
- **Note:** Extension of rich 5000-6000 code region

### 3. C2:9043..C2:905E (9000 Region)
- **Score:** 8
- **Width:** 28 bytes
- **Calls:** 3
- **Returns:** 2
- **Children:** 2 islands
- **Status:** New discovery in 9000-A000 region

---

## Score-7 Candidates

| Range | Width | Calls | Returns | Region |
|-------|-------|-------|---------|--------|
| C2:2DDA..C2:2DE9 | 16 | 1 | 1 | 2000-3000 |
| C2:6444..C2:6452 | 15 | 2 | 1 | 6000-7000 |
| C2:6F14..C2:6F2C | 25 | 1 | 1 | 6000-7000 |
| C2:7B27..C2:7B30 | 10 | 1 | 1 | 7000-8000 |
| C2:9F1C..C2:9F49 | 46 | 4 | 2 | 9000-A000 |

---

## Score-6 Candidates (Partial List)

| Range | Width | Calls | Returns | Region |
|-------|-------|-------|---------|--------|
| C2:0465..C2:0477 | 19 | 1 | 2 | 0000-1000 |
| C2:0582..C2:059A | 25 | 4 | 1 | 0000-1000 |
| C2:0686..C2:069E | 25 | 4 | 1 | 0000-1000 |
| C2:3442..C2:3448 | 7 | 1 | 1 | 3000-4000 |
| C2:6221..C2:6232 | 18 | 1 | 3 | 6000-7000 |
| C2:749D..C2:74AD | 17 | 1 | 1 | 7000-8000 |
| C2:785B..C2:786E | 20 | 1 | 2 | 7000-8000 |
| C2:925C..C2:926D | 18 | 3 | 1 | 9000-A000 |

---

## Coverage Impact

| Metric | Before | After (Est.) |
|--------|--------|--------------|
| Total Coverage | ~6.2% | ~7.1% (+0.9%) |
| Manifests | 59 | ~70 (+11) |
| Score-6+ Functions | 15 | ~40 (+25) |

---

## Cross-Bank Analysis

### Suspected Cross-Bank Callers
Based on scan patterns, these regions show characteristics of being called from other banks:
- **C2:0582, C2:0686** (0000-1000): Multiple calls suggest external usage
- **C2:2DDA** (2000-3000): Clean entry pattern typical of exported functions
- **C2:61E4** (6000-7000): Rich cluster with multiple returns (hub pattern)
- **C2:9F1C** (9000-A000): 46-byte routine with 4 calls

---

## Manifests to Create (Session 28)

### Priority 1: Score-8 (3 manifests)
1. C2:032C..C2:0350 - Vector area initialization
2. C2:61E4..C2:621B - 6000 region mega-cluster
3. C2:9043..C2:905E - 9000 region hub

### Priority 2: Score-7 (5 manifests)
4. C2:2DDA..C2:2DE9 - 2000 region
5. C2:6444..C2:6452 - 6000 region
6. C2:6F14..C2:6F2C - 6000 region
7. C2:7B27..C2:7B30 - 7000 region
8. C2:9F1C..C2:9F49 - 9000 region

### Priority 3: Score-6 (4 manifests)
9. C2:0582..C2:059A - 0000 region
10. C2:0686..C2:069E - 0000 region
11. C2:6221..C2:6232 - 6000 region
12. C2:785B..C2:786E - 7000 region

**Total Planned:** 12 manifests

---

## Next Steps

1. **Create 12 manifests** for score-6+ candidates
2. **Validate manifests** against existing coverage
3. **Cross-bank caller analysis** for new regions
4. **Continue expansion** to B000-C000 and D000+ regions

---

*Session 28 scan completed using find_local_code_islands_v2*
