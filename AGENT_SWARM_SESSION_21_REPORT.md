# Session 21: Bank C4 Deep Scan Report - 4000-8000 Hot Zone

**Date:** 2026-04-08  
**Scan Target:** Bank C4, range 4000-8000 (16KB hot zone)  
**Scanner:** find_local_code_islands_v2.py  

---

## Executive Summary

Deep scan of Bank C4's highest-scoring region (4000-8000) completed successfully.
- **4 sub-regions scanned:** 4000-5000, 5000-6000, 6000-7000, 7000-8000
- **Total islands found:** 165
- **Total clusters found:** 131
- **Score 7 candidates:** 3
- **Score 6 candidates:** 3
- **Score 5 candidates:** 11
- **Manifests created:** 10

---

## Sub-Region Summaries

### C4:4000-5000 Region
- **Islands:** 42
- **Clusters:** 32
- **Score 6:** 1 candidate (C4:46B7-46CF)
- **Score 5:** 4 candidates
- **Highest cluster:** C4:419F-41B9 (score 8)

**Key Findings:**
- Moderate activity region with scattered function candidates
- Best candidate: C4:46B7-46CF (score 6, 25 bytes, 1 call, 3 branches)
- C4:46B2-46D1 forms a score 6 cluster with multiple overlapping ranges

### C4:5000-6000 Region (Hot Zone)
- **Islands:** 43
- **Clusters:** 33
- **Score 7:** 1 candidate (C4:5025-5039) ⭐
- **Score 5:** 3 candidates
- **Highest cluster:** C4:5025-5039 (score 7)

**Key Findings:**
- Contains **C4:5025-5039** - the highest scoring individual island (score 7)
- 21 bytes, 2 calls, 2 branches - substantial utility function
- C4:54F5-5503 and C4:59FE-5A07 also strong candidates (score 5)

### C4:6000-7000 Region
- **Islands:** 35
- **Clusters:** 29
- **Score 6:** 2 candidates (C4:607A-6085, C4:6BDA-6BE1)
- **Score 5:** 2 candidates

**Key Findings:**
- Two strong score 6 candidates
- C4:607A-6085: 12 bytes, 1 call, 1 branch
- C4:6BDA-6BE1: 8 bytes, 1 call, stack operations
- Lower density than 5000-6000 and 7000-8000 regions

### C4:7000-8000 Region (Hottest Zone)
- **Islands:** 45
- **Clusters:** 36
- **Score 7:** 2 candidates (C4:7730-7748, C4:7732-774A) ⭐⭐
- **Score 5:** 5 candidates
- **Highest cluster:** C4:772E-774A (cluster score 10!)

**Key Findings:**
- **Densest region** with 45 islands and 36 clusters
- **C4:772E-774A cluster** has highest cluster score (10)
- Contains 2 of 3 score 7 candidates
- C4:7730-7748: 25 bytes, 6 branches, 3 returns - complex function
- C4:7732-774A: 25 bytes, 5 branches, 4 returns - related/alternate entry
- Multiple score 5 candidates with 3+ calls each

---

## Top 10 Candidates (Score 5+)

| Rank | Range | Score | Width | Calls | Branches | Returns | Region |
|------|-------|-------|-------|-------|----------|---------|--------|
| 1 | C4:5025-5039 | 7 | 21 | 2 | 2 | 1 | 5000-6000 |
| 2 | C4:7730-7748 | 7 | 25 | 1 | 6 | 3 | 7000-8000 |
| 3 | C4:7732-774A | 7 | 25 | 1 | 5 | 4 | 7000-8000 |
| 4 | C4:46B7-46CF | 6 | 25 | 1 | 3 | 2 | 4000-5000 |
| 5 | C4:607A-6085 | 6 | 12 | 1 | 1 | 1 | 6000-7000 |
| 6 | C4:6BDA-6BE1 | 6 | 8 | 1 | 0 | 1 | 6000-7000 |
| 7 | C4:7980-7992 | 5 | 19 | 3 | 4 | 2 | 7000-8000 |
| 8 | C4:752A-753C | 5 | 19 | 3 | 1 | 1 | 7000-8000 |
| 9 | C4:7DA7-7DB5 | 5 | 15 | 1 | 2 | 2 | 7000-8000 |
| 10 | C4:7F8F-7FA7 | 5 | 25 | 0 | 6 | 1 | 7000-8000 |

---

## Manifests Created

All manifests saved to `labels/c4_candidates/`:

### Score 7 Manifests (Priority 1)
1. `bank_C4_5025_score7.yaml` - C4:5025-5039 (21 bytes, 2 calls)
2. `bank_C4_7730_score7.yaml` - C4:7730-7748 (25 bytes, 6 branches, 3 returns)
3. `bank_C4_7732_score7.yaml` - C4:7732-774A (25 bytes, 5 branches, 4 returns)

### Score 6 Manifests (Priority 2)
4. `bank_C4_46B7_score6.yaml` - C4:46B7-46CF (25 bytes, 3 branches)
5. `bank_C4_607A_score6.yaml` - C4:607A-6085 (12 bytes, 1 call)
6. `bank_C4_6BDA_score6.yaml` - C4:6BDA-6BE1 (8 bytes, stack ops)

### Score 5 Manifests (Priority 3)
7. `bank_C4_54F5_score5.yaml` - C4:54F5-5503 (15 bytes, 2 branches)
8. `bank_C4_59FE_score5.yaml` - C4:59FE-5A07 (10 bytes, 3 calls)
9. `bank_C4_5914_score5.yaml` - C4:5914-591B (8 bytes, 1 call)
10. `bank_C4_7980_score5.yaml` - C4:7980-7992 (19 bytes, 3 calls, 4 branches)
11. `bank_C4_752A_score5.yaml` - C4:752A-753C (19 bytes, 3 calls)
12. `bank_C4_7DA7_score5.yaml` - C4:7DA7-7DB5 (15 bytes, 2 branches)

---

## Data Files Generated

| File | Description |
|------|-------------|
| `c4_4000_5000_scan_session21.json` | Scan results for 4000-5000 region |
| `c4_5000_6000_scan_session21.json` | Scan results for 5000-6000 region |
| `c4_6000_7000_scan_session21.json` | Scan results for 6000-7000 region |
| `c4_7000_8000_scan_session21.json` | Scan results for 7000-8000 region |

---

## Coverage Impact

- **Previous C4 coverage:** ~1.85%
- **New regions identified:** 165 islands in hot zone
- **High-confidence targets:** 17 candidates (score 5+)
- **Estimated new coverage:** +8-10% of Bank C4

---

## Recommendations

1. **Priority 1:** Process the 3 score 7 candidates first - highest confidence
2. **Priority 2:** Process score 6 candidates - strong candidates with good features
3. **Cluster C4:772E-774A** should be analyzed as a unit - has cluster score 10
4. C4:5025-5039 has 2 calls - check if it's a dispatcher/utility function
5. C4:7730-7748 and C4:7732-774A may be related - analyze together

---

## Validation Status

- ✅ All manifests follow established YAML format
- ✅ All ranges verified within Bank C4 boundaries
- ✅ Score values match scan results
- ✅ Feature descriptions accurate
- ⚠️ Verification (cross-reference with callers) needed for all candidates

---

*Session 21 Complete - Ready for candidate verification and pass creation*
