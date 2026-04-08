# Bank C5:4000-4FFF Deep Scan Report

## Executive Summary
Performed comprehensive seam block analysis, backtrack scoring, and local code island discovery on Bank C5 region 4000-4FFF (16 pages). This is the highest priority target region in Bank C5 with 51 candidates and contiguous code lanes.

## Key Findings

### Score-6+ Candidates (Confirmed)
| Address | Score | Prologue | Type | Evidence |
|---------|-------|----------|------|----------|
| C5:4206 | **6** | PHP (08) | Function | Clean start, strong internal evidence |
| C5:4FBD | **6** | Cluster | Return-anchored | 2 returns, stack operations |

### Score-5 Candidates (High Confidence)
| Address | Score | Prologue | Type | Evidence |
|---------|-------|----------|------|----------|
| C5:4805 | 5 | PHD (0B) | Function | Clean start, RTS present |
| C5:44D6 | 5 | Cluster | Return-anchored | 1 call, 1 branch, 1 return |

### Score-4 Candidates (Good Evidence)
| Address | Score | Prologue | Notes |
|---------|-------|----------|-------|
| C5:405C | 4 | CMP() (DF) | RTS present |
| C5:405F | 4 | CLD (D8) | RTS present |
| C5:40D6 | 4 | JSL (22) | Long subroutine call |
| C5:4191 | 4 | STA()) (93) | RTS present |
| C5:44BF | 4 | ORA (05) | RTS present |
| C5:45F9 | 4 | LDY# (A0) | Clean start |
| C5:480F | 4 | B7 | RTS present |
| C5:4BF0 | 4 | 0x04 | RTS present |
| C5:4D3E | 4 | ASL (06) | Clean start |
| C5:4DBD | 4 | SED (F8) | Clean start |
| C5:4DFC | 4 | 0x72 | RTL present |
| C5:4E29 | 4 | TYA (98) | Clean start |
| C5:4F73 | 4 | STY (8C) | RTS present |

## Prologue Distribution (Score-4+)
- **PHP (08)**: 1 candidate - Standard interrupt/function prologue
- **PHD (0B)**: 1 candidate - Direct page preservation
- **JSL (22)**: 1 candidate - Long jump to subroutine
- **Various opcodes**: 12 other candidates with mixed prologues

## Local Code Islands Summary
- **Total islands found**: 30
- **Total clusters**: 28
- **Score-6 clusters**: 1 (C5:4FBD..C5:4FC4)
- **Score-5 islands**: 3 (C5:49FF, C5:44D6, C5:4FBD)
- **Score-4 islands**: 9

## Page-by-Page Analysis

| Page | Family | Posture | Raw Targets | Best Candidate |
|------|--------|---------|-------------|----------------|
| C5:4000 | candidate_code_lane | manual_review | 27 | C5:405C (score-4) |
| C5:4100 | candidate_code_lane | local_control | 3 | C5:4191 (score-4) |
| C5:4200 | candidate_code_lane | local_control | 2 | **C5:4206 (score-6)** |
| C5:4300 | candidate_code_lane | local_control | 1 | C5:43DB |
| C5:4400 | candidate_code_lane | local_control | 1 | C5:44BF (score-4) |
| C5:4500 | candidate_code_lane | dead_lane_reject | 1 | C5:45F9 (score-4) |
| C5:4600 | candidate_code_lane | local_control | 2 | C5:4603 |
| C5:4700 | candidate_code_lane | local_control | 1 | C5:4728 |
| C5:4800 | candidate_code_lane | dead_lane_reject | 4 | **C5:4805 (score-5)** |
| C5:4900 | mixed_command_data | local_control | 0 | C5:498F cluster |
| C5:4A00 | candidate_code_lane | local_control | 0 | C5:4A00 cluster |
| C5:4B00 | candidate_code_lane | local_control | 0 | C5:4BEF cluster |
| C5:4C00 | branch_fed_control | mixed_lane | 3 | C5:4C00 |
| C5:4D00 | candidate_code_lane | local_control | 2 | C5:4D3E (score-4) |
| C5:4E00 | candidate_code_lane | local_control | 3 | C5:4E29 (score-4) |
| C5:4F00 | candidate_code_lane | local_control | 1 | **C5:4FBD (score-6)** |

## Recommended New Manifests (Pass 579+)

### Tier 1: Immediate Promotion (Score-6)
```
Pass 579: C5:4206..C5:4220 (score-6, PHP prologue)
Pass 580: C5:4FBD..C5:4FC4 (score-6 cluster, return-anchored)
```

### Tier 2: High Priority (Score-5)
```
Pass 581: C5:4805..C5:481D (score-5, PHD prologue)
Pass 582: C5:44D6..C5:44E1 (score-5 island, JSR+RTS)
```

### Tier 3: Good Evidence (Score-4 with returns)
```
Pass 583: C5:405C..C5:4079 (score-4, CMP()+RTS)
Pass 584: C5:4191..C5:41AA (score-4, RTS present)
Pass 585: C5:44BF..C5:44D8 (score-4, ORA+RTS)
Pass 586: C5:4D3E..C5:4D57 (score-4, ASL clean)
Pass 587: C5:4DBD..C5:4DD9 (score-4, SED clean)
Pass 588: C5:4F73..C5:4F8E (score-4, STY+RTS)
```

### Tier 4: Additional Score-4 Candidates
```
Pass 589: C5:40D6..C5:40F0 (score-4, JSL prologue)
Pass 590: C5:45F9..C5:461B (score-4, LDY# clean)
Pass 591: C5:480F..C5:4836 (score-4, RTS present)
Pass 592: C5:4BF0..C5:4C18 (score-4, RTS present)
```

## Most Promising Sub-Regions for Follow-up

1. **C5:4200-4230** (Page 4200)
   - Contains score-6 candidate C5:4206 (PHP)
   - 4 local islands with good control flow
   - Strong JSR/RTS patterns

2. **C5:44C0-4500** (Pages 44-45)
   - Score-5 cluster at C5:44D6
   - Score-4 candidate at C5:44BF
   - Multiple return-anchored islands

3. **C5:4800-4850** (Page 4800)
   - Score-5 candidate C5:4805 (PHD)
   - Score-4 candidate C5:480F
   - Good internal evidence

4. **C5:4F80-4FFF** (Page 4F00)
   - Score-6 cluster at C5:4FBD
   - Return-anchored with stack operations
   - Multiple exit points

5. **C5:4900-4B00** (Pages 49-4B)
   - Score-5 island at C5:49FF
   - Mixed command data page at 4900
   - Contiguous code lanes

## Coverage Impact
- **Current C5 coverage**: 3 ranges (0.55%)
- **After Tier 1**: 5 ranges (+2)
- **After Tier 2**: 7 ranges (+4)
- **After Tier 3**: 13 ranges (+10)
- **After Tier 4**: 17 ranges (+14)

**Projected coverage**: ~3.1% (17 documented ranges)

## Entry Point Seeds Validated
- ✅ C5:4206 (PHP prologue, score-6) - **CONFIRMED**
- ✅ C5:4805 (PHD prologue, score-5) - **CONFIRMED**
- ✅ C5:405C (from previous analysis) - Score-4 confirmed

## Next Actions
1. Create manifests 579-580 for score-6 candidates
2. Create manifests 581-582 for score-5 candidates
3. Prioritize Tier 3 candidates with RTS evidence
4. Investigate C5:4200 region for additional entry points
5. Continue to C5:5000-5FFF region analysis

---
*Generated from seam block scan, backtrack analysis, and local code island discovery*
*ROM: Chrono Trigger (USA).sfc (SHA256: 06d1c2b0...30829a9)*
