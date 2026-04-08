# Bank C4:9000-FFFF Analysis Report

## Executive Summary
- **Region Analyzed**: C4:9000-FFFF (96 pages, 24KB)
- **Current Pass Number**: 697
- **Next Pass Number**: 698+
- **Total New Function Candidates Identified**: 26 score-6+ clusters

## Seam Block Analysis Results

### Page Family Distribution
| Block | Candidate Code | Mixed Data | Branch Fed |
|-------|---------------|------------|------------|
| 9000-9FFF | 11 | 3 | 2 |
| A000-AFFF | 13 | 3 | 0 |
| B000-BFFF | 10 | 4 | 2 |
| C000-CFFF | 12 | 1 | 3 |
| D000-DFFF | 7 | 7 | 2 |
| E000-EFFF | 10 | 5 | 1 |
| F000-FFFF | 8 | 2 | 6 |

### Review Posture Summary
- **bad_start_or_dead_lane_reject**: 38 pages (low-quality code/data mix)
- **local_control_only**: 43 pages (internal branches only)
- **manual_owner_boundary_review**: 17 pages (needs expert review)
- **mixed_lane_continue**: 12 pages (data with scattered code)

## Score-6+ Candidates Found

### Score 6 (Highest Confidence)
| Address | Target | Start Byte | Prologue Type | Notes |
|---------|--------|------------|---------------|-------|
| C4:9013 | C4:9014 | A0 | LDY# (likely prologue) | Cross-bank caller at C4:2953 |
| C4:9D10 | C4:9D12 | A0 | LDY# | Strong candidate, score-6 cluster nearby |
| C4:9FEA | C4:9FEF | 20 | JSR | Page boundary code |
| C4:B3B1 | C4:B3BC | 20 | JSR | Strong caller from C4:09C9 |
| C4:B8B1 | C4:B8B3 | 08 | PHP | Stack operation prologue |
| C4:C0DF | C4:C0E0 | 08 | PHP | Cross-bank entries (D1:xxxx) |
| C4:C0DF | C4:C0E2 | 08 | PHP | Multi-entry function |
| C4:C4DD | C4:C4DF | 4B | PHK | Bank push (common prologue) |
| C4:C8C7 | C4:C8C8 | C2 | REP | Mode set prologue |
| C4:E0EC | C4:E0F0 | A0 | LDY# | Multiple callers |
| C4:E0EC | C4:E0F8 | A0 | LDY# | Extended function |
| C4:E35E | C4:E362 | 08 | PHP | Clear prologue pattern |
| C4:EE00 | C4:EE01 | 08 | PHP | Excellent candidate |
| C4:EFD1 | C4:EFD2 | 22 | JSL | Long jump (cross-bank) |
| C4:F21C | C4:F21E | C2 | REP | Mode set |
| C4:F9FA | C4:FA00 | A2 | LDX# | Register init |
| C4:F9FA | C4:FA05 | A2 | LDX# | Extended |
| C4:FA07 | C4:FA10 | 22 | JSL | Long subroutine call |
| C4:FDB9 | C4:FDC0 | A2 | LDX# | High page candidate |
| C4:FDFE | C4:FE01 | 08 | PHP | End-of-region code |
| C4:FE2F | C4:FE30 | 20 | JSR | Strong candidate |
| C4:FE2F | C4:FE35 | 20 | JSR | Extended range |
| C4:FF0F | C4:FF15 | 08 | PHP | Near end of bank |
| C4:FF0F | C4:FF1E | 08 | PHP | Extended |
| C4:FF5C | C4:FF5D | A2 | LDX# | Final page candidate |
| C4:FF5C | C4:FF5E | A2 | LDX# | Extended |

### Score 5 (High Confidence)
- C4:BC00 (PHB push), C4:C0DF (PHP), C4:C831 (PHP), C4:F838 (PHP)

### Score 4 (Medium-High Confidence)
- 60+ candidates across the region (see full backtrack output)

## Recommended New Manifests (Passes 698-723)

Based on the analysis, the following 26 manifests are recommended:

1. **pass698**: C4:9013..C4:902C (score-6, LDY# prologue)
2. **pass699**: C4:9D10..C4:9D2A (score-6, cluster at C4:9DE6)
3. **pass700**: C4:9FEA..C4:9FFF (score-6, JSR prologue)
4. **pass701**: C4:B3B1..C4:B3D4 (score-6, manual boundary review)
5. **pass702**: C4:B8B1..C4:B8CB (score-6, PHP prologue)
6. **pass703**: C4:C0DF..C4:C0F8 (score-6, cross-bank entries)
7. **pass704**: C4:C0DF..C4:C0FA (score-6, extended)
8. **pass705**: C4:C4DD..C4:C4F7 (score-6, PHK prologue)
9. **pass706**: C4:C8C7..C4:C8E0 (score-6, REP prologue)
10. **pass707**: C4:E0EC..C4:E108 (score-6, LDY# prologue)
11. **pass708**: C4:E0EC..C4:E110 (score-6, extended)
12. **pass709**: C4:E35E..C4:E37A (score-6, PHP prologue)
13. **pass710**: C4:EE00..C4:EE19 (score-6, PHP prologue)
14. **pass711**: C4:EFD1..C4:EFEA (score-6, JSL prologue)
15. **pass712**: C4:F21C..C4:F236 (score-6, REP prologue)
16. **pass713**: C4:F9FA..C4:FA18 (score-6, LDX# prologue)
17. **pass714**: C4:F9FA..C4:FA1D (score-6, extended)
18. **pass715**: C4:FA07..C4:FA28 (score-6, JSL prologue)
19. **pass716**: C4:FDB9..C4:FDD8 (score-6, LDX# prologue)
20. **pass717**: C4:FDFE..C4:FE19 (score-6, PHP prologue)
21. **pass718**: C4:FE2F..C4:FE48 (score-6, JSR prologue)
22. **pass719**: C4:FE2F..C4:FE4D (score-6, extended)
23. **pass720**: C4:FF0F..C4:FF2D (score-6, PHP prologue)
24. **pass721**: C4:FF0F..C4:FF36 (score-6, extended)
25. **pass722**: C4:FF5C..C4:FF75 (score-6, LDX# prologue)
26. **pass723**: C4:FF5C..C4:FF76 (score-6, extended)

## Final C4 Coverage Assessment

### Before This Analysis
- **Documented ranges**: 24
- **Coverage**: 1.12%
- **Mapped regions**: C4:0000-1000, C4:4000-5000, C4:8000-9000, C4:C000-CFFF (partial)

### After Adding New Manifests
- **New ranges added**: 26 score-6+ candidates
- **Estimated new coverage**: +3.5%
- **Total estimated coverage**: ~4.6%

### Key Findings
1. **C4:9000-CFFF**: Dense code region with many dispatch-style functions
2. **C4:D000-DFFF**: Mixed code/data region, requires careful manual review
3. **C4:E000-EFFF**: High-value code area with strong prologue patterns
4. **C4:F000-FFFF**: End-of-bank code with control flow pockets

### Cross-Bank Callers
Several functions in this region are called from other banks:
- D1:xxxx → C4:C0C0, C4:C0DF (cross-bank entries in C0-CF region)
- FD:xxxx → C4:C405, C4:C406
- F7:xxxx → C4:EFD2
- F8:xxxx → C4:E812
- FA:xxxx → C4:E812
- D6:xxxx → C4:E300
- C7:xxxx → C4:E373, C4:EBE3

## Next Steps
1. Create manifests for all 26 score-6+ candidates
2. Run verification on newly added ranges
3. Investigate score-4/5 candidates for additional mappings
4. Review mixed_command_data pages for hidden code islands
