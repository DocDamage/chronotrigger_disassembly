# Pass 199: C3:4500 Data Table Analysis

## Overview
Candidate code lane with suspiciously high cluster score (13). Analysis reveals data table, not code.

## Range
- **C3:4548..C3:459F** (88 bytes, cluster score 13)

## Cluster Characteristics
| Metric | Value | Interpretation |
|--------|-------|----------------|
| Width | 88 bytes | Large for single function |
| Returns | 25 | Excessive - suggests data coincidences |
| Calls | 0 | No JSR/JSL - unusual for code |
| Branches | 5 | Low for 88 bytes of code |
| ASCII ratio | 0.398 | High for executable code |

## Why This Is Data, Not Code

### 25 Returns in 88 Bytes
A genuine 88-byte function would typically have:
- 1-3 actual return points
- Multiple JSR/JSL calls to subroutines
- Higher branch density for control flow

This region has:
- 25 bytes that happen to be $60 (RTS) or $40 (RTI)
- 0 JSR/JSL instructions
- Low branch density

### Data Misread Flag
The scanner correctly identified:
```
"data_misread_flags": ["rti_rts_proximity_at_20"]
```

This indicates multiple $40/$60 bytes in close proximity - a hallmark of data tables that happen to contain those values.

## Likely Contents
Based on the high ASCII ratio (0.398) and structured patterns:
- **Text table**: Menu strings or dialog fragments
- **Jump table**: Pointers for switch/case dispatch
- **Lookup table**: Game data or configuration values

## Labels
- `ct_c3_4548_data_table` - 88-byte data region
- `ct_c3_45a9_function_fragment` - Secondary cluster (score 4)
