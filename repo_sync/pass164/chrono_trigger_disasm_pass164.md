# Chrono Trigger Disassembly — Pass 164

## Scope
Pass 164 closes the remaining low-bank gap between the exact externally callable byte-mix helper at `C3:02DD..C3:0306` and the already-frozen exact temporary trampoline/entry code that begins at exact `C3:0529`.

## Closed span
- **`C3:0307..C3:0528`** — exact `7F`-backed tile-strip builder with exact regenerate/reuse/blank fast paths and exact sampled-byte-to-planar-4bpp pack core

## Why this is one owner
This span contains several internal branch targets, but the exact body is still one callable owner:
- exact entry starts at `C3:0307`
- exact loop-back path at `C3:034C` is **not** one separate public helper; it rejoins the exact shared strip-iteration path rooted at `C3:0309`
- exact exits route through the exact shared tail and final exact `RTL` at `C3:0528`

So the honest closure is the full exact span `0307..0528` as one routine.

## Behavioral summary
The routine builds one exact strip of exact planar tile data in WRAM bank `7F`.

### Inputs/state touched
- exact source selectors and state rooted at direct-page / work variables including exact `2D/2F/31/33/35/37/39/3B`
- exact stream/source bytes through exact pointer `(31),Y`
- exact destination buffer rooted at exact `7F:0000`
- exact previous-strip / comparison state rooted at exact `7F:0000+X` and exact work bytes around exact `7F:420C+X`

### High-level operation
For each exact strip position, the routine chooses one of three exact actions:
1. **regenerate tile**
   - sample exact 8 bytes from `(31),Y`
   - convert them into exact 4-bitplane row layout
   - write exact `0x20` bytes of tile output into exact `7F:0000+X`
2. **reuse previous tile**
   - when the exact compare/state path says the tile is unchanged, skip the expensive rebuild and preserve the previous exact tile bytes
3. **blank trailing tile/span**
   - if the strip has crossed the exact active width boundary, write zeros across the exact `0x20`-byte tile block

### Internal core
The exact tile-build core at exact `C3:0394..C3:03E9`:
- reads exact 8 source bytes from `(31),Y`
- accumulates four exact 8-bit plane rows (`29/2B/2D/2F`-style working set)
- packs them into SNES planar 4bpp row order
- emits exact `0x20` bytes per tile

### Width / strip progression
- exact `33` acts as the exact current strip/tile position counter
- exact `25` acts as the exact limit/width boundary reference
- exact `35/37/39/3B` advance through the exact source stream and destination/compare helpers as the routine walks across the strip

## Control-flow notes that matter
- exact `034C` looks helper-like at first glance because it starts a visible compare/branch cluster, but it is one internal re-entry target into the exact owner, not one separate callable routine
- exact `0529` remains outside this closure; it is the already-frozen exact next owner/trampoline region

## Resulting seam update
With exact `C3:0307..C3:0528` frozen, the next live unresolved bank-`C3` seam exposed by the workspace is:
- **`C3:08A9..C3:0EF9`**

## Completion snapshot after pass 164
- overall completion estimate remains **~70.2%**
- exact label rows: **1316**
- exact strong labels: **998**

## Confidence
Medium-high.
The exact owner boundary is strong because the entry, internal re-entry structure, and shared terminal `RTL` line up cleanly. The exact semantic name is intentionally descriptive of what the bytes provably do without pretending we already know the final engine-facing feature name.
