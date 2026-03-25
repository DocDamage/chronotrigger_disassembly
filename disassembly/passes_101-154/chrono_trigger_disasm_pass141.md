# Chrono Trigger Disassembly — Pass 141

## Summary

Pass 141 closes the exact follow-on callable/helper family that pass 140 left open at `C2:DF76..C2:E095`, but the old seam end is structurally short again: the code stays live well past `E095`, and the exact callable/helper closure here runs cleanly through `C2:E162`. The resolved family is:

- one exact shared threshold-recovery owner at `C2:DF76..C2:DFC4`
- one exact local 5-word selector table at `C2:DFC5..C2:DFCE`
- one exact shared restore/clear/import helper at `C2:DFCF..C2:E000`
- one exact shared selector-packet wrapper at `C2:E001..C2:E011`
- one exact shared direct tail wrapper at `C2:E012..C2:E016`
- one exact `104D`-window export owner at `C2:E017..C2:E057`
- one exact shared `3404 + 8*slot` row-pointer helper at `C2:E058..C2:E071`
- one exact shared bounded `104D` export helper at `C2:E072..C2:E0A4`
- one exact negative refresh/export owner at `C2:E0A5..C2:E0F0`
- one exact short marker/finalizer wrapper at `C2:E0F1..C2:E107`
- one exact cyclic selector-step owner at `C2:E108..C2:E14F`
- one exact short latched-selector marker-writer wrapper at `C2:E150..C2:E162`

## Exact closures

### C2:DF76..C2:DFC4

This span freezes as the exact shared threshold-recovery owner reached from the earlier exact negative lanes at `D5D3` and `D683`.

- Begins `PHP ; SEP #$30`.
- Uses exact byte `04C9` as `X`, loads exact byte `7C00,X -> 0D4D`, and snapshots exact byte `54 -> 7F`.
- Seeds exact byte `54 = 0A`.
- Reenters exact `REP #$30`, seeds exact word `5D5A = 216F`, and uses overlapping exact `MVN 7E,7E` from `5D5A -> 5D5C` with exact count `001D`, producing a repeated exact `216F` fill across the downstream exact `5D5x` work band.
- Loads exact `X = 3BDE`, runs exact helper `F2DC` from exact byte `04C9`, and then always runs exact shared helper `E001`.
- Reruns exact helper `8881` from exact byte `04C9`.
- Doubles exact word `04CC` into `X`, uses exact local table `DFC5` to load one exact selector root, and emits that exact selector through exact helper `ED31`.
- Finishes through exact selector tail `X = FC3E ; JSR 8385`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact shared threshold-recovery owner that snapshots exact byte `7C00[04C9]` into `0D4D`, saves exact selector context through exact byte `7F`, seeds a repeated exact `216F` work band in `5D5A..`, reruns exact shared helper `E001`, emits one exact selector chosen from local table `DFC5`, and exits through exact selector `FC3E`.

### C2:DFC5..C2:DFCE

This span freezes as the exact local 5-word selector table consumed only by exact owner `DF76`.

- Exact words: `C2E8, C2F5, C2F5, C302, C302`.
- Strongest safe reading: exact local 5-word selector table keyed by exact word `04CC` for the exact `DF76` threshold-recovery owner.

### C2:DFCF..C2:E000

This span freezes as the exact shared restore/clear/import helper reached from the earlier exact tails at `D642` and `D6BA`.

- Begins `PHP`.
- Restores exact byte `7F -> 54`.
- Reenters exact `REP #$30`, clears exact word `5D5A`, then uses overlapping exact `MVN 7E,7E` from `5D5A -> 5D5C` with exact count `001D`, yielding an exact zero-filled work band across the downstream exact `5D5x` range.
- Because the exact block-copy count exhausts, stores exact word `FFFF -> 83`.
- Seeds exact `X = 3046`, exact `Y = 2C53`, exact source descriptor `A = 7E63`, and runs exact helper `F114`.
- Emits exact selector `FC3E`, then exact selector `FBE3`, through exact helper `8385`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact shared restore/clear/import helper that restores exact selector byte `54`, zero-fills the exact `5D5x` work band, seeds exact word `83 = FFFF`, imports one exact block through exact helper `F114` using exact `3046 / 2C53 / 7E63`, and exits through exact selectors `FC3E` then `FBE3`.

### C2:E001..C2:E011

This span freezes as the exact shared selector-packet wrapper used by both the earlier exact `DA01` dispatch family and the exact `DF76` owner.

- Begins `PHP ; REP #$30`.
- Seeds exact `X = C2DE` and emits that exact selector through exact helper `ED31`.
- Seeds exact `X = FBEA` and emits that exact selector through exact helper `8385`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact shared selector-packet wrapper that emits exact selector `C2DE` and then exits through exact selector `FBEA`.

### C2:E012..C2:E016

This span freezes as the exact shared direct tail wrapper reached from the earlier exact tails at `D602` and `DB10`.

- Loads exact accumulator from exact word `51`.
- Tail-jumps directly to exact helper `F2F3`.

Strongest safe reading: exact one-shot direct tail wrapper that forwards exact word `51` into exact helper `F2F3`.

### C2:E017..C2:E057

This span freezes as the exact `104D`-window export owner reached from the earlier exact `D546` clear-path service lane.

- Begins `PHP ; SEP #$20`.
- Snapshots exact byte `54 -> 80`, seeds exact byte `68 = 06`, and mirrors exact byte `79 -> 54`.
- Seeds exact direct-page exact word `02 = 1004` and exact loop index `04 = 85`.
- Walks compact exact list `104D[04]` until the exact negative terminator or exact bound `04 == 1055`.
- For each exact live entry, stages that exact entry into exact byte `00`, runs exact helper `FFF628`, mirrors exact loop index `04 -> 00`, and runs exact shared helper `E058`.
- Increments exact loop index `04` and repeats while the exact bound still holds.
- Finishes by emitting exact selector `C2D5` through exact helper `ED31`, then exact selector `FBE3` through exact helper `8385`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact `104D`-window export owner that saves/restores exact selector context through exact bytes `80/54`, seeds exact state byte `68 = 06`, walks the compact exact `104D` list from exact start index `85` up to exact bound `1055`, runs exact helper `FFF628` on each live entry, materializes the matching exact `3404` row slot through exact helper `E058`, and exits through exact selectors `C2D5` then `FBE3`.

### C2:E058..C2:E071

This span freezes as the exact shared row-pointer helper used by exact owners `D6C3`, `E017`, and `E072`.

- Begins `PHP ; REP #$30`.
- Loads exact word `00`, masks it down to exact byte width, shifts it left three times, adds exact base word `3404`, and stores the exact result into exact word `61`.
- Seeds exact `X = 0002`, loads exact direct-page exact word `02`, and runs exact helper `EC93`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact shared row-pointer helper that maps exact byte `00` to exact destination base `3404 + 8*00`, stages that exact row base into exact word `61`, and then runs exact helper `EC93` from exact descriptor word `02`.

### C2:E072..C2:E0A4

This span freezes as the exact shared bounded `104D` export helper used by exact owners `D715`, `E017`, and `E108`.

- Begins `PHP ; SEP #$20`.
- Seeds exact byte `22 = 51` and snapshots exact byte `03 -> 05`.
- When exact byte `22 == 71`, clears exact byte `03` for that exact slot pass.
- Per exact slot, stages exact byte `22 -> 00` and runs exact shared helper `E058`.
- Then reloads exact `X = 22`, stages exact byte `104D,X -> 00`, and runs exact helper `FFF628`.
- Restores exact byte `05 -> 03`, increments exact byte `22`, and loops while exact byte `22 < 85`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact shared bounded export helper that iterates exact slot byte `22` from exact start `51` up to exact bound `85`, temporarily clears exact byte `03` only on the exact slot matching exact byte `71`, materializes one exact `3404` row through exact helper `E058`, and then stages the matching exact compact-list entry `104D[22]` through exact helper `FFF628`.

### C2:E0A5..C2:E0F0

This span freezes as the exact negative refresh/export owner reached from the earlier exact negative lane at `D6E0`.

- Begins `PHP ; REP #$30`.
- Clears exact local work band `0D4D..0D51` by clearing exact word `0D4D` and using overlapping exact `MVN 7E,7E` from `0D4D -> 0D4F` with exact count `0004`.
- Reenters exact `SEP #$20`, derives exact start byte `71 = 54 - 0C`, and runs exact helper `8820`.
- Emits exact selector `C309` through exact helper `ED31`.
- Runs exact helper `A6F0` with exact `X = 3664`, then exact helper `821E`, then exact shared helper `E0F1`.
- Seeds exact byte `0D13 = 55`, clears exact byte `0D0B`, decrements exact byte `0D78`, and reruns exact helper `F2F3` with exact accumulator `00`.
- Seeds exact direct-page exact word `02 = 1004` and runs exact shared helper `E072`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact negative refresh/export owner that clears exact local work band `0D4D..0D51`, derives exact start slot `71 = 54 - 0C`, reruns the exact `8820 / C309 / 3664 / 821E` service chain, then runs exact helper `E0F1`, signals exact byte `0D13 = 55`, decrements exact byte `0D78`, reruns exact helper `F2F3(00)`, and exports the exact `104D` window through exact helper `E072`.

### C2:E0F1..C2:E107

This span freezes as the exact short marker/finalizer wrapper used by the earlier exact owner `D715` and the just-closed exact owner `E0A5`.

- Begins `PHP ; REP #$30`.
- Runs exact shared helper `E150`.
- Seeds exact word `0D92 = 2A68`.
- Runs exact helper `A463`.
- Exits through exact selector tail `X = FBF1 ; JSR 8385`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact short marker/finalizer wrapper that refreshes the exact `77`-latched marker lane through exact helper `E150`, seeds exact word `0D92 = 2A68`, runs exact helper `A463`, and exits through exact selector `FBF1`.

### C2:E108..C2:E14F

This span freezes as the exact cyclic selector-step owner reached from the earlier exact owner `D71F`.

- Begins `PHP ; SEP #$30`.
- Uses exact byte `71` as the current exact step index.
- Masks exact byte `0D1D & 03`; exact zero returns immediately.
- Exact bit `0D1D.bit1` selects the direction: one exact lane steps exact byte `71` backward with wrap to exact byte `84`, the other steps it forward with wrap to exact byte `00` once exact bound `85` is reached.
- When the stepped exact index matches the old exact `71`, returns immediately.
- Otherwise stores the stepped exact index back into exact byte `71`, reenters exact `REP #$10`, and runs exact helpers `EAC2`, `8820`, `ED31(C309)`, and `A6F0(3664)`.
- Seeds exact direct-page exact word `02 = 1004`, runs exact shared helper `E072`, then exact shared helper `E150`, then exact helper `821E`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact low-2-bits-gated cyclic selector-step owner that moves exact byte `71` one step backward or forward inside exact range `00..84`, reruns the exact `EAC2 / 8820 / C309 / 3664` service chain whenever the step actually changes the exact index, exports the exact active window through exact helper `E072`, refreshes the exact `77`-latched marker lane through exact helper `E150`, and finishes with exact helper `821E`.

### C2:E150..C2:E162

This span freezes as the exact short latched-selector marker-writer wrapper used by exact owners `E0F1` and `E108`.

- Begins `PHP ; SEP #$20`.
- Mirrors exact byte `54 -> 0077`.
- Reenters exact `REP #$30`, seeds exact `X = 3624`, and runs exact helper `A3ED`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact short wrapper that mirrors exact selector byte `54` into exact latch byte `0077` and reruns exact helper `A3ED` with exact descriptor `3624`.

## Honest remaining gap

- the old seam `C2:DF76..C2:E095` is now closed more honestly as `C2:DF76..C2:E162`
- the next follow-on family begins at exact owner `C2:E163` and visibly pulls in downstream local tables and helper/dispatch code well beyond the old `E095` seam hint
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
