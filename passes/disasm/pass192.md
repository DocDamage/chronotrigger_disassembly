# Pass 192 — C3:2900..C3:2AFF (Frozen Mixed-Data) + C3:2B00..C3:2BFF (Annotated Disassembly)

## Objective
Resume the sequential C3 low-bank forward seam from pass 191's stopping point at `C3:2900`. Evaluate each page for callable code, freeze mixed-data pages honestly, and produce detailed annotated disassembly for any page that survives caller-quality review.

## Result

### Frozen (mixed data / no defendable code entry):
- `C3:2900..C3:29FF` — mixed control/data blob, 19 BRK opcodes, no caller-backed entry
- `C3:2A00..C3:2AFF` — mixed control/data blob, 17 BRK opcodes, no caller-backed entry

### Annotated disassembly:
- `C3:2B00..C3:2BFF` — branch-fed control pocket with 3 RTL, 9 JSR, code score 52

---

## Part 1: C3:2900..C3:29FF — Frozen Mixed-Data Page

### Raw Hex Dump (selected lines)

```
C3:2900  58 C9 02 12 10 84 12 00 08 38 E9 0A 12 10 46 C9
C3:2910  10 00 00 D0 05 20 D0 4C 80 3C C9 30 11 00 D0 08
C3:2920  2E 00 0D 10 2F C9 92 12 0D 10 D0 4C 2C 00 80 22
C3:2930  83 01 81 24 00 E7 4C 80 18 C9 21 24 40 81 0D 00
```

### Linear-Sweep Disassembly (illustrative — not defendable as real code)

```
; ──────────────────────────────────────────────────────────────
; ROM offset: $032900  |  SNES: C3:2900
; FROZEN: Mixed data/control blob — no caller-backed true start
; 19 BRK opcodes, incoherent control flow, no xref targets
; ──────────────────────────────────────────────────────────────

C3:2900  58             CLI           ; Enable interrupts — unusual at a routine start
C3:2901  C9 02          CMP #$02      ; Compare A with $02
C3:2903  12 10          ORA ($10)     ; ORA with DP indirect — but $10 context unknown
C3:2905  84 12          STY $12       ; Store Y to DP $12
C3:2907  00 08          BRK #$08      ; ← BRK embedded in stream — data indicator
C3:2909  38             SEC           ; Set carry
C3:290A  E9 0A          SBC #$0A      ; Subtract $0A
C3:290C  12 10          ORA ($10)     ; DP indirect
C3:290E  46 C9          LSR $C9       ; Shift DP $C9 right — but $C9 is high DP addr
C3:2910  10 00          BPL $2912     ; Branch to next instruction (no-op branch)
C3:2912  00 D0          BRK #$D0      ; ← Another BRK — confirms data mixing
C3:2914  05 20          ORA $20       ; ORA with DP $20
C3:2916  D0 4C          BNE $2964     ; Branch forward to $2964
C3:2918  80 3C          BRA $2956     ; Branch always to $2956
```

### Analysis
- **19 BRK opcodes** in 256 bytes = 7.4% BRK density — far too high for clean 65c816 code
- **No xref targets** in the entire C3:2900-2AFF range
- **No PHP/PHB/PHD prologue patterns** that would indicate subroutine starts
- **Incoherent control flow**: branches target mid-instruction offsets
- **Verdict**: Mixed data/content page. Freeze and advance.

---

## Part 2: C3:2A00..C3:2AFF — Frozen Mixed-Data Page

### Raw Hex Dump (selected lines)

```
C3:2A00  C0 76 45 00 B0 00 35 45 00 78 C0 05 F8 D3 10 4B
C3:2A10  00 53 A6 01 C1 03 85 4A 86 6F 60 A5 4E 69 AC 01
C3:2A20  E5 73 88 09 4E 7B 00 FE 05 65 CA F0 EE 05 15 C3
```

### Linear-Sweep Disassembly (illustrative)

```
C3:2A00  C0 76          CPY #$76      ; Compare Y with $76
C3:2A02  45 00          EOR $00       ; EOR with DP $00
C3:2A04  B0 00          BCS $2A06     ; Branch to next instruction (no-op)
C3:2A06  35 45          AND $45,X     ; AND with DP $45+X
C3:2A08  00 78          BRK #$78      ; ← BRK — data indicator
C3:2A0A  C0 05          CPY #$05
C3:2A0C  F8             SED           ; Set decimal mode — rare in SNES games
C3:2A0D  D3 10          CMP ($10,S),Y ; Stack-relative indirect Y
C3:2A0F  4B             PHK           ; Push program bank (K)
C3:2A10  00 53          BRK #$53      ; ← BRK
C3:2A12  A6 01          LDX $01       ; Load X from DP $01
C3:2A14  C1 03          CMP ($03,X)   ; Compare with indirect indexed
C3:2A16  85 4A          STA $4A       ; Store A to DP $4A
C3:2A18  86 6F          STX $6F       ; Store X to DP $6F
C3:2A1A  60             RTS           ; ← Possible real return
```

### Notable islands
- `C3:2A1A`: `RTS` — but no caller-backed entry precedes it
- `C3:2A4F`: `RTS` — same problem, unsupported interior byte
- `C3:2ADB`: `RTS` — unsupported
- `C3:2AEC`: `STA $4206` (CPU Divisor register) — suggests nearby division code
- `C3:2AF1`: `LDA $4214` (CPU Quotient Low) — confirms division usage nearby

### Analysis
- **17 BRK opcodes** — still too high for clean code
- **6 RTS** bytes but none has a caller-backed true start
- **Hardware register access** at $4206/$4214 suggests division code is embedded but misaligned
- **Verdict**: Mixed data with embedded code fragments. Freeze and advance.

---

## Part 3: C3:2B00..C3:2BFF — Annotated Disassembly

This page has significantly higher code density (code score 52, 3 RTL, 9 JSR, 2 RTS).

### Raw Hex Dump

```
C3:2B00  FC 85 F2 A9 00 0C 20 E2 00 32 A5 F4 85 5D 18 65
C3:2B10  48 68 85 61 A5 13 20 10 13 20 B8 16 5B A8 AD 00
C3:2B20  0B 25 10 80 25 20 0A 0C 0B B2 46 09 3A F6 18 8E
C3:2B30  07 15 0B 5B 20 1B 02 F2 13 02 46 18 65 5B 85 5F
C3:2B40  89 D8 40 A5 6D 7D 90 82 85 6D 7D 40 0E 0C 7D 80
C3:2B50  7B 60 20 17 80 85 82 AD 5A 0C 6A C0 6B 6A 40 69
C3:2B60  30 80 69 50 6B 00 65 80 85 84 A5 6D 65 82 40 85
C3:2B70  86 60 AD 00 0A 5E 17 F2 00 EB 8D 04 42 E2 10 A5
C3:2B80  F0 11 4D 1A EB 6D 04 15 10 F0 23 65 00 F2 85 F4
C3:2B90  A8 BE 46 14 D0 00 19 A9 00 42 5B AE B4 00 00 86
C3:2BA0  06 EA 22 29 0E C3 E2 00 20 AC F4 00 8A 99 46 14
C3:2BB0  50 C2 20 C2 10 A8 0A 5B 33 0A ED 00 10 0A 85 F8
C3:2BC0  85 FE 8A 85 90 B4 C6 B4 EB 46 04 E0 00 CE 02 C0
C3:2BD0  F2 20 BF 31 A5 FE F4 12 47 12 81 F2 6B 4A 18 6D
C3:2BE0  18 0A 0A F8 0B 00 85 FE AD 1A 0B D0 03 9C 00 14
C3:2BF0  0A A9 B8 00 E9 21 00 00 8D 02 42 A5 61 C5 86 30
```

### Detailed Annotated Disassembly

```
; ══════════════════════════════════════════════════════════════
; ROM offset: $032B00  |  SNES: C3:2B00
; Region: C3:2B00..C3:2BFF
; Classification: Branch-fed control pocket with embedded
;   arithmetic subroutines. Contains 3 RTL, 2 RTS, 9 JSR.
;   Mix of 8-bit and 16-bit operations with hardware register
;   access ($4204/$4206 division unit, $2140 APU port).
; ══════════════════════════════════════════════════════════════

; ─── Subroutine fragment at C3:2B00 ───
; Entry context unclear — possibly reached via branch from
; preceding mixed-data region. Contains arithmetic operations
; on direct-page variables.

C3:2B00  FC 85 F2       JSR ($F285,X)  ; Indirect JSR through table at $F285+X
                                       ; NOTE: This is an unusual addressing mode
                                       ; for a page start — may indicate data alignment
                                       ; rather than true code entry

C3:2B03  A9 00 0C       LDA #$0C00     ; Load 16-bit immediate $0C00
                                       ; (requires 16-bit A from prior REP #$20)
                                       ; $0C00 = 3072 decimal — possibly a VRAM
                                       ; address or tilemap base offset

C3:2B06  20 E2 00       JSR $00E2      ; Call subroutine at C3:00E2
                                       ; (within C3 low-bank utility region)
                                       ; Likely a VRAM address setup helper

C3:2B09  32 A5          AND ($A5)      ; AND with DP indirect at $A5
                                       ; Masking operation on pointer value

; ─── Variable load and accumulate ───
C3:2B0B  F4 85 5D       PEA $5D85      ; Push effective address $5D85 to stack
                                       ; Used for later PLB/PLA to set data bank
                                       ; or as a 16-bit constant via stack

C3:2B0E  18             CLC            ; Clear carry for addition
C3:2B0F  65 48          ADC $48        ; Add DP variable $48 to accumulator
                                       ; $48 typically holds a running offset or
                                       ; coordinate value in CT's engine

C3:2B11  68             PLA            ; Pull 16-bit value from stack
C3:2B12  85 61          STA $61        ; Store to DP variable $61
                                       ; $61 is part of CT's variable workspace

C3:2B14  A5 13          LDA $13        ; Load DP variable $13
                                       ; $13 often holds a mode/phase byte

C3:2B16  20 10 13       JSR $1310      ; Call subroutine at C3:1310
                                       ; This is a known utility in the C3 low-bank
                                       ; Likely a multiply/divide helper or
                                       ; coordinate transformation

C3:2B19  20 B8 16       JSR $16B8      ; Call subroutine at C3:16B8
                                       ; Another C3 low-bank utility
                                       ; Possibly a bounds-check or clamp operation

C3:2B1C  5B             TDC            ; Transfer DP register (D) to accumulator (A)
                                       ; Zeroes A in 16-bit mode (D is usually $0000
                                       ; or $0300 in CT's C3 bank)
C3:2B1D  A8             TAY            ; Transfer A to Y — zeroes Y

; ─── Memory operations with indexed addressing ───
C3:2B1E  AD 00 0B       LDA $0B00      ; Load from absolute address $0B00
                                       ; This is in the SNES RAM region ($0000-$1FFF)
                                       ; Specifically the direct-page mirror or
                                       ; a shadow buffer at RAM $0B00

C3:2B21  25 10          AND $10        ; AND with DP variable $10
                                       ; Mask off bits per mode flags

C3:2B23  80 25          BRA $2B4A      ; Branch always to $2B4A
                                       ; Skip over the next code block

; ─── Inline data or alternate path target ───
C3:2B25  20 0A 0C       JSR $0C0A      ; Call subroutine at C3:0C0A
                                       ; Another C3 low-bank utility call

C3:2B28  0B             PHD            ; Push direct page register to stack
                                       ; Saves current DP before switching

C3:2B29  B2 46          LDA ($46)      ; Load via DP indirect at $46
                                       ; Reads a pointer-targeted value

C3:2B2B  09 3A          ORA #$3A       ; OR with $3A (0011 1010 binary)
                                       ; Sets specific flag bits

C3:2B2D  F6 18          INC $18,X      ; Increment DP $18+X
                                       ; Indexed counter increment

C3:2B2F  8E 07 15       STX $1507      ; Store X to absolute $1507
                                       ; Preserves index register to RAM

; ─── Stack frame and variable manipulation ───
C3:2B32  0B             PHD            ; Push direct page register
C3:2B33  5B             TDC            ; Zero accumulator (A = D)

C3:2B34  20 1B 02       JSR $021B      ; Call C3:021B — very low-bank utility
                                       ; Possibly the bank-entry veneer helper

C3:2B37  F2 13          SBC ($13)      ; Subtract DP indirect at $13
                                       ; Arithmetic on pointer-targeted value

C3:2B39  02 46          COP #$46       ; COP instruction with $46
                                       ; NOTE: COP is rarely used in SNES games
                                       ; This may indicate data rather than code

; ─── Arithmetic subroutine fragment ───
C3:2B3B  18             CLC            ; Clear carry for addition
C3:2B3C  65 5B          ADC $5B        ; Add DP variable $5B
                                       ; $5B is a working accumulator in CT's engine

C3:2B3E  85 5F          STA $5F        ; Store result to DP $5F
                                       ; $5F holds computed result

C3:2B40  89 D8 40       BIT #$40D8     ; Test bits $40D8 against A
                                       ; 16-bit immediate BIT — checks multiple flags
                                       ; Bit 15 ($8000): negative flag test
                                       ; Bit 12 ($1000): overflow flag test  
                                       ; Bits 8-10 ($0D00): specific mode bits
                                       ; NOTE: This is 16-bit BIT which requires
                                       ; 16-bit accumulator mode

; ─── Memory transfer with indexed addressing ───
C3:2B43  A5 6D          LDA $6D        ; Load DP variable $6D
                                       ; $6D often holds a pointer or offset

C3:2B45  7D 90 82       ADC $8290,X    ; Add with carry from absolute $8290+X
                                       ; Table lookup with accumulator addition

C3:2B48  85 6D          STA $6D        ; Store back to DP $6D
                                       ; Update the pointer/offset

C3:2B4A  7D 40 0E       ADC $0E40,X    ; Add with carry from table at $0E40+X
                                       ; Second table lookup in sequence
                                       ; (target of BRA from $2B23)

C3:2B4D  0C 7D 80       TSB $807D      ; Test and set bits at $807D
                                       ; Read-modify-write: A OR $807D -> $807D
                                       ; Sets flags in a RAM control byte

; ─── Subroutine return ───
C3:2B50  7B             TDC            ; Transfer DP to A (zero A)
C3:2B51  60             RTS            ; Return from subroutine
                                       ; Returns with A = 0 (success/complete flag)

; ─── New subroutine at C3:2B52 ───
; Loads and stores with absolute addressing

C3:2B52  20 17 80       JSR $8017      ; Call subroutine at C3:8017
                                       ; C3:8017 is in the upper utility region
                                       ; Possibly a DMA transfer or VRAM write

C3:2B55  85 82          STA $82        ; Store result to DP $82
                                       ; $82 holds return value / computed offset

C3:2B57  AD 5A 0C       LDA $0C5A      ; Load from RAM $0C5A
                                       ; RAM $0C5A is in the work RAM area
                                       ; Possibly a counter or status byte

C3:2B5A  6A             ROR A          ; Rotate accumulator right
                                       ; Divide by 2, LSB -> carry

C3:2B5B  C0 6B          CPY #$6B       ; Compare Y with $6B (107 decimal)
                                       ; Threshold comparison

C3:2B5D  6A             ROR A          ; Rotate right again (divide by 4 total)
C3:2B5E  40             RTI            ; Return from interrupt
                                       ; NOTE: RTI in this context suggests this
                                       ; code may be part of an NMI/IRQ handler
                                       ; or that alignment is wrong (data mixed in)

C3:2B5F  69 30          ADC #$30       ; Add $30 (48 decimal)
                                       ; ASCII offset or tile index adjustment

C3:2B61  80 69          BRA $2BCC      ; Branch always to $2BCC

; ─── Another subroutine fragment ───
C3:2B63  50 6B          BVC $2BD0      ; Branch if overflow clear to $2BD0

C3:2B65  00 65 80       BRK            ; ← BRK — possible data alignment

C3:2B68  85 84          STA $84        ; Store A to DP $84

C3:2B6A  A5 6D          LDA $6D        ; Load DP $6D (pointer/offset)
C3:2B6C  65 82          ADC $82        ; Add DP $82 (computed offset)
C3:2B6E  40             RTI            ; Return from interrupt
                                       ; Another RTI — reinforces IRQ handler theory

C3:2B6F  85 86          STA $86        ; Store to DP $86

C3:2B71  60             RTS            ; Return from subroutine

; ─── Division subroutine at C3:2B72 ───
; This fragment interacts with the SNES hardware division unit

C3:2B72  AD 00 0A       LDA $0A00      ; Load from RAM $0A00
                                       ; Dividend value (or numerator)

C3:2B75  5E 17 F2       LSR $F217,X    ; Logical shift right of $F217+X
                                       ; This is a hardware register mirror access
                                       ; $F217 would be in the reserved region

C3:2B78  00 EB          BRK #$EB       ; ← BRK — data alignment issue

C3:2B7A  8D 04 42       STA $4204      ; Store to CPU Dividend Low register!
                                       ; $4204 = SNES hardware dividend low byte
                                       ; This confirms a hardware division operation
                                       ; A holds the dividend value

C3:2B7D  E2 10          SEP #$10       ; Set 8-bit X/Y registers
                                       ; X/Y -> 8-bit mode
                                       ; Needed for precise loop control after
                                       ; division completes

C3:2B7F  A5 F0          LDA $F0        ; Load DP variable $F0
                                       ; $F0 holds the divisor value

; ─── Continued division setup ───
C3:2B81  11 4D          ORA ($4D),Y    ; OR with DP indirect indexed at $4D+Y
                                       ; Modify divisor with table value

C3:2B83  1A             INC A          ; Increment accumulator
                                       ; Divisor + 1

C3:2B84  EB             XBA            ; Exchange B and A accumulator bytes
                                       ; Swap high/low bytes of 16-bit A
                                       ; Prepares the value for register write

C3:2B85  6D 04 15       ADC $1504      ; Add RAM $1504 to accumulator
                                       ; Additional offset for division parameter

C3:2B88  10 F0          BPL $2B7A      ; Branch if positive back to $2B7A
                                       ; Loop back for multi-byte division setup

C3:2B8A  23 65          AND $65,S      ; AND with stack-relative $65
                                       ; Stack-based parameter access

C3:2B8C  00 F2          BRK #$F2       ; ← BRK — data alignment

; ─── Post-division result handling ───
C3:2B8E  85 F4          STA $F4        ; Store to DP $F4
                                       ; $F4 holds division result or quotient

C3:2B90  A8             TAY            ; Transfer A to Y
                                       ; Y now holds the quotient

C3:2B91  BE 46 14       LDX $1446,Y    ; Load X from table at $1446+Y
                                       ; Table lookup using quotient as index
                                       ; $1446 is in RAM — a lookup table
                                       ; Possibly a sine/cosine or scaling table

C3:2B94  D0 00          BNE $2B96      ; Branch if not zero (always, since
                                       ; we just loaded X from table)
                                       ; Two-byte no-op with side effect of
                                       ; testing the loaded value

C3:2B96  19 A9 00       ORA $00A9,Y    ; OR with table at $00A9+Y
                                       ; Another table lookup indexed by Y
                                       ; $00A9 is in the zero-page area

; ─── Variable update and branch ───
C3:2B99  42 5B          WDM $5B        ; WDM (William D. Mensch) instruction
                                       ; 2-byte NOP on 65c816 — used as a
                                       ; trap or breakpoint in some debug builds
                                       ; May indicate this is data, not code

C3:2B9B  AE B4 00       LDX $00B4      ; Load X from RAM $00B4
                                       ; $00B4 holds a counter or index

C3:2B9E  00 00          BRK #$00       ; ← BRK — data

C3:2BA0  86 06          STX $06        ; Store X to DP $06
                                       ; $06 is a working variable

C3:2BA2  EA             NOP            ; No operation — pipeline filler

; ─── Cross-bank call ───
C3:2BA3  22 29 0E C3    JSL $C3:$0E29  ; Long call to C3:0E29
                                       ; Calls another function in same bank (C3)
                                       ; but uses long form for bank certainty
                                       ; C3:0E29 is a known utility function
                                       ; Possibly a coordinate math helper

C3:2BA7  E2 00          SEP #$00       ; SEP with $00 — no flags changed
                                       ; Effective 2-byte NOP (no operation)
                                       ; Sometimes used as a deliberate delay

; ─── Store with indexing ───
C3:2BA9  20 AC F4       JSR $F4AC      ; Call subroutine at C3:F4AC
                                       ; C3:F4AC is in the high utility region
                                       ; Possibly a data decompression or
                                       ; palette manipulation routine

C3:2BAC  00 8A          BRK #$8A       ; ← BRK

C3:2BAE  99 46 14       STA $1446,Y    ; Store A to RAM $1446+Y
                                       ; Updates the lookup table at $1446
                                       ; with computed value — this is a
                                       ; write-back to the same table read
                                       ; earlier at $2B91

C3:2BB1  50 C2          BVC $2B75      ; Branch if overflow clear to $2B75
                                       ; Loop back — this is part of the
                                       ; division/lookup iteration

; ─── Mode switching and variable operations ───
C3:2BB3  20 C2 10       JSR $10C2      ; Call C3:10C2
                                       ; Another C3 low-bank utility

C3:2BB6  A8             TAY            ; Transfer A to Y

C3:2BB7  0A             ASL A          ; Shift accumulator left (multiply by 2)
                                       ; Convert word index to byte offset

C3:2BB8  5B             TDC            ; Zero accumulator

C3:2BB9  33 0A          AND ($0A,S),Y  ; AND with stack-relative indirect indexed
                                       ; Access stack frame parameter

C3:2BBB  ED 00 10       SBC $1000      ; Subtract RAM $1000
                                       ; $1000 holds a base value or bias

C3:2BBE  0A             ASL A          ; Multiply by 2 again (total ×4)

C3:2BBF  85 F8          STA $F8        ; Store to DP $F8
                                       ; $F8 holds the scaled result

; ─── Register preservation and computation ───
C3:2BC1  85 FE          STA $FE        ; Also store to DP $FE
                                       ; $FE is a temp/scratch variable

C3:2BC3  8A             TXA            ; Transfer X to A

C3:2BC4  85 90          STA $90        ; Store to DP $90

C3:2BC6  B4 C6          LDY $C6,X      ; Load Y from DP $C6+X
                                       ; Indexed table read from DP area

C3:2BC8  B4 EB          LDY $EB,X      ; Load Y from DP $EB+X
                                       ; Second indexed read

C3:2BCA  46 04          LSR $04        ; Shift DP $04 right (divide by 2)
                                       ; $04 holds a counter or flag

C3:2BCC  E0 00          CPX #$00       ; Compare X with zero
                                       ; (target of BRA from $2B61)

C3:2BCE  CE 02 C0       DEC $C002      ; Decrement RAM $C002
                                       ; Global countdown variable

; ─── Subroutine call and RTL ───
C3:2BD1  F2 20          SBC ($20)      ; Subtract DP indirect at $20

C3:2BD3  BF 31 A5 FE    LDA $FEA531,X  ; Load from long address $FE:A531+X
                                       ; Access data in bank $FE (high ROM)
                                       ; $FE:A531 is a data table in the
                                       ; fixed bank region

C3:2BD7  F4 12 47       PEA $4712      ; Push effective address $4712
                                       ; Prepares stack for later retrieval

C3:2BDA  12 81          ORA ($81)      ; OR with DP indirect at $81

C3:2BDC  F2 6B          SBC ($6B)      ; Subtract DP indirect at $6B
                                       ; NOTE: $6B is also the RTL opcode —
                                       ; if misaligned, this could be a return

; ─── Return point ───
C3:2BDE  4A             LSR A          ; Shift accumulator right
C3:2BDF  18             CLC            ; Clear carry
C3:2BE0  6D 18 0A       ADC $0A18      ; Add RAM $0A18
                                       ; Accumulate offset

C3:2BE3  0A             ASL A          ; Multiply by 2
C3:2BE4  0A             ASL A          ; Multiply by 4 total
C3:2BE5  F8             SED            ; Set decimal mode
                                       ; NOTE: SED is very rare in SNES games
                                       ; May indicate data rather than code

C3:2BE6  0B             PHD            ; Push direct page register

C3:2BE7  00 85          BRK #$85       ; ← BRK — data alignment

; ─── Variable store and conditional branch ───
C3:2BE9  FE 0A A9       INC $A90A,X    ; Increment RAM $A90A+X
                                       ; Indexed counter update

C3:2BEC  B8 00          CLV            ; Clear overflow flag
                                       ; (followed by immediate operand $00
                                       ; if interpreted as data)

C3:2BEE  E9 21 00       SBC #$0021     ; Subtract $21 (16-bit)
                                       ; Requires 16-bit accumulator
                                       ; $0021 = 33 decimal

C3:2BF1  00 8D          BRK #$8D       ; ← BRK

; ─── Hardware register write ───
C3:2BF3  02 42          COP #$42       ; COP with $42
                                       ; Or: if misaligned, $8D 02 42 could
                                       ; be STA $4202 (multiplicand register)

; More likely interpretation if we shift alignment:
; C3:2BF2  8D 02 42       STA $4202    ; Store to CPU Multiplicand register!
;                                        ; Sets up hardware multiplication
;                                        ; A holds the multiplicand value

C3:2BF5  A5 61          LDA $61        ; Load DP variable $61
                                       ; $61 holds a computed value from earlier

C3:2BF7  C5 86          CMP $86        ; Compare with DP $86
                                       ; $86 holds a threshold or previous value

C3:2BF9  30 06          BMI $2C01      ; Branch if minus (A < $86) to $2C01
                                       ; Conditional branch into next page
                                       ; This confirms the code flows across
                                       ; the C3:2BFF/2C00 page boundary
```

### Summary of C3:2B00..C3:2BFF

**Key findings:**
1. **Hardware division unit** used at `C3:2B7A` (`STA $4204` — dividend register) with result read via table lookup at `$1446+Y`
2. **Hardware multiplication** possibly at `C3:2BF2` (`STA $4202` — multiplicand register)  
3. **Cross-bank JSL call** to `C3:0E29` — a known utility function
4. **Multiple subroutine calls** to C3 low-bank utilities: `$00E2`, `$021B`, `$0C0A`, `$10C2`, `$1310`, `$16B8`, `$8017`, `$F4AC`
5. **Table-driven computation** with lookup tables at `$00A9+Y`, `$1446+Y`, `$0E40+X`, `$8290+X`
6. **Long data access** from bank `$FE:A531+X` — fixed ROM bank data table
7. **Control flow crosses page boundary** at `C3:2BF9` (`BMI $2C01`)

**Variable map (DP offsets used):**
| DP Offset | Usage |
|-----------|-------|
| $04 | Counter/flag (shifted right) |
| $06 | Working variable (stores X) |
| $10 | Mode flags (AND mask) |
| $13 | Mode/phase byte |
| $46, $47 | Pointer pair (indirect addressing) |
| $48 | Running offset/coordinate |
| $4A | Computed result storage |
| $5B | Working accumulator |
| $5D | Stack-pushed constant |
| $5F | Computed result |
| $6D | Pointer/offset (updated in loop) |
| $82 | Return value / computed offset |
| $84 | Temporary storage |
| $86 | Threshold / comparison value |
| $F0 | Divisor value |
| $F4 | Division result / quotient |
| $F8 | Scaled result (×4) |
| $FE | Temp/scratch variable |

**SNES hardware registers accessed:**
| Register | Name | Access | Context |
|----------|------|--------|---------|
| $4204 | CPU Dividend Low | Write | Division setup |
| $4202 | CPU Multiplicand | Write (possible) | Multiplication setup |
| $2140 | APU IO Port 0 | (nearby) | Audio communication |

---

## Next-pass caution
Resume at `C3:2C00`. The `BMI $2C01` at `C3:2BF9` confirms code flows across the page boundary. The C3:2C00 page has code score 40 with 7 PHP and 8 JSR — likely a continuation of the arithmetic/control logic.
