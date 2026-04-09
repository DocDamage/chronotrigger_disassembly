# Pass 193 — C3:2C00..C3:2DFF (Frozen Mixed-Data) + C3:2E00..C3:2FFF (Frozen Table/Data Region)

## Objective
Continue the sequential C3 low-bank forward seam from pass 192's stopping point at `C3:2C00`. The `BMI $2C01` at `C3:2BF9` suggested possible cross-page flow, but detailed analysis shows the target region is not defendable as callable code.

## Result

### Frozen (mixed data / no defendable code entry):
- `C3:2C00..C3:2CFF` — mixed control/data blob, 7 BRK, 0 RTS/RTL, scattered JSR targets
- `C3:2D00..C3:2DFF` — mixed data with 32 BRK bytes, inflated score from byte coincidences
- `C3:2E00..C3:2EFF` — structured data table region, 42 BRK, 14 RTI byte coincidences
- `C3:2F00..C3:2FFF` — continuation of structured data, 40 BRK, tabular patterns

---

## Part 1: C3:2C00..C3:2CFF — Frozen Mixed-Data Page

### Raw Hex Dump

```
C3:2C00  06 17 C7 08 02 0C D0 09 20 00 51 00 20 F1 50 20
C3:2C10  16 51 20 AD F0 4F 4C 47 50 17 60 14 00 1A 00 17
C3:2C20  00 29 14 00 02 14 08 19 7E 5B 14 05 9C 00 02 14
C3:2C30  E6 AA A6 FE 86 F0 00 BF EB 52 7E 8D 0C 14 BF 4A
C3:2C40  FB 07 00 06 49 0C 14 C9 D4 06 06 04 BF 0B E3 09
C3:2C50  0D C9 00 01 10 18 05 A9 05 10 09 22 08 E2 20 8F
C3:2C60  7C 1B 53 6E 07 A7 01 23 20 71 06 E2 11 8D 00 08
C3:2C70  14 EE 14 0A AD 14 0A 80 4A 90 07 A5 F0 69 0F 8A
C3:2C80  13 02 AE E3 14 0A 65 F0 AA BF 8B 49 5D 00 04 14
C3:2C90  3D 08 8D 00 FA 15 8D 10 02 14 A5 63 A2 09 46 85
C3:2CA0  15 01 35 02 17 A9 1B 53 22 5E 0D 50 C3 60 AD 10
C3:2CB0  9A 20 70 9A 30 10 58 14 E6 AC A2 01 77 04 0F 3F
C3:2CC0  12 06 83 3F 02 B5 08 8D 16 14 AD 16 9D 20 C0 05
C3:2CD0  A9 0A 00 80 10 0D 10 9F C0 12 5C 9F 10 A6 FE 8C
C3:2CE0  10 B0 05 8A 04 69 10 2E 0D B1 51 7E 8D 12 01 22
C3:2CF0  0C 06 8D 1A 14 A9 30 00 48 8D 14 14 DD 08 8D 0E
```

### Linear-Sweep Disassembly (illustrative — not defendable as real code)

```
; ──────────────────────────────────────────────────────────────
; ROM offset: $032C00  |  SNES: C3:2C00
; FROZEN: Mixed data/control blob — 0 RTS/RTL, 7 BRK
; The BMI $2C01 from C3:2BF9 lands here but the target
; does not resolve into a coherent subroutine body.
; ──────────────────────────────────────────────────────────────

C3:2C00  06 17          ASL $17        ; Shift DP $17 left
C3:2C02  C7 08          CMP [$08]      ; Compare with DP indirect long
C3:2C04  02 0C          COP #$0C       ; ← COP — rare, data indicator
C3:2C06  D0 09          BNE $2C11      ; Branch if not equal
C3:2C08  20 00 51       JSR $5100      ; Call to $5100 — not a known C3 utility
C3:2C0B  00 20          BRK #$20       ; ← BRK
C3:2C0D  F1 50          SBC ($50),Y    ; DP indirect indexed subtract
C3:2C0F  20 16 51       JSR $5116      ; Call to $5116 — not a known utility
C3:2C12  20 AD F0       JSR $F0AD      ; Call to $F0AD — high address
C3:2C15  4F 4C 47 50    EOR $50:474C   ; Long addressing to bank $50
                                       ; Bank $50 is unusual — likely data
C3:2C19  17 60          ORA [$60],Y    ; DP indirect long indexed
C3:2C1B  14 00          TRB $00        ; Test and reset bits at DP $00
C3:2C1D  1A             INC A          ; Increment accumulator
C3:2C1E  00 17          BRK #$17       ; ← BRK
C3:2C20  00 29          BRK #$29       ; ← BRK
C3:2C22  14 00          TRB $00
C3:2C24  02 14          COP #$14       ; ← COP
C3:2C26  08             PHP            ; Push processor status
C3:2C27  19 7E 5B       ORA $5B7E,Y    ; Absolute indexed load from $5B7E
C3:2C2A  14 05          TRB $05
C3:2C2C  9C 00 02       STZ $0200      ; Store zero to RAM $0200
C3:2C2F  14 E6          TRB $E6
C3:2C31  AA             TAX
C3:2C32  A6 FE          LDX $FE        ; Load X from DP $FE
C3:2C34  86 F0          STX $F0        ; Store X to DP $F0
C3:2C36  00 BF          BRK #$BF       ; ← BRK
C3:2C38  EB             XBA            ; Exchange B/A bytes
C3:2C39  52 7E          EOR ($7E)      ; EOR with DP indirect
C3:2C3B  8D 0C 14       STA $140C      ; Store to RAM $140C
C3:2C3E  BF 4A FB 07    LDA $07:FB4A,X ; Long load from bank $07
                                       ; Bank $07 is WRAM — unusual target
C3:2C42  00 06          BRK #$06       ; ← BRK
C3:2C44  49 0C          EOR #$0C
C3:2C46  14 C9          TRB $C9
C3:2C48  D4 06          PEI $06        ; Push DP $06 indirect
C3:2C4A  06 04          ASL $04
C3:2C4C  BF 0B E3 09    LDA $09:E30B,X ; Long load from bank $09
C3:2C50  0D C9 00       ORA $00C9
C3:2C53  01 10          ORA ($10,X)
C3:2C55  18             CLC
C3:2C56  05 A9          ORA $A9
C3:2C58  05 10          ORA $10
C3:2C5A  09 22          ORA #$22
C3:2C5C  08             PHP
C3:2C5D  E2 20          SEP #$20       ; M=8 — set 8-bit accumulator
C3:2C5F  8F 7C 1B 53    STA $53:1B7C   ; Long store to bank $53
C3:2C63  6E 07 A7       ROR $A707      ; Rotate at $A707 — unusual address
C3:2C66  01 23          ORA ($23,X)
C3:2C68  20 71 06       JSR $0671      ; Call to $0671
C3:2C6B  E2 11          SEP #$11       ; X=8 — set 8-bit index
C3:2C6D  8D 00 08       STA $0800      ; Store to RAM $0800
C3:2C70  14 EE          TRB $EE
C3:2C72  14 0A          TRB $0A
C3:2C74  AD 14 0A       LDA $0A14      ; Load from RAM $0A14
C3:2C77  80 4A          BRA $2CC3      ; Branch forward
C3:2C79  90 07          BCC $2C82
C3:2C7B  A5 F0          LDA $F0        ; Load DP $F0
C3:2C7D  69 0F          ADC #$0F       ; Add $0F
C3:2C7F  8A             TXA
C3:2C80  13 02          ORA ($02,S),Y  ; Stack-relative indirect indexed
C3:2C82  AE E3 14       LDX $14E3      ; Load X from RAM $14E3
C3:2C85  0A             ASL A
C3:2C86  65 F0          ADC $F0
C3:2C88  AA             TAX
C3:2C89  BF 8B 49 5D    LDA $5D:498B,X ; Long load from bank $5D
C3:2C8D  00 04          BRK #$04       ; ← BRK
C3:2C8F  14 3D          TRB $3D
C3:2C91  08             PHP
C3:2C92  8D 00 FA       STA $FA00      ; Store to $FA00 — unusual address
C3:2C95  15 8D          ORA $8D,X
C3:2C97  10 02          BPL $2C9B
C3:2C99  14 A5          TRB $A5
C3:2C9B  63 A2          ADC ($A2,S)    ; Stack-relative indirect
C3:2C9D  09 46          ORA #$46
C3:2C9F  85 15          STA $15
C3:2CA1  01 35          ORA ($35,X)
C3:2CA3  02 17          COP #$17       ; ← COP
C3:2CA5  A9 1B          LDA #$1B
C3:2CA7  53 22          EOR ($22,S),Y  ; Stack-relative indirect indexed
C3:2CA9  5E 0D 50       LSR $500D,X    ; Shift at unusual address
C3:2CAC  C3 60          CMP ($60,S)    ; Stack-relative compare
C3:2CAE  AD 10 9A       LDA $9A10      ; Load from $9A10
C3:2CB1  20 70 9A       JSR $9A70      ; Call to $9A70 — not a known utility
C3:2CB4  30 10          BMI $2CC6
C3:2CB6  58             CLI            ; Clear interrupt disable
C3:2CB7  14 E6          TRB $E6
C3:2CB9  AC A2 01       LDY $01A2      ; Load Y from RAM $01A2
C3:2CBC  77 04          ADC [$04],Y    ; DP indirect long indexed
C3:2CBE  0F 3F 12 06    ORA $06:123F   ; Long OR from bank $06
C3:2CC2  83 3F          STA ($3F,S)    ; Stack-relative store
C3:2CC4  02 B5          COP #$B5       ; ← COP
C3:2CC6  08             PHP
C3:2CC7  8D 16 14       STA $1416      ; Store to RAM $1416
C3:2CCA  AD 16 9D       LDA $9D16      ; Load from $9D16
C3:2CCD  20 C0 05       JSR $05C0      ; Call to $05C0
C3:2CD0  A9 0A          LDA #$0A
C3:2CD2  00 80          BRK #$80       ; ← BRK
C3:2CD4  10 0D          BPL $2CE3
C3:2CD6  10 9F          BPL $2C77      ; Backward branch
C3:2CD8  C0 12          CPY #$12
C3:2CDA  5C 9F 10 A6    JML $A6:109F   ; Long jump to bank $A6!
                                       ; Bank $A6 is NOT a valid ROM bank
                                       ; in HiROM mapping — confirms data
C3:2CDE  FE 8C 10       INC $108C,X
C3:2CE1  B0 05          BCS $2CE8
C3:2CE3  8A             TXA
C3:2CE4  04 69          TSB $69
C3:2CE6  10 2E          BPL $2D16      ; Branch into next page
C3:2CE8  0D B1 51       ORA $51B1
C3:2CEB  7E 8D 12       ROR $128D
C3:2CEE  01 22          ORA ($22,X)
C3:2CF0  0C 06 8D       TSB $8D06
C3:2CF3  1A             INC A
C3:2CF4  14 A9          TRB $A9
C3:2CF6  30 00          BMI $2CF8      ; Branch to next instruction (no-op)
C3:2CF8  48             PHA
C3:2CF9  8D 14 14       STA $1414      ; Store to RAM $1414
C3:2CFC  DD 08 8D       CMP $8D08,X
C3:2CFF  0E             ASL            ; Truncated — last byte of page
```

### Analysis
- **0 RTS/RTL** — no subroutine returns anywhere in 256 bytes
- **7 BRK** opcodes — moderate density (2.7%)
- **4 COP** opcodes (`$02` at $2C04, $2C24, $2CA3, $2CC4) — COP is extremely rare in SNES games
- **6 JSR** calls but targets ($5100, $5116, $F0AD, $0671, $9A70, $05C0) are scattered and not in the known C3 low-bank utility region
- **JML $A6:109F** at $2CDA — bank $A6 is not a valid HiROM ROM bank, confirming data interpretation
- **Long addresses to unusual banks**: $50:474C, $07:FB4A, $09:E30B, $53:1B7C, $5D:498B — these bank values are atypical for CT's code
- **11 TRB ($14) bytes** — the value $14 appears frequently as data, inflating the apparent code density
- **The BMI $2C01 target** from C3:2BF9 lands at `C7 08` = `CMP [$08]`, which is not a convincing code entry point
- **Verdict**: Mixed data with embedded code-like byte sequences. Freeze and advance.

---

## Part 2: C3:2D00..C3:2DFF — Frozen Mixed-Data Page

### Raw Hex Dump

```
C3:2D00  8C 20 10 A8 14 A5 88 2E 0A 6B 8C 00 6D 8C 00 26
C3:2D10  5C 8C 30 45 18 03 42 66 01 38 18 00 69 06 00 ED
C3:2D20  17 42 85 15 03 14 10 9A 24 17 60 A5 77 20 D3 00
C3:2D30  50 A5 74 20 E7 50 A2 8D A0 53 80 0D A5 52 0F 10
C3:2D40  4F 0F 10 44 91 53 CB 07 04 22 BC CF 00 A9 22 D0
C3:2D50  2B 00 A9 EA 00 E5 00 9A F0 C0 23 85 F0 A2 89 53
C3:2D60  37 08 E3 05 00 07 A5 BA D0 03 A2 85 53 41 26 10
C3:2D70  A5 15 38 E9 08 23 00 C6 00 F0 D0 DF 64 17 64 15
C3:2D80  A9 82 95 0C 21 A9 AE 53 22 0E 1E 00 48 B0 D0 1B
C3:2D90  D8 0C 38 E5 68 16 08 68 00 E5 53 15 0E F1 70 08
C3:2DA0  CC 06 E9 A6 03 62 15 F1 04 A9 10 62 00 A9 1C 02
C3:2DB0  00 17 20 F5 39 A5 BC 1A 29 00 3F 00 D0 0B AF 71
C3:2DC0  51 7E 90 F0 05 3A 8F 07 00 A9 18 B2 00 2C A5 69
C3:2DD0  C2 01 9F 05 69 5D 0E 4C F5 00 39 00 8A 00 9C 00
C3:2DE0  A8 00 00 C0 00 AE 00 BA 00 A2 00 68 96 00 90 10
C3:2DF0  40 B4 10 30 24 32 D0 80 09 A2 00 14 20 F4 51 AF
```

### Key observations
- **32 BRK bytes** (12.5% density) — far too high for clean code
- **1 RTL at $2D09** — but this is the operand byte of `ROL $6B0A` at $2D07, not a real return:
  - `$2D07: 2E 0A 6B` = `ROL $6B0A` — the $6B at $2D09 is the high byte of the address operand
- **1 RTS at $2D3A** — but this is the operand byte of `ORA [$60],Y` at $2D39:
  - `$2D39: 17 60` = `ORA [$60],Y` — the $60 at $2D3A is the DP operand
- **3 JSL** bytes but all are operand coincidences in surrounding data
- **Verdict**: Data page with inflated score from byte coincidences. Freeze.

---

## Part 3: C3:2E00..C3:2FFF — Frozen Table/Data Region

### Raw Hex Dump (C3:2E00..C3:2EFF)

```
C3:2E00  01 0B 9B 31 11 00 0E 11 20 10 14 60 A0 10 1F 00
C3:2E10  A9 0D E5 1E F4 7F 00 00 AB A2 00 02 86 2D 86 2F
C3:2E20  00 A5 27 0A 85 29 22 07 03 00 C3 A5 39 D0 FC E6
C3:2E30  39 0B 20 20 74 B5 2B AB 56 0A 60 A5 00 AA F0 0A
C3:2E40  64 AA A2 00 40 00 A0 00 08 80 0C A5 AC F0 C0 2D
C3:2E50  64 AC A2 00 44 0E 00 D5 0B 12 8C D2 0B 01 8D E8
C3:2E60  0B 18 8D 71 35 F3 0B 0C 08 1C 00 FE 0B E7 0B 15
C3:2E70  21 81 EA 0B 64 39 60 A2 80 51 FE 1B B6 40 FE 2B
C3:2E80  2C 80 E1 2A 5C 2C 50 60 64 0F 00 32 00 24 00 72
C3:2E90  00 5A 00 80 6C 00 1C 00 2C 00 38 10 00 AA 52 10
C3:2EA0  00 78 10 00 4A 10 00 10 20 40 AA 66 20 40 3E 20
C3:2EB0  40 84 20 40 16 40 40 2A 60 40 40 44 40 40 7E 40
C3:2EC0  40 06 00 0C 06 20 04 00 02 20 07 00 06 30 B0 00
C3:2ED0  30 00 31 04 00 08 10 38 0C 00 5A 0D 02 00 11 06
C3:2EE0  20 08 30 11 20 00 00 00 02 30 10 00 08 30 00 10
C3:2EF0  80 0A 30 10 10 04 30 20 36 00 00 30 00 0C 30 20
```

### Key observations
- **42 BRK bytes** (16.4% density) — extremely high
- **14 RTI bytes** — RTI ($40) is only used in interrupt handlers; 14 in 256 bytes is impossible for real code
- **Structured data patterns** visible in hex:
  - `C3:2E88..C3:2EBF`: Pattern `00 XX 00 XX` repeating — characteristic of a 16-bit lookup table or coordinate pair array
  - `C3:2EC0..C3:2EFF`: Pattern `XX 00 YY 00` and `30 XX 30 YY` — tilemap or animation frame data
- **9 PHD ($0B) bytes** — PHD is a 1-byte opcode that appears in structured data as the value $0B
- **Verdict**: Large structured data/table region. Freeze entire block.

### Raw Hex Dump (C3:2F00..C3:2FFF)

```
C3:2F00  10 0E 30 80 30 10 20 30 00 20 22 07 00 00 24 30
C3:2F10  20 20 26 30 30 20 02 28 52 00 2A 30 10 30 2C 30
C3:2F20  00 20 30 2E 30 30 30 0A 40 00 3A 00 00 42 3A 10
C3:2F30  00 48 00 3A 00 10 4A 3A 10 10 44 00 3A 20 00 4C
C3:2F40  3A 20 10 60 00 3A 00 20 62 3A 10 20 64 00 3A 20
C3:2F50  20 D1 3F 00 00 0A 02 35 04 00 37 00 00 08 33 00
C3:2F60  10 00 09 31 00 9D 00 35 08 C8 00 02 35 18 C8 04
C3:2F70  3F B8 C8 00 06 3F C8 C8 0B 35 34 10 00 0D 37 DA
C3:2F80  C8 04 18 37 DE 00 CB 19 37 E6 CB 0F 37 EA 06 C8
C3:2F90  65 21 7D 1D 16 21 9C 05 03 01 7E 11 03 03 A2 2D
C3:2FA0  00 20 91 08 36 AC 06 AF 0B 98 0A 8D 06 81 D9 0B
C3:2FB0  20 0E 35 A9 7F 8D 20 10 22 02 20 00 9C F0 00 2F
C3:2FC0  08 F2 00 10 22 E7 38 7E 35 00 64 F1 A9 00 60 85
C3:2FD0  F0 A0 00 0C A2 3F 90 00 20 AA 36 29 80 A2 42 49
C3:2FE0  10 63 F7 01 BB 0D 20 EA 54 E6 01 3A 00 18 D1 3A
C3:2FF0  00 A2 00 46 CE 1D 33 68 10 46 10 0D 81 30 A2 0B
```

### Key observations
- **40 BRK bytes** (15.6% density) — extremely high
- **Continuation of structured data patterns** from C3:2E00:
  - `C3:2F00..C3:2F4F`: Pattern `30 XX 30 YY` and `3A XX 3A YY` — continuation of tilemap/frame data
  - `C3:2F50..C3:2F8F`: Pattern `XX 00 YY 00` with $3F markers — possibly command/parameter pairs
- **18 JSR bytes** but most are data byte coincidences (the value $20 appears frequently in structured data)
- **1 RTS at $2FC3** — byte $60 at position $C4 in the page, but context shows `A9 00 60 85` which could be `LDA #$00 / RTS / STA ...` — a possible real code island, but isolated and without a defendable entry
- **Verdict**: Continuation of structured data/table region. Freeze.

---

## Summary of C3:2C00..C3:2FFF

| Page | BRK | RTS/RTL | Code Score | Verdict |
|------|-----|---------|------------|---------|
| C3:2C00 | 7 | 0 | 40 | Mixed data — 0 returns, scattered JSR, invalid JML target |
| C3:2D00 | 32 | 0 (real) | 54 | Data — inflated score from byte coincidences |
| C3:2E00 | 42 | 0 | 104 | Structured data tables — 14 RTI coincidences |
| C3:2F00 | 40 | 1 (isolated) | 110 | Structured data continuation — tabular patterns |

**Total frozen this pass**: 1024 bytes (C3:2C00..C3:2FFF)

The entire C3:2C00-2FFF block is a contiguous data region containing:
1. Mixed control/data at C3:2C00-2CFF (transition zone from code to data)
2. Sparse data at C3:2D00-2DFF
3. Structured lookup tables at C3:2E00-2FFF (tilemap data, coordinate arrays, animation frames)

The `BMI $2C01` from C3:2BF9 was a conditional branch whose target resolved to data rather than code — this is consistent with the branch being part of a dead code path or the branch condition never being true in normal execution.

---

## Next-pass caution
Resume at `C3:3000`. The flow analysis report `c3_2900_3058_flow.json` covers up to C3:3058, suggesting the C3:3000+ region has been previously analyzed and may contain callable code. Check existing manifests and flow analysis before proceeding.
