# Chrono Trigger Disassembly Pass 53

## Scope of this pass
This pass continued directly from pass 52's live seam:

- resolve the higher-level split between the two seed/export pairs:
  - `B158 / AFAB / B03A`
  - `B15B / AFAE / B03D`
- decide whether they are truly two separate systems, or two partitions of one larger timer/state family
- re-check the seed/init paths at:
  - `C1:80FD..811D`
  - `FD:B4E0..B54D`
  - `FD:B800..B94F`
- tighten the visible vs non-visible split using the export path at the end of `FD:B8F5..B94F`

This pass resolves the biggest remaining structural ambiguity from pass 52.

The main result is simple:

> `B158/B15B`, `AFAB/AFAE`, and `B03A/B03D` are **not** best treated as two unrelated sibling pairs.  
> They are the **head and tail partitions of one contiguous 11-slot battle-readiness/timer family**.

That is a real structural upgrade because it replaces the old “primary vs sibling pair” wording with a single indexed model.

---

## Method
1. Re-read the absolute initialization at `C1:80FD..811D`.
2. Re-read the bulk default writer at `FD:B4E0..B54D`.
3. Re-read the exact loop shapes in `FD:B800..B94F`.
4. Compare those findings against pass 33's selector/finalizer work around `C1:9E78`.
5. Use the final export copy at `FD:B93B..B94F` to decide which partition is directly panel-visible.

---

## 1. The addresses themselves already hint at one contiguous family
The old split from pass 52 was:

- `B158 / AFAB / B03A`
- `B15B / AFAE / B03D`

The crucial structural fact is that these are not arbitrary separate bases:

- `B15B = B158 + 3`
- `AFAE = AFAB + 3`
- `B03D = B03A + 3`

So the “sibling” path is landing exactly 3 bytes after the “primary” path in every case.

That makes the old wording suspicious immediately: it looks like a **head partition of length 3** followed by a **tail partition**, not two disconnected systems.

This pass confirms that suspicion from code.

---

## 2. `C1:80FD..811D` hard-proves the head/tail partition in the work array
The init block at `C1:80FD..811D` does:

```text
A9 01
STA $AFAB
STA $AFAC
STA $AFAD

A9 FF
STA $AFAE
STA $AFAF
STA $AFB0
STA $AFB1
STA $AFB2
STA $AFB3
STA $AFB4
STA $AFB5
```

This is not ambiguous.

### What it proves
The readiness/work family at `AFAB..AFB5` is being initialized as:

- **head partition**: `AFAB..AFAD` = 3 entries, all seeded to `01`
- **tail partition**: `AFAE..AFB5` = 8 entries, all seeded to `FF`

So the old pass-52 interpretation of
- `AFAB` as one family
- `AFAE` as a separate sibling family

is too fragmented.

The stronger structural reading is:

> `AFAB..AFB5` is one contiguous 11-entry work array, with a fixed 3-entry head and an 8-entry tail partition initialized differently.

That is direct ROM proof.

---

## 3. `FD:B4E0..B54D` reinforces the contiguous-array model across 11 entries
The bulk default writer at `FD:B4E0..B54D` runs with:

```text
INX
CPX #$000B
BCC ...
```

so the loop count is **11 entries**.

Inside that loop it repeatedly writes indexed values like:

```text
STA $B158,X
...
```

with `X = 0..10`.

That means the seed family rooted at `B158` is not just a 3-entry head.

It is an **11-entry contiguous indexed array**:

- `B158..B162` = 11 bytes total

This exactly matches the `AFAB..AFB5` layout above.

So the better structural model now is:

- `B158..B162` = seed/base array
- `AFAB..AFB5` = work/current array
- `B03A..B044` = dirty/valid/update array

with a head/tail split of `3 + 8`.

---

## 4. `FD:B800..B8BE` seeds the fixed 3-entry head partition
The first loop in the seed routine is the one already tightened in pass 52.

Key facts:
- it clamps record byte `+0x38` to `0x10`
- it uses the exact pass-52 formula
- it stores to:

```text
STA $B158,X
STA $AFAB,X
STA $B03A,X
```

with `X` driven through the first three entries

and exits when:

```text
CMP #$03
```

lands the loop done.

### Strong reading
This is the **fixed head-partition seeder**:
- indices `0..2`
- direct panel-facing/head readiness slots

This is the branch that pass 50/51/52 were correctly reading as the visible-lane readiness branch.

---

## 5. `FD:B867..B8EC` seeds the tail partition starting exactly 3 bytes later
After the head loop finishes, the routine resets the local index and enters the second loop.

The tail loop:
- gates on `AF0D[x] != FF`
- pulls the participant/record source through the table at `FD:A811`
- reuses the same speed/config formula from pass 52
- conditionally sets `AF15.bit6` from record byte `+0x0A` bit 0
- stores to:

```text
STA $B15B,X
STA $AFAE,X
...
STA $B03D,X    ; only when AF02[x] != FF
```

The important structural point is not just the math.
It is the addressing:

- `B15B,X` = `B158 + (3 + X)`
- `AFAE,X` = `AFAB + (3 + X)`
- `B03D,X` = `B03A + (3 + X)`

So this is not a second unrelated readiness family.
It is the **tail-partition seeder** for the same contiguous arrays.

### Count control
This loop compares its local index against `AEC6`, not a hardcoded 8.

So the best current reading is:

> the tail partition has **capacity 8**, but the actively seeded live extent is controlled by `AEC6`.

That is stronger than pass 52's “sibling visible lane” wording.

---

## 6. Pass 33's `C1:9E78` work now clicks into place
Pass 33 already proved that `C1:9E78` scans 8 runtime entries and, for accepted entries, does:

- `AF0D -> AF02`
- `B15B -> AFAE`
- per-entry side effects / materialization helpers

Under the new pass-53 model, this is no longer a weird sibling special case.

It is exactly what we would expect from the **tail partition** of the readiness family:

- `B15B..B162` = tail-slot seed/base values
- `AFAE..AFB5` = tail-slot working/current values
- selector/finalizer paths can mirror seed -> work when a tail slot is activated/materialized

So pass 33 and pass 52 now reinforce each other instead of sitting as two half-separate stories.

---

## 7. The visible/non-visible split is proven by the export tail at `FD:B93B..B94F`
After the seed logic, the routine ends with an explicit copy:

```text
LDA $AFAB  ; slot 0
STA $99DD
STA $9F22

LDA $AFAC  ; slot 1
STA $99DE
STA $9F23

LDA $AFAD  ; slot 2
STA $99DF
STA $9F24
```

That is hard proof.

### What it proves
Only the **head partition** (`AFAB..AFAD`, slots `0..2`) is copied directly into the visible export buffers:
- `99DD..99DF`
- `9F22..9F24`

The tail partition (`AFAE..AFB5`, slots `3..10`) is **not** copied by this export tail.

So the semantic split is now much tighter:

- **head partition** = directly panel-exported readiness/timer values
- **tail partition** = runtime battle-slot readiness/timer values that participate in selection/materialization logic, but are not directly copied into the 3 visible panel lanes here

This is the cleanest direct answer to pass 52's open question.

---

## 8. Strongest safe structural reading after pass 53

### Unified seed array
`B158..B162`

Best current reading:

> **11-slot battle-readiness seed/base array**
> - head partition: slots `0..2`
> - tail partition: slots `3..10`

### Unified work array
`AFAB..AFB5`

Best current reading:

> **11-slot battle-readiness work/current array**
> - head partition directly feeds visible gauge exports
> - tail partition is runtime-slot facing

### Unified dirty/valid array
`B03A..B044`

Best current reading:

> **11-slot readiness seed/update-valid array**
> - head partition asserted by the head seeder
> - tail partition asserted only under the additional `AF02 != FF` gate

### `AEC6`
Best current reading:

> **live tail-partition count / populated runtime-tail-slot count**

I am still keeping a step of caution on the final gameplay-facing noun, but its role in the tail loop is now much tighter than before.

---

## 9. What this changes from pass 52

### Retired framing
The pass-52 wording of:
- “primary pair”
- “sibling pair”
- “sibling visible lane”

is now too fragmented and slightly misleading.

The code now supports a better model:

> one contiguous 11-slot readiness family with:
> - a fixed 3-entry visible head
> - a variable live tail behind it

### Stronger replacement
The correct structural split is now:

- **head / panel-exported partition**
  - `B158..B15A`
  - `AFAB..AFAD`
  - `B03A..B03C`

- **tail / runtime-slot partition**
  - `B15B..B162`
  - `AFAE..AFB5`
  - `B03D..B044`

That is a real upgrade in certainty.

---

## 10. Open edges after this pass
This pass resolves the structural split, but a few useful follow-ups remain:

1. the exact gameplay-facing identity of the **tail partition**
   - active non-party battlers?
   - extended runtime battlers?
   - materialized enemy-side battlers?
2. the exact meaning of `AF15.bit6` in the tail seeder
3. the exact role of `AEC6` versus the full tail capacity of 8
4. the exact normalization semantics in `FD:B8F5..B93A`
   - it clearly prepares the head export state
   - but the exact minimum/subtractive normalization story still deserves one clean pass

---

## Bottom line
Pass 53 materially upgrades the readiness branch again.

The old split from pass 52:

- `B158 / AFAB / B03A`
- `B15B / AFAE / B03D`

is no longer the best model.

The stronger ROM-backed model is:

> **one contiguous 11-slot readiness/timer family**
> with
> - a **3-slot head partition** directly copied into the visible panel/gauge exports
> - a **tail runtime-slot partition** seeded from the same battle-speed/speed formula and tied into the selector/materializer logic from pass 33

That is real structural progress, not just a rename.
