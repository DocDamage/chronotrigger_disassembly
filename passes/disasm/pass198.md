# Pass 198: C3:4200 Fragment Analysis

## Overview
Mixed command/data page flagged for manual review. Disassembly revealed fragmented code patterns insufficient for promotion.

## Range
- **C3:4200..C3:42FF** (256 bytes)

## Key Findings

### Fragment 1: C3:427B (Score-6 Candidate)
```
C3:427B: JSR $2440      ; Call to low-bank function
C3:427E: .db $3B        ; Data byte (TSC opcode but out of context)
C3:427F: .db $14        ; Data
C3:4280: .db $56        ; Data (LSR $xx,X operand)
C3:4285: LDA $6282      ; Valid load from $6282
C3:4288-428E: Data bytes interspersed
C3:428F: PHP            ; Valid opcode
C3:4292: STA $8200      ; Valid store
```

### Fragment 2: C3:42C2 (High-Score Cluster)
```
C3:42C2: REP #$18       ; Clear carry and decimal flags (65816)
C3:42C4: .db $00        ; BRK - likely data
C3:42C5: STA $A801      ; Store to $A801
C3:42C8: PHP            ; Push processor status
C3:42C9: .db $01        ; ORA ($xx,X) operand
C3:42CA: JSR $8E8E      ; Call to $8E8E
C3:42CD-42CF: Data bytes
C3:42D0: BEQ #$27       ; Branch
C3:42D2: .db $E5        ; SBC $xx operand
C3:42D3: RTL            ; Return from long
```

### Fragment 3: C3:42C5 (Score-6 Candidate)
```
C3:42C5: PHP            ; Push status
C3:42C6: .db $01        ; Data
C3:42C7: JSR $8E8E      ; Call
C3:42CA-42CC: Data bytes
C3:42CD: LDX #$7A       ; Load index
C3:42CF: BEQ #$27       ; Branch if equal
C3:42D1: .db $01        ; Data
C3:42D2: STA $600E      ; Store to $600E
C3:42D5-42E1: Fragmented data/code
C3:42D3: RTL            ; Return from long
```

## Analysis
The C3:4200 page demonstrates the importance of byte-coincidence analysis:

1. **Score inflation**: Backtrack scores of 6 are inflated by data bytes that happen to match opcode patterns
2. **Fragmented execution**: No coherent function spans more than 3-4 valid instructions
3. **Data interleaving**: Valid opcodes are followed by data bytes breaking flow
4. **Missing returns**: Few clean RTS/RTL endpoints for functions

## Why Not Promoted
- No clean entry points with verified caller chains
- Fragmented execution with data bytes breaking flow
- High cluster score at C3:4548 (score 13) is actually a data table with 25 RTI/RTS coincidences
- Local clusters lack sufficient structural integrity

## Labels (Tentative)
- `ct_c3_427b_fragment` - JSR to $2440
- `ct_c3_42c2_rep_cluster` - REP #$18 start
- `ct_c3_42d3_rtl_return` - RTL return point
