# Bank C2 Expansion - Session 29 Report

**Date:** 2026-04-08  
**Session:** 29  
**Bank:** C2  
**Goal:** Continue expansion toward 8% coverage

---

## Executive Summary

Successfully created **12 new manifests** covering **1,002 bytes** across 6 target regions.  
All manifests validated with no overlaps.

**Coverage Impact:**
- Previous: ~6.5%
- New manifests add: +0.41%
- Current estimated: ~6.9%

---

## Regions Explored

| Region | Manifests | Bytes | Status |
|--------|-----------|-------|--------|
| C2:0000-1000 | 3 | 59 | Vector area - initialization helpers |
| C2:1000-2000 | 1 | 151 | Post-vector handlers |
| C2:5000-6000 | 3 | 394 | Rich region continuation |
| C2:8000-9000 | 2 | 278 | Hub area expansion |
| C2:9000-A000 | 1 | 66 | Beyond 9F1C hub network |
| C2:B000-C000 | 2 | 54 | Bank-end helpers |
| **TOTAL** | **12** | **1,002** | 6 regions covered |

---

## Manifests Created (Session 29)

| Pass | Range | Score | Bytes | Calls | Region | Label |
|------|-------|-------|-------|-------|--------|-------|
| 1100 | C2:0465-C2:0477 | 6 | 18 | 2 | 0000-1000 | ct_c2_0465_vector_handler_s29 |
| 1101 | C2:04D7-C2:04E8 | 6 | 17 | 1 | 0000-1000 | ct_c2_04d7_init_helper_s29 |
| 1102 | C2:0582-C2:059A | 6 | 24 | 3 | 0000-1000 | ct_c2_0582_system_handler_s29 |
| 1103 | C2:8006-C2:8090 | 6 | 138 | 6 | 8000-9000 | ct_c2_8006_hub_entry_s29 |
| 1104 | C2:8249-C2:82D5 | 6 | 140 | 4 | 8000-9000 | ct_c2_8249_sweep_service_s29 |
| 1105 | C2:5319-C2:539D | 6 | 132 | 5 | 5000-6000 | ct_c2_5319_rich_subroutine_s29 |
| 1106 | C2:BFE6-C2:BFFE | **7** | 24 | 2 | B000-C000 | ct_c2_bfe6_bank_end_handler_s29 |
| 1107 | C2:BDF7-C2:BE15 | 6 | 30 | 2 | B000-C000 | ct_c2_bdf7_be00_service_s29 |
| 1108 | C2:1011-C2:10A8 | 6 | 151 | 5 | 1000-2000 | ct_c2_1011_post_vector_handler_s29 |
| 1109 | C2:5793-C2:5818 | 6 | 133 | 4 | 5000-6000 | ct_c2_5793_mode_switcher_s29 |
| 1110 | C2:55AC-C2:562D | 6 | 129 | 3 | 5000-6000 | ct_c2_55ac_mode_handler_s29 |
| 1111 | C2:9F4A-C2:9F8C | 6 | 66 | 3 | 9000-A000 | ct_c2_9f4a_hub_extension_s29 |

**Summary:**
- 12 manifests created
- 1,002 bytes of new coverage
- 40 call sites documented
- Average score: 6.1
- 1 score-7 manifest (BFE6)

---

## Key Discoveries

### 1. Vector Region Expansion (0000-1000)
- **C2:0465**: Score-6 with 2 calls, vector handler family
- **C2:04D7**: Initialization helper, post-boot routine
- **C2:0582**: System handler with PHP prologue

### 2. Hub Area Expansion (8000-9000)
- **C2:8006**: Major hub entry with 6 internal calls (largest in session)
- **C2:8249**: Settlement sweep service, related to documented 823C function

### 3. Rich Region Continuation (5000-6000)
- **C2:5319**: JSR-targeted subroutine, 5 calls
- **C2:55AC**: Mode handler with REP/SEP switching
- **C2:5793**: Mode switcher, non-overlapping with 5319 cluster

### 4. Beyond 9F1C Hub (9000-A000)
- **C2:9F4A**: Extension of session 28's 9F1C complex hub network

### 5. Bank-End Helpers (B000-C000)
- **C2:BFE6**: Score-7 bank-end handler (highest score in session)
- **C2:BDF7**: BE00-region service function

---

## Coverage Analysis

| Metric | Before S29 | After S29 | Change |
|--------|------------|-----------|--------|
| Total Manifests | 70 | 82 | +12 |
| Coverage | ~6.5% | ~6.9% | +0.41% |
| Score-6+ Functions | ~25 | ~35 | +10 |
| Regions Mapped | 7 | 7 | (expanded) |

---

## Call-Rich Functions (3+ calls)

| Address | Calls | Bytes | Type |
|---------|-------|-------|------|
| C2:8006 | 6 | 138 | Hub entry |
| C2:1011 | 5 | 151 | Post-vector handler |
| C2:5319 | 5 | 132 | Rich subroutine |
| C2:8249 | 4 | 140 | Sweep service |
| C2:5793 | 4 | 133 | Mode switcher |
| C2:0582 | 3 | 24 | System handler |
| C2:55AC | 3 | 129 | Mode handler |
| C2:9F4A | 3 | 66 | Hub extension |

**Total: 8 call-rich functions**

---

## Dispatch Patterns

### Multi-Call Hubs
- C2:8006 (6 calls) - Primary hub entry
- C2:1011 (5 calls) - Vector extension handler
- C2:5319 (5 calls) - Rich subroutine cluster

### Mode Switching Functions
- C2:55AC - REP/SEP pattern
- C2:5793 - Mode switcher

---

## Validation Results

✅ All 12 manifests validated  
✅ No address conflicts detected  
✅ All ranges unique and non-overlapping  
✅ Pass numbers sequential (1100-1111)

---

## Files Created

### Manifests
```
passes/manifests/pass_1100_c2_0465.yaml
passes/manifests/pass_1101_c2_04d7.yaml
passes/manifests/pass_1102_c2_0582.yaml
passes/manifests/pass_1103_c2_8006.yaml
passes/manifests/pass_1104_c2_8249.yaml
passes/manifests/pass_1105_c2_5319.yaml
passes/manifests/pass_1106_c2_bfe6.yaml
passes/manifests/pass_1107_c2_bdf7.yaml
passes/manifests/pass_1108_c2_1011.yaml
passes/manifests/pass_1109_c2_5793.yaml
passes/manifests/pass_1110_c2_55ac.yaml
passes/manifests/pass_1111_c2_9f4a.yaml
```

### ASM Labels
```
labels/CT_C2_8006_HUB_ENTRY.asm
labels/CT_C2_BFE6_BANK_END.asm
labels/CT_C2_9F4A_HUB_EXT.asm
labels/CT_C2_1011_POST_VECTOR.asm
```

### Report
- `C2_SESSION_29_REPORT.md` - This file

---

## Next Steps

### To Reach 8% Coverage:
1. **Create 10-12 more manifests** targeting:
   - C2:3000-4000 region (sparse coverage)
   - C2:6000-7000 region (continuation)
   - C2:A000-B000 region (gap)
   - C2:C000-D000 region (gap)
   - C2:E000-FFFF region (bank end)

2. **Cross-bank analysis:**
   - Verify C2:8006 callers
   - Map call chains from new functions
   - Identify dispatch patterns

3. **High-value targets remaining:**
   - C2:3001-3082 (score-6, 3000 region)
   - C2:3772-37FC (score-6, 3000 region)
   - C2:8167-81EA (score-6, 8000 region)
   - C2:84D1-8552 (score-6, 8000 region)

---

*Session 29 complete. 12 manifests created, 6 regions expanded, coverage reached ~6.9%.*
