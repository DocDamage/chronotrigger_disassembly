# Chrono Trigger Disassembly — Pass 24

This pass targeted the remaining class-3 render question left open after pass 23:

- pass 23 proved that the runtime class-3 path in `C0:B701` goes straight to a **cache re-anchor** routine (`C0:C73A`)
- but it did **not** prove where the class-3 `7F:4BC0` cache records were originally built

## Goal

Find the **real full-build / materialization path** for class 3, if one exists, and determine whether class 3 has its own upstream source format.

## High-confidence finding

## `C0:E12A` is the missing full-build path for class 3

The runtime renderer at `C0:B701` still uses the re-anchor-only path for class 3:

- `C0:C73A  Reanchor_Class3_RenderCache_From4BC0`

But there is a separate routine at:

- `C0:E12A`

that performs the **actual class-3 build**.

This resolves the apparent contradiction:

- class 3 does have a full build path
- it just does **not** live inside the `B701` runtime render dispatch block
- `B701` assumes the class-3 cache is already built and only refreshes anchored positions / high-table bytes

## Direct caller proof

A clean runtime caller exists at `C0:47E9`.

That code does:

- load `1201,X`
- `AND #$03`
- compare against `#$03`
- if class 3, call `JSR E12A`

So `E12A` is not a random helper. It is an explicit **class-3 setup/build route** selected from the per-slot class byte.

There is also an earlier call at `C0:0212`, consistent with a more global / initial rebuild path.

## What `C0:E12A` does

This routine is the real answer to “where do class-3 `4BC0` cache records come from?”

### 1. It loads two source streams from per-slot pointer fields

At entry it pulls two long-pointer style sources from the slot tables:

- `1200 / 1280` -> source used by the 32-byte chunk copy/flip helpers
- `1300 / 1380` -> source used as the class-3 descriptor / XY-tail stream

So class 3 is not driven from `7F:4800`.
It has its **own source format**.

## 2. It builds `0x60` tile chunks = exactly the class-3 graphics payload

The key loop starts with:

- `LDA #$3800`
- store to `0D80,X` and local work ptr `$D0`
- set WRAM port address to bank `01`, offset `$3800`
- `LDA #$0060`
- `STA $C9`
- `LDY #$0000`

Then, for each of the `0x60` entries:

- read a **16-bit descriptor word** from `[$D3],Y`
- test bit `0x4000`
- dispatch to:
  - `C0:E687` when set (direct 32-byte chunk copy)
  - `C0:E534` when clear (32-byte horizontal-flip copy via the `FD:0000` bit-reversal table)
- advance `Y` by 2
- repeat `0x60` times

That means class 3 uses:

- **96 chunk descriptors**
- each descriptor expands/copies **32 bytes**
- total output size = `0x60 * 0x20 = 0x0C00`

That exactly matches the later DMA size configured by the same routine.

## 3. It DMA-uploads the generated class-3 graphics block

After the `0x60` chunk loop, the routine programs DMA channel 7:

- source bank: `7F`
- source addr: `0x3800`
- transfer size: `0x0C00`
- VRAM destination: `0x0400`
- start DMA via `$420B`

So this is not just a render-cache setup routine.
It is a **graphics-build + upload** path for class 3.

That is a major distinction from the `B701` re-anchor path.

## 4. It then builds the class-3 `7F:4BC0` cache records directly

After DMA, the routine switches to cache construction.

It loads:

- `X = 1700,slot`
- `Y = 0x00C0`

Then it reads the class-3 tail stream from `[$D3],Y` and writes directly into the `4BC0` cache family.

### XY record build

For each of the 24 records, it writes:

- signed relative X byte -> `4BC2/4BC3`, `4BCA/4BCB`, ... up through `4C7A/4C7B`
- relative Y byte -> `4BC4`, `4BCC`, ... up through `4C7C`

The X byte is explicitly sign-extended into the adjacent high byte.

So the class-3 cache records are **not** materialized from `7F:4800`.
They are built directly from the class-3 tail stream.

## 5. It writes a fixed tile-number layout for all 24 records

The routine then assigns literal tile bytes directly into the class-3 cache:

First 8 records:

- `40, 42, 44, 46, 48, 4A, 4C, 4E`

Next 8 records:

- `60, 62, 64, 66, 68, 6A, 6C, 6E`

Final 8 records:

- `80, 82, 84, 86, 88, 8A, 8C, 8E`

These are written to:

- `4BC6 .. 4BFE`
- `4C06 .. 4C3E`
- `4C46 .. 4C7E`

So the class-3 layout uses a fixed **3 x 8 tile-number grid**.

## 6. It writes a fixed attr byte for all 24 records

After the tile bytes, it writes a constant attr byte:

- `#$22`

into every attr slot:

- `4BC7 .. 4BFF`
- `4C07 .. 4C3F`
- `4C47 .. 4C7F`

So class 3 has:

- variable graphics chunk content
- variable signed XY tail
- but a fixed literal tile-index layout and fixed attr byte pattern

## What this resolves

This is the missing bridge from pass 23.

The class-3 render architecture now reads cleanly:

### Full-build path
- `C0:E12A`
- uses a class-3 descriptor/tail stream
- builds `0x60` 32-byte graphics chunks
- DMA uploads them to VRAM
- directly builds the `7F:4BC0` cache records for all 24 sprites

### Runtime draw path
- `C0:B701` selects class 3
- branches to `C0:C73A`
- `C73A` only re-anchors existing cache records and rebuilds packed high-table bytes

So the answer is:

**class 3 absolutely does have a full build path — it just lives upstream at `C0:E12A`, not in the runtime render dispatch.**

## Strongest current labels

- `C0:E12A  BuildClass3_GfxUpload_AndRenderCache`
- `1200/1280  Class3_ChunkSourceLongPtr`
- `1300/1380  Class3_DescriptorTailLongPtr`
- `0D80,X     Class3_GfxBufferOffset_7F`
- `7F:3800    Class3_GeneratedTileChunkBuffer`
- `7F:4BC2..4C7C  Class3_CachedRelativeXyFields`
- `7F:4BC6..4C7E  Class3_CachedTileBytes`
- `7F:4BC7..4C7F  Class3_CachedAttrBytes`

## Honest limit

I have **not** yet proven who populates the per-slot pointer fields:

- `1200/1280`
- `1300/1380`

But I **have** now proven where the class-3 cache records actually come from.

That was the main open render-side question.

## Bottom line

Pass 23 established that class 3 is re-anchored from already prepared `4BC0` cache data at runtime.

This pass proves where that prepared data comes from:

- `C0:E12A` is the class-3 full-build route
- it uses a dedicated class-3 source format
- it builds tile graphics, uploads them, and directly constructs the 24-record `4BC0` cache
- then the runtime renderer later reuses that cache through `C0:C73A`
