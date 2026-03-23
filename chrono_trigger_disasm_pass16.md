# Chrono Trigger (USA) — Disassembly Pass 16

## What this pass focused on

This round followed the **consumer side** of the active-region bucket lists found in the previous pass.

The main target was:

- `C0:B2A0`

with the goal of answering:

- what the `0E00/0E81` bucket traversal is actually used for
- whether the movement rebucketing feeds rendering, collision, updates, or some mix
- what kind of output buffers the traversal writes into

---

## Biggest conclusion

## The bucket lists feed the **sprite/OAM shadow builder**

This is the clean architectural answer.

The movement/update system does not rebucket active slots just for generic bookkeeping.
The downstream walk at `C0:B2A0` consumes:

- `0E00[bucket]` as the bucket head table
- `0E81,X` as the linked-list next pointer

and uses that traversal to emit per-slot sprite data into a set of WRAM buffers that strongly match an **OAM shadow layout**.

That means the current model is now:

1. slot VM updates movement/state
2. movement code rebuckets active slots into camera-relative spatial buckets
3. render-side code walks those buckets in bucket order
4. per-slot render logic writes sprite entries into OAM-shadow-style buffers
5. leftover entries are hidden with `Y = $E0`

So the bucket system is not vague anymore.
It is directly part of the **object rendering pipeline**.

---

## `C0:B2A0` walks 64 bucket heads, then follows `0E81` next-links

### Core structure
The routine begins:

- `LDX #$08A0`
- `STX $DD`
- `LDY #$007E`

Then it loops:

- `LDA $0E00,Y`
- if head is valid, store to `$6D`
- `JSR $B309`
- follow `LDA $0E81,X`
- continue until next-link is negative
- `DEY`
- `DEY`
- repeat until `Y < 0`

### What that means
- `0E00` is being consumed exactly as a **64-entry bucket-head table**
- the lists are traversed through `0E81`
- traversal order is **bucket 0x3F down to 0x00** (because `Y = 0x7E, 0x7C, ..., 0x00`)

This is the missing downstream proof that the `A98A/A9CD` rebucketing work was not dead state.

### New label
- `C0:B2A0  Traverse_SlotBucketsDescending_AndBuildOamShadow`

---

## The output buffers strongly match OAM shadow memory, not generic work RAM

Just before the bucket traversal, the code seeds a group of cursors:

- `$DB = $0770`
- `$DD = $08A0`
- `$DF = $0710`

and earlier:

- `$89 = $0901`
- `$81 = $0907`
- `$85 = $091A`

These addresses live in a tight WRAM window from `$0710` up through `$091A`, which is exactly the kind of packed shadow-buffer arrangement you expect for sprite/OAM staging.

### The smoking gun
After traversal finishes, the routine fills the remaining records with:

- `LDA #$E0`
- `STA $0001,X`
- advance `X` by 4
- repeat

This happens for each remaining record in the cursor ranges.

That is a huge tell: writing **`$E0` into byte 1 of every 4-byte record** is classic sprite-hide behavior, because a sprite with Y near/off-screen is treated as hidden.

So this is not a generic list serializer.
It is building fixed-size 4-byte sprite records and hiding the unused tail.

### Stronger naming upgrades
- `$DB/$DD/$DF` = active low-table write cursors for three OAM-shadow subranges
- `$7B/$7D/$7F` = previous-frame high-water marks used to hide leftover sprite records

I am still keeping the labels conservative because I have not fully solved why the low-table area is partitioned into three write regions, but the broad role is now strong.

### New labels
- `$dp:DB  OamShadowCursor_A`
- `$dp:DD  OamShadowCursor_B`
- `$dp:DF  OamShadowCursor_C`
- `$dp:7B  OamShadowPrevEnd_A`
- `$dp:7D  OamShadowPrevEnd_B`
- `$dp:7F  OamShadowPrevEnd_C`
- `$dp:81  OamShadowHiCursor_A`
- `$dp:85  OamShadowHiCursor_B`
- `$dp:89  OamShadowHiCursor_C`

---

## `C0:B309` is the per-slot OAM emitter

This routine is called once per traversed slot from `B2A0`.

Its first action is:

- `JSR $B701`
- `BCC +1`
- `RTS`

So `B701` acts as a render-prep / eligibility gate.
If it returns carry set, the slot is skipped.
If it returns carry clear, `B309` continues.

Then `B309` checks:

- `LDA $1201,X`
- `AND #$03`

and dispatches to one of **four render-class paths**.

### What this means
- `1201,X` low two bits are a real **render-class selector**
- `B309` is not a generic helper — it is the actual **per-slot sprite/OAM emission dispatcher**

### New labels
- `C0:B309  Emit_CurrentSlotOam_ByRenderClass`
- `$1201,X  SlotRenderClassFlags`

---

## `C0:B701` is a render-prep / visibility gate, not the final emitter

This helper also branches on:

- `LDA $1201,X`
- `AND #$03`

and has four class-specific paths.

Across those paths, it checks `1B00,X`, calls different class-local helpers, and often finishes with:

- `LDA #$80`
- `STA $1B00,X`
- `CLC`
- `RTS`

while skip cases return with carry set.

### Practical read
`B701` appears to be:

- per-class render state preparation
- animation/frame/precondition handling
- visibility / skip gating

before the actual OAM records are emitted by `B309`.

I am not pretending `1B00,X` is fully solved, but it is clearly **render-prep state**, not generic movement state.

### New labels
- `C0:B701  Prepare_CurrentSlotRenderState_ByClass_AndSkipIfHidden`
- `$1B00,X  SlotRenderPrepState`

---

## `B309` pulls from per-slot screen-position and metasprite tables

The class-local emitters inside `B309` use long reads from:

- `7F:4F00`
- `7F:4BC0`

and then write fixed-size sprite records through the OAM-shadow cursors.

### Strong read now
- `7F:4F00` behaves like a **per-slot screen-position / packed sprite placement table**
- `7F:4BC0` behaves like a **metasprite template / frame data area**

I am still leaving the labels generic because I have not yet solved the exact record layouts for every class, but these are clearly render data sources, not physics tables.

### New labels
- `$7F:4F00  SlotScreenSpritePlacementTable`
- `$7F:4BC0  MetaspriteTemplateTable`

---

## Why the spatial bucket result matters

This is the practical engine picture now:

### Earlier passes already established
- movement updates coarse camera-relative bucket state in `0A80`
- active slots are inserted/removed from linked buckets via `A98A/A9CD`

### This pass adds the missing consumer
- render traversal walks those buckets in descending order
- each traversed slot emits sprite data into OAM-shadow-style buffers

So the bucket lists are doing real work for **render ordering / render traversal**, not just culling.

That does not rule out additional consumers, but it **does** prove rendering is one of the main reasons the structure exists.

---

## What is now substantially stronger

### Strong now
- `B2A0` = descending traversal of the slot bucket lists
- `B2A0` writes into OAM-shadow-style buffers
- leftover sprite records are explicitly hidden with byte-1 = `$E0`
- `B309` = per-slot OAM emission dispatcher
- `B701` = render-prep / skip gate
- `1201 & 3` = render class selector
- `1B00` = render-prep state byte
- `7F:4F00` and `7F:4BC0` are render-data sources, not movement data

### Still not fully solved
- exact record layout of each render class
- why the low-table output is partitioned into three cursor regions
- exact bit meaning of `1201` beyond the low two render-class bits
- full field map for the `7F:4F00` and `7F:4BC0` records

---

## Best next target

The cleanest next step is to decode the four `B309` render-class branches in detail.

That should answer:

- how many sprite/OAM records each class emits
- what each record layout is
- whether the three cursor regions correspond to sprite size, priority band, or object category
