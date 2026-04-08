# Bank CF:D000-E000 Analysis Report

**Date:** 2026-04-08  
**Task:** Map Bank CF:D000-E000 (16 pages, 4096 bytes)  
**Status:** COMPLETE - 12 new function ranges identified and documented

---

## Executive Summary

Analyzed the previously unexplored CF:D000-E000 region using seam block scanning, backtrack analysis, code island detection, and data pattern classification. Found **12 high-confidence function ranges** with scores 3-8.

### Coverage Improvement

| Region | Before | After | Improvement |
|--------|--------|-------|-------------|
| CF:D000-DFFF | 232 bytes (5.7%) | 571 bytes (13.9%) | **+339 bytes (+8.2%)** |
| CF:E000-EFFF | 234 bytes (5.7%) | 234 bytes (5.7%) | No change |
| CF:F000-FFFF | 469 bytes (11.5%) | 469 bytes (11.5%) | No change |
| **CF Total** | **1062 bytes (1.62%)** | **1401 bytes (2.14%)** | **+339 bytes (+0.52%)** |

---

## Analysis Tools Used

1. **toolkit_doctor.py** - Verified toolkit health (100%)
2. **run_seam_block_v1.py** - Scanned CF:D000-E000 region
3. **score_target_owner_backtrack_v1.py** - Found 7 backtrack candidates (scores 2-4)
4. **find_local_code_islands_v2.py** - Identified 51 code islands, 22 clusters
5. **detect_data_patterns_v1.py** - Classified all regions as CODE_CANDIDATE

---

## Data vs Code Assessment

### Region Classification

| Region | Classification | Reason | Confidence |
|--------|----------------|--------|------------|
| CF:D000-D200 | CODE_CANDIDATE | RTS/RTL present, standard code region | High |
| CF:D200-D400 | CODE_CANDIDATE | High RTL density (9), many calls | High |
| CF:D400-D800 | CODE_CANDIDATE | High PHP/JSR density, score-10 cluster | High |
| CF:D800-DC00 | CODE_CANDIDATE | Mixed call patterns, score clusters | High |
| CF:DC00-E000 | CODE_CANDIDATE | PLP returns, balanced structure | High |

**No data regions identified** - The entire CF:D000-E000 range appears to be executable code.

---

## New Function Manifests (Pass 764-775)

### Score-8 Functions (1)

| Pass | Range | Label | Bytes | Score | Description |
|------|-------|-------|-------|-------|-------------|
| 765 | CF:DAF0..CF:DB2A | ct_cf_daf0_score8_cluster | 59 | 8 | 3 calls, 5 returns, 59-byte function group in DA00 region |

### Score-7 Functions (1)

| Pass | Range | Label | Bytes | Score | Description |
|------|-------|-------|-------|-------|-------------|
| 764 | CF:D5A7..CF:D5D6 | ct_cf_d5a7_score7_cluster | 48 | 7 | 6 calls, 4 returns, 48-byte function group in D500 region |

### Score-5 Functions (4)

| Pass | Range | Label | Bytes | Score | Description |
|------|-------|-------|-------|-------|-------------|
| 766 | CF:D7BC..CF:D7EA | ct_cf_d7bc_score5_cluster | 47 | 5 | 13 calls, 2 returns, stack operations in D700 region |
| 767 | CF:D8B9..CF:D8CA | ct_cf_d8b9_score5_cluster | 18 | 5 | 3 calls, 2 returns, 18-byte function in D800 region |
| 768 | CF:D0B0..CF:D0BA | ct_cf_d0b0_score5_cluster | 11 | 5 | 1 call, 3 returns, 11-byte entry function in D000 region |
| 769 | CF:D8DF..CF:D8EA | ct_cf_d8df_score5_cluster | 12 | 5 | 2 calls, 3 returns, 12-byte function in D800 region |

### Score-4 Functions (4)

| Pass | Range | Label | Bytes | Score | Description |
|------|-------|-------|-------|-------|-------------|
| 770 | CF:DE2C..CF:DE44 | ct_cf_de2c_score4_cluster | 25 | 4 | 2 calls, 1 return in DE00 region |
| 771 | CF:D5DD..CF:D5F6 | ct_cf_d5dd_score4_cluster | 26 | 4 | 4 calls, 3 returns in D500 region |
| 772 | CF:DC49..CF:DC61 | ct_cf_dc49_score4_cluster | 25 | 4 | 2 calls, 1 return, 3 branches in DC00 region |
| 773 | CF:DE47..CF:DE58 | ct_cf_de47_score4_cluster | 18 | 4 | 4 calls, 1 return, stackish ops in DE00 region |

### Score-3 High-Caller Functions (2)

| Pass | Range | Label | Bytes | Score | Description |
|------|-------|-------|-------|-------|-------------|
| 774 | CF:DDD2..CF:DDEA | ct_cf_ddd2_score3_cluster | 25 | 3 | **11 callers**, 1 return - high-caller utility in DD00 region |
| 775 | CF:DFD2..CF:DFEA | ct_cf_dfd2_score3_cluster | 25 | 3 | **11 callers**, 1 return - high-caller utility in DF00 region |

---

## Previously Mapped CF:D000-E000 Functions

| Pass | Range | Label | Bytes | Region |
|------|-------|-------|-------|--------|
| 710 | CF:D41E..CF:D47A | ct_cf_d41e_score10_cluster | 93 | D400 |
| 712 | CF:D284..CF:D2BE | ct_cf_d284_score8_cluster | 59 | D200 |
| 721 | CF:DA2F..CF:DA4D | ct_cf_da2f_c7_cross_bank | 31 | DA00 |
| 722 | CF:D3B0..CF:D3E0 | ct_cf_d3b0_score8_cluster | 49 | D300 |

---

## Key Findings

### 1. D200-DFFF Highest Density (Confirmed)
The D200-DFFF region contains the highest density of code functions:
- 10 of the 12 new functions are in this region
- Score-10 cluster at D41E (already mapped)
- Score-8 clusters at D284, D3B0 (already mapped)
- New score-7 cluster at D5A7

### 2. D000-D100 Is Code (Not Data)
Contrary to initial hypothesis, the D000-D100 region contains code:
- Score-5 function at D0B0..D0BA (11 bytes, 1 call, 3 returns)
- PHP prologue detected
- Standard code region classification

### 3. High-Caller Utilities at DD00 and DF00
Two new high-caller functions discovered:
- CF:DDD2..CF:DDEA with **11 callers**
- CF:DFD2..CF:DFEA with **11 callers**
These are likely shared utility functions called from multiple locations.

### 4. Connections to CF:E000+ Regions
The new D000-E000 functions show call patterns that may connect to:
- CF:E000-F000 (partially mapped, 5.7% coverage)
- CF:F000-FFFF (11.5% coverage, session 10)
Cross-bank analysis recommended for future sessions.

---

## Repeating Patterns Detected

| Pattern | Count | Region | Interpretation |
|---------|-------|--------|----------------|
| [1C 20 1C 20] | 73+ | D000-E000 | Common instruction sequence (TRB $201C or similar) |
| [53 2E 53 6E] | 4 | D100-D400 | Bit manipulation pattern |
| [53 AE 53 EE] | 4 | D100-D400 | Memory operation pattern |
| [D7 21 D7 61] | 4 | D800-DC00 | CMP indirect patterns |
| [D7 A1 D7 E1] | 4 | D800-DC00 | CMP indexed patterns |

---

## Files Created

### New Manifests (12)
- `passes/manifests/pass764.json` - CF:D5A7..CF:D5D6 (score-7)
- `passes/manifests/pass765.json` - CF:DAF0..CF:DB2A (score-8)
- `passes/manifests/pass766.json` - CF:D7BC..CF:D7EA (score-5)
- `passes/manifests/pass767.json` - CF:D8B9..CF:D8CA (score-5)
- `passes/manifests/pass768.json` - CF:D0B0..CF:D0BA (score-5)
- `passes/manifests/pass769.json` - CF:D8DF..CF:D8EA (score-5)
- `passes/manifests/pass770.json` - CF:DE2C..CF:DE44 (score-4)
- `passes/manifests/pass771.json` - CF:D5DD..CF:D5F6 (score-4)
- `passes/manifests/pass772.json` - CF:DC49..CF:DC61 (score-4)
- `passes/manifests/pass773.json` - CF:DE47..CF:DE58 (score-4)
- `passes/manifests/pass774.json` - CF:DDD2..CF:DDEA (score-3, 11 callers)
- `passes/manifests/pass775.json` - CF:DFD2..CF:DFEA (score-3, 11 callers)

### Report Files
- `reports/cf_d000_analysis_report.md` - This report

---

## Recommended Next Steps

1. **Cross-bank caller validation** for CF:D000-E000 functions
2. **Label file creation** for the 12 new functions
3. **CF:E000-F000 expansion** - Currently only 5.7% mapped
4. **Gap analysis** - Many small gaps exist between mapped functions
5. **Connection tracing** - Follow high-caller functions (11 callers each) to understand their role

---

## Statistics Summary

- **Functions identified:** 12
- **Bytes documented:** 339
- **CF:D000-DFFF coverage:** 13.9% (571/4096 bytes)
- **CF bank total coverage:** 2.14% (1401/65536 bytes)
- **Manifest pass range:** 764-775
- **Average function size:** 28.3 bytes
- **Total manifests in CF:** 28 (710-775)
