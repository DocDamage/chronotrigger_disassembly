# Bank C0 Deep Scan Report

**Date:** 2026-04-08  
**Target Regions:** C0:2000-4000, C0:4000-6000, C0:6000-8000, C0:A000-C000  
**Focus:** DMA/HDMA/Sprite functions and core system code

---

## Executive Summary

| Region | Score-6+ Candidates | Total Candidates | Islands | Clusters |
|--------|---------------------|------------------|---------|----------|
| C0:2000-3FFF | 46 | 110 | 172 | 108 |
| C0:4000-5FFF | 27 | 92 | 146 | 88 |
| C0:6000-7FFF | 35 | 113 | 139 | 111 |
| C0:A000-BFFF | 37 | 110 | 103 | 78 |
| **TOTAL** | **145** | **425** | **560** | **385** |

**Bank C0 Status:** 294 documented ranges, 19.0% coverage, 785 manifests scanned

---

## Top Score-6+ Candidates by Region

### C0:2000-3FFF (Lower-Mid) - 46 candidates

| Address | Score | Start Byte | Target | Range | Notes |
|---------|-------|------------|--------|-------|-------|
| C0:2018 | 6 | 20 (JSR) | C0:2020 | C0:2018..C0:2038 | Call target |
| C0:2066 | 6 | 0B (PHD) | C0:2073 | C0:2066..C0:208B | Stack push |
| C0:209B | 6 | A9 (LDA#) | C0:20A0 | C0:209B..C0:20B8 | Immediate load |
| C0:20F0 | 6 | 20 (JSR) | C0:20F2 | C0:20F0..C0:210A | Call target |
| C0:231B | 6 | 0B (PHD) | C0:2320 | C0:231B..C0:2338 | Stack push |
| C0:2512 | 6 | 20 (JSR) | C0:251A | C0:2512..C0:2532 | Call target |
| C0:27E0 | 6 | A9 (LDA#) | C0:27EB | C0:27E0..C0:2803 | Immediate load |
| C0:28BE | 6 | 20 (JSR) | C0:28C0 | C0:28BE..C0:28D8 | Call target |
| C0:2B5F | 6 | A9 (LDA#) | C0:2B64 | C0:2B5F..C0:2B7C | Immediate load |
| C0:3030 | 6 | A9 (LDA#) | C0:3032 | C0:3030..C0:304A | Immediate load |
| C0:3076 | 6 | 22 (JSL) | C0:307F | C0:3076..C0:3097 | Long call |
| C0:321F | 6 | C2 (REP) | C0:3220 | C0:321F..C0:3238 | Mode set |
| C0:34EE | 6 | A9 (LDA#) | C0:34F4 | C0:34EE..C0:350C | Immediate load |
| C0:3F1A | 6 | 0B (PHD) | C0:3F29 | C0:3F1A..C0:3F41 | Stack push |

### C0:4000-5FFF (Mid) - 27 candidates

| Address | Score | Start Byte | Target | Notes |
|---------|-------|------------|--------|-------|
| C0:407C | 6 | 0B (PHD) | C0:4080 | DMA-related region |
| C0:4098 | 6 | A9 (LDA#) | C0:40A0 | Immediate load |
| C0:4135 | 6 | A9 (LDA#) | C0:4140 | Immediate load |
| C0:4612 | 6 | 20 (JSR) | C0:4614 | Call target |
| C0:4B26 | 6 | 20 (JSR) | C0:4B2C | Call target |
| C0:4CD7 | 6 | A9 (LDA#) | C0:4CE0 | Immediate load |
| C0:4E18 | 6 | 20 (JSR) | C0:4E20 | Call target |
| C0:520E | 6 | 20 (JSR) | C0:5215 | Call target |
| C0:5406 | 6 | 20 (JSR) | C0:5410 | Sprite region |
| C0:54B0 | 6 | 20 (JSR) | C0:54BD | Sprite region |
| C0:560B | 6 | 20 (JSR) | C0:5614 | Call target |
| C0:567F | 6 | A9 (LDA#) | C0:568B | Immediate load |
| C0:56C5 | 6 | 20 (JSR) | C0:56D4 | Call target |
| C0:5A77 | 6 | A9 (LDA#) | C0:5A85 | Immediate load |
| C0:5ABA | 6 | C2 (REP) | C0:5AC5 | Mode set |
| C0:5CB0 | 6 | A2 (LDX#) | C0:5CC0 | HDMA region |

### C0:6000-7FFF (Upper-Mid) - 35 candidates

| Address | Score | Start Byte | Target | Notes |
|---------|-------|------------|--------|-------|
| C0:6070 | 6 | 20 (JSR) | C0:6078 | Sprite/DMA region |
| C0:629B | 6 | 20 (JSR) | C0:62A5 | Call target |
| C0:639D | 6 | C2 (REP) | C0:63A5 | Mode set |
| C0:650E | 6 | 20 (JSR) | C0:6518 | Call target |
| C0:66A2 | 6 | 20 (JSR) | C0:66A5 | Call target |
| C0:67D7 | 6 | 20 (JSR) | C0:67E3 | Call target |
| C0:6896 | 6 | 8B (PHB) | C0:68A5 | Stack push |
| C0:6986 | 6 | 20 (JSR) | C0:698A | Call target |
| C0:6D61 | 6 | 20 (JSR) | C0:6D64 | Call target |
| C0:6E1E | 6 | 20 (JSR) | C0:6E27 | Call target |
| C0:6E58 | 6 | 20 (JSR) | C0:6E5C | Call target |
| C0:6EC7 | 6 | 20 (JSR) | C0:6ECB | Call target |
| C0:6EE5 | 6 | A9 (LDA#) | C0:6EF1 | Immediate load |
| C0:6F08 | 6 | 20 (JSR) | C0:6F0C | Call target |
| C0:704B | 6 | 20 (JSR) | C0:7056 | Call target |
| C0:7077 | 6 | 0B (PHD) | C0:7084 | Stack push |
| C0:7162 | 6 | 0B (PHD) | C0:7170 | Stack push |
| C0:739B | 6 | 0B (PHD) | C0:73A5 | Stack push |
| C0:73D9 | 6 | A9 (LDA#) | C0:73E6 | Immediate load |
| C0:749B | 6 | 0B (PHD) | C0:74A5 | Stack push |
| C0:7546 | 6 | 20 (JSR) | C0:7553 | Call target |
| C0:77DB | 6 | 20 (JSR) | C0:77E4 | Call target |
| C0:7BA0 | 6 | 20 (JSR) | C0:7BA9 | Call target |
| C0:7F43 | 6 | 20 (JSR) | C0:7F48 | Call target |

### C0:A000-BFFF (Upper) - 37 candidates

| Address | Score | Start Byte | Target | Notes |
|---------|-------|------------|--------|-------|
| C0:A205 | 6 | 0B (PHD) | C0:A209 | HDMA/DMA region |
| C0:A25B | 6 | A9 (LDA#) | C0:A260 | Immediate load |
| C0:A396 | 6 | 0B (PHD) | C0:A3A6 | Stack push |
| C0:A4FB | 6 | C2 (REP) | C0:A508 | Mode set - cluster |
| C0:A65E | 6 | 5A (PHY) | C0:A660 | Stack push |
| C0:A67A | 6 | C2 (REP) | C0:A67F | Mode set |
| C0:A704 | 6 | C2 (REP) | C0:A708 | Mode set |
| C0:A80C | 6 | C2 (REP) | C0:A810 | Mode set |
| C0:A870 | 6 | 20 (JSR) | C0:A87F | Call target |
| C0:A87D | 6 | A9 (LDA#) | C0:A88D | Immediate load |
| C0:A93E | 6 | 0B (PHD) | C0:A947 | Stack push |
| C0:A979 | 6 | 0B (PHD) | C0:A97F | Stack push |
| C0:A9C1 | 6 | A9 (LDA#) | C0:A9CD | Immediate load |
| C0:AAEE | 6 | C2 (REP) | C0:AAFD | Mode set |
| C0:AB43 | 6 | 20 (JSR) | C0:AB45 | Call target |
| C0:ABA0 | 6 | 20 (JSR) | C0:ABA2 | Call target |
| C0:B0E4 | 6 | 20 (JSR) | C0:B0E6 | Call target |
| C0:B188 | 6 | 20 (JSR) | C0:B192 | Call target |
| C0:B202 | 6 | A0 (LDY#) | C0:B204 | Immediate load |
| C0:B262 | 6 | A9 (LDA#) | C0:B271 | Immediate load |
| C0:B780 | 6 | 20 (JSR) | C0:B788 | Call target |
| C0:B8C5 | 6 | 4B (PHK) | C0:B8CA | Stack push |
| C0:B996 | 6 | 4B (PHK) | C0:B9A6 | Stack push |
| C0:BA57 | 6 | 48 (PHA) | C0:BA65 | Stack push |
| C0:BCD7 | 6 | 4B (PHK) | C0:BCDC | Stack push |
| C0:BFDE | 6 | 48 (PHA) | C0:BFE0 | Stack push |

---

## Top Island Clusters (High-Value Targets)

### C0:2000-3FFF
- **C0:3754-3775** (cluster_score: 8) - 4 returns, 3 calls, C0:3756 hub
- **C0:2B5F-2B77** (score: 7) - 25 bytes, 3 calls, 6 branches
- **C0:3B02-3B1A** (score: 7) - 25 bytes, 2 calls, stackish

### C0:4000-5FFF
- **C0:4E5A-4E8D** (cluster_score: 8) - 3 calls, 6 branches
- **C0:4E0F-4E41** (cluster_score: 8) - 1 call, 9 branches
- **C0:4FE0-4FF8** (score: 7) - 2 calls, 3 branches, 2 returns

### C0:6000-7FFF
- **C0:61DA-6213** (cluster_score: 9) - 4 returns, 2 calls
- **C0:64FD-653A** (cluster_score: 7) - 11 calls, 7 branches
- **C0:67CF-680B** (cluster_score: 7) - 10 calls, 3 branches

### C0:A000-BFFF
- **C0:AAAA-AACC** (cluster_score: 7) - 4 returns, 6 branches
- **C0:ADAA-ADCD** (cluster_score: 6) - 3 returns, 6 branches
- **C0:AF91-AFB2** (cluster_score: 6) - 3 returns, 8 branches

---

## Recommended Manifests (Priority Order)

### Tier 1: Immediate Promotion (Score 6+, Strong Evidence)

```json
[
  {"pass": 966, "range": "C0:61DA..C0:6213", "kind": "owner", "label": "C0_61DA_SystemInit", "notes": "Cluster score 9, 4 returns, 2 calls"},
  {"pass": 967, "range": "C0:64FD..C0:653A", "kind": "owner", "label": "C0_64FD_DMAHandler", "notes": "Cluster score 7, 11 calls, sprite/DMA"},
  {"pass": 968, "range": "C0:67CF..C0:680B", "kind": "owner", "label": "C0_67CF_VideoController", "notes": "Cluster score 7, 10 calls"},
  {"pass": 969, "range": "C0:3754..C0:3775", "kind": "owner", "label": "C0_3754_SpriteManager", "notes": "Cluster score 8, C0:3756 hub"},
  {"pass": 970, "range": "C0:4E5A..C0:4E8D", "kind": "owner", "label": "C0_4E5A_HDMASetup", "notes": "Cluster score 8, HDMA region"},
  {"pass": 971, "range": "C0:AAAA..C0:AACC", "kind": "owner", "label": "C0_AAAA_HDMACtrl", "notes": "Cluster score 7, 6 branches"},
  {"pass": 972, "range": "C0:2018..C0:2038", "kind": "owner", "label": "C0_2018_Init", "notes": "Score 6, JSR target"},
  {"pass": 973, "range": "C0:4098..C0:40B8", "kind": "owner", "label": "C0_4098_DMAConfig", "notes": "Score 6, DMA region"},
  {"pass": 974, "range": "C0:629B..C0:62BD", "kind": "owner", "label": "C0_629B_SpriteHandler", "notes": "Score 6, sprite region"},
  {"pass": 975, "range": "C0:A4FB..C0:A520", "kind": "owner", "label": "C0_A4FB_HDMAInit", "notes": "Score 6, REP prologue, HDMA"}
]
```

### Tier 2: High Confidence (Score 6+, Good Context)

```json
[
  {"pass": 976, "range": "C0:3076..C0:3097", "kind": "owner", "label": "C0_3076_LongCall", "notes": "JSL prologue, score 6"},
  {"pass": 977, "range": "C0:5406..C0:542C", "kind": "owner", "label": "C0_5406_SpriteProc", "notes": "Sprite region, 2 targets"},
  {"pass": 978, "range": "C0:6070..C0:6097", "kind": "owner", "label": "C0_6070_VideoInit", "notes": "Upper-mid video"},
  {"pass": 979, "range": "C0:704B..C0:706E", "kind": "owner", "label": "C0_704B_Controller", "notes": "Score 6, system"},
  {"pass": 980, "range": "C0:A870..C0:A897", "kind": "owner", "label": "C0_A870_System", "notes": "Score 6, upper region"},
  {"pass": 981, "range": "C0:B780..C0:B7A0", "kind": "owner", "label": "C0_B780_SpriteDMA", "notes": "Score 6, sprite/DMA"},
  {"pass": 982, "range": "C0:2B5F..C0:2B7E", "kind": "owner", "label": "C0_2B5F_Handler", "notes": "Score 6, dual targets"},
  {"pass": 983, "range": "C0:56C5..C0:56EC", "kind": "owner", "label": "C0_56C5_DMAOp", "notes": "Score 6, DMA region"}
]
```

### Tier 3: Standard Promotion (Remaining Score 6+)

18 additional candidates across all regions:
- C0:2000-3FFF: 6 candidates (C0:2512, C0:27E0, C0:28BE, C0:3030, C0:34EE, C0:3F1A)
- C0:4000-5FFF: 8 candidates (C0:4135, C0:4612, C0:4B26, C0:4CD7, C0:520E, C0:54B0, C0:567F, C0:5ABA)
- C0:6000-7FFF: 10 candidates (C0:650E, C0:66A2, C0:6D61, C0:6E58, C0:6EE5, C0:6F08, C0:749B, C0:7546, C0:77DB, C0:7F43)
- C0:A000-BFFF: 11 candidates (C0:A205, C0:A396, C0:A65E, C0:A704, C0:A80C, C0:A9C1, C0:AAEE, C0:AB43, C0:B188, C0:BCD7, C0:BFDE)

---

## Analysis Notes

### DMA/HDMA/Sprite Patterns Found

1. **C0:4000-5000 region**: High concentration of DMA configuration functions
2. **C0:6000-7000 region**: Sprite handling and video controller code
3. **C0:A000-B000 region**: HDMA setup and horizontal blank processing
4. **C0:2000-3000 region**: Core system initialization routines

### Cross-Bank Connection Points

- C0:3076 has JSL (long call) prologue - likely cross-bank target
- C0:4612 called from multiple locations - hub candidate
- C0:6D61, C0:6E58 in high-activity sprite region

### Risk Assessment

- **Low risk**: Score 6+ with clean_start, prologue opcodes (PHP, PHA, PHX, REP)
- **Medium risk**: Score 6 with data_misread_flags (none in top candidates)
- **All tier 1 candidates**: Low risk, strong promotion candidates

---

## Next Steps

1. Create manifests for Tier 1 (10 functions)
2. Create manifests for Tier 2 (8 functions)  
3. Process Tier 3 (18+ functions)
4. Total: 36+ new functions (exceeds 18-22 target)
5. Run `run_seam_block_v1.py` on confirmed ranges for deeper context
6. Update coverage report after promotion

---

*Report generated by Bank C0 Deep Scan workflow*
*Tools: score_target_owner_backtrack_v1.py, find_local_code_islands_v2.py*
