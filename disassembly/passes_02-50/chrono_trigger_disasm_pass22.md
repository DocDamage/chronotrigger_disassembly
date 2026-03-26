# Chrono Trigger Disassembly — Pass 22

This round targeted the last big render-side gap from the earlier passes:

- how the upstream `7F:4800` metasprite template staging actually turns into the later `7F:4BC0 / 4F00 / 4B40 / 4F80` prepared render cache.

## Goal

Earlier passes had already established:

- `7F:4800` is an upstream template/staging family
- `7F:4BC0` and the `4F00/4B40/4F80` side tables are what the OAM emitter actually consumes
- class-sized builders exist at:
  - `C0:B8CA`
  - `C0:BCDC`
  - `C0:C2BF`
  - `C0:C73E`

The open question was whether there was a *direct* handoff from the `4800` staging records into the later render cache, or whether another hidden format conversion stage sat between them.

## High-confidence finding

## `C0:B8CA` is a direct materializer from `7F:4800` staging records into the `7F:4BC0` prepared render cache

The class-0 cache builder is the cleanest proof.

At the front of `C0:B8CA`:

- `0A80,X & #$01FF` is loaded into `$C5`
- `0A00,X` is loaded into `$C3`
- `1700,X` is used as the class-local record-base offset

Then the routine repeatedly does this shape on an 8-byte stride:

```asm
LDA $4802,X
STA $4BC2,X
CLC
ADC $C3
SEP #$20
STA $4BC0,X
...
LDA $4804,X
STA $4BC4,X
CLC
ADC $C5
...
STA $4BC1,X
...
REP #$20
LDA $4806,X
STA $4BC6,X
```

That is not a vague relationship.
It is a direct record materialization path.

## What the materializer is doing

For each staged sprite record:

- **`4802/4803` -> `4BC2/4BC3`**
  - copy the 16-bit relative X work word
  - add the slot X anchor in `$C3`
  - write finalized low-OAM X into `4BC0`

- **`4804` -> `4BC4`**
  - copy the relative Y work byte
  - add the slot Y anchor in `$C5`
  - write finalized low-OAM Y into `4BC1`
  - apply an `E0` hide/clamp rule when the result is offscreen

- **`4806/4807` -> `4BC6/4BC7`**
  - copy the tile/attr word straight through into the prepared cache

This is the exact bridge between the two staging families that was still open after the previous passes.

## The `7F:4800` records are now better specified

The earlier passes already showed that `7F:4800` uses an 8-byte stride.
This pass shows which of those bytes are actually consumed by the materializers.

### Strong current read on the staging-record fields

On the 8-byte stride at `7F:4800`:

- `+02/+03` = relative X work word
- `+04` = relative Y work byte
- `+06/+07` = tile/attribute word

This is now stronger than before because the class-0 builder copies those exact fields into the later render cache and finalizes screen-space X/Y from them.

### Honest limit

I am **not** claiming that `+00/+01/+05` are globally unused everywhere.
I **am** claiming that in the direct `4800 -> 4BC0` materializer path at `C0:B8CA`, the consumed per-record payload is the `+02`, `+04`, and `+06/+07` set.

## The high-table byte is built during the same materialization pass

The same builder accumulates one packed OAM high-table byte while walking the class-0 records.

The loop:

- adds the X anchor
- extracts the X MSB
- accumulates two-bit groups into `$E5`
- and then stores the final packed byte to `7F:4F00,X`

That means the materialization pass is not just copying records.
It is also generating the cache-side high-table payload for the class.

## The larger class builders reuse the same `4800 -> 4BC0` pattern

The larger builders at `C0:BCDC` and `C0:C2BF` follow the same structural pattern:

- same slot anchor setup from `0A00/0A80`
- same use of `1700,X` as the class-local record-base
- same `4802 -> 4BC2`, `4804 -> 4BC4`, `4806 -> 4BC6` materialization shape
- same packed-X-MSB high-table generation shape

They then repeat the operation across additional subgroup offsets (`+0x20`, `+0x40`, etc.) to cover the larger metasprite classes.

So the open architectural question can now be answered cleanly:

- **yes, the `7F:4800` family is the direct upstream source for the prepared render cache in the class-0/1/2 builders**
- the handoff is not hypothetical
- it is implemented as an explicit record-materialization pass

## What this changes architecturally

This tightens the whole render chain:

1. earlier builders create/stage template records in `7F:4800`
2. class materializers (`B8CA / BCDC / C2BF`) copy and finalize them into `7F:4BC0`
3. those materializers also build the high-table payload bytes in `4F00/4B40/...`
4. the bucketed OAM emitter later consumes the prepared cache

So the old wording:

- "`7F:4800` is an upstream staging family"

can now be sharpened to:

- **`7F:4800` is the direct per-sprite template source for the class-0/1/2 cache materializers**

## Best current labels

- `C0:B8CA  Materialize_Class0_RenderCache_From7F4800`
- `C0:BCDC  Materialize_Class1_RenderCache_From7F4800`
- `C0:C2BF  Materialize_Class2_RenderCache_From7F4800`
- `7F:4800+2  StagedRelativeXWord`
- `7F:4800+4  StagedRelativeYByte`
- `7F:4800+6  StagedTileAttrWord`

## Still open

The main remaining render-side questions are now narrower:

1. whether class 3 (`C0:C73E`) uses the same upstream record family indirectly or arrives through a separate pre-materialized route
2. exact meaning of the `+00/+01/+05` bytes in the `7F:4800` records
3. whether there is a reusable “reposition-only” path that updates `4BC0` from already materialized cache data without re-reading `4800`

## Bottom line

This pass resolves the biggest remaining handoff question on the render side:

- `7F:4800` is not just a vaguely related upstream area
- for class 0/1/2, it is the **direct source** of the prepared render cache
- the class builders copy staged relative X/Y/tile+attr fields from `4800`
- then finalize them into `4BC0` and generate the OAM high-table bytes
