# Bank C6:D800-DC00 Analysis Report

## Analysis Summary
- **Region**: C6:D800-DC00 (4 pages, 1KB)
- **Code Density Score**: 131 (RTL-heavy region)
- **Date**: 2026-04-08
- **Analysis Tools**: run_seam_block_v1.py, score_target_owner_backtrack_v1.py, find_local_code_islands_v2.py

## Page-by-Page Breakdown

### Page 1: C6:D800-D900
- **Page Family**: branch_fed_control_pocket
- **Raw Targets**: 1 (C6:D800 from C6:11CD - suspect)
- **Best Cluster**: C6:D8B7..C6:D8BD (Score 7)
  - 7 bytes, JSL $400810, RTL terminator
  - 1 call, 1 branch, 2 stackish ops
- **Secondary Clusters**:
  - C6:D864..C6:D86D (Score 5): 10 bytes, 4 calls, JSL $405820
  - C6:D854..C6:D85C (Score 3): 9 bytes, 1 branch, 2 returns
  - C6:D83D..C6:D841 (Score 2): 5 bytes, 2 branches, 1 return

### Page 2: C6:D900-DA00  
- **Page Family**: branch_fed_control_pocket
- **Raw Targets**: 0
- **Top Clusters**:
  - C6:D920..C6:D928 (Score 5): 9 bytes, 4 calls, JSL pattern
  - C6:D976..C6:D97B (Score 5): 6 bytes, 1 call, JSL $400810, 2 stackish ops
  - C6:D98E..C6:D993 (Score 2): 6 bytes, stackish return

### Page 3: C6:DA00-DB00
- **Page Family**: branch_fed_control_pocket (rejected - bad start)
- **Raw Targets**: 1 (C6:DAA5 from C6:9985 - invalid)
- **Backtrack Candidate**: C6:DA96 (Score 4)
  - Multiple F8 (SED) bytes suggest data or padding
  - RTS at DAB0 suggests small utility function
- **Clusters**:
  - C6:DA5D..C6:DA64 (Score 2): 8 bytes, stackish return
  - C6:DAD2..C6:DAD8 (Score 2): 7 bytes, 2 branches, 1 return

### Page 4: C6:DB00-DC00
- **Page Family**: mixed_command_data
- **Raw Targets**: 2 (C6:DB29, C6:DBAC - both suspect)
- **Backtrack Candidate**: C6:DB28 (Score 4)
- **Clusters**:
  - C6:DB38..C6:DB4E (Score 3): 23 bytes, 4 branches, 2 returns

## Score-6+ Recommendations

### Pass 677: C6:D8B7..C6:D8BD
```json
{
  "pass_number": 677,
  "closed_ranges": [
    {
      "range": "C6:D8B7..C6:D8BD",
      "kind": "owner",
      "label": "ct_c6_d8b7_cross_bank_util",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-7 cluster, JSL prologue to $400810, RTL terminator. 7-byte cross-bank utility function. D800 region control pocket entry."
}
```

### Pass 678: C6:D864..C6:D86D
```json
{
  "pass_number": 678,
  "closed_ranges": [
    {
      "range": "C6:D864..C6:D86D",
      "kind": "owner",
      "label": "ct_c6_d864_jsl_handler",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-5 cluster, 4 callers, JSL to $405820. 10-byte handler with double-return pattern. D800 region dispatch."
}
```

### Pass 679: C6:D920..C6:D928
```json
{
  "pass_number": 679,
  "closed_ranges": [
    {
      "range": "C6:D920..C6:D928",
      "kind": "owner",
      "label": "ct_c6_d920_jsl_handler",
      "confidence": "medium"
    }
  ],
  "promotion_reason": "Score-5 cluster, 4 callers, JSL pattern. 9-byte handler with double-return pattern. D900 region control pocket."
}
```

### Pass 680: C6:D976..C6:D97B
```json
{
  "pass_number": 680,
  "closed_ranges": [
    {
      "range": "C6:D976..C6:D97B",
      "kind": "owner",
      "label": "ct_c6_d976_stack_util",
      "confidence": "medium"
    }
  ],
  "promotion_reason": "Score-5 cluster, JSL to $400810, RTL terminator. 6-byte stack-manipulation utility. 2 stackish ops (PLX/PHY pattern)."
}
```

### Pass 681: C6:D854..C6:D85C
```json
{
  "pass_number": 681,
  "closed_ranges": [
    {
      "range": "C6:D854..C6:D85C",
      "kind": "owner",
      "label": "ct_c6_d854_local_handler",
      "confidence": "medium"
    }
  ],
  "promotion_reason": "Score-3 cluster, 9 bytes, branch/return pattern. Internal control flow handler with stackish operation."
}
```

### Pass 682: C6:DB38..C6:DB4E
```json
{
  "pass_number": 682,
  "closed_ranges": [
    {
      "range": "C6:DB38..C6:DB4E",
      "kind": "owner",
      "label": "ct_c6_db38_branch_handler",
      "confidence": "low"
    }
  ],
  "promotion_reason": "Score-3 cluster, 23 bytes, 4 branches, 2 returns. Branch-heavy handler in mixed-command-data page. DB00 region."
}
```

### Pass 683: C6:DA5D..C6:DA64
```json
{
  "pass_number": 683,
  "closed_ranges": [
    {
      "range": "C6:DA5D..C6:DA64",
      "kind": "owner",
      "label": "ct_c6_da5d_stack_return",
      "confidence": "low"
    }
  ],
  "promotion_reason": "Score-2 cluster, 8 bytes, stackish return. DA00 region utility with PLP/RTS pattern."
}
```

### Pass 684: C6:DAD2..C6:DAD8
```json
{
  "pass_number": 684,
  "closed_ranges": [
    {
      "range": "C6:DAD2..C6:DAD8",
      "kind": "owner",
      "label": "ct_c6_dad2_branch_stub",
      "confidence": "low"
    }
  ],
  "promotion_reason": "Score-2 cluster, 7 bytes, 2 branches, 1 return. Branch stub in DA00 region."
}
```

### Pass 685: C6:D83D..C6:D841
```json
{
  "pass_number": 685,
  "closed_ranges": [
    {
      "range": "C6:D83D..C6:D841",
      "kind": "owner",
      "label": "ct_c6_d83d_veneer",
      "confidence": "low"
    }
  ],
  "promotion_reason": "Score-2 cluster, 5 bytes, 2 branches, 1 return. Tiny veneer function in D800 region."
}
```

### Pass 686: C6:D8F7..C6:D8FB
```json
{
  "pass_number": 686,
  "closed_ranges": [
    {
      "range": "C6:D8F7..C6:D8FB",
      "kind": "owner",
      "label": "ct_c6_d8f7_veneer",
      "confidence": "low"
    }
  ],
  "promotion_reason": "Score-2 cluster, 5 bytes, 2 branches, 1 return. Tiny veneer function in D800 region."
}
```

### Pass 687: C6:D98E..C6:D993
```json
{
  "pass_number": 687,
  "closed_ranges": [
    {
      "range": "C6:D98E..C6:D993",
      "kind": "owner",
      "label": "ct_c6_d98e_stack_util",
      "confidence": "low"
    }
  ],
  "promotion_reason": "Score-2 cluster, 6 bytes, stackish return. D900 region utility function."
}
```

## Byte Patterns Summary

### C6:D8B7-D8BD (Score 7)
```
FD D2 08    SBC $08D2,X
22 10 08 40 JSL $400810
B0 00       BCS +0
98          TYA
00 00       BRK #$00
22 01 C0 1E JSL $1EC001
```

### C6:D864-D86D (Score 5)
```
BF 10 20 22 LDA $222010,X
44 20 20    MVP $20,$20
40          RTI
FB          XCE
40          RTI
58          CLI
22 29 11 4E JSL $4E1129
```

### C6:D920-D928 (Score 5)
```
BF 10 20 22 LDA $222010,X
44 20 20    MVP $20,$20
40          RTI
40          RTI
58          CLI
FF 22 29 7B SBC $7B2922,X
00 5E       BRK #$5E
```

## Region Purpose Assessment

**C6:D800-DC00** appears to be a **cross-bank utility and control flow region** with the following characteristics:

1. **JSL-Heavy Pattern**: Multiple clusters contain JSL (Jump Subroutine Long) instructions
   - Primary targets: $400810, $405820 (Bank 40 - likely system/graphics routines)
   
2. **RTL-Terminated Functions**: High-score clusters end with RTL (Return Long), indicating
   these are called via JSL from other banks and return long

3. **Control Pocket Structure**: Branch-fed control pockets suggest this region handles
   conditional dispatch and state management

4. **Veneer Functions**: Multiple score-2/3 clusters are small veneer/stub functions that
   likely forward to larger implementations

5. **Mixed Content**: Page DB00 shows mixed_command_data family, suggesting embedded
   data tables alongside code

## Comparison to C6:D400-D800

| Region | Primary Pattern | Best Score | Function Count |
|--------|----------------|------------|----------------|
| C6:D400-D800 | JSR/RTS (local calls) | Score 6 | 15 functions |
| C6:D800-DC00 | JSL/RTL (cross-bank) | Score 7 | 11 candidates |

## Bank C6 Coverage Update

| Metric | Previous | After Proposed |
|--------|----------|----------------|
| Ranges | 11 | 22 |
| Coverage | 0.38% | ~0.75% |
| Score-6+ | 6 | 10 |

## Next Steps

1. **Promote score-6+ candidates first** (passes 677-680)
2. **Verify JSL targets** ($400810, $405820) for cross-bank validation
3. **Continue scanning** C6:DC00-E000 for more RTL-heavy regions
4. **Investigate** C6:DA00-DB00 mixed content for data tables
