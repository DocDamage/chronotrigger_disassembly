# Chrono Trigger Disassembly — Pass 142

## Summary

Pass 142 closes the exact follow-on callable/helper family that pass 141 left open at `C2:E163..C2:E34A`, but the seam correction goes the other direction this time: the old end was one byte too long. `C2:E34A` is the first byte of the next live callable owner, so the exact closure here stops at `C2:E349`.

The resolved family is:

- one exact selected-entry loader owner at `C2:E163..C2:E18A`
- one exact partial slot-reseed / marker-refresh owner at `C2:E18B..C2:E1DB`
- one exact local 8-byte selector table at `C2:E1DC..C2:E1E3`
- one exact caution-only pointer-looking 5-word local table at `C2:E1E4..C2:E1ED`
- one exact `299F|71`-gated lane owner at `C2:E1EE..C2:E209`
- one exact `00F0`-gated setup tail at `C2:E20A..C2:E21E`
- one exact poll/wait owner at `C2:E21F..C2:E235`
- one exact `E984/E5D3` front-end owner with exact `2990.bit6` update lane at `C2:E236..C2:E266`
- one exact `0D1E`-dispatched owner at `C2:E267..C2:E297`
- one exact local 5-word indirect dispatch table at `C2:E298..C2:E2A1`
- one exact overlapping decrement/increment updater pair for exact byte `0F09` at `C2:E2A0..C2:E2CB`
- one exact overlapping decrement/increment updater pair for exact byte `0F08` at `C2:E2CC..C2:E2F3`
- one exact `0D1D`-gated tail / refill dispatcher at `C2:E2F4..C2:E315`
- one exact lookup-backed `0F00` fill helper at `C2:E316..C2:E349`

## Exact closures

### C2:E163..C2:E18A

This span freezes as the exact selected-entry loader owner at the front of the pass-141 live seam.

Key facts now pinned:
- Begins `PHP ; SEP #$20`.
- Runs exact helper `8820`.
- Clears exact `A` with `TDC`, then loads exact byte `0FC8`, adds exact selector byte `54`, subtracts exact constant `04`, and uses the result as exact `X`.
- Loads exact byte `0F00,X -> 04C9`.
- Loads exact word `0D26 -> X` and mirrors exact byte `04C9 -> 9A90,X`.
- Calls exact local landing byte `E18A`.
- Emits exact selector `FBF1` through exact helper `8385`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact selected-entry loader owner that runs exact helper `8820`, derives one exact `0F00` source index from exact bytes `0FC8` and `54`, stages that exact source byte into `04C9`, mirrors it into exact table `9A90[0D26]`, touches the exact local `E18A` landing byte, and exits through exact selector `FBF1`.

### C2:E18B..C2:E1DB

This span freezes as the exact partial slot-reseed / marker-refresh owner directly following the `E163` loader.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Runs exact helper `916E`.
- When exact byte `9ABA == A8`, increments exact word `9B21` once.
- Seeds exact loop index from exact byte `51`.
- On each exact pass, reads one exact selector byte from exact local table `E1DC + X`, then uses that exact selector as the exact `X` index for paired tables `9A90` and `9AE6`.
- Snapshots exact byte `9A90,selector -> 00`.
- Mirrors exact byte `9AE6,selector -> 9A90,selector`.
- Compares the new exact `X` selector value against the snapped old exact byte `00` and chooses exact marker byte `00`, `08`, or `1C`.
- Stores that exact marker byte into exact work byte `0D4D,index`.
- Advances the exact loop index and repeats while the exact index stays below exact bound `07`.
- Derives exact row stride `Y = 8 * 71`, runs exact helper `DE21`, emits exact selector `C318` through exact helper `ED31`, loads exact byte `04C9`, and runs exact helper `F2F3`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact partial slot-reseed / marker-refresh owner that, starting from exact byte `51`, walks the downstream exact selector table at `E1DC`, promotes exact bytes from `9AE6` into `9A90`, writes one exact marker byte per processed lane into `0D4D`, refreshes one exact row through exact helper `DE21`, emits exact selector `C318`, and finishes through exact helper `F2F3(04C9)`.

### C2:E1DC..C2:E1E3

This span freezes as the exact local 8-byte selector table consumed by exact owner `E18B`.

Key facts now pinned:
- Exact bytes: `60 36 38 3B 39 37 3A 3C`.
- Consumed directly as exact selector bytes through exact long read `LDA $C2E1DC,X` inside exact owner `E18B`.

Strongest safe reading: exact local 8-byte selector table for the exact `E18B` partial slot-reseed / marker-refresh owner.

### C2:E1E4..C2:E1ED

This span does **not** freeze as clean callable code in this pass. It remains safest as a caution-only local pointer-looking table immediately after the exact `E1DC` selector bytes.

Key facts now pinned:
- Exact words: `E1ED, E21E, E236, E201, E209`.
- The exact bytes are structurally isolated between the exact `E18B` owner and the exact `E1EE` owner.
- A clean local direct consumer is still not proven in this pass.

Strongest safe reading: exact local five-word pointer-looking table fragment between the `E18B` and `E1EE` owners; keep the exact consumer open.

### C2:E1EE..C2:E209

This span freezes as the exact `299F|71`-gated owner that chooses one of two downstream lanes before exact tail `83B2`.

Key facts now pinned:
- Loads exact byte `299F`, ORs it with exact byte `71`, and stores the exact result back into exact byte `299F`.
- When the exact result is zero, runs exact helper `E576`, seeds exact byte `68 = 02`, and jumps to exact tail `83B2`.
- Otherwise runs exact helper `E40E`, increments exact byte `68`, and jumps to exact tail `83B2`.

Strongest safe reading: exact `299F|71`-gated owner that latches exact byte `299F`, chooses exact zero-lane helper `E576` versus exact nonzero-lane helper `E40E`, and rejoins the shared exact `83B2` tail with exact byte `68` updated.

### C2:E20A..C2:E21E

This span freezes as the exact `00F0`-gated setup tail.

Key facts now pinned:
- Loads exact word `00F0 -> X`.
- Exact zero returns immediately.
- Nonzero path runs exact helper `EAC2`, seeds exact byte `0D13 = 1D`, clears exact byte `0D9A`, seeds exact byte `68 = 01`, and returns.

Strongest safe reading: exact `00F0`-gated setup tail that conditionally reruns exact helper `EAC2`, signals exact byte `0D13 = 1D`, clears exact byte `0D9A`, seeds exact byte `68 = 01`, and exits.

### C2:E21F..C2:E235

This span freezes as the exact poll/wait owner that fronts the later exact `E267` dispatcher.

Key facts now pinned:
- Runs exact helpers `E984` and `E267`.
- Tests exact byte `00F0.bit0`; exact clear returns immediately.
- Exact set path repeatedly runs exact helper `E363` until the returned exact accumulator becomes zero.
- Then jumps to exact tail `82B2`.

Strongest safe reading: exact poll/wait owner that runs exact `E984/E267`, only continues when exact byte `00F0.bit0` is set, spins on exact helper `E363` until the exact returned byte clears, and then rejoins exact tail `82B2`.

### C2:E236..C2:E266

This span freezes as the exact `E984/E5D3` front-end owner with the exact negative-lane `2990.bit6` update and exact `83CA` tail.

Key facts now pinned:
- Runs exact helpers `E984` and `E5D3`.
- Tests exact status byte `0D1D` with `BIT`.
- Exact non-negative path compares exact byte `0081` against exact selector byte `54`; when they differ, reruns exact helper `EAC2`, then returns.
- Exact negative path loads exact selector byte `54`, shifts its exact bit0 into carry, seeds exact mask byte `40`, and then uses exact `TSB 2990` versus exact `TRB 2990` to set or clear exact bit `40` of exact config byte `2990`.
- Seeds exact byte `68 = 03`, exact accumulator `74`, runs exact helper `8255`, and jumps to exact tail `83CA`.

Strongest safe reading: exact `E984/E5D3` front-end owner that either conditionally reruns exact helper `EAC2` on the exact non-negative lane, or on the exact negative lane toggles exact bit `40` in exact config byte `2990` from exact `54.bit0`, seeds exact byte `68 = 03`, and exits through exact helper `8255(74)` plus exact tail `83CA`.

### C2:E267..C2:E297

This span freezes as the exact `0D1E`-dispatched owner at the center of the family.

Key facts now pinned:
- Begins `PHP ; SEP #$20`.
- Loads exact byte `9380 -> 7F` and seeds exact hardware register `4202 = 10`.
- Clears exact `A`, loads exact byte `0D1E`, and skips the indirect dispatch when that exact byte is negative.
- Otherwise doubles exact byte `0D1E` into exact `X` and dispatches through exact local indirect table `E298` using exact `JSR ($E298,X)`.
- Restores exact byte `7F -> X`, compares it against exact byte `9380`, and reruns exact helper `EAC2` when the exact value changed.
- Always runs exact helper `E2F4`, then exact helper `E34A`, then emits exact selector `FBE3` through exact helper `8385`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact `0D1E`-dispatched owner that snapshots exact byte `9380`, optionally dispatches one exact state handler through exact local table `E298`, conditionally reruns exact helper `EAC2` when exact byte `9380` changed, then always runs exact helper pair `E2F4 -> E34A` before exact selector tail `FBE3`.

### C2:E298..C2:E2A1

This span freezes as the exact local 5-word indirect dispatch table consumed by exact owner `E267`.

Key facts now pinned:
- Exact words: `E2D6, E2CC, E2AA, E2A0, E2AD`.
- Consumed directly by exact indirect dispatch `JSR ($E298,X)` from exact owner `E267`.

Strongest safe reading: exact local 5-word indirect dispatch table for the exact `E267` owner, keyed by exact state byte `0D1E`.

### C2:E2A0..C2:E2CB

This span freezes as the exact overlapping decrement / increment updater pair for exact byte `0F09`.

Key facts now pinned:
- Exact dispatch entry `E2A0` decrements exact byte `0F09` with wrap from exact negative result to exact byte `07`.
- Exact dispatch entry `E2AA` increments exact byte `0F09` with wrap from exact bound `08` back to exact byte `00`.
- Both lanes store the final exact value back into exact byte `0F09` and into exact hardware register `4203`.
- Both lanes clear exact byte `0F0A`.
- Both lanes compute exact byte `9381 = 53 + 4216` and mirror that exact result into exact byte `0F0B`.
- Exit `RTS`.

Strongest safe reading: exact overlapping decrement / increment updater pair for exact byte `0F09` that wraps the exact value inside exact range `00..07`, mirrors it into exact hardware register `4203`, clears exact byte `0F0A`, and rebuilds exact bytes `9381 / 0F0B` from exact hardware-math result `4216` plus exact bias `53`.

### C2:E2CC..C2:E2F3

This span freezes as the exact overlapping decrement / increment updater pair for exact byte `0F08`.

Key facts now pinned:
- Exact dispatch entry `E2CC` decrements exact byte `0F08` with wrap from exact negative result to exact byte `09`.
- Exact dispatch entry `E2D6` increments exact byte `0F08` with wrap from exact bound `0A` back to exact byte `00`.
- Both lanes store the final exact value back into exact byte `0F08` and into exact hardware register `4203`.
- Both lanes leave exact `EA EA` padding before the exact final hardware-math readback.
- Both lanes compute exact byte `9380 = 24 + 4216`.
- Exit `RTS`.

Strongest safe reading: exact overlapping decrement / increment updater pair for exact byte `0F08` that wraps the exact value inside exact range `00..09`, mirrors it into exact hardware register `4203`, and rebuilds exact byte `9380` from exact hardware-math result `4216` plus exact bias `24`.

### C2:E2F4..C2:E315

This span freezes as the exact `0D1D`-gated tail / refill dispatcher.

Key facts now pinned:
- Tests exact status byte `0D1D` with `BIT`.
- Exact negative path runs exact helper `E316`.
- Exact overflow-clear path skips both exact update lanes and falls through directly to exact selector tail `C41F` through exact helper `ED31`.
- Remaining exact update lane tests exact byte `0F06`; when nonzero, writes exact byte `FF` into exact buffer `0EFF,X` and decrements exact byte `0F06`.
- Both exact update lanes rerun exact helper `EAC2` before the final exact selector tail.
- Finishes through exact selector `C41F` via exact helper `ED31`.

Strongest safe reading: exact `0D1D`-gated tail / refill dispatcher that chooses an exact `E316` refill lane, an exact `0F06` tail-pop lane, or an immediate exact `C41F` selector tail, with exact helper `EAC2` rerun only on the active update lanes.

### C2:E316..C2:E349

This span freezes as the exact lookup-backed `0F00` fill helper at the back edge of the pass.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Seeds exact hardware register `4202 = 0A`.
- Mirrors exact byte `0F09 -> 4203`.
- Loads exact byte `0F08`, adds exact hardware-math result `4216`, and uses the exact result as exact `X`.
- Loads one exact byte from exact long table `FF:C9AC,X`.
- Loads exact write index `0F06 -> Y`, clamps it to exact max `04`, writes the fetched exact byte into exact buffer `0F00,Y`, increments exact `Y`, and stores the exact incremented value back into exact byte `0F06` while exact `Y < 06`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact lookup-backed `0F00` fill helper that combines exact bytes `0F08/0F09` through the SNES exact hardware-math lane, fetches one exact byte from exact long table `FF:C9AC`, and appends it into exact `0F00` through the capped exact write index `0F06`.

## Honest remaining gap

- the old seam `C2:E163..C2:E34A` is now closed more honestly as `C2:E163..C2:E349`
- `C2:E34A` is the first byte of the next live callable owner, not part of the old family
- the exact local fragment `C2:E1E4..C2:E1ED` is only safe as a caution-only pointer-looking table for now; its clean exact consumer is still open
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
