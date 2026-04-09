# Session 22: Bank C2 Extended Hub Analysis Report

**Date:** 2026-04-08  
**Scope:** Extend Bank C2 disassembly from B716 hub (both directions)  
**Session:** 22

---

## Executive Summary

Extended Bank C2 analysis from the B716 cross-bank hub in both directions:
- **Preceding region:** C2:A000-C2:B000
- **Following region:** C2:B800-C2:C000

**Results:**
- 56 islands discovered in A000-B000 region
- 27 islands discovered in B800-C000 region
- 11 new manifests created (session target: 6-8, achieved: 11)
- Total C2 coverage: 18 manifests across B000-C000 and A000-B000 regions

---

## Scan Results

### Region 1: C2:A000-C2:B000 (Preceding B716)

| Statistic | Value |
|-----------|-------|
| Total Islands | 56 |
| Total Clusters | 48 |
| Score 7+ | 4 candidates |
| Score 6 | 7 candidates |
| Score 5 | 12 candidates |

**High-Value Candidates:**

| Address | End | Score | Width | Calls | Branches | ASCII |
|---------|-----|-------|-------|-------|----------|-------|
| C2:A4FF | C2:A517 | 7 | 25 | 3 | 3 | 0.20 |
| C2:A6D7 | C2:A6EF | 7 | 25 | 1 | 4 | 0.16 |
| C2:AB24 | C2:AB3A | 7 | 23 | 1 | 3 | 0.13 |
| C2:A5D2 | C2:A5E6 | 7 | 21 | 2 | 1 | 0.24 |
| C2:A492 | C2:A4AA | 6 | 25 | 4 | 0 | 0.28 |
| C2:AA53 | C2:AA6B | 6 | 25 | 2 | 3 | 0.28 |
| C2:ACE8 | C2:AD00 | 6 | 25 | 3 | 2 | 0.20 |
| C2:AE9D | C2:AEB5 | 6 | 25 | 3 | 0 | 0.28 |

**Cluster Discovery:**
- **AF72 Cluster (Score 8):** C2:AF72-C2:AFB4 (67 bytes, 3 returns)
  - Largest continuous code block in scan
  - Very low ASCII (0.149) - strongly indicates code
  - Multiple return points suggest dispatch pattern

### Region 2: C2:B800-C2:C000 (Following B716)

| Statistic | Value |
|-----------|-------|
| Total Islands | 27 |
| Total Clusters | 23 |
| Score 7 | 1 candidate |
| Score 6 | 5 candidates |
| Score 5 | 4 candidates |

**High-Value Candidates:**

| Address | End | Score | Width | Calls | Branches | ASCII |
|---------|-----|-------|-------|-------|----------|-------|
| C2:BFE6 | C2:BFFE | 7 | 25 | 4 | 1 | 0.24 |
| C2:B9F0 | C2:BA08 | 6 | 25 | 3 | 0 | 0.28 |
| C2:BEB5 | C2:BECD | 6 | 25 | 3 | 0 | 0.24 |
| C2:BFAC | C2:BFC4 | 6 | 25 | 4 | 1 | 0.24 |
| C2:BB07 | C2:BB19 | 6 | 19 | 1 | 0 | 0.16 |
| C2:B8B2 | C2:B8C0 | 6 | 15 | 1 | 1 | 0.13 |

---

## Manifests Created (Session 22)

### Score 8 (1 manifest)
| File | Range | Notes |
|------|-------|-------|
| bank_C2_AF72_cluster_score8.yaml | AF72-AFB4 | 67-byte cluster, dispatch pattern |

### Score 7 (4 manifests)
| File | Range | Notes |
|------|-------|-------|
| bank_C2_A4FF_score7.yaml | A4FF-A517 | 3 calls, 3 branches |
| bank_C2_A6D7_score7.yaml | A6D7-A6EF | 4 branches, pure code |
| bank_C2_AB24_score7.yaml | AB24-AB3A | Low ASCII (0.13) |
| bank_C2_A5D2_score7.yaml | A5D2-A5E6 | Compact utility (21 bytes) |

### Score 6 (5 manifests)
| File | Range | Notes |
|------|-------|-------|
| bank_C2_A492_score6.yaml | A492-A4AA | 4 calls, shared utility |
| bank_C2_ACE8_score6.yaml | ACE8-AD00 | 3 calls, 2 branches |
| bank_C2_AE9D_score6.yaml | AE9D-AEB5 | 3 calls, straight-line |
| bank_C2_BB07_score6.yaml | BB07-BB19 | Low ASCII (0.16) |
| bank_C2_B8B2_score6.yaml | B8B2-B8C0 | Compact 15-byte |

### Score 5 (1 manifest)
| File | Range | Notes |
|------|-------|-------|
| bank_C2_BD95_score5.yaml | BD95-BDA5 | High stack ops (3) |

**Total New Manifests: 11**

---

## Complete C2 Manifest Inventory

| Score | Count | Manifests |
|-------|-------|-----------|
| 8 | 1 | AF72 cluster |
| 7 | 7 | A4FF, A6D7, AB24, A5D2, B030, B475, BFE6 |
| 6 | 9 | A492, ACE8, AE9D, B1C5, B8B2, B9F0, BB07, BFAC |
| 5 | 2 | B54F, BD95 |

**Total: 18 manifests**

---

## Cross-Bank Activity Analysis

### JSL Caller Search
Cross-bank caller analysis performed on key targets. JSL patterns not detected for A000-B000 region candidates, suggesting:
1. Functions called via internal JSR within Bank C2
2. Callers may be in unresolved regions
3. Functions may be data tables misidentified as code

### Settlement Service Context
- **B716 hub** remains the primary cross-bank settlement anchor
- **AF72 cluster** (score 8) shows dispatch pattern - possible secondary hub
- Functions between A000-B000 likely service helpers
- Functions between B800-C000 likely post-processing utilities

---

## Coverage Analysis

### Before Extension (Session 21)
- 7 manifests in B000-C000 region
- Focus on B716 hub and immediate neighbors

### After Extension (Session 22)
- 11 new manifests across A000-B000 and B800-C000
- Coverage extended to AF00 cluster (largest found)
- A400, A600, AB00, AC00, AE00 regions now documented

### Bank C2 Overall Coverage
- **Vector region (0000-1000):** Limited (1 candidate page)
- **A000-B000 region:** 11 manifests (new)
- **B000-C000 region:** 7 manifests (existing)
- **Coverage estimate:** ~2.1% of bank (up from ~1.66%)

---

## Key Findings

1. **AF72 Cluster (Score 8)**
   - Largest continuous code block found (67 bytes)
   - 3 return points indicate complex control flow
   - Possible dispatch table or switch-case structure
   - Highest priority for detailed disassembly

2. **A000-B000 Code Density**
   - Higher code density than expected
   - 56 islands in 4KB region vs 27 in B800-C000
   - Suggests active service region

3. **B800-C000 Boundaries**
   - Functions near C000 boundary (BFE6, BFAC)
   - Possible service/data transition
   - High call counts suggest shared utilities

---

## Recommendations

1. **Priority Disassembly Targets:**
   - AF72 cluster (score 8, dispatch pattern)
   - A4FF-A517 (score 7, 3 branches)
   - A6D7-A6EF (score 7, 4 branches)

2. **Cross-Bank Caller Investigation:**
   - Search unresolved banks for JSL patterns
   - Check banks CA, CB, CC, D7 (common callers)

3. **Next Scan Regions:**
   - C2:5000-6000 (vector targets 57DF, 5823)
   - C2:B200, B400, BC00 (candidate lanes)

4. **Hub Relationship Analysis:**
   - Map relationships between AF72 and B716
   - Identify settlement service call chains

---

## Files Modified/Created

### New Manifests (11)
- `labels/c2_candidates/bank_C2_AF72_cluster_score8.yaml`
- `labels/c2_candidates/bank_C2_A4FF_score7.yaml`
- `labels/c2_candidates/bank_C2_A6D7_score7.yaml`
- `labels/c2_candidates/bank_C2_AB24_score7.yaml`
- `labels/c2_candidates/bank_C2_A5D2_score7.yaml`
- `labels/c2_candidates/bank_C2_A492_score6.yaml`
- `labels/c2_candidates/bank_C2_ACE8_score6.yaml`
- `labels/c2_candidates/bank_C2_AE9D_score6.yaml`
- `labels/c2_candidates/bank_C2_BB07_score6.yaml`
- `labels/c2_candidates/bank_C2_B8B2_score6.yaml`
- `labels/c2_candidates/bank_C2_BD95_score5.yaml`

### Reports
- `AGENT_SWARM_SESSION_22_REPORT.md` (this file)

---

*Session 22 completed. 11 manifests created and validated. All manifests passed validation checks.*
