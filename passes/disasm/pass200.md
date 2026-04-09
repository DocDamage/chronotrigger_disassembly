# Pass 200: C3:4900 Fragment Analysis

## Overview
"Local control only" page with fragmented code patterns. No promotable functions identified.

## Range
- **C3:4900..C3:49FF** (256 bytes)

## Key Findings

### Fragment at C3:4930
```
C3:4930: RTS               ; Return point
C3:4931: LDA #$1B          ; Load immediate
C3:4933-4934: .db $00, $00 ; Data breaks flow (LDA long operand?)
C3:4935: STA $35           ; Store to DP
C3:4937: LDA $1F           ; Load from DP
C3:4939: ASL               ; Shift left
C3:493A: STA $7480BB       ; Long store to $7E:7480BB
C3:493E: .db $7E           ; Data (bank byte from long address)
C3:493F: LDA $21           ; Load from DP
C3:4941: ASL               ; Shift left
C3:4942: STA $0007A7       ; Store to $07A7
C3:4946: DEY               ; Decrement Y
C3:4947: .db $25           ; Data (AND $xx operand)
C3:4948: STA $000D9E       ; Store to $0D9E
C3:494C: .db $23           ; Data
C3:494D: STA $0013B0       ; Store to $13B0
C3:4951: .db $02, $27      ; Data bytes
C3:4953: JMP $3810         ; Jump to $3810
```

### Analysis
The fragment shows a pattern of:
1. Valid load/store operations
2. Long addressing to bank $7E
3. Data bytes interspersed between instructions
4. Abrupt JMP to $3810

This is characteristic of **inline data** within code or a **jump table dispatch** sequence.

### Score-4 Candidate at C3:4994
```
C3:4994: JSR $0080         ; Call to low address
C3:4997: STA $F6           ; Store to DP
C3:4999: TAX               ; Transfer A to X
C3:499A: JSR $7210         ; Call to $7210
C3:499D: CLI               ; Clear interrupt disable
C3:499E: PLX               ; Pull X
C3:499F-49A1: .db $95, $CB, $0E ; Data (STA $0ECB long)
C3:49A2: LDA $F4           ; Load from DP
C3:49A4: BPL #$70          ; Branch if positive
... (fragmented)
```

## Why Not Promoted
- No coherent function entry points
- Data bytes break execution flow throughout
- Local clusters lack verified external callers
- Long addressing suggests data structures, not pure code

## Labels
- `ct_c3_4930_rts_fragment` - RTS return point
- `ct_c3_493a_long_store` - STA $7480BB long addressing
- `ct_c3_4994_jsr_fragment` - JSR $0080 entry
