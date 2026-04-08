# Bank CF Exploration Report

**Date:** 2026-04-08  
**Status:** COMPLETE - Initial Reconnaissance  
**Bank Range:** CF:0000..CF:FFFF (0xF0000-0xFFFFF)

---

## Executive Summary

Bank CF is a **MAJOR UNEXPLORED CODE BANK** with extensive function code distributed throughout the upper half (CF:8000-FFFF). Currently has **zero documented ranges** and no existing labels or manifests.

---

## Initial Sampling Results

| Region | Code Density | Assessment |
|--------|--------------|------------|
| CF:0000 | 0 | Data/Tables only |
| CF:4000 | 1 | Data/Bitmasks |
| CF:8000 | 134 | **VERY HIGH** - Dispatch/jump table region |
| CF:C000 | 50 | **HIGH** - Code region |

---

## High-Density Code Regions (1KB chunks, score >= 20)

| Offset | Score | RTS | RTL | JSR | JSL | Assessment |
|--------|-------|-----|-----|-----|-----|------------|
| CF:8000 | 301 | 4 | 0 | 208 | 84 | **DISPATCH TABLE** |
| CF:A000 | 285 | 12 | 6 | 227 | 37 | **MAJOR CODE** |
| CF:A400 | 277 | 2 | 2 | 189 | 82 | **MAJOR CODE** |
| CF:D400 | 200 | 6 | 16 | 174 | 2 | **MAJOR CODE** |
| CF:DC00 | 203 | 7 | 5 | 184 | 5 | **MAJOR CODE** |
| CF:B800 | 188 | 3 | 1 | 163 | 21 | **MAJOR CODE** |
| CF:B000 | 148 | 3 | 3 | 135 | 5 | **MAJOR CODE** |
| CF:8C00 | 149 | 5 | 0 | 104 | 35 | Code region |
| CF:8400 | 137 | 2 | 0 | 79 | 50 | Code region |
| CF:CC00 | 130 | 4 | 4 | 114 | 6 | Code region |

**Total: 39 high-density code regions identified**

---

## Code Island Analysis Results

| Region | Islands | Clusters | Max Score | Best Cluster |
|--------|---------|----------|-----------|--------------|
| CF:8000-9000 | 28 | 24 | 7 | CF:8C39..CF:8C68 |
| CF:A000-B000 | 20 | 15 | 9 | CF:A16E..CF:A1A7 |
| CF:D000-E000 | 51 | 22 | 10 | CF:D41E..CF:D47A |
| CF:E000-F000 | 28 | 25 | 8 | CF:ECE2..CF:ED17 |
| CF:F000-FFFF | 65 | 44 | 8 | CF:F606..CF:F635 |
| CF:6400-7000 | 23 | 15 | 8 | CF:6BA0..CF:6BC4 |

**Total: 215 code islands in 165 clusters**

---

## Score-6+ Candidates (Backtrack Analysis)

### CF:D000-FFFF (39 candidates)

| Candidate | Target | Score | Distance | Start | Type |
|-----------|--------|-------|----------|-------|------|
| CF:E777 | CF:E781 | 6 | 10 | A0 | LDY# |
| CF:E8F1 | CF:E906 | 6 | 21 | 20 | JSR |
| CF:E97F | CF:E99C | 6 | 29 | 20 | JSR |
| CF:ECE0 | CF:ECEB | 6 | 11 | A2 | LDX# |
| CF:ECFB | CF:ED18 | 6 | 29 | A2 | LDX# |
| CF:F003 | CF:F01F | 6 | 28 | A2 | LDX# |
| CF:F063 | CF:F06F | 6 | 12 | 20 | JSR |
| CF:F18A | CF:F193 | 6 | 9 | 08 | PHP |
| CF:F39F | CF:F3BA | 6 | 27 | 20 | JSR |
| CF:F5FB | CF:F619 | 6 | 30 | A2 | LDX# |
| CF:FAC3 | CF:FADD | 6 | 26 | A9 | LDA# |
| CF:FB63 | CF:FB65 | 6 | 2 | A0 | LDY# |
| CF:FCEF | CF:FCFB | 6 | 7 | C2 | REP |
| CF:FD1D | CF:FD36 | 6 | 25 | A9 | LDA# |
| CF:FD51 | CF:FD6A | 6 | 25 | A9 | LDA# |

### CF:A000-B000 (4 candidates)

| Candidate | Target | Score | Distance | Start | Type |
|-----------|--------|-------|----------|-------|------|
| CF:A0DF | CF:A0FF | 4 | 32 | 20 | JSR |
| CF:A151 | CF:A163 | 4 | 18 | 20 | JSR |
| CF:A170 | CF:A17F | 4 | 15 | 48 | PHA |
| CF:A1A5 | CF:A1C5 | 4 | 32 | 20 | JSR |

---

## Recommended New Manifest Ranges

### Priority 1 (Score 8-10)

```
CF:A16E..CF:A1A7    cluster_score=9   width=58
CF:D41E..CF:D47A    cluster_score=10  width=93
CF:D284..CF:D2BE    cluster_score=8   width=59
CF:D3B0..CF:D3EA    cluster_score=8   width=59
CF:DAF0..CF:DB2A    cluster_score=8   width=59
CF:ECE2..CF:ED17    cluster_score=8   width=54
```

### Priority 2 (Score 6-7)

```
CF:8C39..CF:8C68    cluster_score=7   width=48
CF:8C72..CF:8C95    cluster_score=6   width=36
CF:A256..CF:A279    cluster_score=5   width=36  (backtrack score 6)
CF:D5A7..CF:D5D6    cluster_score=7   width=48
CF:F606..CF:F635    cluster_score=8   width=48
CF:F3DC..CF:F404    cluster_score=8   width=41
CF:FD85..CF:FDAC    cluster_score=8   width=40
```

---

## Bank Comparison

| Metric | CF:8000-9000 | C0:8000-9000 |
|--------|--------------|--------------|
| Islands | 28 | 79 |
| Clusters | 24 | 64 |
| Max Score | 7 | 6 |

Bank CF has ~35% the code density of Bank C0 in the same range, but CF:8000-9000 appears to be a **dispatch table region** with many JSR/JSL instructions pointing to functions elsewhere in the bank.

---

## Bank CF Content Assessment

| Range | Content Type |
|-------|--------------|
| CF:0000-4000 | Data tables, bitmasks, configuration data |
| CF:4000-6000 | Sparse code, data tables |
| CF:6000-8000 | Code regions with moderate density |
| CF:8000-A000 | **Dispatch tables, jump tables, function vectors** |
| CF:A000-D000 | **MAJOR CODE REGION** - High function density |
| CF:D000-FFFF | **MAJOR CODE REGION** - Very high function density |

---

## Potential Function Purpose

Based on location (upper banks C0-CF) and code patterns:

- **Audio/SPC driver code** - Common for upper bank placement
- **Save game management** - Often in dedicated banks
- **System/kernel utilities** - High code density suggests core functions
- **Interrupt handlers** - RTL usage suggests interrupt returns
- **DMA transfer routines** - Common in upper banks

---

## Next Steps Recommendation

1. **Create manifests** for the 15+ score-6+ candidates identified
2. **Run seam block analysis** on CF:8000-9000 to resolve dispatch table structure
3. **Cross-reference** with calling banks to understand function purposes
4. **Document CF:A000-FFFF first** - Most promising continuous code region
5. **Look for string references** to identify audio/save functionality

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Code Islands | 215+ |
| High-Confidence Functions (score 6+) | 43+ |
| High-Density 1KB Regions | 39 |
| Clusters | 165 |
| Current Manifests | 0 |

**Most Promising Region:** CF:A000-FFFF (continuous high-density code)
