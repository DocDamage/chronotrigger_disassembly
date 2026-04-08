# Bank C2:B700-B800 Cross-Bank Hub Analysis Report

**Analysis Date:** 2026-04-08  
**Target Region:** C2:B700..C2:B800 (256 bytes)  
**Analyst:** Automated analysis via toolkit scripts  

---

## Executive Summary

The analysis of Bank C2:B700-B800 reveals a **dense function cluster** with significant structural evidence, though direct JSL/JML cross-bank calls to C2:B716 could not be validated. The region contains **8 score-6+ function candidates** and **16 total clusters** in the B600-BFFF range, indicating this is an active code region rather than a documented cross-bank hub.

### Key Finding
**No direct JSL/JML calls to C2:B716 were found** in the ROM. The "15 bank caller" claim from previous analysis may refer to:
1. Indirect calls via jump tables
2. Dynamic dispatch through RAM pointers
3. JSL calls to other C2 addresses that branch to B716
4. Historical analysis that has not been verified

---

## 1. Cross-Bank Caller Validation Results

### Direct Call Search Results

| Call Pattern | Search Result | Count |
|--------------|---------------|-------|
| JSL $C2B716 (22 16 B7 C2) | ❌ Not found | 0 |
| JML $C2B716 (5C 16 B7 C2) | ❌ Not found | 0 |
| Any JSL to C2:B7xx range | ❌ Not found | 0 |
| Pointer refs to C2:B716 | ❌ Not found | 0 |

### JSL Calls to C2 Bank (Verified)

The ROM contains **31+ JSL calls to C2 bank**, but targeting different addresses:

| Source | Target | Notes |
|--------|--------|-------|
| C0:0059 | C2:8004 | System init |
| C0:0D18 | C2:8000 | Early boot |
| C0:1960 | C2:8000 | Event system |
| C1:BD6C | C2:60AF | Battle system |
| C1:EE27 | C2:8002 | Audio/DMA |
| C2:031B | C2:8002 | Internal call |

**Observation:** C2:8000-8004 appears to be the primary cross-bank entry point for C2, not B716.

---

## 2. Related Functions in Hub Region (C2:B600-BFFF)

### Score-6+ Clusters (8 candidates)

| Range | Score | Width | Description |
|-------|-------|-------|-------------|
| C2:B716..C2:B741 | **8** | 44 bytes | Primary cluster (2 children) |
| C2:BFE6..C2:BFFE | **7** | 25 bytes | Late bank helper |
| C2:BDF7..C2:BE15 | **6** | 31 bytes | BE00-region function |
| C2:B7B3..C2:B7CB | **6** | 25 bytes | Hub neighbor |
| C2:B9F0..C2:BA08 | **6** | 25 bytes | BA00-region function |
| C2:BFAC..C2:BFC4 | **6** | 25 bytes | Late bank helper |
| C2:BB07..C2:BB19 | **6** | 19 bytes | BB00-region function |
| C2:B8B2..C2:B8C0 | **6** | 15 bytes | B800-region tail |

### Score-5 Clusters (8 additional candidates)

| Range | Score | Width | Notes |
|-------|-------|-------|-------|
| C2:BEB5..C2:BECE | 5 | 26 bytes | RTI/RTS proximity flagged |
| C2:B825..C2:B83D | 5 | 25 bytes | B800 neighbor |
| C2:BA36..C2:BA4E | 5 | 25 bytes | BA00 continuation |
| C2:BC6D..C2:BC83 | 5 | 23 bytes | BC00 region |
| C2:BD95..C2:BDA5 | 5 | 17 bytes | BD00 region |
| C2:BC4C..C2:BC58 | 5 | 13 bytes | Small helper |
| C2:BBCC..C2:BBD5 | 5 | 10 bytes | String/data op |
| C2:BE71..C2:BE78 | 5 | 8 bytes | Minimal helper |

---

## 3. Score-6+ Entry Point Candidates (B700-B800 detailed)

### Primary Cluster: C2:B716..C2:B741 (Score=8)

```
Children:
  - C2:B716..C2:B72E (child 1)
  - C2:B729..C2:B741 (child 2)

Bytes at C2:B710-B720:
  2f b7 a5 54 8d 48 0f c5 81 f0 03 20 c2 ea 20 1f
```

**Disassembly Context:**
- C2:B716: `A5 54` (LDA $54)
- C2:B718: `8D 48 0F` (STA $0F48)
- C2:B71B: `C5 81` (CMP $81)
- C2:B71D: `F0 03` (BEQ +3)
- C2:B71F: `20 C2 EA` (JSR $EAC2)

This appears to be a **state comparison and branch routine** with hardware register access.

### Secondary Clusters

| Entry | Start | Pattern | Purpose Guess |
|-------|-------|---------|---------------|
| C2:B7B3 | C2:B772 | A2 LDA_imm | Index setup |
| C2:B9F0 | C2:B9F2 | 20 JSR | Call helper |
| C2:BB07 | C2:BB0A | A9 LDA_imm | Immediate load |
| C2:BDF7 | C2:BDFA | A2 LDA_imm | Index setup |
| C2:BFAC | C2:BFAC | 20 JSR | Call dispatcher |
| C2:BFE6 | C2:BFE6 | A9 LDA_imm | Late bank init |

---

## 4. Recommended New Manifests

### Priority 1: High Confidence (Score 6+)

```json
{
  "range": "C2:B716..C2:B741",
  "label": "ct_c2_b716_state_handler_score8",
  "score": 8,
  "callers": "UNKNOWN - no direct JSL found",
  "note": "Primary cluster with hardware register access ($0F48)"
}
```

```json
{
  "range": "C2:B7B3..C2:B7CB",
  "label": "ct_c2_b7b3_index_setup_score6",
  "score": 6
}
```

```json
{
  "range": "C2:B9F0..C2:BA08",
  "label": "ct_c2_b9f0_call_helper_score6",
  "score": 6
}
```

```json
{
  "range": "C2:BB07..C2:BB19",
  "label": "ct_c2_bb07_imm_handler_score6",
  "score": 6
}
```

### Priority 2: Medium Confidence (Score 5)

```json
{
  "range": "C2:B825..C2:B83D",
  "label": "ct_c2_b825_helper_score5",
  "score": 5
}
```

```json
{
  "range": "C2:BA36..C2:BA4E",
  "label": "ct_c2_ba36_helper_score5",
  "score": 5
}
```

```json
{
  "range": "C2:BDF7..C2:BE15",
  "label": "ct_c2_bdf7_be00_handler_score6",
  "score": 6
}
```

---

## 5. Assessment of Hub Function Purpose

### Code Pattern Analysis

The C2:B716 region contains:

1. **Hardware Register Access:**
   - `$0F48` - Unknown register (likely PPU or DMA related)
   - `$54` - Direct page variable
   - `$81` - Direct page variable

2. **Control Flow:**
   - Conditional branch (BEQ)
   - Subroutine call to $EAC2 (local C2 call)
   - RTS at end (implied by score algorithm)

3. **Neighbors:**
   - C2:B700: Entry point with `64 01` (STZ $01)
   - C2:B702: Score-6 candidate start

### Function Purpose Hypothesis

**NOT a cross-bank hub** - No evidence of:
- JSL/JML instructions
- Bank-switching code (PHB/PLB patterns)
- Return bank handling

**Likely a local state handler:**
- Compares hardware state against expected values
- Branches to error handler or continuation
- Called internally within C2 (JSR from C2:B6xx region)

### Why No Callers Found?

1. **Internal Bank Calls Only:** May only be called via JSR from within C2
2. **Indirect Jumps:** May be reached via `JMP (addr,X)` or similar
3. **Dynamic Dispatch:** Address loaded from table at runtime
4. **Historical Mislabeling:** Original "15 bank caller" claim may be incorrect

---

## 6. Files Generated

| File | Description |
|------|-------------|
| `reports/c2_b716_anchors.txt` | Call anchor report (0 calls found) |
| `reports/c2_b700_islands.txt` | Local code islands in B700-B800 |
| `reports/c2_b700_scores.txt` | Backtrack scoring results |
| `reports/c2_b700_b800_analysis_report.md` | This report |

---

## 7. Recommendations

### Immediate Actions

1. **Verify C2:B716 Cross-Bank Claim:**
   - Search disassembly passes for indirect references
   - Check if JSL targets other C2 addresses that branch to B716
   - Investigate RAM jump tables in $0F00-$0FFF region

2. **Create Manifests for Score-6+ Clusters:**
   - Priority: B716 (score 8), BFE6 (score 7), others score 6
   - Label with descriptive names based on code analysis

3. **Extend Analysis:**
   - Check C2:8000-8100 (actual cross-bank entry points)
   - Analyze C2:EAC2 (subroutine called from B716)

### Long-term

1. **Bank C2 Coverage:** 0.85% documented - needs significant work
2. **Focus on 8000-region:** Actual cross-bank entry points found there
3. **Investigate B716 callers:** Manual trace from C2 internal JSR calls

---

## Appendix: Raw Scoring Data (B600-BFFF)

```
candidate_count: 50

Score 6+ candidates:
  C2:B6AE -> best_start=C2:B68F score=6
  C2:B6D3 -> best_start=C2:B6CE score=6
  C2:B72F -> best_start=C2:B702 score=6
  C2:B7C8 -> best_start=C2:B772 score=6
  C2:B7CC -> best_start=C2:B772 score=6
  C2:B83E -> best_start=C2:B823 score=6
  C2:B979 -> best_start=C2:B95B score=6
  C2:B988 -> best_start=C2:B95B score=6
  C2:BA09 -> best_start=C2:B9F2 score=6
  C2:BA2F -> best_start=C2:BA2A score=6
  C2:BA4F -> best_start=C2:BA2A score=6
  C2:BB0B -> best_start=C2:BB0A score=6
  C2:BB1F -> best_start=C2:BB0A score=6
  C2:BBD6 -> best_start=C2:BBCE score=6
  C2:BC59 -> best_start=C2:BC51 score=6
  C2:BDAD -> best_start=C2:BD99 score=6
  C2:BDB2 -> best_start=C2:BD99 score=6
  C2:BDEB -> best_start=C2:BDE3 score=6
  C2:BDEF -> best_start=C2:BDE3 score=6
  C2:BE16 -> best_start=C2:BDFA score=6
  C2:BE33 -> best_start=C2:BDFA score=6
  C2:BE4C -> best_start=C2:BDFA score=6
  C2:BFD4 -> best_start=C2:BF7A score=6
```

---

*Report generated by Bank C2 analysis toolkit  
Scripts: build_call_anchor_report_v3.py, find_local_code_islands_v2.py, score_target_owner_backtrack_v1.py*
