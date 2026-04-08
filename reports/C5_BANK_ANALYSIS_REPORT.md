# Bank C5 Deep Scan Analysis Report

**Date:** 2026-04-08
**ROM:** Chrono Trigger (USA).sfc
**Bank:** C5 (major code bank, similar to C0)
**Current Coverage:** 4.10% (31 documented ranges)

---

## Executive Summary

Bank C5 is a major code bank with high potential for function discovery. Deep scan analysis identified **rich code regions** and **multiple score-6+ function candidates**. The bank contains a mix of:
- **Clean code regions** (CODE_CANDIDATE classification)
- **Bytecode/data regions** (PHP/SED/PLP/BRK structural patterns - avoid)
- **High-score function clusters** (score-9 at 9BC1 is highest in C5)

### Key Finding: Score-9 Cluster at C5:9BC1
- **Highest score in C5** (confirmed)
- Part of 9000-AFFF region
- Multiple child functions detected
- Likely dispatch table or related utilities

---

## Data Pattern Analysis by Region

### CODE_CANDIDATE Regions (Recommended for Mapping)

| Region | Size | Classification | PHP | RTS | RTL | Notes |
|--------|------|----------------|-----|-----|-----|-------|
| C5:0000-1000 | 4KB | CODE_CANDIDATE | 31 | 25 | 5 | Bank start - vector/entry functions |
| C5:1000-2000 | 4KB | CODE_CANDIDATE | 43 | 19 | 5 | Clean code region |
| C5:2000-3000 | 4KB | CODE_CANDIDATE | 36 | 29 | 3 | Clean code region |
| C5:3000-4000 | 4KB | CODE_CANDIDATE | 46 | 43 | 4 | Clean code region |
| C5:B000-C000 | 4KB | CODE_CANDIDATE | 73 | 44 | 6 | High code density |
| C5:D000-E000 | 4KB | CODE_CANDIDATE | 39 | 42 | 1 | Score-8 cluster region |
| C5:E000-FFFF | 8KB | CODE_CANDIDATE* | 59 | 47 | 2 | Mixed code/data |

### DATA_ENCODED_CONTROL Regions (Avoid - Bytecode/State Machine)

| Region | Size | Classification | PHP | BRK | Pattern |
|--------|------|----------------|-----|-----|---------|
| C5:4000-6000 | 8KB | DATA_ENCODED_CONTROL | 102 | 869 | PHP/SED/PLP/BRK bytecode |
| C5:6000-8000 | 8KB | DATA_ENCODED_CONTROL | 88 | 796 | Repeating [01 F0 01 F0] |
| C5:9000-AFFF | 8KB | DATA_ENCODED_CONTROL | 128 | 674 | Score-9 cluster within |
| C5:C000-E000 | 8KB | DATA_ENCODED_CONTROL | 109 | 580 | Heavy [01 F0] pattern |

---

## Score-6+ Function Candidates

### Region: C5:0000-1000 (Bank Start)

| Candidate | Score | Target | Distance | Start Byte | Notes |
|-----------|-------|--------|----------|------------|-------|
| **C5:001E** | 6 | C5:001F | 1 | 08 (PHP) | ⭐ EXISTING - Bank entry/vector |
| **C5:03DC** | 6 | C5:03DF | 3 | 08 (PHP) | NEW CANDIDATE |
| **C5:04A7** | 6 | C5:04AD | 6 | 20 (JSR) | ⭐ EXISTING - Score 6 |
| **C5:04CF** | 6 | C5:04D8 | 9 | 20 (JSR) | NEW CANDIDATE |
| **C5:0CBA** | 6 | C5:0CC2 | 8 | 08 (PHP) | NEW CANDIDATE |
| **C5:0EFE** | 6 | C5:0F00 | 2 | 20 (JSR) | NEW CANDIDATE |
| **C5:0D1A** | 7 | C5:0D23 | 8 | 8E | ⭐ EXISTING - Score 7 |

**New Candidates from 0000-1000:** 4

### Region: C5:1000-2000

| Candidate | Score | Target | Distance | Start Byte | Notes |
|-----------|-------|--------|----------|------------|-------|
| **C5:103B** | 6 | C5:1040 | 5 | 48 (PHA) | NEW CANDIDATE |
| **C5:103B** | 6 | C5:1042 | 7 | 48 (PHA) | NEW CANDIDATE |
| **C5:109B** | 6 | C5:10A0 | 5 | A0 (LDY#) | NEW CANDIDATE |
| **C5:11F8** | 6 | C5:1202 | 10 | 20 (JSR) | NEW CANDIDATE |
| **C5:11F8** | 6 | C5:1203 | 11 | 20 (JSR) | NEW CANDIDATE |
| **C5:17FE** | 6 | C5:1804 | 6 | 08 (PHP) | NEW CANDIDATE |
| **C5:18EF** | 6 | C5:18F7 | 8 | 48 (PHA) | NEW CANDIDATE |
| **C5:1909** | 6 | C5:190E | 5 | A0 (LDY#) | NEW CANDIDATE |

**New Candidates from 1000-2000:** 8

### Region: C5:2000-3000

| Candidate | Score | Target | Distance | Start Byte | Notes |
|-----------|-------|--------|----------|------------|-------|
| **C5:2021** | 6 | C5:2023 | 2 | 8B (PHB) | NEW CANDIDATE |
| **C5:21FD** | 6 | C5:2200 | 3 | C2 (REP) | NEW CANDIDATE |
| **C5:27EF** | 6 | C5:27F0 | 1 | 0B (PHD) | NEW CANDIDATE |

**New Candidates from 2000-3000:** 3

### Region: C5:4000-5000

| Candidate | Score | Target | Distance | Start Byte | Notes |
|-----------|-------|--------|----------|------------|-------|
| **C5:4206** | 6 | C5:4208 | 2 | 08 (PHP) | ⭐ EXISTING - Score 6 |

**New Candidates from 4000-5000:** 0 (region is mostly bytecode data)

### Region: C5:6000-7000

| Candidate | Score | Target | Distance | Start Byte | Notes |
|-----------|-------|--------|----------|------------|-------|
| **C5:6272** | 7 | - | - | - | ⭐ EXISTING - Score 7 |
| **C5:69F5** | 7 | - | - | - | ⭐ EXISTING - Score 7 |

**New Candidates from 6000-7000:** 0 (region is bytecode data)

### Region: C5:8000-9000

| Candidate | Score | Target | Distance | Start Byte | Notes |
|-----------|-------|--------|----------|------------|-------|
| **C5:804F** | 6 | C5:8050 | 1 | 20 (JSR) | ⭐ EXISTING - Score 6 |
| **C5:80DE** | 6 | C5:80DF | 1 | 08 (PHP) | NEW CANDIDATE |

**New Candidates from 8000-9000:** 1

### Region: C5:9000-A000 (Score-9 Area)

| Candidate | Score | Target | Distance | Start Byte | Notes |
|-----------|-------|--------|----------|------------|-------|
| **C5:9BC1** | 9 | - | - | - | ⭐ EXISTING - HIGHEST IN C5 |
| **C5:9BF3** | 4 | C5:9C00 | 13 | A0 (LDY#) | Related to 9BC1 cluster |
| **C5:9C25** | 6 | C5:9C34 | 15 | 4B (PHK) | NEW CANDIDATE (in cluster) |
| **C5:9F66** | 7 | - | - | - | ⭐ EXISTING - Score 7 |

**New Candidates from 9000-A000:** 1 (plus cluster expansion)

### Region: C5:B000-C000

| Candidate | Score | Target | Distance | Start Byte | Notes |
|-----------|-------|--------|----------|------------|-------|
| **C5:B03F** | 6 | C5:B040 | 1 | 20 (JSR) | NEW CANDIDATE |
| **C5:B03F** | 6 | C5:B04F | 16 | 20 (JSR) | NEW CANDIDATE (wider) |
| **C5:B097** | 6 | C5:B098 | 1 | C2 (REP) | NEW CANDIDATE |
| **C5:B0D5** | 6 | C5:B0DB | 6 | A0 (LDY#) | NEW CANDIDATE |
| **C5:B4B1** | 6 | C5:B4BC | 11 | 08 (PHP) | NEW CANDIDATE |
| **C5:B4D7** | 6 | C5:B4D8 | 1 | 08 (PHP) | NEW CANDIDATE |
| **C5:B73F** | 6 | C5:B740 | 1 | 20 (JSR) | NEW CANDIDATE |
| **C5:B85E** | 6 | C5:B860 | 2 | A0 (LDY#) | NEW CANDIDATE |
| **C5:BBFD** | 6 | C5:BC08 | 11 | 0B (PHD) | NEW CANDIDATE |
| **C5:BF2D** | 6 | C5:BF2F | 2 | 20 (JSR) | NEW CANDIDATE |
| **C5:BF2D** | 6 | C5:BF30 | 3 | 20 (JSR) | NEW CANDIDATE |

**New Candidates from B000-C000:** 11

### Region: C5:C000-D000

| Candidate | Score | Target | Distance | Start Byte | Notes |
|-----------|-------|--------|----------|------------|-------|
| **C5:C030** | 6 | C5:C034 | 4 | 08 (PHP) | ⭐ EXISTING - Score 6 |
| **C5:C036** | 6 | C5:C038 | 2 | 20 (JSR) | ⭐ EXISTING - Score 6 |
| **C5:C0B7** | 6 | C5:C0C0 | 9 | 22 (JSL) | NEW CANDIDATE |
| **C5:C0EA** | 6 | C5:C0F4 | 10 | 08 (PHP) | NEW CANDIDATE |
| **C5:C1E6** | 6 | C5:C1EF | 9 | 20 (JSR) | NEW CANDIDATE |
| **C5:CEF2** | 6 | C5:CF00 | 14 | 08 (PHP) | NEW CANDIDATE |
| **C5:CB70** | 7 | - | - | - | ⭐ EXISTING - Score 7 |

**New Candidates from C000-D000:** 4

### Region: C5:D000-E000 (Score-8 Area)

| Candidate | Score | Target | Distance | Start Byte | Notes |
|-----------|-------|--------|----------|------------|-------|
| **C5:DC49** | 8 | - | - | - | ⭐ EXISTING - Score 8 |
| **C5:DB2B** | 7 | - | - | - | ⭐ EXISTING - Score 7 |
| **C5:DCB6** | 6 | C5:DCBC | 6 | 20 (JSR) | NEW CANDIDATE |
| **C5:DF2E** | 6 | C5:DF38 | 10 | 20 (JSR) | NEW CANDIDATE |

**New Candidates from D000-E000:** 2

### Region: C5:E000-F000

| Candidate | Score | Target | Distance | Start Byte | Notes |
|-----------|-------|--------|----------|------------|-------|
| **C5:E017** | 6 | C5:E01F | 8 | 08 (PHP) | NEW CANDIDATE |
| **C5:E017** | 6 | C5:E020 | 9 | 08 (PHP) | NEW CANDIDATE (shared entry) |
| **C5:E026** | 6 | C5:E02F | 9 | 20 (JSR) | NEW CANDIDATE |
| **C5:E4E6** | 6 | C5:E4F0 | 10 | A0 (LDY#) | NEW CANDIDATE |
| **C5:E781** | 6 | C5:E790 | 15 | 08 (PHP) | NEW CANDIDATE |
| **C5:E8F6** | 6 | C5:E902 | 12 | 0B (PHD) | NEW CANDIDATE |
| **C5:EFF9** | 6 | C5:F000 | 7 | 20 (JSR) | NEW CANDIDATE |

**New Candidates from E000-F000:** 7

---

## Summary: Score-6+ Candidates

### Existing Labels (15):
- C5:001E (score 6)
- C5:04A7 (score 6)
- C5:0D1A (score 7)
- C5:4206 (score 6)
- C5:6272 (score 7)
- C5:69F5 (score 7)
- C5:804F (score 6)
- C5:9BC1 (score 9) - **HIGHEST**
- C5:9F66 (score 7)
- C5:C030 (score 6)
- C5:C036 (score 6)
- C5:CB70 (score 7)
- C5:DB2B (score 7)
- C5:DC49 (score 8)

### New Candidates Identified: **40+**

---

## Recommended Manifests (Priority Order)

### Tier 1: High Confidence (Score 6+, Clean Prologue)

1. **C5:001E** (already exists) - Bank entry, PHP prologue
2. **C5:04A7** (already exists) - JSR prologue
3. **C5:0D1A** (already exists) - Score 7
4. **C5:103B** - PHA prologue, dual targets
5. **C5:109B** - LDY# immediate
6. **C5:11F8** - JSR prologue, dual targets
7. **C5:17FE** - PHP prologue
8. **C5:1909** - LDY# immediate
9. **C5:2021** - PHB prologue
10. **C5:21FD** - REP prologue (mode set)
11. **C5:27EF** - PHD prologue
12. **C5:4206** (already exists) - PHP prologue
13. **C5:804F** (already exists) - JSR prologue
14. **C5:80DE** - PHP prologue
15. **C5:9BC1** (already exists) - **HIGHEST SCORE 9**
16. **C5:B03F** - JSR prologue, dual targets
17. **C5:B097** - REP prologue
18. **C5:B0D5** - LDY# immediate

### Tier 2: Medium Confidence (Score 6, Good Context)

19. **C5:03DC** - PHP prologue
20. **C5:04CF** - JSR prologue
21. **C5:0CBA** - PHP prologue
22. **C5:0EFE** - JSR prologue
23. **C5:18EF** - PHA prologue
24. **C5:6272** (already exists) - Score 7
25. **C5:69F5** (already exists) - Score 7
26. **C5:B4B1** - PHP prologue
27. **C5:B4D7** - PHP prologue
28. **C5:B73F** - JSR prologue
29. **C5:B85E** - LDY# immediate
30. **C5:BBFD** - PHD prologue
31. **C5:BF2D** - JSR prologue, dual targets
32. **C5:C0B7** - JSL long call
33. **C5:C0EA** - PHP prologue
34. **C5:C1E6** - JSR prologue
35. **C5:CB70** (already exists) - Score 7
36. **C5:CEF2** - PHP prologue
37. **C5:DC49** (already exists) - Score 8
38. **C5:DCB6** - JSR prologue
39. **C5:DB2B** (already exists) - Score 7
40. **C5:DF2E** - JSR prologue

### Tier 3: Extended Candidates (E000-FFFF)

41. **C5:E017** - PHP prologue, dual targets (E01F, E020)
42. **C5:E026** - JSR prologue
43. **C5:E4E6** - LDY# immediate
44. **C5:E781** - PHP prologue
45. **C5:E8F6** - PHD prologue
46. **C5:EFF9** - JSR prologue

---

## Regions to AVOID (Data/Bytecode)

| Region | Reason |
|--------|--------|
| C5:4000-5FFF | PHP/SED/PLP/BRK bytecode pattern |
| C5:6000-7FFF | PHP/SED/PLP/BRK bytecode pattern |
| C5:8000-8FFF | Repeating structural pattern [01 F0 01 F0] |
| C5:9000-AFFF | Data-encoded control (contains 9BC1 cluster though) |
| C5:C000-DFFF | Heavy [01 F0] repeating pattern |

---

## Next Steps

1. **Create manifests** for Tier 1 candidates (18 functions)
2. **Verify** 9BC1 cluster boundaries (highest score in C5)
3. **Expand** D000-E000 region mapping (score-8 area)
4. **Cross-reference** callers to validate entry points
5. **Avoid** 4000-BFFF data regions (except isolated clusters)

---

## Statistics

- **Total Score-6+ Candidates:** 46
- **Already Documented:** 15
- **New Candidates:** 31
- **Recommended for Immediate Manifests:** 18
- **Code Regions Identified:** 7 (28KB)
- **Data Regions Identified:** 5 (32KB)
- **Coverage Potential:** 28KB / 64KB = ~44% mappable

---

*Report generated by deep scan analysis tools*
*Scripts: detect_data_patterns_v1.py, score_target_owner_backtrack_v1.py, run_seam_block_v1.py*
