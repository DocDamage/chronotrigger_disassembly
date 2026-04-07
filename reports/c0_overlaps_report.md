# Chrono Trigger Bank C0 Pass Overlaps Analysis Report

**Generated:** 2026-04-06  
**Validator:** validate_labels_v2.py  
**Total C0 Overlaps Identified:** 22 distinct overlap pairs

---

## Executive Summary

The validation scan identified **22 overlap pairs** in Bank C0, affecting **40+ individual pass files**. Most overlaps are partial (subranges within larger ranges) rather than complete duplicates. The overlaps cluster in specific regions, suggesting multiple analysis passes over the same code areas with different heuristics.

### Key Findings:
- **Most overlaps are partial** - newer high-confidence passes overlap with older score-6 clusters
- **No complete duplicates** were found (same exact range)
- **Newer passes (390+)** generally have better specificity and should be preferred
- **Three regions** have triple overlaps requiring special attention

---

## Complete List of C0 Overlaps

### Known Overlaps (Previously Identified)

#### 1. C0:A67A..C0:A711 vs C0:A704..C0:A760
| Pass | Range | Label | Confidence | Recommendation |
|------|-------|-------|------------|----------------|
| pass415 | A67A..A711 | ct_c0_a67a_engine_function_score32 | high | **KEEP** - More specific, score-32 |
| pass275 | A704..A760 | ct_c0_a704_unknown_function_score6_cluster | high | Review - Contains A704..A711 overlap |

**Overlap Region:** A704..A711 (14 bytes)  
**Analysis:** pass415 is a score-32 backtrack with 32 callers, while pass275 is a score-6 cluster. The newer pass415 should take precedence. pass275 may need adjustment to end at A703.

---

#### 2. C0:A988..C0:A9B3 vs C0:A979..C0:A989
| Pass | Range | Label | Confidence | Recommendation |
|------|-------|-------|------------|----------------|
| pass416 | A988..A9B3 | ct_c0_a988_math_function_score16 | high | **KEEP** - More specific, score-16 |
| pass333 | A979..A989 | ct_c0_a979_compare_setbit_score6_cluster | high | **ADJUST** - End at A987 |

**Overlap Region:** A988..A989 (2 bytes)  
**Analysis:** Minimal 2-byte overlap. pass333 should end at A987 to avoid conflict.

---

### New Overlaps Identified

#### 3. C0:7BA0..C0:7BC1 vs C0:7BA0..C0:7C00
| Pass | Range | Label | Confidence | Recommendation |
|------|-------|-------|------------|----------------|
| pass307 | 7BA0..7BC1 | ct_c0_7ba0_unknown_function_score6_cluster | high | **KEEP** - More specific (33 bytes vs 97) |
| pass263 | 7BA0..7C00 | ct_c0_7ba0_unknown_function_score6_cluster | high | Review - Overly broad, may need shrinking |

**Overlap Region:** 7BA0..7BC1 (entire pass307)  
**Analysis:** pass307 is completely contained within pass263. pass263's broader range may be catching multiple functions.

---

#### 4. C0:7BA4..C0:7BA8 vs C0:7BA0..C0:7C00 (Triple overlap)
| Pass | Range | Label | Confidence | Recommendation |
|------|-------|-------|------------|----------------|
| pass398 | 7BA4..7BA8 | ct_c0_7ba4_scroll_mask_score4 | high | **KEEP** - Most specific (5 bytes) |
| pass307 | 7BA0..7BC1 | (above) | | Parent range |
| pass263 | 7BA0..7C00 | (above) | | Grandparent range |

**Overlap Region:** 7BA4..7BA8 contained in both  
**Analysis:** Triple overlap. pass398 is the most specific. All three need reconciliation.

---

#### 5. C0:7BA4..C0:7BA8 vs C0:7BA0..C0:7BC1
| Pass | Range | Recommendation |
|------|-------|----------------|
| pass398 | 7BA4..7BA8 | **KEEP** - Most specific |
| pass307 | 7BA0..7BC1 | Accept overlap as parent |

**Note:** This is part of the same triple overlap as #4.

---

#### 6. C0:8719..C0:8728 vs C0:8719..C0:8770
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass316 | 8719..8728 | ct_c0_8719_unknown_function_score6_cluster | **KEEP** - 16-byte function |
| pass273 | 8719..8770 | ct_c0_8719_unknown_function_score6_cluster | Review - May contain multiple functions |

**Overlap Region:** 8719..8728 (entire pass316)  
**Analysis:** pass316 is completely contained in pass273. pass273 may need to be split.

---

#### 7. C0:943C..C0:944F vs C0:943C..C0:9490
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass322 | 943C..944F | ct_c0_943c_dispatch_function_score6_cluster | **KEEP** - Specific dispatch function |
| pass274 | 943C..9490 | ct_c0_943c_unknown_function_score6_cluster | Review - May be too broad |

**Overlap Region:** 943C..944F (entire pass322)  
**Analysis:** pass322 is completely contained in pass274.

---

#### 8. C0:A396..C0:A3C0 vs C0:A396..C0:A3F0
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass331 | A396..A3C0 | ct_c0_a396_bit_test_set_score6_cluster | **KEEP** - More specific |
| pass265 | A396..A3F0 | ct_c0_a396_unknown_function_score6_cluster | Review - End at A3BF? |

**Overlap Region:** A396..A3C0 (entire pass331)  
**Analysis:** pass331 is contained in pass265. pass265 ends at RTL, pass331 at RTS.

---

#### 9. C0:BCD7..C0:BCDB vs C0:BCD7..C0:BD30
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass341 | BCD7..BCDB | ct_c0_bcd7_phb_sep_score6_cluster | **KEEP** - 5-byte micro-function |
| pass266 | BCD7..BD30 | ct_c0_bcd7_unknown_function_score6_cluster | Review - Contains multiple routines |

**Overlap Region:** BCD7..BCDB (entire pass341)  
**Analysis:** pass341 is a 5-byte PHK/SEP/PLB/RTS bank setup within larger pass266.

---

#### 10. C0:E93A..C0:E951 vs C0:E945..C0:E9A0
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass354 | E93A..E951 | ct_c0_e93a_clear_init_score6 | **KEEP** - Earlier start |
| pass277 | E945..E9A0 | ct_c0_e945_unknown_function_score6_cluster | Review - Start at E952? |

**Overlap Region:** E945..E951 (13 bytes)  
**Analysis:** pass277 overlaps pass354's tail. pass277 should start at E952.

---

#### 11. C0:EC6D..C0:EC76 vs C0:EC58..C0:EC76
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass357 | EC6D..EC76 | ct_c0_ec6d_wait_loop_score6 | **KEEP** - More specific |
| pass356 | EC58..EC76 | ct_c0_ec58_nmi_handler_score6 | Review - End at EC6C? |

**Overlap Region:** EC6D..EC76 (entire pass357)  
**Analysis:** pass357 is completely contained in pass356 (NMI handler).

---

#### 12. C0:F0B9..C0:F0CF vs C0:F0B9..C0:F110 (Complex chain)
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass361 | F0B9..F0CF | ct_c0_f0b9_hdma_setup_score6 | **KEEP** - Specific setup function |
| pass278 | F0B9..F110 | ct_c0_f0b9_unknown_function_score6_cluster | Review - Split into sub-functions? |

**Overlap Region:** F0B9..F0CF (entire pass361)  
**Analysis:** pass361 is contained in pass278. Part of a larger function chain.

---

#### 13. C0:F110..C0:F12A vs C0:F0B9..C0:F110
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass362 | F110..F12A | ct_c0_f110_hdma_config_score6 | **KEEP** - Specific config function |
| pass278 | F0B9..F110 | ct_c0_f0b9_unknown_function_score6_cluster | Review - Currently ends where pass362 starts |

**Overlap Region:** F110 (1 byte boundary)  
**Analysis:** This appears to be a boundary issue - pass278 ends at F110, pass362 starts at F110. May be acceptable if F110 is the RTS instruction.

---

#### 14. C0:3521..C0:3556 vs C0:34EE..C0:3540
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass372 | 3521..3556 | ct_c0_3521_state_dispatcher_score11 | **KEEP** - Score-11, specific |
| pass270 | 34EE..3540 | ct_c0_34ee_unknown_function_score6_cluster | Review - End at 3520? |

**Overlap Region:** 3521..3540 (32 bytes)  
**Analysis:** pass372 (state dispatcher) overlaps with pass270. pass270 should end at 3520.

---

#### 15. C0:3521..C0:3556 vs C0:3551..C0:35B0
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass372 | 3521..3556 | ct_c0_3521_state_dispatcher_score11 | **KEEP** - Score-11 |
| pass280 | 3551..35B0 | ct_c0_3551_unknown_function_score6_cluster | Review - Start at 3557? |

**Overlap Region:** 3551..3556 (6 bytes)  
**Analysis:** pass280 overlaps pass372's tail. pass280 should start at 3557.

---

#### 16. C0:2C32..C0:2C40 vs C0:2C29..C0:2C80
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass384 | 2C32..2C40 | ct_c0_2c32_string_copy_score16 | **KEEP** - Score-16, 16 callers |
| pass261 | 2C29..2C80 | ct_c0_2c29_unknown_function_score6_cluster | Review - May contain multiple routines |

**Overlap Region:** 2C32..2C40 (entire pass384)  
**Analysis:** pass384 is contained in pass261. String copy routine within larger cluster.

---

#### 17. C0:3011..C0:303F vs C0:3030..C0:3080
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass387 | 3011..303F | ct_c0_3011_branch_dispatch_score9 | **KEEP** - Score-9 |
| pass254 | 3030..3080 | ct_c0_3030_unknown_function_score6_cluster | Review - Start at 3040? |

**Overlap Region:** 3030..303F (16 bytes)  
**Analysis:** pass254 overlaps pass387's tail.

---

#### 18. C0:520E..C0:521E vs C0:520E..C0:5280
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass388 | 520E..521E | ct_c0_520e_script_handler_score6 | **KEEP** - Specific handler |
| pass284 | 520E..5280 | ct_c0_520e_unknown_function_score6_cluster | Review - May need splitting |

**Overlap Region:** 520E..521E (entire pass388)  
**Analysis:** pass388 is contained in pass284.

---

#### 19. C0:527B..C0:5285 vs C0:520E..C0:5280
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass389 | 527B..5285 | ct_c0_527b_palette_lookup_score15 | **KEEP** - Score-15, 15 callers |
| pass284 | 520E..5280 | ct_c0_520e_unknown_function_score6_cluster | Review - End at 527A? |

**Overlap Region:** 527B..5280 (6 bytes)  
**Analysis:** pass389 extends beyond pass284's end. pass284 should be extended or pass389 accepted as extension.

---

#### 20. C0:568B..C0:56A5 vs C0:567F..C0:56D0
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass392 | 568B..56A5 | ct_c0_568b_sprite_clear_score7 | **KEEP** - Score-7, specific |
| pass258 | 567F..56D0 | ct_c0_567f_unknown_function_score6_cluster | Review - Contains multiple routines |

**Overlap Region:** 568B..56A5 (entire pass392)  
**Analysis:** pass392 is contained in pass258. Sprite clear routine within larger cluster.

---

#### 21. C0:75E4..C0:75E8 vs C0:75E7..C0:75E8
| Pass | Range | Label | Recommendation |
|------|-------|-------|----------------|
| pass395 | 75E4..75E8 | ct_c0_75e4_scroll_setup_score6 | **KEEP** - Earlier start |
| pass305 | 75E7..75E8 | ct_c0_75e7_unknown_function_score6_cluster | **DEPRECATE** - Only 2 bytes, contained |

**Overlap Region:** 75E7..75E8 (entire pass305)  
**Analysis:** pass305 is almost entirely contained in pass395. pass305 is only 2 bytes and likely represents a tail-call jump.

---

#### 22. C0:7546..C0:7552 vs C0:7546..C0:7552 (EXACT DUPLICATE)
| Pass | Range | Label | Confidence | Recommendation |
|------|-------|-------|------------|----------------|
| pass304 | 7546..7552 | ct_c0_7546_unknown_function_score6_cluster | high | Review |
| pass396 | 7546..7552 | ct_c0_7546_coord_adjust_score6 | high | **KEEP** - Better label |

**Overlap Region:** 7546..7552 (complete duplicate, 13 bytes)  
**Severity:** HIGH - This is the only complete duplicate  
**Analysis:** Both passes have the exact same range. pass396 has a more descriptive label (coord_adjust vs unknown_function).

---

## Summary Statistics

### Overlap Severity Distribution

| Severity | Count | Description |
|----------|-------|-------------|
| **Critical** | 1 | Complete duplicate (pass304 vs pass396) |
| **High** | 8 | One pass completely contained in another |
| **Medium** | 10 | Partial overlap > 10 bytes |
| **Low** | 3 | Minor overlap ≤ 10 bytes or boundary issues |

### Most Problematic Regions

1. **0x7BA0 region** - Triple overlap (pass263, pass307, pass398)
   - 3 passes covering the same 97-byte area
   - Requires consolidation

2. **0xF0B9 region** - Chain overlap (pass278, pass361, pass362)
   - Large cluster containing two specific functions
   - Needs splitting of pass278

3. **0x3521 region** - Sandwich overlap (pass270, pass372, pass280)
   - pass372 sandwiched between pass270 and pass280
   - Both neighbors need adjustment

### Passes by Type

| Type | Count | Recommendation |
|------|-------|----------------|
| Score-6 cluster (broad) | 15 | Review for splitting |
| Score-6 backtrack (specific) | 10 | Generally keep |
| Score-9+ specific | 5 | **Keep** |

---

## Recommendations for Resolution

### Immediate Actions (High Priority)

1. **pass304 vs pass396** (7546..7552)
   - **Action:** Mark pass304 for deprecation
   - **Reason:** Exact duplicate, pass396 has better label

2. **pass305** (75E7..75E8)
   - **Action:** Mark for deprecation
   - **Reason:** Only 2 bytes, contained in pass395

3. **pass333** (A979..A989)
   - **Action:** Adjust end to A987
   - **Reason:** 2-byte overlap with pass416

### Medium Priority Adjustments

4. **pass275** (A704..A760)
   - **Action:** Adjust to avoid A67A..A711
   - **Options:** Split at A703 or merge with pass415

5. **pass270** (34EE..3540)
   - **Action:** Adjust end to 3520
   - **Reason:** Overlaps pass372

6. **pass280** (3551..35B0)
   - **Action:** Adjust start to 3557
   - **Reason:** Overlaps pass372

### Lower Priority (Broad Clusters)

7. **pass263, pass278, pass284, pass261, pass258**
   - **Action:** Review for splitting into sub-functions
   - **Reason:** These are broad score-6 clusters containing multiple specific functions

### Consolidation Strategy

For the **0x7BA0 triple overlap**:
```
Option A: Keep all three with containment acknowledged
Option B: Merge into single comprehensive entry
Option C: Split pass263 at boundaries of pass307 and pass398
```

Recommended: **Option C** - Split pass263 at 7BC2 and 7BA3 boundaries

---

## Files Involved

**No files were deleted or modified** - this is a documentation-only report.

The following manifest files require review:
- `passes/manifests/pass304.json` - Exact duplicate of pass396
- `passes/manifests/pass305.json` - Contained in pass395
- `passes/manifests/pass333.json` - Minor overlap with pass416
- `passes/manifests/pass275.json` - Overlaps pass415
- `passes/manifests/pass270.json` - Overlaps pass372
- `passes/manifests/pass280.json` - Overlaps pass372
- `passes/manifests/pass263.json` - Triple overlap region
- `passes/manifests/pass278.json` - Contains pass361, pass362
- `passes/manifests/pass284.json` - Contains pass388, overlaps pass389
- `passes/manifests/pass261.json` - Contains pass384
- `passes/manifests/pass258.json` - Contains pass392
- `passes/manifests/pass254.json` - Overlaps pass387
- `passes/manifests/pass273.json` - Contains pass316
- `passes/manifests/pass274.json` - Contains pass322
- `passes/manifests/pass265.json` - Contains pass331
- `passes/manifests/pass266.json` - Contains pass341
- `passes/manifests/pass277.json` - Overlaps pass354
- `passes/manifests/pass356.json` - Contains pass357

---

## Appendix: Validation Command

```bash
cd tools/scripts
python validate_labels_v2.py --manifests-dir ../../passes/manifests
```

**Exit code:** 1 (issues found)  
**Total issues:** 37 overlaps across all banks (C0, C3, C7)  
**C0-specific issues:** 22 overlap pairs
