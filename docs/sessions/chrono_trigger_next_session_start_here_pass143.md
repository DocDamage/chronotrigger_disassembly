# Chrono Trigger — Next Session Start Here (Pass 143)

## What pass 143 actually closed

Pass 143 finished the front callable/helper family that pass 142 left open at `C2:E34A..C2:E5F0`, with the important structural correction that the old seam end was too short. The clean closure stops at `C2:E60A`, because `C2:E5CC..C2:E60A` is one complete callable owner.

### Exact new closures now frozen

- `C2:E34A..C2:E361`
  - exact count-capped offset writer that turns exact byte `0F06` into one exact `8 * min(0F06, 4) + 9C` byte mirrored into exact work/config bytes `0880/0884`

- `C2:E362..C2:E38E`
  - exact `0F0C`-selected clear / normalize / compare / fallback-copy owner that clears one exact destination byte, runs exact helpers `E390` and exact core entry `E3E0`, and on the unresolved exact path copies exact `0x0006` bytes from exact `9890` into the exact `0F0C`-selected lane

- `C2:E38F..C2:E3DD`
  - exact compact-list normalizer that seeds exact `98A0` from exact `0F00`, strips exact `EF` placeholders, and compacts the surviving exact bytes back into exact staging band `9890` starting from exact byte `51`

- `C2:E3DE..C2:E40D`
  - exact overlapping row-match helper pair scanning exact five-byte rows in exact table family `2C23 + 6*n` against the live exact `9890` compact list and returning exact `FF` only on an exact row match after exact helper `EACC`

- `C2:E40E..C2:E53D`
  - exact large setup / import / selector-emission owner that clears/initializes exact selector state, materializes exact `9890 / 0F00 / 4E40 / 5E00` work bands, drives exact service chain `C41F -> 86DD -> F90C -> FB97 -> FF:FC04`, emits exact selector chain `FBCE -> FBF8 -> FC37 -> FC1B -> E53E`, stamps exact bytes `0D13 / 299F`, and tail-jumps into exact helper `E34A`

- `C2:E53E..C2:E544`
  - exact local selector packet / descriptor blob `00 78 00 5E 7E 00 08` consumed through exact helper `8385` from exact owner `E40E`

- `C2:E545..C2:E575`
  - exact `FF:C9AC` stream materializer that builds delimiter-rich exact `9890` output from exact selector byte `51` using exact `0A` inner count, exact `08` outer count, exact `FF` separators, exact `01` group delimiters, and a final exact `00` terminator

- `C2:E576..C2:E5CB`
  - exact zero-lane import / staging owner that copies exact `FF:F008` source streams into exact WRAM destination `3600`, stages exact block `FF:CE9A -> 7E:9500`, increments exact byte `0D15`, seeds exact byte `0D13 = 05`, and exits through exact selector chain `FBCE -> FBF8 -> FC61`

- `C2:E5CC..C2:E60A`
  - exact `(54 + 1)` change-handler / refresh owner that watches the live exact selector byte `54`, refreshes exact latch/output bytes `0D77 / 020C`, seeds exact service block `5248 / 6A20 / CF3B / 0200`, and reruns exact helper `FA49` only on exact value change

## What not to reopen

Do not reopen `C2:E34A..C2:E5F0` as the old seam; the exact closure stops at `C2:E60A`.
Do not treat `C2:E5F0` as a natural stopping point; it cut the exact `E5CC` owner in half.
Do not misread `C2:E53E..C2:E544` as code; in this pass it is only safe as the exact local selector packet consumed through exact helper `8385`.

## The real next seam now

1. next clean follow-on callable family:
   - `C2:E60B..C2:E760`

2. immediate structural hints already visible in that follow-on family:
   - the exact seam begins with one strange stack-relative opener at `C2:E60B..C2:E61A` that immediately exits through exact jump `83B2`
   - clearer downstream exact owners visibly begin at `C2:E61B`, `C2:E6AE`, `C2:E705`, and `C2:E73F`
   - exact helper `EAC2` is still threaded heavily through that next band
   - exact bytes `68`, `54`, `81`, `0D1D`, and `0D4C` remain hot in the follow-on family

3. broader gameplay-facing nouns still worth tightening:
   - `7E:0F0F`
   - `7E:0D1F`
   - broader gameplay/system role of `7E:0D8B`
   - broader gameplay/system role of `7E:0D8C`
   - broader gameplay/system role of `7E:0D90`

4. broader top-level family noun:
   - `C2:A886..C2:AA30`
