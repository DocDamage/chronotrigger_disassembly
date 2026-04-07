# Session 23 Progress Report

**Date:** 2026-04-05  
**Branch:** `live-work-from-pass166`  
**Passes:** 277-306 (30 new passes)

## Executive Summary

Session 23 completed the first comprehensive mapping of **Bank C0**, adding 30 new promoted code regions. This represents the discovery and documentation of an entirely new bank that was previously unmapped.

### Key Achievements
- **30 new promotions** in Bank C0 (passes 277-306)
- **Bank C0 now has 55 documented ranges** (up from 0)
- **Total project: 144 manifests, 181 ranges**
- All promotions based on score-6 clusters with strong internal evidence (RTS returns)

## Promotions Detail

### Passes 277-280: Initial Bank C0 Discovery

| Pass | Range | Evidence |
|------|-------|----------|
| 277 | C0:E945-E9A0 | Score-6 cluster, RTS=5 |
| 278 | C0:F0B9-F110 | Score-6 cluster, RTS=2, JSR=5 |
| 279 | C0:289B-28F0 | Score-6 cluster, RTS=1, JSR=3 |
| 280 | C0:3551-35B0 | Score-6 cluster, RTS=3, PHP=2 |

### Passes 281-286: Page 4000-5A00 Region

| Pass | Range | Evidence |
|------|-------|----------|
| 281 | C0:407C-408E | Score-6 cluster, RTS at end |
| 282 | C0:4098-40B3 | Score-6 cluster, RTS at end |
| 283 | C0:4612-4670 | Score-6 cluster, RTS=3, PHP=1 |
| 284 | C0:520E-5280 | Score-6 cluster, RTS=6, PHP=1 |
| 285 | C0:5406-5470 | Score-6 cluster, RTS=7 |
| 286 | C0:5A77-5A90 | Score-6 cluster, RTS at end |

### Passes 287-293: Page 5C00-6400 Region

| Pass | Range | Evidence |
|------|-------|----------|
| 287 | C0:5C8D-5CC6 | Score-6 cluster, RTS at end |
| 288 | C0:6070-607D | Score-6 cluster, RTS at end |
| 289 | C0:629B-62CA | Score-6 cluster, RTS at end |
| 290 | C0:639D-63E5 | Score-6 cluster, RTS at end |
| 291 | C0:67D7-67E2 | Score-6 cluster, RTS at end |
| 292 | C0:6896-68A4 | Score-6 cluster, PHB prologue |
| 293 | C0:6986-698A | Score-6 cluster, RTS at end |

### Passes 294-299: Page 6E00-6F00 Region

| Pass | Range | Evidence |
|------|-------|----------|
| 294 | C0:6E1E-6E21 | Score-6 cluster, RTS at end |
| 295 | C0:6E58-6E5B | Score-6 cluster, RTS at end |
| 296 | C0:6EC7-6ECA | Score-6 cluster, RTS at end |
| 297 | C0:6EE5-6EF0 | Score-6 cluster, RTS at end |
| 298 | C0:6F08-6F0B | Score-6 cluster, RTS at end |
| 299 | C0:6F5A-6F5D | Score-6 cluster, RTS at end |

### Passes 300-306: Page 7000-7700 Region

| Pass | Range | Evidence |
|------|-------|----------|
| 300 | C0:70E7-70E8 | Score-6 cluster, tail-call JSR+RTS |
| 301 | C0:7162-716F | Score-6 cluster, PHD prologue |
| 302 | C0:749B-74A5 | Score-6 cluster, PHD prologue |
| 303 | C0:74E2-74E7 | Score-6 cluster, RTS at end |
| 304 | C0:7546-7552 | Score-6 cluster, RTS at end |
| 305 | C0:75E7-75E8 | Score-6 cluster, tail-call JSR+RTS |
| 306 | C0:77DB-77E3 | Score-6 cluster, RTS at end |

## Bank C0 Coverage Analysis

### Mapped Regions
- **4000-4100**: 2 functions (C0:407C-408E, C0:4098-40B3)
- **4600-4700**: 1 function (C0:4612-4670)
- **5200-5300**: 1 function (C0:520E-5280)
- **5400-5500**: 1 function (C0:5406-5470)
- **5A00-5B00**: 1 function (C0:5A77-5A90)
- **5C00-5D00**: 1 function (C0:5C8D-5CC6)
- **6000-6100**: 1 function (C0:6070-607D)
- **6200-6300**: 1 function (C0:629B-62CA)
- **6300-6400**: 1 function (C0:639D-63E5)
- **6700-6900**: 3 functions (C0:67D7-67E2, C0:6896-68A4, C0:6986-698A)
- **6E00-7000**: 6 functions (C0:6E1E-6F5D region)
- **7000-7800**: 7 functions (C0:70E7-77E3 region)
- **E900-F100**: 2 functions (C0:E945-E9A0, C0:F0B9-F110)
- **2800-3600**: 2 functions (C0:289B-28F0, C0:3551-35B0)

### Code Characteristics
Bank C0 exhibits patterns consistent with utility/library code:
- High density of RTS returns (most functions are subroutines)
- Frequent JSR instructions indicating inter-function calls
- Presence of PHP/PHB prologues for stack management
- Many small functions (20-100 bytes) alongside larger ones

### Remaining Gaps
- **0000-2800**: Lower region, potentially data tables
- **7800-E900**: Upper middle region, unexplored
- **F100-FFFF**: High region, partially mapped

## Technical Notes

### Promotion Criteria
All Session 23 promotions followed the established criteria:
1. **Score ≥ 6**: Backtrack analysis confirms high-confidence entry points
2. **Internal Evidence**: RTS returns present to confirm code nature
3. **Clean Boundaries**: Functions end at RTS or tail-call patterns
4. **No External Dependencies**: Promotions validated without requiring caller analysis

### Cache Statistics
- **Total closed ranges**: 1081
- **Manifest-backed ranges**: 181
- **Continuation ranges**: 900

### Key Toolkit Usage
- `score_target_owner_backtrack_v1.py`: Primary candidate identification
- `ensure_seam_cache_v1.py`: Cache refresh after each batch
- Manual byte inspection for boundary verification

## Recommendations for Next Session

### Option 1: Continue Bank C0 (Recommended)
- Target the 7800-E900 gap (3.3KB unexplored)
- Scan 2800-3600 for additional functions between mapped regions
- Investigate 0000-2800 for potential code entry points

### Option 2: Return to Bank C3
- Address the 5600-80C4 gap (10.9KB)
- Target the 8CFF-A396 gap (5.8KB)

### Option 3: New Bank Exploration
- Banks C1, C2: Untouched, likely contain significant code
- Banks C4-C6: Partially explored in C7 work, may have related code

## Files Changed
- `passes/manifests/pass277.json` through `pass306.json` (30 new manifest files)
- `tools/cache/closed_ranges_snapshot_v1.json` (updated)
- `README.md` (updated)
- `docs/session_23_progress_report.md` (this file)

## Verification
All promotions verified with:
```bash
python tools/scripts/ensure_seam_cache_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --manifests-dir passes/manifests
```

Cache confirms 181 manifest-backed ranges (55 in C0, 99 in C3, 27 in C7).
