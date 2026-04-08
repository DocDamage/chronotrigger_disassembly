# Bank C1 Hub Function Deep Dive Report

**Date:** 2026-04-08  
**Analysis Target:** C1:179C, C1:1B55, C1:4AEB Hub Regions  
**Status:** COMPLETE

---

## 1. Executive Summary

Three major hub functions in Bank C1 have been analyzed and validated:

| Hub | Callers | Type | Validation |
|-----|---------|------|------------|
| C1:179C | 25 valid, 1 invalid | Jump-based | Weak anchors (callers in unresolved regions) |
| C1:1B55 | 29 valid, 0 invalid | JSR-based | Weak anchors (callers in unresolved regions) |
| C1:4AEB | 27 valid, 3 invalid | JSR-based | Weak anchors (callers in unresolved regions) |

**Total new function candidates identified:** 12+ score-6+ candidates  
**Coverage increase potential:** Bank C1: 0.59% → ~2-3%

---

## 2. Hub Validation Results

### 2.1 C1:179C Hub (25 JMP Callers)

**Caller Distribution:**
- 25 JMP callers from C1:1100-C1:1700 region
- 1 invalid JSR from D2:E012 (bank mismatch - resolves to D2:179C)

**Key Callers:**
```
C1:115C, C1:11DE, C1:1215, C1:124D, C1:1261, C1:1278, C1:12B9, C1:12EA
C1:131D, C1:1366, C1:138C, C1:13AA, C1:13F1, C1:143A, C1:1495, C1:14D8
C1:14E9, C1:14FF, C1:1519, C1:1534, C1:1548, C1:155E, C1:1617, C1:174B, C1:1783
```

**Analysis:**
- All callers use JMP (not JSR) → This is a jump table dispatch hub
- Callers are in unresolved regions → Weak but valid anchor evidence
- Hub function appears to handle multiple entry points for state dispatch

### 2.2 C1:1B55 Hub (29 JSR Callers)

**Caller Distribution:**
- 29 JSR callers from C1:1100-C1:2300 region

**Key Callers:**
```
C1:11B7, C1:11C3, C1:11D8, C1:11E7, C1:121E, C1:1334, C1:1340, C1:1350
C1:1360, C1:1443, C1:144F, C1:145F, C1:146F, C1:147B, C1:1487, C1:1574
C1:15EE, C1:1602, C1:1611, C1:217A, C1:2188, C1:21C0, C1:21CE, C1:2214
C1:2222, C1:226B, C1:2279, C1:2301, C1:230F
```

**Analysis:**
- All callers use JSR → This is a proper subroutine hub
- Wide distribution suggests utility/initialization function

### 2.3 C1:4AEB Hub (27 JSR Callers)

**Caller Distribution:**
- 27 JSR callers from C1:8500-C1:E000 region
- 3 invalid JSR from FD:XXXX (bank mismatch - resolve to FD:4AEB)

**Key Callers:**
```
C1:851F, C1:8660, C1:86F4, C1:88B1, C1:88D8, C1:89AD, C1:89F1, C1:8A3D
C1:8A89, C1:8AB2, C1:8B23, C1:8BF4, C1:8E2D, C1:9A0A, C1:9DF7, C1:9E38
C1:B22D, C1:B3FB, C1:C02B, C1:C064, C1:C183, C1:C1EB, C1:C2AC, C1:C303
C1:C360, C1:C3EC, C1:E00B
```

**Analysis:**
- Most dispersed caller distribution (8500-E000)
- Likely a core utility or data processing function
- Many callers in C1:B200-C1:C400 (battle/event related region)

---

## 3. Backtrack Scoring Results

### 3.1 C1:1700-1800 Region (C1:179C Hub)

| Target | Best Start | Score | Distance | Notes |
|--------|------------|-------|----------|-------|
| C1:179C | C1:178E | **6** | 14 | clean_start - HUB CANDIDATE |
| C1:17B3 | C1:17A5 | **6** | 14 | clean_start |
| C1:17BF | C1:17BC | **6** | 3 | clean_start |
| C1:17DD | C1:17DA | **6** | 3 | clean_start |
| C1:17D1 | C1:17D1 | 5 | 0 | clean_start |

### 3.2 C1:1B00-1C00 Region (C1:1B55 Hub)

| Target | Best Start | Score | Distance | Notes |
|--------|------------|-------|----------|-------|
| C1:1B14 | C1:1B06 | **6** | 14 | clean_start |
| C1:1BAA | C1:1B9B | **6** | 15 | clean_start |
| C1:1B55 | C1:1B55 | 3 | 0 | clean_start - HUB ENTRY |
| C1:1B67 | C1:1B67 | 1 | 0 | clean_start |

### 3.3 C1:4A00-4B00 Region (C1:4AEB Hub)

| Target | Best Start | Score | Distance | Notes |
|--------|------------|-------|----------|-------|
| C1:4A71 | C1:4A6B | **6** | 6 | clean_start |
| C1:4AA8 | C1:4A9F | 4 | 9 | clean_start |
| C1:4AD0 | C1:4AC7 | 4 | 9 | clean_start |
| C1:4AEB | C1:4ADB | 2 | 16 | clean_start - HUB ENTRY |

---

## 4. Code Island Discoveries

### 4.1 High-Score Clusters (Score 6+)

| Region | Cluster | Score | Width | Priority |
|--------|---------|-------|-------|----------|
| C1:1100-1600 | C1:1569-159C | 9 | 52 bytes | HIGH |
| C1:1100-1600 | C1:1183-119B | 6 | 25 bytes | MEDIUM |
| C1:1100-1600 | C1:15A6-15BD | 6 | 24 bytes | MEDIUM |
| C1:1500-1A00 | C1:1933-194B | 6 | 25 bytes | MEDIUM |
| C1:1900-1F00 | C1:1C3E-1C65 | 8 | 40 bytes | HIGH |
| C1:4800-4D00 | C1:4CBD-4CF6 | 9 | 58 bytes | HIGH |
| C1:4800-4D00 | C1:492A-4942 | 6 | 25 bytes | MEDIUM |
| C1:4800-4D00 | C1:49E6-49FE | 6 | 25 bytes | MEDIUM |
| C1:4800-4D00 | C1:4A58-4A70 | 6 | 25 bytes | MEDIUM |
| C1:8000-8700 | C1:83DE-83EE | 6 | 17 bytes | MEDIUM |
| C1:8500-9000 | C1:8E95-8EAA | 8 | 22 bytes | HIGH |
| C1:8500-9000 | C1:8C2F-8C3D | 7 | 15 bytes | HIGH |
| C1:8500-9000 | C1:8824-883C | 6 | 25 bytes | MEDIUM |
| C1:8500-9000 | C1:8EF8-8F10 | 6 | 25 bytes | MEDIUM |
| C1:8500-9000 | C1:8D21-8D35 | 6 | 21 bytes | MEDIUM |
| C1:8500-9000 | C1:8963-8974 | 6 | 18 bytes | MEDIUM |
| C1:9A00-9F00 | C1:9DD4-9DDF | 6 | 12 bytes | MEDIUM |
| C1:B200-B600 | C1:B3A2-B3C2 | 8 | 33 bytes | HIGH |
| C1:B200-B600 | C1:B2F8-B301 | 6 | 10 bytes | MEDIUM |
| C1:C000-C500 | C1:C011-C029 | 6 | 25 bytes | MEDIUM |

---

## 5. Score-6+ Promotion Candidates

### 5.1 Immediate Promotion Candidates (Score 6+)

| Address | Score | Caller Count | Region | Recommended Name |
|---------|-------|--------------|--------|------------------|
| C1:178E | 6 | 25 | C1:1700-1800 | CT_C1_178E_HUB_25CALLERS |
| C1:17A5 | 6 | - | C1:1700-1800 | CT_C1_17A5_UTILITY_SCORE6 |
| C1:17BC | 6 | - | C1:1700-1800 | CT_C1_17BC_DISPATCH_SCORE6 |
| C1:17DA | 6 | - | C1:1700-1800 | CT_C1_17DA_HANDLER_SCORE6 |
| C1:1B06 | 6 | - | C1:1B00-1C00 | CT_C1_1B06_INIT_SCORE6 |
| C1:1B9B | 6 | - | C1:1B00-1C00 | CT_C1_1B9B_HANDLER_SCORE6 |
| C1:1B55 | 3* | 29 | C1:1B00-1C00 | CT_C1_1B55_HUB_29CALLERS |
| C1:4A6B | 6 | - | C1:4A00-4B00 | CT_C1_4A6B_UTILITY_SCORE6 |
| C1:4AEB | 2* | 27 | C1:4A00-4B00 | CT_C1_4AEB_HUB_27CALLERS |

*Hub entries have lower backtrack scores but high caller validation

### 5.2 Secondary Promotion Candidates (Related to Hubs)

| Address | Score | Relation to Hub |
|---------|-------|-----------------|
| C1:1569 | 9 | Called from C1:179C hub region |
| C1:1183 | 6 | C1:1100-1600 caller region |
| C1:1C3E | 8 | Post-C1:1B55 region |
| C1:4CBD | 9 | Near C1:4AEB hub callers |
| C1:8E95 | 8 | C1:4AEB caller (C1:8E2D nearby) |
| C1:8C2F | 7 | C1:4AEB caller region |
| C1:B3A2 | 8 | C1:4AEB caller (C1:B22D/B3FB) |

---

## 6. Recommended New Manifests

### 6.1 Hub Function Manifests (Priority 1)

```json
{
  "label": "CT_C1_178E_JUMP_HUB_25CALLERS",
  "addr": "C1:178E",
  "score": 6,
  "type": "hub",
  "caller_count": 25,
  "callers": ["C1:115C", "C1:11DE", "C1:1215", "C1:124D", "C1:1261", "C1:1278", "C1:12B9", "C1:12EA", "C1:131D", "C1:1366", "C1:138C", "C1:13AA", "C1:13F1", "C1:143A", "C1:1495", "C1:14D8", "C1:14E9", "C1:14FF", "C1:1519", "C1:1534", "C1:1548", "C1:155E", "C1:1617", "C1:174B", "C1:1783"]
}
```

```json
{
  "label": "CT_C1_1B55_SUB_HUB_29CALLERS",
  "addr": "C1:1B55",
  "score": 3,
  "validated_callers": 29,
  "type": "hub",
  "note": "Hub entry - score overridden by caller validation"
}
```

```json
{
  "label": "CT_C1_4AEB_SUB_HUB_27CALLERS",
  "addr": "C1:4AEB",
  "score": 2,
  "validated_callers": 27,
  "type": "hub",
  "note": "Hub entry - score overridden by caller validation"
}
```

### 6.2 Score-6 Function Manifests (Priority 2)

```json
[
  {"label": "CT_C1_17A5_HANDLER_SCORE6", "addr": "C1:17A5", "score": 6},
  {"label": "CT_C1_17BC_DISPATCH_SCORE6", "addr": "C1:17BC", "score": 6},
  {"label": "CT_C1_17DA_UTILITY_SCORE6", "addr": "C1:17DA", "score": 6},
  {"label": "CT_C1_1B06_INIT_SCORE6", "addr": "C1:1B06", "score": 6},
  {"label": "CT_C1_1B9B_HANDLER_SCORE6", "addr": "C1:1B9B", "score": 6},
  {"label": "CT_C1_4A6B_UTILITY_SCORE6", "addr": "C1:4A6B", "score": 6}
]
```

### 6.3 High-Score Cluster Manifests (Priority 3)

```json
[
  {"label": "CT_C1_1569_CLUSTER_SCORE9", "addr": "C1:1569", "score": 9, "width": 52},
  {"label": "CT_C1_1C3E_CLUSTER_SCORE8", "addr": "C1:1C3E", "score": 8, "width": 40},
  {"label": "CT_C1_4CBD_CLUSTER_SCORE9", "addr": "C1:4CBD", "score": 9, "width": 58},
  {"label": "CT_C1_8E95_CLUSTER_SCORE8", "addr": "C1:8E95", "score": 8, "width": 22},
  {"label": "CT_C1_8C2F_CLUSTER_SCORE7", "addr": "C1:8C2F", "score": 7, "width": 15},
  {"label": "CT_C1_B3A2_CLUSTER_SCORE8", "addr": "C1:B3A2", "score": 8, "width": 33}
]
```

---

## 7. Regional Analysis

### 7.1 C1:1000-2000 Region (Jump Table Territory)
- Dominated by C1:179C jump hub
- 25 JMP callers suggests switch/case dispatch pattern
- C1:1183, C1:1569, C1:15A6 candidates in caller region

### 7.2 C1:2000-3000 Region (Subroutine Network)
- C1:1B55 hub connects to C1:2100-2400 callers
- C1:214A, C1:2310, C1:211E, C1:238E island candidates
- Likely initialization or state management code

### 7.3 C1:4000-5000 Region (Core Processing)
- C1:4AEB hub with 27 dispersed callers
- C1:4CBD high-score cluster nearby
- C1:492A, C1:49E6, C1:4A58 score-6 candidates
- Likely central data processing or utility functions

### 7.4 C1:8000-A000 Region (Extended Utilities)
- C1:8E95, C1:8C2F, C1:8824, C1:8EF8 score-6+ clusters
- Multiple C1:4AEB callers in this region
- Rich code territory for further exploration

### 7.5 C1:B000-C000 Region (Battle/Event Support)
- C1:B3A2 high-score cluster
- Many C1:4AEB callers (C1:B22D, C1:B3FB)
- C1:C011, C1:C100, C1:C169, C1:C1C4 candidates
- Likely battle system or event script support

---

## 8. Next Steps & Recommendations

### Immediate Actions:
1. **Promote 3 hub functions** with caller-validation override
2. **Promote 6 score-6 functions** around hub regions
3. **Promote 6 high-score clusters** (score 7-9)

### Follow-up Analysis:
1. Run anchor reports on C1:1569 (score-9 cluster)
2. Investigate C1:2100-2400 caller network
3. Deep dive C1:8000-9000 rich code region
4. Cross-bank analysis: FD:4AEB relationship to C1:4AEB

### Coverage Impact:
- Current Bank C1: 3 documented ranges (0.59%)
- Projected after promotions: ~15-20 ranges (~2-3%)
- Remaining untapped regions: C1:3000-4000, C1:6000-8000, C1:A000-FFFF

---

## 9. Files Generated

- Anchor reports: C1:179C, C1:1B55, C1:4AEB
- Backtrack scores: C1:1700-1800, C1:1B00-1C00, C1:4A00-4B00
- Code island scans: C1:1500-1A00, C1:1900-1F00, C1:4800-4D00, C1:8000-8700, C1:8500-9000, C1:9A00-9F00, C1:B200-B600, C1:C000-C500

---

*Report generated by Bank C1 Hub Deep Dive analysis workflow*
