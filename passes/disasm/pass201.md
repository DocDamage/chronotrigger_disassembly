# Pass 201: C3:4A00 Data Table Analysis

## Overview
Mixed command/data page with inflated cluster score (11). High ASCII ratio indicates data table.

## Range
- **C3:4A00..C3:4AFF** (256 bytes)

## Cluster Analysis

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Cluster Score | 11 | Inflated by data coincidences |
| Width | 42 bytes | Large for single function |
| Returns | 7 | Excessive - data coincidences |
| Calls | 5 | Moderate |
| Branches | 3 | Low for 42 bytes of code |
| ASCII Ratio | 0.619 | **Very high - indicates text/data** |

## Raw Bytes (Key Section)
```
C3:4A00: 00 B0 29 7E 89 A2 11 0F B2 2C 00 54 AF B1 0E 40
C3:4A10: 02 B3 3A 00 55 C2 20 20 49 76 57 A5 0F 9E 05 4D
C3:4A20: 00 B9 4D 60 81 4D 50 00 52 02 4D 50 20 3C 4D 20
C3:4A30: B5 4D 40 B7 55 4D 20 B6 5B 40 B8 4D F0 BE 9A 60
```

## Pattern Analysis

### High ASCII Ratio (0.619)
Normal executable code typically has ASCII ratios of 0.2-0.3. This page's 0.619 ratio indicates:
- Printable text characters
- Menu strings or dialog fragments
- Structured data with high byte values ($40-$7F)

### Frequent $4D Byte
The byte $4D appears repeatedly:
- $4D = 'M' in ASCII
- $4D = EOR $xx absolute addressing opcode

In context, this is more likely **text data** than EOR instructions.

### $60 (RTS) Coincidences
Multiple $60 bytes appear:
- C3:4A23: $60 (after $4D $81)
- C3:4A37: $60 (after $9A)

These are likely data values, not return instructions.

## Data Misread Flag
```
"data_misread_flags": ["rti_rts_proximity_at_12"]
```

Multiple RTS/RTI bytes in close proximity confirms data table interpretation.

## Conclusion
This is **NOT code** - it's a data table with:
- Text/menu strings
- Lookup tables
- Pointer arrays

The cluster score of 11 is entirely inflated by byte coincidences.

## Labels
- `ct_c3_4a00_data_table` - 42-byte data region
- `ct_c3_4a20_text_fragment` - Probable text data
