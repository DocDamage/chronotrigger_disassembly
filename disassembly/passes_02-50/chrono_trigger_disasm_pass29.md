# Chrono Trigger Disassembly — Pass 29

This pass stayed on the exact thread left open in pass 28, but the useful breakthrough came one layer up:

- the first bounds consumers were already confirmed
- the better question was what *query / decision system* those consumers feed
- tracing that path exposed a compact mode-dispatch block around `C1:2986..2D81`

This pass also fixes an address-alignment mistake from pass 28.

## Address correction from pass 28

While tracing real call flow, I found that the previously named routine starts were off by a few bytes because they were picked from the middle of trailing instructions.

The corrected starts are:

- `C1:28B0 = Scan_ActiveObjectBoundsOverlap_ClassifyHit`
- `C1:2926 = Test_ObjectBounds_Against_LocalCollisionFlagGrid16x16`

The behavioral read from pass 28 still holds. The correction is the entry addresses.

## High-confidence findings

## `C1:2986` is a relation/query workspace seeder plus mode dispatcher

The routine at `C1:2986` does three concrete things:

1. loads `7E:986F` and `7E:9870` as slot indices
2. snapshots the live slot positions from `1D0C/1D23` into the projected-work arrays at `A039/A050`
3. clears `9872`, then dispatches through an indexed-indirect jump table using `986E`

The dispatch is:

- `LDA 986E`
- `ASL A`
- `TAX`
- `JSR ($2D81,X)`

That makes `986E` a real **query mode selector**.

### Best-fit names

- `C1:2986 = Prepare_RelationQueryWorkspace_AndDispatch`
- `7E:986E = RelationQueryMode`
- `7E:986F = RelationQuery_SubjectSlot`
- `7E:9870 = RelationQuery_ArgSlotA`
- `7E:9871 = RelationQuery_ArgSlotB`
- `7E:9872 = RelationQuery_FlagResult`
- `7E:9873 = RelationQuery_ValueResult`

## `C1:2D81` is a 14-entry relation-query mode jump table

The table at `C1:2D81` resolves cleanly to these entry points:

- `29B2`
- `29FB`
- `2A43`
- `2A98`
- `2B37`
- `2BBC`
- `2BDA`
- `2BEE`
- `2C02`
- `2CA7`
- `2CBA`
- `2CCD`
- `2CE0`
- `2CF3`

So this is not general script flow. It is a compact **mode-dispatched relation / proximity / predicate subsystem**.

### Best-fit name

- `C1:2D81 = RelationQueryModeJumpTable`

## `C1:2B37` computes a squared-distance metric using projected positions

This routine turned out to be much better than a generic “distance” guess.

It uses the projected position work arrays:

- `A039` for one axis
- `A050` for the other axis

It computes absolute deltas between:

- `RelationQuery_SubjectSlot`
- `RelationQuery_ArgSlotA`

Then it squares both deltas by calling the helper at `C1:0089`, which is a real 8-bit hardware multiply wrapper over `$4202/$4203 -> $4216`.

The two squared deltas are added, so the metric is:

- `dx^2 + dy^2`

It then compares that metric against `9893` and writes the sign-style result to `9872`.

So this is not Manhattan distance and not a vague proximity bucket.
It is a real **squared Euclidean distance test**.

### Best-fit names

- `C1:2B37 = EvaluateSquaredDistance_SubjectVsArgA`
- `7E:9893 = RelationQuery_SquaredDistanceThreshold`

## `C1:29B2 / 29FB / 2A43 / 2A98` are nearest/farthest search modes over fixed slot ranges

These four routines all loop candidate slot indices, gate them through the active/valid checks, call `2B37`, and keep either the minimum or maximum metric.

The range splits are explicit in code:

- `29B2` scans `0..2`
- `29FB` scans `0..2`
- `2A43` scans `3..0A`, excluding the subject slot
- `2A98` scans `3..0A`, excluding the subject slot

The compare direction shows which routines are keeping the minimum versus maximum metric.

### Best-fit names

- `C1:29B2 = FindNearestActiveSlot_Range00to02`
- `C1:29FB = FindFarthestActiveSlot_Range00to02`
- `C1:2A43 = FindNearestActiveSlot_Range03to0A_ExcludeSubject`
- `C1:2A98 = FindFarthestActiveSlot_Range03to0A_ExcludeSubject`

These routines store the chosen slot index into `9873`.

That matters because it proves `9873` is **not always a boolean-style output**.

## `9873` is mode-dependent output, not a universal “selected slot” register

The clean proof is `C1:2CF3`.

That routine does **not** return a slot index.
Instead, it computes:

- the squared-distance from the subject slot to `ArgSlotA`
- the squared-distance from the subject slot to `ArgSlotB`
- the absolute difference between those two metrics
- an 8-bit compressed value derived from that difference

It stores that numeric result into `9873`.

So `9873` must be treated as a **mode-dependent value/result register**.
Some modes write slot indices there.
Other modes write a numeric comparison result.

### Best-fit name

- `C1:2CF3 = ComputeAbsDiff_BetweenSubjectToArgA_AndSubjectToArgB_DistanceMetric`

## `2AE3..2B30` are preset-wrapper entry points into the common squared-distance test

A useful structural detail showed up while decoding `2C02`:

the small routines at

- `2AE3`
- `2AEE`
- `2AF9`
- `2B04`
- `2B0F`
- `2B1A`
- `2B25`
- `2B30`

are not dead setup stubs.

They load canned values into `9893` and `9894`, then branch into the common path at `2B40`, which is the body of the squared-distance evaluator.

So the relation-query subsystem includes **preset threshold/mode wrappers** around the common distance test.

What is still open is the exact role of `9894`.
This pass confirms it is part of the preset package, but not how later code interprets it.

## What this pass does and does not prove

## What it **does** prove

- there is a real relation-query dispatcher centered at `C1:2986`
- `986E` is a true mode selector
- `2B37` is a true squared-distance test using projected positions
- four dispatch modes are nearest/farthest searches over explicit slot ranges
- `9873` is mode-dependent output, not a fixed semantic register
- the pass-28 bounds routines had correct behavior but slightly wrong entry addresses

## What it **does not** prove yet

- the exact gameplay meaning of the two slot ranges `0..2` versus `3..0A`
- the exact semantic meaning of `9894`
- the full high-level name of mode `2C02`, even though it is clearly a projected-move / query path and not a trivial compare

## Best next target

The best next move is tracing **who loads `986E / 986F / 9870 / 9871`** before `C1:2986` runs.

That should finally tell us whether this relation-query block is being used by:

- NPC / object AI
- event / map actor logic
- movement validation
- or a shared gameplay predicate layer used by several systems
