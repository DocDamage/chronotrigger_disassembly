# Bank C3 Disassembly - Session 26 Report

## Date: 2026-04-08

---

## Executive Summary

Session 26 continued Bank C3 disassembly beyond the 28% target, exploring new regions and creating additional manifests for high-confidence code candidates.

### Achievements
- **10 new manifests created** (pass 943-952)
- **187 bytes of new code documented**
- **Coverage maintained above 28%**
- **Regions explored:** C3:2000-4000, C3:8000-9000, C3:9000-A000, C3:C000-D000

---

## New Regions Explored

### 1. C3:2000-3000 Region
| Address | Score | Type | Pass | Bytes |
|---------|-------|------|------|-------|
| C3:2CF8 | 7 | Score-7 code island | 943 | 18 |
| C3:28E6 | 6 | Score-6 code island | 944 | 14 |

**Analysis:** This region contains high-scoring code islands with good call/branch/return patterns.

### 2. C3:3000-4000 Region
| Address | Score | Type | Pass | Bytes |
|---------|-------|------|------|-------|
| C3:373D | 6 | Score-6 code island | 945 | 17 |
| C3:30B6 | 6 | Score-6 code island | 946 | 9 |

**Analysis:** Gap region with scattered code islands. C3:30B6 is a compact 9-byte function.

### 3. C3:8000-9000 Region
| Address | Score | Type | Pass | Bytes |
|---------|-------|------|------|-------|
| C3:8074 | 6 | JSR entry | 951 | 29 |
| C3:8274 | 6 | JSR entry | 952 | 29 |

**Analysis:** High-activity region with JSR entry patterns and clean starts.

### 4. C3:9000-A000 Region
| Address | Score | Type | Pass | Bytes |
|---------|-------|------|------|-------|
| C3:97B1 | 7 | Score-7 code island | 947 | 25 |
| C3:957B | 7 | Score-7 code island | 948 | 14 |
| C3:960C | 6 | Score-6 code island | 949 | 25 |

**Analysis:** This region has exceptional candidates - two score-7 functions with high call/branch activity.

### 5. C3:C000-D000 Region
| Address | Score | Type | Pass | Bytes |
|---------|-------|------|------|-------|
| C3:C120 | 6 | Score-6 code island | 950 | 7 |

**Analysis:** Upper bank region with compact but high-confidence candidates.

---

## Manifests Created (Session 26)

### Pass 943-946: C3:2000-4000 Region
1. `pass943_c3_2cf8_score7.json` - C3:2CF8..C3:2D0A (18 bytes, score 7)
2. `pass944_c3_28e6_score6.json` - C3:28E6..C3:28F4 (14 bytes, score 6)
3. `pass945_c3_373d_score6.json` - C3:373D..C3:374E (17 bytes, score 6)
4. `pass946_c3_30b6_score6.json` - C3:30B6..C3:30BF (9 bytes, score 6)

### Pass 947-949: C3:9000-A000 Region
5. `pass947_c3_97b1_score7.json` - C3:97B1..C3:97CA (25 bytes, score 7)
6. `pass948_c3_957b_score7.json` - C3:957B..C3:9589 (14 bytes, score 7)
7. `pass949_c3_960c_score6.json` - C3:960C..C3:9625 (25 bytes, score 6)

### Pass 950: C3:C000-D000 Region
8. `pass950_c3_c120_score6.json` - C3:C120..C3:C127 (7 bytes, score 6)

### Pass 951-952: C3:8000-9000 Region
9. `pass951_c3_8074_jsr_entry.json` - C3:8074..C3:8091 (29 bytes, score 6)
10. `pass952_c3_8274_jsr_entry.json` - C3:8274..C3:8291 (29 bytes, score 6)

---

## Label Files Created

All label files created in `labels/c3_candidates_session26/`:
- CT_C3_2CF8_SCORE7.asm
- CT_C3_28E6_SCORE6.asm
- CT_C3_373D_SCORE6.asm
- CT_C3_30B6_SCORE6.asm
- CT_C3_97B1_SCORE7.asm
- CT_C3_957B_SCORE7.asm
- CT_C3_960C_SCORE6.asm
- CT_C3_C120_SCORE6.asm
- CT_C3_8074_JSR_ENTRY.asm
- CT_C3_8274_JSR_ENTRY.asm

---

## Coverage Analysis

### Before Session 26:
- **~80 documented ranges**
- **~18,500 bytes documented**
- **~28.2% coverage**

### After Session 26:
- **90 documented ranges** (+10 new)
- **~18,687 bytes documented** (+187 bytes)
- **~28.5% coverage** (+0.3%)

### Target Status:
✅ **28% coverage target EXCEEDED and maintained**

---

## High-Activity Regions Identified

Based on the scan results, these regions warrant further investigation:

1. **C3:9000-A000** - Multiple score-7 candidates, high call/branch density
2. **C3:2000-3000** - Score-7 candidate at C3:2CF8
3. **C3:8000-9000** - JSR entry patterns with clean starts

---

## Next Steps

1. ✅ **Session 26 complete** - 10 manifests created
2. 🔲 **Promote manifests to passes** - Move from new_manifests to manifests/
3. 🔲 **Continue gap analysis** - Focus on C3:A000-B000 and C3:D000-FFFF
4. 🔲 **Generate disassembly** - Create ASM files for new functions

---

## Tools Used

1. `find_local_code_islands_v2.py` - Scanned regions for code candidates
2. `validate_passes.py` - Validated manifests

---

*Session 26 completed: 10 new manifests, 187 bytes documented*
*Total C3 manifests in new_manifests: 59*
*Coverage: 28.2% → 28.5%*
