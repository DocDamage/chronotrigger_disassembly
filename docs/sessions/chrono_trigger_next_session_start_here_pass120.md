# Chrono Trigger — Next Session Start Here (Pass 120)

## What pass 120 actually closed

Pass 120 stayed on the corrected same-bank caller seam and froze several real helper/packet/fill/export routines behind the settlement/search subsystem.

### Exact new closures now frozen

- `C2:9DAF..C2:9E75`
  - exact settlement-tail-driven dual-`EF05` materializer
  - exact 12-step signed ramp writer into `5D42..5D58`
  - exact mirrored fill/finalizer tail

- `C2:9E76..C2:9EAF`
  - exact three-block dual-page `EC93` emitter over `2E84 + n*0180`

- `C2:9EB0..C2:9ECC`
  - exact paired-page `EC93` submit helper for `61` and `61 + 1000`

- `C2:A051..C2:A0E6`
  - exact clamp/bootstrap wrapper for the corrected settlement/materializer caller family
  - owns the dual `5D42/5DC2` propagated fills before the `A1B2/A22F` chain and masked strip export

- `C2:A0E7..C2:A0F6`
  - exact masked strip exporter from `9480 + 51` to caller destination `Y`

- `C2:A970..C2:AA05`
  - exact decrement-by-6 fill updater for the `5CC2/5D42` family
  - exact WRAM `$2180` stream writer rooted at `7E:969A`

- `C2:AA19..C2:AA30`
  - exact `$2180` triplet emitter with split negative-value path

- `C2:AFED..C2:B044`
  - exact three-row settlement packet loop with the `B045` word table and `0D5D` gate

- `C2:BA2F..C2:BA4E`
  - exact BA-side post-compare gate writing `0D5E` and emitting `ED31` selector `C01F`

- `C2:BA4F..C2:BAFB`
  - exact capped iterative settlement loop with `BAFC/BA2F` tails
  - exact hardware-math finalizer seeding `0D92/0D94/0D95/0DDB`

- `C2:BAFC..C2:BB19`
  - exact selector packet row builder using `BB1A + 22`

- `C2:BEE6..C2:BF2E`
  - exact settlement row packet loop behind the handoff target `BEEF`
  - uses `BF2F + 2*71` plus inline threshold compare against `9A93`

- `C2:BFD4..C2:BFFE`
  - exact selector-indexed indirect dispatch wrapper
  - latches `54 -> 0417`, runs one jump-table-selected worker, then fans into `C4BC/C3E4/FBE3`

---

## What **not** to reopen

Do **not** reopen the bank bug. The corrected owner band is still:

- `C2:8820..C2:991F`

Do **not** backslide into treating raw absolute `JSR $8820` hits in other banks as proof of cross-bank callers.

Also do **not** reopen these pass-120 closures as vague “generic helpers”:

- `C2:9DAF..9E75`
- `C2:9E76..9ECC`
- `C2:A051..A0F6`
- `C2:A970..AA05`
- `C2:AFED..B044`
- `C2:BA2F..BB19`
- `C2:BEE6..BF2E`
- `C2:BFD4..BFFE`

---

## The real next seam now

The best next targets are now:

1. broader unresolved caller/table family:
   - `C2:A886..AA30`
   - especially the top-level noun and the worker/table ownership around `A970/AA19`

2. post-`AFED` table/helper family:
   - `C2:B04C..B05D`
   - exact table/helper ownership behind the three-row settlement packet loop

3. post-`BEE6` table/worker family:
   - `C2:BF2F..BFFF`
   - exact table extent and the jump-table-selected workers behind `BFD4`

4. strengthened WRAM noun hunt:
   - `7E:0DAB`
   - `7E:0D24`
   - `7E:0D5E`
   - `7E:0FC4`

---

## Important carry-forward wording

Carry these exact readings forward:

- `C2:9DAF..C2:9E75` = exact settlement-tail-driven dual-`EF05` materializer with 12-step signed ramp writer and mirrored fill finalizer
- `C2:9E76..C2:9EAF` = exact three-block dual-page `EC93` emitter over `2E84 + n*0180`
- `C2:9EB0..C2:9ECC` = exact paired-page `EC93` submit helper for `61` and `61 + 1000`
- `C2:A051..C2:A0E6` = exact clamp/bootstrap wrapper for the corrected settlement/materializer caller family
- `C2:A0E7..C2:A0F6` = exact masked strip exporter from `9480 + 51` to destination `Y`
- `C2:A970..C2:AA05` = exact decrement-by-6 fill updater plus WRAM `$2180` stream writer for the `5CC2/5D42` family
- `C2:AFED..C2:B044` = exact three-row settlement packet loop with the `B045` word table and `0D5D` gate
- `C2:BA2F..C2:BA4E` = exact BA-side post-compare gate writing `0D5E` and emitting `ED31` selector `C01F`
- `C2:BA4F..C2:BAFB` = exact capped iterative settlement loop with `BAFC/BA2F` tails and hardware-math finalizer
- `C2:BAFC..C2:BB19` = exact selector packet row builder using `BB1A + 22`
- `C2:BEE6..C2:BF2E` = exact settlement row packet loop with inline threshold compare and the `BF2F` word table
- `C2:BFD4..C2:BFFE` = exact selector-indexed indirect dispatch wrapper latching `54 -> 0417` before the fixed `C4BC/C3E4/FBE3` tail
