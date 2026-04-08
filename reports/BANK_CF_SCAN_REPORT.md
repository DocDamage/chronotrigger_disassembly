# Bank CF Scan Report - CF:0000-C000 Analysis

## Executive Summary

Completed scan of CF:0000-C000 (final 48KB of Bank CF). This region represents the last major unmapped portion of Bank CF.

## Regional Analysis

### CF:0000-3FFF (Lower Region - 16KB)
- **Status**: CODE_CANDIDATE - Standard code region
- **Backtrack Candidates**: 1,058 total, 24 with score-6+
- **Local Islands**: 227 islands, 171 clusters
- **Priority**: HIGHEST - Contains most promising candidates

**Key Score-6+ Candidates:**
| Address | Score | Start Byte | Notes |
|---------|-------|------------|-------|
| CF:04C0 | 6 | - | 23 bytes, 1 call, 1 return |
| CF:1CD0 | 6 | - | 18 bytes, stack setup |
| CF:102F | 6 | 8B (PHB) | Distance 16 from target |
| CF:19FA | 6 | 08 (PHP) | Strong prologue |
| CF:1A82 | 6 | 0B (PHD) | Clean start |
| CF:200B | 6 | 08 (PHP) | Multiple targets |
| CF:2027 | 6 | 22 (JSL) | Long call pattern |
| CF:20D7 | 6 | C2 (REP) | Mode set prologue |
| CF:21EB | 6 | C2 (REP) | Distance 9 |
| CF:2285 | 6 | 08 (PHP) | Clean prologue |

### CF:4000-7FFF (Mid Region - 16KB)  
- **Status**: VECTOR_TABLE - Likely jump vector table
- **Backtrack Candidates**: 92 total, max score 4
- **Recommendation**: AVOID - Low code density, high data pattern

**Findings:**
- Heavy repeating patterns: [FF 00 FF 00] x132
- Low opcode density
- Classification suggests pointer table, not executable code

### CF:8000-BFFF (Upper Region - 16KB)
- **Status**: VECTOR_TABLE - Likely jump vector table
- **Backtrack Candidates**: 90 total, 17 score-4+
- **Recommendation**: SECONDARY - Moderate potential

**Key Score-4+ Candidates:**
| Address | Score | Notes |
|---------|-------|-------|
| CF:8059 | 5 | 13 calls, high ASCII (92%) |
| CF:8200 | 5 | JSR/RTS pattern |
| CF:83A0 | 5 | 13 calls, stackish |
| CF:84E4 | 5 | 4 calls, 1 branch |
| CF:883E | 5 | ASCII text region |
| CF:898A | 5 | Multiple callers |
| CF:8ABC | 5 | 3 calls, 96% ASCII |
| CF:8C39 | 5 | 5 calls, 8 stackish |

## Data Regions to Avoid

1. **CF:4000-7FFF**: Classified as VECTOR_TABLE
   - Pattern: [FF 00 FF 00] repeating
   - Statistics: 2118 BRK, 72 RTS, 8 RTL

2. **CF:8000-BFFF**: Classified as VECTOR_TABLE
   - Pattern: [00 20 02 20] repeating x106
   - High ASCII ratio (text data)

## Recommended Function Targets (Score-6+)

**Tier 1 - Immediate Promotion (Score 6+):**
1. `CF:04C0..CF:04D6` - Score 6, verified island
2. `CF:1CD0..CF:1CE1` - Score 6, stack setup + return
3. `CF:102F` - Score 6, PHB prologue
4. `CF:19FA` - Score 6, PHP prologue
5. `CF:1A82` - Score 6, PHD prologue
6. `CF:200B` - Score 6, PHP prologue, multi-target
7. `CF:2027` - Score 6, JSL long call
8. `CF:20D7` - Score 6, REP mode set
9. `CF:21EB` - Score 6, REP mode set
10. `CF:2285` - Score 6, PHP prologue
11. `CF:2405` - Score 6, PHP prologue
12. `CF:2499` - Score 6, PHP prologue

**Tier 2 - Secondary Candidates (Score 5):**
13. `CF:1450` - Score 5, call + branch
14. `CF:2EBE` - Score 5, branch heavy
15. `CF:6656` - Score 5, mid-region exception
16. `CF:6BA7` - Score 5, multi-return
17. `CF:3833` - Score 5, stack setup
18. `CF:383A` - Score 5, LDA# prologue

## CF Bank Completion Status

| Region | Status | Coverage |
|--------|--------|----------|
| CF:0000-3FFF | In Progress | ~5% mapped |
| CF:4000-7FFF | Data/Vectors | Avoid |
| CF:8000-BFFF | Partial | ~10% mapped |
| CF:C000-FFFF | Complete | 80%+ mapped |
| **Total CF** | **~70%** | **44 documented ranges** |

## Next Steps

1. **Immediate**: Promote 12 score-6 candidates from CF:0000-3FFF
2. **Secondary**: Evaluate 6 score-5 candidates
3. **Avoid**: Skip CF:4000-7FFF (vector table region)
4. **Review**: Manually inspect CF:8000-BFFF for false positives

## Tools Used

- `score_target_owner_backtrack_v1.py` - Backtrack scoring
- `detect_data_patterns_v1.py` - Data region identification  
- `find_local_code_islands_v2.py` - Local code cluster detection

*Report generated: Bank CF scan complete*
