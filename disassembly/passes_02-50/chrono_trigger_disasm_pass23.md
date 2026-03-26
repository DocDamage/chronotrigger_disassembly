# Chrono Trigger Disassembly — Pass 23

This pass targeted the render-side question left open after pass 22:

- if classes 0/1/2 materialize from `7F:4800 -> 7F:4BC0`,
- then what exactly is the class-3 route,
- and do the negative `1B00` paths on the other classes indicate a reusable cache-only render path?

## Goal

Resolve whether the remaining render routines are:

1. another hidden `4800 -> 4BC0` materializer stage, or
2. a family of **cache re-anchor / reposition-only** paths that reuse already prepared `4BC0` records.

## High-confidence finding

## There is a real family of cache-only re-anchor paths for metasprite classes 0–3

The routines are:

- `C0:B788` — class 0 cache re-anchor
- `C0:BA65` — class 1 cache re-anchor
- `C0:BFF2` — class 2 cache re-anchor
- `C0:C73A` — class 3 cache re-anchor

These routines **do not read `7F:4800` at all**.

Instead, they:

- read the slot anchors from `0A00 / 0A80`
- walk already prepared relative records in the `7F:4BC0` family
- recompute low-OAM X from the cached relative X words
- rebuild packed X-MSB / high-table bytes
- recompute low-OAM Y from cached relative Y bytes
- leave tile/attr payloads alone

That is a materially different path from the class-0/1/2 materializers found earlier.

## Dispatch proof from `C0:B701`

The class selector at `C0:B701` now reads very cleanly in 8-bit A mode:

- `1201,X & 3 == 0` -> class 0 path
  - full materializer: `JSR B8CA`
  - cache re-anchor fallback: `JSR B788`

- `1201,X & 3 == 1` -> class 1 path
  - full materializer: `JSR BCDC`
  - cache re-anchor fallback: `JSR BA65`

- `1201,X & 3 == 2` -> class 2 path
  - full materializer: `JSR C2BF`
  - cache re-anchor fallback: `JSR BFF2`

- `1201,X & 3 == 3` -> class 3 path
  - direct `BRL C73A`

So class 3 is special here:

- it goes straight to the cache re-anchor routine
- it does **not** go through a `4800 -> 4BC0` materializer in this dispatch block

## What the cache re-anchor paths do

## Common setup

All four routines start the same way:

- switch DB to `7F`
- load slot Y anchor from `0A80,X & 01FF` -> `$C5`
- load slot X anchor from `0A00,X` -> `$C3`
- load the record-base from `1700,X`

This is the same anchor setup used by the full materializers, but the data source is different.

## X side: cached relative-X words -> finalized low X + packed X MSBs

Example from `C0:C6E7`, which `C73A` calls repeatedly:

- read `4BC2 / 4BCA / 4BD2 / 4BDA`
- add slot X anchor `$C3`
- write finalized low X to:
  - `4BC0`
  - `4BC8`
  - `4BD0`
  - `4BD8`
- extract the X MSB from each result
- pack the four bits into one byte
- OR with `#$AA`
- return the packed high-table byte

`C73A` calls that helper six times and stores the results to:

- `4F00`
- `4F01`
- `4B40`
- `4B41`
- `4F80`
- `4F81`

That matches class 3 exactly:

- `24 sprites / 4 sprites per high-table byte = 6 packed bytes`

## Y side: cached relative-Y bytes -> finalized low Y

The class-3 path then updates Y directly from the cached relative-Y bytes:

- `4BC4 -> 4BC1`
- `4BCC -> 4BC9`
- `4BD4 -> 4BD1`
- `4BDC -> 4BD9`
- `4BE4 -> 4BE1`
- ...
- continuing on an 8-byte stride through the class-3 record span

It applies the same hide/clamp logic seen elsewhere, writing `E0` when the result is offscreen.

The important point is:

- the class-3 path updates **existing cache records in place**
- it is not staging from `4800`

## Class 0/1/2 re-anchor paths show the same pattern

The sibling routines at `B788`, `BA65`, and `BFF2` do the same kind of work, scaled to their class sizes:

- walk cached `4BC2`-family relative-X words
- finalize low X
- rebuild packed X-MSB bytes
- then walk cached `4BC4`-family relative-Y bytes
- finalize low Y with the same hide/clamp logic

They also never touch `4800`.

So the architectural split is now clear:

### Full materializer path
Used when the slot needs the prepared render cache rebuilt from upstream staged template records.

- class 0: `B8CA`
- class 1: `BCDC`
- class 2: `C2BF`

### Cache re-anchor path
Used when the prepared cache is already valid and only the anchored on-screen positions / high-table bytes need refreshing.

- class 0: `B788`
- class 1: `BA65`
- class 2: `BFF2`
- class 3: `C73A`

## What this means for class 3

This answers the class-3 question from pass 22:

- class 3 **does not** appear to use the `4800 -> 4BC0` materializers in the `B701` dispatch path
- instead, it uses a dedicated **cache-only re-anchor path**
- that path assumes the `4BC0`-family cache records already exist
- and only refreshes anchored X/Y plus packed high-table bytes

That is the cleanest current explanation for why class 3 looked different.

## Honest limit

I have **not** yet proven where the class-3 `4BC0` cache records are first built.

I **have** proven that:

- the routine used at runtime by the class selector is a cache re-anchor path
- it does not consume `4800`
- and it works entirely from already prepared `4BC0`-family relative records

So the next unresolved question is now narrower:

- **where does the class-3 prepared cache originally come from?**

## Best current labels

- `C0:B788  Reanchor_Class0_RenderCache_From4BC0`
- `C0:BA65  Reanchor_Class1_RenderCache_From4BC0`
- `C0:BFF2  Reanchor_Class2_RenderCache_From4BC0`
- `C0:C73A  Reanchor_Class3_RenderCache_From4BC0`
- `C0:C6E7  Pack4SpriteXmsbs_AndFinalizeLowX_Class3`
- `7F:4BC2  CachedRelativeXWord_RecordField`
- `7F:4BC4  CachedRelativeYByte_RecordField`

## Bottom line

This pass resolves the render-path split:

- `7F:4800` is the direct upstream source for the **full materializers**
- but there is a separate family of **cache-only re-anchor** paths that reuse already prepared `4BC0` records
- class 3 currently lands in that re-anchor family directly
- so class 3’s runtime path is **not** another hidden `4800` materializer — it is a prepared-cache reuse path
