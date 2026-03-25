# Chrono Trigger — Next Session Start Here (Pass 151)

## What pass 151 actually closed

Pass 151 finished the callable/helper family that pass 150 left open at `C2:F2F3..C2:F360`, with the structural correction that the old seam end was too short:

- the old seam end at `C2:F360` was **not** a stop; live exact wrapper/helper/owner code continues through exact `C2:F3CA`
- the honest closure for this family now runs through exact `C2:F3CA`

### Exact new closures now frozen

- `C2:F2F3..C2:F331`
  - exact accumulator-byte or forced-refresh change-handler that mirrors exact `A -> 0D77 / 020C`, seeds exact fields `0DC5 = 4E84`, `0DCC = 6840`, `020D = 2EB1`, `020F = CC`, `0DC9 = 01`, `0DD0 = 0080`, and then runs exact helper `FA49`

- `C2:F332..C2:F336`
  - exact short helper mirroring exact word `5B -> 61`

- `C2:F337..C2:F360`
  - exact zero-bank record builder that writes exact word `5D` plus one exact derived `9000`-based pointer into the exact record rooted at exact word `5B`, with exact bank byte `7E` stored into exact offsets `+4` and `+7`

- `C2:F361..C2:F363`
  - exact short wrapper forcing exact `X/Y` 16-bit mode before exact shared late entry `F364`

- `C2:F364..C2:F377`
  - exact FF-bank length-prefixed block importer from exact source pointer `5B` into exact bank-`7E` destination `61`

- `C2:F378..C2:F3CA`
  - exact coordinate-to-coordinate multi-row word-swap owner using exact helper `ED90`, exact packed coordinates `5B/5D`, exact extents `5F/60`, and exact row base `61`

## What not to reopen

Do not reopen `C2:F2F3..C2:F360` as the old seam; the honest closure now stops at exact `C2:F3CA`.
Do not keep the old off-by-one start guesses from pass 150: the exact local dispatch-table entries here are `F332`, `F337`, `F364`, and `F378`.
Do not treat exact `C2:F361..C2:F363` as stray bytes; it is a real exact width/flags wrapper feeding exact late entry `F364`.

## The real next seam now

1. next clean follow-on callable/helper family:
   - `C2:F3CB..C2:F421`

2. immediate structural anchors already visible there:
   - exact owner entry `C2:F3CB`
   - exact lookahead owner entry `C2:F422`

3. broader gameplay-facing nouns still worth tightening:
   - exact latch byte `0D77`
   - exact force-refresh byte `0D78`
   - exact packed coordinate words `5B/5D`
   - exact extent bytes `5F/60`
   - exact row-base / pointer words `61/63/65`
