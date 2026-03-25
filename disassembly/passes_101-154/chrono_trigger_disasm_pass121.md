# Chrono Trigger Disassembly — Pass 121

## Scope

Pass 120 closed the first same-bank `C2` caller/helper seam, but three concrete gaps were still sitting there:

- the broader `A886..AA30` driver family above `A970/AA19`
- the unresolved `B04B` helper path selected from the `AE75` table gate
- the `BF2F..BFFF` table-and-worker family behind the already-frozen `BFD4` dispatch wrapper

This pass stays on those exact gaps and pushes them into concrete table/driver/worker territory instead of leaving them as vague “next seam” notes.

## Starting point

Previous carry-forward anchor from pass 120:

- `C2:A970..AA05` = exact decrement-by-6 fill updater plus WRAM `$2180` stream writer
- `C2:AA19..AA30` = exact `$2180` triplet emitter
- `C2:BEE6..BF2E` = exact settlement row packet loop using `BF2F + 2*71`
- `C2:BFD4..BFFE` = exact selector-indexed indirect dispatch wrapper rooted at jump table `BFFF`

## Biggest closure

The `BFD4` family is no longer just “a wrapper with some unknown workers.”

This pass freezes:

- the exact contiguous word-table extent at `BF2F`
- the exact jump-table extent at `BFFF`
- the first resolved worker cluster behind that table
- the higher driver above `A970` that seeds the `969A` stream template and runs a two-phase counted update loop

That is a real structural step: the surrounding `C2` pocket is turning from isolated helper labels into a connected driver/table/worker family.

---

## 1. `C2:A886..A969` is the exact two-phase `A970` driver with seeded `969A` template copy and preseeded `5CC2/5D42` fills

### Exact body skeleton

```text
C2:A886  JSR $A1B2
C2:A889  LDX #$FBEA
C2:A88C  JSR $8385
C2:A88F  JSR $821E
C2:A892  STZ $5D40
C2:A895  LDX #$5D40
C2:A898  LDY #$5D42
C2:A89B  LDA #$007D
C2:A89E  MVN $7E,$7E
C2:A8A1  JSR $9E76
C2:A8A4  LDA #$969A
C2:A8A7  STA $9694
C2:A8AA  LDA #$9300
C2:A8AD  STA $9696
C2:A8B0  LDA #$0013
C2:A8B3  STA $9698
C2:A8B6  LDX #$AA06
C2:A8B9  LDY #$969A
C2:A8BC  LDA #$0012
C2:A8BF  MVN $7E,$C2
C2:A8C2  LDA #$60FF
C2:A8C5  STA $5CC2
C2:A8C8  LDX #$5CC2
C2:A8CB  LDY #$5CC4
C2:A8CE  LDA #$0015
C2:A8D1  MVN $7E,$7E
C2:A8D4  LDA $0411
C2:A8D7  AND #$FF00
C2:A8DA  LSR A
C2:A8DB  LSR A
C2:A8DC  LSR A
C2:A8DD  PHA
C2:A8DE  LSR A
C2:A8DF  ADC $01,S
C2:A8E1  DEC A
C2:A8E2  AND #$01FF
C2:A8E5  ORA #$6000
C2:A8E8  STA $5D42
C2:A8EB  LDX #$5D42
C2:A8EE  LDY #$5D44
C2:A8F1  LDA #$0015
C2:A8F4  MVN $7E,$7E
C2:A8F7  PLA
C2:A8F8  LDX #$FC45
C2:A8FB  JSR $8385
C2:A8FE  LDX #$FBE3
C2:A901  JSR $8385
C2:A904  STZ $0DAB
C2:A907  STZ $0D24
C2:A90A  DEC $0D9A
C2:A90D  SEP #$20
C2:A90F  LDA #$E5
C2:A911  STA $0D13
C2:A914  LDA #$30
C2:A916  STA $22
C2:A918  LDA #$90
C2:A91A  STA $24
C2:A91C  LDA #$10
C2:A91E  STA $26
C2:A920  LDA $0412
C2:A923  BNE do_mult
C2:A925  LDA #$18
C2:A927  STA $0D25
C2:A92A  BRA loop
do_mult:
C2:A92C  LDA #$08
C2:A92E  STA $4202
C2:A931  LDA $0412
C2:A934  STA $4203
C2:A937  LDA #$06
C2:A939  STA $0DAB
C2:A93C  LDA $4216
C2:A93F  STA $0D25
loop:
C2:A942  JSR $821E
C2:A945  INC $0D9B
C2:A948  LDX #$FC45
C2:A94B  JSR $8385
C2:A94E  JSR $A970
C2:A951  LDA #$E5
C2:A953  STA $0D13
C2:A956  INC $0D24
C2:A959  LDA $0D24
C2:A95C  CMP $0D25
C2:A95F  BCC loop
C2:A961  STZ $0DAB
C2:A964  LDA $0D24
C2:A967  CMP #$18
C2:A969  BCC loop
C2:A96B  PLP
C2:A96C  RTS
```

### Exact behavior now frozen

- runs exact full-span settlement sweep `A1B2`
- fans through exact service selectors `FBEA`, `821E`, `FC45`, and `FBE3`
- clears `5D40` and uses an overlapping same-bank `MVN` to propagate that zero seed forward from `5D42`
- reruns exact three-block dual-page helper `9E76`
- seeds stream-control words:
  - `9694 = 969A`
  - `9696 = 9300`
  - `9698 = 0013`
- copies exact `0x13` bytes from ROM template `C2:AA06..AA18` into WRAM `7E:969A`
- seeds `5CC2 = 60FF` and propagates that fill across the `5CC2` band
- derives a tagged `5D42` seed from the masked high-byte path of `0411`, then propagates that fill across the `5D42` band
- zeroes `0DAB` and `0D24`, then decrements `0D9A`
- enters an exact two-phase counted loop around `A970`:
  - initializes `0D13 = E5`, `22 = 30`, `24 = 90`, `26 = 10`
  - if `0412 == 0`, seeds `0D25 = 18`
  - otherwise computes `0D25 = 8 * 0412` through hardware multiply and seeds `0DAB = 06`
  - each pass runs `821E`, increments `0D9B`, runs selector `FC45`, runs exact updater `A970`, restores `0D13 = E5`, and increments `0D24`
  - first phase continues while `0D24 < 0D25`
  - then the routine clears `0DAB` and continues the same counted update loop until `0D24 == 18`

Strongest safe reading:

> **`C2:A886..A969` is the exact two-phase `A970` driver that seeds the `969A` WRAM stream template, preloads the `5CC2/5D42` fill bands, and then runs a counted update loop with an initial decrement-step phase followed by a zero-step tail phase up to exactly `0x18` iterations.**

---

## 2. `C2:AA06..AA18` is the exact 19-byte ROM seed template copied to `7E:969A`

### Exact bytes

```text
10 FF FF 30 E0 01 30 D0 01 30 D0 01 30 D0 01 10 F0 01 00
```

### Exact behavior now frozen

- `A886..A969` writes `9694 = 969A`, `9696 = 9300`, and `9698 = 0013`
- then performs `MVN $7E,$C2` with:
  - `X = AA06`
  - `Y = 969A`
  - `A = 0012`
- that copies exactly `0x13` bytes from this ROM root into the WRAM block later streamed by `A970..AA05`

Strongest safe reading:

> **`C2:AA06..AA18` is the exact 19-byte ROM seed template copied into `7E:969A` before the `A970` / `$2180` stream-update phase begins.**

---

## 3. `C2:B04B..B0AA` is the exact `0D4D`-gated dual-`EF65` block builder with `0D4E` mid-copy and `FF:B310` tail-table selection

### Exact body skeleton

```text
C2:B04B  PHP
C2:B04C  SEP #$20
C2:B04E  LDA $0D4D
C2:B051  BEQ alt
C2:B053  REP #$20
C2:B055  AND #$00FF
C2:B058  ASL A
C2:B059  TAY
C2:B05A  LDA $7D00,Y
C2:B05D  TAY
C2:B05E  LDA #$CC0B
C2:B061  JSR $EF65
C2:B064  LDA $7D
C2:B066  AND #$00FF
C2:B069  ORA #$002D
C2:B06C  STA $0000,X
C2:B06F  INX
C2:B070  INX
C2:B071  LDY #$0D4E
C2:B074  LDA #$7E11
C2:B077  JSR $F114
C2:B07A  INX
C2:B07B  INX
C2:B07C  PHX
C2:B07D  STZ $0000,X
C2:B080  TXY
C2:B081  INY
C2:B082  INY
C2:B083  LDA #$000F
C2:B086  MVN $7E,$7E
C2:B089  LDA $0D4D
C2:B08C  AND #$00FF
C2:B08F  ASL A
C2:B090  TAX
C2:B091  LDA $FFB310,X
C2:B095  TAY
C2:B096  PLX
C2:B097  LDA #$FF09
C2:B09A  JSR $EF65
C2:B09D  PLP
C2:B09E  RTS
alt:
C2:B09F  LDY #$9B76
C2:B0A2  LDA #$7E
C2:B0A4  XBA
C2:B0A5  LDA #$18
C2:B0A7  PLP
C2:B0A8  JMP $EF65
```

### Exact behavior now frozen

- when `0D4D == 0`, tail-jumps directly into `EF65` with:
  - `Y = 9B76`
  - `A = 7E18`
- otherwise:
  - uses `0D4D * 2` to select a word from table root `7D00`
  - uses that selected word as `Y`
  - runs `EF65` with exact source descriptor `CC0B`
  - writes exact tagged word `(7D & 00FF) | 002D` at the current output pointer in `X`
  - runs `F114` with exact source descriptor `7E11` and `Y = 0D4E`
  - zeroes the next word, then uses an overlapping same-bank `MVN` with `A = 000F` to shift-copy the following `0x10` bytes forward by two bytes in place
  - reuses `0D4D * 2` to select a second source from long-table root `FF:B310`
  - restores `X` and runs `EF65` again with exact source descriptor `FF09`

Strongest safe reading:

> **`C2:B04B..B0AA` is the exact `0D4D`-gated block-builder tail that either emits one fallback `7E:9B76` block through `EF65`, or builds a composed output by combining a selector-chosen `CC` block, the live `0D4E` block, and a selector-chosen `FF:B310` tail block.**

---

## 4. `C2:BF2F..BF3C` is the exact contiguous word-table root consumed by the `BEE6` row loop

### Exact words

```text
E458
E478
E498
BF3D
BF45
BF6D
BF9F
```

### Exact behavior now frozen

- `BEE6..BF2E` indexes this root as `BF2F + 2*71`
- the contiguous table runs from `BF2F` through `BF3C`
- executable code begins immediately afterward at `BF3D`

Strongest safe reading:

> **`C2:BF2F..BF3C` is the exact contiguous word table rooted at `BF2F` for the `BEE6` row-loop family, ending immediately before live worker code begins at `BF3D`.**

---

## 5. `C2:BFFF..C016` is the exact 12-entry jump table behind `BFD4`

### Exact entries

```text
C017
C06E
C038
C04A
C05C
C0A7
C12C
C080
C0E9
C095
C0B9
C0D1
```

### Exact behavior now frozen

- `BFD4` doubles selector `54` and performs `JSR ($BFFF,X)`
- the contiguous jump-table extent is exactly `BFFF..C016`
- the first resolved worker roots are:
  - `C017`
  - `C038`
  - `C04A`
  - `C05C`
  - `C06E`
  - `C080`
  - `C095`
  - `C0A7`
  - `C0B9`
  - `C0D1`
  - `C0E9`
- entry `C12C` remains the first still-open worker target in this table

Strongest safe reading:

> **`C2:BFFF..C016` is the exact 12-entry jump table consumed by the already-frozen `BFD4` selector-indexed indirect dispatch wrapper.**

---

## 6. `C2:C017..C0E8` is the exact negative-gated toggle / selector worker family behind the `BFD4` jump table

### Exact resolved worker roles

#### `C017..C037`
- returns immediately unless `0D1D` is negative
- toggles `0D86 & 1`
- mirrors that result into `0F09`
- emits exact packet:
  - `1E00 = F3`
  - `1E01 = 0D86`
  - `JSL C7:0004`

#### `C038..C049`
- negative-gated toggle/mirror worker:
  - `0D88 ^= 1`
  - mirrors to `0F0B`

#### `C04A..C05B`
- negative-gated toggle/mirror worker:
  - `0D8D ^= 1`
  - mirrors to `0F10`

#### `C05C..C06D`
- negative-gated toggle/mirror worker:
  - `0D8E ^= 1`
  - mirrors to `0F11`

#### `C06E..C07F`
- negative-gated toggle/mirror worker:
  - `0D89 ^= 1`
  - mirrors to `0F0C`

#### `C080..C094`
- negative-gated selector-advance worker:
  - loads `0D8A`
  - adds exact step `0C`
  - stores the result into selector `54`
  - increments `0F0D`
  - sets `68 = 03`

#### `C095..C0A6`
- negative-gated toggle/mirror worker:
  - `0D8F ^= 1`
  - mirrors to `0F12`

#### `C0A7..C0B8`
- negative-gated selector-forcing worker:
  - `54 = 0A`
  - `0417 = 0A`
  - `0F0E = 01`

#### `C0B9..C0D0`
- calls shared helper `C164` with `X = 0D8B`
- when `0D1D & C0 != 0`:
  - forces `54 = 05`
  - forces `0417 = 05`
  - clears `0F0E`

#### `C0D1..C0E8`
- calls shared helper `C164` with `X = 0D90`
- when `0D1D & C0 != 0`:
  - forces `54 = 05`
  - forces `0417 = 05`
  - clears `0F0E`

Strongest safe reading:

> **`C2:C017..C0E8` is the exact negative-gated worker family behind the `BFD4` jump table, owning the resolved `0D86/88/89/8A/8B/8D/8E/8F/90` toggle-or-selector updates and their mirrors into `0F09/0B/0C/0D/0E/10/11/12`.**

---

## 7. `C2:C0E9..C12B` is the exact selector-08 / `0D87` worker with optional `0408 -> 0F00` copy and fixed `C54F` tail

### Exact body behavior now frozen

- always ends through exact helper `C54F`
- if `0D1D` is negative:
  - toggles `0D87 & 1`
  - mirrors that result into `0F0A`
  - if the new value is nonzero:
    - forces `54 = 0F`
    - increments `68`
    - copies exact `0x09` bytes from `0408` to `0F00` via same-bank `MVN`
- if `0D1D` is not negative:
  - requires exact selector `7F == 08`
  - requires `5A & 01 != 0`
  - if `0D87 == 0`, forces `54 = 03` and `0417 = 03`
  - otherwise increments/toggles `0D87 & 1`, mirrors to `0F0A`, and on the nonzero result takes the same `54 = 0F` / `68++` / `0408 -> 0F00` copy path

Strongest safe reading:

> **`C2:C0E9..C12B` is the exact selector-08 dispatch worker around `0D87/0F0A`, with an optional `0408 -> 0F00` same-bank copy, selector forcing through `54`, and a fixed `C54F` tail.**

---

## Caution-strengthened outputs

### `7E:0DAB`

Pass 120 already proved that `A970` consumes `0DAB` as the exact decrement step for the `5D42` band and that `9DAF` accumulates it during the 12-step ramp.

Pass 121 adds one more exact fact:

- `A886..A969` seeds `0DAB = 06` only for the first counted `A970` phase when `0412 != 0`
- then explicitly clears `0DAB` for the second phase up to the exact `0x18`-iteration limit

That is enough to tighten the wording from a generic shared “step word” to a more exact staged decrement step word inside the `A886/A970` driver family.

### `7E:0D24`

Pass 120 only froze `0D24` as the exact 12-step countdown for `9DAF`.

Pass 121 proves that the same word is also reused very differently by `A886..A969`:

- starts at zero
- increments once per `A970` pass
- is compared first against `0D25`
- then compared against exact limit `18`

So the safe reading broadens from “that single countdown” to an exact loop-progress word reused by at least two staged `C2` fill/update drivers.

---

## Strong labels / semantics added this pass

- `C2:A886..C2:A969`
- `C2:AA06..C2:AA18`
- `C2:B04B..C2:B0AA`
- `C2:BF2F..C2:BF3C`
- `C2:BFFF..C2:C016`
- `C2:C017..C2:C0E8`
- `C2:C0E9..C2:C12B`

## Corrections made this pass

- tightened the `BF2F` reading from vague “word table somewhere after the loop” to an exact contiguous table extent ending immediately before live code at `BF3D`
- tightened the `BFD4` reading from “wrapper with unknown workers” to an exact 12-entry jump-table root plus resolved worker cluster
- tightened `0DAB` / `0D24` wording so they are no longer artificially trapped inside only one pass-120 routine

## Still unresolved

- jump-table entry `C2:C12C` and the deeper `C12C..C180` tail family
- exact helper semantics of `C164`, `C511`, and the unresolved `B0AB..` continuation lane
- broader gameplay-facing nouns for the `0D86..0D90` / `0F09..0F12` state family
- broader gameplay-facing noun for the `A886..AA30` stream/template/update family
- stronger noun for live source block `0D4E`

## Next recommended target

1. **`C2:C12C..C180`**
   - finish the last unresolved jump-table worker behind `BFD4`

2. **`C2:B0AB..B1xx`**
   - continue the `B04B` tail lane and see whether `0D4D/0D4E` fold into a bigger sibling builder family

3. **WRAM noun hunt**
   - `7E:0D86..7E:0D90`
   - `7E:0F09..7E:0F12`
   - `7E:0D4E`

4. **broader `A886..AA30` family noun**
   - now that the driver and seed template are exact, the remaining gap is mostly the bigger system-facing name
