# Chrono Trigger Disassembly — Pass 72

## Scope of this pass
This pass continues directly from the pass-71 seam.

Pass 71 closed promoted global `70..7D` and explicitly left the next clean seam as:

- global `90..A9`

This pass re-opened that late promoted selector-control band from the real master-table bytes and split it into three useful buckets:

1. **lane-derived timed-state updaters**
   - `90`
   - `92`
   - `93`
   - `94`
   - `95`
   - `9A`
2. **lane-derived helper/seed gates**
   - `91`
   - `98`
   - `99`
3. **internal alias entries into the late-pack executor blob**
   - `9D..A9`

The most important correction is this:

> the toolkit's old late-band framing overstated `A0` as a clean standalone top-level entry.
> Direct byte re-open shows the dispatch pointer lands **inside** the late-pack blob, not at its true initializer.
>
> So `9D..A9` should be carried as **internal alias entries**, not as independent clean top-level command bodies.

That is a real architectural correction, not just wording cleanup.

---

## 1. Globals `90`, `92`, `93`, `94`, `95`, and `9A` are one lane-derived timed-state family
These six bodies all share the same skeleton:

1. choose a lane source byte
   - either a specific `B179/B17B/B17C/B17D/B17E` source byte
   - or fallback `AEC7` when that source byte is zero
2. subtract `1`
3. map through the ranking byte stream at `B163`
4. treat the resulting value as a **lane ID**
5. derive the lane-block WRAM base as `lane * 0x80`
6. set a per-lane scratch/active flag
7. copy one lane work byte into a mirrored scratch byte
8. clear selected bits from `B186`
9. decrement a per-lane countdown byte
10. when the countdown hits zero:
    - reload it to `0x0A`
    - optionally clear one lane-block flag bit
    - clear the matching per-lane scratch/active flag

The lane-block proof is now direct.
The family computes `X = lane * 0x80` through:

```text
TYA
REP #$20
XBA
LSR A
TAX
```

With a zero high byte, that transforms lane `n` into `n << 7`.
That is exactly the stride used by the `5E4A/5E4B/5E4D/5E4E/...` lane blocks already established in the service-7 work.

So the safe structural read is:

> this band is maintaining **timed lane-state scratch/active flags** with optional lane-block bit release on expiry.

### Global `90` (`C1:8876`)
What it does:

- uses `B179[0]`, or `AEC7` if that byte is zero
- maps through `B163`
- sets `AFB6[lane] = 1`
- copies `B0D4[lane] -> AF27[lane]`
- clears high bits from `B186` with `AND #$0FFF`
- decrements `B045[lane]`
- on expiry:
  - reloads `B045[lane] = 0x0A`
  - clears `5E4B + lane*0x80` bit `0x80`
  - clears `AFB6[lane]`

Strongest safe reading:

> **global `90` updates `AFB6/B045` for a mapped lane and releases `5E4B.bit7` when the countdown expires**

### Global `92` (`C1:8975`)
What it does:

- uses `B17B`, or `AEC7` if zero
- maps through `B163`
- sets `AFCC[lane] = 1`
- copies `B0EA[lane] -> AF3D[lane]`
- clears `B186` with `AND #$1BFF`
- decrements `B05B[lane]`
- on expiry:
  - reloads `B05B[lane] = 0x0A`
  - clears `AFCC[lane]`

Strongest safe reading:

> **global `92` updates `AFCC/B05B` for a mapped lane and clears the active flag on expiry**

### Global `93` (`C1:89B9`)
What it does:

- uses `B17C`, or `AEC7` if zero
- maps through `B163`
- sets `AFD7[lane] = 1`
- copies `B0F5[lane] -> AF48[lane]`
- clears `B186` with `AND #$1DFF`
- decrements `B066[lane]`
- on expiry:
  - reloads `B066[lane] = 0x0A`
  - clears `5E4D + lane*0x80` bit `0x80`
  - clears `AFD7[lane]`

Strongest safe reading:

> **global `93` updates `AFD7/B066` for a mapped lane and releases `5E4D.bit7` on expiry**

### Global `94` (`C1:8A05`)
What it does:

- uses `B17D`, or `AEC7` if zero
- maps through `B163`
- sets `AFE2[lane] = 1`
- copies `B100[lane] -> AF53[lane]`
- clears `B186` with `AND #$1EFF`
- decrements `B071[lane]`
- on expiry:
  - reloads `B071[lane] = 0x0A`
  - clears `5E4D + lane*0x80` bit `0x40`
  - clears `AFE2[lane]`

Strongest safe reading:

> **global `94` updates `AFE2/B071` for a mapped lane and releases `5E4D.bit6` on expiry**

### Global `95` (`C1:8A51`)
What it does:

- uses `B17E`, or `AEC7` if zero
- maps through `B163`
- sets `AFED[lane] = 1`
- copies `B10B[lane] -> AF5E[lane]`
- clears `B186` with `AND #$1F7F`
- decrements `B07C[lane]`
- on expiry:
  - reloads `B07C[lane] = 0x0A`
  - clears `5E4E + lane*0x80` bit `0x40`
  - clears `AFED[lane]`

Strongest safe reading:

> **global `95` updates `AFED/B07C` for a mapped lane and releases `5E4E.bit6` on expiry**

### Global `9A` (`C1:8BB9`)
What it does:

- uses `B179[0x0A]`, or `AEC7` if zero
- maps through `B163`
- sets `B024[lane] = 1`
- copies `B142[lane] -> AF95[lane]`
- clears `B186` with `AND #$1FFB`
- decrements `B0B3[lane]`
- on expiry:
  - reloads `B0B3[lane] = 0x0A`
  - clears `5E4E + lane*0x80` bit `0x04`
  - clears `B024[lane]`

Strongest safe reading:

> **global `9A` updates `B024/B0B3` for a mapped lane and releases `5E4E.bit2` on expiry**

---

## 2. Global `91` is the lane-gated `AFC1/AF32` setup path with geometry seeding
Handler body: `C1:88C5..C1:8974`

This entry starts from the same lane-mapping front-end as the timed family, but it diverges into a more complex helper path.

What it does:

- uses `B179[1]`, or `AEC7` if zero
- maps through `B163`
- computes the lane-block base as `lane * 0x80`
- refuses the helper path unless:
  - `5E4A + lane*0x80` has bit `0x80` set
  - `5E4B + lane*0x80` has bit `0x40` clear
- when both conditions pass:
  - sets `AFC1[lane] = 1`
  - computes `AF32[lane] = B0DF[lane] + 5E64[lane_block]`
  - seeds geometry scratch through `5E32/5E33/5E64` and `JSR C92A`
  - stores results into `AD9C[0E]`
  - stores mode byte `AD9E[0E] = 3`
  - clears `B202`
  - runs `JSR EBF8`
- whether gated or not, it clears `B186` with `AND #$17FF` before returning

Strongest safe reading:

> **global `91` conditionally seeds `AFC1/AF32` and `AD9C/AD9E` from lane geometry when `5E4A.bit7` is set and `5E4B.bit6` is clear**

Important caution:
The precise gameplay-facing noun of the `AD9C/AD9E/EBF8` helper chain is still open.
This pass only freezes the lane gating and state-seeding mechanics.

---

## 3. Globals `98` and `99` are lane-derived helper/seed gates, not plain timer clearers
### Global `98` (`C1:8A9F`)
What it does:

- uses `B179[8]`, or `AEC7` if zero
- maps through `B163`
- computes `lane * 0x80`
- sets `B00E[lane] = 1`
- copies `B12C[lane] -> AF7F[lane]`
- conditionally transforms that copied byte:
  - if `(5E4D | 5E52)` has bit `0x80`, halve it
  - if `5E4B` has bit `0x20`, double it
- clears `B186` with `AND #$1FEF`
- if `5E4B` bit `0x10` is set:
  - seeds `AD89 = 1`
  - mirrors `AD98 -> B1FD`
  - clears `B202`
  - runs `JSR EBF8`
  - runs `JSR EC7F`

Strongest safe reading:

> **global `98` captures a lane-derived `B12C` variant into `AF7F`, applies status-based scale adjustments, and optionally runs the `EBF8 -> EC7F` helper chain when `5E4B.bit4` is set**

### Global `99` (`C1:8B10`)
What it does:

- uses `B179[9]`, or `AEC7` if zero
- maps through `B163`
- computes `lane * 0x80`
- sets `B019[lane] = 1`
- copies `B137[lane] -> AF8A[lane]`
- conditionally transforms that copied byte:
  - if `(5E4D | 5E52)` has bit `0x80`, halve it
  - if `5E4B` has bit `0x20`, double it
- clears `B186` with `AND #$1FF7`
- decrements `B0A8[lane]`
- when the countdown expires:
  - reloads `B0A8[lane] = 0x0A`
  - aborts if `5E4A.bit7` is set
  - otherwise requires `(5E4E | 5E53)` bit `0x20`
  - then seeds:
    - `AD89 = 5`
    - `AD9E[0E] = 2`
    - `B202 = 0xC0`
  - runs the same geometry/helper chain used by the entry

Strongest safe reading:

> **global `99` updates `B019/B0A8` for a mapped lane and, on expiry, conditionally seeds `AD9C/AD9E` through a helper path gated by `5E4A` and `5E4E|5E53` lane flags**

Again, the exact human-facing noun of the helper chain is still open, but the gating and state writes are now solid.

---

## 4. Globals `96`, `97`, and `9B` are exact `RTS` aliases
Direct bytes:

```text
C1:8A9D  60
C1:8A9E  60
C1:8C08  60
```

So these entries are not deferred helpers and not hidden mutators.
They are exact no-op returns.

Strongest safe reading:

- global `96` = exact `RTS`
- global `97` = exact `RTS`
- global `9B` = exact `RTS`

---

## 5. Global `9C` stays open, but it is clearly a large lane/service controller and not a tiny wrapper
Handler entry: `C1:8461`

This entry is large and materially different from the small timed-state family.
What is already clear from the direct bytes:

- it clears controller scratch like `B2C0` and `B3B9`
- it iterates lane-related state through the `B179/B163` mapping again
- it checks occupancy and active/readiness bytes like `AEFF`, `AFAB`, `B247`, and lane-block bytes in `5E0A`
- it calls into the already-labeled service/readiness helpers, including:
  - `C1:8CF9`
  - `C1:BD6F` (`ct_c1_apply_status_modifiers_to_lane_time_increment`)
  - `C1:B575` (`ct_c1_service7_reconcile_canonical_record_lane_pairs`)
  - `C1:B725` (`ct_c1_init_lane_active_time_gauge_exports`)
- it also writes readiness/active-time style state such as `B03A`

That is enough to state one thing safely:

> global `9C` is a **real lane/service controller** in the service-7 / active-time / canonical-lane neighborhood, not a trivial selector wrapper.

But this pass does **not** claim a final one-line gameplay noun for it yet.
So `9C` should stay explicitly unresolved while the rest of the band is promoted.

---

## 6. Globals `9D..A9` are internal alias entries into the late-pack executor blob
This is the biggest correction in the pass.

The master table really does point here:

```text
9D -> C1:AFB6
9E -> C1:AFC1
9F -> C1:AFCC
A0 -> C1:AFD7
A1 -> C1:AFE2
A2 -> C1:AFED
A3 -> C1:AFF8
A4 -> C1:B003
A5 -> C1:B00E
A6 -> C1:B019
A7 -> C1:B024
A8 -> C1:B02F
A9 -> C1:B03A
```

But when reopened against the live bytes, these are **not** clean standalone bodies.
Several of them land in the middle of surrounding instructions.

Examples:

- `A0 -> AFD7` lands **two bytes inside** the true `LDA.l CC:8B08,X` pointer-load sequence, whose executable start is at `AFD5`
- `A1 -> AFE2` lands inside the `STA $0A` / `SEP #$20` transition into the common path
- `A2 -> AFED` lands inside the `CMP #$FE` test / second-sub-op arming logic
- `A4`, `A8`, and `A9` also land inside already-running executor logic rather than at clean prologues

So the strongest safe correction is:

> globals `9D..A9` are **internal late-pack helper / continuation aliases** inside the blob `C1:AFB6..C1:B08E`.
>
> They should not be described as independent clean top-level opcode bodies.

### Safe structural split inside that alias band
Even without overclaiming more than the bytes allow, the band now splits usefully:

- `9D..9F`
  - helper/return aliases in the `AFB6..AFD1` lead-in
- `A0..A6`
  - continuation aliases inside the late-pack executor common path
  - pointer/segment selection, current-op fetch, and optional chained second-op dispatch
- `A7..A9`
  - continuation aliases inside the result-capture / nonzero-result tail

### Important correction to earlier toolkit wording
The old wording that treated `A0` as the clean top-level late-pack executor entry should be retired.
The real executable top of that blob is earlier than the master-table pointer.
So `A0` belongs in the alias bucket with the rest of `9D..A9`.

---

## Net result of pass 72
This pass materially improves the late promoted master range.

What is now strong:

- `90`, `92`, `93`, `94`, `95`, `9A` = lane-derived timed-state updaters
- `91`, `98`, `99` = lane-derived helper/seed gates
- `96`, `97`, `9B` = exact `RTS` aliases
- `9D..A9` = internal aliases into the late-pack executor blob, **not** clean standalone top-level bodies

What stays explicitly open:

- `9C`
- the final gameplay-facing noun behind the `AD9C/AD9E/EBF8/EC7F` helper chains used by `91`, `98`, and `99`

That is still real progress because it closes most of `90..A9` while also correcting one stale assumption in the toolkit.

---

## Suggested next seam
The next clean continuation point is now:

1. fully decode `9C -> C1:8461`
2. then re-open the helper chain used by:
   - `91`
   - `98`
   - `99`
3. especially:
   - `C1:E89F`
   - `C1:EBF8`
   - `C1:EC7F`
   - `C1:8CF9`

That should finally convert the late `90..99` band from purely structural labels into firmer gameplay-facing names.
