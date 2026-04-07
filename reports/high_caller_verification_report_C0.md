# C0 Bank High-Caller Function Verification Report

**Date:** 2026-04-06  
**ROM:** Chrono Trigger (USA).sfc (SHA256: 06d1c2b06b716052c5596aaa0c2e5632a027fee1a9a28439e509f813c30829a9)

---

## Executive Summary

This report documents the verification status of 8 high-caller functions in Bank C0 of the Chrono Trigger disassembly project.

| Status | Count | Functions |
|--------|-------|-----------|
| Already Covered | 5 | C0:857F, C0:1B31, C0:3885, C0:107F, C0:0A0A |
| Boundary Adjusted | 2 | C0:8085, C0:808D (combined in pass454) |
| New Pass Created | 1 | C0:8500 (pass459) |

---

## Detailed Status of Each Target

### 1. C0:857F (93 callers) - Major Dispatcher ✅ COVERED

**Status:** Already covered by pass410.json  
**Range:** C0:857F..C0:8584  
**Size:** 6 bytes  
**Label:** ct_c0_857f_major_dispatcher_score93  
**Manifest:** `passes/manifests/pass410.json`  
**Label File:** `labels/ct_c0_857f_major_dispatcher_score93.asm`

**Notes:**
- SEP #$20/JSR $84A7/RTS pattern
- 3 RTS exits
- Highest caller count in C0 bank

---

### 2. C0:1B31 (92 callers) - Major Utility ✅ COVERED

**Status:** Already covered by pass369.json  
**Range:** C0:1B31..C0:1B52  
**Size:** 34 bytes  
**Label:** ct_c0_1b31_major_utility_score92  
**Manifest:** `passes/manifests/pass369.json`

**Notes:**
- 2 RTS points (C0:1B46, C0:1B52)
- Bit shift and add operation
- Second highest caller count

---

### 3. C0:808D (32 callers) - DMA Utility ✅ ADJUSTED

**Status:** Now covered by extended pass454.json (combined with C0:8085)  
**Range:** C0:8085..C0:813C (entry at 808D)  
**Size:** 175 bytes from entry point  
**Label:** ct_c0_8085_dma_shared_function_60callers  
**Manifest:** `passes/manifests/pass454.json` (updated)

**Notes:**
- Primary entry point (32 callers)
- Shares function body with C0:8085
- Single RTS at C0:813C
- **Boundary Adjustment:** Extended pass454 from C0:80BD to C0:8085

---

### 4. C0:8085 (28 callers) - DMA Utility ✅ ADJUSTED

**Status:** Now covered by extended pass454.json (combined with C0:808D)  
**Range:** C0:8085..C0:813C  
**Size:** 183 bytes  
**Label:** ct_c0_8085_dma_shared_function_60callers  
**Manifest:** `passes/manifests/pass454.json` (updated)

**Notes:**
- Secondary entry point (28 callers)
- Same function body as C0:808D
- Combined 60 callers total
- **Boundary Adjustment:** Extended pass454 from C0:80BD to C0:8085

---

### 5. C0:8500 (20 callers) - DMA Setup ✅ NEW PASS

**Status:** Created new pass459.json  
**Range:** C0:8500..C0:8522  
**Size:** 34 bytes  
**Label:** ct_c0_8500_dma_setup_20callers  
**Manifest:** `passes/manifests/pass459.json` (NEW)  
**Label File:** `labels/ct_c0_8500_dma_setup_20callers.asm` (NEW)

**Notes:**
- DMA setup utility with LDA #$7E/STA $0305 pattern
- RTS at C0:8522 (+34 bytes)
- Contains pass312 range (C0:851E..C0:8522)
- **Action Required:** pass312 should be removed as contained within pass459

---

### 6. C0:3885 (26 callers) - Cross-Bank Loader ✅ COVERED

**Status:** Already covered by pass373.json  
**Range:** C0:3885..C0:38A7  
**Size:** 35 bytes  
**Label:** ct_c0_3885_cross_bank_loader_score26  
**Manifest:** `passes/manifests/pass373.json`

**Notes:**
- JSL $C18003/JSL $C28004 pattern
- 2 RTS points
- Cross-bank loader utility

---

### 7. C0:107F (25 callers) - VRAM Calc ✅ COVERED

**Status:** Already covered by pass380.json  
**Range:** C0:107F..C0:1097  
**Size:** 25 bytes  
**Label:** ct_c0_107f_vram_calc_score25  
**Manifest:** `passes/manifests/pass380.json`

**Notes:**
- VRAM calculation with AND #$1F00
- Score-4 backtrack target

---

### 8. C0:0A0A (25 callers) - DMA Setup ✅ COVERED

**Status:** Already covered by pass376.json  
**Range:** C0:0A0A..C0:0A13  
**Size:** 10 bytes  
**Label:** ct_c0_0a0a_dma_setup_score25  
**Manifest:** `passes/manifests/pass376.json`

**Notes:**
- LDA #$7E/STA $0305/JSL $C30002 pattern
- Score-5 target

---

## Files Created/Modified

### Modified Files
1. `passes/manifests/pass454.json` - Extended range from C0:80BD..C0:813B to C0:8085..C0:813C

### New Files
1. `passes/manifests/pass459.json` - New pass for C0:8500..C0:8522
2. `labels/ct_c0_8500_dma_setup_20callers.asm` - Label documentation for C0:8500

### Recommended for Cleanup
1. `passes/manifests/pass312.json` - Now contained within pass459 (C0:851E..C0:8522 inside C0:8500..C0:8522)

---

## Boundary Adjustments Summary

### Pass454 Extension
```
Before: C0:80BD..C0:813B (label: ct_c0_80bd_dma_handler_23callers)
After:  C0:8085..C0:813C (label: ct_c0_8085_dma_shared_function_60callers)

Reason: The DMA function actually starts at C0:8085 with 28 callers,
        and C0:808D is an alternative entry point with 32 callers.
        Combined 60 callers for this shared function body.
```

### Pass459 Creation
```
New:    C0:8500..C0:8522 (label: ct_c0_8500_dma_setup_20callers)
        Size: 34 bytes
        Callers: 20
        
Note:   Contains the previous pass312 range (C0:851E..C0:8522)
```

---

## Call Graph Context

### DMA Function Cluster (C0:8000 region)
```
C0:8085 (28 callers) ──┐
                       ├──→ Shared function body ──→ RTS at C0:813C
C0:808D (32 callers) ──┘

C0:80BD (23 callers) ──→ Previously thought to be separate,
                          actually part of 8085/808D function
```

### DMA Setup Cluster (C0:8500 region)
```
C0:8500 (20 callers) ──→ DMA setup function ──→ RTS at C0:8522
                              │
                              ├── C0:851E..C0:8522 (was pass312)
                              │   Tiny wrapper now recognized as
                              │   part of larger function
```

---

## Verification Checklist

- [x] C0:857F (93 callers) - Verified covered by pass410
- [x] C0:1B31 (92 callers) - Verified covered by pass369
- [x] C0:808D (32 callers) - Verified and added to pass454
- [x] C0:8085 (28 callers) - Verified and added to pass454
- [x] C0:8500 (20 callers) - Verified and created pass459
- [x] C0:3885 (26 callers) - Verified covered by pass373
- [x] C0:107F (25 callers) - Verified covered by pass380
- [x] C0:0A0A (25 callers) - Verified covered by pass376

---

## Next Steps

1. **Run overlap resolution:** Execute `fix_overlaps.py` to remove pass312 (now contained in pass459)
2. **Create label file for 8085:** Consider creating `labels/ct_c0_8085_dma_shared_function_60callers.asm`
3. **Update pass404:** Consider updating to reference the adjusted pass454
4. **Cross-reference validation:** Verify no other passes reference the old pass454 boundaries

---

*Report generated by high-caller verification script*  
*All addresses verified against ROM bytes*
