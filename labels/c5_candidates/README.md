# Bank C5 Function Candidates

**Generated:** 2026-04-08
**Analysis:** Deep scan of Bank C5 rich regions
**Total New Candidates:** 24

---

## Overview

This directory contains score-6+ function candidate manifests for Bank C5, identified through deep scan analysis of rich code regions.

### Regions Analyzed
- C5:0000-1000 (bank start) - 7 candidates
- C5:1000-2000 - 8 candidates
- C5:2000-3000 - 3 candidates
- C5:8000-9000 - 1 candidate
- C5:B000-C000 - 11 candidates
- C5:C000-D000 - 4 candidates
- C5:D000-E000 (score-8 area) - 2 candidates
- C5:E000-F000 - 7 candidates

### Regions Avoided (Data/Bytecode)
- C5:4000-6000 - PHP/SED/PLP/BRK bytecode
- C5:6000-8000 - Structural data patterns
- C5:9000-AFFF - Data-encoded control (contains 9BC1 cluster)
- C5:C000-DFFF - Heavy repeating patterns

---

## Candidate List

| File | Address | Score | Prologue | Region |
|------|---------|-------|----------|--------|
| bank_C5_103B_score6.yaml | C5:103B | 6 | PHA | 1000-2000 |
| bank_C5_109B_score6.yaml | C5:109B | 6 | LDY# | 1000-2000 |
| bank_C5_11F8_score6.yaml | C5:11F8 | 6 | JSR | 1000-2000 |
| bank_C5_17FE_score6.yaml | C5:17FE | 6 | PHP | 1000-2000 |
| bank_C5_18EF_score6.yaml | C5:18EF | 6 | PHA | 1000-2000 |
| bank_C5_1909_score6.yaml | C5:1909 | 6 | LDY# | 1000-2000 |
| bank_C5_2021_score6.yaml | C5:2021 | 6 | PHB | 2000-3000 |
| bank_C5_21FD_score6.yaml | C5:21FD | 6 | REP | 2000-3000 |
| bank_C5_27EF_score6.yaml | C5:27EF | 6 | PHD | 2000-3000 |
| bank_C5_80DE_score6.yaml | C5:80DE | 6 | PHP | 8000-9000 |
| bank_C5_B03F_score6.yaml | C5:B03F | 6 | JSR | B000-C000 |
| bank_C5_B097_score6.yaml | C5:B097 | 6 | REP | B000-C000 |
| bank_C5_B0D5_score6.yaml | C5:B0D5 | 6 | LDY# | B000-C000 |
| bank_C5_B4B1_score6.yaml | C5:B4B1 | 6 | PHP | B000-C000 |
| bank_C5_B4D7_score6.yaml | C5:B4D7 | 6 | PHP | B000-C000 |
| bank_C5_B73F_score6.yaml | C5:B73F | 6 | JSR | B000-C000 |
| bank_C5_B85E_score6.yaml | C5:B85E | 6 | LDY# | B000-C000 |
| bank_C5_BBFD_score6.yaml | C5:BBFD | 6 | PHD | B000-C000 |
| bank_C5_BF2D_score6.yaml | C5:BF2D | 6 | JSR | B000-C000 |
| bank_C5_C0B7_score6.yaml | C5:C0B7 | 6 | JSL | C000-D000 |
| bank_C5_C0EA_score6.yaml | C5:C0EA | 6 | PHP | C000-D000 |
| bank_C5_C1E6_score6.yaml | C5:C1E6 | 6 | JSR | C000-D000 |
| bank_C5_CEF2_score6.yaml | C5:CEF2 | 6 | PHP | C000-D000 |
| bank_C5_DCB6_score6.yaml | C5:DCB6 | 6 | JSR | D000-E000 |
| bank_C5_DF2E_score6.yaml | C5:DF2E | 6 | JSR | D000-E000 |
| bank_C5_E017_score6.yaml | C5:E017 | 6 | PHP | E000-F000 |
| bank_C5_E026_score6.yaml | C5:E026 | 6 | JSR | E000-F000 |
| bank_C5_E4E6_score6.yaml | C5:E4E6 | 6 | LDY# | E000-F000 |
| bank_C5_E781_score6.yaml | C5:E781 | 6 | PHP | E000-F000 |
| bank_C5_E8F6_score6.yaml | C5:E8F6 | 6 | PHD | E000-F000 |
| bank_C5_EFF9_score6.yaml | C5:EFF9 | 6 | JSR | E000-F000 |

---

## Existing C5 Labels (Not in this directory)

- bank_C5_001E_score6.yaml
- bank_C5_04A7_score6.yaml
- bank_C5_0D1A_score7.yaml
- bank_C5_4206_score6.yaml
- bank_C5_6272_score7.yaml
- bank_C5_69F5_score7.yaml
- bank_C5_804F_score6.yaml
- bank_C5_9BC1_score9.yaml (HIGHEST IN C5)
- bank_C5_9BC1_cluster_score9.yaml
- bank_C5_9F66_score7.yaml
- bank_C5_C030_score6.yaml
- bank_C5_C036_score6.yaml
- bank_C5_CB70_score7.yaml
- bank_C5_DB2B_score7.yaml
- bank_C5_DC49_score8.yaml

---

## Next Steps

1. Verify candidate boundaries through disassembly
2. Cross-reference with calling functions
3. Create pass manifests for verified functions
4. Focus on D000-E000 region (score-8 area) for expansion
5. Expand 9BC1 cluster analysis (highest score in C5)

---

## Analysis Tools Used

- `detect_data_patterns_v1.py` - Data vs code classification
- `score_target_owner_backtrack_v1.py` - Function entry scoring
- `run_seam_block_v1.py` - Page-level analysis

## Report

See: `reports/C5_BANK_ANALYSIS_REPORT.md`
