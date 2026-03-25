# Chrono Trigger Disassembly — Pass 28

This pass followed the exact thread left open in pass 27:

- pass 27 proved that `975A / 9765 / 9770 / 977B` are real per-object bounds outputs
- but the missing question was what *uses* those bounds downstream, and whether that path crosses back into the unresolved extended-slot state

So this round stayed grounded on the immediate consumers in bank `C1`.

## Goal

Answer two concrete questions:

1. what the first direct bounds consumers are actually doing
2. whether they expose trustworthy new semantics without overlabeling the unresolved `970B / 9716 / 9721 / 972C` banks

## High-confidence findings

## `C1:28AD` is an active-object bounds overlap scan with a classified return code

The routine beginning at `C1:28AD` does not touch the unresolved `97xx` tail banks directly.
Instead, it walks the already-built bounds outputs and checks them against other active slots.

### Core behavior

It starts by scanning `Y` from zero upward, skipping the current slot (`CPY $80`) and ignoring entries that fail three gate checks:

- `96F5,Y` must be nonzero
- `9FF7,Y` must be nonnegative
- `A5CD,Y` must be nonnegative

After that, it compares the current slot's rectangle against slot `Y` using the pass-27 bounds outputs:

- `975A` / `9770` for X min/max
- `9765` / `977B` for Y min/max

The compare sequence is real rectangle-overlap logic, not a vague proximity test:

- reject if one rectangle is fully left/right of the other
- reject if one rectangle is fully above/below the other
- otherwise treat it as overlap

### Return behavior

The routine returns:

- `0` when no overlap is found
- `0x80` when an overlap is found with a slot index `< 3`
- `0x81` when an overlap is found with a slot index `>= 3`

So this is not just a boolean overlap test.
It is a **classified overlap result**, where the low bit reflects whether the collided slot falls in one of two index ranges.

### Best-fit name

`C1:28AD = Scan_ActiveObjectBoundsOverlap_ClassifyHit`

That is the strongest honest name after this pass.
It does **not** claim to know exactly what slots `0..2` versus `3..10` represent, only that the routine explicitly distinguishes them.

## `C1:2927` tests object bounds against a 16x16 local collision-flag grid

The next consumer starts at `C1:2927`.
This one finally answers what one major downstream use of the pass-27 bounds outputs is.

### Nibble-scale tile bounds

The routine converts:

- `975A`
- `9765`
- `9770`
- `977B`

into tile-space values by shifting right four times.
So the bounds are being projected into a coarse cell grid.

It then builds a cell index of the form:

- `row * 16 + column`

using the shifted min/max values.
That gives a very strong practical read:

- the scanned grid is **16 cells wide**
- the function is scanning a **cell rectangle covered by the object's bounds**

### Cell-flag checks

For each cell, it reads from `7BFD,Y` and tests flag bits.
The hard behavior is:

- bit `0x40` is always treated as a blocking/hit condition
- bit `0x80` is conditionally treated as blocking depending on `9875`

So `9875` is a real collision-test mode/state byte, even if its final high-level name is still open.

### Return behavior

If the scan finds no blocking cell, it returns `0`.
If it finds a blocking cell, it returns `0xFF` (`TDC` then `DEC A`).

So this is a real **bounds-vs-cell-flags collision test**, not just an occupancy query.

### Best-fit names

- `C1:2927 = Test_ObjectBounds_Against_LocalCollisionFlagGrid16x16`
- `7E:7BFD = LocalCollisionFlagGrid16x16`
- `7E:9875 = CollisionFlagGrid_TestMode`

The first two are strong.
The third is intentionally conservative: it names the role without pretending we already know the exact gameplay meaning of the mode switch.

## What this does and does not tell us about the unresolved `F600` tail banks

## What it **does** tell us

It gives a much cleaner downstream picture for the geometry side of the `97xx` block:

- pass 27 showed where the bounds are built
- pass 28 shows those bounds are immediately used for:
  - **object-object overlap classification**
  - **object-vs-cell-flag collision testing**

So the `97xx` region is unquestionably part of a real spatial/collision layer, not just generic scratch state.

## What it **does not** tell us yet

These two routines still do **not** directly consume:

- `970B..9712`
- `9716..971D`
- `9721..9728`
- `972C..9733`

So the honest state is still:

- the unresolved extended-slot banks live next to confirmed geometry/control data
- but these particular bounds consumers do not yet expose their exact meaning

## Best-fit labels after this pass

These are the labels I am comfortable assigning now:

- `C1:28AD = Scan_ActiveObjectBoundsOverlap_ClassifyHit`
- `C1:2927 = Test_ObjectBounds_Against_LocalCollisionFlagGrid16x16`
- `7E:7BFD = LocalCollisionFlagGrid16x16`
- `7E:9875 = CollisionFlagGrid_TestMode`

## Honest limits

Still unresolved after this pass:

- the exact gameplay meaning of the `0x80` vs `0x81` overlap classification
- the exact meaning of `9875` beyond toggling whether bit `0x80` cells count as blocking
- any direct consumer that ties the bounds path back into the copied `F605..F608` banks

## Practical takeaway

Pass 27 established the bounds builder.
Pass 28 establishes the first two real downstream uses of those bounds:

1. **rectangle-overlap classification against active objects**
2. **coarse-grid collision testing against a 16x16 local cell-flag map**

That is a real step forward because it turns the `97xx` geometry block into an actual spatial/collision subsystem slice, even though the extended-slot tail banks are still not directly named.

The clean next move is to find the code that *feeds* or *reacts to* the `0x80/0x81` overlap-class return, because that is the likeliest place the unresolved extended-slot parameters and the confirmed geometry layer finally meet.
