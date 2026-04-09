# Pass 204: C3:5800-5FFF Analysis

## Overview
Eight pages of local_control_only regions with no verified external callers. All frozen as data.

## Session Summary

| Range | Posture | Family | Key Finding |
|-------|---------|--------|-------------|
| C3:5800..C3:58FF | local_control_only | candidate_code_lane | 4 local clusters, no external callers |
| C3:5900..C3:59FF | local_control_only | branch_fed_control_pocket | 2 suspect callers, score-4 candidates |
| C3:5A00..C3:5AFF | manual_review | branch_fed_control_pocket | Structured data patterns |
| C3:5B00..C3:5BFF | local_control_only | mixed_command_data | 2 local clusters |
| C3:5C00..C3:5CFF | local_control_only | mixed_command_data | 3 local clusters |
| C3:5D00..C3:5DFF | local_control_only | candidate_code_lane | Data misread flag: RTS proximity |
| C3:5E00..C3:5EFF | local_control_only | branch_fed_control_pocket | Score-6 candidates but no verification |
| C3:5F00..C3:5FFF | local_control_only | branch_fed_control_pocket | High ASCII ratio (0.889) |

## C3:5A00 - Structured Data Analysis

### Pattern Recognition
```
C3:5A00: 14 30 00 09 80 31 00 00 82 31 10 00 00 88 31 00
C3:5A10: 10 8A 31 10 08 10 84 31 95 00 31 30 00 8C 00 31
```

**Key Observations**:
- **$31 repeated frequently**: Appears at offsets $05, $08, $0D, $11, $15, $19, $1D, $21, etc.
- **Regular spacing**: Values appear in consistent patterns
- **Structured layout**: Suggests table/array data rather than code

### $31 Byte Analysis
- $31 = '1' in ASCII
- $31 = AND ($xx),Y opcode (but requires DP operand)
- In context: Likely data value, not opcode

## Why No Promotions

### Local Control Only
All 7 pages marked as "local_control_only" meaning:
- Code islands exist internally
- No verified external callers
- Cannot confirm as reachable code

### Suspect Callers
The few callers identified (e.g., C3:8ADA → C3:5A0A) are:
- Single callers only (not multiple)
- Suspect strength (not weak or strong)
- May be data misreads

### Score Analysis
Highest backtrack scores found:
- C3:5E34: Score 6, but local only
- C3:5E47: Score 6, but local only

Without verified external callers, these cannot be promoted.

## Labels

### C3:5900 Page
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:5900 | ct_c3_5900_data | data | Score-4 candidate area |

### C3:5A00 Page
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:5A00 | ct_c3_5a00_structured_data | data | Repeated $31 pattern |

### C3:5E00 Page
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:5E34 | ct_c3_5e34_score6_local | code | Score-6 local cluster |

## Conclusion
This session demonstrates the importance of the "local_control_only" classification. While code-like patterns exist internally, without verified external callers, these regions cannot be confidently promoted as functions. The conservative approach is to freeze them as data pending additional context.
