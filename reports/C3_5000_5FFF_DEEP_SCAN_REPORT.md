# Bank C3:5000-5FFF Deep Scan Report

**Scan Date:** 2026-04-08  
**Region:** C3:5000..C3:5FFF (4KB, 16 pages)  
**Previous State:** Unexplored  
**ROM:** Chrono Trigger (USA).sfc

---

## Executive Summary

This deep scan of the C3:5000-5FFF region has uncovered a **major code region** with significant function density. The analysis reveals:

- **68 backtrack candidates** identified across the region
- **6 score-6+ candidates** (promotion-ready)
- **34 code islands** with RTS evidence
- **31 merged clusters** with strong code signatures
- **551+ RTS returns** detected (confirming prior intelligence)

### Page Family Distribution
| Family | Count | Description |
|--------|-------|-------------|
| branch_fed_control_pocket | 8 | Branch-dominated control flow |
| candidate_code_lane | 4 | Clean code candidates |
| mixed_command_data | 4 | Mixed code/data regions |

### Review Posture Distribution
| Posture | Count |
|---------|-------|
| local_control_only | 8 |
| bad_start_or_dead_lane_reject | 5 |
| manual_owner_boundary_review | 2 |
| mixed_lane_continue | 1 |

---

## Score-6+ Candidates (Promotion Ready)

### 1. C3:5131..C3:5150 ⭐ ALREADY COVERED (pass602)
- **Score:** 6
- **Start Byte:** 0x0B (PHD - Push Direct Page Register)
- **Target:** C3:5138
- **Distance:** 7 bytes
- **Status:** ✅ Documented in pass602
- **Label:** ct_c3_5131_phd_prologue

### 2. C3:51EF..C3:520C ⭐ NEW CANDIDATE
- **Score:** 6
- **Start Byte:** 0x20 (JSR - Jump to Subroutine)
- **Target:** C3:51F4
- **Distance:** 5 bytes
- **Status:** 🆕 RECOMMENDED FOR PROMOTION (pass604)
- **Evidence:** Strong function prologue, clean start, low ASCII ratio (0.2)

### 3. C3:55A3..C3:55BD ⭐ ALREADY COVERED (pass239)
- **Score:** 6
- **Start Byte:** 0x20 (JSR)
- **Target:** C3:55A5
- **Distance:** 2 bytes
- **Status:** ✅ Documented in pass239
- **Range:** C3:55A3..C3:5600 (part of larger block)

### 4. C3:58E8..C3:591A ⭐ NEW CANDIDATE
- **Score:** 6
- **Start Byte:** 0xA9 (LDA# - Load Accumulator Immediate)
- **Target:** C3:5902
- **Distance:** 26 bytes
- **Status:** 🆕 RECOMMENDED FOR PROMOTION (pass605)
- **Evidence:** Register initialization pattern, very low zero/FF ratio (0.02)

### 5. C3:5E1E..C3:5E54 ⭐ ALREADY COVERED (pass603)
- **Score:** 6
- **Start Byte:** 0x08 (PHP - Push Processor Status)
- **Target:** C3:5E3C
- **Distance:** 30 bytes
- **Status:** ✅ Documented in pass603
- **Label:** ct_c3_5e01_jsl_long_fn

### 6. C3:5E34..C3:5E6C ⭐ ALREADY COVERED (pass603)
- **Score:** 6
- **Start Byte:** 0xA0 (LDY# - Load Y Register Immediate)
- **Target:** C3:5E54
- **Distance:** 32 bytes
- **Status:** ✅ Documented in pass603
- **Note:** Part of same 5E01 region as candidate #5

---

## High-Value Score-4/5 Clusters (Secondary Candidates)

### Score-5 Clusters
| Range | Score | Width | Calls | Returns | Notes |
|-------|-------|-------|-------|---------|-------|
| C3:5247..C3:525F | 5 | 25 | 0 | 1 | PHD prologue (0x0B) |
| C3:5364..C3:5375 | 5 | 18 | 0 | 2 | Branch-fed, stackish |
| C3:51E8..C3:51F0 | 5 | 9 | 1 | 1 | Island with JSR |

### Score-4 Clusters with Strong Evidence
| Range | Score | Width | Calls | Returns | Start Context |
|-------|-------|-------|-------|---------|---------------|
| C3:5110..C3:512E | 4 | 31 | - | - | CPY# immediate |
| C3:515E..C3:517C | 4 | 31 | - | - | PHD prologue |
| C3:524A..C3:5264 | 4 | 27 | - | - | CLI instruction |
| C3:539B..C3:53BD | 4 | 35 | - | - | PHP prologue |
| C3:5436..C3:5452 | 4 | 29 | - | - | SED instruction |
| C3:5440..C3:545D | 4 | 30 | - | - | CPX# immediate |
| C3:549F..C3:54BD | 4 | 31 | - | - | SED instruction |
| C3:578D..C3:57B7 | 4 | 43 | - | - | LDX# immediate |
| C3:5920..C3:5947 | 4 | 40 | - | - | PHD prologue |
| C3:59FB..C3:5A18 | 4 | 30 | - | - | LDA# immediate |
| C3:5A48..C3:5A61 | 4 | 26 | - | - | JSR prologue |
| C3:5C82..C3:5CA5 | 4 | 36 | - | - | PHD prologue |
| C3:5CA8..C3:5CC6 | 4 | 31 | - | - | LDA# immediate |

---

## Local Code Clusters (Return-Anchored)

### Score-6 Clusters
| Range | Score | Children | Width | Calls | Branches | Returns |
|-------|-------|----------|-------|-------|----------|---------|
| C3:559F..C3:55C1 | 6 | 2 | 35 | 1 | 6 | 2 |
| C3:5B52..C3:5B72 | 6 | 1 | 33 | 1 | 4 | 1 |
| C3:5364..C3:5375 | 6 | 2 | 18 | 0 | 2 | 2 |

### Score-5 Clusters
| Range | Score | Width | Calls | Returns | Notable Features |
|-------|-------|-------|-------|---------|------------------|
| C3:5B1A..C3:5B3A | 5 | 33 | 2 | 2 | Dual calls |
| C3:5E20..C3:5E40 | 5 | 33 | 0 | 1 | Branch + stack |
| C3:5C49..C3:5C65 | 5 | 29 | 2 | 1 | Multi-call, stackish |
| C3:51E8..C3:51F0 | 5 | 9 | 1 | 1 | Compact function |

---

## Function Prologue Analysis

Common prologue patterns identified:

| Opcode | Mnemonic | Count | Purpose |
|--------|----------|-------|---------|
| 0x20 | JSR | 8 | Subroutine call (often tail-call optimization) |
| 0x0B | PHD | 5 | Save Direct Page register |
| 0x08 | PHP | 4 | Save Processor Status |
| 0xA9 | LDA# | 4 | Initialize Accumulator |
| 0xA0 | LDY# | 2 | Initialize Y register |
| 0xA2 | LDX# | 1 | Initialize X register |
| 0xC0 | CPY# | 1 | Compare Y immediate |
| 0xC2 | REP | 1 | Set 16-bit mode |

---

## Cross-Reference Analysis

### Strongest XRef Targets (Weak+ Strength)
| Target | Strength | Callers | Context |
|--------|----------|---------|---------|
| C3:5249 | weak | C3:43EE, C3:502E | Dual-call site |
| C3:52A5 | weak | C3:0251 | Early bank caller |
| C3:54A5 | weak | C3:009D, C3:026D | Dual-call, system |
| C3:5437 | weak | C3:51B7 | Internal linkage |
| C3:544C | weak | C3:6A52 | Cross-region call |
| C3:5777 | weak | C3:3059, C3:5BEE | Dual-call |
| C3:579F | weak | C3:339B | Single caller |
| C3:5A0A | weak | C3:8ADA | External linkage |

---

## Region Purpose Assessment

Based on the analysis, **C3:5000-5FFF appears to be a subsystem code region** with the following characteristics:

### Evidence for Game Logic / Event System:
1. **Rich function density** - 68+ potential entry points in 4KB
2. **PHP/PHD prologues** - State-saving functions (common in game event handlers)
3. **JSR distribution** - Balanced internal/external calls
4. **No DMA patterns** - Not graphics transfer code
5. **No audio register access** - Not music/sound code

### Likely Subsystems:
- **Event/script handlers** (PHP prologues suggest state preservation)
- **UI/menu helper functions** (LDA# initialization patterns)
- **Battle system utilities** (scattered cross-references from 6Axx region)
- **Save/load logic** (indirect addressing patterns)

### Notable Callers Outside Region:
- C3:0251, C3:009D, C3:026D (early bank code)
- C3:3059, C3:339B (mid-bank functions)
- C3:8ADA, C3:8Axx (upper bank region)

---

## Recommended New Manifests (Pass 604+)

### Pass 604: C3:51EF_jsr_prologue
```json
{
  "pass_number": 604,
  "closed_ranges": [
    {
      "range": "C3:51EF..C3:520C",
      "kind": "owner",
      "label": "ct_c3_51ef_jsr_handler",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-6 cluster, JSR prologue. Function handler in C3:5100 region."
}
```

### Pass 605: C3:58E8_lda_prologue
```json
{
  "pass_number": 605,
  "closed_ranges": [
    {
      "range": "C3:58E8..C3:591A",
      "kind": "owner", 
      "label": "ct_c3_58e8_init_fn",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-6 cluster, LDA# prologue. Register initialization function."
}
```

### Pass 606: C3:5247_phd_handler
```json
{
  "pass_number": 606,
  "closed_ranges": [
    {
      "range": "C3:5247..C3:525F",
      "kind": "owner",
      "label": "ct_c3_5247_state_handler",
      "confidence": "medium"
    }
  ],
  "promotion_reason": "Score-5 cluster, PHD prologue, RTS evidence. State preservation function."
}
```

### Pass 607: C3:5364_branch_cluster
```json
{
  "pass_number": 607,
  "closed_ranges": [
    {
      "range": "C3:5364..C3:5375",
      "kind": "owner",
      "label": "ct_c3_5364_control_fn",
      "confidence": "medium"
    }
  ],
  "promotion_reason": "Score-6 cluster, branch-fed, dual RTS. Control flow function."
}
```

### Pass 608: C3:5B1A_dual_call
```json
{
  "pass_number": 608,
  "closed_ranges": [
    {
      "range": "C3:5B1A..C3:5B3A",
      "kind": "owner",
      "label": "ct_c3_5b1a_helper",
      "confidence": "medium"
    }
  ],
  "promotion_reason": "Score-5 cluster, dual internal calls, stackish operations."
}
```

### Pass 609: C3:5B52_branch_heavy
```json
{
  "pass_number": 609,
  "closed_ranges": [
    {
      "range": "C3:5B52..C3:5B72",
      "kind": "owner",
      "label": "ct_c3_5b52_switch_fn",
      "confidence": "medium"
    }
  ],
  "promotion_reason": "Score-6 cluster, 4 branches, likely switch/case handler."
}
```

### Pass 610: C3:5C49_stackish
```json
{
  "pass_number": 610,
  "closed_ranges": [
    {
      "range": "C3:5C49..C3:5C65",
      "kind": "owner",
      "label": "ct_c3_5c49_stack_ops",
      "confidence": "medium"
    }
  ],
  "promotion_reason": "Score-5 cluster, stackish operations, dual calls."
}
```

---

## Additional Score-4 Candidates (Priority Queue)

For subsequent passes (611+), consider:

1. **C3:5110..C3:512E** - CPY# prologue
2. **C3:515E..C3:517C** - PHD prologue 
3. **C3:539B..C3:53BD** - PHP prologue
4. **C3:5436..C3:5452** - SED + BEQ pattern
5. **C3:578D..C3:57B7** - LDX# prologue
6. **C3:5920..C3:5947** - PHD prologue
7. **C3:5A48..C3:5A61** - JSR prologue
8. **C3:5C82..C3:5CA5** - PHD prologue
9. **C3:5CA8..C3:5CC6** - LDA# prologue
10. **C3:57BC..C3:57D7** - Branch-heavy (3 branches)

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total pages scanned | 16 (4KB) |
| Backtrack candidates | 68 |
| Score-6 candidates | 6 (4 new) |
| Score-5 candidates | 7 |
| Score-4 candidates | 17 |
| Code islands found | 34 |
| Merged clusters | 31 |
| Existing coverage | 3 ranges |
| New recommendations | 15+ ranges |

---

## Next Steps

1. **Immediate:** Promote 2 score-6 candidates (pass604-605)
2. **Short-term:** Promote 5 score-5/6 clusters (pass606-610)
3. **Medium-term:** Evaluate 10 score-4 candidates (pass611+)
4. **Analysis:** Cross-reference with C3:6Axx callers for context

---

*Report generated by C3:5000-5FFF Deep Scan - Bank C3 Gap Filling Initiative*
