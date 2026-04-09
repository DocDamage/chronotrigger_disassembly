# Pass 203: C3:5600 Data Table Analysis

## Overview
Mixed lane continue page with highly structured data patterns.

## Range
- **C3:5600..C3:56FF** (256 bytes)

## Pattern Analysis

### Regular Data Sequence
```
C3:5600: 23 09 23 29 F8 F0 22 00 29 F0 F0 21 29 E8 F0 20
C3:5610: 00 29 E0 F0 13 29 F8 E8 12 00 29 F0 E8 11 29 E8
```

### Repeating Values
The page shows a highly regular pattern with repeating values:
- `$00` - frequent null bytes
- `$21`, `$42`, `$63`, `$84` - arithmetic progression (+$21)
- `$29` - frequent byte (AND $xx absolute opcode or data)
- `$F0`, `$E8`, `$F8` - stack-relative or data values

### Structured Data Indicators
1. **Arithmetic progression**: $21, $42, $63, $84 suggests lookup table
2. **Regular spacing**: Values appear at consistent intervals
3. **High byte patterns**: $00, $10, $20, $30 structure

### Likely Contents
Based on the patterns, this region likely contains:
- **Graphics/tile data**: The regular progression suggests tile indices
- **Lookup tables**: Mathematical or coordinate tables
- **Menu/dialog data**: Structured text or command data

### Why Not Code
- No valid entry points with clean caller chains
- Data patterns too regular for executable code
- No RTS/RTL endpoints for functions
- ASCII-like patterns in places ($21 = '!')

## Comparison to Code
| Feature | This Region | Typical Code |
|---------|-------------|--------------|
| Byte pattern | Regular, repeating | Irregular, varied |
| Return instructions | None | 1-3 per function |
| Entry points | None valid | Clean prologues |
| Progression | Arithmetic (+$21) | Random access |

## Labels
- `ct_c3_5600_data_table` - Structured data region
- `ct_c3_5640_lookup_entry` - Arithmetic progression entry point
