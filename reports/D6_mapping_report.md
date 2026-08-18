# Bank D6 Mapping Report

**Date:** 2026-04-08  
**ROM:** Chrono Trigger (USA).sfc  
**Bank:** D6 (SNES HiROM)

---

## Executive Summary

Bank D6 has **49 cross-bank callers** (highest in ROM!) and significant unmapped regions. This analysis identified **69 score-6+ code clusters** suitable for manifest creation, with **15 high-priority recommendations** targeting the 12-15 new function goal.

---

## Current State

### Existing Manifests (10 passes)
| Pass | Range | Label | Score |
|------|-------|-------|-------|
| pass785 | D6:68FB-692F | ct_d6_68fb_score8_cluster | 8 |
| pass806 | D6:6165-6186 | ct_d6_6165_score6_cluster | 6 |
| pass807 | D6:68D3-68F0 | ct_d6_68d3_score6_cluster | 6 |
| pass808 | D6:6C2D-6C48 | ct_d6_6c2d_php_prologue | - |
| pass809 | D6:763A-7660 | ct_d6_763a_rep_handler | - |
| pass822 | D6:62B0-62CD | ct_d6_62b0_score6_cluster | 6 |
| pass823 | D6:6404-641D | ct_d6_6404_score6_cluster | 6 |
| pass824 | D6:7BFE-7C1F | ct_d6_7bfe_score6_cluster | 6 |
| pass831 | D6:72EF-7314 | ct_d6_72ef_phx_handler | - |
| pass832 | D6:7EEF-7F0B | ct_d6_7eef_score6_cluster | 6 |

### Coverage Status
- **D6:0000-6000**: ❌ Unmapped (24KB - largest gap!)
- **D6:6000-7000**: ⚠️ Partially mapped (pass806, 822-823 around 62B0-641D)
- **D6:7000-8000**: ⚠️ Partially mapped (pass809, 824, 831-832)
- **D6:8000-C000**: ❌ Unmapped (16KB)
- **D6:C000-FFFF**: ❌ Unmapped (16KB)

---

## Score-6+ Cluster Analysis

### Top Candidates by Score

#### Score 10 (Highest Priority)
| # | Range | Region | Size | Calls | Returns | Notes |
|---|-------|--------|------|-------|---------|-------|
| 1 | D6:BE65-BE8A | D6:8000-C000 | 38B | 3 | 4 | Multi-child cluster, no flags |

#### Score 9
| # | Range | Region | Size | Calls | Returns | Notes |
|---|-------|--------|------|-------|---------|-------|
| 2 | D6:973F-976A | D6:8000-C000 | 44B | 1 | 3 | Large function, no flags |

#### Score 8
| # | Range | Region | Size | Calls | Returns | Notes |
|---|-------|--------|------|-------|---------|-------|
| 3 | D6:15DB-15FA | D6:0000-6000 | 32B | 2 | 4 | Well-formed subroutine |
| 4 | D6:2532-2579 | D6:0000-6000 | 72B | 4 | 9 | Large multi-exit function |
| 5 | D6:3AF0-3B1E | D6:0000-6000 | 47B | 1 | 6 | Complex branch structure |
| 6 | D6:5979-5998 | D6:0000-6000 | 32B | 3 | 4 | Multiple callers |
| 7 | D6:D47B-D4A4 | D6:C000-FFFF | 42B | 1 | 4 | Late bank function |
| 8 | D6:D94C-D96A | D6:C000-FFFF | 31B | 2 | 5 | Multiple exits |

#### Score 7 (Selected Top Candidates)
| # | Range | Region | Size | Calls | Returns | Notes |
|---|-------|--------|------|-------|---------|-------|
| 9 | D6:0CD8-0CF0 | D6:0000-6000 | 25B | 1 | 3 | Clean subroutine |
| 10 | D6:0D7E-0D93 | D6:0000-6000 | 22B | 1 | 1 | Single-entry, single-exit |
| 11 | D6:3C35-3C4D | D6:0000-6000 | 25B | 1 | 1 | Prologue pattern |
| 12 | D6:7647-765F | D6:7000-8000 | 25B | 2 | 1 | Near existing pass809 |
| 13 | D6:8BC8-8BE0 | D6:8000-C000 | 25B | 2 | 1 | Upper bank function |
| 14 | D6:A412-A433 | D6:8000-C000 | 34B | 1 | 3 | Medium-size function |
| 15 | D6:B384-B3A1 | D6:8000-C000 | 30B | 3 | 3 | Multiple callers |

---

## Cross-Bank Caller Analysis

### Top Entry Points by Reference Count

| Entry Point | References | Region | Priority |
|-------------|------------|--------|----------|
| D6:002A | 8 | D6:0000-6000 | **HIGH** |
| D6:00E0 | 4 | D6:0000-6000 | **HIGH** |
| D6:102B | 4 | D6:0000-6000 | **HIGH** |
| D6:20DD | 4 | D6:0000-6000 | **HIGH** |
| D6:C0EF | 4 | D6:C000-FFFF | **HIGH** |
| D6:0705 | 3 | D6:0000-6000 | Medium |
| D6:0C07 | 3 | D6:0000-6000 | Medium |
| D6:1013 | 3 | D6:0000-6000 | Medium |
| D6:304F | 3 | D6:0000-6000 | Medium |
| D6:400D | 3 | D6:0000-6000 | Medium |

**Total unique high-score entry points:** 159  
**Total caller candidates analyzed:** 1,245

---

## Recommended Manifests (15 New Functions)

### Tier 1: Highest Priority (Score 8-10, Cross-Bank Callers)
```json
// passXXX.json - Score 10 cluster
{"range": "D6:BE65..D6:BE8A", "label": "ct_d6_be65_score10_handler", "confidence": "high"}

// passXXX.json - Score 9 cluster  
{"range": "D6:973F..D6:976A", "label": "ct_d6_973f_score9_handler", "confidence": "high"}

// passXXX.json - Cross-bank entry point (8 refs)
{"range": "D6:002A..D6:0043", "label": "ct_d6_002a_entry_8callers", "confidence": "medium"}
```

### Tier 2: High Priority (Score 7-8)
```json
// passXXX.json - D6:0000-6000 region
{"range": "D6:15DB..D6:15FA", "label": "ct_d6_15db_score8_handler", "confidence": "high"}
{"range": "D6:3AF0..D6:3B1E", "label": "ct_d6_3af0_score8_handler", "confidence": "high"}
{"range": "D6:0CD8..D6:0CF0", "label": "ct_d6_0cd8_score7_handler", "confidence": "medium"}
{"range": "D6:3C35..D6:3C4D", "label": "ct_d6_3c35_score7_handler", "confidence": "medium"}

// passXXX.json - D6:7000-8000 region
{"range": "D6:7647..D6:765F", "label": "ct_d6_7647_score7_handler", "confidence": "medium"}

// passXXX.json - D6:C000-FFFF region  
{"range": "D6:D47B..D6:D4A4", "label": "ct_d6_d47b_score8_handler", "confidence": "high"}
{"range": "D6:D94C..D6:D96A", "label": "ct_d6_d94c_score8_handler", "confidence": "high"}
```

### Tier 3: Medium Priority (Score 6, Fill Gaps)
```json
// passXXX.json - Additional D6:0000-6000
{"range": "D6:2532..D6:2579", "label": "ct_d6_2532_score8_multiexit", "confidence": "high"}
{"range": "D6:5979..D6:5998", "label": "ct_d6_5979_score8_handler", "confidence": "high"}
{"range": "D6:0D7E..D6:0D93", "label": "ct_d6_0d7e_score7_handler", "confidence": "medium"}

// passXXX.json - D6:8000-C000
{"range": "D6:8BC8..D6:8BE0", "label": "ct_d6_8bc8_score7_handler", "confidence": "medium"}
{"range": "D6:A412..D6:A433", "label": "ct_d6_a412_score7_handler", "confidence": "medium"}
{"range": "D6:B384..D6:B3A1", "label": "ct_d6_b384_score7_handler", "confidence": "medium"}
```

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Clusters Analyzed | 661 |
| Score 6+ Clusters | 69 |
| Score 7+ Clusters | 22 |
| Score 8+ Clusters | 8 |
| Score 9+ Clusters | 2 |
| Score 10 Clusters | 1 |
| Cross-Bank Entry Points | 159 |
| Recommended New Manifests | 15 |
| Existing Manifests | 10 |
| **Total Coverage Target** | **25** |

---

## Next Steps

1. **Create Tier 1 manifests** (3 functions) - Highest impact
2. **Create Tier 2 manifests** (8 functions) - Strong confidence
3. **Create Tier 3 manifests** (4 functions) - Fill remaining gaps
4. **Verify boundaries** against cross-bank caller sources
5. **Generate label files** for all new manifests

---

## Files Generated

- `reports/D6_0000_6000_islands.json` - Lower bank analysis
- `reports/D6_7000_8000_islands.json` - 7000 region analysis
- `reports/D6_8000_C000_islands.json` - Upper region analysis
- `reports/D6_C000_FFFF_islands.json` - Bank end analysis
- `reports/D6_0000_6000_callers.json` - Cross-bank caller analysis
- `reports/D6_7000_8000_callers.json` - Cross-bank caller analysis
- `reports/D6_8000_C000_callers.json` - Cross-bank caller analysis
- `reports/D6_C000_FFFF_callers.json` - Cross-bank caller analysis
- `reports/analyze_d6.py` - Analysis script
- `reports/D6_mapping_report.md` - This report
