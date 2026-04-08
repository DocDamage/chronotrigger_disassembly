# Bank D5 Assessment Report
## Chrono Trigger SNES ROM Disassembly

**Assessment Date:** 2026-04-08
**ROM:** Chrono Trigger (USA).sfc
**Bank Range:** D5:0000-D5:FFFF (offset 0x150000-0x15FFFF)

---

## Executive Summary

**Bank D5 Classification: CODE/DATA (MIXED)**

Bank D5 contains **significant executable code** embedded within a data-encoded control region. While the overall bank exhibits PHP/SED/PLP/BRK structural patterns similar to other data-encoded banks (like C6:CC00-D000), extensive code island analysis reveals **951 code islands** forming **672 clusters**, with **75 clusters scoring 6 or higher** (strong function candidates).

---

## Data Pattern Analysis

All four sampled regions show **DATA_ENCODED_CONTROL** classification:

| Region | Size | PHP | PLP | SED | BRK | RTS | RTL | Classification |
|--------|------|-----|-----|-----|-----|-----|-----|----------------|
| D5:0000-4000 | 16KB | 257 | 118 | 97 | 3060 | 201 | 6 | DATA_ENCODED_CONTROL |
| D5:4000-8000 | 16KB | 220 | 89 | 95 | 3911 | 201 | 10 | DATA_ENCODED_CONTROL |
| D5:8000-C000 | 16KB | 251 | 97 | 136 | 1942 | 208 | 12 | DATA_ENCODED_CONTROL |
| D5:C000-FFFF | 16KB | 291 | 68 | 166 | 1410 | 177 | 20 | DATA_ENCODED_CONTROL |

**Key Observations:**
- High BRK (0x00) density indicates encoded bytecode or state machine data
- Substantial RTS/RTL presence suggests genuine code functions
- PHP/SED/PLP patterns suggest banked context save/restore operations

---

## Code Island Analysis

| Region | Islands | Clusters | Score-6+ | Assessment |
|--------|---------|----------|----------|------------|
| Lower (0000-3FFF) | 253 | 170 | 17 | Moderate code density |
| Mid (4000-7FFF) | 217 | 155 | 19 | Good code density |
| Upper (8000-BFFF) | 253 | 183 | 25 | **Highest code density** |
| Bank End (C000-FFFF) | 227 | 164 | 14 | Moderate code density |
| **TOTAL** | **951** | **672** | **75** | **CODE BANK** |

---

## Top Score-6+ Function Candidates (20 of 75)

| Rank | Address Range | Score | Width | Priority |
|------|---------------|-------|-------|----------|
| 1 | D5:933C..D5:9370 | 10 | 53 bytes | **HIGHEST** |
| 2 | D5:BA86..D5:BAB4 | 9 | 47 bytes | **HIGHEST** |
| 3 | D5:D87B..D5:D8A7 | 9 | 45 bytes | **HIGHEST** |
| 4 | D5:497D..D5:4994 | 9 | 24 bytes | **HIGHEST** |
| 5 | D5:B253..D5:B267 | 9 | 21 bytes | **HIGHEST** |
| 6 | D5:CE2D..D5:CE5C | 8 | 48 bytes | HIGH |
| 7 | D5:AE41..D5:AE63 | 8 | 35 bytes | HIGH |
| 8 | D5:FCDB..D5:FCF6 | 8 | 28 bytes | HIGH |
| 9 | D5:EC5A..D5:EC6E | 8 | 21 bytes | HIGH |
| 10 | D5:69AD..D5:69E3 | 7 | 55 bytes | HIGH |
| 11 | D5:6FDE..D5:700C | 7 | 47 bytes | HIGH |
| 12 | D5:ECA6..D5:ECD1 | 7 | 44 bytes | HIGH |
| 13 | D5:8E41..D5:8E63 | 7 | 35 bytes | HIGH |
| 14 | D5:318B..D5:31A9 | 7 | 31 bytes | HIGH |
| 15 | D5:1A8F..D5:1AAC | 7 | 30 bytes | HIGH |
| 16 | D5:38F4..D5:3910 | 7 | 29 bytes | HIGH |
| 17 | D5:DBEC..D5:DC08 | 7 | 29 bytes | HIGH |
| 18 | D5:94DF..D5:94F9 | 7 | 27 bytes | HIGH |
| 19 | D5:ACAD..D5:ACC5 | 7 | 25 bytes | HIGH |
| 20 | D5:B1AF..D5:B1C3 | 7 | 21 bytes | HIGH |

**Full list:** 75 score-6+ clusters identified (see `reports/d5_analysis.json`)

---

## Backtrack Analysis Summary

**982 function entry point candidates** identified with backtrack scoring:
- Score 6+: Multiple high-confidence entry points
- Clean prologue signatures: PHP (08), PHA (48), PHD (0B), JSR (20), JSL (22), REP (C2)
- Well-distributed across all regions

---

## Recommendations

### Bank Classification
**Bank D5 is a CODE BANK with heavy data encoding.** This is the LAST unexplored D-bank and contains substantial undocumented code.

### Next Steps
1. **Prioritize the top 20 score-6+ clusters** for disassembly
2. **Focus on D5:8000-BFFF region** - highest code density (25 score-6+ clusters)
3. **Investigate D5:933C** first - only score-10 cluster in bank
4. **Cross-reference with D4 and D6** to identify call patterns

### Estimated New Functions
- **Conservative:** 12-15 high-confidence functions
- **Moderate:** 20-25 functions (all score-6+)
- **Aggressive:** 40+ functions (including score-5 clusters)

---

## Files Generated

- `reports/d5_analysis.json` - Full code island analysis (1.1MB)
- `reports/d5_report.py` - Analysis script
- `reports/BANK_D5_ASSESSMENT_REPORT.md` - This report

---

## Conclusion

**Bank D5 exploration is COMPLETE.** The bank is confirmed as the final D-bank requiring documentation. With 75 score-6+ clusters and 951 code islands, this bank contains significant undocumented functionality. Target the top 12-20 candidates for immediate disassembly to achieve the project goal of 8-12 new functions.
