# Chrono Trigger Disassembly — Pass 100

## Scope
Pass 99 proved that the D1 tail is a real `CDC9 -> phase tables -> doubled ring -> three-window materializer` path,
but it still left the feeder loop at `D1:EA5F..EAF4` under-described.

This pass stayed on that exact seam and closed the part that matters most:

- decode `D1:EA4B..EA5E` exactly as the top-level guard/branch wrapper
- decode `D1:EA5F..EAF4` exactly
- decide whether the three mask groups are just arbitrary fields or a real color format
- tighten `D0:FBE2..`, `CDCC..CE03`, and `CE0A..CE0D` if the result holds

## Starting point
- previous top-of-stack: **pass 99**
- live seam from the note: **`D1:EA5F..EAF4`**

## Work performed
- disassembled `D1:EA4B..EA5E` exactly
- disassembled `D1:EA5F..EAF4` exactly
- rechecked the `D1:E9EF -> D0:FBE2` source family against the new mask logic
- dumped the full `D0:FBE2..FD01` table family to test whether the selected records are plausible color words
- rechecked the downstream `EB00 / EB1D / EBDF` path against the new color reading
- kept `D1:EB4C..EB6F` honest as caution instead of force-labeling it

## Strongest keepable result
`D1:EA5F..EAF4` is not a generic "profile convergence" helper.

It is an exact **per-channel BGR555 palette tween/convergence loop** over the active 14-word span at `CDCC..CDE7`.

That is not a vibe guess. It falls straight out of the masks and step sizes:

- `0x001F` stepped by `±1`
- `0x03E0` stepped by `±0x0020`
- high-byte `0x7C` stepped by `±0x04`, i.e. `±0x0400` on the 16-bit word

Those are the exact three component fields of SNES `BGR555` color words.

That turns the whole local chain from abstract "profile words" into concrete palette data:

1. `EB70..EBCF` chooses one target palette profile and seeds/rebuilds a 14-color active buffer
2. `EA5F..EAF4` steps each active color toward the target one channel at a time
3. `EB00..EB1C` duplicates that 14-color span into a doubled ring
4. `EB1D..EB4B` materializes three phase-shifted 14-color windows
5. `EBDF..EBFF` copies those windows into the promoted palette-band interiors at `20A2+Y` and `22A2+Y`

That is the main closure of pass 100.

## 1. `D1:EA4B..EA5E` is an exact guard/dispatch wrapper
This block is exact:

- `LDA $5D9B`
- `ORA $05A4`
- `ORA $0598`
- `ORA $058C`
- `ORA $0580`
- if any result is nonzero, `RTL`
- otherwise:
  - `LDA $CE0A`
  - if nonzero, continue into `EA5F`
  - if zero, `JMP $EB4C`

Strongest safe reading:

> one exact top-level guard for the local D1 palette-profile maintenance tick.
>
> It refuses to run while the auxiliary-stage / low-RAM activity bytes are nonzero,
> then chooses between the active in-place convergence path (`CE0A != 0`) and the prelude-plus-selector-rebuild path (`CE0A == 0`).

I am **not** pretending I know the final noun of `0580 / 058C / 0598 / 05A4` from this alone.
The body is exact; those four nouns are not.

## 2. `D1:EA5F..EAF4` is an exact BGR555 convergence loop
This block is exact.

### 2a. selector and source setup
- reads `CE0B`
- doubles it
- uses `D1:E9EF` as a word-offset table
- adds that offset under the ROM root `D0:FBE2`

So the selected source record is:

> `D0:FBE2 + D1:E9EF[2 * CE0B]`

### 2b. low component step
For each word in the active span:

- target: `LDA D0:FBE2,X ; AND #$1F`
- current: `LDA CDCC,Y ; AND #$1F`
- if current > target, decrement current word by `1`
- if current < target, increment current word by `1`
- if equal, do nothing

### 2c. middle component step
Then for that same word:

- target: `LDA D0:FBE2,X ; AND #$03E0`
- current: `LDA CDCC,Y ; AND #$03E0`
- if current > target, subtract `0x0020`
- if current < target, add `0x0020`
- if equal, do nothing

### 2d. high component step
Then for the second byte of the same word:

- target: `LDA D0:FBE3,X ; AND #$7C`
- current: `LDA CDCD,Y ; AND #$7C`
- if current > target, subtract `0x04` from the high byte
- if current < target, add `0x04` to the high byte
- if equal, do nothing

### 2e. loop bounds
- `Y += 2`
- `X += 2`
- loop until `Y == 0x001C`

That is exactly 14 words.

## 3. why the color reading is real, not decorative overreach
The three masks and step sizes line up perfectly with SNES 15-bit palette words:

- `0x001F` = one 5-bit color component
- `0x03E0` = the next 5-bit component
- high-byte `0x7C` = the remaining 5-bit component in the top byte

And the step sizes match the component bit positions exactly:

- `±1`
- `±0x20`
- `±0x400` (via high-byte `±0x04`)

That is why pass 100 is a real semantic upgrade.
Not just because the loop is exact, but because it finally tells us what kind of words these are.

## 4. `D0:FBE2..FD01` is a compact palette-profile family
The full root dump now makes sense structurally.

What holds:

- the root at `D0:FBE2` contains one base 16-word record
- `D1:E9EF` selects eight additional `0x20`-byte-spaced records under the same family
- the active copy/tween loops only consume the first 14 words from each selected record
- the two trailing words are not touched by the active loops in this seam

Strongest safe reading:

> `D0:FBE2..FD01` is a compact palette-profile root:
> one base profile plus eight selectable target profiles,
> each stored in 16-word / `0x20`-byte slots,
> with the active D1 path using the first 14 colors from each.

## 5. what this changes semantically
Before pass 100:

- `CDCC..CE03` was known as a doubled sliding "profile ring"
- `D0:FBE2..` was known as a source-profile root
- `EA5F..EAF4` was still just a suspicious in-place stepper

After pass 100:

- `CDCC..CDE7` is an active **14-color BGR555 palette profile buffer**
- `CDE8..CE03` is the duplicated tail of that active palette ring
- `D0:FBE2..FD01` is a **base + eight selectable palette-profile family**
- `CE0A` is now sharper as the active palette-convergence latch
- `CE0D` is now sharper as the exact convergence cooldown/countdown byte
- `CE0B / CE0C` are no longer generic profile bytes; they are palette-profile selector bytes
- the `EB1D` three-window materializer is now plainly a palette-window materializer

That is a materially better noun map than we had at the end of pass 99.

## 6. what still did not close
The main honest leftover in this pocket is still `D1:EB4C..EB6F`.

Its exact behavior is now very clear:

- start with `X = 1`
- compute `threshold = 5FB2 >> 3`
- compare `5FB0` against the threshold
- if `5FB0 >= threshold`, double the threshold and repeat
- stop after at most 8 tries
- leave no persistent state before falling into the selector rebuild at `EB70`

So I can now say this with confidence:

> `EB4C..EB6F` is a real side-effect-free threshold-doubling probe over `5FB2 >> 3` and `5FB0`,
> but I still do **not** have enough proof to assign it a final gameplay-facing noun.

I am keeping that caution instead of making up a subsystem name.

## Strong labels / semantics added
- `D1:EA4B..EA5E` — exact guard/dispatch wrapper for the D1 palette-profile maintenance tick
- `D1:EA5F..EAF4` — exact BGR555 per-channel palette convergence loop
- `D0:FBE2..FD01` — base + eight selectable 16-word palette-profile family
- `7E:CDCC..7E:CDE7` — active 14-color BGR555 palette profile buffer
- `7E:CDE8..7E:CE03` — duplicated trailing half of the active palette ring for sliding window reads
- `7E:CE0A` — active palette-profile convergence latch
- `7E:CE0D` — palette-profile convergence cooldown byte
- `7E:CE0B / 7E:CE0C` — target / active palette-profile selector bytes

## Corrections made this pass
- corrected the old generic noun of `EA5F..EAF4` to an exact color-format reading
- corrected the old generic noun of `D0:FBE2..` from abstract source profiles to palette profiles
- corrected the old generic noun of `CDCC..CE03` from abstract profile data to active palette data

## Next recommended target
The cleanest next static move is now:

1. stay in the same D1 pocket one more time
2. decide whether `D1:EB4C..EB6F` can be justified beyond its exact side-effect-free probe behavior
3. after that, either:
   - reopen the surrounding caller chain for this full palette-maintenance tick, or
   - stop pretending `CE0F` will necessarily yield statically and plan the first runtime proof instead

## Completion estimate after pass 100
Conservative project completion estimate: **~68.3%**

What I expect qualitatively:
- semantic/control coverage moved up a real amount in this bank
- rebuild readiness did **not** jump much from this pass alone
