# Chrono Trigger Disassembly Pass 56

## Scope of this pass
This pass continued from pass 55's live seam:

- identify the **direct producer path** for the tail/runtime-slot occupant assignments
- decide whether the tail-side bytes:
  - `AF02..AF09`
  - `AF0D..AF14`
  - `AF15.bit7`
  - `AEC6`
  should now be upgraded from loose runtime-tail wording into stronger slot-ownership nouns
- re-check how this producer lines up with the already-solved consumers:
  - group-2 opcode `0x10` (`C1:9E78`)
  - the `C1:C1DD` type-`3` gating noted in pass 35
- decide whether the 11-slot occupant model from pass 55 can now be frozen across **both head and tail partitions**, not just the visible head

This pass resolves the owner/producer side of the tail half strongly enough to upgrade several labels.

The main result is:

> `AEFF..AF09` and `AF0A..AF14` are now best treated as **two contiguous 11-slot occupant-map families**.
>
> - `AEFF..AF09` = live occupant map
> - `AF0A..AF14` = remembered/canonical occupant map
>
> Pass 55 had already frozen this for the visible head (`0..2`).
> Pass 56 now proves the **tail half (`3..10`) is built the same way**, through the canonical producer at `FD:B2A3..B2D3`.

That is materially stronger than the pass-55 wording, which still treated the tail producer as unresolved.

---

## Method
1. Re-read the canonical visible-head map builder from pass 55:
   - `FD:B24D..B2A3`
2. Disassemble the immediately following block at:
   - `FD:B2A3..B2D3`
3. Compare its writes against the already-proven array geometry:
   - `AEFF..AF09`
   - `AF0A..AF14`
4. Cross-check the resulting semantics against later consumers:
   - `C1:9E78`
   - `C1:C1DD` type `3`
5. Decide whether `AEC6` and `AF15.bit7` can now be upgraded.

---

## 1. `FD:B2A3..B2D3` is the canonical **tail occupant-map builder**
The first crucial observation is address geometry.

From pass 55:

- `AEFF..AF09` = 11-byte live occupant map
- `AF0A..AF14` = 11-byte remembered/default occupant map

So the tail halves are exactly:

- `AF02..AF09` = live slots `3..10`
- `AF0D..AF14` = remembered/canonical slots `3..10`

The block at `FD:B2A3` writes **precisely those two ranges**.

Relevant bytes:

```text
FD:B2A3  7B
FD:B2A4  8D C6 AE
FD:B2A7  AA
FD:B2A8  A8
FD:B2A9  BD C5 29
FD:B2AC  30 1B
FD:B2AE  BD C4 29
FD:B2B1  99 02 AF
FD:B2B4  99 0D AF
FD:B2B7  BD C6 29
FD:B2BA  10 0D
FD:B2BC  A9 FF
FD:B2BE  99 02 AF
FD:B2C1  B9 15 AF
FD:B2C4  09 80
FD:B2C6  99 15 AF
FD:B2C9  EE C6 AE
FD:B2CC  C8
FD:B2CD  C2 20
FD:B2CF  8A
FD:B2D0  18
FD:B2D1  69 0C 00
FD:B2D4  AA
FD:B2D5  7B
FD:B2D6  E2 20
FD:B2D8  E0 60 00
FD:B2DB  90 CC
FD:B2DD  6B
```

### Strong structural read
This block:

1. clears `AEC6`
2. iterates `X` across a source record family with stride `0x0C`
3. iterates `Y` across exactly 8 tail-slot entries
4. populates:
   - `AF02,Y`
   - `AF0D,Y`
   - `AF15,Y`
   - `AEC6`

That is not incidental scratch.
It is the missing tail-half builder for the same occupant-map system pass 55 already froze on the head side.

---

## 2. `AEC6` is **not** best treated as a live materialized-tail count
Pass 53 cautiously described `AEC6` as a live tail count.
This pass corrects and strengthens that.

The producer starts with:

```text
FD:B2A3  TDC
FD:B2A4  STA $AEC6
```

So the count is reset to zero before the tail build.

Then for each accepted source entry it does:

```text
FD:B2C9  INC $AEC6
FD:B2CC  INY
```

Crucially, this increment happens for every accepted source record, **including** the branch where `AF02` is forced back to `FF` and `AF15.bit7` is set.

So `AEC6` does **not** count only currently live/materialized tail occupants.
It counts the number of **canonical/populated tail entries** built into the tail partition.

### Strongest safe reading
`AEC6` is now best treated as:

> **canonical populated tail-slot count**

Meaning:
- it counts how many tail entries were admitted into the tail half of the occupant-map family
- some of those entries may still be withheld from the live map (`AF02 = FF`)

This is a real upgrade from pass 53.

---

## 3. `AF0D[Y]` is the canonical tail occupant, while `AF02[Y]` is the live/materialized tail occupant
The producer's core copy is:

```text
FD:B2AE  LDA $29C4,X
FD:B2B1  STA $AF02,Y
FD:B2B4  STA $AF0D,Y
```

So both tail arrays begin with the same occupant identity.

Then there is an immediate split:

```text
FD:B2B7  LDA $29C6,X
FD:B2BA  BPL $B2C9
FD:B2BC  LDA #$FF
FD:B2BE  STA $AF02,Y
FD:B2C1  LDA $AF15,Y
FD:B2C4  ORA #$80
FD:B2C6  STA $AF15,Y
```

### What this proves
For accepted tail source records:

- `AF0D[Y]` always keeps the admitted occupant identity
- `AF02[Y]` keeps that identity **only when the secondary gate passes**
- otherwise:
  - `AF02[Y]` is forced to `FF`
  - `AF15.bit7` is set

That means the two arrays are **not** redundant mirrors.
They match the same split pass 55 already proved for the head:

- canonical / remembered slot identity
- live / currently active slot identity

### Strongest safe reading
For tail slots `3..10`:

- `AF0D..AF14` = **canonical / remembered tail occupant map**
- `AF02..AF09` = **live / currently materialized tail occupant map**

This is the tail-side analogue of pass 55's:

- `AF0A..AF14` = remembered/canonical occupant map
- `AEFF..AF09` = live occupant map

The address geometry now lines up perfectly across all 11 slots.

---

## 4. The source record family is an 8-entry, `0x0C`-stride tail-source table rooted at `29C4`
The producer advances `X` by `0x000C` each iteration:

```text
REP #$20
TXA
CLC
ADC #$000C
TAX
...
CPX #$0060
BCC loop
```

So there are exactly:

- `0x60 / 0x0C = 8`

source records in this family.

The relevant header bytes per record are:

- `+0x00` -> `29C4 + record*0x0C`
- `+0x01` -> `29C5 + record*0x0C`
- `+0x02` -> `29C6 + record*0x0C`

with semantics now strong enough to separate structurally:

### `+0x01` (`29C5 + n*0x0C`)
Gate for whether the source record contributes a tail entry at all.

Because:

```text
LDA $29C5,X
BMI skip
```

### `+0x00` (`29C4 + n*0x0C`)
The occupant identity copied into the tail slot maps.

Because:

```text
LDA $29C4,X
STA $AF02,Y
STA $AF0D,Y
```

### `+0x02` (`29C6 + n*0x0C`)
Secondary gate that can withhold the entry from the live tail map while preserving it canonically.

Because negative values trigger:

- `AF02[Y] = FF`
- `AF15.bit7 = 1`

### Conservative naming
I am still keeping the human-facing noun for the `29C4` record family one step cautious.
The shape is now very strong:

> **8 tail-source battler/participant records, 12 bytes each**

but the exact gameplay-facing noun (enemy-side only, reserve-side, extended battler roster, etc.) still wants a bit more caller proof before it should be frozen.

---

## 5. `AF15.bit7` is now strongly a **canonical-but-not-live tail-entry flag**
Before this pass, `AF15.bit7` only had indirect evidence:

- pass 33 showed `C1:9E78` requires it to be clear
- pass 35 showed `C1:C1DD` type `3` sometimes requires it to be set for entries `>= 3`

This pass gives the missing producer-side proof.

The only direct builder-side action here is:

```text
if source_byte_+0x02 is negative:
    AF02[Y] = FF
    AF15[Y] |= 0x80
```

while **leaving `AF0D[Y]` populated**.

So bit 7 is definitely **not** a generic random status bit.
It is tied exactly to the case where:

- the canonical tail occupant exists
- but the live tail occupant slot is withheld/empty

### Strongest safe reading
`AF15.bit7` is now best carried forward as:

> **tail entry present canonically but withheld from the live tail occupant map**

This is stronger than pass 35/53, but still conservative enough to avoid overclaiming whether the gameplay-facing noun is “reserve”, “hidden”, “queued”, or something more specific.

---

## 6. `C1:9E78` is now more specifically a **tail-entry materializer from the canonical tail map**
Pass 33 already proved the acceptance gates for group-2 opcode `0x10`:

- `AF0D[x] != FF`
- `AF02[x] == FF`
- `AF15.bit7` clear

and that the handler then does:

- append `x + 3` into the live selection list
- `AF0D[x] -> AF02[x]`
- `B15B[x] -> AFAE[x]`
- plus several per-slot materialization side effects

This pass sharpens the noun.

Given the canonical producer at `FD:B2A3`, the handler is no longer best described as a generic “eligible runtime slot selector.”
It is more specifically:

> **materialize a live tail slot from the canonical tail occupant map, provided the slot is currently empty and not marked with the bit-7 withheld flag**

That is a real semantic upgrade, and it comes directly from the now-solved producer.

---

## 7. The 11-slot map model is now strong enough to freeze across head and tail together
Pass 55 had already frozen the visible head:

### Head slots `0..2`
- live map: `AEFF..AF01`
- remembered map: `AF0A..AF0C`

built from the visible source at `2980,X`.

This pass now freezes the tail:

### Tail slots `3..10`
- live map: `AF02..AF09`
- remembered map: `AF0D..AF14`

built from the `29C4 + n*0x0C` source family.

### The unified result
This is now the cleanest safe full-model description:

```text
AEFF..AF09  = 11-slot live occupant map
AF0A..AF14  = 11-slot remembered/canonical occupant map

slots 0..2  = visible head partition
slots 3..10 = runtime tail partition
```

That is no longer just a nice-looking address coincidence.
The ROM now proves both halves.

---

## 8. What this changes about pass 53's tail wording
Pass 53 correctly solved the readiness/timer geometry, but it still used somewhat cautious wording for tail live extent.

Pass 56 sharpens that:

- the tail **capacity** is 8
- `AEC6` counts canonical populated tail entries
- `AF0D` is the canonical tail occupant array
- `AF02` is the live/materialized tail occupant array
- `AF15.bit7` marks canonical entries that are withheld from the live map

So the tail partition is not merely “a hidden runtime tail.”
It is a **real canonical-vs-live slot system** parallel to the visible head.

---

## 9. Tightened roles now safe to carry forward

### `7E:AEFF..AF09`
Best current noun:

> **11-slot live battle-slot occupant map**

- slots `0..2` = visible head live occupants
- slots `3..10` = tail live/materialized occupants
- `FF` = unoccupied / not live in this map

### `7E:AF0A..AF14`
Best current noun:

> **11-slot canonical / remembered battle-slot occupant map**

- head half built from the visible source path
- tail half built from the `29C4` source family

### `7E:AEC6`
Best current noun:

> **canonical populated tail-slot count**

not merely “live tail count”.

### `7E:AF15 bit7`
Best current noun:

> **canonical tail entry withheld from live-map flag**

still conservative on the exact gameplay-facing noun.

### `FD:B2A3..B2DD`
Best current noun:

> **build canonical/live tail occupant maps from the 8-entry `29C4` tail-source record family**

This is the main structural promotion of the pass.

---

## 10. What remains open after this pass
This pass closes the direct producer side for the tail occupant maps, but a few edges remain worth keeping cautious:

1. the exact gameplay-facing identity of the 8 source records rooted at `29C4`
   - probably a battler/extended-roster family
   - but I am not freezing “enemy-only” yet without stronger caller proof
2. the exact outward meaning of `AF15.bit7`
   - structurally it is now strong
   - flavor-wise (“reserve”, “hidden”, “not eligible for this mode”, etc.) still needs more proof
3. why `C1:C1DD` type `3` wants `AF15.bit7` for entries `>= 3`
   - this now looks much less arbitrary
   - but the final gameplay-facing interpretation still needs the caller chain above it
4. the downstream helpers that distinguish occupied slots by readiness `0`, `1`, and `>1`
   - still a valid next seam

---

## Net result of pass 56
Pass 55 had already proven the visible head side of the occupant-map model.
Pass 56 closes the biggest remaining ownership gap on the tail side.

The slot system is now much cleaner:

- one contiguous **11-slot live occupant map**
- one contiguous **11-slot canonical/remembered occupant map**
- a visible head built from `2980`
- a tail built from an 8-entry `29C4` source family
- a real producer-side flag (`AF15.bit7`) that means “canonically present, but not live in the current tail map”

That is enough to stop describing the tail as vague “runtime slot noise.”
The ROM now shows it as the second half of the same occupant-map system.
