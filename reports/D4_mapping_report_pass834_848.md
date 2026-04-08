# Bank D4 Mapping Report - Pass 834-848

## Scan Summary
Completed mapping of remaining Bank D4 regions:
- **D4:0000-4000** (lower bank): 357 islands, 201 clusters
- **D4:6000-8000** (mid-upper): 179 islands, 80 clusters  
- **D4:8000-C000** (upper): 122 islands, 98 clusters
- **D4:C000-FFFF** (bank end): 133 islands, 104 clusters

## Score-9 Reference (Previously Mapped)
| Range | Score | Size | Pass |
|-------|-------|------|------|
| D4:45BB-45EB | 9 | 49 bytes | 786 |

## New Score-7+ Candidates (15 Functions)

### Score-8 (Highest in remaining regions)
| Range | Score | Size | Region | Manifest |
|-------|-------|------|--------|----------|
| D4:F1CC-F1EC | 8 | 33 bytes | C000-FFFF | **pass834** |

### Score-7 (High Confidence)
| Range | Score | Size | Region | Calls | Branches | Manifest |
|-------|-------|------|--------|-------|----------|----------|
| D4:F257-F26F | 7 | 25 bytes | C000-FFFF | 1 | 7 | **pass835** |
| D4:FE52-FE5D | 7 | 12 bytes | C000-FFFF | 1 | 3 | **pass836** |
| D4:0036-004E | 7 | 25 bytes | 0000-4000 | 1 | 6 | **pass837** |
| D4:02B6-02CE | 7 | 25 bytes | 0000-4000 | 2 | 8 | **pass838** |
| D4:1A8D-1AA5 | 7 | 25 bytes | 0000-4000 | 1 | 6 | **pass839** |
| D4:69B4-69CC | 7 | 25 bytes | 6000-8000 | 2 | 1 | **pass840** |
| D4:6A6D-6A85 | 7 | 25 bytes | 6000-8000 | 1 | 4 | **pass841** |
| D4:778C-77A2 | 7 | 23 bytes | 6000-8000 | 3 | 3 | **pass842** |

### Score-6 (Good Confidence)
| Range | Score | Size | Region | Calls | Branches | Manifest |
|-------|-------|------|--------|-------|----------|----------|
| D4:6EF6-6F0E | 6 | 25 bytes | 6000-8000 | 4 | 5 | **pass843** |
| D4:76EE-7706 | 6 | 25 bytes | 6000-8000 | 2 | 6 | **pass844** |
| D4:A442-A457 | 6 | 22 bytes | 8000-C000 | 2 | 6 | **pass845** |
| D4:B408-B40E | 6 | 7 bytes | 8000-C000 | 1 | 0 | **pass846** |
| D4:FAF0-FAF8 | 6 | 9 bytes | C000-FFFF | 1 | 2 | **pass847** |
| D4:7BC9-7BDE | 6 | 22 bytes | 6000-8000 | 1 | 2 | **pass848** |

## Region Summary

### D4:0000-4000 (Lower Bank)
- **Total islands scanned**: 357
- **Total clusters**: 201
- **Score-7 candidates**: 3 (pass837, pass838, pass839)
- **Score-6 candidates**: 4 (not promoted - lower priority)
- **Primary characteristics**: Handler functions, early bank code

### D4:6000-8000 (Mid-Upper)
- **Total islands scanned**: 179
- **Total clusters**: 80
- **Score-7 candidates**: 3 (pass840, pass841, pass842)
- **Score-6 candidates**: 3 (pass843, pass844, pass848)
- **Primary characteristics**: Stack-heavy operations, JSL handlers

### D4:8000-C000 (Upper)
- **Total islands scanned**: 122
- **Total clusters**: 98
- **Score-7 candidates**: 0
- **Score-6 candidates**: 2 (pass845, pass846)
- **Primary characteristics**: Mixed code/data regions

### D4:C000-FFFF (Bank End)
- **Total islands scanned**: 133
- **Total clusters**: 104
- **Score-8 candidates**: 1 (pass834) - **HIGHEST**
- **Score-7 candidates**: 2 (pass835, pass836)
- **Score-6 candidates**: 1 (pass847)
- **Primary characteristics**: Return-heavy handlers, multi-call functions

## Manifests Created
| Pass | Range | Label | Score |
|------|-------|-------|-------|
| 834 | D4:F1CC-F1EC | ct_d4_f1cc_score8_cluster | 8 |
| 835 | D4:F257-F26F | ct_d4_f257_score7_handler | 7 |
| 836 | D4:FE52-FE5D | ct_d4_fe52_score7_handler | 7 |
| 837 | D4:0036-004E | ct_d4_0036_score7_handler | 7 |
| 838 | D4:02B6-02CE | ct_d4_02b6_score7_handler | 7 |
| 839 | D4:1A8D-1AA5 | ct_d4_1a8d_score7_handler | 7 |
| 840 | D4:69B4-69CC | ct_d4_69b4_score7_handler | 7 |
| 841 | D4:6A6D-6A85 | ct_d4_6a6d_score7_handler | 7 |
| 842 | D4:778C-77A2 | ct_d4_778c_score7_handler | 7 |
| 843 | D4:6EF6-6F0E | ct_d4_6ef6_score6_handler | 6 |
| 844 | D4:76EE-7706 | ct_d4_76ee_score6_handler | 6 |
| 845 | D4:A442-A457 | ct_d4_a442_score6_handler | 6 |
| 846 | D4:B408-B40E | ct_d4_b408_score6_handler | 6 |
| 847 | D4:FAF0-FAF8 | ct_d4_faf0_score6_handler | 6 |
| 848 | D4:7BC9-7BDE | ct_d4_7bc9_score6_handler | 6 |

## Statistics
- **Total new functions mapped**: 15
- **Score-8**: 1 (6.7%)
- **Score-7**: 8 (53.3%)
- **Score-6**: 6 (40.0%)
- **Total bytes mapped**: ~328 bytes
- **Cross-bank caller context**: 36 callers identified in D2-D9

## Notes
- D4:F1CC-F1EC (pass834) is the **highest scoring cluster** in the C000-FFFF region
- D4:45BB-45EB (pass786) remains the **highest overall in D4** (score-9)
- Lower bank (0000-4000) shows moderate code density with score-7 peaks
- Mid-upper region (6000-8000) has strong handler functions
- Bank end (C000-FFFF) contains the most complex multi-return handlers

## Validation
All manifests validated against:
- Return instruction presence
- Clean ASCII ratios (< 0.30 for score-7+)
- No data misread flags
- Cross-bank caller references verified
