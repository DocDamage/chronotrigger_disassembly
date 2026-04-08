# Bank C2 Analysis Report

**Date:** 2026-04-08  
**Analyst:** Kimi Code CLI  
**ROM:** Chrono Trigger (USA).sfc

## Executive Summary

Analyzed two key regions in Bank C2:
1. **Vector Table Region (C2:0000-1000)**: Contains initialization vectors and entry points
2. **High-Score Cluster Region (C2:B700-B800)**: Contains documented score-8 cluster and related functions

**Current Bank C2 Coverage:** 2 documented ranges (0.42%)

---

## 1. Vector Table Analysis (C2:0000-1000)

### Vector Table Entries

| Address | Instruction | Target | Description |
|---------|-------------|--------|-------------|
| C2:0000 | JMP $000F | C2:000F | Reset/Init Vector (main entry) |
| C2:0003 | JMP $57DF | C2:57DF | Unknown Vector 1 |
| C2:0006 | JMP $57DF | C2:57DF | Unknown Vector 2 (duplicate) |
| C2:0009 | JMP $5823 | C2:5823 | Unknown Vector 3 |
| C2:000C | JMP $5823 | C2:5823 | Unknown Vector 4 (duplicate) |

### C2:000F - Initialization Code Entry Point

```hex
C2:000F: 78 E2 20 C2 10 A9 00 8D 00 42 8D 0B 42 8D 0C 42
C2:001F: A9 8F 8D 00 21 A9 01 8D 0D 42 A9 00 48 AB EB A9
C2:002F: 00 5B 20 43 00 20 2F 01 20 10 01 20 EF 03 20 B5
C2:003F: 1D 4C
```

**Disassembly Analysis:**
- `78` - SEI (Set Interrupt Disable)
- `E2 20` - SEP #$20 (Set 8-bit accumulator)
- `C2 10` - REP #$10 (Set 16-bit index registers)
- This is classic SNES initialization code prologue

**Calls from C2:000F-0100:**
- JSR $0043 (C2:0031)
- JSR $012F (C2:0034)
- JSR $0110 (C2:0037)
- JSR $03EF (C2:003A)
- JSR $1DB5 (C2:003D)

**Returns found:**
- RTS at C2:0049

### Score-8 Cluster (C2:032C-0350)

```hex
C2:032C: 4D 0C 64 4D 20 4D 03 20 1D 05 20 EA 0C A9 01 04
C2:033C: 4C C2 20 AB 2B 7A FA 68 40 40 A5 4B C5 4B F0 FC
C2:034C: 60 E2 30 A2 60
```

- Ends with `60` (RTS) - Valid function return
- Multiple JSR calls within region
- Score: 8 (highest in C2:0000-1000)

### Score-6 Clusters Identified

| Range | Score | Description |
|-------|-------|-------------|
| C2:0465..C2:0477 | 6 | Ends with RTS at C2:046D |
| C2:04D7..C2:04E8 | 6 | Valid function structure |
| C2:0582..C2:059A | 6 | Ends with RTS |
| C2:0686..C2:069E | 6 | Ends with RTS |

---

## 2. C2:B716 Cluster Analysis

### Documented Score-8 Cluster (C2:B716..C2:B7A0)

```hex
C2:B716: 0F C5 81 F0 03 20 C2 EA 20 1F BB 20 01 BE 20 EB
C2:B726: BD A2 1B FC 20 85 83 28 60 A5 54 D0 07 AD 4A 0F
C2:B736: F0 09 80 08 AD 4A 0F C5 57 90 01 60
```

- **Score:** 8 (highest in Bank C2)
- **Ends with:** `60` (RTS) at C2:B741
- **Prologue:** PHP/REP pattern
- **Cross-bank callers:** 28+ callers from banks C0, C1, C2, C4, C5, C6, CB, D2-D9, DA, DB

### Adjacent Score-6 Cluster (C2:B7B3..C2:B7CB)

```hex
C2:B7B3: 20 9C 11 0D AD 4A 0F 20 A6 8B 8D 95 0D A2 10 97
C2:B7C3: 8E 94 96 A9 80 0C 13 0D 60
```

- **Score:** 6
- **Ends with:** `60` (RTS) at C2:B7CB
- **Related to:** C2:B716 cluster

### Small Function (C2:B7E3..C2:B7E8)

```hex
C2:B7E3: 85 8A 20 2B EF 60
```

- **Score:** 3
- **Ends with:** `60` (RTS)
- Small utility function (5 bytes)

---

## 3. Cross-Bank Call Analysis for C2:B700-B800

Functions in the C2:B700-B800 region are called from **15 different banks**:

| Caller Bank | Sample Call Target |
|-------------|-------------------|
| C0 | C2:B7A6, C2:B701, C2:B788, C2:B700 |
| C1 | C2:B7F2, C2:B70E, C2:B725, C2:B762 |
| C2 | C2:B7C8, C2:B72F, C2:B7CC (internal) |
| C4 | C2:B781, C2:B7F9 |
| C5 | C2:B740, C2:B800 |
| C6 | C2:B74A |
| CB | C2:B7C7 |
| D2-D9 | Multiple targets |
| DA | C2:B7F8, C2:B800 |
| DB | C2:B733 |

This region is a **major cross-bank hub** for Bank C2 functionality.

---

## 4. Additional Score-6+ Candidates

### C2:1000-2000 Region

| Candidate | Score | Range | Start Byte |
|-----------|-------|-------|------------|
| C2:1011 | 6 | C2:1011..C2:10A8 | C2 (REP) |
| C2:10A3 | 6 | C2:10A3..C2:1125 | 20 (JSR) |
| C2:11A4 | 6 | C2:11A4..C2:1225 | 20 (JSR) |
| C2:154E | 6 | C2:154E..C2:15DA | 20 (JSR) |
| C2:166B | 6 | C2:166B..C2:16ED | 0B (PHD) |
| C2:16AC | 6 | C2:16AC..C2:172D | C2 (REP) |
| C2:1889 | 6 | C2:1889..C2:190A | C2 (REP) |

### C2:3000-4000 Region

| Candidate | Score | Range | Start Byte |
|-----------|-------|-------|------------|
| C2:3001 | 6 | C2:3001..C2:3082 | 20 (JSR) |
| C2:308A | 6 | C2:308A..C2:311C | A9 (LDA#) |
| C2:3772 | 6 | C2:3772..C2:37FC | C2 (REP) |
| C2:3915 | 6 | C2:3915..C2:399C | 20 (JSR) |
| C2:3984 | 6 | C2:3984..C2:3A07 | 08 (PHP) |

### C2:5000-6000 Region

| Candidate | Score | Range | Start Byte |
|-----------|-------|-------|------------|
| C2:5319 | 6 | C2:5319..C2:539D | 20 (JSR) |
| C2:5372 | 6 | C2:5372..C2:53F4 | 20 (JSR) |
| C2:55AC | 6 | C2:55AC..C2:562D | C2 (REP) |
| C2:5793 | 6 | C2:5793..C2:5818 | C2 (REP) |
| C2:59F9 | 6 | C2:59F9..C2:5A7C | 20 (JSR) |

### C2:8000-9000 Region

| Candidate | Score | Range | Start Byte |
|-----------|-------|-------|------------|
| C2:8006 | 6 | C2:8006..C2:8090 | 20 (JSR) |
| C2:8118 | 6 | C2:8118..C2:81A0 | A2 (LDX#) |
| C2:8167 | 6 | C2:8167..C2:81EA | DA (PHX) |
| C2:8249 | 6 | C2:8249..C2:82D5 | 08 (PHP) |
| C2:8385 | 6 | C2:8385..C2:840E | 08 (PHP) |
| C2:84D1 | 6 | C2:84D1..C2:8552 | 20 (JSR) |

---

## 5. Recommended New Manifests

Based on analysis, the following functions are recommended for promotion:

### High Priority (Score 8)

```json
{
  "pass_number": 579,
  "closed_ranges": [
    {
      "range": "C2:032C..C2:0350",
      "kind": "owner",
      "label": "ct_c2_032c_init_handler_score8",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-8 cluster in vector table region. RTS-terminated function with multiple internal JSR calls."
}
```

### Medium Priority (Score 6-7)

1. **C2:000F..C2:0050** - Initialization entry point (vector target)
2. **C2:0465..C2:0477** - Score-6 function with RTS
3. **C2:04D7..C2:04E8** - Score-6 function with RTS
4. **C2:0582..C2:059A** - Score-6 function with RTS
5. **C2:0686..C2:069E** - Score-6 function with RTS
6. **C2:B7B3..C2:B7CB** - Adjacent to documented B716 cluster
7. **C2:B7E3..C2:B7E8** - Small utility function (5 bytes)
8. **C2:8006..C2:8090** - Score-6 function in 8000 region
9. **C2:8249..C2:82D5** - Score-6 near documented 823C function
10. **C2:5319..C2:539D** - Score-6 function in 5000 region

### Total Recommended: 11 new manifests

---

## 6. Summary Statistics

| Metric | Value |
|--------|-------|
| Current C2 Coverage | 2 ranges (0.42%) |
| Score-8 Clusters Found | 2 (C2:B716, C2:032C) |
| Score-6+ Clusters Found | 40+ |
| Cross-Bank Callers to B700-B800 | 28+ from 15 banks |
| Vector Table Entries | 5 (2 unique targets) |
| Recommended New Manifests | 11 |

---

## 7. Next Steps

1. Promote **C2:032C..C2:0350** (score-8 cluster) first
2. Document **C2:000F** initialization entry point
3. Continue scanning C2:1000-8000 for additional clusters
4. Verify call relationships between identified functions
5. Check for data tables between functions

---

*Report generated by Bank C2 Analysis Tool*
