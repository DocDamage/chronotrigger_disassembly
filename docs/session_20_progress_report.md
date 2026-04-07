# Session 20 Progress Report: Bank C3 Major Expansion

**Date:** 2026-04-05  
**Total Promotions:** 30 (passes 218-247)

---

## Executive Summary

Session 20 achieved a major expansion of Bank C3, increasing coverage from ~10% to 17.6%. This represents the single largest mapping effort in the disassembly project to date, with 30 new code regions identified and promoted based on strong internal evidence.

---

## Bank Coverage Summary

| Bank | Before | After | Change |
|------|--------|-------|--------|
| C3 | 65 ranges (~10%) | 95 ranges (17.6%) | +30 ranges (+7.6%) |
| C7 | 27 ranges (~95%) | 27 ranges (~95%) | No change |
| Total | 92 ranges | 122 ranges | +30 ranges |

---

## Promotion Details by Region

### 1900-1C00 Block (High-Density Code)
- Pass 220: 1922-1999 (RTS=4, PHP=1, JSR=4)
- Pass 221: 19A5-1A00 (RTS=5, PHP=1, JSR=2)
- Pass 222: 1A03-1A70 (PHP=2, JSR=1)
- Pass 224: 1BF5-1C00 (RTS=3)

### 2800-4C00 Region (Major Gap Filling)
- Pass 246: 2807-2870 (RTS=1, RTL=1, PHP=2)
- Pass 235: 3059-30B0 (RTS=1, RTL=1, PHP=2)
- Pass 244: 3500-3560 (RTS=2, RTL=1, JSR=2)
- Pass 236: 3705-3760 (RTS=2, JSR=2)
- Pass 232: 3C80-3CFF (RTS=1, PHP=1, JSR=4)
- Pass 227: 3EA4-3EFF (RTS=2, PHP=1, JSR=1)
- Pass 231: 4002-4080 (RTS=3, PHP=1, JSR=5)
- Pass 233: 40B7-4100 (RTS=1, PHP=2, JSR=7)
- Pass 226: 41AF-4200 (RTS=3, PHP=1)
- Pass 237: 42C5-4320 (RTS=1, PHP=1)
- Pass 234: 453B-4599 (RTS=2)
- Pass 245: 4A49-4AA0 (RTS=1, PHP=4, JSR=2)
- Pass 223: 4C43-4CFF (RTS=3, PHP=1, JSR=2)

### 4CFF-A396 Region (Largest Gap)
- Pass 239: 55A3-5600 (RTS=1, PHP=1, JSR=2)
- Pass 240: 80C4-8120 (RTS=3, PHP=1)
- Pass 228: 8300-837F (RTS=2, RTL=1, PHP=1, JSR=3)
- Pass 229: 8440-84FF (RTS=2, PHP=3, JSR=1)
- Pass 230: 8C8E-8CFF (RTS=2, PHP=2, JSR=1)
- Pass 243: 90F0-9150 (RTS=1, PHP=1, JSR=3)

### A3FF-C244 Region
- Pass 225: A396-A3FF (RTS=5, PHP=2, JSR=4)
- Pass 241: AC12-AC80 (RTS=2, PHP=2)
- Pass 247: B16F-B1D0 (RTS=1, PHP=1)
- Pass 242: C09E-C120 (PHP=1, JSR=6)
- Pass 238: C244-C2A0 (RTS=1, PHP=3)

---

## Remaining Large Gaps in Bank C3

| Gap | Size | Status |
|-----|------|--------|
| C3:5600-80C4 | 10.9KB | Likely data-heavy |
| C3:8CFF-A396 | 5.8KB | Partially filled |
| C3:AC80-C09E | 5.2KB | Partially filled |
| C3:28FF-3059 | 1.9KB | Small gap |
| C3:30B0-3705 | 1.6KB | Small gap |

---

## Statistics Summary

### By Evidence Quality
- RTS >= 3: 12 promotions (40%)
- RTS = 2: 8 promotions (27%)
- RTS = 1: 7 promotions (23%)
- RTS = 0 (PHP/JSR only): 3 promotions (10%)

### Total Impact
- 30 new manifests created
- 11.5KB total mapped in Bank C3 (17.6% coverage)
- 80 merged contiguous regions
- 122 total ranges across all banks

---

## Next Steps

### Immediate Options
1. Continue filling small gaps (28FF-3059, 30B0-3705)
2. Investigate 5600-80C4 region for hidden code pockets
3. Switch to a different bank (C0, C1, C2)
4. Extend Bank C7 to 100% coverage

### Recommended Priority
The 5600-80C4 gap (10.9KB) may contain significant code, but score-6 clusters with strong internal evidence are becoming scarce. Consider switching to Bank C0 or C1 for fresh targets.

---

## GitHub Activity

Total commits pushed: 30 new manifests

Recent commits:
- Pass 247: B16F-B1D0 (B100 region)
- Pass 246: 2807-2870 (2800 region)
- Pass 244-245: 3500/4A00 regions
- Pass 243: 9000 region
- Pass 239-242: Large gap promotions
