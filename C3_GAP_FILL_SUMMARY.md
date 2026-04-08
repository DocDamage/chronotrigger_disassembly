# Bank C3 Gap Fill Analysis - Summary Report

## Analysis Completed: 2026-04-08

---

## 1. Score-6+ Candidates Found in Gaps

### Major Gap: C3:0000-01E3 (Bank Start)
| Address | Type | Score | Status |
|---------|------|-------|--------|
| C3:01A8 | JSR prologue | 6 | Already mapped (pass 599) |
| C3:01B4 | PHP prologue | 6 | Already mapped (pass 600) |
| C3:01BA | JSR variant | 6 | **New candidate** |
| C3:01BD | REP prologue | 6 | **New candidate** |
| C3:0026 | PHP handler | 6 | Candidate label exists |

### Major Gap: C3:0529-08A0 (Early Gap)
| Address | Type | Score | Status |
|---------|------|-------|--------|
| C3:052A | JSR entry | 6 | **New candidate** |
| C3:0540 | LDA init | 6 | **New candidate** |
| C3:058A | PHY prologue | 6 | **New candidate** |
| C3:058B | PHD handler | 6 | Candidate label exists |
| C3:05B0 | BRA handler | 6 | Candidate label exists |
| C3:06CE | PLY handler | 6 | Candidate label exists |
| C3:0733 | PHD handler | 6 | Candidate label exists |
| C3:084D | PHP handler | 6 | Candidate label exists |

### Major Gap: C3:2900-3058
| Address | Type | Score | Status |
|---------|------|-------|--------|
| C3:2E31 | PHD prologue | 6 | Already mapped (pass 565) |

### Region C3:5000-5FFF (Game Logic)
| Address | Type | Score | Status |
|---------|------|-------|--------|
| C3:5131 | PHD prologue | 6 | Already mapped (pass 602) |
| C3:51EF | JSR handler | 6 | Already mapped (pass 604) |
| C3:55A3 | JSR entry | 6 | Already mapped (pass 239) |
| C3:5E34 | LDY init | 6 | **New candidate** |
| C3:5E47 | LDA init | 6 | **New candidate** |

### Region C3:6000-6FFF (Unexplored - High Priority)
| Address | Type | Score | Status |
|---------|------|-------|--------|
| C3:65AB | PHD prologue | 6 | **New candidate** |
| C3:6643 | LDA init | 6 | **New candidate** |
| C3:66A6 | LDA init | 6 | **New candidate** |
| C3:6A29 | JSR entry | 6 | **New candidate** |
| C3:6ACB | PHP prologue | 6 | **New candidate** |
| C3:6C11 | JSL entry | 6 | **New candidate** |

### Region C3:7000-7FFF
| Address | Type | Score | Status |
|---------|------|-------|--------|
| C3:7207 | PHP prologue | 6 | **New candidate** |
| C3:78EF | PHA prologue | 6 | **New candidate** |

### Region C3:8000-8FFF
| Address | Type | Score | Status |
|---------|------|-------|--------|
| C3:8074 | JSR entry | 6 | **New candidate** |
| C3:80C4 | PHP prologue | 6 | Already mapped (pass 240) |
| C3:8274 | JSR entry | 6 | **New candidate** |
| C3:8400 | JSR entry | 6 | **New candidate** |
| C3:8912 | PHP prologue | 6 | **New candidate** |
| C3:8C8E | JSL entry | 6 | Already mapped (pass 230) |

### Region C3:A000-AFFF
| Address | Type | Score | Status |
|---------|------|-------|--------|
| C3:A1F9 | JSL entry | 6 | **New candidate** |
| C3:A396 | JSL entry | 6 | Already mapped (pass 225) |
| C3:A3E2 | JSR entry | 6 | **New candidate** |
| C3:A3F1 | JSR entry | 6 | **New candidate** |
| C3:A8BA | JSR entry | 6 | **New candidate** |
| C3:AC12 | PHD prologue | 6 | Already mapped (pass 241) |
| C3:ADF8 | LDY init | 6 | **New candidate** |
| C3:AF42 | LDY init | 6 | **New candidate** |

### Region C3:B000-BFFF
| Address | Type | Score | Status |
|---------|------|-------|--------|
| C3:B002 | PHP prologue | 6 | **New candidate** |
| C3:B086 | PHX prologue | 6 | **New candidate** |
| C3:B0F3 | JSR entry | 6 | **New candidate** |
| C3:B16F | JSL entry | 6 | Already mapped |
| C3:B573 | PHD prologue | 6 | **New candidate** |
| C3:BB75 | PHP prologue | 6 | **New candidate** |

### Region C3:C000-CFFF
| Address | Type | Score | Status |
|---------|------|-------|--------|
| C3:C09E | JSR entry | 6 | **New candidate** |
| C3:C244 | PHP prologue | 6 | **New candidate** |
| C3:C2C2 | PHP prologue | 6 | **New candidate** |
| C3:CB47 | PHP prologue | 6 | **New candidate** |

### Region C3:D000-DFFF
| Address | Type | Score | Status |
|---------|------|-------|--------|
| C3:DF00 | PHP prologue | 6 | **New candidate** |

### Region C3:E000-EFFF
| Address | Type | Score | Status |
|---------|------|-------|--------|
| C3:E4EF | JSL entry | 6 | **New candidate** |

### Region C3:F000-FFFF
| Address | Type | Score | Status |
|---------|------|-------|--------|
| C3:F701 | JSR entry | 6 | **New candidate** |

---

## 2. Gap Fill Analysis Summary

| Gap/Region | Size | Score-6+ Count | Priority | Action |
|------------|------|----------------|----------|--------|
| C3:0000-01E3 | 484 bytes | 4 | Medium | Fill remaining candidates |
| C3:0529-08A0 | 1,383 bytes | 8 | **High** | Major gap fill needed |
| C3:2900-3058 | 3,416 bytes | 1 | Low | Mostly mapped/data |
| C3:5000-5FFF | 4,096 bytes | 5 | Medium | Continue from seam |
| C3:6000-6FFF | 4,096 bytes | 6 | **High** | Unexplored region |
| C3:7000-7FFF | 4,096 bytes | 2 | Medium | Partial coverage |
| C3:8000-8FFF | 4,096 bytes | 7 | Medium | Partial coverage |
| C3:A000-AFFF | 4,096 bytes | 8 | Medium | Partial coverage |
| C3:B000-BFFF | 4,096 bytes | 6 | Medium | Partial coverage |
| C3:C000-FFFF | 16,384 bytes | 6 | Low | Sparse coverage |

---

## 3. Recommended New Manifests (35 Functions)

### Created Manifests (8 files in passes/new_manifests/):
1. `pass679_c3_65ab_phd_prologue.json` - C3:65AB..C3:65C6
2. `pass680_c3_6643_lda_init.json` - C3:6643..C3:6660
3. `pass681_c3_6a29_jsr_entry.json` - C3:6A29..C3:6A47
4. `pass682_c3_052a_jsr_entry.json` - C3:052A..C3:0543
5. `pass683_c3_058a_phy_prologue.json` - C3:058A..C3:05AA
6. `pass684_c3_7207_php_prologue.json` - C3:7207..C3:7228
7. `pass685_c3_8074_jsr_entry.json` - C3:8074..C3:8094
8. `pass686_c3_b002_php_prologue.json` - C3:B002..C3:B01D
9. `pass687_c3_c244_php_prologue.json` - C3:C244..C3:C260

### Additional Recommended Manifests (27 more):

**C3:6000-6FFF (3 more):**
- C3:66A6..C3:66C8 - ct_c3_66a6_lda_init
- C3:6ACB..C3:6AE5 - ct_c3_6acb_php_prologue
- C3:6C11..C3:6C38 - ct_c3_6c11_jsl_entry

**C3:0529-08A0 (2 more):**
- C3:0540..C3:0559 - ct_c3_0540_lda_init
- C3:01BA..C3:01DE - ct_c3_01ba_jsr_prologue (from 0000-01E3 gap)

**C3:5000-5FFF (2 more):**
- C3:5E34..C3:5E54 - ct_c3_5e34_ldy_init
- C3:5E47..C3:5E6C - ct_c3_5e47_lda_init

**C3:7000-7FFF (1 more):**
- C3:78EF..C3:7908 - ct_c3_78ef_pha_prologue

**C3:8000-8FFF (4 more):**
- C3:8274..C3:8290 - ct_c3_8274_jsr_entry
- C3:8400..C3:841A - ct_c3_8400_jsr_entry
- C3:8912..C3:8939 - ct_c3_8912_php_prologue
- C3:8C8E..C3:8CA8 - ct_c3_8c8e_jsl_entry_b

**C3:A000-AFFF (6 more):**
- C3:A1F9..C3:A218 - ct_c3_a1f9_jsl_entry
- C3:A3E2..C3:A406 - ct_c3_a3e2_jsr_entry
- C3:A3F1..C3:A419 - ct_c3_a3f1_jsr_entry
- C3:A8BA..C3:A8D3 - ct_c3_a8ba_jsr_entry
- C3:ADF8..C3:AE18 - ct_c3_adf8_ldy_init
- C3:AF42..C3:AF60 - ct_c3_af42_ldy_init

**C3:B000-BFFF (4 more):**
- C3:B086..C3:B0AA - ct_c3_b086_phx_prologue
- C3:B0F3..C3:B119 - ct_c3_b0f3_jsr_entry
- C3:B573..C3:B58C - ct_c3_b573_phd_prologue
- C3:BB75..C3:BB99 - ct_c3_bb75_php_prologue

**C3:C000-CFFF (3 more):**
- C3:C09E..C3:C0C1 - ct_c3_c09e_jsr_entry
- C3:C2C2..C3:C2E8 - ct_c3_c2c2_php_prologue
- C3:CB47..C3:CB64 - ct_c3_cb47_php_prologue

**C3:D000-FFFF (3 more):**
- C3:DF00..C3:DF1E - ct_c3_df00_php_prologue
- C3:E4EF..C3:E508 - ct_c3_e4ef_jsl_entry
- C3:F701..C3:F720 - ct_c3_f701_jsr_entry

---

## 4. C3 Coverage Improvement

### Current State:
- **112 documented ranges**
- **21.24% coverage**
- **43 gaps remain**

### After Recommended Mapping:
- **147 documented ranges** (+35 new)
- **~28% estimated coverage** (+6.76%)
- **Existing candidates:** 12 ready for promotion

---

## 5. Files Created/Modified

### Reports Created:
1. `reports/C3_GAP_ANALYSIS_REPORT.md` - Comprehensive analysis with all candidates
2. `C3_GAP_FILL_SUMMARY.md` - This summary file

### Manifests Created (passes/new_manifests/):
- `pass679_c3_65ab_phd_prologue.json`
- `pass680_c3_6643_lda_init.json`
- `pass681_c3_6a29_jsr_entry.json`
- `pass682_c3_052a_jsr_entry.json`
- `pass683_c3_058a_phy_prologue.json`
- `pass684_c3_7207_php_prologue.json`
- `pass685_c3_8074_jsr_entry.json`
- `pass686_c3_b002_php_prologue.json`
- `pass687_c3_c244_php_prologue.json`

---

## 6. Next Steps

1. **High Priority:** Create manifests for C3:6000-6FFF region (6 candidates)
2. **Gap Fill:** Complete C3:0529-08A0 mapping (3 new + 5 existing candidates)
3. **Promotion:** Convert 12 existing candidate labels to manifests
4. **Continuation:** Scan remaining gaps for additional score-6+ clusters

---

*Analysis completed using score_target_owner_backtrack_v1.py*  
*Total score-6+ candidates identified: 47 (12 existing + 35 new)*
