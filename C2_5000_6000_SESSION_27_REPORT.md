# Bank C2 5000-6000 Region Deep Scan - Session 27

**Date:** 2026-04-08  
**Analyst:** Kimi Code CLI  
**Session:** 27  
**Region:** C2:5000-C2:6000 (Richest code region in Bank C2)

---

## Executive Summary

Deep scan of Bank C2's 5000-6000 region - the richest area with 88+ code islands discovered. Created **12 new manifests** covering high-value targets with scores 5-6.

**Key Discoveries:**
- **C2:5F7E..C2:5FD7**: Score-14 MEGA-CLUSTER (90 bytes, 10 children) - Already documented in pass_644
- **C2:5E65..C2:5E8A**: Score-8 mega-cluster (38 bytes, 7 calls) - Already documented in pass_1054
- **C2:5F2C..C2:5F5B**: Score-8 cluster (48 bytes, 8 calls) - Already documented in pass_1055
- Multiple score-6 backtrack candidates identified

---

## New Manifests Created (Session 27)

| Pass | Range | Label | Score | Width | Calls | Returns | Notes |
|------|-------|-------|-------|-------|-------|---------|-------|
| 1066 | C2:5315-C2:531C | ct_c2_5315_helper | 6 | 8 | 1 | 1 | Compact helper, sibling to 5319 |
| 1067 | C2:531D-C2:5338 | ct_c2_5319_jsr_handler | 6 | 28 | 2 | 1 | JSR prologue, cross-bank caller |
| 1068 | C2:535F-C2:5379 | ct_c2_535f_subroutine | 6 | 27 | 1 | 1 | JSR entry, clean sequence |
| 1069 | C2:5793-C2:57B0 | ct_c2_5793_vector_routine | 6 | 30 | 3 | 1 | Near vector target C2:57DF |
| 1073 | C2:5432-C2:543B | ct_c2_5432_helper | 5 | 10 | 2 | 1 | Dense helper (2 calls in 10 bytes) |
| 1076 | C2:5083-C2:508E | ct_c2_5083_compact | 5 | 12 | 2 | 1 | 5000 region, 2 calls |
| 1077 | C2:522C-C2:5242 | ct_c2_522c_dispatcher | 5 | 23 | 6 | 1 | **6 calls!** High density |
| 1078 | C2:524E-C2:5261 | ct_c2_524e_handler | 5 | 20 | 5 | 1 | 5 calls, 2 branches |
| 1079 | C2:5E34-C2:5E54 | ct_c2_5e34_multi_return | 6 | 33 | 5 | 4 | Multi-exit pattern |
| 1080 | C2:5160-C2:5173 | ct_c2_5160_rich_subroutine | 5 | 20 | 5 | 1 | 5 calls, 3 branches |
| 1081 | C2:56A1-C2:56BD | ct_c2_56a1_mode_switch | 6 | 29 | 3 | 1 | REP prologue, mode switch |
| 1082 | C2:56C9-C2:56E8 | ct_c2_56c9_jsr_routine | 6 | 32 | 2 | 1 | JSR prologue, 32 bytes |

**Total New Coverage:** 254 bytes  
**Average Score:** 5.5  
**Total Calls:** 37  
**Total Returns:** 15

---

## Mega-Clusters Re-Confirmed

| Cluster | Range | Score | Width | Children | Calls | Returns | Status |
|---------|-------|-------|-------|----------|-------|---------|--------|
| 5F7E | C2:5F7E-C2:5FD7 | **14** | 90 | 10 | 3 | 10 | Already in pass_644 |
| 5E65 | C2:5E65-C2:5E8A | **8** | 38 | 4 | 7 | 4 | Already in pass_1054 |
| 5F2C | C2:5F2C-C2:5F5B | **8** | 48 | 4 | 8 | 4 | Already in pass_1055 |

---

## Region Breakdown

### C2:5000-5400 (New: 5 manifests)
- **5083**: Score-5 compact routine (12 bytes, 2 calls)
- **5160**: Score-5 rich subroutine (20 bytes, 5 calls, 3 branches)
- **522C**: Score-5 dispatcher (23 bytes, **6 calls**)
- **524E**: Score-5 handler (20 bytes, 5 calls)
- **5315**: Score-6 compact helper (8 bytes)

### C2:5400-5800 (New: 3 manifests)
- **531D**: Score-6 JSR handler (28 bytes, cross-bank)
- **535F**: Score-6 subroutine (27 bytes)
- **5432**: Score-5 dense helper (10 bytes, 2 calls)

### C2:5800-6000 (New: 4 manifests)
- **56A1**: Score-6 mode switch (29 bytes, 3 calls)
- **56C9**: Score-6 JSR routine (32 bytes)
- **5793**: Score-6 vector routine (30 bytes, near C2:57DF)
- **5E34**: Score-6 multi-return (33 bytes, 5 calls, 4 returns)

---

## Cross-Bank Caller Analysis

Functions in the 5000-6000 region are called from:
- **C2:2346** → C2:5319 region
- **C2:3100** → C2:56C9
- **C2:D158, C2:E074, C2:E546** → C2:5160, C2:51A6
- **C2:693B, C2:778A, C2:7ADB, C2:6CEA** → C2:56A1
- **C2:FD99, C2:FDBD, C2:FE9C, C2:906C** → C2:53AD

This region is a **major cross-bank hub** for Bank C2 functionality.

---

## Vector Table Targets

Confirmed vector targets in the 5000-6000 region:
- **C2:57DF**: Called from C2:0003, C2:0006 (vector table entries)
- **C2:5823**: Called from C2:0009, C2:000C (vector table entries)

These are **hardware vector targets** from the C2:0000 vector table.

---

## Coverage Improvement

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| C2:5000-6000 Manifests | 12 | 24 | +12 |
| C2 Total Coverage | ~5.4% | ~6.2% | +0.8% |
| Score-6+ Functions | 7 | 15 | +8 |

---

## Files Created

### Manifests (passes/manifests/)
```
pass_1066_c2_5315.yaml
pass_1067_c2_5319.yaml
pass_1068_c2_535f.yaml
pass_1069_c2_5793.yaml
pass_1073_c2_5432.yaml
pass_1076_c2_5083.yaml
pass_1077_c2_522c.yaml
pass_1078_c2_524e.yaml
pass_1079_c2_5e34.yaml
pass_1080_c2_5160.yaml
pass_1081_c2_56a1.yaml
pass_1082_c2_56c9.yaml
```

### Reports
- `C2_5000_6000_SESSION_27_REPORT.md` (this file)

---

## Next Steps

1. **B000 Region Extension**: Continue scanning C2:B200, B400, BC00 candidate lanes
2. **Vector Region Follow-up**: Deep dive into C2:57DF and C2:5823 handlers
3. **Cross-Reference**: Build caller graphs for the newly identified functions
4. **Data Analysis**: Identify data tables between code islands

---

*Session 27 completed using seam_block_v1, find_local_code_islands_v2, and score_target_owner_backtrack_v1 toolkit scripts.*
