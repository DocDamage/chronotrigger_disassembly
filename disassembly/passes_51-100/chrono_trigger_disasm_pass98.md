# Chrono Trigger Disassembly — Pass 98

## Scope
Pass 97 finished the warm C7 bridge seam and explicitly sent the work back to the old `CDC8 / CE0F / CFFF` control-byte pocket.

I took the strict route here instead of forcing a bad noun:

- re-scan `CE0F` with **valid mapped CPU-opcode** filters only
- pressure-test the old `CD:BEF8` candidate that had been hanging around as the only apparent reader lead
- then stay in the nearest clean D1 code and freeze whatever adjacent controller logic was actually honest

So this pass is partly a cleanup pass and partly a new-control-cluster pass.

## Starting point
- previous top-of-stack: **pass 97**
- live seam from the handoff: return to **`CE0F`** and find the first clean reader chain if possible

## Work performed
- ran a strict mapped-code scan for direct absolute `$CE0F` opcode uses
- checked the exact hit list against raw ROM neighborhoods instead of trusting opcode-pattern matches in isolation
- re-dumped `CD:BED8..C014` to see whether the old `CD:BEF8` lead was real code or dense data
- fully decoded the clean D1 helper at `D1:EB70..EBCF`
- decoded the small selector helper at `D1:EBD0..EBDE`
- dumped the exact table root at `D1:E9EF` and the exact source-profile root at `D0:FBE2`

## Strongest keepable result
This pass does **not** find a clean direct `CE0F` reader.

But it does make the seam materially more honest:

- the old `CD:BEF8` “reader” lead does **not** survive scrutiny as clean CPU code
- the valid mapped direct-opcode hits for `$CE0F` collapse to:
  - `D1:E987` — `INC $CE0F`
  - `D1:F26E` — `STZ $CE0F`
  - plus several obvious dense-data false positives in non-clean neighborhoods
- meanwhile the adjacent clean D1 controller at `EB70` is exact enough to keep and it materially upgrades the neighboring `CE0E / CE10 / CE0B / CE0C / CE0D / CDCC..CDE7` cluster

So the real upgrade of pass 98 is:

> the static `CE0F` hunt is now cleaner because the bad `CD:BEF8` lead is gone,
> and the neighboring D1 controller has become exact enough that the local control-byte neighborhood is no longer just fog.

## 1. strict mapped-code scan: no honest direct `CE0F` reader yet
Using only valid mapped CPU opcode locations, the direct absolute `$CE0F` hits are:

- `C9:D2CB` — `TSB $CE0F`
- `D1:E987` — `INC $CE0F`
- `D1:F26E` — `STZ $CE0F`
- `DE:C063` — `CMP $CE0F`
- `DF:DA14` — `ORA $CE0F`
- `E1:A45C` — `STX $CE0F`
- `E3:F361` — `DEC $CE0F`
- `EC:BBF4` — `CMP $CE0F`
- `ED:ED95` — `DEC $CE0F`

After dumping those neighborhoods, only the D1 pair remains honest clean control-byte code.
The others sit in obvious dense table/script/data regions.

That means the project should stop pretending there is already a believable direct static reader.

## 2. `CD:BEF8` does not survive as clean code
The old “lone mapped `LDA $CE0F` at `CD:BEF8`” lead was worth killing carefully.

The raw bytes around `CD:BED8..C014` show:

- `CD:BF18..BF2F` is a 12-entry local pointer table:
  - `BF32`
  - `BF33`
  - `BF61`
  - `BF61`
  - `BF6D`
  - `BF86`
  - `BF9B`
  - `BFB0`
  - `BFC5`
  - `BFDA`
  - `BFEF`
  - `C004`
- the pointed-to bodies at `BF32..C014` are dense structured data / bytecode-like chunks, not normal 65816 subroutines
- the bytes at `CD:BEF8` sit immediately inside that same data block

So the safest keepable statement is:

> `CD:BEF8` is not honest frozen CPU code for a direct `CE0F` read.
> It belongs to the same dense local pointer-table-backed data block rooted at `CD:BF18`.

That is a real correction to the old seam.

## 3. `D1:EB70..EBCF` is an exact controller for the neighboring CE/D1 selector bytes
This is the main positive gain of the pass.

Exact body, in behavior terms:

- `SEP #$20`
- read `CE0E`
- if negative, mask it with `0x7F`
- store the resulting unsigned value to `CE0B`
- compare `CE0B` against `CE0C`
- if equal, return immediately
- otherwise:
  - increment `CE0A`
  - seed `CE0D = 0x20`
  - use `CE0E` sign to decide how `CE0C` moves toward the target in `CE0B`
    - negative `CE0E` snaps `CE0C = CE0B`
    - non-negative `CE0E` steps `CE0C` by `+1` or `-1` toward `CE0B`
  - mirror the new `CE0C` back into `CE0B`
  - switch to 16-bit A/X/Y
  - use exact word table `D1:E9EF` indexed by `2 * CE0C`
  - use that fetched word as an exact offset into data root `D0:FBE2`
  - copy exactly `0x1C` bytes / 14 words into `CDCC..CDE7`
  - return

That is strong enough to freeze structurally.

The strongest safe reading is:

> `D1:EB70..EBCF` steps the active selector/profile byte toward a signed target derived from `CE0E`, then rebuilds one exact 14-word active profile buffer at `CDCC..CDE7` from table roots `D1:E9EF` and `D0:FBE2`.

## 4. `D1:EBD0..EBDE` is a tiny direct-vs-mirrored selector helper gated by `CE10`
The exact helper is:

- `LDA $CE10`
- if nonzero, return direct byte `$45`
- if zero, return `0x0E - $45`

Strongest safe reading:

> `D1:EBD0..EBDE` is a one-byte helper that chooses direct vs `0x0E`-mirrored output based on the `CE10` latch.

This matters because it proves `CE10` is not only a vague token-side latch. It is consumed by clean D1-side control code as a real one-bit direction / inversion selector.

## 5. `D1:E9EF` and `D0:FBE2` are now exact table roots for the new controller
`D1:EB70` makes both table roots exact enough to keep.

### `D1:E9EF..E9FE`
Exact 8-entry word table:

- `00A0`
- `0100`
- `00C0`
- `0080`
- `00E0`
- `0060`
- `0040`
- `0020`

This is the exact word-offset selector table used by `2 * CE0C`.

### `D0:FBE2`
This is the exact source root the controller copies from after applying the offset from `D1:E9EF`.

The controller copies an exact `0x1C`-byte span from here into `CDCC..CDE7`.

That is enough to call it the active source-profile root for this helper, even though the final gameplay-facing noun is still open.

## 6. what changed semantically
Before pass 98, the honest state still had a tempting bad seam:

- there seemed to be one last static `CE0F` reader candidate at `CD:BEF8`
- the neighboring `CE0E / CE10` control bytes were still partly described through older token-local language

After pass 98:

- the `CD:BEF8` lead is dead as clean code
- `CE0F` remains a write-side control byte with no frozen direct static reader yet
- the neighboring `CE0E / CE10 / CE0B / CE0C / CE0D / CDCC..CDE7` controller is exact enough to keep

That is a smaller gain than pass 97, but it is a much cleaner foundation for the next pass.

## Strong labels / semantics added
- `D1:EB70..D1:EBCF` — exact active-selector/profile stepper + rebuild helper
- `D1:EBD0..D1:EBDE` — exact direct-vs-mirrored one-byte helper gated by `CE10`
- `D1:E9EF..D1:E9FE` — exact 8-entry word-offset table for that controller
- strengthened understanding of `CE0E / CE10 / CE0B / CE0C / CE0D / CDCC..CDE7`

## Corrections made this pass
- removed the old confidence hanging off `CD:BEF8` as a plausible clean `CE0F` reader
- tightened the static `CE0F` seam to the honest state: no frozen direct mapped-code reader yet
- promoted the adjacent D1 controller instead of forcing a bad noun from table/data noise

## Still unresolved
- the first exact direct static reader of `CE0F` is still not frozen
- the final gameplay-facing noun of the `CDCC..CDE7` 14-word profile buffer is still open
- the final gameplay-facing noun of the `D0:FBE2` source profiles is still open
- the larger endgame remains unchanged: bank separation, decompressor/data grammar work, runtime-backed WRAM proof, and rebuildability

## Next recommended target
The best static next move is now **not** to go back to `CD:BEF8` again.

The better next seam is:
1. stay on the same clean D1 neighborhood
2. decode **`D1:EBDF..EC26`** and the immediate follow-up controller bytes around `CE0A..CE10`
3. only then decide whether `CE0F` can be tightened statically or whether it really needs runtime proof
