# Chrono Trigger Disassembly — Pass 139

## Summary

Pass 139 closes the exact follow-on callable/helper family that pass 138 left open at `C2:DC7B..C2:DD80`, but the first correction is structural again: that seam does **not** stop at `DD80`. The old seam end landed in the middle of a larger exact hardware-math helper. The clean closure resolves into:

- one exact refresh/materializer owner at `C2:DC7B..C2:DCBF`
- two exact local strip helpers at `C2:DCC0..C2:DD01`
- one shared exact eight-pass export driver at `C2:DD02..C2:DD1D`
- two shared exact materializer helpers at `C2:DD20..C2:DD97`
- one exact `104D`-driven refresh owner at `C2:DD98..C2:DE1C`
- one exact local 4-byte table at `C2:DE1D..C2:DE20`
- two exact downstream helpers at `C2:DE21..C2:DE97`

## Exact closures

### C2:DC7B..C2:DCBF

This span freezes as the exact refresh/materializer owner entered from `C2:D57E`.

- Begins `PHP ; SEP #$20`.
- Seeds exact byte `0D78 = FF`, clears exact byte `54`, seeds exact word `0D92 = 2AF0`, and runs exact helper `ED31` with exact selector word `C2C1`.
- When exact byte `0D88` is zero, clears exact bytes `1040` and `1041`.
- Mirrors exact byte `1040 -> 54` and exact byte `1041 -> 0D95`.
- Runs exact helper `DD02`, loads exact `Y = 104A`, runs exact helper `DD40`, then exact helper `DCDA`.
- Finishes with exact helper `8B93` and exact selector tail `X = FBE3 ; JSR 8385`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact refresh/materializer owner that normalizes exact bytes `1040/1041`, reruns the shared exact `DD02` export driver, prepares one exact `EA81` service through exact helper `DD40`, refreshes exact downstream state through `DCDA`, and exits through exact selector `FBE3`.

### C2:DCC0..C2:DCD7

This span freezes as an exact local tail-clear helper for the `1000` strip.

- Begins `PHP ; SEP #$30`.
- Scans exact byte strip `1000,Y` upward from exact `Y = 00` until the first exact zero entry.
- Stores that exact first-zero slot index into exact byte `104A`.
- Clears the exact tail of `1000,Y` from that first zero slot through exact upper bound `Y == 20`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact first-zero-slot scanner and tail-clear helper for the `1000` strip that also seeds exact byte `104A`.

### C2:DCD8..C2:DD01

This span freezes as the exact `1000 -> 1020` translation helper.

- Begins `PHP ; SEP #$30`.
- Walks exact live entries in exact strip `1000,Y` until the exact zero terminator.
- For each exact source byte, scans exact lookup table `2400,X` for the matching exact selector byte.
- When a match is found, loads exact mapped byte `2500,X`; exact zero mapped bytes do **not** terminate the search and instead continue scanning for another exact match.
- Writes the accepted exact mapped byte into exact strip `1020,Y`.
- When no exact match exists, writes exact byte `00` into exact strip `1020,Y`.
- Exits `PLP ; RTS` when exact strip `1000` terminates.

Strongest safe reading: exact `1000`-to-`1020` lookup translation helper using paired exact tables `2400/2500`, with exact zero mapped values treated as “keep searching.”

### C2:DD02..C2:DD1D

This span freezes as the shared exact eight-pass export driver used by both `D7CF` and `DC7B`.

- Begins `PHP ; REP #$30`.
- Seeds exact word `61 = 2F5C` and clears exact word `22`.
- Repeatedly runs exact helper `DD20`.
- After each exact pass, increments exact word `22` and advances exact word `61 += 0080`.
- Loops while exact word `61` remains below exact bound `335C`, producing exact destinations `2F5C, 2FDC, 305C, 30DC, 315C, 31DC, 325C, 32DC`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact eight-pass `0x80`-stride export driver that iterates the shared exact `DD20` materializer across the `2F5C..32DC` destination band.

### C2:DD20..C2:DD3F

This span freezes as the shared exact per-pass entry loader/materializer helper.

- Begins `PHP ; SEP #$20`.
- Uses exact byte `1041 + 22` as the live exact source index.
- Loads exact byte `1000,Y -> 04C9`.
- Reenters exact `REP #$30`, doubles the exact source byte into exact `Y`, loads exact word `6E00,Y -> 1044`, and runs exact helper `DD56`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact per-pass strip-entry loader that selects one exact `1000` entry, loads its paired exact word from `6E00`, stages exact bytes `04C9/1044`, and then enters the shared exact `DD56` hardware-math materializer.

### C2:DD40..C2:DD55

This span freezes as the exact local prep wrapper used by `DC7B` and `DF10`.

- Begins `PHP`.
- Seeds exact byte `00 = 08` and clears exact word `0DDB`.
- Reenters exact `REP #$20`, writes exact word `5400` to exact hardware-math register `4204`, and runs exact helper `EA81`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact local `00 = 08` / `4204 = 5400` prep wrapper for the downstream exact `EA81` service.

### C2:DD56..C2:DD97

This span freezes as the shared exact hardware-math-backed four-byte materializer.

- Begins by writing exact byte `00` to exact hardware register `4204` and exact divisor byte `0A` to exact register `4206`.
- Chooses exact tile byte `21`, `3D`, or `29` from the exact comparison between direct-page exact bytes `00` and `01`.
- Writes that exact selected tile byte into exact row fields `3407,Y` and `3409,Y`.
- Reads exact quotient `4214`, adds exact bias `6E`, and writes the exact result into exact row field `3406,Y`.
- Reruns the exact hardware-math path with divisor byte `64`, uses exact remainder register `4216`, conditionally adds exact bias `64`, and writes the exact result into exact row field `3408,Y`.
- Exits `RTS`.

Strongest safe reading: exact hardware-division-backed four-byte materializer that writes exact fields `3406/3407/3408/3409` from staged exact bytes `00/01` and the SNES exact hardware-math registers.

### C2:DD98..C2:DE1C

This span freezes as the exact `104D`-driven refresh owner that follows the earlier exact compactor at `DBE8`.

- Begins `STZ 3254 ; STZ 71 ; STZ 61 ; SEP #$20`.
- Runs exact helpers `8881` and `8900` from exact byte `04C9`.
- Mirrors exact word `04CC -> 0DAD`, then uses exact local table `DE1D` to seed exact loop-base byte `22`.
- When exact byte `04C9` is nonzero, copies exact blocks `3192 -> 04CA` and `3254 -> 0D82` through exact helper `F114`.
- Walks compact exact list `104D[71]` until the exact negative terminator.
- For each exact live entry, runs exact helper `8816`, snapshots exact words `9ACD -> 9B23`, runs exact helper `F626`, clears exact field `1811,Y`, and conditionally writes exact byte `0B` back into exact row field `1811,Y` when exact helper `93A8` returned a nonzero exact result.
- Mirrors exact byte `04C9` into exact table `9A90[22]`, runs exact helper `916E`, loads exact `Y = 61`, and runs exact helper `DE21`.
- Increments exact bytes `71` and exact byte-lane `61 += 08`, then loops.
- Exits `PLP ; RTS` when exact `104D` reaches its exact negative terminator.

Strongest safe reading: exact `104D`-driven refresh owner that seeds exact per-slot base byte `22` from local table `DE1D`, conditionally primes exact work bands `04CA/0D82`, updates one exact `1811` row entry and one exact `9A90` slot entry per compact exact `104D` element, and then runs exact helper `DE21` at exact row stride `+08`.

### C2:DE1D..C2:DE20

This span freezes as the exact local 4-byte table used only by `DD98`.

- Exact bytes: `29 28 27 2A`.
- Strongest safe reading: exact local 4-byte `04CC`-indexed base-byte table for the `DD98` refresh owner.

### C2:DE21..C2:DE55

This span freezes as the exact dual-lane materializer helper used by `DD98` and later by `E1C9`.

- Begins `PHP ; SEP #$30`.
- Uses exact slot byte `71` to test exact byte `1056[71]`; when nonzero, writes exact byte `38` into exact field `2E84,Y`.
- Loads exact word pair `9B23/9ACD` into direct-page exact bytes `00/01` and runs exact helper `DE56` for the first exact lane.
- Then sets exact `Y |= 40`, loads exact word pair `9B24/9ACE` into exact bytes `00/01`, and reruns exact helper `DE56` for the second exact lane.
- Exits `PLP ; RTS`.

Strongest safe reading: exact dual-lane row/materializer helper that optionally stamps exact byte `38` into `2E84`, then formats one exact lower lane and one exact upper lane through the shared exact `DE56` helper.

### C2:DE56..C2:DE97

This span freezes as the shared exact hardware-division-backed lane writer used by `DE21`.

- Writes staged exact byte `00` into exact hardware register `4204` and exact divisor byte `0A` into exact register `4206`.
- Selects exact glyph/tile byte `21`, `3D`, or `29` from the exact comparison between staged exact bytes `00` and `01`.
- Writes that exact selected byte into exact fields `3407,Y` and `3409,Y`.
- Reads exact quotient register `4214`, adds exact bias `6E`, and writes the exact result into exact field `3406,Y`.
- Reruns the exact hardware-math path with exact divisor byte `64`, reads exact remainder register `4216`, conditionally adds exact bias `64`, and writes the exact result into exact field `3408,Y`.
- Exits `RTS`.

Strongest safe reading: exact hardware-division-backed lane writer that materializes exact fields `3406/3407/3408/3409` from staged exact bytes `00/01` for the `DE21` dual-lane helper.

## Honest remaining gap

- the next clean seam now begins at the follow-on callable family `C2:DE98..C2:DF76`
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
