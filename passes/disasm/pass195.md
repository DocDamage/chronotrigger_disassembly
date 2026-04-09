# Pass 195: C3:353B..C3:3554 Disassembly

## Overview
Score-6 function at C3:353B with $A9 (LDA immediate) clean start.

## Range
- **C3:353B..C3:3554** (26 bytes)

## Raw Bytes
```
C3:353B: A9 D8 00 00 85 62 A9 82 00 85 64 40 A9 C8 14 85
C3:354B: 66 A9 36 05 6C 00 A9 FF FF 8F
```

## Analysis
- Starts with LDA #$00D8 (16-bit immediate load)
- STA $62 - storing to direct page
- LDA #$0082, STA $64
- RTI at C3:3546 - possible return or data coincidence
- LDA #$14C8, STA $66
- LDA #$0536
- JMP ($00A9) - indirect jump (may be data misread)

## Labels
- `ct_c3_353b_score6_function` - Entry point

## Notes
This region shows mixed code/data characteristics. The RTI at $3546 may indicate a boundary or could be data. The JMP ($00A9) suggests possible jump table usage or data misinterpretation.
