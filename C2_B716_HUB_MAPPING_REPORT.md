# C2:B716 Cross-Bank Hub Mapping Report

**Date**: 2026-04-08  
**Task**: Map C2:B716 hub region (cross-bank settlement service)  
**Status**: ✅ COMPLETE

---

## Manifests Created

| Pass | Range | Label | Score | Confidence | Type |
|------|-------|-------|-------|------------|------|
| 1000 | C2:B716-B741 | ct_c2_b716_cross_bank_hub | 8 | 7 | MAIN HUB |
| 1001 | C2:B7B3-B7CB | ct_c2_b7b3_hub_helper | 6 | 6 | Helper |
| 1002 | C2:B7E3-B7E8 | ct_c2_b7e3_hub_wrapper | 3 | 6 | Wrapper |

---

## C2:B716-B741 Main Hub Details

### Cross-Bank Activity
- **28+ callers from 15+ banks**
- Settlement service hub with DP=$1D00 pipeline
- Primary dispatch hub for inter-bank operations

### Characteristics
- **Size**: 44 bytes
- **Calls**: 5 (JSR/JSL)
- **Branches**: 5
- **Stack Operations**: 2 (PHP/PHB/PHD)
- **Returns**: 2 (RTS/RTL)

### Boundaries
- Primary function: C2:B716-C2:B72E (25 bytes)
- Extended: C2:B716-C2:B741 (44 bytes, includes helper logic)
- Return points: C2:B72E (primary), C2:B741 (extended)

### Context Functions
- Predecessor: C2:B6A2-C2:B6C6 (bridge function, score-6 JSL)
- Adjacent helper: C2:B721-C2:B747 (helper function, score-6 JSR)

---

## C2:B7B3-B7CB Helper Details

- **Size**: 25 bytes
- **Calls**: 2
- **Branches**: 2
- **Pattern**: PHP prologue, RTS-terminated
- **Purpose**: Supports settlement service operations

---

## C2:B7E3-B7E8 Wrapper Details

- **Size**: 6 bytes
- **Type**: Tiny thunk/wrapper
- **Purpose**: Entry/exit point for cross-bank calls
- **Location**: B700-B800 settlement service pipeline

---

## Files Created

### Manifests
- `passes/manifests/pass1000.json` - Main cross-bank hub
- `passes/manifests/pass1001.json` - Hub helper
- `passes/manifests/pass1002.json` - Hub wrapper

### ASM Labels
- `labels/CT_C2_B716_CROSS_BANK_HUB.asm`
- `labels/CT_C2_B7B3_HUB_HELPER.asm`
- `labels/CT_C2_B7E3_HUB_WRAPPER.asm`

---

## Bank C2 Progress Update

| Metric | Value |
|--------|-------|
| Total Manifests | 830+ (including new passes 1000-1002) |
| C2:B700-B800 Coverage | Hub region mapped |
| High-Value Targets | B716 (score 8) - COMPLETE |

---

## Notes

The C2:B716 region has been identified as a **critical cross-bank settlement service hub** with extensive caller relationships across 15+ banks. This is one of the most significant hubs discovered in the Chrono Trigger disassembly project to date.

The manifests refine earlier coverage (pass574 covered B716-B7A0 broadly) with precise boundaries for the main hub (B716-B741), helper (B7B3-B7CB), and wrapper (B7E3-B7E8) functions.
