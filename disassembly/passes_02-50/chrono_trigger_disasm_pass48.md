# Chrono Trigger Disassembly Pass 48

## Scope of this pass
This pass continued from pass 47’s seam, but the strongest productive progress came from the **generator side** rather than from forcing a premature final name onto the bank-`C0` consumer.

The goals for this pass were:

- resolve the helper path behind the `9499..949F`, `011F`, `0174`, and `104E` dynamic glyph generation mentioned at the end of pass 47
- determine whether the dynamic groups emitted by `C1:0299` are text-like, icon-like, or numeric
- re-check the bank-`C0` consumer only far enough to strengthen the producer/consumer relationship without inventing a final subsystem label

This pass stayed conservative about the final gameplay-facing name of the whole panel/strip system.

---

## Method
1. Re-read `C1:0299` linearly, especially the three dynamic helper call sites after the fixed 5-glyph lane run.
2. Decoded the local helper routines at:
   - `C1:011F`
   - `C1:0174`
   - `C1:104E`
3. Recovered the live ROM table at `CC:F903` used by those helpers.
4. Re-checked the `C0:A270..A335` consumer band only for provable source-plane relationships.
5. Promoted only byte-level results that were directly proven.

---

## Starting point from pass 47
Pass 47 had already established:

- `C1:0299` is the full rebuild/controller for the three-lane `0CC0` companion strip
- the strip includes a fixed 5-byte per-lane run from `CC:F837 + lane`
- additional dynamic glyph groups are emitted through a helper path involving `9499..949F`
- `C1:06F0` is a scaled bar/meter renderer
- `0E80+` is definitely read downstream in bank `C0`

The main unresolved question was what those dynamic helper-generated glyph groups actually were.

---

## 1. `C1:011F` is a real **3-digit decimal tile formatter**
This routine is now structurally clear.

### Proven behavior
It uses `7E:9499` as a 16-bit working value and does two subtraction-count loops:

- subtract `0x0064` repeatedly to count the hundreds digit
- subtract `0x000A` repeatedly to count the tens digit
- the remaining value is the ones digit

It then maps those three digit counts through the ROM table at `CC:F903` and stores the resulting tile bytes to:

- `949D` = hundreds tile
- `949E` = tens tile
- `949F` = ones tile

It also sets:

- `949C = 0xFF`

### Why this is strong
This is not a text decoder, icon selector, or generic glyph copier.
It is plain decimal decomposition followed by tile lookup.

Safest keepable reading:

> `C1:011F` = **format a 16-bit value as three decimal digit tiles into `949D..949F`**

---

## 2. `C1:0174` is the sibling **2-digit decimal tile formatter**
This routine is a cut-down version of the same pattern.

### Proven behavior
It:

- subtracts `0x000A` repeatedly to count the tens digit
- leaves the remainder as the ones digit
- maps both through `CC:F903`
- stores the results to:
  - `949E` = tens tile
  - `949F` = ones tile
- fills the higher positions with blanks:
  - `949C = 0xFF`
  - `949D = 0xFF`

Safest keepable reading:

> `C1:0174` = **format a value as two decimal digit tiles into `949E..949F`, blanking the higher positions**

---

## 3. `C1:104E` is not a renderer; it is a **leading-zero blanker** for the decimal tile buffer
This helper is tiny but important.

### Proven behavior
It checks the already-generated tile bytes at `949D` and `949E`.

- if `949D == 0x73`, it replaces it with `0xFF`
- if `949E == 0x73` **and** `949D == 0xFF`, it replaces `949E` with `0xFF`

So it only removes zero tiles from the left side, and only after the numeric formatter has already run.

### Why this matters
This proves the glyph groups in this path are not meant to be fixed-width raw digits only.
They are **presentation-formatted decimal fields** with suppressed leading zeroes.

Safest keepable reading:

> `C1:104E` = **blank leading zero digit tiles in `949D..949E` by converting tile `0x73` to `0xFF`**

---

## 4. `CC:F903` is the live **decimal digit tile code table**
The helpers above all index the same ROM table beginning at `CC:F903`.

### Proven live values
The first ten live bytes are:

```text
73 74 75 76 77 78 79 7A 7B 7C
```

Those are indexed by the decimal digit counters produced by `011F` / `0174`.

So the safe reading is:

> `CC:F903` = **decimal digit tile codes for `0..9`**

This also explains why `104E` specifically tests for `0x73`:
that is the tile code for decimal digit `0` in this presentation path.

---

## 5. The “dynamic glyph groups” in `C1:0299` are now proven to be **numeric fields**, not generic icons or text fragments
This is the biggest semantic gain of the pass.

After the fixed 5-glyph lane run, `C1:0299` builds three dynamic groups per enabled lane.

### Shared source-selection pattern
The lane index is converted through `CC:F8ED`, whose proven live values in this path are:

```text
0000, 0080, 0100
```

That is then used as an `X` offset into a `0x80`-stride per-record block rooted at `5E30`.

So the dynamic fields are not free-floating state reads.
They are pulled from a real lane-selected record family.

### Field A — three-digit formatted numeric value from `5E30[offset]`
The first dynamic group:

- loads `5E30[offset]` into `9499`
- formats it through `011F`
- runs `104E`
- writes the resulting decimal tiles into the lane’s `0CC0` block

There is also a pre-render comparison against `5E32[offset] >> 8` that can increment `A10F`, so this field is structurally related to the next field rather than being an isolated number.

### Field B — second three-digit formatted numeric value from `5E32[offset]`
The next group:

- loads `5E32[offset]` into `9499`
- formats it through `011F`
- runs `104E`
- writes the resulting decimal tiles into a second anchor position in the lane block

### Field C — two-digit formatted numeric value from `5E34[offset]`
The third group:

- loads `5E34[offset]` into `9499`
- formats it through `0174`
- conditionally runs `104E` depending on layout path
- writes the resulting tiles into a smaller 2-digit field in the lane block

### Structural consequence
The dynamic groups in the strip are now best read as:

> **lane-selected decimal numeric presentation fields rendered into the `0CC0` strip**

That is a materially harder result than pass 47’s generic “dynamic glyph groups” wording.

The exact gameplay-facing names of the three fields are still open.
But they are now clearly **numbers**, not names, commands, or arbitrary tile fragments.

---

## 6. `9F20` is more strongly acting like a **3-layout numeric panel mode**, not just a vague strip selector
Pass 47 already established that `9F20` chose among strip layouts.
This pass tightens that from the numeric writer side.

For the three dynamic numeric fields, `9F20` changes:

- which horizontal anchor each field uses
- whether a field is placed at `base + offset` versus `base - offset`
- whether the later fixed separator/bar logic is present

So `9F20` is not merely selecting between unrelated template fragments.
It is choosing among three **numeric panel layouts** that reposition the same underlying fields.

That is still not enough to assign final human-facing mode names.
But it is stronger than the older generic “3-state strip layout selector” wording.

---

## 7. Re-checking the bank-`C0` consumer strengthens the source-plane model, even though the final routine name is still not ready
This pass did revisit the seam from pass 47.
The strongest safe result is not a final routine label, but a clearer producer/consumer relationship.

### Proven from `C0:A270..A335`
The consumer reads four source planes in lockstep:

- `7F:0C00,X`
- `7F:0C80,X`
- `7F:0E00,X`
- `7F:0E80,X`

It conditionally forwards the first two planes when the source byte is nonzero, while still copying the latter pair into adjacent destination bytes.

### What this strengthens
This means the downstream path is not treating `0E80` as a free-standing record blob.
Instead, the bank-`C0` copy logic is consuming the `0Cxx` and `0Exx` families as **parallel source planes**.

That is enough to strengthen the broader model:

> the strip/record presentation branch is built as paired or parallel byte planes that are later merged/copied downstream

I am still **not** forcing a final routine name for `C0:A270..A335`, because the destination-side higher-level identity is not yet locked.

---

## Net result of pass 48
This pass materially advances the presentation branch in four ways.

### 1. The helper path is no longer generic
`011F`, `0174`, and `104E` are now solved as:

- 3-digit decimal formatter
- 2-digit decimal formatter
- leading-zero blanker

### 2. The dynamic strip groups are now known to be numeric
The lane strip emitted by `C1:0299` does not just mix fixed icons and unknown helper output.
It contains **real decimal presentation fields** sourced from lane-selected record data.

### 3. The lane-selected record source is structurally stronger
The `CC:F8ED` live subgroup `0000/0080/0100` plus the `5E30/5E32/5E34` access pattern show the numeric fields come from a genuine `0x80`-stride record family.

### 4. The consumer relationship is stronger even though the final name is still open
The bank-`C0` path is now better understood as consuming **parallel source planes**, which supports the producer-side panel/strip model without overclaiming the final subsystem label.

---

## Next clean seam after pass 48
The best continuation target is now:

1. identify the exact semantics of the three numeric source fields:
   - `5E30[offset]`
   - `5E32[offset]`
   - `5E34[offset]`
2. determine what the `A10F` increment path is counting/warning about when `5E32 >> 8` falls below `5E30`
3. tighten the downstream bank-`C0` destination side enough to decide whether this is best described as a status panel, formation panel, command panel, or another presentation subsystem

That is now the cleanest abstraction gap on this branch.
