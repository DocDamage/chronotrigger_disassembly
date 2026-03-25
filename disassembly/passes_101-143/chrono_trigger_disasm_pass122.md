# Chrono Trigger Disassembly — Pass 122

## Scope

Pass 121 left two honest gaps sitting right next to already-frozen structure:

- the last unresolved `BFD4` jump-table worker lane starting at `C2:C12C`
- the `B0AB..` continuation lane above the already-frozen `B04B` builder tail

This pass stays inside those exact seams and pushes them into concrete worker/helper/preset territory instead of leaving them as hand-wavy “still unresolved” glue.

## Starting point

Carry-forward anchors from pass 121:

- `C2:BFD4..C016` = exact selector-indexed dispatch wrapper with an exact 12-entry jump table
- `C2:C017..C12B` = resolved negative-gated worker family for most of the jump-table lanes
- `C2:B04B..B0AA` = exact `0D4D`-gated composed block-builder tail
- `C2:A886..AA18` = exact two-phase `A970` driver plus exact 19-byte `969A` ROM seed template

## Biggest closure

The `C12C` seam is no longer just “the last unresolved jump-table leg.”

This pass freezes:

- the exact `0F0F/0D8C` worker body at `C2:C12C..C163`
- the shared `C164` helper path that either cyclically adjusts a low-3-bit state byte or falls into a template-stage/mask-select finalizer
- the exact local `C207` mask table consumed by that finalizer
- the first exact `B0AB` continuation-family loader and the multiplier/threshold preset chooser behind it

That is enough to turn both open seams into named, traceable families instead of loose code islands.

---

## 1. `C2:C12C..C163` is the exact `0F0F/0D8C` worker with optional `C164` stage, fixed `C511` call, conditional toggle, and final `0D1F` mirror

### Exact body skeleton

```text
C2:C12C  LDA $0F0F
C2:C12F  BEQ +0F
C2:C131  LDX #$0D8C
C2:C134  JSR $C164
C2:C137  LDX #$0010
C2:C13A  STX $0D47
C2:C13D  JSR $C511
C2:C140  LDA $0D1D
C2:C143  AND #$C0
C2:C145  BEQ done_toggle
C2:C147  LDX #$3B38
C2:C14A  LDA $0F0F
C2:C14D  EOR #$01
C2:C14F  STA $0F0F
C2:C152  BEQ store_word
C2:C154  LDX #$3788
C2:C157  STX $93A4
C2:C15A  JSR $EAC2
done_toggle:
C2:C15D  LDA $0F0F
C2:C160  STA $0D1F
C2:C163  RTS
```

### Exact behavior now frozen

- if `0F0F != 0`:
  - calls shared helper `C164` with `X = 0D8C`
  - seeds exact word `0D47 = 0010`
  - runs fixed helper `C511`
- regardless of that first gate, checks `0D1D & C0`
- when `0D1D & C0 != 0`:
  - toggles exact latch byte `0F0F ^= 01`
  - writes exact word `93A4 = 3B38` when the new `0F0F == 0`
  - writes exact word `93A4 = 3788` when the new `0F0F != 0`
  - runs exact helper `EAC2`
- always mirrors final `0F0F` into `0D1F`

Strongest safe reading:

> **`C2:C12C..C163` is the exact `0F0F/0D8C` dispatch worker behind the last unresolved `BFD4` jump-table leg: it optionally stages `0D8C` through `C164`, seeds `0D47 = 0010`, runs fixed helper `C511`, conditionally toggles `0F0F` under `0D1D & C0`, selects exact word `3788` or `3B38` into `93A4`, and finally mirrors `0F0F -> 0D1F`.**

---

## 2. `C2:C164..C183` is the exact shared low-3-bit cyclic adjust helper over the byte at `X`, keyed by `5A.low2`

### Exact body skeleton

```text
C2:C164  TDC
C2:C165  LDA $0000,X
C2:C168  TAY
C2:C169  LDA $5A
C2:C16B  AND #$03
C2:C16D  BEQ $C184
C2:C16F  AND #$01
C2:C171  BNE +02
C2:C173  DEY
C2:C174  DEY
C2:C175  INY
C2:C176  TYA
C2:C177  AND #$07
C2:C179  STA $0000,X
C2:C17C  JSR $C456
C2:C17F  JSR $EAC2
C2:C182  RTS
```

### Exact behavior now frozen

- reads the byte at exact target `X`
- if `5A.low2 != 0`:
  - uses `5A.bit0` to choose direction
  - net effect is exact `-1` when `5A.bit0 == 0`, exact `+1` when `5A.bit0 == 1`
  - masks the result to exact low-3-bit ring `& 07`
  - stores that adjusted value back through `X`
  - runs exact helpers `C456` and `EAC2`
  - returns
- if `5A.low2 == 0`, falls through into the downstream `C184` stage instead of returning locally

Strongest safe reading:

> **`C2:C164..C183` is the exact shared low-3-bit cyclic adjust helper used by the `0D8B/0D8C/0D90` worker family: when `5A.low2 != 0`, it rotates the byte at `X` by exactly `±1` modulo `8`, then runs `C456` and `EAC2`; when `5A.low2 == 0`, it falls into the downstream template-stage path at `C184`.**

---

## 3. `C2:C184..C206` is the exact template-stage / mask-select finalizer reached from the zero-control `C164` path

### Exact body skeleton

```text
C2:C184  PHP
C2:C185  SEP #$20
C2:C187  LDA $F0
C2:C189  BIT #$01
C2:C18B  BEQ alt_copy
C2:C18D  JSR $EAC2
C2:C190  TDC
C2:C191  LDX #$FCA9
C2:C194  LDY #$0408
C2:C197  LDA #$08
C2:C199  MVN $7E,$C2
C2:C19C  TDC
C2:C19D  LDX #$FCA9
C2:C1A0  LDY #$0F00
C2:C1A3  LDA #$08
C2:C1A5  MVN $7E,$C2
C2:C1A8  JSR $C54F
C2:C1AB  BRA choose_mask
alt_copy:
C2:C1AD  LDA $5A
C2:C1AF  AND #$0C
C2:C1B1  BEQ choose_mask
C2:C1B3  JSR $EAC2
C2:C1B6  TDC
C2:C1B7  LDX #$0F00
C2:C1BA  LDY #$0408
C2:C1BD  LDA #$08
C2:C1BF  MVN $7E,$7E
C2:C1C2  JSR $C54F
choose_mask:
C2:C1C5  SEP #$30
C2:C1C7  LDA $54
C2:C1C9  SEC
C2:C1CA  SBC #$0F
C2:C1CC  TAY
C2:C1CD  LDX $51
scan:
C2:C1CF  LDA.l $C207,X
C2:C1D3  CMP #$FF
C2:C1D5  BEQ final
C2:C1D7  CMP $0F00,Y
C2:C1DA  BNE mismatch
C2:C1DC  INX
C2:C1DD  BRA scan
mismatch:
C2:C1DF  LDA $0D1E
C2:C1E2  CMP #$02
C2:C1E4  BCS final
C2:C1E6  DEC A
C2:C1E7  BEQ use_current
C2:C1E9  INX
C2:C1EA  CPX #$07
C2:C1EC  BCC load_mask
C2:C1EE  LDX #$01
use_current:
C2:C1F0  DEX
C2:C1F1  BPL load_mask
C2:C1F3  LDX #$06
load_mask:
C2:C1F5  LDA.l $C207,X
C2:C1F9  STA $00
C2:C1FB  JSR $C20F
C2:C1FE  JSR $EAC2
final:
C2:C201  PLP
C2:C202  LDX #$FBE3
C2:C205  JMP $8385
```

### Exact behavior now frozen

- if `F0.bit0 != 0`:
  - runs exact helper `EAC2`
  - copies exact `0x09` bytes from ROM template `C2:FCA9` into `0408`
  - copies the same exact `0x09` bytes from ROM template `C2:FCA9` into `0F00`
  - runs fixed helper `C54F`
- otherwise, if `5A & 0C != 0`:
  - runs exact helper `EAC2`
  - copies exact `0x09` bytes from `0F00` into `0408`
  - runs fixed helper `C54F`
- then always enters an exact local mask-selection stage:
  - uses `Y = 54 - 0F`
  - scans exact byte table `C207` against `0F00,Y`
  - stops on mismatch or exact sentinel `FF`
  - if mismatch occurs and `0D1E < 2`, uses a bounded local fallback chooser to move to a neighboring table entry before loading the final mask byte
  - stores the chosen mask byte into direct page `00`
  - runs exact helper `C20F`
  - runs exact helper `EAC2`
  - exits through exact selector `FBE3` via `8385`

Strongest safe reading:

> **`C2:C184..C206` is the exact template-stage / mask-select finalizer reached from the zero-control `C164` path: it conditionally seeds `0408` and `0F00` from exact ROM template `FCA9`, or copies `0F00 -> 0408`, then chooses one mask byte from local table `C207` against `0F00[54-0F]` with a small `0D1E`-bounded fallback, runs `C20F`, reruns `EAC2`, and exits through `FBE3`.**

---

## 4. `C2:C207..C20E` is the exact eight-byte mask-priority table consumed by the `C184` finalizer

### Exact bytes

```text
80 08 40 04 10 20 02 FF
```

### Exact behavior now frozen

- consumed directly by `C184..C206`
- scanned linearly until mismatch or exact sentinel `FF`
- fallback chooser reloads a neighboring entry from this exact same table when `0D1E < 2`

Strongest safe reading:

> **`C2:C207..C20E` is the exact eight-byte local mask-priority table (`80, 08, 40, 04, 10, 20, 02, FF`) consumed by the `C184` template-stage finalizer.**

---

## 5. `C2:B0AB..C2:B106` is the exact `CC`-record preset loader and shift-walk dispatch selector above the post-`B04B` builder lane

### Exact body skeleton

```text
C2:B0AB  PHP
C2:B0AC  SEP #$20
C2:B0AE  LDA $04C9
C2:B0B1  JSR $8881
C2:B0B4  LDX $04CE
C2:B0B7  LDA.l $CC1BB5,X
C2:B0BB  AND #$03
C2:B0BD  ASL
C2:B0BE  ASL
C2:B0BF  STA $0DBD
C2:B0C2  JSR $88D8
C2:B0C5  LDA.l $CC0001,X
C2:B0C9  ORA $0DBD
C2:B0CC  STA $0DBD
C2:B0CF  LDA.l $CC0002,X
C2:B0D3  AND #$0F
C2:B0D5  STA $0DC0
C2:B0D8  CMP #$0F
C2:B0DA  BNE +05
C2:B0DC  LDA #$40
C2:B0DE  STA $0DC0
C2:B0E1  LDA.l $CC0000,X
C2:B0E5  JSR $B0FA
C2:B0E8  JSR ($B0EE,X)
C2:B0EB  PLP
C2:B0EC  RTS

C2:B0FA  LDX $51
scan:
C2:B0FC  ASL A
C2:B0FD  BCS done
C2:B0FF  INX
C2:B100  INX
C2:B101  CPX #$000A
C2:B104  BCC scan
done:
C2:B106  RTS
```

### Exact behavior now frozen

- reads exact selector `04C9` and fans through exact helpers `8881` and `88D8`
- uses exact long-table roots:
  - `CC:1BB5,X`
  - `CC:0001,X`
  - `CC:0002,X`
  - `CC:0000,X`
- builds exact control byte `0DBD` as:
  - `((CC:1BB5,X & 03) << 2) | CC:0001,X`
- builds exact companion control byte `0DC0` as:
  - `CC:0002,X & 0F`
  - with exact remap `0F -> 40`
- passes exact source byte `CC:0000,X` into `B0FA`
- `B0FA` then shift-walks that byte left until the carry sets, advancing `X` by exact two-byte steps starting from exact seed `51`
- resulting `X` is used as the local indirect-dispatch selector for `JSR ($B0EE,X)`

Strongest safe reading:

> **`C2:B0AB..C2:B106` is the exact `CC`-record preset loader and shift-walk dispatch selector above the post-`B04B` builder lane: it derives exact control bytes `0DBD` and `0DC0` from `CC` tables, then uses a carry-seeking shift walk over `CC:0000,X` to choose a same-bank handler through local indirect dispatch.**

---

## 6. `C2:B10D..C2:B17E` is the exact multiplier/threshold bucket chooser that writes preset bytes into `0DBD/0DC0/0DBF`

### Exact body skeleton

```text
C2:B10D  PHP
C2:B10E  SEP #$30
C2:B110  LDA #$64
C2:B112  STA $4202
C2:B116  LDX $0D00
C2:B119  LDA.l $C0FE00,X
C2:B11D  STA $4203
C2:B121  XBA
C2:B122  XBA
C2:B123  NOP
C2:B124  LDA.l $004217
C2:B128  LDX #$00
compare:
C2:B12A  CMP.l $C2B13D,X
C2:B12E  BCC choose
C2:B130  INX
C2:B131  CPX #$03
C2:B133  BCC compare
choose:
C2:B135  TXA
C2:B136  ASL
C2:B137  TAX
C2:B138  JSR ($B141,X)
C2:B13B  PLP
C2:B13C  RTS

C2:B13D  .db 05,14,32,64
C2:B141  .dw B149,B154,B15F,B16F

C2:B149  LDA #$C2 : STA $0DBD : LDA #$40 : STA $0DC0 : RTS
C2:B154  LDA #$82 : STA $0DBD : LDA #$40 : STA $0DC0 : RTS
C2:B15F  LDA #$41 : STA $0DBD : LDA #$03 : STA $0DC0 : LDA #$8A : STA $0DBF : RTS
C2:B16F  LDA #$80 : STA $0DBD : LDA #$01 : STA $0DC0 : LDA #$B2 : STA $0DBF : RTS
```

### Exact behavior now frozen

- writes exact constant `64` into hardware multiplier input `4202`
- multiplies it by exact table byte `C0:FE00[0D00]`
- reads exact result byte from `4217`
- compares that result against exact local threshold table:
  - `05`
  - `14`
  - `32`
  - `64`
- selects one of four exact local preset writers at `B149/B154/B15F/B16F`
- exact preset outcomes are now frozen:
  - case 0 -> `0DBD = C2`, `0DC0 = 40`
  - case 1 -> `0DBD = 82`, `0DC0 = 40`
  - case 2 -> `0DBD = 41`, `0DC0 = 03`, `0DBF = 8A`
  - case 3 -> `0DBD = 80`, `0DC0 = 01`, `0DBF = B2`

Strongest safe reading:

> **`C2:B10D..C2:B17E` is the exact multiplier/threshold bucket chooser reused inside the post-`B04B` lane: it computes `0x64 * C0:FE00[0D00]`, buckets the result against local thresholds `05/14/32/64`, and writes one of four exact control-byte presets into `0DBD/0DC0/0DBF`.**

---

## Honest remaining gap

This pass closes the two biggest structural gaps from pass 121, but a few honest holes remain:

- `C2:B17F..B24A` is now the real continuation of the `B0AB` handler family
- `C2:C20F..` still deserves its own exact helper ownership instead of only being carried as a called finalizer
- broader gameplay-facing nouns are still open for:
  - `0D8B/0D8C/0D90`
  - `0F0F/0D1F`
  - `0DBD/0DC0/0DBF`
  - the overall `A886..AA30` stream/template/update family
