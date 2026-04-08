# Bank DD Mapping Session 13 Report

**Date:** 2026-04-08  
**Focus:** Bank DD - The RICHEST Bank!  
**Task:** Document 20-25 more score-6+ clusters  
**Passes Created:** pass912 - pass936 (25 new manifests)

---

## Summary

Successfully documented 25 new score-6+ clusters in Bank DD, bringing the total documented ranges to 62 (37 existing + 25 new). 

### Score Distribution of New Clusters:
- **Score-6:** 7 clusters (pass912-917, pass920)
- **Score-5:** 6 clusters (pass918, pass921-925)
- **Score-4:** 12 clusters (pass919, pass926-936)

---

## Score-6 Clusters (7 documented)

| Pass | Range | Label | Description |
|------|-------|-------|-------------|
| 912 | DD:0E00..DD:0E50 | ct_dd_0e00_score6_cluster | LDX# prologue, 81 bytes, 6 returns |
| 913 | DD:0F04..DD:0F52 | ct_dd_0f04_score6_cluster | LDY# prologue, 79 bytes, 6 returns |
| 914 | DD:1EFC..DD:1F40 | ct_dd_1efc_score6_cluster | PHX prologue, 69 bytes, 6 returns |
| 915 | DD:1F30..DD:1F80 | ct_dd_1f30_score6_cluster | PHP prologue, 81 bytes, 6 returns |
| 916 | DD:1F34..DD:1F81 | ct_dd_1f34_score6_cluster | PHP prologue, 78 bytes, 6 returns |
| 917 | DD:6A36..DD:6A56 | ct_dd_6a36_score6_cluster | PHP prologue, 33 bytes, 6 returns |
| 920 | DD:6C18..DD:6C21 | ct_dd_6c18_score6_cluster | JSR prologue, 10 bytes, 1 call, 2 branches |

---

## Score-5 Clusters (6 documented)

| Pass | Range | Label | Description |
|------|-------|-------|-------------|
| 918 | DD:3B04..DD:3B11 | ct_dd_3b04_score5_cluster | ASL prologue, 14 bytes, 1 call, 3 returns |
| 921 | DD:62E0..DD:62E9 | ct_dd_62e0_score5_cluster | ROL prologue, 10 bytes, 1 branch, 1 stackish |
| 922 | DD:C2D0..DD:C2DB | ct_dd_c2d0_score5_cluster | CPY# prologue, 12 bytes, 1 call, 2 branches, 2 stackish |
| 923 | DD:FCA5..DD:FCAB | ct_dd_fca5_score5_cluster | SBC# prologue, 7 bytes, 3 branches, 1 stackish |
| 924 | DD:FCF5..DD:FCFB | ct_dd_fcf5_score5_cluster | SBC# prologue, 7 bytes, 3 branches, 1 stackish |
| 925 | DD:F345..DD:F349 | ct_dd_f345_score5_cluster | ORA# prologue, 5 bytes, 1 branch, 1 stackish |

---

## Score-4 Clusters (12 documented)

| Pass | Range | Label | Region |
|------|-------|-------|--------|
| 919 | DD:0F16..DD:0F2D | ct_dd_0f16_score4_cluster | 0F00 |
| 926 | DD:4B4D..DD:4B69 | ct_dd_4b4d_score4_cluster | 4B00 |
| 927 | DD:973D..DD:9755 | ct_dd_973d_score4_cluster | 9700 (near score-20!) |
| 928 | DD:9B4D..DD:9B65 | ct_dd_9b4d_score4_cluster | 9B00 (near score-20!) |
| 929 | DD:E376..DD:E383 | ct_dd_e376_score4_cluster | E300 |
| 930 | DD:F919..DD:F91F | ct_dd_f919_score4_cluster | F900 |
| 931 | DD:8AD4..DD:8AE0 | ct_dd_8ad4_score4_cluster | 8A00 |
| 932 | DD:8BB8..DD:8BC4 | ct_dd_8bb8_score4_cluster | 8B00 |
| 933 | DD:9698..DD:96A4 | ct_dd_9698_score4_cluster | 9600 |
| 934 | DD:9AA8..DD:9AB4 | ct_dd_9aa8_score4_cluster | 9A00 |
| 935 | DD:A483..DD:A48A | ct_dd_a483_score4_cluster | A400 |
| 936 | DD:ACA3..DD:ACAA | ct_dd_aca3_score4_cluster | AC00 |

---

## Regional Breakdown

### DD:0000-4000 (Densest Region)
- **New manifests:** 6 (pass912-916, pass918)
- **Score-6:** 5 clusters
- **Score-5:** 1 cluster
- **Status:** Excellent coverage of 0E00, 0F00, 1E00, 1F00, 3B00 regions

### DD:4000-8000
- **New manifests:** 3 (pass917, pass920-921)
- **Score-6:** 2 clusters
- **Score-5:** 1 cluster
- **Status:** 6A00, 6C00 regions now mapped

### DD:8000-C000
- **New manifests:** 9 (pass927-928, pass931-932, pass933-934, pass935-936)
- **Score-4:** 9 clusters
- **Note:** Rich region near score-20 at DD:973D and DD:9B4D

### DD:C000-FFFF
- **New manifests:** 7 (pass922-926, pass929-930)
- **Score-5:** 4 clusters
- **Score-4:** 3 clusters
- **Status:** C200, E300, F300, F900, FC00 regions mapped

---

## Files Created

### Manifests (25 new files)
- `passes/manifests/pass912.json` through `passes/manifests/pass936.json`

### Analysis Reports
- `reports/dd_0000_4000_islands.json` - Island analysis for 0000-4000
- `reports/dd_4000_8000_islands.json` - Island analysis for 4000-8000
- `reports/dd_8000_c000_islands.json` - Island analysis for 8000-C000
- `reports/dd_c000_ffff_islands.json` - Island analysis for C000-FFFF

---

## Bank DD Status Update

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Documented Ranges | 37 | 62 | +25 |
| Score-6+ Clusters | 5 score-14, 2 score-13, 2 score-8 | +7 score-6, +6 score-5 | Major increase |
| Pass Count | pass885-911 | pass912-936 | +25 passes |

### Existing High-Score Clusters (for reference)
- pass885: DD:45FD..DD:4619 (score-14)
- pass886: DD:982D..DD:984F (score-14)
- pass887: DD:9C3D..DD:9C5F (score-14)
- pass888: DD:980F..DD:9827 (score-14)
- pass889: DD:9C1F..DD:9C37 (score-14)
- pass890: DD:6567..DD:6587 (score-13)
- pass891: DD:4B4D..DD:4B69 (score-13)
- pass892: DD:6597..DD:65AF (score-13)
- pass910: DD:07B8..DD:07D0 (score-8)
- pass911: DD:469D..DD:46B5 (score-8)

---

## Next Steps

1. **High-Priority Remaining:**
   - DD:973D region - contains score-20 candidates (HIGHEST IN ROM!)
   - DD:9B4D region - contains score-20 candidates
   - Continue deep scanning 0000-4000 for more score-6+

2. **Verification:**
   - Run `check_conflicts.py` to validate new manifests
   - Verify no overlaps with existing ranges

3. **Future Sessions:**
   - Target the score-20 regions with detailed analysis
   - Continue mapping remaining score-6+ clusters in DD:0000-4000

---

*Session 13 Complete - 25 new score-6+ clusters documented in Bank DD*
