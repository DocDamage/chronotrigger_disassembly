# Bank C2 Expansion - Session 28 Final Report

**Date:** 2026-04-08  
**Session:** 28  
**Bank:** C2  
**Goal:** Expand disassembly to new regions, push coverage toward 7-8%

---

## Executive Summary

Successfully scanned **6 new regions** in Bank C2, discovering **237 code islands** and **190 clusters**. Created **11 new manifests** for high-value score-6+ candidates.

**Coverage Impact:**
- Previous: ~6.2%
- New manifests add: +0.32%
- Current estimated: ~6.5%
- New bytes documented: 209 bytes

---

## Regions Explored

| Region | Islands | Clusters | Score-6+ | Status |
|--------|---------|----------|----------|--------|
| C2:0000-1000 | 50 | 42 | 9 | Vector table area - rich with handlers |
| C2:2000-3000 | 24 | 20 | 1 | Mid region - moderate code density |
| C2:3000-4000 | 34 | 29 | 1 | Mid region - scattered islands |
| C2:6000-7000 | 54 | 35 | 8 | Extension of rich 5000-6000 region |
| C2:7000-8000 | 31 | 27 | 5 | Upper region - moderate density |
| C2:9000-A000 | 44 | 37 | 4 | Upper region - call-rich area |
| **TOTAL** | **237** | **190** | **28** | 6 new regions mapped |

---

## Manifests Created (Session 28)

| Pass | Range | Score | Width | Calls | Region | Label |
|------|-------|-------|-------|-------|--------|-------|
| 1083 | C2:0686-C2:069E | 6 | 25 | 4 | 0000-1000 | ct_c2_0686_vector_helper |
| 1084 | C2:2DDA-C2:2DE9 | 7 | 16 | 1 | 2000-3000 | ct_c2_2dda_mid_handler |
| 1085 | C2:3442-C2:3448 | 6 | 7 | 1 | 3000-4000 | ct_c2_3442_compact_fn |
| 1086 | C2:6444-C2:6452 | 7 | 15 | 2 | 6000-7000 | ct_c2_6444_sub_handler |
| 1087 | C2:7B27-C2:7B30 | 7 | 10 | 1 | 7000-8000 | ct_c2_7b27_tiny_vector |
| 1088 | C2:749D-C2:74AD | 6 | 17 | 1 | 7000-8000 | ct_c2_749d_mode_routine |
| 1089 | C2:785B-C2:786E | 6 | 20 | 1 | 7000-8000 | ct_c2_785b_data_handler |
| 1090 | C2:9F1C-C2:9F49 | 7 | 46 | 4 | 9000-A000 | ct_c2_9f1c_complex_hub |
| 1091 | C2:925C-C2:926D | 6 | 18 | 3 | 9000-A000 | ct_c2_925c_jsr_target |
| 1092 | C2:6221-C2:6232 | 6 | 18 | 1 | 6000-7000 | ct_c2_6221_multi_return |
| 1093 | C2:68D3-C2:68E3 | 6 | 17 | 3 | 6000-7000 | ct_c2_68d3_call_hub |

**Totals:**
- 11 manifests created
- 209 bytes of new coverage
- 22 call sites documented
- Average score: 6.4

---

## Key Discoveries

### 1. Vector Table Area (0000-1000)
- **C2:0686**: Score-6 helper with 4 calls, located near vector table
- High density of initialization and handler routines
- Cross-bank caller candidates identified

### 2. 6000-7000 Region Extension
- **C2:6221**: Multi-exit function with 3 returns (exception handler pattern)
- **C2:6444**: Score-7 subroutine with 2 calls
- **C2:68D3**: Call hub dispatching to 3 child functions
- Natural extension of rich 5000-6000 code region

### 3. 9000-A000 Region
- **C2:9F1C**: Score-7 mega-cluster (46 bytes, 4 calls, 5 branches)
- **C2:925C**: JSR-targeted subroutine with 3 internal calls
- Call-rich area with complex hub functions

---

## Coverage Analysis

| Metric | Before S28 | After S28 | Change |
|--------|------------|-----------|--------|
| Total Manifests | 59 | 70 | +11 |
| Coverage | ~6.2% | ~6.5% | +0.32% |
| Score-6+ Functions | 15 | ~25 | +10 |
| Regions Mapped | 1 (5000-6000) | 7 (+6 new) | +6 |

---

## Dispatch Patterns Identified

### Multi-Return Functions
- **C2:6221**: 3 returns (exception handler pattern)
- **C2:785B**: 2 returns (data-dependent exit)
- **C2:9F1C**: 2 returns (complex hub)

### Call Hubs
- **C2:68D3**: 3 calls in 17 bytes
- **C2:9F1C**: 4 calls in 46 bytes
- **C2:925C**: 3 calls in 18 bytes

### Cross-Bank Caller Candidates
- C2:0686 (4 calls) - likely called from multiple banks
- C2:2DDA (clean entry) - exported function pattern

---

## Validation Results

✓ All 11 manifests validated  
✓ No address conflicts detected  
✓ All ranges unique and non-overlapping  
✓ Pass numbers sequential (1083-1093)

---

## Files Created

### Manifests
```
passes/manifests/pass_1083_c2_0686.yaml
passes/manifests/pass_1084_c2_2dda.yaml
passes/manifests/pass_1085_c2_3442.yaml
passes/manifests/pass_1086_c2_6444.yaml
passes/manifests/pass_1087_c2_7b27.yaml
passes/manifests/pass_1088_c2_749d.yaml
passes/manifests/pass_1089_c2_785b.yaml
passes/manifests/pass_1090_c2_9f1c.yaml
passes/manifests/pass_1091_c2_925c.yaml
passes/manifests/pass_1092_c2_6221.yaml
passes/manifests/pass_1093_c2_68d3.yaml
```

### Reports
- `C2_SESSION_28_REPORT.md` - Detailed scan results
- `C2_SESSION_28_FINAL_REPORT.md` - This file

### Data
- `c2_session28_scan.json` - Full scan data for all 6 regions
- `validate_session28.py` - Validation script
- `scan_c2_regions.py` - Region scanning script

---

## Next Steps

### To Reach 7-8% Coverage:
1. **Create 10-15 more manifests** from remaining score-6 candidates:
   - C2:0465, C2:0483, C2:049E, C2:04D7 (0000 region)
   - C2:7191, C2:71BE (7000 region)
   - Additional candidates from 6000-7000 region

2. **Explore remaining regions:**
   - C2:A000-B000 (partial)
   - C2:B000-C000 (Bxxx manifests exist, check gaps)
   - C2:C000-D000
   - C2:D000-E000
   - C2:E000-FFFF

3. **Cross-bank analysis:**
   - Build caller graphs for new functions
   - Identify dispatch patterns
   - Map cross-bank call chains

---

*Session 28 complete. 11 manifests created, 6 new regions mapped, coverage expanded to ~6.5%.*
