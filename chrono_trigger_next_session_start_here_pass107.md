# Next Session Start Here

Latest completed pass: **107**

## What pass 107 actually closed
Pass 107 stayed on the exact live seam inherited from pass 106 and fully closed the body at `FD:C1EE..C2C0`.

The strongest keepable results are:

- `FD:C1EE..C2C0` is now exact
  - `PHD`
  - `REP #$20 ; LDA #$4300 ; TCD`
  - `SEP #$20`
  - writes exact control bytes into the eight channel control slots at `$4300/$4310/.../$4370`
  - writes exact B-bus target bytes into `$4301/$4311/.../$4371`
  - sets every source-bank and indirect-bank byte to `7F`
  - reads `0153 & 0x0F`
  - installs one of two exact 8-entry WRAM source-address bundles
  - exits `PLD ; RTL`
- strongest safe reading: exact eight-channel indirect-HDMA installer/finalizer body for this local family

- the two exact WRAM bundles are now frozen
  - zero-side bundle:
    - `7F:0F80, 0FD7, 102E, 1085, 10DC, 1133, 118A, 11E1`
    - exact span `7F:0F80..7F:1237`
  - nonzero-side bundle:
    - `7F:1238, 128F, 12E6, 133D, 1394, 13EB, 1442, 1499`
    - exact span `7F:1238..7F:14EF`

- `7E:013C.bit0` now has an exact local contract here
  - clear -> channel 7 B-bus target byte `0x28`
  - set   -> channel 7 B-bus target byte `0x29`

- `FD:C1EE` is now exact enough to stop treating it as the `0128` producer
  - there is no clean direct `7E:0128` read/write inside this body
  - so the real producer seam has moved upstream again into the paired builder families behind `FD:C2C1`

## What this means semantically
The exact answer to the pass-106 live seam is now:

- `FD:C1EE` is not the shadow-byte producer
- it is the exact local **HDMA channel-register programming/finalization** step
- `FD:C2C1` still chooses one of six exact builder targets
- those builder families prepare one of the two paired WRAM HDMA table bundles
- `FD:C1EE` installs the chosen bundle into the eight channel register blocks
- `C0:0AFF` then returns the already-prepared `7E:0128` HDMA enable shadow byte

## Best next seam
Do **not** reopen `FD:C1EE` itself unless new evidence appears.

The cleanest next move is:

1. stay in the exact same FD-side family
2. move one layer upstream into the paired builder targets behind `FD:C2C1`
3. freeze, in order:
   - whether `0126=0` (`FD:C2EB / FD:C847`) is the direct owner of `7E:0128`
   - then `0126=1` (`FD:C995 / FD:CD0C`)
   - then `0126=2` (`FD:CFCF / FD:D27E`)
4. specifically answer:
   - which builder family directly writes/finalizes `7E:0128`
   - whether the two `7F` bundles are true double-buffer siblings, true mode siblings, or mixed state/buffer siblings
   - whether `0126` is only a local 3-way builder-family index or a wider display/state selector byte

That is cleaner than jumping back sideways into unrelated CD/C0 pockets, because pass 107 has now removed the last big uncertainty from the exact `FD:C1EE` finalizer body.

## Completion estimate after pass 107
Use the toolkit-generated weighted report as the source of truth.

Conservative project completion estimate: **pending toolkit recompute**

Still true:
- semantic/control coverage is ahead of rebuild readiness
- the expensive endgame is still bank separation, decompressor/data grammar work, runtime-backed WRAM proof, source lift, and rebuild validation
