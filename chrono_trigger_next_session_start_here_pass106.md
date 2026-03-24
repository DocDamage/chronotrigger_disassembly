# Next Session Start Here

Latest completed pass: **106**

## What pass 106 actually closed
Pass 106 stayed on the exact trampoline seam opened by pass 105 and fully closed the `C0:0005 -> C0:0AFF` return-value question.

The strongest keepable results are:

- `C0:0AFF..0B27` is now exact
  - sets `D = 0x0100`
  - sets `DB = 0x00`
  - raises `0153.bit7`
  - runs `JSL FD:C2C1` twice
  - clears `0153.bit7`
  - runs `JSL FD:C1EE`
  - returns with exact `LDA $28 ; RTL`
- because `D = 0x0100`, that return is the current contents of **`7E:0128`**

- `7E:0128` is now exact enough to stop calling it anonymous WRAM
  - `C0:AE2B  STA $420C`
  - `C0:AE33  STA $0128`
  - `C0:EC48  LDA $0128`
  - `C0:EC4B  STA $420C`
  - `C0:0B23  LDA $28` with `D = 0x0100`
  - `D1:F4E6  STA $420C`
- strongest safe reading: exact low-bank / FD-side **HDMA enable shadow byte**

- `FD:C2C1..C2DF` is now exact
  - branches on `0153.bit0`
  - uses `0126 * 2` as the index
  - dispatches through one of two exact 3-entry local jump tables
  - flips `0153.bit0` on return
- strongest safe reading: exact front dispatcher in the helper family that rebuilds / materializes the HDMA-shadow path behind `C0:0AFF`

- `C0:0B2B..0B50` is now exact as a startup sibling
  - runs `FD:C124`, `FD:C2C1`, `FD:C1EE`
  - waits on `$4210`
  - sets `$4200 = 0x81`
  - sets `VTIME = 0x00D3`
  - exits with `CLI`

## What this means semantically
The exact answer to the pass-105 seam is now:

- `D1:F4C0` does **not** receive a fixed literal from `C0:0005`
- it receives the current contents of **`7E:0128`**
- `7E:0128` is the exact **HDMA enable shadow byte** for this low-bank / FD-side family
- so the trampoline-side `STA $420C` now has a real producer edge, not a mystery helper byte

## Best next seam
Do **not** reopen `C0:0AFF` itself unless new evidence appears.

The cleanest next move is:

1. stay on the exact helper family behind the now-closed shadow return
2. follow **`FD:C1EE..C2C0`**
3. specifically freeze:
   - what pointer/table family it seeds
   - how it finalizes or materializes `7E:0128`
   - whether `0153` and `0126` are true mode/state bytes or only local builder selectors in this family

That is cleaner than jumping sideways to `CD:09CE` or `CD:0C89`, because the HDMA-mask producer edge inside the installed trampoline has now been isolated down to the remaining FD-side body.

## Completion estimate after pass 106
Use the toolkit-generated weighted report as the source of truth.

Conservative project completion estimate: **pending toolkit recompute**

Still true:
- semantic/control coverage is ahead of rebuild readiness
- the expensive endgame is still bank separation, decompressor/data grammar work, runtime-backed WRAM proof, source lift, and rebuild validation
