# Chrono Trigger Disassembly Progress — Pass 137

## Summary

Pass 137 closes the exact status/selector family that pass 136 left open at `C2:DA00..C2:DACA`, but the first correction is structural again: `C2:DA00` is **not** the callable entry. It is the terminal `RTS` byte of the already-frozen exact helper at `C2:D995..C2:D9FF`. The real callable family starts at `C2:DA01` and resolves into:

- one exact externally-reused dispatch owner at `C2:DA01..C2:DA34`
- one exact local 4-word dispatch table at `C2:DA35..C2:DA3C`
- four exact bounded step/clamp handlers at `C2:DA3D..C2:DA9E`
- one exact signed-negate / sign-extend preparer at `C2:DA9F..C2:DAB0`
- one exact shared `FD68` accumulator/update tail at `C2:DAB1..C2:DACA`

The important closure is that this seam is not one fuzzy status blob. It is an exact selector-step dispatcher with four exact local movement modes (`+1`, `-1`, `+10`, `-10`) that all funnel into one shared exact accumulator tail.

## What this pass closes

### C2:DA01..C2:DA34

This span freezes as the exact externally-reused selector-step dispatch owner reached from earlier exact dispatchers at `C2:D627` and `C2:D69F`.

Key facts now pinned:
- Entry begins `PHP ; REP #30`.
- Seeds exact word `04 = 1047`, exact byte `06 = 00`, and exact word `02 = 0003` before switching back to exact 8-bit mode via `SEP #30`.
- Seeds exact byte `0D1F = FF`.
- Exact signed byte `0D1E` is the mode selector. Negative exact values return immediately through the local `PLP ; RTS` tail.
- Non-negative path doubles exact selector byte `0D1E`, moves it into exact `X`, mirrors exact byte `04CB -> 83`, and dispatches through exact local indirect table `JSR ($DA35,X)`.
- After the selected exact handler returns, the owner always runs exact helper `E001`.
- If exact byte `04CB` changed against the staged exact byte `83`, it reruns exact helper `EAC2` before returning through exact `PLP ; RTS`.

Strongest safe reading: exact selector-step dispatch owner that stages exact control words from `1047`, dispatches through the exact 4-entry local table keyed by exact byte `0D1E`, always runs exact helper `E001`, and only reruns exact helper `EAC2` when the chosen exact handler changed exact byte `04CB`.

### C2:DA35..C2:DA3C

This span freezes as the exact 4-word local step-mode dispatch table used only by `DA01`.

Key facts now pinned:
- Table entries resolve exactly to:
  - selector `0` -> `DA3D`
  - selector `1` -> `DA50`
  - selector `2` -> `DA83`
  - selector `3` -> `DA64`
- The exact mode order is therefore structural, not linear by address: `+1`, `-1`, `-10`, `+10`.

Strongest safe reading: exact local 4-word step-mode dispatch table for the exact `0D1E` selector-step owner at `DA01`.

### C2:DA3D..C2:DA4F

This span freezes as the exact `+1` bounded step handler.

Key facts now pinned:
- Seeds exact byte `00 = 01`.
- Loads exact byte `04CB`, increments it by exact one step, and compares the result against exact bound byte `04CA`.
- When the incremented exact value reaches or exceeds exact byte `04CA`, the handler returns immediately through the local `RTS` tail.
- Otherwise stores the incremented exact value back into exact byte `04CB` and branches directly into the shared exact positive accumulator tail at `DAB1`.

Strongest safe reading: exact bounded `+1` selector-step handler that advances exact byte `04CB` by one when still below the exact upper-exclusive bound `04CA`, seeds exact step count `00 = 01`, and then enters the shared exact positive accumulator tail.

### C2:DA50..C2:DA63

This span freezes as the exact `-1` bounded step handler.

Key facts now pinned:
- Seeds exact byte `00 = 01`.
- Loads exact byte `04CB` and decrements it by exact one step.
- Exact zero result returns immediately through the local `RTS` tail, enforcing exact floor `01`.
- Exact results still greater than or equal to exact byte `04CA` also return immediately through the local `RTS` tail.
- Otherwise stores the decremented exact value back into exact byte `04CB` and branches into the shared exact signed-negate preparer at `DA9F`.

Strongest safe reading: exact bounded `-1` selector-step handler that only accepts decremented exact values still inside the live exact `01 .. 04CA-1` range, seeds exact step count `00 = 01`, and then enters the shared exact negative accumulator prep lane.

### C2:DA64..C2:DA82

This span freezes as the exact `+10` bounded step/clamp handler.

Key facts now pinned:
- Seeds exact byte `00 = 0A`.
- Adds exact decimal step `0x0A` to exact byte `04CB` and compares the result against exact bound byte `04CA`.
- When the tentative exact result stays below exact byte `04CA`, the handler stores it back into exact byte `04CB` and branches directly into the shared exact positive accumulator tail at `DAB1`.
- Otherwise clamps exact byte `04CB` to exact byte `04CA - 01`.
- On that exact clamp path it also recomputes exact byte `00` as the exact remaining distance from the old exact value of `04CB` to the exact clamp value `04CA - 01`.

Strongest safe reading: exact bounded `+10` selector-step/clamp handler that either advances exact byte `04CB` by ten or clamps it to exact ceiling `04CA - 01`, while updating exact byte `00` to the exact accepted forward distance before the shared exact positive accumulator tail.

### C2:DA83..C2:DA9E

This span freezes as the exact `-10` bounded step/clamp handler.

Key facts now pinned:
- Seeds exact byte `00 = 0A`.
- Subtracts exact decimal step `0x0A` from exact byte `04CB` by adding exact byte `F6` in exact 8-bit mode.
- Exact zero result does not store zero; it enters the exact clamp path.
- Exact tentative results still below exact bound byte `04CA` store directly back into exact byte `04CB`.
- Otherwise the exact clamp path reloads the old exact value of `04CB`, decrements it by exact one step into exact byte `00`, forces exact byte `04CB = 01`, and then falls into the shared exact negative accumulator preparer at `DA9F`.

Strongest safe reading: exact bounded `-10` selector-step/clamp handler that either moves exact byte `04CB` backward by ten when the exact result stays inside the live range, or clamps exact byte `04CB` to exact floor `01` while recomputing exact byte `00` as the accepted backward distance before the shared exact negative accumulator prep lane.

### C2:DA9F..C2:DAB0

This span freezes as the exact shared signed-negate / sign-extend preparer reached only from the decrementing exact handlers.

Key facts now pinned:
- Switches into exact 16-bit accumulator mode through `REP #20`.
- Loads exact word `04`, bit-inverts it through exact `EOR #FFFF`, increments it, and stores the exact 2's-complement result back into exact word `04`.
- Returns to exact 8-bit accumulator mode through `SEP #20`.
- When the exact negated result is nonzero, seeds exact byte `06 = FF`; otherwise exact byte `06` remains `00`.
- Falls straight into the shared exact accumulator tail at `DAB1`.

Strongest safe reading: exact shared decrement-lane preparer that converts staged exact word `04` into its exact signed negative form and seeds exact byte `06` as the corresponding exact sign-extension byte before the common `FD68` update tail.

### C2:DAB1..C2:DACA

This span freezes as the exact shared `FD68` accumulator/update tail used by all four exact step handlers.

Key facts now pinned:
- Begins with exact helper `FD68`.
- Reenters exact 16-bit accumulator mode through `REP #20`.
- Loads exact word `1044`, adds exact word `3E`, and stores the exact sum back into `1044`.
- Returns to exact 8-bit accumulator mode through `SEP #20`.
- Loads exact byte `1046`, adds exact byte `40` with carry from the prior exact word addition, and stores the exact result back into `1046`.
- Exits `RTS`.

Strongest safe reading: exact shared `FD68` accumulator/update tail that consumes the staged exact step parameters in direct page, then adds the resulting exact signed delta from exact `3E/40` into the live exact accumulator pair `1044/1046`.

## What remains after pass 137

- the next clean seam now starts at the exact follow-on callable family beginning `C2:DACB..C2:DB30`
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
