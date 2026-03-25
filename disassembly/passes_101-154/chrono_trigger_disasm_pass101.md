# Chrono Trigger Disassembly — Pass 101

## Scope
Pass 100 closed the color semantics of `D1:EA5F..EAF4`, but it still left one annoying question open:

- what exactly is `D1:EB4C..EB6F` doing before the selector/profile rebuild at `EB70`?

This pass stayed on that seam first, then used the now-stable D1 block to reopen the first honest clean caller chain.

## Starting point
- previous top-of-stack: **pass 100**
- live seam from the note: **`D1:EB4C..EB6F`**

## Work performed
- decoded `D1:EB4C..EB6F` instruction-for-instruction
- checked register / scratch liveness across the fallthrough into `EB70`
- rechecked the older `5FB0 / 5FB2` family against pass-33 evidence
- searched the ROM again for clean external callers of `D1:EA4B`
- validated the first clean caller block at **PC `0x0D0978..0x0D09CB`** (mirrored SNES CPU view `CD:8978..89CB`)

## Strongest keepable result
`D1:EB4C..EB6F` is no longer an honest mystery helper.

It is an exact **dead-output timing shim / cycle-burn prelude** that quantizes `5FB0` against eighths of `5FB2` before falling into `EB70`.

That conclusion is stronger than the old “threshold-doubling probe” wording, because the pass now proves the important negative fact too:

- the loop produces **no surviving semantic output** for the later selector rebuild
- `X` is overwritten immediately by `EB70`
- `A` is overwritten immediately by `EB70`
- `$45 / $47` are only local scratch inside the prelude
- the branch falls straight into `EB70`, and `EB70` does not consume the prelude’s bucket count

So the code is real, but it is not a selector calculator, not a palette-data mutator, and not a hidden state writer.

## 1. `D1:EB4C..EB6F` exact behavior
The exact body is:

- `LDX #$0001`
- `REP #$20`
- `LDA $5FB2`
- `LSR` three times
- `STA $45`
- `STA $47`
- loop:
  - `LDA $5FB0`
  - `CMP $45`
  - if `5FB0 < current_threshold`, exit
  - otherwise:
    - `LDA $45`
    - `CLC`
    - `ADC $47`
    - `STA $45`
    - `INX`
    - repeat until `X == 8`
- then `PLD / SEP #$20` fall straight into `EB70`

Equivalent reading:

- `base = floor(5FB2 / 8)`
- `threshold = base`
- advance through up to 8 buckets while `5FB0 >= threshold`
- each bucket raises the threshold by one more `base`
- no final bucket index survives into the following controller logic

So the only durable thing this block contributes is **time spent executing**.

## 2. why the “timing shim” reading is justified
This is the key closure of pass 101.

The old reading only proved the arithmetic. This pass proves the liveness story:

- on exit, `EB70` immediately reloads `A` from `CE0E`
- `EB70` immediately overwrites `X` from the new selector path
- the temporary DP bytes `$45 / $47` are not consumed by `EB70`
- the prelude performs no WRAM writes other than those scratch bytes
- it performs no ROM-indexed copy, no selector store, and no palette-buffer store

That means the bucket loop is **structurally side-effect-free** with respect to the palette/profile controller that follows.

Strongest safe reading:

> `D1:EB4C..EB6F` is a quantized timing/burn loop keyed by the local `5FB0 / 5FB2` ratio, placed only on the `CE0A == 0` branch before the active selector/profile rebuild.

I am still **not** freezing the final gameplay-facing noun of the `5FB0 / 5FB2` family itself from this pass alone.

## 3. first clean external caller chain for the D1 palette-maintenance tick
Pass 98 killed the fake `CE0F` reader lead at `CD:BEF8`, but that did not mean the whole D1 pocket lacked callers.

This pass confirms the first honest clean external caller chain for the palette-maintenance entry at `D1:EA4B`:

- **PC `0x0D0985`**
- mirrored CPU/SNES view: **`CD:8985`**
- exact instruction: `JSL $D1EA4B`

And it sits inside a clean surrounding driver block at:

- **PC `0x0D0978..0x0D09CB`**
- mirrored CPU/SNES view: **`CD:8978..89CB`**

The strongest exact facts from that block are:

- if the earlier local condition is met, it may first call `CE:E18E`
- it then gates the D1 palette-maintenance call through `CE13`
  - if `(A & CE13) != 0`, it skips `D1:EA4B`
  - otherwise it calls `D1:EA4B`
- after that it continues through already-known neighboring control paths, including:
  - `CD:1609` auxiliary two-slot descriptor runtime tick
  - `D1:F426` descriptor-header suspend/restore selector
  - later follow-up calls at `FD:FFF7` and `C2:8002`

## 4. what this changes semantically
Before pass 101:

- `EB4C..EB6F` was an exact arithmetic curiosity with no frozen role
- `EA4B` had no confirmed clean external caller chain in hand during the current seam

After pass 101:

- `EB4C..EB6F` is now honestly classifiable as a **timing-only prelude**
- the D1 palette-maintenance tick is now anchored inside a **real CD-side driver block**, not floating as an isolated local controller
- the best next static move is no longer “stare at EB4C again”
- the best next static move is the **caller block around `CD:8978..89CB`**

## Strong labels / semantics added
- `D1:EB4C..D1:EB6F` — exact quantized timing/cycle-burn prelude keyed by `5FB0` against eighths of `5FB2`
- `CD:8985` / PC `0x0D0985` — first clean external `JSL D1:EA4B` caller now explicitly anchored
- `CD:8978..89CB` / PC `0x0D0978..0x0D09CB` — clean surrounding CD-side driver block for the D1 palette-maintenance path

## Corrections made this pass
- corrected the old “threshold-doubling probe” wording into a stronger **dead-output timing shim** reading
- corrected the current seam status from “no clean caller chain in hand” to “first clean caller chain now anchored at `CD:8985` / PC `0x0D0985`"

## What still did not close
- I have **not** frozen the final gameplay-facing noun of `5FB0 / 5FB2`.
- I have **not** frozen the higher-level noun of `CE13`, `A028`, `A013`, or `CD29` inside the new CD-side caller block.
- I have **not** frozen a clean direct static reader for `CE0F`.
- I have **not** claimed the whole `CD:8978..89CB` block is fully named; only the D1-call anchor and immediate local control facts are frozen.

## Next recommended target
The cleanest next static move is now:

1. stay on the new caller chain
2. decode **`CD:8978..89CB`** (PC `0x0D0978..0x0D09CB`) as one real driver block
3. specifically freeze:
   - what `CE13` is doing as the gate for `D1:EA4B`
   - how `A028 / A013 / CD29 / CD2D / CD2E` interact around the post-call tail
   - whether this whole block is the real frame/stage owner of the D1 palette-maintenance tick

## Completion estimate after pass 101
Conservative project completion estimate: **~68.3%**

Qualitatively:
- semantic coverage moved a little, not a lot
- the value of this pass is mostly that it removed one fake “maybe-stateful” fog pocket and found the first clean caller anchor for the D1 maintenance tick
