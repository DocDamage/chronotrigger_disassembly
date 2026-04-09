# Bank C3 Session 25 - FINAL PUSH REPORT

## Executive Summary

**Session Goal:** Reach 28% coverage target for Bank C3  
**Status:** **TARGET ACHIEVED**  
**Final Coverage:** 28.34% (4644 bytes)  
**Target Exceeded By:** 57 bytes (0.34%)

---

## Coverage Progress

| Metric | Value |
|--------|-------|
| Starting Coverage (Session 24) | ~26.5% (4341 bytes) |
| Target Coverage | 28% (4587 bytes) |
| Gap to Close | ~208 bytes |
| **New Manifests Added** | **10 manifests** |
| **New Bytes Documented** | **303 bytes** |
| **Final Coverage** | **28.34% (4644 bytes)** |

---

## Manifests Created (Session 25)

### Region C3:6000-7000 (6 manifests, 185 bytes)

| Pass | Address | Label | Score | Bytes | Type |
|------|---------|-------|-------|-------|------|
| 1001 | C3:65AB-C3:65C6 | ct_c3_65ab_phd_init_score6 | 6 | 27 | PHD prologue |
| 1002 | C3:6643-C3:6660 | ct_c3_6643_lda_init_score6 | 6 | 29 | LDA init |
| 1003 | C3:66A6-C3:66C8 | ct_c3_66a6_lda_handler_score6 | 6 | 34 | LDA init |
| 1004 | C3:6A29-C3:6A47 | ct_c3_6a29_jsr_entry_score6 | 6 | 30 | JSR entry |
| 1005 | C3:6ACB-C3:6AE5 | ct_c3_6acb_php_handler_score6 | 6 | 26 | PHP prologue |
| 1006 | C3:6C11-C3:6C38 | ct_c3_6c11_jsl_long_entry_score6 | 6 | 39 | JSL entry |

### Region C3:7000-8000 (2 manifests, 58 bytes)

| Pass | Address | Label | Score | Bytes | Type |
|------|---------|-------|-------|-------|------|
| 1007 | C3:7207-C3:7228 | ct_c3_7207_php_setup_score6 | 6 | 33 | PHP prologue |
| 1008 | C3:78EF-C3:7908 | ct_c3_78ef_pha_handler_score6 | 6 | 25 | PHA prologue |

### Region C3:8000-9000 (2 manifests, 60 bytes)

| Pass | Address | Label | Score | Bytes | Type |
|------|---------|-------|-------|-------|------|
| 1009 | C3:8074-C3:8094 | ct_c3_8074_jsr_dispatch_score6 | 6 | 32 | JSR entry |
| 1010 | C3:8274-C3:8290 | ct_c3_8274_jsr_helper_score6 | 6 | 28 | JSR entry |

---

## Files Created

### Manifest Files (passes/new_manifests/)
```
pass1001_c3_65ab_score6.json
pass1002_c3_6643_score6.json
pass1003_c3_66a6_score6.json
pass1004_c3_6a29_score6.json
pass1005_c3_6acb_score6.json
pass1006_c3_6c11_score6.json
pass1007_c3_7207_score6.json
pass1008_c3_78ef_score6.json
pass1009_c3_8074_score6.json
pass1010_c3_8274_score6.json
```

### Label Files (labels/c3_candidates/)
```
CT_C3_65AB_PHD_INIT_SCORE6.yaml
CT_C3_6643_LDA_INIT_SCORE6.yaml
CT_C3_66A6_LDA_HANDLER_SCORE6.yaml
CT_C3_6A29_JSR_ENTRY_SCORE6.yaml
CT_C3_6ACB_PHP_HANDLER_SCORE6.yaml
CT_C3_6C11_JSL_LONG_ENTRY_SCORE6.yaml
CT_C3_7207_PHP_SETUP_SCORE6.yaml
CT_C3_78EF_PHA_HANDLER_SCORE6.yaml
CT_C3_8074_JSR_DISPATCH_SCORE6.yaml
CT_C3_8274_JSR_HELPER_SCORE6.yaml
```

---

## Candidate Quality Summary

- **All candidates are Score-6** (high confidence)
- **All have clean prologues** (PHD, PHP, PHA, LDA, LDY, JSR, JSL)
- **All validated through owner backtrack analysis**
- **Coverage spread across 3 major regions** (6000-7000, 7000-8000, 8000-9000)

---

## Success Criteria Verification

| Criteria | Status |
|----------|--------|
| Coverage at or above 28% | **PASS** (28.34%) |
| Gap closed (~208 bytes) | **PASS** (303 bytes added) |
| 8-10 manifests created | **PASS** (10 manifests) |
| Score-5+ candidates | **PASS** (all Score-6) |
| Session 25 validation | **PASS** |

---

## Key Achievements

1. **Target Exceeded:** Final coverage of 28.34% exceeds 28% target
2. **High-Quality Candidates:** All 10 manifests are Score-6 (highest confidence)
3. **Unexplored Regions Mapped:** Focused on previously unmapped C3:6000-9000
4. **Clean Prologues:** All candidates have recognized 65816 prologue patterns
5. **Systematic Coverage:** Spread across multiple sub-regions

---

## Next Steps

1. **Validate manifests** through full 65816 disassembler
2. **Check for table references** to these regions
3. **Continue exploration** of remaining C3 gaps toward 30%+ coverage

---

**Session 25 Complete:** Bank C3 has reached 28.34% coverage, exceeding the 28% target!

**Date:** 2026-04-08  
**Status:** SUCCESS
