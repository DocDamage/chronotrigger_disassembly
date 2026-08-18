# Chrono Trigger — Next Session Start Here (Pass 163)

## What pass 163 actually closed

Pass 163 closed the exact downstream family reached by exact low-bank veneer `C3:000E` and split the old seam honestly.

### Exact new closures now frozen

- `C3:01E4..C3:02DC`
  - exact selected-`7E/7F` `0xE0`-byte band initializer
  - exact 32-step saturating add/subtract WRAM stream worker
  - exact first activation seeds the exact selected-bank band with exact `00` for exact mode `01` or exact `FF` for surviving nonzero modes
  - exact active steps stream one exact `0xE0`-byte band through exact `$2180` while updating the exact selected-bank source band in place
  - exact mode `01` is the exact saturating-add side and exact mode `02` is the exact saturating-subtract side

- `C3:02DD..C3:0306`
  - exact externally callable byte-mix helper
  - exact updates state rooted at exact `0386`
  - exact mixes in exact `X`, exact `0008`, exact `F0/F2/F4`, and exact `2137/213C/213D`
  - exact returns one exact start byte used to seed the exact `C0:FE??` chained-byte walk through exact pointer bytes `55/56/57`

## Important correction/state change

- do **not** keep treating exact `C3:01E4..C3:0306` as one exact monolithic owner
- the honest split is now:
  - exact owner `01E4..02DC`
  - exact helper `02DD..0306`
- exact `02DD..0306` is one exact real callable helper, not one exact buried private tail, because exact `C3:15E4` also calls it directly

## What not to reopen

- do not flatten exact `01E4..02DC` into one vague “graphics updater” blob; the exact persistent 32-step lifetime and exact add/subtract split are both real
- do not forget the exact first-activation seed stage:
  - exact mode `01` seeds exact `00`
  - exact mode `02` seeds exact `FF`
- do not reopen exact `02DD..0306` as one exact random math tail without preserving the exact role it plays in feeding the exact `C0:FE??` chained-byte walk

## The real next seam now

1. exact next manual/raw target:
   - `C3:0307..C3:0528`

2. exact reasons this is the right next place:
   - exact `000E -> 01E4` family is now honestly closed
   - exact `02DD..0306` is split cleanly as one exact helper
   - the next unfrozen exact bank-`C3` body before the already-frozen exact temporary trampoline code at `0529` begins immediately after exact `0306`

3. exact safest next move:
   - inspect exact raw bytes `C3:0307..C3:0528` manually
   - preserve exact callable/helper boundaries if more exact internal `RTL/RTS` islands show up
   - keep low-bank `C3` moving in exact callable-owner order before jumping to farther bank-`C3` xref sites
