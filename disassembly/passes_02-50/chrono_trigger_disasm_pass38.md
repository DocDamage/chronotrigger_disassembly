# Chrono Trigger (USA) — Disassembly Pass 38

## Scope
This pass continues directly from pass 37 and stays on the exact live seam it identified:

- the four real service-7 bodies behind `C1:1FDD`
  - `C1:2332`
  - `C1:23A4`
  - `C1:25A3`
  - `C1:2701`
- the packet bytes they actually consume from `$9604..$9608`
- the post-scan tail at `C1:27AD / C1:27C5`

The goal of this pass was to stop describing service-7 as merely “spatial / coordinate-driven” and to pin the actual geometric family used by each real handler body.

This pass does **not** claim final gameplay/UI names for these queries yet.
It pins the geometry and buffer behavior the bytes actually prove.

---

## Baseline carried forward from pass 37
Pass 37 had already established:

- `C1:0003 / C1:0045` is the local bank-`C1` service dispatcher
- service `#07` lands at `C1:1FDD`
- `C1:1FDD` sub-dispatches via `$99CC` and table `C1:1FEA`
- the 7 submodes collapse to 4 real bodies:
  - `0/4 -> 25A3`
  - `1/2 -> 2701`
  - `3/5 -> 23A4`
  - `6 -> 2332`
- `27D9` / `27E8` are the service-7 result clear/finalize helpers

What remained open was the actual predicate/geometry implemented by each body.

---

## What was done in this pass
1. Fully re-traced `C1:2332` instruction-by-instruction
2. Fully re-traced `C1:2701`, including helpers `C1:011A` and the square table at `CC:FB6F`
3. Fully re-traced `C1:23A4`, including the pre-scan vertex ordering and the three angle-sector tests
4. Re-traced `C1:25A3` far enough to pin its geometric structure and packet-byte roles without overclaiming the final outward gameplay meaning
5. Resolved the common post-scan tail at `C1:27AD / C1:27C5`
6. Strengthened the service-7 packet-byte interpretation, especially `$9604`, `$9605`, `$9606`, `$9607`, and `$9608`

---

## Core results

### 1. `$9604` is a real service-7 candidate partition selector
This is no longer just a generic packet byte for the service-7 family.

Across `2332`, `25A3`, and `2701`, the same structure appears:

```text
LDX #$000B    ; default upper bound / limit
STX $90
LDX #$0003    ; default scan start = 3
STX $8E
LDA $9604
BEQ keep_default
  STX $90     ; upper bound becomes 3
  TDC
  TAX
  STX $8E     ; scan start becomes 0
```

So service-7 handlers do **not** always scan the same slot range.
They all have a packet-driven partition gate:

- `$9604 == 0`  -> scan slots `3..10`
- `$9604 != 0` -> scan slots `0..2`

That is a strong structural result.

Safest reading:

> `$9604` = **service-7 candidate partition selector (first-three slots vs later slots)**

This is stronger than the generic pass-36 “packet byte 0” wording.

---

### 2. `C1:2332` is a seeded half-open band scan on the `$1D23` axis
This routine is now exact enough to rename materially.

Resolved structure:

```text
LDA $9605
TAX
STX $88                    ; seed slot

SEC
LDA $1D23,x
SBC #$20
BCS +
  TDC                      ; clamp low bound to 00h
+
STA $85                    ; low bound

CLC
LDA $1D23,x
ADC #$20
BCC +
  LDA #$FF                 ; clamp high bound to FFh
+
STA $87                    ; high bound

JSR $27D9                  ; clear result vectors
... scan selected partition ...

candidate accepted iff:
  - candidate != seed
  - active/eligibility flags pass
  - low_bound <= $1D23[candidate] < high_bound

accepted candidates -> $99C1+,
seed slot -> $99C0
```

Key upgrades over pass 37:

- the comparison is a **half-open interval**: `[seed-0x20, seed+0x20)`
- the tested axis is specifically `$1D23[...]`
- the scan always seeds the primary slot into `$99C0`
- accepted matches are appended into `$99C1+`
- the scan range itself is partitioned by `$9604`

Safest reading:

> `C1:2332` = **seeded same-axis band scan using `$1D23` with width `0x40`**

The exact real-world axis name of `$1D23` is still open, so the label should stay axis-neutral.

---

### 3. `C1:2701` is a cell-radius scan using squared-distance lookup, not a vague transformed metric
This routine is now far stronger than the pass-37 wording.

#### 3a. `C1:011A` is just a `>>4` cell normalizer
The helper used at the top of `2701` is:

```text
LSR A
LSR A
LSR A
LSR A
RTS
```

So `2701` does **not** compare raw coordinates.
It first normalizes both tested axes into coarse cell-space by dividing by 16.

#### 3b. `CC:FB6F` begins with squares
The lookup table used in the core compare begins:

```text
00 01 04 09 10 19 24 31 40 51 64 79 90 A9 C4 E1 ...
```

That is a square table:

- `0^2 = 0x00`
- `1^2 = 0x01`
- `2^2 = 0x04`
- `3^2 = 0x09`
- ...
- `15^2 = 0xE1`

#### 3c. The routine computes `dx^2 + dy^2` in cell-space and compares it against `$9607`
Resolved core body:

- load seed slot from `$9605`
- normalize seed `$1D0C` and `$1D23` with `>>4`
- for each qualifying candidate in the selected partition:
  - normalize candidate `$1D0C` and `$1D23` with `>>4`
  - compute absolute `dx` and `dy`
  - map both through `CC:FB6F`
  - add them
  - accept candidate iff `(dx^2 + dy^2) < $9607`

So this is no longer just some “delta threshold scan.”
It is explicitly a **coarse cell-radius test using squared distance**.

Safest reading:

> `C1:2701` = **seeded cell-radius scan using `(dx^2 + dy^2) < $9607` in 16-unit cell space**

#### 3d. The seed slot is only preserved if it belongs to the scanned partition
After the loop, `2701` flows into `27AD`.
That tail stores the seed slot from `$92` into `$99C0` **only if** it matches the active partition implied by `$9604`.
If no seed was written, the tail left-compacts `$99C1+` down into `$99C0+`.

So `2701` is not merely “seeded”; it is **partition-aware seeded**.

---

### 4. `C1:23A4` is a three-vertex inclusion scan over slots `0/1/2`
This is the biggest semantic upgrade of the pass.

Pass 37 only knew `23A4` loaded multiple positions and ran geometry/math helpers.
This pass pins the actual structure.

#### 4a. The three vertices are hardcoded from slots `0`, `1`, and `2`
The routine loads:

- slot `0` -> `$80/$81`
- slot `1` -> `$82/$83`
- slot `2` -> `$84/$85`

using `$1D0C` and `$1D23` as the coordinate pair source.

#### 4b. It then orders the three vertices before the scan
The next block is a swap-heavy ordering pass that compares and swaps those three coordinate pairs.
It is not dead code and not a random prelude.
It normalizes the vertex order before edge-angle derivation.

#### 4c. It computes directed edge sectors between all three vertices
After ordering, the routine repeatedly feeds the helper at `0222` with vertex pairs and materializes six angle values:

- `86/87`
- `88/89`
- `8A/8B`

Then it derives wrap flags in:

- `$92`
- `$93`
- `$94`

Each wrap flag records whether an angle interval crosses the circular wrap boundary.

#### 4d. Candidate acceptance requires passing all three angle-sector tests
For each eligible candidate slot, `23A4`:

- computes the candidate angle relative to vertex 0 and checks it against sector `86..87`
- computes the candidate angle relative to vertex 1 and checks it against sector `88..89`
- computes the candidate angle relative to vertex 2 and checks it against sector `8A..8B`
- accepts the candidate only if all three sector tests pass

This is not a generic “geometry scan family.”
It is a genuine **three-vertex inclusion test**.

Safest reading:

> `C1:23A4` = **three-vertex inclusion scan using the slot-0/1/2 coordinate triangle/polygon**

The exact intended gameplay-facing identity of slots `0/1/2` should still stay conservative here.
The bytes do prove that the shape is formed from those three fixed slot coordinates.

#### 4e. Unlike `2332` and `2701`, this path does not preserve a seed slot
`23A4` ends with `JMP $27C5`, not `27AD`.
So it only left-compacts the candidate list if `$99C0` is empty.
It does **not** conditionally inject a seed slot first.

That is a real semantic split inside service-7.

---

### 5. `C1:25A3` is a dual-anchor oriented inclusion scan, and the packet-byte roles are much clearer now
This path is still the least outwardly named family, but it is no longer vague.

#### 5a. `$9605`, `$9606`, `$9607`, and `$9608` all matter directly here
Observed entry behavior:

- `$9605` -> first anchor slot
- `$9606` -> second anchor / preserved-subject slot
- `$9607` -> scaled by `*8` and stored in `$AE`
- `$9608` -> toggles one side of the geometric construction

So this mode family is not just “uses a wider packet.”
It directly consumes the whole slot/range/toggle packet.

#### 5b. `0222` + `01F9` derive an oriented construction from the vector between `$9605` and `$9606`
The routine:

1. loads coordinates for slot `$9605` and slot `$9606`
2. calls `0222` to derive an angle-like direction value in `$DB`
3. calls `01F9` repeatedly with `$DB`, `$DB+0x40`, `$DB+0x80`, and `$DB+0xC0`
4. uses `$AE = ($9607 * 8)` as the magnitude input for those calls

This is a trig/angle-driven oriented construction, not a raw coordinate compare.

#### 5c. The scan builds two wrapped angle windows and requires candidates to pass both
After the construction step, `25A3` materializes two wrapped angle sectors and corresponding wrap flags in `$8C` / `$8D`.
For each candidate it then:

- computes candidate angle from one constructed anchor point and checks the first sector
- computes candidate angle from a second constructed anchor point and checks the second sector
- accepts only if both checks pass

So this is structurally a **dual-anchor oriented inclusion test**, not a simple radius check.

#### 5d. `$9608` toggles whether one side of the construction is anchored from slot `$9605` or slot `$9606`
This is the strongest new structural detail for modes `0/4`.

When `$9608 == 0`, one branch builds the second comparison anchor from the same slot basis as the first.
When `$9608 != 0`, that branch instead uses the other packet slot basis.

That means modes `0/4` are not just aliased for convenience.
They are the same geometric core with a packet-controlled anchor-selection variation.

Safest reading:

> `C1:25A3` = **dual-anchor oriented inclusion scan derived from the `$9605 -> $9606` direction, with extent `($9607 * 8)` and anchor toggle `$9608`**

That is a real improvement over the old “extended spatial metric scan” wording.

---

### 6. `C1:27AD / C1:27C5` is the common service-7 seed-preserve / left-compact tail
This tail was implicit before; it is now explicit.

Resolved behavior:

#### `27AD`
- consult `$9604` to determine which partition is active
- test whether preserved slot `$92` belongs to that partition
- if yes, store `$92 -> $99C0`
- otherwise leave `$99C0` untouched
- then fall into `27C5`

#### `27C5`
- if `$99C0` is already non-negative, return
- otherwise shift `$99C1..` left into `$99C0..`

So the common tail does **not** always preserve a seed.
It conditionally preserves one, then normalizes the result vector if slot 0 is empty.

This explains the behavior split between the service-7 families:

- `2332`, `25A3`, `2701` all use the seed-aware tail
- `23A4` skips the seed-preserve part and goes directly to left-compaction

---

## Resulting upgraded service-7 family picture
After pass 38, the four real service-7 families can be stated much more concretely:

- `2332` = seeded same-axis band scan on `$1D23`
- `23A4` = three-vertex inclusion scan over the fixed slot-`0/1/2` coordinate shape
- `25A3` = dual-anchor oriented inclusion scan derived from the `$9605 -> $9606` vector with extent/toggle packet bytes
- `2701` = seeded 16-unit-cell radius scan using squared distance against `$9607`

That is a major reduction in ambiguity compared with pass 37.

---

## Strongest label implications from this pass
The labels file carries the formal names, but the most important upgrades are:

- `$9604` can now be strengthened from generic packet byte to **service-7 partition selector**
- `2332`, `23A4`, and `2701` all deserve materially stronger geometry-facing labels
- `25A3` should move from vague “extended spatial metric” wording to a **dual-anchor oriented inclusion** label
- `27AD / 27C5` deserve helper labels rather than being treated as anonymous tail bytes

---

## What remains unresolved after pass 38
Still intentionally unresolved:

1. the exact gameplay-facing identity of the slot partitions behind `$9604`
2. the exact outward axis names of `$1D0C` vs `$1D23`
3. the exact human-readable shape name for the `25A3` family
   - the geometry is now strong
   - the final “cone / strip / beam / box” naming still needs one more proof pass
4. the small wrappers around `2029..22F3` that choose and parameterize these service-7 families

---

## Best next continuation point
The best next target is no longer the heavy service-7 bodies themselves.
Those are much cleaner now.

The next real seam is the wrapper layer above them:

- `C1:2029..22F3`

That layer should let us translate the now-solved geometric families into the engine’s actual higher-level selector/use cases.

A secondary continuation point is a dedicated pass on the exact shape semantics of `25A3`, but the wrappers are now the higher-value move.
