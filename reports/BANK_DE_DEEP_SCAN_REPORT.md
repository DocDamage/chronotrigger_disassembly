# Bank DE Deep Scan Report

**Session 13 Discovery - Highest Quality Code Bank!**

## Executive Summary

Bank DE (offset 0x1E0000-0x1EFFFF) is the **highest quality code bank** discovered so far with a **score-19 cluster** at DE:8B35 - the **THIRD HIGHEST in the entire ROM**!

### Key Findings

| Metric | Count |
|--------|-------|
| Score-19 clusters | 1 (DE:8B35) |
| Score-18 clusters | 1 (DE:8B5D) |
| Score-10+ clusters | 5 total |
| Score-6+ clusters | 8 total |
| Score-4+ clusters | 71 total |
| **Recommended manifests** | **20** |

## Regional Analysis

### DE:8000-C000 (The GOLDMINE Region)
**This region contains ALL 5 score-10+ functions!**

| Rank | Score | Range | Width | Notes |
|------|-------|-------|-------|-------|
| 1 | 19 | DE:8B35..DE:8B57 | 35 bytes | **THIRD HIGHEST IN ROM** |
| 2 | 18 | DE:8B5D..DE:8B7F | 35 bytes | 16 child returns |
| 3 | 13 | DE:8931..DE:894F | 31 bytes | High call count |
| 4 | 12 | DE:8CF7..DE:8D0F | 25 bytes | Stack-heavy |
| 5 | 10 | DE:8A21..DE:8A3F | 31 bytes | 16 returns |

### Other Regions

| Region | Score-6+ | Best Cluster |
|--------|----------|--------------|
| DE:0000-4000 | 1 | DE:1E20..DE:1E2B (score-6) |
| DE:4000-8000 | 1 | DE:4558..DE:4577 (score-7) |
| DE:C000-FFFF | 1 | DE:D886..DE:D8A6 (score-6) |

## Recommended Manifests (20 Functions)

### Tier 1: ELITE (Score 10+) - 5 functions
```
DE:8B35..DE:8B57  (score-19)  - HIGHEST PRIORITY
DE:8B5D..DE:8B7F  (score-18)  - SECOND HIGHEST
DE:8931..DE:894F  (score-13)
DE:8CF7..DE:8D0F  (score-12)
DE:8A21..DE:8A3F  (score-10)
```

### Tier 2: HIGH (Score 6-9) - 3 functions
```
DE:4558..DE:4577  (score-7)
DE:D886..DE:D8A6  (score-6)
DE:1E20..DE:1E2B  (score-6)
```

### Tier 3: GOOD (Score 5) - 12 functions
```
DE:6FC1..DE:6FE3  (score-5, width-35)
DE:E872..DE:E893  (score-5, width-34)
DE:CB29..DE:CB49  (score-5, width-33)
DE:5794..DE:57AB  (score-5, width-24)
DE:0864..DE:0873  (score-5, width-16)
DE:25DC..DE:25EB  (score-5, width-16)
DE:5AE8..DE:5AF7  (score-5, width-16)
DE:60AD..DE:60BB  (score-5, width-15)
DE:6BF7..DE:6C03  (score-5, width-13)
DE:6A54..DE:6A5F  (score-5, width-12)
DE:BF10..DE:BF1B  (score-5, width-12)
DE:5390..DE:5399  (score-5, width-10)
```

## Technical Details

### Score-19 Cluster Analysis (DE:8B35..DE:8B57)
- **Width**: 35 bytes
- **Children**: 16 overlapping islands
- **Returns**: 16
- **Calls**: 1
- **Branches**: 1
- **ASCII ratio**: 0.629
- **Data misread flags**: None

This cluster shows exceptional code density with 16 return instructions, suggesting a complex control flow with many exit points - likely a state machine or jump table.

### Score-18 Cluster Analysis (DE:8B5D..DE:8B7F)
- **Width**: 35 bytes
- **Children**: 16 overlapping islands
- **Returns**: 16
- **Calls**: 0
- **Branches**: 1
- **Stackish**: 1
- **ASCII ratio**: 0.657

Similar structure to the score-19 cluster - likely a related function or variant.

## Existing Documentation

- Currently only **1 range documented** (pass838)
- **No existing DE manifests** found
- Bank DE is effectively **virgin territory** for disassembly

## Next Steps

1. **Immediate**: Create manifests for the 5 Tier 1 (score-10+) functions
2. **High Priority**: Document the 3 Tier 2 (score-6-9) functions  
3. **Medium Priority**: Add the 12 Tier 3 (score-5) functions
4. **Investigation**: Analyze the relationship between DE:8B35 and DE:8B5D clusters

## Files Generated

- `reports/de_0000_4000_islands.json` - Lower region scan
- `reports/de_4000_8000_islands.json` - Mid region scan
- `reports/de_8000_c000_islands.json` - Upper region scan (contains score-19!)
- `reports/de_c000_ffff_islands.json` - Bank end scan
- `reports/de_deep_scan_summary.json` - Summary data
- `reports/de_extended_scan.json` - Extended analysis with 20 targets
- `reports/BANK_DE_DEEP_SCAN_REPORT.md` - This report

---
**Scan completed**: 2026-04-08
**Total clusters found**: 154
**High-value targets identified**: 20
