# Next Session Start Here

Latest completed pass: **99**

## What pass 99 actually closed
Pass 99 stayed on the pass-98 seam around `D1:EBDF..EC26`, but the useful closure widened a bit.

The strongest keepable results are:

- `D1:EA01..EA20` now gives `CDC9` an exact local meaning
  - it scans `D0:FBE2` against the first materialized 14-word window at `20A2..20BD`
  - it stores the first matching word index to `CDC9`
  - if no match exists across the 14-word span, it stores `0`

- `D1:EA21..EA4A` is now exact
  - three 14-entry circular phase-offset tables:
    - base
    - `+4`
    - `+10`

- `D1:EB00..EB1C` is now exact
  - decrements `CE0D`
  - clears `CE0A` when the cooldown expires
  - duplicates `CDCC..CDE7` into `CDE8..CE03`

- `D1:EB1D..EB4B` is now exact enough to keep
  - uses `CDC9` plus the three phase tables
  - runs the result through `EBD0` for direct vs reversed selection via `CE10`
  - materializes three 14-word windows into `20A2/22A2` at `Y = 0x0000`, `0x0020`, `0x0040`

- `D1:EBDF..EBFF` is now exact
  - copies one 14-word window from the doubled profile ring `CDCC..CE03`
  - mirrors it into both `20A2+Y` and `22A2+Y`

## What this means semantically
The honest static picture is now:

- `CDC9` is no longer anonymous; it is a real local phase/match index byte
- `CDCC..CDE7` is not just a rebuilt 14-word buffer anymore; it is the head half of a doubled 28-word sliding source once `CDE8..CE03` is populated
- the post-controller D1 tail is now a real **three-window phase materialization path** into the promoted paired bands rooted at `20A0` and `22A0`

So the seam is materially cleaner than it was at the end of pass 98.

## Best next seam
Do **not** waste time re-proving `EBDF` or `CDC9`.

The cleanest next static move is:

1. stay in the same D1 neighborhood
   - decode **`D1:EA5F..EAF4`** next

2. specifically freeze:
   - the in-place active-profile convergence loop over `CDCC..CDE7`
   - how it uses the `D0:FBE2/FBE3` source bytes and the mask groups
   - whether it directly drives the materialized-window path or only feeds it indirectly

3. keep `D1:EB4C..EB6F` as caution until that is done
   - it still looks like a real executed prelude
   - but it still leaves no obvious persistent state before falling into the pass-98 `CE0E` selector rebuild

## Completion estimate after pass 99
Conservative project completion estimate: **~68.2%**

Still true:
- semantic/control coverage is ahead of byte-accurate rebuild readiness
- the expensive endgame is still bank separation, decompressor/data grammar work, runtime-backed WRAM proof, source lift, and rebuild validation
