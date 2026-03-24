# Chrono Trigger Disassembly — Pass 99

## Scope
Pass 98 killed the fake `CE0F` reader lead and tightened the neighboring D1 selector/profile controller, then explicitly pointed the next pass at `D1:EBDF..EC26`.

This pass stayed on that seam, but the real win was slightly wider than the original target:

- decode the `EBDF` copier exactly
- decode the caller that feeds it from `CDC9` and the three local phase tables
- find where `CDC9` itself comes from
- keep the honest boundary clear where the remaining `EA65..EAF4` in-place profile-stepper is still not fully frozen

So pass 99 turns the old “mystery post-controller tail” into a real **phase-window materialization path**.

## Starting point
- previous top-of-stack: **pass 98**
- live seam from the note: **`D1:EBDF..EC26`**

## Work performed
- decoded `D1:EBDF..EBFF` exactly
- decoded `D1:EB1D..EB4B` exactly enough to keep
- decoded `D1:EB00..EB1C` exactly
- decoded `D1:EA01..EA20` exactly
- identified and froze the three exact 14-entry phase tables at `D1:EA21..EA4A`
- rechecked the old pass-98 `CDCC..CDE7` noun against the new copier path
- explicitly checked the adjacent `20A2/22A2` destination context against the earlier pass-82 palette-band work

## Strongest keepable result
The post-pass-98 D1 tail is no longer just “some helper after the profile rebuild”.

It now resolves into a concrete chain:

1. `D1:EA01..EA20` scans the first materialized 14-word window at `20A2..20BD` against `D0:FBE2` and stores the first matching word index to `CDC9`
2. `D1:EA21..EA4A` supplies three exact 14-entry circular phase-offset tables
3. `D1:EB00..EB1C` decrements `CE0D`, conditionally clears `CE0A`, and duplicates `CDCC..CDE7` into `CDE8..CE03`
4. `D1:EB1D..EB4B` uses `CDC9`, the three phase tables, and the `CE10` direct-vs-reversed selector helper to materialize **three 14-word phase windows**
5. those windows are copied into the interiors of the promoted paired palette bands rooted at `20A0` and `22A0`

That is a real structural upgrade.

## 1. `D1:EA01..EA20` gives `CDC9` an exact local meaning
This helper is exact:

- `TDC ; TAX ; TAY`
- `REP #$20`
- loop across `X = 0, 2, 4, ... 0x1A`
  - `LDA D0:FBE2,X`
  - `CMP 20A2,X`
  - if equal, stop immediately
  - otherwise `INY ; INX ; INX`
- if no equality was found before `X == 0x1C`, force `Y = 0`
- `TDC ; SEP #$20 ; TYA ; STA $CDC9 ; RTS`

Strongest safe reading:

> `D1:EA01..EA20` finds the first word position where the first materialized 14-word window at `20A2..20BD`
> matches the base profile root `D0:FBE2`, then stores that word index into `CDC9`.
>
> If no match is found across the 14-word span, it stores `0`.

This is the first exact static anchor for `CDC9`.

## 2. `D1:EA21..EA4A` is three exact 14-entry circular phase-offset tables
Immediately after the `EA01` helper sit three exact 14-byte tables:

### `D1:EA21..EA2E`
`00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D`

### `D1:EA2F..EA3C`
`04 05 06 07 08 09 0A 0B 0C 0D 00 01 02 03`

### `D1:EA3D..EA4A`
`0A 0B 0C 0D 00 01 02 03 04 05 06 07 08 09`

These are not random constants.
`D1:EB1D..EB4B` indexes all three with the current `CDC9` value.

Strongest safe reading:

> `D1:EA21..EA4A` is a three-table family of exact 14-entry circular phase-offset maps:
> base, `+4`, and `+10`.

## 3. `D1:EB00..EB1C` turns the 14-word active profile into a doubled 28-word sliding source
This block is exact:

- `DEC $CE0D`
- if that reaches zero, `STZ $CE0A`
- then:
  - `TDC ; TAX`
  - `REP #$20`
  - copy exactly `0x1C` bytes / 14 words from `CDCC..CDE7` to `CDE8..CE03`
  - `TDC ; SEP #$20`

Strongest safe reading:

> `D1:EB00..EB1C` decrements the profile-change cooldown byte `CE0D`, clears `CE0A` when the cooldown expires,
> then duplicates the active 14-word profile buffer from `CDCC..CDE7` into `CDE8..CE03`.

This matters because it explains how the later copier can read contiguous 14-word windows without needing wrap logic:
the source has been explicitly doubled into a 28-word ring-style slab.

## 4. `D1:EB1D..EB4B` materializes three 14-word phase windows from that doubled profile ring
This block is now exact enough to keep.

Exact structure:

- `LDA $CDC9 ; TAX`
- table 1:
  - `LDA D1:EA21,X`
  - `STA $45`
  - `LDY #$0000`
  - `JSR $EBD0`
  - `JSR $EBDF`
- table 2:
  - `LDA D1:EA2F,X`
  - `STA $45`
  - `LDY #$0020`
  - `JSR $EBD0`
  - `JSR $EBDF`
- table 3:
  - `LDA D1:EA3D,X`
  - `STA $45`
  - `LDY #$0040`
  - `JSR $EBD0`
  - `JSR $EBDF`
- `RTL`

Strongest safe reading:

> `D1:EB1D..EB4B` uses the current phase index in `CDC9` plus three exact circular offset tables
> to materialize three 14-word phase windows from the doubled profile ring.
>
> The three windows are written at `Y = 0x0000`, `0x0020`, and `0x0040`.

Context matters here:
the destination writes performed by `EBDF` land at `20A2+Y` and `22A2+Y`,
which places the three windows inside the already-known promoted paired palette bands
rooted at `20A0` and `22A0`.

## 5. `D1:EBD0..EBDE` and `D1:EBDF..EBFF` are now exact helpers in that path, not floating leaf routines
Pass 98 already froze `EBD0`, but the new caller makes its strongest local reading sharper.

### `D1:EBD0..EBDE`
Exact body:

- `LDA $CE10`
- if nonzero, return direct `$45`
- if zero, return `0x0E - $45`

In this path the safest local reading is:

> direct-vs-reversed 14-step phase-selector helper gated by `CE10`.

### `D1:EBDF..EBFF`
Exact body:

- `PHX`
- `REP #$20`
- `ASL A ; TAX`
- `LDA #$000E ; STA $45`
- loop 14 times:
  - `LDA $CDCC,X`
  - `STA $20A2,Y`
  - `STA $22A2,Y`
  - `INX ; INX ; INY ; INY`
- `TDC ; SEP #$20 ; PLX ; RTS`

Strongest safe reading:

> `D1:EBDF..EBFF` copies one exact 14-word contiguous window from the doubled profile ring
> rooted at `CDCC..CE03` into the paired band interiors at `20A2+Y` and `22A2+Y`.

The new important correction here is the source noun:
the copy is **not** limited to only `CDCC..CDE7`.
It relies on the duplicated tail at `CDE8..CE03` to support sliding contiguous reads.

## 6. what changed semantically
Before this pass:

- `CDC9` was still an anonymous local byte
- `EBDF` was a live seam but not yet placed in a full caller contract
- `CDCC..CDE7` was known as a rebuilt 14-word profile buffer, but its downstream windowing/materialization path was still foggy

After this pass:

- `CDC9` is now an exact local **phase/match index**
- `CDCC..CE03` is now an honest doubled sliding profile ring for the `EBDF` window copies
- `EB1D..EB4B` is a real three-window materializer into the `20A0/22A0` promoted paired bands
- `CE10` is sharper locally as a direct-vs-reversed phase-window selector latch

That is enough to promote this seam from “post-controller helper noise” to a concrete staged path.

## Strong labels / semantics added
- `D1:EA01..D1:EA20` — exact `CDC9` finder helper
- `D1:EA21..D1:EA4A` — exact three-table circular phase-offset family
- `D1:EB00..D1:EB1C` — exact cooldown decrement + active-profile duplication helper
- `D1:EB1D..D1:EB4B` — exact three-window phase materializer
- `D1:EBDF..D1:EBFF` — exact 14-word window copier from the doubled profile ring
- `7E:CDC9` — exact local phase/match index byte
- `7E:CDE8..7E:CE03` — duplicated trailing half of the active profile ring for contiguous sliding-window reads

## Corrections made this pass
- corrected the effective source noun for the `EBDF` copier from only `CDCC..CDE7` to the doubled ring `CDCC..CE03`
- stopped treating `CDC9` as anonymous local state
- stopped treating the `20A2/22A2` writes as isolated stores; they are now part of a three-window materialization path into the promoted paired bands

## Still unresolved
- I have **not** frozen the exact purpose of the odd `D1:EB4C..EB6F` prelude; it computes a `5FB2 >> 3` doubling loop against `5FB0` but leaves no obvious persistent state before falling into the pass-98 `CE0E` profile rebuild path.
- I have **not** fully frozen `D1:EA5F..EAF4`, the in-place active-profile convergence loop that runs before the duplication/materialization stage when `CE0A != 0`.
- I have **not** frozen the final gameplay-facing noun of the `CDCC..CE03` profile family or of the promoted paired-band interiors that receive the three materialized windows.
- I have **not** found a clean direct static reader of `CE0F`.

## Next recommended target
The best next static seam is now:

1. stay in the same D1 pocket
2. decode **`D1:EA5F..EAF4`** exactly as the active-profile convergence/stepper path
3. only after that decide whether the weird `D1:EB4C..EB6F` prelude can be justified as real timed behavior or should remain caution-noted

## Completion estimate after pass 99
Conservative project completion estimate: **~68.2%**

Still true:
- semantic/control coverage is well ahead of rebuild readiness
- the expensive endgame is still broad bank separation, decompressor/data grammar ownership, runtime-backed WRAM proof, source lift, and rebuild validation
