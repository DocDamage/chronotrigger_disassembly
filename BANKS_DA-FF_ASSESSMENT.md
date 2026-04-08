# Banks DA-FF Assessment Report

## Summary
Exploration of the final 6 upper ROM banks (DA-FF) in Chrono Trigger SNES ROM.

| Bank | File Offset | Type | Islands | Clusters | Max Score | Assessment |
|------|-------------|------|---------|----------|-----------|------------|
| **DA** | 0x1A0000-0x1AFFFF | CODE | 803 | 580 | 9 | ⭐ CODE BANK |
| **DB** | 0x1B0000-0x1BFFFF | CODE | 163 | 136 | 8 | CODE BANK (small) |
| **DC** | 0x1C0000-0x1CFFFF | DATA | 150 | 110 | 7 | DATA/MIXED |
| **DD** | 0x1D0000-0x1DFFFF | CODE | 770 | 320 | **19** | ⭐⭐ RICH CODE |
| **DE** | 0x1E0000-0x1EFFFF | CODE | 228 | 118 | 18 | ⭐ CODE BANK |
| **DF** | 0x1F0000-0x1FFFFF | CODE | 809 | 579 | 12 | ⭐ CODE BANK |

---

## Bank DA ($1A0000-$1AFFFF)
**Assessment: CODE BANK**

### Sample Analysis
| Offset | RTS | RTL | JSR | JSL | Unique | Assessment |
|--------|-----|-----|-----|-----|--------|------------|
| +$0000 | 0 | 0 | 2 | 0 | 35 | Code patterns |
| +$4000 | 1 | 0 | 3 | 0 | 30 | Code patterns |
| +$8000 | 0 | 0 | 1 | 2 | 38 | Code patterns |
| +$C000 | 0 | 0 | 1 | 0 | 43 | Code patterns |

### Score 6+ Clusters (Candidates)
| Cluster | Score | Width | Notes |
|---------|-------|-------|-------|
| DA:B148..DA:B17C | 9 | 53 | **Top candidate** |
| DA:D5E6..DA:D609 | 9 | 36 | **Top candidate** |
| DA:C2B4..DA:C2DC | 8 | 41 | **Top candidate** |
| DA:F69F..DA:F6C0 | 8 | 34 | **Top candidate** |
| DA:6301..DA:631B | 8 | 27 | **Top candidate** |
| DA:1219..DA:1230 | 8 | 24 | **Top candidate** |
| DA:EAAF..DA:EAC2 | 8 | 20 | conseq_ident_branch |
| DA:F2DC..DA:F30C | 7 | 49 | Large function |
| DA:7614..DA:7636 | 7 | 35 | |
| DA:00E0..DA:0101 | 7 | 34 | |
| DA:CC73..DA:CC8F | 7 | 29 | |
| DA:10E2..DA:10FB | 7 | 26 | |
| DA:06CE..DA:06E6 | 7 | 25 | |
| DA:081C..DA:0832 | 7 | 23 | |
| DA:5837..DA:584D | 7 | 23 | |
| DA:C544..DA:C559 | 7 | 22 | |
| DA:CD1A..DA:CD2F | 7 | 22 | |
| DA:1281..DA:1294 | 7 | 20 | |
| DA:8383..DA:8395 | 7 | 19 | |
| DA:7300..DA:7311 | 7 | 18 | |
| DA:D063..DA:D073 | 7 | 17 | |
| DA:61F8..DA:6207 | 7 | 16 | |
| DA:3127..DA:3132 | 7 | 12 | |
| DA:5FF4..DA:5FFF | 7 | 12 | |
| DA:82B1..DA:82CC | 6 | 28 | |
| DA:E5AE..DA:E5C8 | 6 | 27 | |
| DA:8EBE..DA:8ED5 | 6 | 24 | |
| DA:8A7E..DA:8A94 | 6 | 23 | consecutive_rts |
| DA:9AFE..DA:9B14 | 6 | 23 | |
| DA:017B..DA:018E | 6 | 20 | |
| DA:57D2..DA:57E5 | 6 | 20 | |
| DA:6AE8..DA:6AFA | 6 | 19 | |
| DA:AE52..DA:AE64 | 6 | 19 | |

**DA Candidate Count:** 32 functions with score 6+

---

## Bank DB ($1B0000-$1BFFFF)
**Assessment: CODE BANK (smaller)**

### Sample Analysis
| Offset | RTS | RTL | JSR | JSL | Unique | Assessment |
|--------|-----|-----|-----|-----|--------|------------|
| +$0000 | 1 | 0 | 2 | 0 | 31 | Code patterns |
| +$4000 | 0 | 0 | 2 | 1 | 39 | Code patterns |
| +$8000 | 0 | 0 | 0 | 0 | 1 | **ALL ZEROS** |
| +$C000 | 0 | 0 | 0 | 0 | 2 | **Sparse data** |

Note: Upper half (+$8000-$FFFF) appears to be mostly empty/zero-filled.

### Score 6+ Clusters
| Cluster | Score | Width | Notes |
|---------|-------|-------|-------|
| DB:5090..DB:50AC | 8 | 29 | **Top candidate** |
| DB:7551..DB:7568 | 8 | 24 | **Top candidate** |
| DB:1D81..DB:1D95 | 7 | 21 | |
| DB:1358..DB:1366 | 7 | 15 | |
| DB:1A53..DB:1A5A | 7 | 8 | |
| DB:0C32..DB:0C4C | 6 | 27 | |
| DB:7966..DB:7973 | 6 | 14 | |
| DB:62B8..DB:62C3 | 6 | 12 | |
| DB:41C2..DB:41CC | 6 | 11 | |

**DB Candidate Count:** 9 functions with score 6+

---

## Bank DC ($1C0000-$1CFFFF)
**Assessment: DATA/MIXED BANK**

### Sample Analysis
| Offset | RTS | RTL | JSR | JSL | Unique | Assessment |
|--------|-----|-----|-----|-----|--------|------------|
| +$0000 | 0 | 0 | 1 | 0 | 24 | Low entropy |
| +$4000 | 0 | 0 | 0 | 0 | 19 | Low entropy |
| +$8000 | 0 | 0 | 0 | 0 | 19 | Low entropy |
| +$C000 | 0 | 0 | 0 | 0 | 24 | Low entropy |

### Score 6+ Clusters
| Cluster | Score | Width | Notes |
|---------|-------|-------|-------|
| DC:D51D..DC:D537 | 7 | 27 | **Top candidate** |
| DC:CE38..DC:CE43 | 6 | 12 | |
| DC:B30A..DC:B313 | 6 | 10 | |
| DC:A394..DC:A39B | 6 | 8 | |

**DC Candidate Count:** 4 functions with score 6+

---

## Bank DD ($1D0000-$1DFFFF)
**Assessment: ⭐⭐ RICHEST CODE BANK**

### Sample Analysis
| Offset | RTS | RTL | JSR | JSL | Unique | Assessment |
|--------|-----|-----|-----|-----|--------|------------|
| +$0000 | 0 | 0 | 0 | 0 | 29 | Low patterns |
| +$4000 | 0 | 0 | 0 | 0 | 27 | Low patterns |
| +$8000 | 0 | 0 | 0 | 0 | 27 | Low patterns |
| +$C000 | 0 | 0 | 0 | 0 | 13 | Low patterns |

Despite low sample patterns, this bank has **EXTREMELY HIGH** code density with score-19 clusters!

### Score 12+ Clusters (Top Tier)
| Cluster | Score | Width | Notes |
|---------|-------|-------|-------|
| DD:973D..DD:975F | **19** | 35 | 🏆 HIGHEST SCORE |
| DD:9B4D..DD:9B6F | **19** | 35 | 🏆 HIGHEST SCORE |
| DD:3407..DD:343D | **13** | 55 | Large function |
| DD:6567..DD:6587 | **13** | 33 | |
| DD:980F..DD:9827 | **13** | 25 | |
| DD:9C1F..DD:9C37 | **13** | 25 | |
| DD:982D..DD:984F | **12** | 35 | |
| DD:9C3D..DD:9C5F | **12** | 35 | |
| DD:45FD..DD:4619 | **12** | 29 | |
| DD:6597..DD:65AF | **12** | 25 | |

### Score 6-11 Clusters (High Value)
| Cluster | Score | Width | Notes |
|---------|-------|-------|-------|
| DD:4B4D..DD:4B69 | 11 | 29 | |
| DD:1EF8..DD:1F0F | 11 | 24 | |
| DD:1027..DD:1037 | 9 | 17 | |
| DD:07B8..DD:07C7 | 9 | 16 | |
| DD:4DB1..DD:4DD7 | 8 | 39 | Large function |
| DD:6605..DD:6625 | 8 | 33 | |
| DD:96C9..DD:96E7 | 8 | 31 | |
| DD:9AD9..DD:9AF7 | 8 | 31 | |
| DD:205D..DD:2077 | 8 | 27 | |
| DD:469D..DD:46AD | 8 | 17 | |
| DD:7310..DD:731F | 8 | 16 | |
| DD:94A9..DD:94DF | 7 | 55 | Large function |
| DD:3187..DD:31A7 | 7 | 33 | |
| DD:09B8..DD:09C7 | 7 | 16 | |
| DD:4F92..DD:4F9F | 7 | 14 | |
| DD:315F..DD:317D | 6 | 31 | |
| DD:689D..DD:68B7 | 6 | 27 | |
| DD:19E1..DD:19F7 | 6 | 23 | sed_decimal |
| DD:1A31..DD:1A47 | 6 | 23 | sed_decimal |
| DD:1FE5..DD:1FFB | 6 | 23 | |
| DD:3B04..DD:3B15 | 6 | 18 | |
| DD:31BF..DD:31CF | 6 | 17 | |
| DD:0228..DD:0237 | 6 | 16 | |
| DD:03B8..DD:03C7 | 6 | 16 | |
| DD:0A48..DD:0A57 | 6 | 16 | |

**DD Candidate Count:** 35+ functions with score 6+

---

## Bank DE ($1E0000-$1EFFFF)
**Assessment: CODE BANK**

### Sample Analysis
| Offset | RTS | RTL | JSR | JSL | Unique | Assessment |
|--------|-----|-----|-----|-----|--------|------------|
| +$0000 | 0 | 0 | 0 | 0 | 21 | Low patterns |
| +$4000 | 0 | 0 | 0 | 0 | 17 | Low patterns |
| +$8000 | 0 | 0 | 0 | 0 | 14 | Low patterns |
| +$C000 | 0 | 0 | 0 | 0 | 41 | Code patterns |

### Score 10+ Clusters (Top Tier)
| Cluster | Score | Width | Notes |
|---------|-------|-------|-------|
| DE:8B35..DE:8B57 | **18** | 35 | 🏆 **Highest in DE** |
| DE:8B5D..DE:8B7F | **13** | 35 | |
| DE:8931..DE:894F | **13** | 31 | |
| DE:8CF7..DE:8D0F | **11** | 25 | |
| DE:8A21..DE:8A3F | **10** | 31 | |

### Score 6-9 Clusters
| Cluster | Score | Width | Notes |
|---------|-------|-------|-------|
| DE:4558..DE:4577 | 7 | 32 | |
| DE:1E20..DE:1E2B | 6 | 12 | |

**DE Candidate Count:** 6 functions with score 6+ (but 5 are score 10+!)

---

## Bank DF ($1F0000-$1FFFFF)
**Assessment: ⭐ CODE BANK**

### Sample Analysis
| Offset | RTS | RTL | JSR | JSL | Unique | Assessment |
|--------|-----|-----|-----|-----|--------|------------|
| +$0000 | 0 | 0 | 3 | 1 | 38 | Code patterns |
| +$4000 | 1 | 0 | 1 | 1 | 44 | Code patterns |
| +$8000 | 0 | 0 | 0 | 0 | 53 | High entropy |
| +$C000 | 1 | 0 | 0 | 0 | 40 | Code patterns |

### Score 8+ Clusters (Top Tier)
| Cluster | Score | Width | Notes |
|---------|-------|-------|-------|
| DF:6497..DF:64BB | **12** | 37 | 🏆 **Highest in DF** |
| DF:EAC0..DF:EAED | **10** | 46 | |
| DF:D6C2..DF:D6EA | **9** | 41 | |
| DF:4F12..DF:4F30 | **9** | 31 | |
| DF:D1F9..DF:D215 | **9** | 29 | |
| DF:F1BA..DF:F1D6 | **9** | 29 | rti_rts_proximity |
| DF:A343..DF:A371 | **8** | 47 | Large function |
| DF:315F..DF:3188 | **8** | 42 | |
| DF:E58D..DF:E5B3 | **8** | 39 | |
| DF:7494..DF:74B6 | **8** | 35 | sed_decimal |
| DF:BBAD..DF:BBC5 | **8** | 25 | |
| DF:D7DB..DF:D7EC | **8** | 18 | |
| DF:C230..DF:C23E | **8** | 15 | |

### Score 7 Clusters (High Value)
| Cluster | Score | Width | Notes |
|---------|-------|-------|-------|
| DF:B80C..DF:B838 | 7 | 45 | sed_decimal |
| DF:E15A..DF:E180 | 7 | 39 | sed_decimal |
| DF:D4C5..DF:D4E5 | 7 | 33 | |
| DF:A52A..DF:A549 | 7 | 32 | |
| DF:DA05..DF:DA21 | 7 | 29 | |
| DF:D86D..DF:D888 | 7 | 28 | |
| DF:C8D7..DF:C8F1 | 7 | 27 | |
| DF:CA6B..DF:CA85 | 7 | 27 | |
| DF:C8AB..DF:C8C4 | 7 | 26 | |
| DF:35A6..DF:35BE | 7 | 25 | |
| DF:7CF3..DF:7D0B | 7 | 25 | |
| DF:AC77..DF:AC8F | 7 | 25 | |
| DF:CCC9..DF:CCE1 | 7 | 25 | rti_rts_proximity |
| DF:D9B3..DF:D9CB | 7 | 25 | |
| DF:F8CF..DF:F8E7 | 7 | 25 | |
| DF:3EAD..DF:3EC4 | 7 | 24 | |
| DF:FA77..DF:FA8D | 7 | 23 | |
| DF:5441..DF:5453 | 7 | 19 | |
| DF:B9BF..DF:B9CE | 7 | 16 | |
| DF:B694..DF:B69E | 7 | 11 | |
| DF:3DCA..DF:3DD3 | 7 | 10 | |

**DF Candidate Count:** 34+ functions with score 7+

---

## Recommendations

### Priority 1: Bank DD (Highest Value)
- **35+ score-6+ functions available**
- Score-19 clusters are exceptional
- Rich code patterns throughout
- **Target for immediate analysis**

### Priority 2: Bank DA
- **32 score-6+ functions**
- Well-distributed code patterns
- Good variety of function sizes

### Priority 3: Bank DF
- **34+ score-7+ functions**
- High density of code
- Final ROM bank (often contains important functions)

### Priority 4: Bank DE
- **6 high-value functions (5 are score 10+!)**
- Smaller but very high quality
- Focus on the score-18 cluster first

### Priority 5: Bank DB
- **9 score-6+ functions**
- Upper half is mostly empty
- Lower half contains code

### Priority 6: Bank DC
- **4 score-6+ functions**
- Mostly data bank
- Only analyze the identified candidates

---

## Target Functions for Documentation (Recommended 8-12)

### Top 12 Recommendations:

1. **DD:973D..DD:975F** (score 19) - Highest score in all banks
2. **DD:9B4D..DD:9B6F** (score 19) - Tied highest
3. **DD:3407..DD:343D** (score 13) - Large function
4. **DD:6567..DD:6587** (score 13)
5. **DD:980F..DD:9827** (score 13)
6. **DE:8B35..DE:8B57** (score 18) - Highest in DE
7. **DE:8B5D..DE:8B7F** (score 13)
8. **DF:6497..DF:64BB** (score 12) - Highest in DF
9. **DA:B148..DA:B17C** (score 9) - Highest in DA
10. **DA:D5E6..DA:D609** (score 9)
11. **DD:4DB1..DD:4DD7** (score 8) - Large function
12. **DA:C2B4..DA:C2DC** (score 8)

---

## Script Commands for Analysis

```bash
# Bank DD (highest priority)
python tools/scripts/find_local_code_islands_v2.py --rom "rom/Chrono Trigger (USA).sfc" --range "DD:973D..DD:975F" --min-width 6

# Bank DE
python tools/scripts/find_local_code_islands_v2.py --rom "rom/Chrono Trigger (USA).sfc" --range "DE:8B35..DE:8B57" --min-width 6

# Bank DF
python tools/scripts/find_local_code_islands_v2.py --rom "rom/Chrono Trigger (USA).sfc" --range "DF:6497..DF:64BB" --min-width 6

# Bank DA
python tools/scripts/find_local_code_islands_v2.py --rom "rom/Chrono Trigger (USA).sfc" --range "DA:B148..DA:B17C" --min-width 6
```

---

*Report generated: 2026-04-08*
*Analysis tool: find_local_code_islands_v2.py*
