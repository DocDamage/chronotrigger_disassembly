# Chrono Trigger (USA) — Disassembly Pass 41

## Scope
This pass continues directly from pass 40 and stays on the exact seam it identified:

- decode the sink at `C1:16DA..1713`
- classify the emitted fields rooted at `7E:93EE`
- classify the smaller queue rooted at `7E:99D4`
- trace the immediate consumers that prove whether this is one flat blob or multiple coordinated structures

The focus in this pass was the contiguous band around:

- `C1:16DA..1713`
- `C1:1750..1768`
- `C1:1B17..1B3F`
- `C1:8590..85AC`
- `C1:B6D1..B70B`
- `C1:B96A..BA25`
- `CC:FAF0`

This pass does **not** force final gameplay-facing names for the whole subsystem yet.
What is now materially stronger is the structure of the outer sink: it is not one vague “record write.”
It is a **small pending-slot FIFO plus a larger per-record metadata table**, with different consumers proving different fields.

---

## Baseline carried forward from pass 40
Pass 40 had already established:

- `C1:1153` is the outer current-slot controller above service 7
- `C1:1F79` is the common launch initializer
- `C1:129C / 1369 / 1498` are the three real launch families
- `$9615` is a launch-family tag carried into the sink
- `$A62D` is the currently exported/selected result slot from the service-7 result vector
- the ambiguous seam had moved into the sink at `16DA..1713` and the records rooted at `93EE..93F4`

What remained open was whether `93EE..93F4` was:

- one tiny packed struct array,
- one large field array,
- or a mixture of queue state plus per-record state.

---

## What was done in this pass
1. Re-traced the write sequence at `16DA..1713` byte-for-byte
2. Traced every in-bank consumer of `99D4..99D8`
3. Traced every in-bank consumer of `93EE/93EF/93F3/93F4`
4. Traced the bit-setting / bit-clearing helpers around `1750` and `1B17`
5. Verified the role of the lookup table at `CC:FAF0`
6. Tightened which sink fields are strong, which are provisional, and which now have explicit bit meanings

---

## Core results

### 1. `C1:16DA..1713` is **two writesystems back-to-back**, not one flat sink
The write sequence splits cleanly:

```text
AD D8 99       LDA $99D8
AA             TAX
AD D5 95       LDA $95D5
A8             TAY
9D D4 99       STA $99D4,X        ; small queue write
AA             TAX
BF F0 FA CC    LDA $CCFAF0,X      ; map current slot -> record offset
AA             TAX
...
9D EE 93       STA $93EE,X
9D EF 93       STA $93EF,X
9D F0 93       STA $93F0,X
9D F1 93       STA $93F1,X
9D F3 93       STA $93F3,X
9D F4 93       STA $93F4,X
EE D8 99       INC $99D8
```

So the sink does **not** write one homogeneous structure.
It does two distinct things:

1. append the current slot to the small queue at `99D4 + count`
2. project that current slot into a per-record metadata table rooted at `93EE`, using `CC:FAF0[current_slot]` as the record offset

That architectural split is now strong.

---

### 2. `7E:99D4..99D6` plus `7E:99D8` is a **3-entry pending-slot FIFO**, not generic scratch
The queue role is now materially stronger because `16DA` appends into it and `8590` pops/shifts it.

Observed structure at `C1:8590`:

```text
LDA $99D4
BMI fail
LDA $99D4 -> $B18B
LDA $99D5 -> $99D4
LDA $99D6 -> $99D5
LDA #$FF  -> $99D6
DEC $99D8
```

This is a real front-pop plus left-shift.
That proves:

- `99D4..99D6` is a bounded pending queue of slot IDs
- `99D8` is the queue count / append index used by `16DA`
- the queue capacity here is **three visible entries**

This also explains why pass 40’s sink could not be treated as a pure per-record emitter: it is simultaneously maintaining a small pending-slot FIFO.

Safest reading:

> `7E:99D4..99D6` = **pending slot FIFO (3-entry visible window)**
>
> `7E:99D8` = **pending slot count / append index**

---

### 3. `CC:FAF0` is the **slot -> record-offset map** for the larger metadata table at `93EE`
After appending the current slot into the small FIFO, `16DA` immediately remaps the same slot:

```text
LDA $95D5
TAX
LDA $CCFAF0,X
TAX
```

The resulting `X` then indexes the emitted fields at:

- `93EE + X`
- `93EF + X`
- `93F0 + X`
- `93F1 + X`
- `93F3 + X`
- `93F4 + X`

So `CC:FAF0` is not decorative data and not a generic category byte.
It is the concrete translation layer between the current service-7 slot ID and the larger metadata record space rooted at `93EE`.

This also explains why the sink can coexist with the canonical fixed records at:

- `93EE`
- `93F5`
- `93FC`

The table is sparse/mixed enough that the first three canonical records are only part of the total record space.

Safest reading:

> `CC:FAF0` = **slot-to-record-offset lookup map for the emitted metadata table rooted at `93EE`**

---

### 4. `7E:93EE + offset` is the **record status byte**, and bits 6 and 7 now have real meanings
Three separate paths now converge on the same byte.

#### 4a. `16DA` sets bit 6 and clears bit 7
At the sink:

```text
LDA $93EE,X
AND #$7F
ORA #$40
STA $93EE,X
```

So the sink explicitly preserves low bits, clears bit 7, and sets bit 6.

#### 4b. `1750..1768` clears bit 7 when unlinking an already-linked slot
The unlink helper does:

```text
LDA $A6D9,X         ; slot ID from the 3-entry ring
...
LDA $CCFAF0,X
TAX
LDA $93EE,X
AND #$7F
STA $93EE,X
```

So that helper is **only** clearing bit 7.

#### 4c. `1B17..1B2B` sets bit 7 when linking a slot into the 3-entry ring
The matching link helper does:

```text
LDA $A6D9,X
...
LDA $CCFAF0,X
TAX
LDA $93EE,X
ORA #$80
STA $93EE,X
```

So bit 7 is not random. It is the ring-link / active-mark bit paired with the `A6D9` ring.

#### 4d. `B96A..B9B4` consumes and clears bit 6 on the first three canonical records
This logic checks `93EE`, `93F5`, and `93FC` for bit 6, selects one of the three fixed records, then clears the same bit.

That makes bit 6 an explicit pending/consumable state bit, not a cosmetic marker.

Safest reading:

> `7E:93EE + offset` = **record status flags**
>
> bit 6 = **pending/consumable record flag**
>
> bit 7 = **linked/active ring marker tied to `A6D9` membership**

This is one of the strongest results in the pass.

---

### 5. `7E:93EF + offset` carries both **latched aux flags** and a **table-reservation bit**
The sink writes:

```text
LDA $80              ; set to 40h earlier in the flow
ORA $9F38,Y          ; Y = current slot from $95D5
STA $93EF,X
```

So the sink proves two things immediately:

- bit 6 is forced on at emit time (`40h`)
- the low bits come from per-slot byte `9F38[current_slot]`

Then `C1:B6D1` proves the meaning of that forced bit much more tightly:

```text
X = 7 * record_index
LDA $93EF,X
BIT #$40
BEQ done
AND #$BF
STA $93EF,X
LDA $93F4,X -> $0E
scan 5-byte entries at 1580 for entry+0 == $0E
INC entry+3
```

So bit 6 in `93EF` is not the same flag as bit 6 in `93EE`.
It is a **reservation/consumption latch** specifically tied to the table-driven launcher family:

- emit path sets it
- release path clears it
- release path restores one unit to `entry+3` in the 5-byte table when the associated `93F4` token matches

Safest reading:

> `7E:93EF + offset` = **record aux flags with a table-reservation latch in bit 6**

And the source of the low bits is now explicit:

> `7E:9F38[x]` = **per-slot aux-flag byte copied into emitted record field `93EF`**

The exact human-facing meaning of those low bits is still open.
The structural role is no longer open.

---

### 6. `7E:93F4 + offset` is the **latched table-entry auxiliary token** used to restore entry counts
Pass 40 had already shown that the sink writes `$84` into `93F4`, and that `$84` often comes from `$9F35`, which itself comes from `entry + 0` in the 5-byte launch table at `1580`.

This pass closes the loop.
`B6D1` does:

```text
LDA $93F4,X -> $0E
scan 5-byte records at 1580 in steps of 5
CMP entry+0 against $0E
if found: INC entry+3
```

So `93F4` is not just “some aux byte.”
It is the record-side copy of the launch table’s `entry + 0` token, used later to refund/restore the consumable count at `entry + 3`.

Safest reading:

> `7E:93F4 + offset` = **record copy of the 5-byte launch-entry auxiliary token (`entry + 0`)**

This is now a strong carried-forward label.

---

### 7. `7E:93F3 + offset` is a **packed pair of 4-bit dispatch categories**, not a plain scalar
Two different consumers prove the nibble structure.

#### `C1:B580..B62A`
Reads `93F3`, `93FA`, and `9401`, splits low and high nibbles, and compares them against small values (`0`, `1`, `2`, `F`).
That already proves the byte is interpreted as two 4-bit subfields, not one normal 8-bit scalar.

#### `C1:B9C0..BA25`
After choosing one of the three canonical records, the logic computes `7 * record_index`, reads `93F3 + offset`, then separately dispatches on:

- low nibble
- high nibble

by setting `B3E7/B3E8/B3E9` and calling into `FD:A8A5` / `FD:A93C` families.

So the byte is a packed pair of small dispatch category IDs.

Safest reading:

> `7E:93F3 + offset` = **packed low/high 4-bit category pair for downstream dispatch**

The exact gameplay names of the nibble values still need one more pass.
The packed-pair structure is now strong.

---

### 8. `7E:93F0 + offset` and `7E:93F1 + offset` remain one-writer fields, but their emit roles are now firm
These two fields are only written here in bank `C1`:

```text
LDA $9615 -> STA $93F0,X
LDA $A62D -> STA $93F1,X
```

That keeps the same safest readings from pass 40, but the sink split in this pass makes them cleaner.
They belong to the **record metadata table**, not the small FIFO.

So they are now best carried as:

> `7E:93F0 + offset` = **emitted launch-family tag for this record**
>
> `7E:93F1 + offset` = **emitted primary result slot for this record**

Their *consumers* still need a later pass.
Their writer-side semantics are now firm enough to keep.

---

### 9. The first three fixed records at `93EE / 93F5 / 93FC` are a **canonical trio** with special handling
The logic at `B96A..BA25` does not walk the whole sparse record map.
It checks exactly three fixed records:

- `93EE`
- `93F5`
- `93FC`

and picks the first one whose status byte still has bit 6 set.

Then it uses `7 * record_index` to reach the matching `93F3 + offset` byte for that record.

So even though `CC:FAF0` feeds a broader record-offset space, there is a clearly special fixed trio rooted at `93EE`, `93F5`, and `93FC` that downstream logic treats as canonical.

This is why the sink felt inconsistent before this pass: it is feeding a larger record space, but some consumers only care about the first three canonical records.

Safest reading:

> `93EE / 93F5 / 93FC` = **first-status bytes of the three canonical fixed records handled by the `B96A` dispatcher path**

---

## Revised structural picture
The outer layer above service 7 now looks like this:

1. outer controller picks launch family and wrapper opcode
2. service-7 wrappers produce/select a result slot and keep it in `$A62D`
3. `16DA` appends the current slot into the small pending FIFO at `99D4..99D8`
4. `16DA` also emits per-record metadata through the slot->record map at `CC:FAF0`
5. `93EE` status bits track both:
   - pending/consumable state (bit 6)
   - ring-link/active mark (bit 7)
6. `93EF.bit6` tracks a separate table-reservation latch tied to the 5-byte launch-entry pool
7. `93F3` carries two 4-bit downstream dispatch categories
8. `93F4` carries the launch-entry refund token used to restore entry counts later

That is a much tighter and more honest description than the old “mysterious `93EE..93F4` sink.”

---

## Strengthened field interpretations

### `7E:99D4..99D6`
> **pending slot FIFO (3-entry visible window)**

### `7E:99D8`
> **pending slot count / append index**

### `CC:FAF0`
> **slot-to-record-offset lookup map for the emitted metadata table**

### `7E:93EE + offset`
> **record status flags**
>
> bit 6 = pending/consumable record flag
>
> bit 7 = linked/active ring marker

### `7E:93EF + offset`
> **record aux flags with table-reservation latch in bit 6**

### `7E:93F0 + offset`
> **emitted launch-family tag**

### `7E:93F1 + offset`
> **emitted primary result slot**

### `7E:93F3 + offset`
> **packed low/high 4-bit downstream category pair**

### `7E:93F4 + offset`
> **record copy of the 5-byte launch-entry token used for count refund**

### `7E:9F38[x]`
> **per-slot aux-flag byte copied into emitted record field `93EF`**

---

## What remains unresolved after pass 41
1. the exact human-facing meaning of the low bits copied from `9F38[x]` into `93EF`
2. the exact gameplay names of the nibble values packed into `93F3`
3. the true upstream producers of `9F38[x]`
4. the downstream consumers of `93F0` and `93F1` outside the immediate C1 writer band
5. whether the larger sparse record space behind `CC:FAF0` has one uniform stride or a mixed layout beyond the canonical first trio

---

## Best next target
The cleanest next continuation point is now:

- the producers of `9F38[x]`
- the downstream dispatch paths reached from the `93F3` category pairs (`FD:A8A5`, `FD:A93C` families)
- the first consumer outside this band that materially uses `93F0` or `93F1`

That is the seam most likely to convert the current conservative record/queue wording into final gameplay-facing subsystem names.
