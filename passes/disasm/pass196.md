# Pass 196: C3:357A..C3:3593 Disassembly

## Overview
Score-4 function at C3:357A with caller anchor validation (3 callers to C3:357B).

## Range
- **C3:357A..C3:3593** (26 bytes)

## Raw Bytes
```
C3:357A: A9 55 85 0B 20 A2 02 21 86 30 00 06 1F A9 82 00
C3:358A: 04 00 C0 85 20 A9 FF 04 00 08
```

## Callers (to C3:357B)
- C3:5584
- C3:6786
- C3:21A8

## Analysis
- LDA #$55, STA $0B - initialize DP variable
- JSR $02A2 - call to low-bank utility
- AND ($21),Y - indirect indexed operation
- STX $30
- ORA $1F06 - absolute indexed
- LDA #$0082
- TSB $00 - test and set bits
- CPY #$85 - compare immediate
- JSR $20A9 - JSR to $20A9 (may be data)

## Labels
- `ct_c3_357a_score4_function` - Entry point

## Notes
Lower confidence than C3:3500/353B due to score-4 rating. Contains some unusual instruction sequences that may indicate data intermixing or 65816 mode switching.
