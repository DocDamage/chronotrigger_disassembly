# Pass 202: C3:5700 Jump Table Analysis

## Overview
"Manual owner boundary review" page with jump table entries rather than actual functions.

## Range
- **C3:5700..C3:57FF** (256 bytes)

## Key Findings

### C3:5777 - Jump Table Entry (2 Callers)
```
C3:5777: JMP $A22A        ; Jump to $A22A (far call)
C3:577A-577B: .db $02, $63 ; Data
C3:577C: JMP $802A        ; Jump to $802A
...
```

**Analysis**: This is NOT a function entry point - it's a **jump table entry**. The callers (C3:3059, C3:5BEE) are actually jumping through this pointer to reach the real function at $A22A.

### C3:579F - Fragment with JSR
```
C3:579F: JSR $8752        ; Call to $8752
C3:57A2: LDX #$82         ; Load index
C3:57A4-57A5: .db $D2, $0D ; Data breaks flow
C3:57A6: BCC #$00         ; Branch
...
C3:57C2: JMP $5550        ; Jump to $5550
```

**Analysis**: Fragmented code with data interspersed. The JMP $5550 at the end suggests this may be part of a switch dispatch or jump table.

### Pattern Analysis
The C3:5700 region contains:
1. Jump table entries (JMP $xxxx instructions)
2. Inline data between jumps
3. Cross-bank references ($A22A, $802A, $5550)

## Why Not Promoted
- **Jump table entries are not functions**: They're dispatch vectors
- **Data interspersed**: Bytes between JMP instructions are data, not code
- **No coherent execution flow**: Each JMP terminates the "function" immediately
- **Callers are using it as a trampoline**: The callers are indirecting through these jumps

## Jump Table Structure
```
C3:5777: JMP $A22A    ; Entry 1 -> Bank $A2
C3:577C: JMP $802A    ; Entry 2 -> Bank $80 (likely data, not a bank)
...
```

This appears to be a dispatch table for far calls, common in SNES games for bank switching.

## Labels
- `ct_c3_5777_jump_a22a` - Jump table entry to $A22A
- `ct_c3_577c_jump_802a` - Jump table entry to $802A
- `ct_c3_579f_fragment` - Code fragment with JSR $8752
