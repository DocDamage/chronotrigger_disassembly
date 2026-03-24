# Chrono Trigger Disassembly Pass 108

## What this pass focused on

Pass 107 closed `FD:C1EE..C2C0` and proved that it is the exact eight-channel indirect-HDMA installer/finalizer body.

That left the real upstream question inside the paired builder targets behind `FD:C2C1`:

> are those paired targets true mode siblings, true double-buffer siblings, and does any one of them actually own the final `7E:0128` HDMA-enable shadow byte?

This pass closes the paired-builder structure far enough to answer that cleanly.

---

## Main result

The six builder targets behind `FD:C2C1` are now exact enough to say three important things:

1. `0153.bit0` does **not** pick different display modes.
   It picks between two **true WRAM-bundle siblings** that use the same table grammar at addresses separated by `0x2B8`.

2. `0126` is the exact local **3-way table-grammar selector** for this family:
   - `0126 = 0` -> fixed-template builder family
   - `0126 = 1` -> variable/chunked builder family driven by `0127`
   - `0126 = 2` -> alternate variable builder family driven by `0127`

3. none of the six builder bodies directly writes `7E:0128`.
   So the still-open direct producer seam for the HDMA-enable shadow has now moved back **out of this FD builder cluster**.

That is a real closure, not a dodge.

---

## What I did

- decoded the six builder targets behind `FD:C2C1`
- matched each clear-side target to its set-side sibling by exact WRAM write pattern
- checked the family-1 and family-2 zero tests at `0127`
- decoded the `CC58/CC5E/CCB2/CCB8` helper cluster far enough to prove it is emitting chunked HDMA table entries, not mask bytes
- scanned the six builder bodies and their local helper lane for direct `7E:0128` and `$420C` stores

---

## 1. The paired targets are true double-buffer siblings, not mode siblings

The dispatcher already proved the exact paired targets:

- set-side table:   `FD:C2EB / FD:C995 / FD:CFCF`
- clear-side table: `FD:C847 / FD:CD0C / FD:D27E`

Pass 108 proves what those pairs mean.

For every family, the two sides write the **same table grammar** into the same six logical table slots, but with every destination moved by a fixed delta of `0x2B8`:

- first-bundle slot starts:
  - `0F80, 0FD7, 1085, 10DC, 1133, 118A`
- second-bundle slot starts:
  - `1238, 128F, 133D, 1394, 13EB, 1442`

Exact pair deltas:

- `1238 - 0F80 = 0x2B8`
- `128F - 0FD7 = 0x2B8`
- `133D - 1085 = 0x2B8`
- `1394 - 10DC = 0x2B8`
- `13EB - 1133 = 0x2B8`
- `1442 - 118A = 0x2B8`

That same delta pattern holds across:
- family 0 (`C2EB` vs `C847`)
- family 1 (`C995` vs `CD0C`)
- family 2 (`CFCF` vs `D27E`)

So the exact safe reading is:

> `0153.bit0` chooses which of two sibling WRAM HDMA bundles is being rebuilt on this subpass, not which display grammar is in use.

That closes one of the biggest remaining ambiguities from pass 107.

---

## 2. `0126` is the exact local 3-way builder-family selector

The dispatcher body from pass 106 already froze the mechanics:

```asm
FD:C2C1  LDA $53
FD:C2C3  BIT #$01
FD:C2C5  BNE set_side
FD:C2C7  LDA $26
FD:C2C9  ASL
FD:C2CA  TAX
FD:C2CB  JSR (C2E5,X)   ; C847 / CD0C / D27E
...
set_side:
FD:C2D3  LDA $26
FD:C2D5  ASL
FD:C2D6  TAX
FD:C2D7  JSR (C2DF,X)   ; C2EB / C995 / CFCF
```

Pass 108 closes the semantics of those three indices locally:

- `0126 = 0`
  - fixed-template builder family
  - set-side: `FD:C2EB..C3FF`
  - clear-side: `FD:C847..C95B`

- `0126 = 1`
  - variable/chunked builder family using `0127`
  - set-side: `FD:C995..CC57`
  - clear-side: `FD:CD0C..CFCE`

- `0126 = 2`
  - alternate variable builder family using `0127`
  - set-side: `FD:CFCF..D27C`
  - clear-side: `FD:D27E..D52B`

So `0126` no longer needs vague “maybe wider display state” wording to continue this pocket honestly.
At minimum, it is now exact as the local 3-way **table-grammar selector** for this FD-side HDMA builder family.

---

## 3. `0127` is the exact variable-template parameter byte in families 1 and 2

The four variable builders all start with the same gate:

```asm
FD:C995  LDA $0127
FD:C998  BNE +3
FD:C99A  BRL FD:C2EB

FD:CD0C  LDA $0127
FD:CD0F  BNE +3
FD:CD11  BRL FD:C847

FD:CFCF  LDA $0127
FD:CFD2  BNE +3
FD:CFD4  BRL FD:C2EB

FD:D27E  LDA $0127
FD:D281  BNE +3
FD:D283  BRL FD:C847
```

That proves an exact local contract:

- when `0127 == 0`
  - family 1 collapses to family 0 on the same bundle side
  - family 2 also collapses to family 0 on the same bundle side
- when `0127 != 0`
  - families 1 and 2 build their variable templates instead

The rest of those bodies then repeatedly use `0127` in exact arithmetic:

family 1 examples:
- `0x29 - 0127`
- `2 * 0127`
- `0x64 - 0127`
- clamped or chunked counts around `0x0A`
- address/pointer words derived from `0127`

family 2 examples:
- `0x29 - 0127 + 1`
- `2 * 0127`
- `0x29 - 0127 - 1`
- additional fixed spans like `0x58`, `0x64`, `0x1D`
- matching derived pointer/address words

That is enough to freeze the strongest safe local reading:

> `7E:0127` is the variable-template parameter byte used by the `0126 = 1` and `0126 = 2` HDMA-table builders; when zero, both families fall back to the fixed family-0 template.

I am still intentionally not pretending to know the final gameplay/UI noun of `0127` yet.

---

## 4. The `CC58/CC5E/CCB2/CCB8` helper lane is a chunked HDMA-entry emitter

This helper cluster is no longer fuzzy.

### `FD:CC58`
Exact body:

```asm
LDY #$0000
STY $EE
RTS
```

It is a reset/init entry for the local builder offset.

### `FD:CC5E..CCB1`
This helper takes a count in `A` and emits one or more 3-byte entries into the first-bundle variable table lane at `1085+Y`.

Exact behavior:
- if `A < 0x10`
  - store `A | 0x80` as the count/control byte
  - store a pointer word derived from `1D27 + 4 * (EE & 0x0F)`
  - advance `Y` by 3
  - add the original count into `EE`
- if `A >= 0x10`
  - emit `0x90` chunks until the remainder is below `0x10`
  - then emit the remainder path above

### `FD:CCB2`
Exact body:

```asm
CLC
ADC $EE
STA $EE
RTS
```

### `FD:CCB8..CD0B`
This is the clear-side sibling of `CC5E..CCB1`.
It performs the same chunked emission grammar, but writes into the second-bundle lane at `133D+Y` and uses the sibling pointer base.

So this helper lane is conclusively building **HDMA table entries**, not the HDMA-enable mask.

---

## 5. None of the six builder families directly writes `7E:0128`

I checked the six builder families and their helper lane specifically for the direct shadow-byte question.

Static result:
- no `STA $0128` inside
  - no `8D 28 01`
  - no `8F 28 01 00`
- no clean `$420C` commit inside the six builder bodies
- no direct store in the `CC58/CC5E/CCB2/CCB8` helper lane either

The only direct absolute `STA $0128` still standing in static code is the already-known writer at:

```asm
C0:AE33  STA $0128
```

So the honest conclusion is now:

> the paired FD builder families prepare and refresh the WRAM HDMA table bundles, but they do **not** directly own the final `7E:0128` HDMA-enable shadow byte.

That means the pass-107 producer question now closes **negatively** for this cluster.
The direct shadow-byte owner seam has moved back out toward the low-bank owner/update lane, not deeper into these six builder bodies.

---

## 6. Strongest safe reading after pass 108

The grounded reading is now:

- `FD:C2C1` dispatches one of **three exact local HDMA-table grammars** chosen by `0126`
- `0153.bit0` selects which of two **true sibling WRAM bundles** is rebuilt on that subpass
- `0126 = 0` -> fixed template family
- `0126 = 1` -> variable/chunked template family driven by `0127`
- `0126 = 2` -> alternate variable template family driven by `0127`
- `0127 = 0` collapses families 1 and 2 back to family 0 on the same bundle side
- the helper lane at `CC58/CC5E/CCB2/CCB8` emits chunked 3-byte HDMA table entries
- none of these six builder bodies directly writes the final `7E:0128` HDMA-enable shadow byte

So the cluster is no longer “six fuzzy upstream routines.”
It is now an exact local **double-buffered 3-family HDMA table builder system**.

---

## Honest caution

Even after this pass:

- I have **not** frozen the final broader gameplay/UI noun of `0126` or `0127`; only the exact local builder contracts.
- I have **not** frozen the exact broader noun of the `1D27..1D65` / `1DA7..1DE3` pointer-source lanes used by the variable builders.
- I have **not** yet closed the true low-bank owner/update path that finally determines `7E:0128`; this pass proves only that the answer is **not** inside these six FD builder bodies.

---

## Best next move

There are now two clean continuation lanes.

### If the goal is the direct `$420C` / `7E:0128` ownership seam
Move back to the low-bank owner lane around:
- `C0:AE2B..AE33`
- `C0:EC48..ED0D`
- any exact callers/updaters that decide the value mirrored into `7E:0128`

That is now the honest place where the remaining direct shadow-byte producer question lives.

### If the goal is to finish this FD-side dossier first
Stay local and freeze:
- the writer(s) of `7E:0127`
- the broader role of `1DF9` / `1DFD`
- the source-pointer lanes at `1D27..1D65` and `1DA7..1DE3`

But the key thing is now settled:

> the pass-107 “which builder directly owns `0128`?” question no longer belongs inside `FD:C2EB/C847/C995/CD0C/CFCF/D27E`.
