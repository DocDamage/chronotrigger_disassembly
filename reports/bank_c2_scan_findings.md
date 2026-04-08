# Bank C2 Initial Scan Findings

**Date:** 2026-04-08  
**Scan Regions:** C2:0000-4000, C2:4000-8000, C2:C000-FFFF  
**Focus Area:** C2:8000 Hub  
**Manifests Created:** 12

---

## Executive Summary

Bank C2 is a **high-density code bank** with significant cross-bank connectivity. The scan identified:
- **2129 total opcode score** in C2:0000-4000
- **2034 total opcode score** in C2:4000-8000  
- **1881 total opcode score** in C2:8000-C000 (hub area)
- **1970 total opcode score** in C2:C000-FFFF

**Key Finding:** C2:8000 is a **major cross-bank hub** with functions called from 15+ different banks.

---

## Region Analysis

### 1. C2:0000-4000 (Vector & Low Functions)

| Metric | Value |
|--------|-------|
| Total Score | 2129 |
| Top Cluster | C2:1540 (Score:40) |
| RTS Count | 347 |
| REP/SEP | 340/246 |

**Key Clusters:**
- **C2:157C** (Score:27) - REP/SEP math handler
- **C2:39AE** (Score:20) - Code with C2 REP patterns
- **C2:1A17** (Score:20) - JSR-heavy function
- **C2:127F** (Score:19) - Clean REP prologue with RTS

**Manifests Created:** 3

---

### 2. C2:4000-8000 (Mid-Bank Functions)

| Metric | Value |
|--------|-------|
| Total Score | 2034 |
| Top Cluster | C2:5F00 (Score:38) |
| RTL Count | 18 |
| JSR Count | 853 |

**Key Clusters:**
- **C2:5F14** (Score:28) - Highest in region, loop controller
- **C2:5E36** (Score:24) - PHB/PHP prologue, bank preservation
- **C2:5E57** (Score:22) - E2/SEP loop structure
- **C2:4932** (Score:21) - A2/LDX prologue

**Manifests Created:** 2

---

### 3. C2:8000-C000 (HUB AREA - Primary Focus)

| Metric | Value |
|--------|-------|
| Total Score | 1881 |
| Top Cluster | C2:ADC0 (Score:28) |
| Cross-Bank Callers | 15+ banks |
| JSL Targets | Multiple |

**Hub Infrastructure:**

| Address | Function | Score | Description |
|---------|----------|-------|-------------|
| C2:8002 | Entry Point | - | JSL target from CD:89C6 |
| C2:8820 | Settlement Service | 24 | Major DP=$1D00 pipeline |
| C2:8E2D | Iterative Sweep | 22 | Settlement sweep with export |
| C2:8F6C | List Builder | 20 | Selective accepted-slot builder |
| C2:B716 | Cross-Bank Hub | 26 | Score-8 cluster, 28+ callers |
| C2:B7A6 | Hub Function | 18 | Cross-bank target |
| C2:B7B3 | Hub Helper | 18 | Adjacent to B716 |

**Cross-Bank Callers to C2:B700-B800:**
- C0, C1, C2 (internal), C4, C5, C6, CB
- D2, D3, D4, D5, D6, D7, D8, D9, DA, DB

**Hex Dump - C2:B716 (Score-8 Hub):**
```
C2:B710: 2F B7 A5 54 8D 48 0F C5 81 F0 03 20 C2 EA 20 1F
C2:B720: BB 20 01 BE 20 EB BD A2 1B FC 20 85 83 28 60 A5
C2:B730: 54 D0 07 AD 4A 0F F0 09 80 08 AD 4A 0F C5 57 90
C2:B740: 01 60 A2 03 93 8E 96 96
```

**Manifests Created:** 4

---

### 4. C2:C000-FFFF (Bank-End Functions)

| Metric | Value |
|--------|-------|
| Total Score | 1970 |
| Top Cluster | C2:DD00 (Score:30) |
| PHP Count | 273 |

**Key Clusters:**
- **C2:C17C** (Score:19) - PHP/SEP worker, BFD4 jump-table family
- **C2:E124** (Score:19) - A2/LDX indexed handler
- **C2:C231** (Score:17) - Code cluster with JSR chain
- **C2:F943-FBD0** - Complex documented family (pass 156)

**Notable: C2:F943-FBD0 already documented in passes 155-159**

**Manifests Created:** 2

---

## Manifest Summary (12 Created)

| # | Pass | Range | Label | Region | Score |
|---|------|-------|-------|--------|-------|
| 1 | 590 | C2:157C..C2:1600 | ct_c2_157c_rep_math_handler_score9 | 0000-4000 | 27 |
| 2 | 591 | C2:5F14..C2:5F80 | ct_c2_5f14_loop_controller_score9 | 4000-8000 | 28 |
| 3 | 592 | C2:8820..C2:8890 | ct_c2_8820_settlement_service_hub | 8000 hub | 24 |
| 4 | 593 | C2:8E2D..C2:8E90 | ct_c2_8e2d_iterative_sweep_score8 | 8000 hub | 22 |
| 5 | 594 | C2:B716..C2:B7A0 | ct_c2_b716_cross_bank_hub_score8 | 8000 hub | 26 |
| 6 | 595 | C2:B7B3..C2:B7D0 | ct_c2_b7b3_hub_helper_score6 | 8000 hub | 18 |
| 7 | 596 | C2:C17C..C2:C1E0 | ct_c2_c17c_php_worker_score7 | C000-FFFF | 19 |
| 8 | 597 | C2:E124..C2:E180 | ct_c2_e124_indexed_handler_score6 | C000-FFFF | 19 |
| 9 | 598 | C2:3D01..C2:3D60 | ct_c2_3d01_php_function_score6 | 0000-4000 | 19 |
| 10 | 599 | C2:5E36..C2:5E90 | ct_c2_5e36_phb_handler_score6 | 4000-8000 | 24 |
| 11 | 600 | C2:8A80..C2:8AE0 | ct_c2_8a80_8000hub_service_score6 | 8000 hub | 17 |
| 12 | 601 | C2:127F..C2:12E0 | ct_c2_127f_rep_rts_score6 | 0000-4000 | 19 |

---

## Key Findings

### 1. C2:8000 is a Critical Hub
The C2:8000 region serves as a **major service hub** for the entire game:
- Settlement/search pipeline at C2:8820..C2:991F
- Cross-bank entry points for 15+ banks
- Documented in passes 118-119 as DP=$1D00 current-slot handler

### 2. C2:B700-B800 is Cross-Bank Central
Functions in this region are called from **17 different banks**:
- C2:B716 (score-8) - 28+ documented callers
- C2:B7B3 (score-6) - Adjacent helper
- C2:B7E3 (score-3) - Tiny utility

### 3. High-Density Code Regions
- **C2:1500-1600**: Score-40 cluster (highest in 0000-4000)
- **C2:5E00-5F80**: Score-38 cluster (highest in 4000-8000)
- **C2:DD00**: Score-30 cluster (highest in C000-FFFF)

### 4. Already Documented Areas
- C2:F943-FBD0: Closed in passes 155-159
- C2:FE00-FFFF: Helper clones and bank-end tails
- C2:823C: Documented function (pass 132 reference)

---

## Recommendations

### Immediate Actions
1. **Promote C2:B716** - Already documented as score-8, needs manifest
2. **Verify C2:8820** - Major hub function, validate boundaries
3. **Check C2:5F14** - Highest score in 4000-8000 region

### Next Scan Targets
1. **C2:2000-3000** - Gap in coverage
2. **C2:9000-B700** - Upper hub area
3. **C2:A000-C000** - Middle-high region

### Cross-Bank Verification Needed
- C2:8002 callers (CD:89C6, etc.)
- C2:B716 caller validation (28+ claimed)
- C2:8820 settlement pipeline integration

---

## Files Created

1. `reports/bank_c2_manifests_batch_1.json` - 12 new manifests
2. `reports/bank_c2_scan_findings.md` - This report

---

*Scan completed by Bank C2 Analysis Tool*
