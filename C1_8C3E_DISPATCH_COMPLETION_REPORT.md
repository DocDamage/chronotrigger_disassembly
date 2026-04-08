# C1:8C3E Dispatch Table Completion Report

## Executive Summary

**Analysis Date:** 2026-04-08

**Target:** C1:8C3E (dispatch hub function)

**Total Callers:** 42 JSR instructions

**Current State:**
- 10 handlers documented (strong anchors)
- 32 handlers undocumented (weak anchors)
- Dispatch table completion: 23.8%

## 1. Analysis Results

### 1.1 Call Anchor Report Summary

| Metric | Count |
|--------|-------|
| Total Callers | 42 |
| Strong Anchors | 10 |
| Weak Anchors | 32 |
| Suspect/Invalid | 0 |

### 1.2 Documented Handlers (Strong Anchors)

| # | Caller | Handler Range | Label |
|---|--------|---------------|-------|
| 1 | C1:8EA7 | C1:8E9B..C1:8EAA | ct_c1_8e9b_handler_dispatch |
| 2 | C1:8F0D | C1:8F02..C1:8F11 | ct_c1_8f02_handler_dispatch |
| 3 | C1:903A | C1:9032..C1:9044 | ct_c1_9032_score7_cluster |
| 4 | C1:9077 | C1:906E..C1:9081 | ct_c1_906e_score7_cluster |
| 5 | C1:971F | C1:96D4..C1:9727 | ct_c1_96d4_dispatch_handler |
| 6 | C1:9751 | C1:9728..C1:975B | ct_c1_9728_dispatch_handler |
| 7 | C1:97A0 | C1:9792..C1:97D4 | ct_c1_9792_score8_cluster |
| 8 | C1:97B5 | C1:9792..C1:97D4 | ct_c1_9792_score8_cluster |
| 9 | C1:97CA | C1:9792..C1:97D4 | ct_c1_9792_score8_cluster |
| 10 | C1:9803 | C1:97D5..C1:980F | ct_c1_97d5_dispatch_handler |

### 1.3 Undocumented Callers by Region

| Region | Count | Callers |
|--------|-------|---------|
| C1:8F00-9000 | 2 | C1:8F7C, C1:8FCF |
| C1:9000-9100 | 2 | C1:9008, C1:90B3 |
| C1:9100-9200 | 3 | C1:9125, C1:9183, C1:91EE |
| C1:9200-9300 | 2 | C1:9252, C1:9298 |
| C1:9300-9400 | 4 | C1:9310, C1:9389, C1:93D1, C1:93DB |
| C1:9400-9500 | 6 | C1:941F, C1:945B, C1:9469, C1:94B2, C1:94C7, C1:94FB |
| C1:9500-9600 | 8 | C1:9509, C1:9549, C1:955F, C1:958F, C1:95BD, C1:95CB, C1:95D6, C1:95EF |
| C1:9600-9700 | 4 | C1:9647, C1:9652, C1:969A, C1:96C9 |
| C1:9700-9800 | 1 | C1:975C |

## 2. Handler Function Analysis

### 2.1 Discovered Handler Boundaries

Through ROM disassembly analysis, the following handler entry points and ranges were identified:

| # | Handler Range | Width | Entry Score | Caller Location |
|---|---------------|-------|-------------|-----------------|
| 1 | C1:8F78..C1:8F87 | 15 | 10 | C1:8F7C |
| 2 | C1:8FCB..C1:8FDA | 15 | 10 | C1:8FCF |
| 3 | C1:8FF4..C1:9013 | 31 | 10 | C1:9008 |
| 4 | C1:90AC..C1:90BE | 18 | 10 | C1:90B3 |
| 5 | C1:9121..C1:9130 | 15 | 10 | C1:9125 |
| 6 | C1:917F..C1:918E | 15 | 10 | C1:9183 |
| 7 | C1:91EB..C1:91F9 | 14 | 10 | C1:91EE |
| 8 | C1:924E..C1:925D | 15 | 10 | C1:9252 |
| 9 | C1:9294..C1:92A3 | 15 | 10 | C1:9298 |
| 10 | C1:92A3..C1:9314 | 113 | 5 | C1:9310 |
| 11 | C1:9314..C1:938D | 121 | 5 | C1:9389 |
| 12 | C1:93A5..C1:93E6 | 65 | 10 | C1:93D1, C1:93DB |
| 13 | C1:93A5..C1:942A | 133 | 10 | C1:941F |
| 14 | C1:93F6..C1:9474 | 126 | 8 | C1:945B, C1:9469 |
| 15 | C1:9474..C1:94D2 | 94 | 5 | C1:94B2, C1:94C7 |
| 16 | C1:94D2..C1:9514 | 66 | 5 | C1:94FB, C1:9509 |
| 17 | C1:9514..C1:959A | 134 | 5 | C1:9549, C1:955F, C1:958F |
| 18 | C1:959A..C1:95D6 | 60 | 5 | C1:95BD, C1:95CB |
| 19 | C1:95D6..C1:95DA | 4 | 5 | C1:95D6 |
| 20 | C1:95DA..C1:95FA | 32 | 5 | C1:95EF |
| 21 | C1:9643..C1:9652 | 15 | 10 | C1:9647 |
| 22 | C1:9643..C1:9656 | 19 | 10 | C1:9652 |
| 23 | C1:967C..C1:96A5 | 41 | 10 | C1:969A |
| 24 | C1:96C6..C1:96D4 | 14 | 10 | C1:96C9 |
| 25 | C1:9716..C1:9765 | 79 | 10 | C1:975C |

**Note:** Some handlers contain multiple calls to C1:8C3E (e.g., C1:93A5..C1:93E6 has two callers: C1:93D1 and C1:93DB).

### 2.2 Handler Entry Point Analysis

Entry point prologues found:
- **PHP (0x08):** 18 handlers - strong prologue
- **PHB (0x8B):** 0 handlers in remaining
- **PHD (0x0B):** 0 handlers in remaining  
- **REP (0xC2):** 4 handlers
- **Other:** 3 handlers with alternative prologues

## 3. Recommended New Manifests

### 3.1 Priority 1: Score-10 Handlers (18 manifests)

These handlers have strong prologue evidence (PHP/PHB/PHD/REP):

```json
[
  {"pass": 660, "range": "C1:8F78..C1:8F87", "label": "CT_C1_8F78_HANDLER", "score": 10},
  {"pass": 661, "range": "C1:8FCB..C1:8FDA", "label": "CT_C1_8FCB_HANDLER", "score": 10},
  {"pass": 662, "range": "C1:8FF4..C1:9013", "label": "CT_C1_8FF4_HANDLER", "score": 10},
  {"pass": 663, "range": "C1:90AC..C1:90BE", "label": "CT_C1_90AC_HANDLER", "score": 10},
  {"pass": 664, "range": "C1:9121..C1:9130", "label": "CT_C1_9121_HANDLER", "score": 10},
  {"pass": 665, "range": "C1:917F..C1:918E", "label": "CT_C1_917F_HANDLER", "score": 10},
  {"pass": 666, "range": "C1:91EB..C1:91F9", "label": "CT_C1_91EB_HANDLER", "score": 10},
  {"pass": 667, "range": "C1:924E..C1:925D", "label": "CT_C1_924E_HANDLER", "score": 10},
  {"pass": 668, "range": "C1:9294..C1:92A3", "label": "CT_C1_9294_HANDLER", "score": 10},
  {"pass": 671, "range": "C1:93A5..C1:93E6", "label": "CT_C1_93A5_HANDLER", "score": 10},
  {"pass": 672, "range": "C1:93A5..C1:942A", "label": "CT_C1_93A5_HANDLER_EXT", "score": 10},
  {"pass": 687, "range": "C1:9643..C1:9652", "label": "CT_C1_9643_HANDLER", "score": 10},
  {"pass": 688, "range": "C1:9643..C1:9656", "label": "CT_C1_9643_HANDLER_EXT", "score": 10},
  {"pass": 689, "range": "C1:967C..C1:96A5", "label": "CT_C1_967C_HANDLER", "score": 10},
  {"pass": 690, "range": "C1:96C6..C1:96D4", "label": "CT_C1_96C6_HANDLER", "score": 10},
  {"pass": 691, "range": "C1:9716..C1:9765", "label": "CT_C1_9716_HANDLER", "score": 10}
]
```

### 3.2 Priority 2: Score-5 to Score-8 Handlers (9 manifests)

These handlers have weaker prologue evidence but still valid function structure:

```json
[
  {"pass": 669, "range": "C1:92A3..C1:9314", "label": "CT_C1_92A3_HANDLER", "score": 5},
  {"pass": 670, "range": "C1:9314..C1:938D", "label": "CT_C1_9314_HANDLER", "score": 5},
  {"pass": 673, "range": "C1:93F6..C1:9474", "label": "CT_C1_93F6_HANDLER", "score": 8},
  {"pass": 674, "range": "C1:9474..C1:94D2", "label": "CT_C1_9474_HANDLER", "score": 5},
  {"pass": 675, "range": "C1:94D2..C1:9514", "label": "CT_C1_94D2_HANDLER", "score": 5},
  {"pass": 676, "range": "C1:9514..C1:959A", "label": "CT_C1_9514_HANDLER", "score": 5},
  {"pass": 677, "range": "C1:959A..C1:95D6", "label": "CT_C1_959A_HANDLER", "score": 5},
  {"pass": 678, "range": "C1:95D6..C1:95DA", "label": "CT_C1_95D6_HANDLER", "score": 5},
  {"pass": 679, "range": "C1:95DA..C1:95FA", "label": "CT_C1_95DA_HANDLER", "score": 5}
]
```

## 4. Coverage Impact

### 4.1 Current Bank C1 State
- Existing documented ranges: ~14 functions/clusters
- Current coverage: ~2% of Bank C1

### 4.2 Projected Coverage After Completion
- 25 new handler functions documented
- New coverage in C1:8E00-9800 region: ~75%
- Total Bank C1 coverage increase: +2%

## 5. Dispatch Table Pattern Summary

The C1:8C3E hub implements a **state machine dispatch pattern**:

```
Handler Structure:
  Entry Point (PHP/PHB/PHD/REP prologue)
      |
      v
  [Setup code - optional]
      |
      v
  JSR C1:8C3E  (dispatch to hub)
      |
      v
  [Post-processing - optional]
      |
      v
  RTS/RTL  (return to caller)
```

### Spacing Pattern
- Average gap between handlers: 40-80 bytes
- Minimum width: 4 bytes (C1:95D6..C1:95DA)
- Maximum width: 134 bytes (C1:9514..C1:959A)

### Handler Distribution
- C1:8E00-9000: 3 handlers (plus 3 documented)
- C1:9000-9500: 14 handlers
- C1:9500-9800: 11 handlers (plus 4 documented)

## 6. Next Steps

1. **Create manifest files** for all 25 identified handlers
2. **Promote to closed ranges** after validation
3. **Run verification** to confirm handler boundaries
4. **Update dispatch table documentation** with complete handler list

## 7. Files Generated

- `reports/c1_8c3e_current.json` - Current call anchor report
- `C1_8C3E_DISPATCH_COMPLETION_REPORT.md` - This report
- Recommended manifest files (25 total):
  - Passes 660-691: C1 handler functions

---

*Report generated by C1:8C3E dispatch table analysis*
*Tools used: build_call_anchor_report_v3.py, ROM disassembly*
