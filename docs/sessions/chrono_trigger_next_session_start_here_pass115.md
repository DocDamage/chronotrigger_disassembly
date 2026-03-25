# Chrono Trigger — Next Session Start Here (Pass 115)

## What pass 115 actually closed

Pass 115 answered the exact fallback/body question that pass 114 left open, and it also stopped treating `30` and `2C` like anonymous scratch inside this later chain.

### Exact closures

- `C0:2E1E..2E65` is now exact:
  - shared fallback target for the local `2D == 0` branch in the `BB/C1/C2/C0/C3/C4` family
  - force blank through `$2100 = 0x80`
  - zero:
    - `$4200`
    - `$420B`
    - `$420C`
    - `0128`
    - `$212C`
    - `$212D`
    - `$2121`
  - write 16-bit `X` into `$2122/$2122`
  - seed `0504 = 0x40`, `0500 = 0x40`, `0119 = 0x0F`
  - re-enable NMI via `$4200 = 0x81`
  - restore `$2100 = 0x0F`
  - `CLI ; BRA $FE` forever
  - calling family preloads `X = 0x7FE0` before entering this body

- `C0:88E5..88EC` is now exact:
  - `2A -> 2E`
  - `2B -> 30`
  - `RTS`

- `C0:88ED..8A69` is now exact enough structurally:
  - tests `0138`
  - when nonzero, returns through the short `REP #$10 ; RTS` tail
  - otherwise reads selector nibble `00F9 & 0x0F`
  - dispatches through the inline helper table beside `8900`
  - active helpers write signed coarse/fine step bytes into `2C/2D`
  - those helpers shift `2E/30` by `±0x10` or `±0x20` according to `00F8.bit1`

- `C0:8A6C..8A9D` is now the first exact downstream reader of `30`:
  - branches on sign/zero of `30`
  - then sign/zero of `2E`
  - selects one of:
    - `8AB5`
    - `8BC4`
    - `8BF9`
    - `8D11`
    - `8E21`
    - `8EF1`
    - `8FC1`
    - `909C`

---

## What **not** to reopen

Do **not** reopen these already-closed seams:

- the exact `0xB8` triplet loader at `3557..356F`
- the exact one-byte `0xBB / 0xC1 / 0xC2` family from pass 114
- the exact two-byte `0xC0 / 0xC3 / 0xC4` family from pass 113
- the `020C..0214 -> C2:0003` packet-builder lane
- the `FD:E022` / `FD:DE98` descriptor-builder chain
- the `ED15` vs `FD:E022` split
- the `C0:2E1E..2E65` fallback itself

The live seam is downstream of the `8A6C` dispatcher now.

---

## The real next seam now

The honest next move is:

1. decode the eight downstream branch bodies selected by `8A6C..8A9D`:
   - `8AB5`
   - `8BC4`
   - `8BF9`
   - `8D11`
   - `8E21`
   - `8EF1`
   - `8FC1`
   - `909C`
2. freeze whichever of those first proves the final human-facing noun of the working pair `2E/30`
3. freeze whichever of those first proves the exact later consumer role of template step bytes `2C/2D`

That is the smallest honest live seam after pass 115.

---

## Important carry-forward wording

Carry this exact wording forward:

- `C0:2E1E..2E65` = exact forced-blank fixed-color hard-stop fallback shared by the local-`2D == 0` invalid path
- `C0:88E5..88EC` = exact local transfer `2A -> 2E`, `2B -> 30`
- `C0:88ED..8A69` = exact signed-step template-dispatch lane writing coarse/fine `2C/2D` step bytes and shifting working pair `2E/30`
- `C0:8A6C..8A9D` = first exact downstream reader of `30`, selecting one of eight later branch bodies
