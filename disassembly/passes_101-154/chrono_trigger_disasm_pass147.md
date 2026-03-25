# Chrono Trigger Disassembly — Pass 147

## Summary

Pass 147 closes the callable/helper family that pass 146 left open at `C2:EB9B..C2:EC37`, and it also closes the immediate callable spillover just beyond that old seam through `C2:ED30`.

The resolved family is:

- one exact WRAM strip / stepped-loop seed helper at `C2:EB9B..C2:EC37`
- one exact six-row ascending-word writer plus FF-bank block importer at `C2:EC38..C2:EC92`
- one exact counted row-stride wrapper at `C2:EC93..C2:ECAB`
- one exact paired odd-byte fill helper at `C2:ECAC..C2:ECC1`
- one exact paired odd-byte nibble-merge helper at `C2:ECC2..C2:ECDA`
- one exact bank-7E setup owner deriving `0D47/0D48` before helper chain `EDF6 -> EE7F -> ED08` at `C2:ECDB..C2:ED07`
- one exact FF-bank 16-byte importer keyed by `0D8C/0D48` at `C2:ED08..C2:ED30`

## Exact closures

### C2:EB9B..C2:EC37

This span freezes as the exact helper family root behind the already-frozen callers at `9F5B`, `AC8A`, `B753`, `D84F`, and `D932`.

Key facts now pinned:
- Begins `PHP ; REP #$30`.
- Seeds exact word `9694 = 969A`.
- Uses exact caller-owned words `9696` and `9698` plus exact count byte `0DAA`.
- Copies an exact `3 * 0DAA` byte prefix from exact caller source base `9696` into exact WRAM band rooted at `9793` through exact `MVN 7E,7E`.
- Then uses the same exact caller-owned metadata to materialize the downstream exact tail block into exact WRAM band `969A + 3*0DAA`.
- Patches exact metadata words in the exact `9790/9791` family, including:
  - exact word write at `9791 + 3*0DAA`
  - exact head-word rewrite at exact `9791`
  - exact byte writes `9790 = 0C` and `9790 + 3*0DAA = 0C`
- Exact control bit `5A.bit2` chooses exact signed step word `0D22 = +0003` versus `0D22 = -0003`.
- Clears exact byte `0DA9`.
- Seeds exact loop word `0D24 = 0004`.
- When exact byte `00FD == 05`, rewrites that exact byte to `04`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact `9696/9698/0DAA`-driven WRAM strip/template materializer that copies a caller-owned exact 3-byte record prefix and trailing block into exact work bands `9793/969A`, patches exact `9790/9791` metadata, and seeds exact control words `0D22/0DA9/0D24` for the downstream exact stepped `EB1F` lane.

### C2:EC38..C2:EC92

This span freezes as the exact callable spillover immediately beyond the old pass-146 seam end.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Uses exact selector byte `0D46` to load one exact seed byte from exact FF-bank table `FF:CE70,X`, mirroring that exact byte into direct-page exact word/bytes `00/01`.
- Seeds exact row count `Y = 0006`.
- Uses exact caller-owned destination base word `61`.
- Across six exact rows spaced by exact stride `0x0040`, writes six consecutive exact words to offsets `+00/+02/+04/+06/+08/+0A`, carrying the incremented exact word across the whole six-row build.
- Uses exact low three bits of exact byte/word `0D46 & 0007` to select one exact FF-bank source pointer from exact table `FF:CE78`.
- Uses exact caller-owned exact byte/word `01`, masked as exact `01 & 001C`, to choose exact WRAM destination band `9480 + 8*(01 & 001C)`.
- Copies exact `0x0020` bytes from that exact FF-bank source block into the chosen exact WRAM destination through exact `MVN 7E,FF`.
- Increments exact byte `0D15`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact six-row ascending-word writer plus exact FF-bank `0x20`-byte importer keyed by exact selector byte `0D46`, exact caller destination base `61`, and exact caller row/destination selector byte `01`.

### C2:EC93..C2:ECAB

This span freezes as the exact counted wrapper immediately behind the importer above.

Key facts now pinned:
- Begins `PHP ; REP #$30`.
- Preserves the exact incoming accumulator `A` on the stack.
- Each exact pass reloads that preserved exact accumulator from exact stack-relative source, pushes exact caller-owned `X`, and runs exact helper `ECC2`.
- After each exact helper pass, advances exact destination base word `61 += 0040`.
- Decrements exact caller-owned loop counter `X` and repeats until exact `X == 0`.
- Restores exact preserved accumulator and exits `PLP ; RTS`.

Strongest safe reading: exact counted row-stride wrapper that repeatedly replays one exact caller-owned descriptor through exact helper `ECC2` while stepping exact destination base word `61` by exact stride `0x0040`.

### C2:ECAC..C2:ECC1

This span freezes as the exact paired odd-byte fill helper shared by several older callers.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Uses exact low byte of caller-owned accumulator `A` as an exact loop count via exact `TAY`.
- Switches exact X/Y width to 16-bit while keeping exact 8-bit accumulator mode.
- Uses exact `XBA` so the exact high byte of caller-owned accumulator `A` becomes the exact written byte value.
- Uses exact destination base word `61`.
- For exact `count` passes, writes that exact byte to both exact odd-byte lanes:
  - exact `61 + 0001 + 2*n`
  - exact `61 + 0041 + 2*n`
- Advances exact `X` by exact stride `2` each pass.
- Exits `PLP ; RTS`.

Strongest safe reading: exact paired odd-byte fill helper that interprets exact caller word `A` as `(value_hi,count_lo)` and writes the exact high byte into both exact odd-byte twin lanes rooted at exact base word `61`.

### C2:ECC2..C2:ECDA

This span freezes as the exact paired odd-byte nibble-merge helper directly behind `ECAC`.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Uses exact low byte of caller-owned accumulator `A` as an exact loop count via exact `TAY`.
- Uses exact destination base word `61`.
- For each exact pass:
  - reads the current exact odd byte at exact `61 + 0001 + 2*n`
  - preserves its exact low nibble through exact `AND #0F`
  - merges in exact caller-owned higher bits through exact `ORA` from exact stack-relative source
  - writes the merged exact byte back to exact odd-byte lane `61 + 0001 + 2*n`
- Advances exact `X` by exact stride `2` each pass and repeats until the exact counter expires.
- Exits `PLP ; RTS`.

Strongest safe reading: exact counted odd-byte nibble-merge helper that preserves the existing exact low nibble in the exact twin-lane odd-byte strip while forcing in exact caller-owned upper bits.

### C2:ECDB..C2:ED07

This span freezes as the exact bank-7E setup owner in front of helper chain `EDF6 -> EE7F -> ED08`.

Key facts now pinned:
- Begins `PHB ; PHP ; SEP #$20`.
- Temporarily sets exact data bank to exact `7E`.
- Loads exact state byte `0D8C`.
- Computes exact word `0D47 = 20 * 0D8C` through the exact `4x + 16x` split-and-add lane.
- Computes exact byte/word `0D48 = (((79 + 1) << 2) | 03)`.
- Runs exact helper chain:
  - exact `EDF6`
  - exact `EE7F`
  - exact `ED08`
- Restores exact flags and exact data bank.
- Exits `RTS`.

Strongest safe reading: exact bank-7E setup owner that derives exact staging words `0D47/0D48` from exact state bytes `0D8C/79`, then runs the exact `EDF6 -> EE7F -> ED08` helper chain.

### C2:ED08..C2:ED30

This span freezes as the exact FF-bank importer tail used both locally and by older callers.

Key facts now pinned:
- Begins `PHP ; REP #$30`.
- Uses exact low three bits of exact state word/byte `0D8C & 0007`.
- Computes exact FF-bank source base `B210 + 0x0010 * (0D8C & 0007)`.
- Uses exact state word/byte `0D48 & 001C`, scaled by exact stride `8`, to choose exact WRAM destination band `9490 + 8*(0D48 & 001C)`.
- Copies exact `0x0010` bytes from the computed exact FF-bank source block into that exact WRAM destination through exact `MVN 7E,FF`.
- Increments exact byte `0D15`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact FF-bank 16-byte importer keyed by exact state bytes `0D8C/0D48`, used both as the tail of exact owner `ECDB` and as a direct helper by older callers.

## Honest remaining gap

- the old seam `C2:EB9B..C2:EC37` was too short
- the honest closure for this pass runs through exact `C2:ED30`
- the next clean follow-on callable/helper family now begins at exact `C2:ED31`
- the next obvious callable band is `C2:ED31..C2:EE7F`
- exact helper/owner anchors immediately visible there are:
  - exact heavy shared helper entry `C2:ED31`
  - exact helper entry `C2:EDF6`
  - exact helper entry `C2:EE7F`
