# Chrono Trigger Disassembly — Pass 144

## Summary

Pass 144 closes the callable/helper family that pass 143 left open at `C2:E60B..C2:E760`, and it corrects the seam at both ends. The seam does **not** begin with one strange stack-relative code opener. It begins with one exact local 4-word dispatch table at `C2:E60B..C2:E612`, followed by a short wrapper at `C2:E613`. The old seam end at `C2:E760` was also too short, because the exact `E743` helper/owner runs cleanly through `PLP ; RTS` at `C2:E840`.

The resolved family is:

- one exact local 4-word dispatch table at `C2:E60B..C2:E612`
- one exact `E7C3 -> INC 68 -> 83B2` wrapper at `C2:E613..C2:E61A`
- one exact `0420/0D1D`-gated dispatcher with special exact `E891` fast lane at `C2:E61B..C2:E682`
- one exact slot-scan / immediate `1E00/1E01` packet emitter plus `C70004` service tail at `C2:E683..C2:E6AD`
- one exact sibling `0D1D`-gated dispatcher with exact `FFFAED` negative lane and exact overflow handoff at `C2:E6AE..C2:E6DC`
- one exact overflow clear/reset wrapper at `C2:E6DF..C2:E704`
- one exact `0D1D`-gated service owner that forces exact selector `54 = 05` on overflow and exits through exact `FC0D` at `C2:E705..C2:E742`
- one exact cyclic occupied-slot search / state-refresh / strip-expansion owner at `C2:E743..C2:E7C2`
- one exact `30:7FE0`-indexed setup/export owner at `C2:E7C3..C2:E840`

## Exact closures

### C2:E60B..C2:E612

This span is not code. It freezes as the exact local 4-word dispatch table at the front of the pass-143 live seam.

Exact words now pinned:
- `E613`
- `E61B`
- `E6AE`
- `E705`

Strongest safe reading: exact local 4-word dispatch table selecting the four downstream callable entries resolved in this pass.

### C2:E613..C2:E61A

This span freezes as the exact short wrapper immediately behind the dispatch table.

Key facts now pinned:
- Begins `JSR E7C3`.
- Increments exact byte `68`.
- Exits through exact jump `83B2`.

Strongest safe reading: exact short wrapper that reruns exact setup/export owner `E7C3`, bumps exact phase/count byte `68`, and rejoins the shared exact `83B2` tail.

### C2:E61B..C2:E682

This span freezes as the exact `0420/0D1D`-gated dispatcher at the front of the family.

Key facts now pinned:
- Begins by loading exact word/byte `0420`.
- When exact byte `0420 == 30` and the live exact selector byte `54 < 03`, seeds exact byte `68 = 03`, reruns exact helper `EAC2`, and exits through exact jump `E891`.
- Otherwise runs exact helper `E984` and tests exact status byte `0D1D` with `BIT`.
- Non-negative path runs exact helper `E743`, compares exact bytes `81` and `54`, reruns exact helper `EAC2` only on mismatch, and returns.
- Negative path always reruns exact helper `EAC2`, then in exact 8-bit mode splits again:
  - when exact byte `54 < 03`, mirrors exact byte `54 -> 79` and `54 -> 0414`, runs exact long helper `FF:FAA3`, and braids into the shared exact `E694` service tail
  - when exact byte `54 >= 03`, runs exact helper `956E`, seeds exact long byte `7F:0061 = 01`, mirrors exact long byte `30:7FE1 -> 299E`, and then:
    - when exact long byte `30:7FE2 != 0` and exact byte `9392 == 78`, clears exact byte `0D4C`, runs exact helper `E841`, increments exact byte `68`, and returns
    - otherwise falls through the shared exact `E683` slot-scan / service tail

Strongest safe reading: exact `0420/0D1D`-gated dispatcher with one exact `0420 == 30` fast lane into exact jump `E891`, a clear exact `E743` compare lane, and a negative exact service lane that chooses `FF:FAA3` versus the exact `956E / 30:7FE1 / E841` branch before the shared service tail.

### C2:E683..C2:E6AD

This span freezes as the exact slot-scan / immediate packet / service tail shared by the front dispatcher family.

Key facts now pinned:
- Scans exact slot bytes `0D49[0..2]` for the first exact nonzero entry.
- When no exact nonzero slot is found, forces exact `X = 00`.
- Mirrors the exact final slot index into exact word/byte `0414`.
- Seeds exact bytes:
  - `1E00 = F3`
  - `1E01 = (2990 & 08)`
- Runs exact long helper `C7:0004`.
- Mirrors exact byte `0D00 -> 29AD`.
- Exits through exact jump `8320`.

Strongest safe reading: exact shared slot-scan / immediate `1E00/1E01` packet emitter that chooses one exact active slot out of `0D49[0..2]`, runs exact helper `C7:0004`, mirrors exact byte `0D00 -> 29AD`, and exits through exact jump `8320`.

### C2:E6AE..C2:E6DC

This span freezes as the exact sibling `0D1D`-gated dispatcher directly behind the shared service tail.

Key facts now pinned:
- Begins `JSR E984 ; BIT 0D1D`.
- Non-negative / non-overflow path runs exact helper `E743`, compares exact bytes `81` and `54`, reruns exact helper `EAC2` only on mismatch, and returns.
- Negative path reruns exact helper `EAC2`, enters exact 8-bit mode, and then:
  - when exact byte `54 >= 03`, exact-jumps into the shared exact `E683` service tail
  - when exact byte `54 < 03`, mirrors exact byte `54 -> 79` and `54 -> 0414`, runs exact long helper `FF:FAED`, and exact-jumps into the shared exact `E694` packet/service tail
- Overflow path hands off into the downstream exact clear/reset wrapper at `E6DF`.

Strongest safe reading: exact sibling `0D1D`-gated dispatcher that either returns after the clear exact `E743` compare lane, chooses an exact `FF:FAED` negative-service lane for selectors below `03`, reuses the shared exact `E683` service tail for selectors at or above `03`, or hands overflow into exact wrapper `E6DF`.

### C2:E6DF..C2:E704

This span freezes as the exact overflow clear/reset wrapper used by the sibling dispatcher above.

Key facts now pinned:
- Begins by rerunning exact helper `EAC2`.
- Decrements exact bytes `68` and `0D4C`.
- Forces exact selector byte `54 = 03`.
- In exact 16-bit mode clears exact word `52C0` and performs one exact overlapping same-bank clear-propagation move `52C0 -> 52C2` for exact length `00FD`, materializing a zeroed exact `52C0`-family work band.
- Clears exact word/byte `0D84`.
- Emits exact selector `FC1B` through exact helper `8385`.

Strongest safe reading: exact overflow clear/reset wrapper that backs down exact state bytes `68/0D4C`, forces exact selector `54 = 03`, zeroes the exact `52C0`-family work band, clears exact byte `0D84`, and exits through exact selector `FC1B`.

### C2:E705..C2:E742

This span freezes as the exact `0D1D`-gated service owner at the back half of the family.

Key facts now pinned:
- Begins `JSR E984 ; BIT 0D1D`.
- Non-negative / non-overflow path compares exact bytes `54` and `81`, reruns exact helper `EAC2` only on mismatch, and returns.
- Overflow path forces exact selector byte `54 = 05`.
- The shared negative/overflow lane then:
  - emits exact selector `C191` through exact helper `ED31`
  - when exact selector byte `54 == 04`, runs exact helper `E8B7`
  - seeds exact byte `0D13 = 5B`
  - mirrors exact byte `0F00 -> 54`
  - seeds exact byte `68 = 01`
  - reruns exact helper `EAC2`
  - exits through exact selector `FC0D` via exact helper `8385`

Strongest safe reading: exact `0D1D`-gated service owner that either returns after an exact `54/81` compare, or on the negative/overflow lane emits exact selector `C191`, optionally runs exact helper `E8B7` for exact selector `54 == 04`, stamps exact byte `0D13 = 5B`, mirrors exact byte `0F00 -> 54`, and exits through exact selector `FC0D`.

### C2:E743..C2:E7C2

This span freezes as the exact cyclic occupied-slot search / state-refresh / strip-expansion owner repeatedly reused by the just-resolved dispatchers.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Uses the live exact selector byte `54` as the current exact slot index.
- Repeatedly probes exact slot bytes `0D49[54]` until one exact nonzero slot is found.
- When the exact current slot is empty, uses exact bit test `5A & 08` to choose whether the exact cyclic step is `+1 mod 4` or `-1 mod 4`, then writes the exact wrapped result back into exact selector byte `54` and retries.
- When exact long byte `30:7FE2 != 0`, exact selector byte `54 == 03`, and exact low bits `5A & 03 != 0`, flips exact byte `9392 ^= 70` and reruns exact helper `EAC2` before continuing.
- Mirrors exact byte `54 -> 79`, derives exact next-slot byte `7F = (54 + 1) & 03`, and runs exact helper `CFFB`.
- In exact 16-bit mode clears exact word `3200`, performs one exact overlapping same-bank block move `3200 -> 3202` for exact length `023D`, then copies exact `0x0012` bytes from the exact shifted `3200` strip into exact downstream buffers `5248` and `5288`.
- Runs exact helper `D36C`.
- Emits exact selector chain `FBDC -> FC0D -> FC29` through exact helper `8385`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact cyclic occupied-slot search / state-refresh owner that walks the live `0D49` slot ring in the direction chosen by exact bit `5A.3`, optionally flips exact byte `9392`, rebuilds the exact `3200` strip, expands it into exact downstream buffers `5248/5288`, refreshes through exact helper `D36C`, and exits through the exact `FBDC / FC0D / FC29` selector chain.

### C2:E7C3..C2:E840

This span freezes as the exact `30:7FE0`-indexed setup/export owner called from the front wrapper at `E613`.

Key facts now pinned:
- Begins `PHP ; SEP #$20`.
- Emits exact selector `C0ED` through exact helper `ED31`.
- Runs exact local helper `D10D`.
- Mirrors exact long byte `30:7FE0 -> 79`.
- ORs exact slot bytes `0D49 / 0D4A / 0D4B`; when that exact combined result is zero, forces exact slot byte `79 = 03`.
- Mirrors exact byte `79 -> 54`.
- Runs exact helper `D36C`.
- Clears exact byte `7E`.
- Emits exact selector `C322` through exact helper `ED31`.
- Runs exact helper `E743`.
- Runs exact helper `86DD`.
- When exact long byte `30:7FE2 != 0`, emits exact selector `C36B` through exact helper `ED31`.
- Increments exact byte `0D15`.
- Seeds exact byte `0D13 = 1B`.
- In exact 16-bit mode copies exact `0x0010` bytes from exact source block `FF:CC74` into exact WRAM destination `94C0`, then copies exact `0x0020` bytes from exact source block `FF:CE30` into exact WRAM destination `9560`.
- Emits exact selector chain `FC53 -> FBCE -> FBF8 -> FC14` through exact helper `8385`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact `30:7FE0`-indexed setup/export owner that chooses one exact live slot, drives exact helper `D10D`, refreshes exact downstream state through exact helper `D36C` and exact owner `E743`, stages exact blocks `FF:CC74 -> 94C0` and `FF:CE30 -> 9560`, then exits through the fixed exact `FC53 / FBCE / FBF8 / FC14` selector chain.

## Honest remaining gap

- the old seam `C2:E60B..C2:E760` is now closed more honestly as `C2:E60B..C2:E840`
- the old seam start at `C2:E60B` was not one strange code opener; it begins with an exact local 4-word dispatch table at `C2:E60B..C2:E612`
- the old seam end at `C2:E760` cut the exact `E743` owner in half
- the next clean follow-on family now begins at `C2:E841`, where exact helper entry `E841`, exact service/helper entry `E8B7`, and the heavily reused exact tail at `E923` are the most obvious immediate anchors
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
