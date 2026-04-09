# Pass 194: C3:3500..C3:3526 Disassembly

## Overview
Score-6 function at C3:3500 with verified cross-bank callers. Clean JSR start byte ($20).

## Range
- **C3:3500..C3:3526** (39 bytes)

## Raw Bytes
```
C3:3500: 20 0B A9 05 5B 03 62 05 56 25 2B A9 70 06 85 50
C3:3510: 00 A9 70 07 85 52 A9 60 08 00 85 54 A9 A0 09 85
C3:3520: 56 A9 00 90 0A 85 58
```

## Callers
- C3:5584 (JSR)
- C3:6786 (JSR)  
- C3:21A8 (JSR)

## Analysis
- Entry point at C3:3500 with JSR $A90B - likely a call to a utility function
- Contains TCD instruction ($5B) - 65816 specific
- PER instruction ($62) - 65816 PC-relative push
- Multiple LDA immediate patterns with STA to DP variables
- Appears to be setting up a data structure or transfer parameters

## Labels
- `ct_c3_3500_score6_function` - Entry point
- `ct_c3_350e_jsr_target` - Internal JSR target from pass scan

## Notes
This function appears to be a setup or initialization routine based on the pattern of LDA #immediate followed by STA to consecutive DP locations ($50, $52, $54, $56, $58).
