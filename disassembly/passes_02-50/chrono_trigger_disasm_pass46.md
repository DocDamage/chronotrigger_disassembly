# Chrono Trigger Disassembly Pass 46

## Scope of this pass
This pass continued directly from pass 45’s live seam:

- split the `0B40` strip composer from the adjacent **companion-buffer** builders in the same `C1:07xx..0Axx` band
- determine whether `0CC0..0E08` and `0E80+` are just more tilemap state or structurally different side buffers
- re-check the caller contexts that choose between the three base strip templates:
  - `D1:5800`
  - `D1:5A50`
  - `D1:5BD0`
- correct any routine boundaries that pass 45 had left too broad

This pass stayed on the exact seam opened by pass 45.
It did **not** claim the final gameplay-facing name of the whole subsystem.

---

## Method
1. Re-read the entire local `C1:07A0..0A87` band against pass 45.
2. Distinguished all direct stores into:
   - `0B40`
   - `0CC0..0E08`
   - `0E80+`
3. Recovered the row/column geometry directly from loop counts and row strides.
4. Re-checked all direct `D1:5800 / 5A50 / 5BD0` copy sites and their immediate callers.
5. Only promoted labels justified directly by byte-level control flow.

---

## Starting point from pass 45
Pass 45 had already proved:

- `0B40` is a `32 x 6` word tilemap strip uploaded to VRAM `7A00`
- `D1:5800 / 5A50 / 5BD0` are three base strip templates of the same geometry
- `C1:0929` blits a `6 x 7` panel segment into `0B40`
- `C1:07FD` had been treated as the broad caller/composer for the three-slot panel strip

This pass materially tightened that last point.
The `07xx` band actually contains **two different companion-strip blitters** before the real `0B40` composer begins.

---

## 1. Pass 45’s broad `07FD` boundary was too loose: the real `0B40` composer begins at `C1:081F`
This is the most important correction in the pass.

At `C1:081F`, the routine begins cleanly with:

- `STZ $84`
- occupancy checks of:
  - `A6D9`
  - `A6DA`
  - `A6DB`
- destination selection in `$82`
- repeated `JSR $0929`

That is the exact behavior pass 45 described for the three-slot `0B40` panel-strip composer.

By contrast, the preceding code at `C1:07BD..081D` never writes to `0B40` at all.
It writes to `0CC0+Y` and `0CC1+Y`.

So the safer corrected split is:

- `C1:081F` = actual `0B40` three-slot strip composer
- `C1:07BD..081D` = companion-strip builder logic immediately before it

This does **not** invalidate pass 45’s structural reading of the panel-strip composer.
It just corrects the entry boundary.

---

## 2. `C1:07BD` and `C1:07EE` are two sibling **6-row x 7-byte companion-strip blitters** into `0CC0`, with a constant paired byte of `0x29`
The two loops are structurally parallel.

### `C1:07BD`
The first loop:
- starts with `TDC / TAX`
- sets outer count = `6`
- sets inner count = `7`
- reads source bytes from `CC:FA41,X`
- stores them to `STA $0CC0,Y`
- then stores constant `#$29` to `STA $0CC1,Y`
- advances `Y` by 2 per source byte
- adds `0x0040` bytes to the destination offset after each row

### `C1:07EE`
The second loop is the same shape except the source bytes come from:

- `CC:FA6B,X`

### Structural consequence
These are not tilemap-word copies like the `0B40` path.
They are **byte-pair strip writes**:

- one data byte from ROM
- one constant companion byte `0x29`

across:

- `6` rows
- `7` data positions per row
- row stride `0x40`

So the safest keepable reading is:

> `07BD` and `07EE` are sibling companion-strip blitters that write a narrow `6 x 7` byte pattern into the `0CC0` family, interleaving each source byte with constant `0x29`.

### Strong supporting data
The ROM source tables are compact and visually structured, not arbitrary code:

- `CC:FA41`
- `CC:FA6B`

Both are dominated by `FF` fill plus a small set of recurring tile-like byte values:

- `A0 CD CD E8`
- `B3 BE BC C1`
- `A8 CD BE C6`
- `A2 C8 C6 BB`
- `65 66`
- `EB`

That is exactly the kind of pattern expected from narrow template data, not executable code.

---

## 3. `0CC0..0E08` is not another `0B40`-style tilemap buffer; it is a **narrow paired-byte companion strip** with row stride `0x40`
The strongest proof comes from the write style, not from any guessed consumer.

### Proven facts
Inside the local `07xx..09xx` controller band:

- `07BD` / `07EE` write alternating bytes into `0CC0/Y` and `0CC1/Y`
- `086D` clears a two-column vertical slice using:
  - `STZ $0CC0,X`
  - `STZ $0D00,X`
  - `STZ $0D40,X`
  - `STZ $0D80,X`
  - `STZ $0DC0,X`
  - `STZ $0E00,X`
  - then repeats the same for the `+2` column
- the row stride is again exactly `0x40`

That makes the safest structural reading:

> `0CC0..0E08` is a narrow, row-strided companion strip buffer built from paired bytes, not a `0B40`-style 16-bit tilemap-word field.

### Why this matters
This is the first clean proof that the `0B40` panel strip is rebuilt together with at least one **different-format side buffer**, not alone.

---

## 4. `C1:086D` and `C1:08E8` perform **slice-local updates** inside the `0CC0` companion strip rather than rebuilding the whole thing
After the three-slot `0B40` composer at `081F`, the controller does more than just increment a dirty flag.

### `C1:086D`
This routine:
- uses `95D5`
- multiplies it by `6`
- uses that as an `X` offset into the `0CC0` family
- clears two adjacent columns across six rows

That is not a whole-buffer clear.
It is a **single slice clear** keyed by the current local index.

### `C1:08E8`
This routine then writes back into the same companion-strip family.
Its behavior is mode-sensitive and still not fully named, but several structural facts are now strong:

- it uses selector tables rooted at:
  - `CC:FA23`
  - `CC:FA29`
  - `CC:FADD`
- it writes fixed byte pairs into the `0CC0` / `0D00` band
- constant `0x29` remains the dominant companion byte
- the writes are confined to a small slice rather than the whole `0x180` region

So the safer reading is:

> `086D` and `08E8` are slice-local mutators for the `0CC0` companion strip, keyed by the current local index and several small ROM selector tables.

I am still **not** forcing a human-facing name like “cursor glyphs” or “slot icons” yet.
The structure is real; the final vocabulary is not.

---

## 5. `C1:0958` proves `0E80..0FFF` is a second **full-size companion buffer** rebuilt in the same refresh band
This is the other major result in the pass.

At `C1:0958`, the code:

- saves the current local index from `95D5`
- clears exactly `0x0180` bytes at `0E80+Y`
- then enters a 3-iteration build loop
- each iteration calls `JSR $09B0`

That is enough to say:

> `0E80..0FFF` is a second `0x180`-byte companion buffer rebuilt alongside `0B40`, not an incidental scratch area.

It shares the same overall size as the `0B40` strip region, but it is **not** built as tilemap words.

---

## 6. `C1:09B0` is a **fixed-structure companion-record emitter**, not a tile blitter
The helper at `09B0` is now structurally clear enough to keep.

### Proven behavior
It:
- checks per-entry control bytes in the `C1:1580` 5-byte launch table family
- computes a destination derived from:
  - `0B5E + 11 * index`
- copies exactly `11` bytes from `CC:94A0` using `MVN`
- appends a zero byte terminator
- emits paired bytes into the `0EC6` and `0E86` regions
- uses constant companion byte `0x2D` in those emitted pairs
- appends a fixed suffix sequence into `0EDE..0EF3` including:
  - `A8`
  - `CD`
  - `BE`
  - `C6`

### Why this is strong
That is a **record emitter** or **formatted entry builder**, not a tilemap patcher.

So the safest keepable reading is:

> `C1:09B0` emits a fixed-format companion record from ROM templates rooted at `CC:94A0`, and writes the result into the `0E80+` companion-buffer family.

The exact human-facing meaning of the record is still unresolved.
But the structural distinction from `0B40` is now very clear.

---

## 7. The three base strip templates now have stronger **caller-context roles**, even though the final mode names are still open
Pass 44 and pass 45 proved the geometry and shared family role of:

- `D1:5800`
- `D1:5A50`
- `D1:5BD0`

This pass focused on the copy-site contexts.

### `D1:5800`
This remains the default/template-reset path through:

- `C1:1C3A`

and is called from multiple controller contexts.
That still looks like the **baseline strip restore** path.

### `D1:5A50`
At `C1:0E9F`, the code checks:

- `A86A`

and, when nonzero, copies `D1:5A50` into `0B40`, increments `99E2`, clears `A86A`, and rejoins the common control path.

That makes `5A50` look like:

> a **latched alternate base strip template** selected by a single-shot controller flag.

### `D1:5BD0`
`5BD0` is copied in several later state-advance paths:

- `C1:1306`
- `C1:1593`
- `C1:15B4`

These contexts also do surrounding state updates such as:

- `INC 99E2`
- `STA $95DB = 2`
- `STA $9920 = FF`
- controller-state resets / transition bookkeeping

That makes `5BD0` look like:

> a **transition/reset-oriented alternate base strip template**, not just another static layout variant.

I am still keeping the final gameplay-facing names open.
But the caller contexts are now stronger than in pass 45.

---

## 8. Net result of pass 46
This pass materially advanced the post-pass-45 seam in four ways.

### 1. It corrected the routine boundary
The actual `0B40` three-slot strip composer begins at:

- `C1:081F`

The preceding `07BD..081D` logic belongs to the adjacent companion-strip layer.

### 2. It split out the `0CC0` companion strip as its own real artifact
`0CC0..0E08` is now structurally solved as a:

> **narrow paired-byte companion strip with row stride `0x40`**

fed by:

- `CC:FA41`
- `CC:FA6B`
- plus slice-local mutators at `086D / 08E8`

### 3. It proved `0E80+` is another rebuilt companion buffer, not scratch
`0958 / 09B0` show a full `0x0180`-byte companion-record build path operating alongside the `0B40` strip refresh.

### 4. It tightened the roles of the three `D1` base templates
The family is now best read as:

- `5800` = default/base restore
- `5A50` = latched alternate
- `5BD0` = transition/reset alternate

with the final human-facing mode names still unresolved.

---

## Next clean seam after pass 46
The best continuation target is now:

1. the **actual consumers / upload paths** for:
   - `0CC0..0E08`
   - `0E80..0FFF`
2. the exact semantics of the small selector tables:
   - `CC:FA23`
   - `CC:FA29`
   - `CC:FADD`
3. whether the `0E80+` record builder ultimately feeds text, icon metadata, or another object-format path

That is the cleanest remaining gap in the strip/roster presentation layer.
