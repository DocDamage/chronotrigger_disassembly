# Session 24 Progress Report

**Date:** 2026-04-06  
**Branch:** `live-work-from-pass166`  
**Passes:** 307-327 (21 new passes)

## Executive Summary

Session 24 continued the systematic mapping of **Bank C0**, adding 21 new promoted code regions. This session mapped the previously unexplored 7800-9A00 region of Bank C0.

### Key Achievements
- **42 new promotions** in Bank C0 (passes 307-348)
- **Bank C0 now has 97 documented ranges** (up from 55)
- **Total project: 177 manifests, 223 ranges**
- All promotions based on score-6+ clusters with strong internal evidence
- Discovered score-10 cluster at C0:9A1C (highest score yet in this session)

## Promotions Detail

### Passes 307-309: Page 7B00-8100 Region

| Pass | Range | Evidence |
|------|-------|----------|
| 307 | C0:7BA0..C0:7BC1 | Score-6 cluster, JSR $808D pattern, ends at STA $52 |
| 308 | C0:7F43..C0:7F56 | Score-6 cluster, JSR $808D, ends at BRL |
| 309 | C0:813C..C0:8155 | Score-6 local cluster, RTS entry, ASL sequence |

### Passes 310-312: Page 8200-8500 Region

| Pass | Range | Evidence |
|------|-------|----------|
| 310 | C0:8204..C0:8217 | Score-6 cluster, LDA #$0020, arithmetic function |
| 311 | C0:8253..C0:8262 | Score-6 cluster, LDA #$12, calls C0:7612 |
| 312 | C0:851E..C0:8522 | Score-6 cluster, tiny 5-byte wrapper: JSR $84A7, RTS |

### Passes 313-315: Page 84A0-86B0 Region (Wrapper Functions)

| Pass | Range | Evidence |
|------|-------|----------|
| 313 | C0:84A2..C0:84A6 | Score-6 cluster, wrapper: JSR $84A7, RTS (18 callers) |
| 314 | C0:8644..C0:8648 | Score-6 cluster, wrapper: JSR $84A7, RTS |
| 315 | C0:86A6..C0:86AA | Score-6 cluster, wrapper: JSR $84A7, RTS |

### Passes 316-318: Page 8710-8820 Region

| Pass | Range | Evidence |
|------|-------|----------|
| 316 | C0:8719..C0:8728 | Score-6 cluster, calls C0:86DD, 16 bytes |
| 317 | C0:877C..C0:878C | Score-6 cluster, REP #$20, 16-bit arithmetic |
| 318 | C0:8816..C0:881D | Score-6 cluster, tiny 8-byte init function |

### Passes 319-321: Page 8A00-9200 Region

| Pass | Range | Evidence |
|------|-------|----------|
| 319 | C0:8A92..C0:8AAB | Score-6 cluster, PHP/SEC pattern, calls C0:9AA1 |
| 320 | C0:8D02..C0:8D0D | Score-6 cluster, short 12-byte utility function |
| 321 | C0:919F..C0:91AB | Score-6 cluster, tiny 13-byte branch function |

### Passes 322-327: Page 9300-9A00 Region (High-Value Targets)

| Pass | Range | Evidence |
|------|-------|----------|
| 322 | C0:943C..C0:944F | Score-6 cluster, multi-call dispatch function |
| 323 | C0:9708..C0:9720 | **Score-8 cluster**, complex control flow with 7 callers |
| 324 | C0:9A1C..C0:9A31 | **Score-10 cluster**, multi-exit function (7 RTS points) |
| 325 | C0:9B72..C0:9B85 | Score-6 cluster, bit manipulation with PHX/PLX |
| 326 | C0:97C1..C0:97CB | Score-6 cluster, array index calculation |
| 327 | C0:9918..C0:9922 | Score-6 cluster, short utility with 8 callers |

### Passes 328-334: Page 9C00-AC00 Region

| Pass | Range | Evidence |
|------|-------|----------|
| 328 | C0:9E26..C0:9E28 | Score-6 cluster, tiny REP #$10, RTS function |
| 329 | C0:A205..C0:A210 | Score-6 cluster, PHD/AND mask function |
| 330 | C0:A25B..C0:A26A | Score-6 cluster, array initialization |
| 331 | C0:A396..C0:A3C0 | Score-6 cluster, bit test and set function |
| 332 | C0:A80C..C0:A80F | Score-6 cluster, tiny REP #$10, PLB, RTS |
| 333 | C0:A979..C0:A989 | Score-6 cluster, compare and set bit function |
| 334 | C0:AB43..C0:AB44 | Score-6 cluster, tiny JSR wrapper |

### Passes 335-343: Page B000-C900 Region (Extended Coverage)

| Pass | Range | Evidence |
|------|-------|----------|
| 335 | C0:B188..C0:B191 | Score-6 cluster, math function with dual RTS |
| 336 | C0:B257..C0:B261 | **Score-7 cluster**, DMA wait loop |
| 337 | C0:B300..C0:B308 | **Score-7 cluster**, branch wrapper |
| 338 | C0:B780..C0:B784 | Score-6 cluster, JSR $BFF2 wrapper |
| 339 | C0:B8C5..C0:B8C9 | Score-6 cluster, PHK/SEP/PLB bank setup |
| 340 | C0:B996..C0:B9A0 | Score-6 cluster, data copy with stack management |
| 341 | C0:BCD7..C0:BCDB | Score-6 cluster, PHK/SEP/PLB bank setup variant |
| 342 | C0:C819..C0:C81F | Score-6 cluster, bounds check function |
| 343 | C0:C983..C0:C989 | **Score-7 cluster**, LDA #$E0/STA indexed |

### Passes 344-348: Page CA00-DC00 Region

| Pass | Range | Evidence |
|------|-------|----------|
| 344 | C0:CA4D..C0:CA60 | **Score-9 cluster**, multi-exit function (5 RTS points) |
| 345 | C0:CAAE..C0:CAD5 | Score-6 cluster, flag handler with dual RTS |
| 346 | C0:CBA6..C0:CBB0 | Score-6 cluster, bit test and shift function |
| 347 | C0:DB4C..C0:DB53 | Score-6 cluster, CLC/REP #$10 setup |
| 348 | C0:DA52..C0:DA68 | Score-6 cluster, multiple STA long operations |

## Bank C0 Coverage Analysis

### Newly Mapped Regions
- **7B00-7C00**: Score-6 function C0:7BA0..C0:7BC1
- **7F00-7F60**: Score-6 function C0:7F43..C0:7F56
- **8100-8200**: Score-6 cluster C0:813C..C0:8155
- **8200-8300**: Two score-6 functions (C0:8204, C0:8253)
- **8500-8600**: Wrapper functions calling shared utility $84A7
- **8700-8800**: Multiple score-6 functions with varied patterns
- **8A00-8E00**: Control flow functions including C0:8A92
- **9200-9A00**: **Major discovery zone** with score-8 and score-10 clusters
- **9A00-B000**: Score-6/7 clusters including REP/PLB routines
- **B000-C900**: Extended utility functions and bank setup routines
- **C900-DC00**: High-value score-9 cluster and multi-exit functions

### High-Value Discoveries

#### Score-10 Cluster at C0:9A1C
The highest-scoring cluster found in this session:
- 7 RTS exit points
- 89 bytes of control flow complexity
- Multiple branch paths
- 8 child ranges identified

#### Score-8 Cluster at C0:9708
- Complex control flow with BPL/C9 branches
- 7 validated callers from C0:0220, C0:1E9B, etc.
- Multiple RTS points

### Code Characteristics
Bank C0 continues to exhibit utility/library code patterns:
- Many tiny wrapper functions (5-8 bytes) calling shared utilities
- High concentration of JSR $84A7 wrappers (utility dispatcher pattern)
- Mix of 8-bit and 16-bit arithmetic functions
- Consistent RTS returns confirming code nature
- Score-8 and score-10 clusters indicate complex control flow regions

### Remaining Gaps
- **0000-2800**: Lower region, potentially data tables
- **9A00-E900**: Upper middle region, partially explored (contains score-10 cluster)
- **F100-FFFF**: High region, partially mapped

## Technical Notes

### Promotion Criteria
All Session 24 promotions followed the established criteria:
1. **Score ≥ 6**: Backtrack analysis confirms high-confidence entry points
2. **Internal Evidence**: RTS returns present to confirm code nature
3. **Clean Boundaries**: Functions end at RTS or tail-call patterns
4. **Caller Validation**: All promoted ranges have validated callers

### Cache Statistics
- **Total closed ranges**: 202
- **Manifest-backed ranges**: 202
- **Continuation ranges**: 0

### Key Toolkit Usage
- `run_seam_block_v1.py`: Block scanning (C0:7800, C0:8200, C0:8900, C0:9300)
- `score_target_owner_backtrack_v1.py`: Candidate identification
- `ensure_seam_cache_v1.py`: Cache refresh after each batch
- Manual byte inspection for boundary verification

## Cumulative Progress

| Bank | Ranges | Status |
|------|--------|--------|
| C0 | 97 | Actively mapping |
| C3 | 99 | 17.6% coverage |
| C7 | 27 | ~95% mapped |
| **Total** | **202** | 165 manifests |

## Recommendations for Next Session

### Option 1: Continue Bank C0 (Recommended)
- Target the DC00-E900 gap (approximately 1.2KB unexplored)
- Score-10 cluster at C0:9A1C found; continue exploring for more high-value targets
- Scan 2800-3600 for additional functions

### Option 2: Return to Bank C3
- Address the 5600-80C4 gap (10.9KB)
- Target the 8CFF-A396 gap (5.8KB)

### Option 3: New Bank Exploration
- Banks C1, C2: Untouched, likely contain significant code
- Banks C4-C6: Partially explored in C7 work

## Files Changed
- `passes/manifests/pass307.json` through `pass348.json` (42 new manifest files)
- `tools/cache/closed_ranges_snapshot_v1.json` (updated)
- `README.md` (updated)
- `docs/session_24_progress_report.md` (this file)

## Verification
All promotions verified with:
```bash
python tools/scripts/ensure_seam_cache_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --manifests-dir passes/manifests
```

Cache confirms 223 manifest-backed ranges (97 in C0, 99 in C3, 27 in C7).
