# Chrono Trigger Disassembly Pass 45

## Scope of this pass
This pass continued directly from pass 44’s live seam:

- identify the **in-place mutators** of the `0B40` tilemap staging buffer
- re-check the true geometry of `0B40` and its `D1` template family
- determine whether the dynamic `0B40` writers are generic patchers or something structurally tied to the
  lane/roster controller from passes 40–44
- only promote labels that are directly justified by the ROM-side control/data flow

This pass stayed on the exact `0B40` seam opened by passes 43–44.
It did **not** pretend to have the final gameplay-facing name of the whole subsystem.

---

## Method
1. Re-traced all local bank-`C1` stores into `0B40` beyond the full-template copy loops.
2. Focused on the only non-copy `STA $0B40,Y` writer at `C1:0943`.
3. Reconstructed the immediate caller at `C1:07FD`.
4. Compared the patcher geometry against:
   - the already-proven `0B40` upload size (`0x0180`)
   - the already-proven ROM template family at `D1:5800 / 5A50 / 5BD0`
   - the pass-43 lane-roster state (`A6D9 / A6DA / A6DB / A6DD`)
5. Preserved earlier results unless the byte-level geometry disproved them.

---

## Starting point from pass 44
Pass 44 had already proved:

- `0B40` is a WRAM staging buffer uploaded by DMA to VRAM `7A00`
- `D1:5800`, `D1:5A50`, and `D1:5BD0` are three `0x0180`-byte template sources copied into `0B40`
- `99E2` is the upload-dirty latch/counter
- the exact **in-place** writers that modify `0B40` before upload were still unresolved
- the template family had been provisionally read as a likely `16x12` word matrix

This pass materially changed that last point.

---

## 1. The `0B40` template family is better understood as **32 words x 6 rows**, not `16x12`
This is the biggest structural correction in the pass.

The strongest evidence comes from the dynamic `0B40` patcher at `C1:0929`.

That routine:
- runs an outer loop exactly **6** times
- after each row, adds **`0x0040` bytes** to the destination offset in `$82`
- writes directly into `STA $0B40,Y`

A `0x40`-byte row stride means:

- `0x40 / 2 = 32` tilemap words per row

And because the whole upload block is still exactly `0x0180` bytes:

- `0x0180 / 0x40 = 6` rows

So the clean structural reading is:

> `0B40` and the `D1:5800 / 5A50 / 5BD0` template family are laid out as a **32-word by 6-row tilemap strip**

This fits the DMA upload size **exactly** and fits the dynamic patcher much better than the old `16x12` reading.

### Correction to pass 44
The pass-44 `16x12` interpretation was a plausible first read from raw size alone, but the proven patcher stride now overrides it.

The safer corrected geometry is:

> **`32 x 6 words`**

not:

> **`16 x 12 words`**

---

## 2. `D1:59FC` is a separate **6-row x 7-word panel-segment template** used only by the dynamic `0B40` patcher
The only non-copy `0B40` patch path in the local controller band is the routine at `C1:0929`.

Its source is a single long ROM table:

- `LDA.l $D1:59FC,X`

No other source table feeds that patch loop.

The table size is also cleanly recoverable from the loop geometry.

### Patcher geometry
- outer rows = `6`
- inner width = either:
  - `0x0E` bytes = **7 words**
  - or `0x0C` bytes = **6 words**
- source is read linearly across rows
- destination advances by one full `0x40`-byte row each outer iteration

When read as six 7-word rows, `D1:59FC` resolves into the exact following structure:

```text
row 0: 00F0 00F1 00F2 00F1 00F2 00F1 00F3
row 1: 00F4 00FC 00FD 03FC 03FD 00FC 00F5
row 2: 00F6 00FE 00FF 03FE 03FF 00FE 00F7
row 3: 00F4 03FC 03FD 00FC 00FD 03FC 00F5
row 4: 00F6 03FE 03FF 00FE 00FF 03FE 00F7
row 5: 00F8 00F9 00FA 00F9 00FA 00F9 00FB
```

That is not generic logic data.
It is a compact **border/interior tile panel segment**.

So this table is now strong enough to keep as its own source artifact:

> `D1:59FC` = **6-row x 7-word panel-segment tile template**

---

## 3. `C1:0929` is a **6-row panel-segment blitter into `0B40`**, with an explicit shared-border merge mode
The routine at `C1:0929` is now structurally clear.

### Proven control shape
It receives:
- destination byte offset in `$82`
- a merge flag in `$84`

It then does:

- set outer row count = `6`
- if `$84 == 0`
  - use width `0x0E` bytes = **7 words**
  - start at source column `0`
- if `$84 != 0`
  - increment source offset by **2 bytes** (skip one word)
  - use width `0x0C` bytes = **6 words**

Then for each of 6 rows:
- read from `D1:59FC,X`
- write into `0B40,Y`
- after row end:
  - destination += `0x0040`
  - source continues linearly into the next row slice

### Why the merge reading is strong
Skipping exactly **one word** at the left edge while shrinking the copied width from **7** words to **6** words is exactly what you do when adjoining panels should **share a border** instead of drawing two borders side-by-side.

So the safest strong reading is:

> `C1:0929` = **blit a 6-row panel segment into `0B40`, optionally omitting its left-edge border to merge with a previous segment**

This is much stronger than “some tile patch loop.”

---

## 4. `C1:07FD` composes a **three-position horizontal panel strip** into `0B40` from the active lane roster
The caller of `0929` is the real payoff of this pass.

At `C1:07FD`, the code checks the three roster markers:

- `A6D9`
- `A6DA`
- `A6DB`

These were already tightened in pass 43 as the local 3-lane active roster.

For each nonnegative/occupied entry, it calls `0929` with a destination offset in `$82`:

### first slot
- if `A6D9 >= 0`
- destination = `0x0000`
- merge flag cleared

### second slot
- if `A6DA >= 0`
- destination =
  - `0x000C` if slot 1 is absent
  - `0x000E` if slot 1 is present
- merge flag set only when slot 1 is present

### third slot
- if `A6DB >= 0`
- destination =
  - `0x0018` if slot 2 is absent
  - `0x001A` if slot 2 is present
- merge flag set only when slot 2 is present

Because the merged form removes exactly one word from the left edge, those offset pairs are not arbitrary:

- `0x0000` = start at word 0
- `0x000C / 0x000E` = start at word 6 or 7
- `0x0018 / 0x001A` = start at word 12 or 13

That is a clean three-position horizontal layout.

### Strong consequence
This is now enough to say:

> `C1:07FD` = **compose a 3-position horizontal panel strip in `0B40` based on which lanes are active in the local roster**

That ties the `0B40` tilemap strip directly to the pass-43 roster controller.
It is no longer just “some generic tilemap staging area.”

It is a tilemap strip that the lane/roster controller actively composites.

---

## 5. The `0B40` buffer is now best understood as a **base strip template plus roster-panel overlays**
Pass 44 had already proved the base-template swaps:

- `D1:5800`
- `D1:5A50`
- `D1:5BD0`

This pass adds the dynamic overlay layer:

- `D1:59FC` panel segment
- composed by `07FD -> 0929`
- using roster state from `A6D9/A6DA/A6DB`

So the practical structure is now:

1. copy one of the **base 32x6 strip templates** into `0B40`
2. patch in one, two, or three **panel segments** depending on roster occupancy
3. mark `99E2`
4. upload the finished strip to VRAM `7A00`

That is a real pipeline, not isolated helper noise.

---

## 6. The exact human-facing identity of the strip is still unresolved, but the layout is no longer vague
I am still **not** forcing a final gameplay/UI name like:

- “battle HUD”
- “menu panel”
- “target ribbon”
- “status strip”

The ROM proof in this pass is structural, not final vocabulary.

What is now strong is:

- the strip is **32x6 words**
- it uses a **three-position horizontal panel layout**
- that layout is driven directly by the **3-lane roster controller**
- adjoining occupied positions share borders through the `0929` merge mode

That is already a meaningful upgrade over the earlier generic “panel/screen tilemap buffer” wording.

---

## 7. The `D1:5800 / 5A50 / 5BD0` variants now look like **alternate base layouts within the same 32x6 strip geometry**
With the corrected 32x6 geometry, the three base templates no longer look like unrelated full-screen layouts.

They are all:
- the same size
- the same row stride
- the same border/fill tile family
- only lightly different at specific fixed word positions

That makes the safest new reading:

> the `5800 / 5A50 / 5BD0` family are **alternate base strip layouts** for the same 32x6 tilemap region

I am still keeping the final mode names open.
But they are now much more obviously members of the **same strip-layout family**, not separate screens.

---

## 8. Negative result: `9F38[x]` still did not get a trustworthy positive producer
I re-checked the `0B40` mutator/controller band for a positive writer into `9F38[x]`.

Nothing in the newly solved `07FD / 0929 / 59FC` layer promoted that label.

So the pass preserves the same stance as passes 43–44:

- clear path = real
- sink/consume path = real
- positive producer = still unresolved

No fake certainty added here.

---

## Net result of pass 45
This pass materially advanced the `0B40` seam in three ways.

### 1. It corrected the strip geometry
`0B40` and the `D1` base-template family are best modeled as:

> **32 words x 6 rows**

### 2. It identified the first real in-place `0B40` mutator
`C1:0929` is now a strong, keepable label as a:

> **6-row panel-segment blitter with shared-border merge mode**

### 3. It tied the mutator directly to the roster controller
`C1:07FD` composes up to three horizontal panel segments into `0B40` from:

- `A6D9`
- `A6DA`
- `A6DB`

That is a real subsystem-level bridge between:

- the pass-43 lane roster controller
- and the pass-44 tilemap upload strip

The abstraction gap moved again.
The next clean seam is now:

1. the **adjacent companion buffers** rebuilt in the same `07FD` band (`0CC0..0E08`, `0E80+`)
2. the **exact caller contexts** that choose between the `5800 / 5A50 / 5BD0` base layouts
3. the still-unresolved **positive writer** for `9F38[x]`
