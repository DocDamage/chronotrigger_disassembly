# Chrono Trigger Disassembly — Pass 27

This pass followed the open thread from pass 26, but with a more grounded target:

- pass 26 proved that `E4:F605..F608` are copied into:
  - `970B`
  - `9716`
  - `9721`
  - `972C`
- but there still were **no clean direct consumers** pinned down for those exact arrays

So instead of pretending otherwise, this pass traced the **adjacent live control block** around them to find the nearest hard geometry/position semantics.

## Goal

Answer two questions cleanly:

1. what are the neighboring `97xx` tables actually doing
2. do they reveal anything trustworthy about the role of the `F600` record tail

## High-confidence findings

## `9708` and `9713` are signed X/Y offset tables

Across multiple routines in bank `C1`, the same exact pattern appears:

- load a base slot coordinate from:
  - `1D0C`
  - `1D23`
- add:
  - `9708`
  - `9713`
- and then store/use the resulting coordinate

The cleanest examples are at:

- `C1:183B..1852`
- `C1:7657..7678`
- `C1:784B..786C`
- `C1:788C..78AD`

The dataflow is consistent:

- `9708` is added to the slot X-side coordinate
- `9713` is added to the slot Y-side coordinate
- `9713` is explicitly treated as signed, with clamp/wrap logic for underflow/overflow

So these are best read as:

- `9708` = signed X offset table
- `9713` = signed Y offset table

The exact higher-level owner of the 3-entry tables is still open, but the coordinate role is not.

## `971E` and `9729` are half-extent / radius tables

The routine at `C1:285A` is the clearest geometry builder in this region.

It takes center-like values from:

- `A039`
- `A050`

and computes:

- low X bound into `975A`
- high X bound into `9770`
- low Y bound into `9765`
- high/terminal Y bound into `977B`

The calculations are explicit:

- X bounds use `971E`
- Y bounds use `9729`

The code does:

- center minus extent
- center plus extent

with signed-aware clamp behavior.

That is not vague “some arithmetic.” It is a real **bounds-from-center-and-half-size** builder.

So the best-fit names are:

- `971E` = half-width / X extent
- `9729` = half-height / Y extent

And the outputs are best understood as per-object signed bounds:

- `975A` = min X
- `9770` = max X
- `9765` = min Y
- `977B` = max/terminal Y

## The `97xx` region is split into interleaved 3-entry geometry tables and 8-entry extended-slot tables

This matters because it makes the layout around the pass-26 arrays less mysterious.

### Early init at `CC:E3C0`
This init code seeds several **3-entry** tables:

- `9708..970A` -> cleared
- `9713..9715` -> `F0`
- `971E..9720` -> `08`
- `9729..972B` -> `08`
- `973F..9741` -> `01`

### Extended loader at `CC:EBB0`
The pass-26 loader installs **8-entry** data into the neighboring regions:

- `970B..9712`
- `9716..971D`
- `9721..9728`
- `972C..9733`

So the WRAM block is not one flat homogeneous table.
It is an **interleaved control area** where:

- 3-entry geometry/profile tables live beside
- 8-entry extended-slot/runtime tables

That layout is important because it means the copied `F605..F608` bytes sit directly next to a confirmed geometry block.

## What this does and does not prove about `F605..F608`

### What it **does** prove
It gives the first trustworthy local context:

- the copied bytes are installed into a WRAM neighborhood that already contains:
  - signed offsets
  - half-extents / radii
  - and later timer/state bytes

So the tail of the `F600` records is living inside a very real **geometry/control/state** region, not some random dead scratch area.

### What it **does not** prove
I still do **not** have a clean direct consumer for the exact arrays:

- `970B..9712`
- `9716..971D`
- `9721..9728`
- `972C..9733`

So I am **not** assigning fake names like:

- “extended X offset”
- “extended Y offset”
- “extended half-width”
- “extended half-height”

That pattern is tempting because of the neighboring 3-entry tables, but it is not locked yet.

## Best-fit names after this pass

These are the names I am comfortable assigning now:

- `C1:285A` = `Build_SignedBounds_FromCenter_UsingHalfExtents`
- `7E:9708` = `Profile3_SignedOffsetX`
- `7E:9713` = `Profile3_SignedOffsetY`
- `7E:971E` = `Profile3_HalfWidth`
- `7E:9729` = `Profile3_HalfHeight`
- `7E:975A` = `ObjectBounds_MinX`
- `7E:9770` = `ObjectBounds_MaxX`
- `7E:9765` = `ObjectBounds_MinY`
- `7E:977B` = `ObjectBounds_MaxOrTerminalY`

For the pass-26 arrays, the honest names remain:

- `970B..9712` = unresolved extended param bank 0
- `9716..971D` = unresolved extended param bank 1
- `9721..9728` = unresolved extended param bank 2
- `972C..9733` = unresolved extended param bank 3

## Honest limits

What is still unresolved after this pass:

- direct consumers for the exact `F605..F608` target arrays
- whether those four 8-byte banks mirror the neighboring offset/extent pattern
- the exact owner/subsystem of the 3-entry geometry profile tables

## Practical takeaway

Pass 26 proved the back half of `E4:F600` is real runtime data.

Pass 27 adds the first clean local structure around that tail:

- neighboring tables are definitely signed offsets and half-extents
- the surrounding WRAM block is a real geometry/control neighborhood
- but the exact semantic names of the copied `F605..F608` banks are still open

So the right next move is **not** to overlabel those four arrays.
The right next move is to trace the routines that touch the later bounds outputs (`975A/9765/9770/977B`) and the nearby unresolved `970B/9716/9721/972C` banks together, because that is where the geometry and extended-tail data are most likely to converge.
