# Chrono Trigger Disassembly — Pass 117

## Purpose

Pass 116 froze the mirrored eight-body candidate-search family at `C0:8AB5..916F`, but the owning solver entry was still just a seam list.

This pass stayed on that exact seam and only promoted what the bytes justify.

---

## Biggest closure

The band at `C0:8820..991F` is no longer a loose cluster around the search family.

It is now closed structurally as one **DP=`$1D00` current-slot candidate-offset settlement pipeline**:

1. copy / seed the working offset pair
2. optionally refine it through the already-closed search family
3. gate the resulting signed components against current-slot axis bounds
4. quantize / zero out-of-range components at nibble scale
5. expand those components into six signed lane accumulators
6. propagate those lane bytes into phase / coarse-cell state plus wrap-flag fanout

That is the first honest closure for the whole enclosing solver entry without bluffing the final gameplay noun.

---

## 1. `C0:8820..8857` is the exact DP-scoped enclosing pipeline entry over the current slot

Byte shape:

```text
C0:8820  8D EB 01
C0:8823  0B
C0:8824  C2 20
C0:8826  A9 00 1D
C0:8829  5B
C0:882A  E2 20
C0:882C  20 E5 88
C0:882F  64 2C
C0:8831  64 2D
C0:8833  AD 62 01
C0:8836  D0 08
C0:8838  AD 1F 01
C0:883B  F0 03
C0:883D  20 EE 88
C0:8840  AD 20 01
C0:8843  F0 07
C0:8845  E2 10
C0:8847  20 6D 8A
C0:884A  C2 10
C0:884C  20 75 91
C0:884F  20 DE 99
C0:8852  20 AC 91
C0:8855  20 E1 93
C0:8858  2B
C0:8859  60
```

Exact structural behavior now frozen:

- writes `01EB`
- `PHD`
- sets `D = $1D00`
- `JSR 88E5`:
  - exact already-closed copy:
  - `2A -> 2E`
  - `2B -> 30`
- clears local `2C` and `2D`
- if either:
  - `0162 != 0`
  - or `011F != 0`
  - then runs the already-closed step-template writer at `88EE`
- if `0120 != 0`, runs the already-closed sign/zero dispatcher at `8A6D`
- then runs the exact downstream sequence:
  - `9175`
  - `99DE`
  - `91AC`
  - `93E1`
- restores `D`
- returns

Strongest safe reading:

> **`C0:8820..8857` is the exact DP=`$1D00` enclosing current-slot candidate-offset settlement pipeline, owning the already-closed `2A/2B -> 2E/30` seed, optional template/search refinement, bound-gating, nibble quantization, six-lane expansion, and later phase/cell propagation.**

I am still intentionally **not** freezing the final gameplay-facing noun of the whole subsystem yet.

---

## 2. `C0:9175..91AB` is the exact initial axis-bound acceptance gate for `2E/30` into `32/33`

This band is now strong enough to promote.

Exact shape:

- clears local `32` and `33`
- uses current slot index `0197`
- tests signed `2E`
  - negative path calls `5B86`
  - nonnegative path calls `5B79`
- only copies `2E -> 32` when the chosen helper accepts
- tests signed `30`
  - negative path calls `5B71`
  - nonnegative path calls `5B63`
- only copies `30 -> 33` when the chosen helper accepts

The exact helper bodies at `5B63 / 5B71 / 5B79 / 5B86` show that these are simple compare/return helpers against current-slot coordinate-side limit words around `1801,X / 1881,X` and local bound bytes `1A..1D`.

So the strongest safe reading is now:

> **`C0:9175..91AB` is the exact initial axis-bound acceptance gate that only copies in-range signed candidate components `2E/30` into accepted locals `32/33`.**

This is intentionally stronger than “misc setup,” but still avoids a fake gameplay noun.

---

## 3. `C0:99DE..9A1E` is the exact signed-component nibble-quantizer / out-of-range zeroer for `2E/30`

This band is now much tighter than in pass 116.

Exact behavior:

- if `2E != 0`:
  - takes sign
  - converts to magnitude
  - divides by `0x10` via four `LSR`
  - calls:
    - `9A60` for nonnegative `2E`
    - `9A7E` for negative `2E`
  - if the chosen helper rejects, it clears `2E`
- if `30 != 0`:
  - same structure
  - calls:
    - `9A1F` for nonnegative `30`
    - `9A3D` for negative `30`
  - if the chosen helper rejects, it clears `30`

That is now enough to promote the band structurally:

> **`C0:99DE..9A1E` is the exact signed candidate-component nibble-quantizer and out-of-range zeroer for the later working pair `2E/30`, using sign-specific positive/negative bound helpers.**

I am intentionally **not** overclaiming the exact world-space noun of those bound helpers yet.

---

## 4. `C0:91AC..93E0` is the exact six-lane signed accumulator builder and nibble splitter

This band is the biggest downstream closure in this pass.

### A. front gate / fallback sign seed

Exact proven front behavior:

- if local `00 == 0`, it skips the fallback compare lane
- otherwise:
  - compares `02` against `0A`
  - writes `2E = +0x10` or `2E = -0x10` when unequal
  - if equal and `87.low_nibble == 0`, sets local `01.bit0`
  - compares `03` against `0E`
  - writes `30 = +0x10` or `30 = -0x10` when unequal
  - if equal and `89.low_nibble == 0`, sets local `01.bit1`
- if both bits become set (`01 == 3`), it forces:
  - `00 = 2`
  - `01 = 0`

### B. optional `0400`-flag-derived bias pair

If `01BC != 0`, the band reads `0400.bit0` and `0400.bit1` and materializes local bias pair `4E/4F` as exact `+0x10 / -0x10 / 0` style axis nudges, with explicit zero suppression when `0A == 0` or `0E == 0`.

### C. exact three-pair accumulator materialization

The band then builds exact signed accumulator pairs:

- `3B / 3C`
- `3D / 3E`
- `3F / 40`

using the working pair `2E/30`, existing lane bytes `24..29`, and optional sibling basis bytes `37..3A`, plus the `4E/4F` bias pair on the relevant paths.

### D. exact high-nibble / low-nibble split

For each of the six resulting signed accumulator bytes `3B..40`, the band:

- extracts the signed high-nibble magnitude into paired locals:
  - `41/42`
  - `43/44`
  - `45/46`
  - `47/48`
  - `49/4A`
  - `4B/4C`
- leaves the signed low-nibble residue back in:
  - `3B..40`

### E. exact decay tail

At the end:

- decrements local `4D` when nonzero
- when it expires, clears exact lane bytes:
  - `24..29`

So the strongest safe reading is now:

> **`C0:91AC..93E0` is the exact six-lane signed accumulator builder and high/low-nibble splitter, with an optional `0400`-flag bias pair and a small decay tail over lane bytes `24..29`.**

---

## 5. `C0:93E1..991F` is the exact six-lane phase / coarse-cell propagation band with wrap-flag fanout

This band is broad, but it is now structurally closed enough to promote as one pipeline stage.

Exact top-level structure:

- clears wrap / crossing flag bytes:
  - `76`
  - `77`
  - `74`
  - `75`
- then runs six lane-updater families over phase-like locals:
  - `93`
  - `96`
  - `94`
  - `97`
  - `95`
  - `98`
- while stepping coarse-cell / coarse-index locals such as:
  - `0A / 0C`
  - `0E / 10`
  - `12 / 14`
  - `16 / 18`
  - and paired locals `87 / 89 / 8B / 8D / 8F / 91`

The exact split is by:

- sign of `0BC9`
- exact bits in local `35`

The repeated updater bodies are now strong enough to characterize honestly:

- they advance or decrement the phase byte
- detect edge crossings at exact thresholds like `0x07 / 0x08 / 0x0F / 0x10 / 0x1F / 0x20`
- set crossing flags in `74..77`
- update the paired coarse-cell / coarse-index byte(s) when those thresholds are crossed

Then the band:

- clears:
  - `78`
  - `79`
  - `7A`
  - `7B`
- and fans the wrap/crossing results into exact downstream helper families at:
  - `97CC..985E`
  - `985F..98F1`
  - `98F2..991F`

which update exact counter/index locals `99..9E`.

That is enough to promote the band structurally:

> **`C0:93E1..991F` is the exact six-lane phase / coarse-cell propagation and wrap-flag fanout stage driven by the signed lane bytes split in `91AC..93E0`.**

I am intentionally avoiding a fake final noun like “pathfinding,” “collision resolution,” or “spawn ring solver” until the caller families are frozen.

---

## 6. What this pass upgrades and what it still does not overclaim

This pass upgrades the enclosing band from “the next seam around the eight-way split” into a closed structural pipeline.

What is now safe to say:

- `8820..8857` is the owner of the whole later candidate-offset settlement pipeline
- `9175..91AB` is the initial in-range acceptance gate for `2E/30`
- `99DE..9A1E` is the nibble-quantizer / zeroer for those signed components
- `91AC..93E0` expands that pair into six signed lane accumulators and splits coarse/fine nibble pieces
- `93E1..991F` propagates those lane bytes through phase/coarse-cell state and wrap-flag fanout

What this pass still does **not** overclaim:

- the final gameplay-facing noun of the whole subsystem
- the exact world/object-space noun of the six propagated lanes
- the final player-facing meaning of locals `99..9E`

Those now belong to the caller side, not the internal solver side.

---

## Clean carry-forward wording

Carry this exact wording forward:

- `C0:8820..8857` = exact DP=`$1D00` enclosing current-slot candidate-offset settlement pipeline
- `C0:9175..91AB` = exact initial axis-bound acceptance gate for signed candidate components `2E/30` into `32/33`
- `C0:99DE..9A1E` = exact signed-component nibble-quantizer and out-of-range zeroer for `2E/30`
- `C0:91AC..93E0` = exact six-lane signed accumulator builder and high/low-nibble splitter with optional `0400`-flag bias pair and lane decay tail
- `C0:93E1..991F` = exact six-lane phase / coarse-cell propagation and wrap-flag fanout stage
