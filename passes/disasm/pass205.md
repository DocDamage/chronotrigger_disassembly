# Pass 205: C3:6600 Fragment Analysis

## Overview
Manual review page with score-6 candidates but fragmented code patterns. No promotions.

## Range
- **C3:6600..C3:66FF** (256 bytes)

## Score-6 Candidates Analyzed

### C3:6643 (Score 6, Caller: C3:D95F)
```
C3:6643: LDA #$15
C3:6645: STY #$85        ; Suspect - STY with immediate?
C3:6647: .db $C0         ; Data breaks flow
C3:6648: JSR $F460       ; Valid call
C3:664B-6653: Data bytes interspersed
C3:6659: RTI             ; RTI in middle of code
C3:665B: RTS             ; Return
```

**Analysis**: Fragmented with data bytes. RTI at $6659 unusual. Cannot confirm as valid function.

### C3:66A6 (Score 6, Callers: C3:3B44, C3:577B)
```
C3:66A6: LDA #$3C
C3:66A8-66A9: .db $00, $00  ; 16-bit immediate high bytes
C3:66AA: STA $15
C3:66AC: LDA #$90
C3:66AE: .db $00         ; 16-bit immediate high byte
C3:66AF: STA $17
C3:66B1: LDA #$40
C3:66B3: LDA #$A1
C3:66B5: JSL $C30D5E     ; Cross-bank long call!
C3:66B9: SEP #$00        ; Clear all status bits
C3:66BB-66C1: Data bytes
```

**Analysis**: 
- Uses 16-bit immediate mode (LDA #$003C, LDA #$0090)
- Cross-bank JSL to $C30D5E
- Fragmented after JSL

### C3:6695 Cluster (Score 4 with RTS)
```
C3:6695: JSR $20F0
C3:6698: BVC #$6F
C3:669A: RTS             ; Return point
```

## Key Findings

### Cross-Bank Call
**JSL $C30D5E** at C3:66B5:
- Calls into bank $C3 (same bank)
- Target $0D5E is low-bank routine
- Indicates this code is part of larger system

### 16-Bit Mode Usage
- LDA with 16-bit immediates suggests native 65816 mode
- SEP #$00 clears all processor status bits
- Code may be setting up parameters for JSL

## Why Not Promoted

### Fragmentation
- Data bytes ($00) interspersed throughout
- No clean function entry/exit
- RTI appearing mid-code ($6659)

### Caller Verification
- C3:577B is from jump table (previous session)
- C3:3B44 is single suspect caller
- Insufficient caller confidence

### Boundary Issues
- Functions don't have clean boundaries
- Overlapping fragments
- Unclear where functions start/end

## Labels

| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:6600 | ct_c3_6600_rep20_fragment | code | REP #$20 fragment |
| C3:6643 | ct_c3_6643_score6_fragment | code | Score-6 candidate |
| C3:6695 | ct_c3_6695_rts_cluster | code | Cluster with RTS |
| C3:66A6 | ct_c3_66a6_score6_fragment | code | Score-6 with JSL |
| C3:66B5 | ct_c3_66b5_jsl_c30d5e | code | Cross-bank JSL |

## Conclusion
While C3:66A6 has promising characteristics (2 callers, JSL, 16-bit mode), the fragmentation and unclear boundaries prevent promotion. Conservative approach maintains database integrity.
