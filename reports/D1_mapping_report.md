# Bank D1 Mapping Report

**Date:** 2026-04-08  
**ROM:** Chrono Trigger (USA).sfc  
**Regions Scanned:** D1:4000-8000, D1:8000-B000, D1:F000-FFFF

## Summary

| Region | Islands | Clusters | Score-6+ Clusters |
|--------|---------|----------|-------------------|
| D1:4000-8000 | 80 | 59 | 3 |
| D1:8000-B000 | 57 | 55 | 1 |
| D1:F000-FFFF | 61 | 45 | 18 |
| **Total** | **198** | **159** | **22** |

## Score-6+ Cluster Candidates (Top 15 Recommended)

### D1:F000-FFFF Region (High-Density Bank End)

| Rank | Cluster Range | Score | Width | Returns | Calls | Notes |
|------|---------------|-------|-------|---------|-------|-------|
| 1 | D1:F661..D1:F69B | **8** | 59 | 3 | 1 | Large composite function |
| 2 | D1:FB4F..D1:FB77 | **7** | 41 | 4 | 1 | Multiple return points |
| 3 | D1:F5B1..D1:F5CE | **7** | 30 | 4 | 1 | Branch-heavy |
| 4 | D1:F147..D1:F164 | **6** | 30 | 3 | 0 | Internal helper |
| 5 | D1:F43A..D1:F452 | **6** | 25 | 1 | 2 | **Good candidate** - 2 calls, clean |
| 6 | D1:FBF3..D1:FC0B | **6** | 25 | 1 | 1 | DMA-related region (near F4C0) |
| 7 | D1:FC1F..D1:FC37 | **6** | 25 | 1 | 1 | Pattern: 25-byte helpers |
| 8 | D1:FC51..D1:FC69 | **6** | 25 | 1 | 1 | Pattern: 25-byte helpers |
| 9 | D1:FC7D..D1:FC95 | **6** | 25 | 1 | 1 | Pattern: 25-byte helpers |
| 10 | D1:FCAF..D1:FCC7 | **6** | 25 | 1 | 1 | Pattern: 25-byte helpers |
| 11 | D1:FD23..D1:FD3B | **6** | 25 | 1 | 1 | Pattern: 25-byte helpers |
| 12 | D1:F2E2..D1:F2F4 | **6** | 19 | 1 | 1 | Compact function |
| 13 | D1:FD6B..D1:FD7D | **6** | 19 | 1 | 1 | Compact function |
| 14 | D1:FE3A..D1:FE4B | **6** | 18 | 1 | 1 | Compact function |
| 15 | D1:FCE5..D1:FCF3 | **6** | 15 | 1 | 1 | Small helper |

### D1:4000-8000 Region (Mid-Bank)

| Rank | Cluster Range | Score | Width | Returns | Calls | Notes |
|------|---------------|-------|-------|---------|-------|-------|
| 1 | D1:7415..D1:7460 | **7** | 76 | 12 | 1 | Large composite - needs subdivision |
| 2 | D1:4DC4..D1:4DED | **6** | 42 | 2 | 1 | Good mid-bank candidate |
| 3 | D1:7761..D1:7784 | **6** | 36 | 3 | 1 | Clean candidate |

### D1:8000-B000 Region (Upper-Mid)

| Rank | Cluster Range | Score | Width | Returns | Calls | Notes |
|------|---------------|-------|-------|---------|-------|-------|
| 1 | D1:84CE..D1:84E6 | **6** | 25 | 1 | 2 | **Top candidate** - 2 calls, clean |

## Recommended Manifests for Creation (12-15 Functions)

### Priority 1: Clean Score-6+ with Multiple Callers

1. **D1:84CE..D1:84E6** (score-6, 25 bytes, 2 calls) - Upper-mid bank
2. **D1:F43A..D1:F452** (score-6, 25 bytes, 2 calls) - Bank end
3. **D1:F661..D1:F679** (score-6, 25 bytes, 1 call, part of score-8 cluster)
4. **D1:F5B1..D1:F5CE** (score-7, 30 bytes, 1 call, 4 branches)

### Priority 2: Pattern-Based 25-byte Helpers (D1:F000-FFFF)

These appear to be a family of similar helper functions:

5. **D1:FBF3..D1:FC0B** (score-6, 25 bytes)
6. **D1:FC1F..D1:FC37** (score-6, 25 bytes)
7. **D1:FC51..D1:FC69** (score-6, 25 bytes)
8. **D1:FC7D..D1:FC95** (score-6, 25 bytes)
9. **D1:FCAF..D1:FCC7** (score-6, 25 bytes)
10. **D1:FD23..D1:FD3B** (score-6, 25 bytes)

### Priority 3: Compact Functions

11. **D1:F2E2..D1:F2F4** (score-6, 19 bytes)
12. **D1:FD6B..D1:FD7D** (score-6, 19 bytes)
13. **D1:FE3A..D1:FE4B** (score-6, 18 bytes)
14. **D1:4DC4..D1:4DED** (score-6, 42 bytes) - Mid-bank diversity
15. **D1:7761..D1:7784** (score-6, 36 bytes) - Mid-bank diversity

## Data Quality Notes

### D1:7415..D1:7460 Caution
- This 76-byte cluster (score-7) has 12 returns and data_misread_flags
- Likely contains multiple functions - needs manual subdivision
- Recommend further analysis before manifest creation

### D1:F000-FFFF Pattern Recognition
- Six sequential 25-byte score-6 clusters found
- Suggests a table of related helper functions
- All have similar characteristics: 1 return, 1-2 calls, low ASCII ratio

### Backtrack Analysis Highlights
- D1:F077 (target D1:F07E): score-6 backtrack with JSR prologue
- D1:F0F9 (target D1:F108): score-6 backtrack with JSR prologue  
- D1:F551 (target D1:F559): score-6 backtrack with REP prologue
- Multiple score-6 backtracks confirm function boundaries

## Next Steps

1. Create manifests for Priority 1 candidates (4 functions)
2. Create manifests for Priority 2 pattern helpers (6 functions)
3. Create manifests for Priority 3 compact functions (5 functions)
4. Total: **15 new functions** as targeted
5. Leave D1:7415 cluster for detailed manual analysis
