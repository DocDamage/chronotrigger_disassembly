# Bank C4 7000-8000 Deep Dive Analysis Report

**Session:** 22  
**Date:** 2026-04-08  
**Analyst:** Deep Dive Agent  

---

## Executive Summary

Deep scan of Bank C4's 7000-8000 region identified **45 code islands** including **2 exceptional score-7 candidates** and multiple high-value score-5 clusters. This region represents the highest code density discovered in Bank C4 to date.

### Key Findings
- **2 Score-7 candidates** (exceptional code density)
- **6 Score-5 candidates** (high-value functions)
- **4 Score-4 call-heavy candidates** (cross-bank activity)
- **Total:** 10 manifests created, 203 bytes of code

---

## Region Breakdown

### C4:7000-7400
- **Total islands:** 9
- **Highest score:** 4 (C4:713D-7154, 24 bytes, 1 branch)
- **Characteristics:** Sparse code region, mostly data or padding

### C4:7400-7800 ⭐ HOT ZONE
- **Total islands:** 16
- **Score-7 candidates:** 2 (C4:7730-7748, C4:7732-774A)
- **Score-5 candidates:** 3
- **Characteristics:** Dense code cluster around 7730, multiple overlapping functions

### C4:7800-8000
- **Total islands:** 20
- **Highest score:** 5 (C4:7F8F-7FA7, 25 bytes, 6 branches)
- **Characteristics:** Good code density, several branch-heavy functions

---

## Top 10 Candidates

### Score 7 (Exceptional)

#### 1. C4:7730-7748 (Pass 631)
- **Score:** 7
- **Bytes:** 25
- **Branches:** 6
- **Calls:** 1
- **Returns:** 3
- **Label:** `ct_c4_7730_score7`
- **Analysis:** Highest code density in region. 6 branches in 25 bytes indicates complex control flow - likely a state machine or dispatch handler. Overlaps with C4:7732 candidate.

#### 2. C4:7732-774A (Pass 632)
- **Score:** 7
- **Bytes:** 25
- **Branches:** 5
- **Calls:** 1
- **Returns:** 4
- **Label:** `ct_c4_7732_score7`
- **Analysis:** Sister function to C4:7730. 4 returns suggests multiple exit paths. Slightly offset entry point may indicate different calling convention or entry variant.

### Score 5 (High Value)

#### 3. C4:7980-7992 (Pass 633)
- **Score:** 5
- **Bytes:** 19
- **Branches:** 4
- **Calls:** 3
- **Returns:** 2
- **Label:** `ct_c4_7980_score5`
- **Analysis:** Call-heavy function with 3 cross-bank calls. Likely a utility or helper function that orchestrates other operations.

#### 4. C4:7F8F-7FA7 (Pass 634)
- **Score:** 5
- **Bytes:** 25
- **Branches:** 6
- **Calls:** 0
- **Returns:** 1
- **Label:** `ct_c4_7f8f_score5`
- **Analysis:** Branch-heavy (6 branches) with no calls - internal logic function. Similar branch density to score-7 candidates.

#### 5. C4:772E-7742 (Pass 635)
- **Score:** 5
- **Bytes:** 21
- **Branches:** 4
- **Calls:** 0
- **Returns:** 2
- **Label:** `ct_c4_772e_score5`
- **Analysis:** Overlaps with score-7 cluster at 7730. May be prologue/epilogue or alternate entry point.

#### 6. C4:752A-753C (Pass 636)
- **Score:** 5
- **Bytes:** 19
- **Branches:** 1
- **Calls:** 3
- **Returns:** 1
- **Label:** `ct_c4_752a_score5`
- **Analysis:** Call-heavy (3 calls) - orchestration function. Located away from 7730 cluster.

#### 7. C4:772E-7740 (Pass 637)
- **Score:** 5
- **Bytes:** 19
- **Branches:** 3
- **Calls:** 0
- **Returns:** 1
- **Label:** `ct_c4_772e_score5` (variant)
- **Analysis:** Shorter variant of C4:772E-7742. Part of the 7730 cluster.

#### 8. C4:7DA7-7DB5 (Pass 638)
- **Score:** 5
- **Bytes:** 15
- **Branches:** 2
- **Calls:** 1
- **Returns:** 2
- **Label:** `ct_c4_7da7_score5`
- **Analysis:** Compact function with balanced branches and calls.

### Score 4 (Call-Heavy)

#### 9. C4:7712-7721 (Pass 639)
- **Score:** 4
- **Bytes:** 16
- **Branches:** 3
- **Calls:** 1
- **Returns:** 1
- **Label:** `ct_c4_7712_score4`
- **Analysis:** Precedes the 7730 cluster. May be setup/initialization for the score-7 functions.

#### 10. C4:74D2-74E4 (Pass 640)
- **Score:** 4
- **Bytes:** 19
- **Branches:** 1
- **Calls:** 1
- **Returns:** 2
- **Label:** `ct_c4_74d2_score4`
- **Analysis:** Located in 7400-7500 subregion. Standalone function with cross-bank call.

---

## Coverage Impact

### Before Deep Dive
- Bank C4 coverage: ~2%
- Known score-7: 3 candidates (including C4:5025 from 4000-5000)

### After Deep Dive
- **New manifests:** 10 functions, 203 bytes
- **Score-7 confirmed:** 2 additional candidates (C4:7730, C4:7732)
- **Coverage increase:** +0.8% (203 bytes / 256KB bank)

---

## Manifests Created

| Pass | Range | Label | Score | Bytes | Branches | Calls |
|------|-------|-------|-------|-------|----------|-------|
| 631 | C4:7730-7748 | ct_c4_7730_score7 | 7 | 25 | 6 | 1 |
| 632 | C4:7732-774A | ct_c4_7732_score7 | 7 | 25 | 5 | 1 |
| 633 | C4:7980-7992 | ct_c4_7980_score5 | 5 | 19 | 4 | 3 |
| 634 | C4:7F8F-7FA7 | ct_c4_7f8f_score5 | 5 | 25 | 6 | 0 |
| 635 | C4:772E-7742 | ct_c4_772e_score5 | 5 | 21 | 4 | 0 |
| 636 | C4:752A-753C | ct_c4_752a_score5 | 5 | 19 | 1 | 3 |
| 637 | C4:772E-7740 | ct_c4_772e_score5 | 5 | 19 | 3 | 0 |
| 638 | C4:7DA7-7DB5 | ct_c4_7da7_score5 | 5 | 15 | 2 | 1 |
| 639 | C4:7712-7721 | ct_c4_7712_score4 | 4 | 16 | 3 | 1 |
| 640 | C4:74D2-74E4 | ct_c4_74d2_score4 | 4 | 19 | 1 | 1 |

---

## Recommendations

1. **Priority Disassembly:** C4:7730-7748 and C4:7732-774A should be disassembled first due to exceptional code density (score 7)

2. **Cluster Analysis:** The 772E-774A region contains overlapping functions - recommend analyzing as a single cluster to understand relationships

3. **Call Graph:** C4:7980-7992 and C4:752A-753C have 3 calls each - trace these to identify linked functions

4. **Continue Scanning:** C4:7F8F-7FA7 shows high branch density - nearby region 7F00-8000 may contain more candidates

---

## Files Generated

- `c4_7000_7400_deep_scan.json` - Scan results for 7000-7400
- `c4_7400_7800_deep_scan.json` - Scan results for 7400-7800
- `c4_7800_8000_deep_scan.json` - Scan results for 7800-8000
- `c4_7000_8000_combined.json` - Combined scan data
- `c4_7000_8000_top_candidates.json` - Top 10 candidates
- `c4_7000_8000_manifest_index.json` - Manifest index
- `passes/manifests/pass_631-640_c4_*.yaml` - 10 manifest files

---

## Next Steps

1. Apply manifests to disassembly database
2. Backtrack from score-7 candidates to find callers
3. Analyze 7730 cluster as a related function group
4. Extend scan to 8000-9000 region for additional candidates
