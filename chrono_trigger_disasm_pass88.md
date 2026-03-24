# Chrono Trigger Disassembly — Pass 88

## Scope of this pass
Pass 87 froze the downstream `F8EB / F91C / F972 / F9AF / F9E7` cluster as a real
**column-raster** family, but it still left one ugly ownership seam open:

- what exactly are the WRAM targets rooted by `C161 / C163 / C4E1 / C4E3`?
- are they one-off strip buffers, or part of a larger structured workspace?
- what code actually owns the copy/mirror behavior between them?

This pass closes that seam enough to stop treating those roots like isolated addresses.

The strongest keepable result is:

> the `7E:C161..7E:C7F3` neighborhood is a real **dual-bundle eight-table raster-target workspace**.
>
> It is not one strip. It is two companion WRAM bundles, and each bundle has two exact band families:
> - one mirrored in **0x6C-byte** windows
> - one mirrored in **0x70-byte** windows
>
> `7C.bit0` is the exact direction selector for those mirror helpers.

I am still keeping the final presentation noun one notch below frozen,
but the structural ownership is now solid.

---

## 1. `CE:E000..CE:E08D` is an exact selected-`0x6C`-band mirror between two eight-table bundles
This helper is now exact enough to freeze.

### exact structure
It does the following:

- reads one byte from `[$40]`
- doubles it (`ASL A`) and uses that as the starting `X`
- computes the stop offset as `start + 0x006C`
- checks `7C.bit0`
- then mirrors one selected `0x6C` window between two eight-table WRAM bundles

When `7C.bit0 != 0`, it copies:

- `C161 + X -> C4E1 + X`
- `C1CD + X -> C54D + X`
- `C239 + X -> C5B9 + X`
- `C2A5 + X -> C625 + X`
- `C311 + X -> C691 + X`
- `C37D + X -> C6FD + X`
- `C3E9 + X -> C769 + X`
- `C455 + X -> C7D5 + X`

When `7C.bit0 == 0`, it performs the exact reverse copy.

The loop advances by `X += 4` until the computed stop offset is reached.

### strongest safe reading
> `CE:E000..CE:E08D` mirrors one selected **0x6C-byte band** between a primary and shadow
> **eight-table raster-target bundle**, with direction chosen by `7C.bit0`.

This is the first exact ownership proof that the `C161 / C4E1` family is part of a larger structured workspace,
not a pair of isolated strip roots.

---

## 2. `D1:F5F6..D1:F676` is an exact selected-`0x70`-band mirror for the companion bundle family
This is the matching D1-side mirror helper for the companion roots.

### exact structure
It:

- enters with `X` already selecting the band start
- checks `7C.bit0`
- mirrors one selected `0x70` window between these exact roots

Primary-side roots:

- `C163`
- `C1D3`
- `C243`
- `C2B3`
- `C323`
- `C393`
- `C403`
- `C473`

Shadow-side roots:

- `C4E3`
- `C553`
- `C5C3`
- `C633`
- `C6A3`
- `C713`
- `C783`
- `C7F3`

When `7C.bit0 != 0`, it copies primary -> shadow.
When `7C.bit0 == 0`, it copies shadow -> primary.

The loop again advances in `X += 4` steps until the selected `0x70` window is done.

### strongest safe reading
> `D1:F5F6..D1:F676` mirrors one selected **0x70-byte band** between the companion primary/shadow
> eight-table raster-target bundles, again with direction chosen by `7C.bit0`.

This is the companion half that proves the workspace is not just one address family.
It is a paired multi-table target structure.

---

## 3. `D1:FD80..D1:FE46` is the transformed mirror for that same `0x70`-band family
This helper is exact, and importantly it is **not** a plain copy.

### exact structure
It uses the same exact root families as `D1:F5F6..F676`, but before each store it applies:

- `EOR #$FFFF`
- `XBA`

Then it stores the transformed word to the opposite bundle.

When `7C.bit0 != 0`, it transforms primary -> shadow.
When `7C.bit0 == 0`, it transforms shadow -> primary.

### strongest safe reading
> `D1:FD80..D1:FE46` mirrors one selected **0x70-byte band** between the same companion bundles,
> but with an exact **complement-and-byte-swap** transform before the store.

I am deliberately keeping the final presentation meaning of that transform open.
What is frozen here is the exact mechanics.

---

## 4. this upgrades the noun for the `C161 / C163 / C4E1 / C4E3` neighborhood
Before this pass, those roots were good targets but still read like scattered raster strips.

After freezing the exact mirror helpers, the safer noun is now:

> `7E:C161..7E:C7F3` is a **dual-bundle eight-table raster-target workspace**.

More specifically:

- one bundle lives in the lower `C1xx..C4xx` roots
- one companion/shadow bundle lives in the upper `C4Ex..C7Fx` roots
- one band family mirrors in `0x6C` windows (`CE:E000..E08D`)
- one companion band family mirrors in `0x70` windows (`D1:F5F6..F676`)
- `D1:FD80..FE46` applies an exact transformed mirror over that same `0x70` family
- `7C.bit0` is the exact direction selector for all of this

That is enough to say the pass-87 column-rasterizer is writing into a real structured target workspace,
not anonymous strips.

---

## 5. what I am **not** freezing yet
Even after this pass, I am **not** claiming these are definitively one specific gameplay/UI object.

I am still not freezing:

- the final presentation noun of the whole workspace
- the first exact higher-level caller contract for the `0x6C` vs `0x70` split
- the first exact external reader of `CE0F`
- the full write-side semantics of the nearby `EDF3 / EE50 / EEA6` D1 cluster

Those are the next seam.

---

## 6. strongest keepable summary from pass 88
If this pass gets reduced to one sentence, it should be this:

> the `C161 / C163 / C4E1 / C4E3` targets are part of a real **dual-bundle eight-table raster workspace**,
> and the ROM contains exact mirror helpers for selected `0x6C` and `0x70` bands between the two bundles,
> with `7C.bit0` selecting direction.
