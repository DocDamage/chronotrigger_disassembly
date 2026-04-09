# Bank C3 Session 24 Coverage Push Report

## Executive Summary

**Session Goal:** Push Bank C3 toward 28% coverage target  
**Current Coverage:** ~24.7%  
**Target Coverage:** 28%  
**Gap to Close:** ~3.3% (~530 bytes)

## Results

### Manifests Created: 15
### Potential Coverage Gain: 322 bytes (60.7% of gap)

---

## Major Discoveries

### Superclusters Found

| Address | Score | Width | Returns | Type |
|---------|-------|-------|---------|------|
| **C3:3779** | 8 | 42 bytes | 5 | Multi-return dispatch |
| **C3:3E53** | 7 | 23 bytes | 3 | Call/branch/return pattern |

These superclusters represent exceptional code discovery opportunities with multiple return points indicating dispatch-style functions.

---

## Manifest Summary by Region

### C3:3000-4000 (7 manifests)
| Manifest | Score | Coverage |
|----------|-------|----------|
| C3_3779_SUPERCLUSTER_SCORE8.yaml | 8 | 42 bytes |
| C3_3E53_SCORE7_DISPATCH.yaml | 7 | 23 bytes |
| C3_373D_SCORE6_FUNCTION.yaml | 6 | 17 bytes |
| C3_30B6_SCORE6_FUNCTION.yaml | 6 | 9 bytes |
| C3_3DE2_SCORE6_DISPATCH.yaml | 6 | 15 bytes |
| C3_3BBD_SCORE5_FUNCTION.yaml | 5 | 21 bytes |
| C3_3B8E_SCORE5_FUNCTION.yaml | 5 | 20 bytes |
| **Subtotal** | | **147 bytes** |

### C3:5000-6000 (4 manifests)
| Manifest | Score | Coverage |
|----------|-------|----------|
| C3_559F_SCORE6_CLUSTER.yaml | 6 | 35 bytes |
| C3_5364_SCORE6_CLUSTER.yaml | 6 | 18 bytes |
| C3_5B22_SCORE5_FUNCTION.yaml | 5 | 25 bytes |
| C3_5C4D_SCORE5_FUNCTION.yaml | 5 | 25 bytes |
| **Subtotal** | | **103 bytes** |

### C3:6000-7000 (2 manifests)
| Manifest | Score | Coverage |
|----------|-------|----------|
| C3_6334_SCORE6_FUNCTION.yaml | 6 | 18 bytes |
| C3_6641_SCORE6_FUNCTION.yaml | 6 | 9 bytes |
| **Subtotal** | | **27 bytes** |

### C3:7000-8000 (2 manifests)
| Manifest | Score | Coverage |
|----------|-------|----------|
| C3_771C_SCORE5_FUNCTION.yaml | 5 | 25 bytes |
| C3_74F5_SCORE5_FUNCTION.yaml | 5 | 20 bytes |
| **Subtotal** | | **45 bytes** |

---

## Coverage Impact Analysis

### By Score Level
- **Score 8:** 42 bytes (1 manifest)
- **Score 7:** 23 bytes (1 manifest)  
- **Score 6:** 121 bytes (6 manifests)
- **Score 5:** 136 bytes (7 manifests)

### Projected Coverage Progress

| Metric | Value |
|--------|-------|
| Starting Coverage | ~24.7% |
| Manifests Created | 15 |
| Potential Bytes Mapped | 322 |
| % of 530-byte Gap | 60.7% |
| **Projected New Coverage** | **~26.5%** |
| **Distance to 28% Target** | **~1.5%** |

---

## Key Findings

### 1. C3:3779 - Multi-Return Dispatch (Score 8)
- **42 bytes** with **5 return points**
- Child count of 5 suggests overlapping code blocks or switch-case structure
- Exceptional candidate for verification

### 2. C3:3E53 - High-Value Cluster (Score 7)
- **23 bytes** with **3 returns** and **2 calls**
- Strong code indicators with multiple stackish ops
- Multiple child ranges indicate complex structure

### 3. Score-6 Clusters (6 manifests, 121 bytes)
- C3:559F (35 bytes, 6 branches) - complex control flow
- C3:5364 (18 bytes, 2 returns) - dual exit function
- C3:373D (17 bytes) - standalone function
- C3:6334 (18 bytes) - low ASCII ratio
- C3:6641 (9 bytes) - compact function
- C3:3DE2 (15 bytes, 3 stackish ops) - stack-heavy dispatch

---

## Recommendations for Reaching 28%

1. **Verify Superclusters First**
   - C3:3779 and C3:3E53 provide 65 bytes of high-confidence code
   - Their dispatch patterns suggest important system functions

2. **Target C3:4000-5000 Gap**
   - This region was not fully scanned in this session
   - May contain additional score-6+ candidates

3. **Continue C3:6000-8000**
   - Only 4 manifests created in this 2KB region
   - Potential for additional 100-150 bytes

4. **Remaining Gap to Close**
   - ~208 bytes needed after these manifests
   - Approximately 10-12 additional score-5+ manifests required

---

## Files Created

```
labels/c3_candidates/
├── C3_30B6_SCORE6_FUNCTION.yaml
├── C3_373D_SCORE6_FUNCTION.yaml
├── C3_3779_SUPERCLUSTER_SCORE8.yaml
├── C3_3B8E_SCORE5_FUNCTION.yaml
├── C3_3BBD_SCORE5_FUNCTION.yaml
├── C3_3DE2_SCORE6_DISPATCH.yaml
├── C3_3E53_SCORE7_DISPATCH.yaml
├── C3_5364_SCORE6_CLUSTER.yaml
├── C3_559F_SCORE6_CLUSTER.yaml
├── C3_5B22_SCORE5_FUNCTION.yaml
├── C3_5C4D_SCORE5_FUNCTION.yaml
├── C3_6334_SCORE6_FUNCTION.yaml
├── C3_6641_SCORE6_FUNCTION.yaml
├── C3_74F5_SCORE5_FUNCTION.yaml
└── C3_771C_SCORE5_FUNCTION.yaml
```

---

## Session 24 Completion Status

✅ **15 manifests created**  
✅ **322 bytes potential coverage**  
✅ **2 superclusters discovered**  
✅ **6 score-6+ candidates**  
✅ **Projected 26.5% coverage** (within 1.5% of target)

**Next Steps:** Verify manifests and continue scanning C3:4000-5000 and C3:6000-8000 regions.
