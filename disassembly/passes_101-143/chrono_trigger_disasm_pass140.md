# Chrono Trigger Disassembly — Pass 140

## Summary

Pass 140 closes the exact follow-on callable/helper family that session-7 left open at `C2:DE98..C2:DF76`, with one more structural correction up front: the old seam end was still one byte too long. `C2:DF76` is the first byte of the next callable owner, not part of the old family. The clean closure resolves into:

- one exact `0D88`-checked sibling refresh owner at `C2:DE98..C2:DECB`
- one shared exact `5600/5700` build-refresh helper at `C2:DECC..C2:DF30`
- one shared exact eight-pass export driver at `C2:DF31..C2:DF50`
- one shared exact `5600` entry loader/materializer helper at `C2:DF51..C2:DF75`

## Exact closures

### C2:DE98..C2:DECB

This span freezes as the exact sibling refresh owner that the earlier `D585` negative path jumps into.

- Begins `PHP ; SEP #$20`.
- Seeds exact word `0D92 = 2AF0`.
- Emits exact selector packet `C2CB` through exact helper `ED31`.
- When exact byte `0D88` is zero, clears exact bytes `1042` and `1043`.
- Mirrors exact byte `1042 -> 54`.
- Runs the shared exact helper `DECC`.
- Seeds exact byte `0D78 = FF`.
- Runs the shared exact helper `DF31`, then exact helper `8B93`.
- Restores flags with exact `PLP`, then exits through exact selector tail `X = FBE3 ; JMP 8385`.

Strongest safe reading: exact `0D88`-checked sibling refresh owner that normalizes exact bytes `1042/1043`, runs the shared exact `DECC` strip/build refresh helper, reruns the shared exact `DF31` export driver, and exits through exact selector `FBE3`.

### C2:DECC..C2:DF30

This span freezes as the shared exact `5600/5700` build-refresh helper used by both `D690` and `DE98`.

- Begins `PHP ; REP #$20`.
- Clears exact word `5600`, then uses overlapping exact `MVN 7E,7E` from `5600 -> 5602` with exact count `0005`, producing an exact zero-filled startup band across `5600..5607`.
- Reenters exact `SEP #$30`, seeds exact byte `0DDC = 07`, clears exact `X`/`Y` through `LDX #00 ; TXY`, and then scans the paired exact tables `2500,X` and `2400,X`.
- Always stages exact byte `2500,X -> 5700,Y` first.
- When exact byte `2400,X == 00`, stops the scan.
- When exact byte `2400,X >= F2`, discards the candidate and advances only exact source index `X`.
- When exact byte `2400,X < F2`, writes that accepted exact byte into `5600,Y`, uses it as an exact index into `7700`, and only advances exact destination index `Y` when exact bit `7700[accepted] & 04` is clear.
- Stores the final exact destination index `Y -> 1049`.
- Writes exact terminator byte `00 -> 5600,Y`.
- Runs exact helper `DD40`.
- Clamps exact byte `54` down against exact byte `0DDC = 07`.
- Compares direct-page exact byte `57` against exact byte `1043`, raises exact byte `1043` when the direct-page value is larger, and mirrors the final exact `1043` into exact bytes `0DD9` and `0D95`.
- Exits `PLP ; RTS`.

Strongest safe reading: shared exact `5600/5700` build-refresh helper that zero-seeds the `5600` work band, filters/stages candidates out of exact paired tables `2400/2500`, records the exact resulting strip length in `1049`, terminates exact strip `5600`, reruns exact helper `DD40`, clamps exact byte `54`, and updates the exact `1043 / 0DD9 / 0D95` window/latch bytes from the downstream direct-page result.

### C2:DF31..C2:DF50

This span freezes as the shared exact eight-pass export driver reused by `D8B2` and `DE98`.

- Begins `PHP ; REP #$30`.
- Seeds exact word `61 = 2F5C` and clears exact word `22`.
- Repeatedly runs exact helper `DF51`.
- After each exact pass, advances exact word `61 += 0080` and increments exact word `22`.
- Loops until exact word `22 == 0008`, producing exact destination rows `2F5C, 2FDC, 305C, 30DC, 315C, 31DC, 325C, 32DC`.
- Exits `PLP ; RTS`.

Strongest safe reading: shared exact eight-pass `0x80`-stride export driver over the exact `2F5C..32DC` destination band, using exact helper `DF51` as its per-pass materializer.

### C2:DF51..C2:DF75

This span freezes as the shared exact `5600` entry loader/materializer helper used by `DF31`.

- Begins `PHP ; REP #$31`.
- Computes exact source index `Y = (1043 + 22) & 00FF`.
- Loads exact byte `5600,Y -> 04C9`.
- Doubles the accepted exact source byte into `X`.
- Loads exact word `7800,X`, shifts it right once, adds exact word `51`, and stores the exact result into `1044`.
- Runs exact helper `DD56`.
- Exits `PLP ; RTS`.

Strongest safe reading: shared exact `5600` strip-entry loader that stages exact byte `04C9` from exact strip `5600`, derives exact word `1044` from exact table `7800` plus exact base word `51`, and then enters the shared exact `DD56` hardware-math materializer.

## Honest remaining gap

- the old seam `C2:DE98..C2:DF76` is now closed, but `C2:DF76` itself is the first byte of the next live callable owner
- the next follow-on family visibly begins with an exact owner at `DF76`, a local exact pointer table rooted at `DFC5`, a shared helper at `DFCF`, and more downstream callable/helper code through at least `E070`
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
