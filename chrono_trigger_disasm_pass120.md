# Chrono Trigger Disassembly — Pass 120

## Purpose

Pass 119 corrected the bank-`C2` ownership bug and closed the first caller cluster around `A1B2/A2CE/A321`, but the real next seam stayed same-bank:

- `C2:9DB9..9ED0`
- `C2:A046..A0BA`
- `C2:A886..`
- `C2:B002`
- `C2:BA32`
- `C2:BEEF`

This pass pushes directly into that same-bank seam instead of drifting elsewhere. The main win is that the settlement/search subsystem is no longer just “called” by those ranges; several of them now freeze as exact packet/fill/export/gate helpers around the corrected owner band.

---

## Biggest closure

The bank-`C2` caller seam widened into a real helper family.

The strongest new closures in this pass are:

- `C2:9DAF..9E75` — exact settlement-tail-driven dual-`EF05` materializer with a 12-step signed ramp writer into `5D42..5D58`
- `C2:9E76..9EAF` and `C2:9EB0..9ECC` — exact shared helper pair that repeatedly feeds `EC93` over `61` and `61+0x1000`
- `C2:A051..A0E6` — exact clamped sweep/materializer bootstrap that seeds dual `5D42/5DC2` fills, runs `A1B2` and `A22F`, then exports a masked strip through `A0E7`
- `C2:A970..AA05` — exact decrement-by-6 fill updater plus WRAM `$2180` stream writer for the `5CC2/5D42` family
- `C2:AFED..B044` — exact three-row settlement packet loop with the `B045` word table and `0D5D` gate
- `C2:BA2F..BB19` — exact BA-side compare gate + capped iterative settlement loop + selector packet row builder
- `C2:BEE6..BF2E` — exact settlement row packet loop behind the handoff target `BEEF`
- `C2:BFD4..BFFE` — exact selector-indexed indirect dispatch wrapper that latches `54` into `0417`, runs a jump-table-selected worker, then fans into `C4BC/C3E4/FBE3`

That is a real structural advance: the caller seam is turning into a concrete subsystem family instead of a loose list of same-bank addresses.

---

## 1. `C2:9DAF..9E75` is the exact settlement-tail-driven dual-`EF05` materializer with a 12-step signed ramp writer and mirrored fill finalizer

### Exact body skeleton

```text
C2:9DAF  SEP #$20
C2:9DB1  LDA $54
C2:9DB4  ADC $0413
C2:9DB7  STA $71
C2:9DB9  JSR $8820
C2:9DBC  REP #$30
C2:9DBE  JSR $A216
C2:9DC1  LDA $61
C2:9DC4  ADC #$0084
C2:9DC7  STA $04
C2:9DC9  LDY #$100C
C2:9DCC  JSR $9EB0
C2:9DCF  LDA #$2E00
C2:9DD2  STA $61
C2:9DD4  LDA #$0202
C2:9DD7  STA $5B
C2:9DD9  LDA $26
C2:9DDB  STA $5D
C2:9DDD  LDA #$120C
C2:9DE0  STA $5F
C2:9DE2  JSR $EF05
C2:9DE5  LDA #$3E00
C2:9DE8  STA $61
C2:9DEA  LDA $26
C2:9DEC  STA $5D
C2:9DEE  JSR $EF05
C2:9DF1  LDX #$FBEA
C2:9DF4  JSR $8385
C2:9DF7  LDX #$FC06
C2:9DFA  JSR $8385
C2:9DFD  STZ $0DAB
C2:9E00  LDA #$000C
C2:9E03  STA $0D24
loop:
C2:9E06  LDA $0DAB
C2:9E0A  ADC $0D22
C2:9E0D  STA $0DAB
C2:9E10  LDA $22
C2:9E13  ADC $0D22
C2:9E16  STA $22
C2:9E18  BCS no_pos_adjust
C2:9E1A  INC $0D95
C2:9E1D  INC $0D95
no_pos_adjust:
C2:9E20  DEC $0D95
C2:9E23  LDX $51
fill:
C2:9E25  LDA $22
C2:9E27  STA $5D42,X
C2:9E2A  INX
C2:9E2B  INX
C2:9E2C  CPX #$0018
C2:9E2F  BCC fill
C2:9E31  LDX #$FC45
C2:9E34  JSR $8385
C2:9E37  DEC $0D24
C2:9E3A  BEQ done_ramp
C2:9E3C  JSR $821E
C2:9E3F  BRA loop
done_ramp:
C2:9E41  LDA $26
C2:9E43  EOR #$0600
C2:9E46  STA $5B
C2:9E48  JSR $EF05
C2:9E4B  LDA #$2E00
C2:9E4E  STA $61
C2:9E50  LDA #$0202
C2:9E53  STA $5D
C2:9E55  JSR $EF05
C2:9E58  LDA #$61FF
C2:9E5B  STA $5D42
C2:9E5E  LDX #$5D42
C2:9E61  LDY #$5D44
C2:9E64  LDA #$0015
C2:9E67  MVN $7E,$7E
C2:9E6A  LDX #$FC45
C2:9E6D  JSR $8385
C2:9E70  SEP #$20
C2:9E72  DEC $0D18
C2:9E75  RTS
```

### Exact behavior now frozen

- seeds `71 = 54 + 0413`
- runs exact settlement/search service `C2:8820`
- immediately runs exact gated post-settlement tail `A216`
- computes `04 = 61 + 0x0084` and runs shared helper `9EB0` with `Y = 100C`
- runs exact `EF05` materialization twice:
  - first with `61 = 2E00`, `5B = 0202`, `5D = 26`, `5F = 120C`
  - then with `61 = 3E00`, `5D = 26`
- fans out through exact service selectors `FBEA` and `FC06`
- then performs an exact 12-step ramp loop:
  - `0DAB += 0D22`
  - `22 += 0D22`
  - when that add does **not** carry, the loop gives `0D95` a net `+1`
  - when it **does** carry, the loop gives `0D95` a net `-1`
  - fills words from `5D42 + 51` up to `5D58` with the current `22`
  - runs exact service selector `FC45`
- after the 12-step loop:
  - flips `5B` with `26 XOR 0600`
  - reruns `EF05`
  - reruns `EF05` again from `61 = 2E00` with `5D = 0202`
  - seeds `5D42 = 61FF` and propagates that fill across `5D42..5D58`
  - runs exact service selector `FC45`
  - decrements `0D18`

Strongest safe reading:

> **`C2:9DAF..9E75` is the exact settlement-tail-driven dual-`EF05` materializer, followed by a 12-step signed ramp writer into `5D42..5D58`, and ending in a mirrored fill/finalizer pass.**

---

## 2. `C2:9E76..9EAF` and `C2:9EB0..9ECC` are the exact shared `EC93` helper pair

### `9E76..9EAF`

- seeds `04 = 2E84`
- masks `0412 -> 02`
- walks exactly three slots with stride `0x0180`
- for each slot calls `9EB0`
- uses `Y = 100C` on the first two slots and `Y = 000C` on the third
- finishes through exact service selector `FBFF`

### `9EB0..9ECC`

- stores incoming `Y -> 06`
- sets `61 = 04`
- runs `EC93` with:
  - `A = Y`
  - `X = 0006`
- then sets `61 = 04 + 1000`
- reruns `EC93` with the same selector value from `06`

Strongest safe reading:

> **`C2:9E76..9EAF` is an exact three-block dual-page `EC93` emitter over `2E84 + n*0x0180`, and `C2:9EB0..9ECC` is its exact shared paired-page submit helper for `61` and `61+0x1000`.**

---

## 3. `C2:A051..A0E6` is the exact clamped sweep/materializer bootstrap with dual `5D` fills and masked strip export

### Exact behavior now frozen

- increments `C9`
- computes `0FC4 = max(85 - 3, 0)`
- clamps `0413` downward to that `0FC4` byte when needed
- clamps `0412` against `73`, storing the chosen value into both `54` and `0412`
- runs exact common service `ED31` with `X = BD74`
- seeds `5D42 = 61FF` and propagates that fill across `5D42..5D58`
- seeds `5DC2 = 61FF` and propagates that fill across `5DC2..5DD8`
- runs exact service selector `FC3E`
- runs `821E`
- then under 8-bit accumulator state runs exact helper `F28D` with:
  - `X = 3390`
  - `Y = 0402`
- runs exact full-span settlement sweep `A1B2`
- runs `821E`
- runs `86DD`
- runs exact one-shot settlement-driven materializer `A22F`
- sets `0D13 = 64`
- increments `0D15`
- copies exact `0x0007` bytes from `FF:CBAC` to `7E:94C8`
- runs exact three-block shared helper `9E76`
- runs exact masked strip exporter `A0E7` with `Y = 9500`

Strongest safe reading:

> **`C2:A051..A0E6` is the exact clamp/bootstrap wrapper that bounds `0412/0413`, seeds dual `5D42/5DC2` fill bands, runs the corrected settlement/materializer chain, then exports a masked strip through `A0E7`.**

---

## 4. `C2:A0E7..A0F6` is the exact masked strip exporter from `9480 + 51`

### Exact body

```text
C2:A0E7  PHP
C2:A0E8  REP #$30
C2:A0EA  LDX $51
loop:
C2:A0EC  LDA $9480,X
C2:A0EF  LSR A
C2:A0F0  AND #$3DEF
C2:A0F3  STA $0000,Y
C2:A0F6  INX
C2:A0F7  INX
C2:A0F8  INY
C2:A0F9  INY
C2:A0FA  CPX #$0030
C2:A0FD  BCC loop
C2:A0FF  PLP
C2:A100  RTS
```

### Exact behavior now frozen

- starts at `X = 51`
- reads words from `9480 + X`
- shifts each right once
- masks with exact word `3DEF`
- streams the result to the caller-supplied destination in `Y`
- advances by exact word stride until `X == 0030`

Strongest safe reading:

> **`C2:A0E7..A0F6` is the exact masked strip exporter that copies a word strip from `9480 + 51`, right-shifts it once, masks by `3DEF`, and streams it to the destination buffer in `Y`.**

---

## 5. `C2:A970..AA05` is the exact decrement-by-6 fill updater and WRAM `$2180` stream writer for the `5CC2/5D42` family

### Exact behavior now frozen

- subtracts `0x0006` from `5CC2`, masks with `01FF`, then re-tags with `6000`
- propagates that updated word across `5CC2..5CD8`
- subtracts exact step word `0DAB` from `5D42`, masks with `01FF`, then re-tags with `6000`
- propagates that updated word across `5D42..5D58`
- sets WRAM stream address via:
  - `$2181 = 969A`
  - `$2183 = 7E`
- advances `22 += 6`
- then moves the trailing bound down by `6` through:
  - `26 -= 6` when `26 != 0`
  - otherwise `24 -= 6`
- performs four exact `$2180` write groups through helper `AA19`, with:
  - `$00 = 01FF`, `A = 10`
  - `$00 = 01E0`, `A = 22`
  - `$00 = 01D0`, `A = C0 - 22`
  - `$00 = 01F0`, `A = 10`
- finishes by writing `00` to `$2180`

Strongest safe reading:

> **`C2:A970..AA05` is the exact decrement-by-6 updater for the `5CC2/5D42` fill family, followed by an exact WRAM `$2180` stream write sequence rooted at `7E:969A`.**

### `C2:AA19..AA30`

This helper is exact enough to freeze too:

- for nonnegative `A`, it writes exact triplet:
  - `A`
  - `$00`
  - `$01`
  to `$2180`
- for negative `A`, it first writes:
  - `(A + 1) & 7F`
  - `$00`
  - `$01`
  and then writes a second exact triplet with leading byte `7F`

Strongest safe reading:

> **`C2:AA19..AA30` is the exact `$2180` triplet emitter used by `A970`, with a split negative-value path.**

---

## 6. `C2:AFED..B044` is the exact three-row settlement packet loop behind the handoff target `B002`

### Exact behavior now frozen

- seeds:
  - `61 = 3580`
  - `7D = 0`
  - `71 = 0`
- repeatedly runs exact settlement/search service `8820`
- exits immediately when `51 != 0`
- otherwise runs exact selector/threshold gate `A1EF`
- runs exact common tail `ED31` with `X = BE0E`
- runs exact helper `F626` from `9A90`
- loads exact word from table `B045 + 2*71` into packet field `180E,Y`
- advances `61 += 0x0140`
- clears packet field `1818,Y`
- writes packet field `1811,Y` as:
  - `00` when `0D5D == 0`
  - `12` when `0D5D != 0`
- increments `71`
- loops while `71 < 73`
- finishes through exact service selector `FBEA`

Strongest safe reading:

> **`C2:AFED..B044` is the exact three-row settlement packet loop using the `B045` word table and the post-threshold gate result in `0D5D`.**

### `C2:B045..B04A`

- exact word table used by `AFED..B044`
- consumed as `B045 + 2*71`
- currently observed entries are the exact first three words used by that loop

---

## 7. `C2:BA2F..BB19` closes the BA-side compare gate, capped iterative settlement loop, and selector packet row builder

### `C2:BA2F..BA4E`

- runs exact selector/threshold gate `A1EF`
- clears `0D5E`
- compares `9A97` against `9890`
- when `9A97 < 9890`, forces `0D5E = 4`
- clears `7E`
- runs exact common service `ED31` with `X = C01F`

Strongest safe reading:

> **`C2:BA2F..BA4E` is the exact BA-side post-compare gate that writes `0D5E` and emits common tail selector `C01F`.**

### `C2:BA4F..BAFB`

- runs exact front helper `F566`
- sets `19D8 = FF`
- clamps local loop-count byte `24 = min(3, 85)`
- clears `25`
- seeds `71 = 041A`
- clears `22` and `7D`
- seeds `61 = 2ECA`
- repeatedly runs exact settlement/search service `8820`
- exits the main loop when `51 != 0`
- on each accepted pass:
  - runs exact selector packet row builder `BAFC` from `9A90`
  - clears `9890`
  - runs exact compare gate `BA2F`
  - advances `61 += 0x0180`
  - increments `71`
  - increments `22`
- continues while `22 < 24`
- then computes the remaining row count `3 - 24`
- for each remaining row:
  - runs exact common service `ED31` with `X = C030`
  - advances `61 += 0x0180`
- finishes with an exact hardware-math finalizer that:
  - writes `09AA` to `$4204`
  - sets `0DDB = 0B`
  - runs `EA81` with `Y = 85`
  - writes `0C` to `$4202`
  - writes `041A` to `$4203`
  - seeds `0D92 = 1278`
  - captures `$4216` into `0D95` and `0D94`

Strongest safe reading:

> **`C2:BA4F..BAFB` is the exact capped iterative settlement loop behind the BA-side caller family, followed by a hardware-math finalizer that seeds `0D92/0D94/0D95/0DDB`.**

### `C2:BAFC..BB19`

- runs exact helper `F626` from the caller-supplied selector in `A`
- writes returned selector byte to packet field `1800,Y`
- clears packet field `1818,Y`
- writes exact constant `1C` to packet field `180F,Y`
- uses exact byte table `BB1A + 22` for packet field `180E,Y`

Strongest safe reading:

> **`C2:BAFC..BB19` is the exact BA-side selector packet row builder used by the capped iterative settlement loop.**

### `C2:BB1A..BB1C`

- exact byte table consumed by `BAFC` as `BB1A + 22`
- current main-loop usage shows the first three entries are the live row-selector bytes for `22 = 0/1/2`

---

## 8. `C2:BEE6..BF2E` is the exact settlement row packet loop behind the handoff target `BEEF`

### Exact behavior now frozen

- repeatedly runs exact settlement/search service `8820`
- exits immediately when `51 != 0`
- otherwise runs exact selector/threshold gate `A1EF`
- runs exact common tail `ED31` with `X = C056`
- runs exact helper `F626` from `9A90`
- loads exact word from table `BF2F + 2*71` into packet field `180E,Y`
- advances `61 += 0x0100`
- compares exact threshold word `0D38,X` against `9A93`
- clears packet field `1818,Y`
- writes packet field `1811,Y` as:
  - `00` when `0D38,X < 9A93`
  - `12` otherwise
- increments `71`
- continues while `71 != 73`

Strongest safe reading:

> **`C2:BEE6..BF2E` is the exact settlement row packet loop behind the handoff target `BEEF`, using the `BF2F` word table and an inline threshold compare against `9A93`.**

---

## 9. `C2:BFD4..BFFE` is the exact selector-indexed indirect dispatch wrapper

### Exact body skeleton

```text
C2:BFD4  PHP
C2:BFD5  SEP #$20
C2:BFD7  TDC
C2:BFD8  LDA $54
C2:BFDA  STA $0417
C2:BFDD  ASL A
C2:BFDE  TAX
C2:BFDF  PHP
C2:BFE0  JSR ($BFFF,X)
C2:BFE3  PLP
C2:BFE4  LDA $0417
C2:BFE7  STA $7F
C2:BFE9  JSR $C4BC
C2:BFEC  JSR $C3E4
C2:BFEF  LDX #$FBE3
C2:BFF2  JSR $8385
C2:BFF5  LDA $0D1D
C2:BFF8  BPL done
C2:BFFA  JSR $EAC2
done:
C2:BFFD  PLP
C2:BFFE  RTS
```

### Exact behavior now frozen

- clears accumulator high byte with `TDC`
- latches selector `54 -> 0417`
- doubles that selector and uses it as exact index into a jump table rooted at `BFFF`
- runs one exact jump-table-selected worker through `JSR ($BFFF,X)`
- restores the latched selector into `7F`
- then runs fixed tail helpers:
  - `C4BC`
  - `C3E4`
  - `8385` with `X = FBE3`
- conditionally runs `EAC2` when `0D1D` is negative

Strongest safe reading:

> **`C2:BFD4..BFFE` is the exact selector-indexed indirect dispatch wrapper that latches `54` into `0417`, runs one jump-table-selected worker, and then fans into `C4BC/C3E4/FBE3` with a sign-gated `EAC2` tail.**

---

## Honest remaining gap

This pass materially advanced the same-bank caller seam, but it did **not** finish the whole `C2` pocket.

The biggest remaining local work is now:

- the broader `A886..AA30` family that still needs a cleaner top-level noun and better worker/table ownership
- the `B04C..B05D` helper/table family behind the `AFED..B044` loop
- the `BF2F..BFFF` table-and-worker family behind `BEE6..BFFE`
- stronger nouns for the newly strengthened WRAM outputs:
  - `0DAB`
  - `0D24`
  - `0D5E`
  - `0FC4`

Those are the real next seams now.
