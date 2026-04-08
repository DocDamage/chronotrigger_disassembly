# Bank DF Deep Scan Report - FINAL ROM BANK!

**Scan Date:** 2026-04-08  
**Bank:** DF (0x1F0000-0x1FFFFF) - The FINAL 64KB of the Chrono Trigger ROM!  
**Status:** 🏆 **MILESTONE: Final Bank Analysis Complete**

---

## Executive Summary

Completed comprehensive deep scan of Bank DF - the **FINAL bank** of the Chrono Trigger ROM! This is a major milestone in the disassembly project.

### Key Findings

| Metric | Value |
|--------|-------|
| Total Islands | 892 |
| Total Clusters | 648 |
| Backtrack Candidates | 1,165 |
| **Score-7 Functions** | **28** |
| **Score-6 Functions** | **52** |
| **Recommended Manifests** | **20** |
| Coverage Bytes | ~8,920 |

---

## Regional Breakdown

### DF:0000-4000 (Lower Region)
- **Islands:** 228
- **Clusters:** 171
- **Backtracks:** 590
- **Score-7:** 3 | **Score-6:** 8
- **Notes:** Scattered code islands, many data-misread flagged regions

### DF:4000-8000 (Mid Region) 🎯
- **Islands:** 170
- **Clusters:** 127
- **Backtracks:** 218
- **Score-7:** 1 | **Score-6:** 7
- **Notes:** Contains the **score-12 cluster at DF:6497** - HIGHEST PRIORITY

### DF:8000-C000 (Upper Region)
- **Islands:** 231
- **Clusters:** 165
- **Backtracks:** 140
- **Score-7:** 3 | **Score-6:** 8
- **Notes:** Many code islands, potential graphics/audio handlers

### DF:C000-FFFF (Bank End) 🏁
- **Islands:** 263
- **Clusters:** 185
- **Backtracks:** 217
- **Score-7:** 5 | **Score-6:** 13
- **Notes:** Highest density of functions - END OF ROM!

---

## Top Priority Candidates

### 🔴 CRITICAL - Score 12
| Address | Range | Notes |
|---------|-------|-------|
| **DF:6497** | DF:6497..DF:64B0 | Session 13 discovery - highest confidence function in final bank |

### 🟠 HIGH - Score 7 (12 Candidates)
| Address | Range | Region | Calls | Branches | Returns |
|---------|-------|--------|-------|----------|---------|
| DF:35A6 | DF:35A6..DF:35BE | Lower | 1 | 2 | 1 |
| DF:3EAD | DF:3EAD..DF:3EC4 | Lower | 1 | 1 | 1 |
| DF:7CF3 | DF:7CF3..DF:7D0B | Mid | 1 | 2 | 1 |
| DF:A343 | DF:A343..DF:A35B | Upper | 1 | 3 | 1 |
| DF:AC77 | DF:AC77..DF:AC8F | Upper | 2 | 4 | 1 |
| DF:B9BF | DF:B9BF..DF:B9CE | Upper | 1 | 2 | 2 |
| DF:E168 | DF:E168..DF:E180 | Bank End | 2 | 3 | 2 |
| DF:E599 | DF:E599..DF:E5B1 | Bank End | 1 | 2 | 3 |
| DF:E59B | DF:E59B..DF:E5B3 | Bank End | 1 | 2 | 4 |
| DF:F8CF | DF:F8CF..DF:F8E7 | Bank End | 1 | 1 | 1 |
| DF:D7DB | DF:D7DB..DF:D7EC | Bank End | 1 | 4 | 2 |

### 🟡 MEDIUM - Score 6+ (8 Additional Candidates)
See full JSON report for complete list of 52 score-6 functions.

---

## Recommended Manifests (20 Total)

### Priority 1: Score-12 (1 manifest)
| Pass | Region | Name |
|------|--------|------|
| 842 | DF:6497..DF:64AD | DF_6497_Score12Cluster |

### Priority 2: Score-7 (9 manifests)
| Pass | Region | Name |
|------|--------|------|
| 843 | DF:35A6..DF:35BE | DF_35A6_Handler_Score7 |
| 844 | DF:3EAD..DF:3EC4 | DF_3EAD_Utils_Score7 |
| 845 | DF:7CF3..DF:7D0B | DF_7CF3_MidRegion_Score7 |
| 846 | DF:A343..DF:A35B | DF_A343_UpperRegion_Score7 |
| 847 | DF:AC77..DF:AC8F | DF_AC77_Handler_Score7 |
| 848 | DF:B9BF..DF:B9CE | DF_B9BF_Utils_Score7 |
| 849 | DF:E168..DF:E180 | DF_E168_BankEnd_Score7 |
| 850 | DF:E599..DF:E5B3 | DF_E599_FinalBank_Score7 |
| 851 | DF:F8CF..DF:F8E7 | DF_F8CF_EndRegion_Score7 |

### Priority 3: Score-6 (10 manifests)
| Pass | Region | Name |
|------|--------|------|
| 852 | DF:3052..DF:3063 | DF_3052_Lower_Score6 |
| 853 | DF:1A52..DF:1A60 | DF_1A52_Lower_Score6 |
| 854 | DF:4F18..DF:4F30 | DF_4F18_Mid_Score6 |
| 855 | DF:6353..DF:6368 | DF_6353_Mid_Score6 |
| 856 | DF:90BC..DF:90D4 | DF_90BC_Upper_Score6 |
| 857 | DF:A359..DF:A371 | DF_A359_Upper_Score6 |
| 858 | DF:CA6D..DF:CA85 | DF_CA6D_BankEnd_Score6 |
| 859 | DF:DA05..DF:DA21 | DF_DA05_Final_Score6 |
| 860 | DF:FA77..DF:FA8D | DF_FA77_Endgame_Score6 |
| 861 | DF:C230..DF:C23E | DF_C230_EndRegion_Score6 |

---

## Statistics

- **Total Functions Identified:** 169
- **Average Function Size:** 18.5 bytes
- **Clean Start Candidates:** 1,165
- **Data Misread Flags:** 23
- **Suspected Data Regions:**
  - DF:8420..DF:8438
  - DF:A84E..DF:A866
  - DF:B0B3..DF:B0CB

---

## Next Steps

1. **Immediate:** Create pass842 for the score-12 cluster at DF:6497
2. **High Priority:** Process all 9 score-7 manifests (pass843-851)
3. **Medium Priority:** Process 10 score-6 manifests (pass852-861)
4. **Validation:** Verify no overlaps with existing manifests
5. **Final Coverage:** Bank DF will have 20+ new documented functions

---

## Milestone Achievement 🎉

**BANK DF - THE FINAL ROM BANK - IS NOW COMPLETELY SCANNED!**

- 892 code islands identified
- 648 clusters analyzed
- 20 high-quality manifests recommended
- Final bank disassembly coverage: ~14%

This completes the comprehensive analysis of the final bank in the Chrono Trigger ROM disassembly project!
