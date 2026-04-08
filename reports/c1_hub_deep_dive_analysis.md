# Bank C1 Hub Function Deep Dive Analysis

**Date:** 2026-04-08  
**Analyzed Regions:**
- C1:1700-1800 (Dispatch Hub)
- C1:1B00-1C00 (Utility Hub)  
- C1:4A00-4B00 (Library Hub)

## Executive Summary

Analyzed three major hub functions in Bank C1 with 20+ callers each:
- **C1:179C** - 25 callers (dispatch hub)
- **C1:1B55** - 29 callers (utility hub)
- **C1:4AEB** - 27 callers (library hub)

**Results:** Identified **10 functions** totaling **243 bytes** for promotion (passes 579-588).

---

## Region 1: C1:1700-1800 - Dispatch Hub

### Hub Function: C1:179C (25 callers)
**Analysis:** Primary dispatch hub reached via JMP instructions from 25 locations.

| Address | Function | Bytes | Callers | Confidence |
|---------|----------|-------|---------|------------|
| C1:179C..17A0 | ct_c1_179c_dispatch_hub | 5 | 25 | HIGH |
| C1:178E..17A0 | ct_c1_178e_dispatch_prologue | 19 | 0 | HIGH |
| C1:17A5..17BE | ct_c1_17a5_dispatch_handler_dec | 26 | 0 | MEDIUM |
| C1:17BC..17DC | ct_c1_17bc_dispatch_handler_inc | 33 | 0 | MEDIUM |

**Code Pattern:**
- C1:179C: `64 EE 64 EF 60` (STZ $EE / STZ $EF / RTS) - 5 byte hub
- All 25 callers use JMP to reach this hub
- Handler functions at C1:17A5 and C1:17BC are score-6 candidates

**Call Graph Context:**
```
25 callers (C1:11xx-C1:17xx) → JMP C1:179C (dispatch_hub)
                              → C1:17A5 (handler_dec)
                              → C1:17BC (handler_inc)
```

---

## Region 2: C1:1B00-1C00 - Utility Hub

### Hub Function: C1:1B55 (29 callers)
**Analysis:** Primary utility hub reached via JSR from 29 locations.

| Address | Function | Bytes | Callers | Confidence |
|---------|----------|-------|---------|------------|
| C1:1B55..1B66 | ct_c1_1b55_utility_hub | 18 | 29 | HIGH |
| C1:1B06..1B18 | ct_c1_1b06_utility_prologue | 19 | 0 | HIGH |
| C1:1B9B..1BAB | ct_c1_1b9b_utility_handler | 17 | 0 | MEDIUM |

**Code Pattern:**
- C1:1B55: `9C 01 1E A9 19 8D 00 1E A9 80 8D 02 1E 22 04 00 C7 60`
  - STZ $1E01 / LDA #$19 / STA $1E00 / LDA #$80 / STA $1E02 / JSL $C7:0004 / RTS
- Makes long call to C7:0004 (common utility)

**Call Graph Context:**
```
29 callers (C1:11xx-C1:23xx) → JSR C1:1B55 (utility_hub)
                              → JSL C7:0004
```

---

## Region 3: C1:4A00-4B00 - Library Hub

### Hub Function: C1:4AEB (27 callers)
**Analysis:** Library hub for array/table processing operations.

| Address | Function | Bytes | Callers | Confidence |
|---------|----------|-------|---------|------------|
| C1:4AEB..4B17 | ct_c1_4aeb_library_hub | 45 | 27 | HIGH |
| C1:4A6B..4A70 | ct_c1_4a6b_library_init | 6 | 0 | MEDIUM |
| C1:4A71..4AA7 | ct_c1_4a71_library_calc_xy | 55 | 0 | MEDIUM |

**Code Pattern:**
- C1:4A6B: `A9 01 8D 30 99 60` (LDA #$01 / STA $9930 / RTS) - Init stub
- C1:4A71: `7B AA A8 E8 86 94 E2 10...` (TDC/TAX/TAY/INX) - X/Y calc
- C1:4AEB: Array processing with `BD FD 7C` (LDA $7CFD,X) patterns

**Call Graph Context:**
```
27 callers (C1:8xxx-C1:Exxx) → JSR C1:4AEB (library_hub)
                              → Table processing at $7CFD
```

---

## Manifests Created

| Pass | Range | Label | Bytes |
|------|-------|-------|-------|
| 579 | C1:179C..C1:17A0 | ct_c1_179c_dispatch_hub | 5 |
| 580 | C1:178E..C1:17A0 | ct_c1_178e_dispatch_prologue | 19 |
| 581 | C1:17A5..C1:17BE | ct_c1_17a5_dispatch_handler_dec | 26 |
| 582 | C1:17BC..C1:17DC | ct_c1_17bc_dispatch_handler_inc | 33 |
| 583 | C1:1B55..C1:1B66 | ct_c1_1b55_utility_hub | 18 |
| 584 | C1:1B06..C1:1B18 | ct_c1_1b06_utility_prologue | 19 |
| 585 | C1:1B9B..C1:1BAB | ct_c1_1b9b_utility_handler | 17 |
| 586 | C1:4AEB..C1:4B17 | ct_c1_4aeb_library_hub | 45 |
| 587 | C1:4A6B..C1:4A70 | ct_c1_4a6b_library_init | 6 |
| 588 | C1:4A71..C1:4AA7 | ct_c1_4a71_library_calc_xy | 55 |

**Total: 10 functions, 243 bytes**

---

## Hub Function Analysis

### What These Hubs Do

**C1:179C Dispatch Hub:**
- Minimal 5-byte dispatcher: clears $EE/$EF and returns
- 25 callers jump here via JMP (not JSR)
- Likely a cleanup/exit path for a larger dispatch system
- Handler functions at C1:17A5 and C1:17BC handle increment/decrement operations

**C1:1B55 Utility Hub:**
- DMA/setup utility function
- Configures registers at $1E00-$1E02
- Calls C7:0004 (common system utility)
- 29 callers from throughout C1 bank

**C1:4AEB Library Hub:**
- Array/table processing library
- Works with tables at $7CFD and $7DFD
- X/Y coordinate calculations nearby at C1:4A71
- 27 callers from high addresses in C1 (C1:8xxx-C1:Exxx)

---

## Coverage Impact

**Before:** C1 coverage: 3 ranges, 386 bytes (0.59%)

**After adding these 10 functions:**
- Additional 243 bytes mapped
- Total C1 coverage: ~629 bytes (~1.0%)
- Three major hub systems now documented

---

## Files Created

- `passes/manifests/pass579.json` through `pass588.json`
- `reports/c1_hub_deep_dive_analysis.md` (this file)

---

## Next Steps

1. Validate manifests with `python tools/scripts/check_pass_manifest.py`
2. Look for additional score-6+ candidates in gaps:
   - C1:17DC..1B06 (gap between dispatch and utility regions)
   - C1:1BAB..4A6B (large gap with potential candidates)
3. Continue scanning C1:0000-1700 and C1:4C00-FFFF for more hub functions
