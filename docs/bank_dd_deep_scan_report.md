# Bank DD Deep Scan Report

**Date:** Session 14  
**Bank:** DD (0x1D0000-0x1DFFFF in ROM)  
**Scan Tool:** `find_local_code_islands_v2.py` with `--max-back 48`

---

## Executive Summary

Bank DD is confirmed as the **RICHEST code bank** in the Chrono Trigger ROM with:
- **61 score-6+ clusters** identified (exceeding target of 20-25!)
- **2 score-20 clusters** (THE HIGHEST SCORES FOUND!)
- **6 score-14 clusters** (high-value targets)
- **3 score-13 clusters** (strong candidates)
- **32 score-6 clusters** (solid function candidates)

---

## 🏆 TIER 1: Score-20 MEGA CLUSTERS (Document Immediately!)

### DD:973D..DD:975F (Score 20)
- **Width:** 35 bytes
- **Returns:** 16 (RTI/RTS opcodes)
- **Calls:** 2 (JSR/JSL)
- **Branches:** 3
- **Child Count:** 16 overlapping islands
- **Analysis:** Highly dense code region with multiple return points
- **Status:** ⭐ PRIORITY 1 - Document as pass

### DD:9B4D..DD:9B6F (Score 20)
- **Width:** 35 bytes
- **Returns:** 16
- **Calls:** 2
- **Branches:** 3
- **Child Count:** 16 overlapping islands
- **Analysis:** Mirror structure of DD:973D cluster - possibly related functions
- **Status:** ⭐ PRIORITY 1 - Document as pass

**Recommended Manifests:**
```json
{"pass": 849, "bank": "DD", "address": "973D", "length": 35, "type": "code", "confidence": "high", "score": 20}
{"pass": 850, "bank": "DD", "address": "9B4D", "length": 35, "type": "code", "confidence": "high", "score": 20}
```

---

## 🥈 TIER 2: Score-14 HIGH-VALUE CLUSTERS

### DD:3407..DD:343D (Score 14)
- **Region:** DD:0000-4000 (lower bank)
- **Width:** 55 bytes (LARGEST by size!)
- **Returns:** 23
- **Calls:** 0
- **Analysis:** Large code block with many exit points

### DD:45FD..DD:4619 (Score 14)
- **Region:** DD:4000-8000 (mid bank)
- **Width:** 29 bytes
- **Returns:** 14
- **Calls:** 1

### DD:982D..DD:984F (Score 14)
- **Region:** DD:8000-C000 (upper bank)
- **Width:** 35 bytes
- **Returns:** 16
- **Calls:** 0
- **Branches:** 4

### DD:9C3D..DD:9C5F (Score 14)
- **Region:** DD:8000-C000 (upper bank)
- **Width:** 35 bytes
- **Returns:** 16
- **Calls:** 0
- **Branches:** 4

### DD:980F..DD:9827 (Score 14)
- **Width:** 25 bytes
- **Returns:** 13
- **Calls:** 1

### DD:9C1F..DD:9C37 (Score 14)
- **Width:** 25 bytes
- **Returns:** 13
- **Calls:** 1

**Recommended Manifests (pass851-856):**
```json
{"pass": 851, "bank": "DD", "address": "3407", "length": 55, "type": "code", "score": 14}
{"pass": 852, "bank": "DD", "address": "45FD", "length": 29, "type": "code", "score": 14}
{"pass": 853, "bank": "DD", "address": "982D", "length": 35, "type": "code", "score": 14}
{"pass": 854, "bank": "DD", "address": "9C3D", "length": 35, "type": "code", "score": 14}
{"pass": 855, "bank": "DD", "address": "980F", "length": 25, "type": "code", "score": 14}
{"pass": 856, "bank": "DD", "address": "9C1F", "length": 25, "type": "code", "score": 14}
```

---

## 🥉 TIER 3: Score-13 STRONG CANDIDATES

### DD:6567..DD:6587 (Score 13)
- **Width:** 33 bytes
- **Returns:** 16
- **Calls:** 2

### DD:4B4D..DD:4B69 (Score 13)
- **Width:** 29 bytes
- **Returns:** 13
- **Calls:** 2

### DD:6597..DD:65AF (Score 13)
- **Width:** 25 bytes
- **Returns:** 13
- **Calls:** 2

**Recommended Manifests (pass857-859):**
```json
{"pass": 857, "bank": "DD", "address": "6567", "length": 33, "type": "code", "score": 13}
{"pass": 858, "bank": "DD", "address": "4B4D", "length": 29, "type": "code", "score": 13}
{"pass": 859, "bank": "DD", "address": "6597", "length": 25, "type": "code", "score": 13}
```

---

## 📊 TIER 4: Score-10 to 12 (Good Candidates)

| Range | Score | Width | Returns | Calls | Recommended Pass |
|-------|-------|-------|---------|-------|------------------|
| DD:1EF8..DD:1F0F | 11 | 24 | 12 | 0 | pass860 |
| DD:1027..DD:1037 | 10 | 17 | 9 | 1 | pass861 |
| DD:6605..DD:6625 | 10 | 33 | 15 | 1 | pass862 |

---

## 📈 TIER 5: Score-8 to 9 (Solid Functions)

| Range | Score | Width | Returns | Calls | Recommended Pass |
|-------|-------|-------|---------|-------|------------------|
| DD:07B8..DD:07C7 | 9 | 16 | 8 | 1 | pass863 |
| DD:469D..DD:46AD | 9 | 17 | 7 | 0 | pass864 |
| DD:205D..DD:2077 | 8 | 27 | 14 | 0 | pass865 |
| DD:4DB1..DD:4DD7 | 8 | 39 | 16 | 0 | pass866 |
| DD:7310..DD:731F | 8 | 16 | 8 | 0 | pass867 |
| DD:96C9..DD:96E7 | 8 | 31 | 16 | 0 | pass868 |
| DD:9AD9..DD:9AF7 | 8 | 31 | 16 | 0 | pass869 |

---

## 📋 TIER 6: Score-7 (Worth Documenting)

8 clusters identified - see full list in appendix.

---

## 📋 TIER 7: Score-6 (32 Clusters - Appendix A)

32 clusters identified with score-6. Full details in appendix.

---

## Regional Distribution

| Region | Total Clusters | Score-10+ | Score-6+ |
|--------|---------------|-----------|----------|
| DD:0000-4000 | 115 | 3 | 29 |
| DD:4000-8000 | 115 | 3 | 14 |
| DD:8000-C000 | 78 | 8 | 11 |
| DD:C000-FFFF | 109 | 0 | 7 |
| **TOTAL** | **417** | **14** | **61** |

---

## Key Findings

1. **DD:8000-C000 is the GOLDMINE region** with 8 score-10+ clusters including the 2 score-20 mega clusters
2. **DD:0000-4000 has the most density** with 29 score-6+ clusters
3. **Pattern detected:** Score-20 clusters at DD:973D and DD:9B4D are 1516 bytes apart - likely related function pairs
4. **Score-14 clusters appear in pairs:** DD:982D/DD:9C3D and DD:980F/DD:9C1F suggest dual-function patterns

---

## Recommended Next Steps

1. **Immediate:** Create manifests pass849-856 for Tier 1-2 clusters (score-14+)
2. **This session:** Document Tier 3 clusters (score-13) as pass857-859
3. **Next session:** Continue with Tier 4-5 (score-8 to 12)
4. **Verification:** Run `score_target_owner_backtrack_v1.py` on Tier 1 clusters to confirm boundaries

---

## Appendix A: All Score-6 Clusters (32 total)

<details>
<summary>Click to expand full list</summary>

### DD:0000-4000 Region
- DD:1FE5..DD:1FFB (score 6, width 23, returns 12)
- DD:2F5F..DD:2F75 (score 6, width 23, returns 12)
- DD:2F87..DD:2F9D (score 6, width 23, returns 12)
- DD:2FAF..DD:2FC5 (score 6, width 23, returns 12)
- DD:3B04..DD:3B15 (score 6, width 18, returns 5, calls 1)
- DD:31BF..DD:31CF (score 6, width 17, returns 9)
- DD:0228..DD:0237 (score 6, width 16, returns 4)
- DD:03B8..DD:03C7 (score 6, width 16, returns 4)
- DD:0A48..DD:0A57 (score 6, width 16, returns 8)
- DD:08AA..DD:08B7 (score 6, width 14, returns 7)
- DD:0E4A..DD:0E57 (score 6, width 14, returns 7)
- DD:1AB8..DD:1AC5 (score 6, width 14, returns 7)
- DD:1B08..DD:1B15 (score 6, width 14, returns 7)
- DD:1B58..DD:1B65 (score 6, width 14, returns 7)
- DD:33D8..DD:33E5 (score 6, width 14, returns 3)
- DD:3900..DD:390D (score 6, width 14, returns 3)
- DD:3928..DD:3935 (score 6, width 14, returns 3)
- DD:19E1..DD:19F7 (score 6, width 23, returns 4)
- DD:1A31..DD:1A47 (score 6, width 23, returns 4)

### DD:4000-8000 Region
- DD:689D..DD:68B7 (score 6, width 27, returns 6)
- DD:653D..DD:654D (score 6, width 17, returns 7, calls 1)
- DD:6C18..DD:6C25 (score 6, width 14, returns 3, calls 1)
- DD:437D..DD:4389 (score 6, width 13, returns 5)
- DD:441D..DD:4429 (score 6, width 13, returns 5)

### DD:8000-C000 Region
- DD:8AD4..DD:8ADF (score 6, width 12, returns 6, calls 1)

### DD:C000-FFFF Region
- DD:E376..DD:E383 (score 6, width 14, returns 4, calls 1)
- DD:C2D0..DD:C2DB (score 6, width 12, returns 2, calls 1)
- DD:F724..DD:F72F (score 6, width 12, returns 6, calls 2)
- DD:F79C..DD:F7A7 (score 6, width 12, returns 6, calls 1)
- DD:F814..DD:F81F (score 6, width 12, returns 6, calls 2)
- DD:FCA5..DD:FCAB (score 6, width 7, returns 2)
- DD:FCF5..DD:FCFB (score 6, width 7, returns 2)

</details>

---

## Appendix B: Score-7 Clusters (8 total)

- DD:3187..DD:31A7 (score 7, width 33, returns 16)
- DD:315F..DD:317D (score 7, width 31, returns 15, calls 1)
- DD:09B8..DD:09C7 (score 7, width 16, returns 8)
- DD:1F21..DD:1F2F (score 7, width 15, returns 8)
- DD:1F71..DD:1F7F (score 7, width 15, returns 8)
- DD:4F92..DD:4F9F (score 7, width 14, returns 7)
- DD:949F..DD:94DF (score 7, width 65, returns 29 - LARGEST!)
- DD:8BB8..DD:8BC3 (score 7, width 12, returns 6, calls 1)

---

*Report generated by Bank DD Deep Scan Session 14*
