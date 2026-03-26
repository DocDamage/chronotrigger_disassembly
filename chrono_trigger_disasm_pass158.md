# Chrono Trigger Disassembly — Pass 158

## Summary

Pass 158 closes the repeated exact clamp/update family immediately after exact `C2:FE09`, and it also freezes the ugly exact overlap/tail islands between those repeated helpers so they stop blocking forward progress.

The clean split is:

- one exact overlap/tail island at `C2:FE0A..C2:FE2C` that is **not** a standalone owner
- one exact direct-call clamp helper clone at `C2:FE2D..C2:FE57`
- one exact tiny overlap/noise tail at `C2:FE58..C2:FE5C`
- one exact second local clamp helper clone at `C2:FE5D..C2:FE87`
- one exact overlap/tail normalizer island at `C2:FE88..C2:FE99`
- one exact subtract/update helper clone at `C2:FE9A..C2:FEBD`
- one exact overlapping late entry into that subtract tail at `C2:FEA2..C2:FEBD`
- one exact direct-call clamp helper clone at `C2:FEBE..C2:FEE8`
- one exact overlap/tail island at `C2:FEE9..C2:FEF9` that ends in two exact `8385` submissions and exact jump `E77B`

This pass does **not** force the next clean owner at exact `C2:FEFA`; it only advances the seam honestly up to that point.

## Exact closures

### C2:FE0A..C2:FE2C
This exact span freezes as an exact overlap/tail island, not one exact standalone callable owner.

No exact direct call xref currently lands on exact `FE0A`, and the exact first bytes do **not** balance cleanly as one exact independent entry. The exact back half, however, is structurally readable: starting inside the exact span, the bytes perform one exact local low-word store into exact `2C53`, narrow through exact `SEP #$20`, subtract exact staged high byte `1046` from exact live exact high byte `2C55`, saturate exact `2C55` to exact `98` on borrow, then run exact helper `FE2D` before exact `PLP ; RTS`.

Strongest safe reading: exact overlap/tail island feeding the downstream exact exact `98:967F` clamp helper at exact `FE2D`, not one exact independent callable owner rooted at exact `FE0A`.

### C2:FE2D..C2:FE57
This exact span freezes as one exact direct-call clone of the earlier exact clamp/normalize helper family.

Real exact caller is exact `C2:FE28`. Exact body is structurally the same as already-frozen exact helpers `FDDF` and later exact `FEBE`: `PHP ; SEP #$30 ; LDX #$00`, compare exact high byte `2C55` against exact bound byte `98`, return immediately for exact values below the bound, compare exact low word `2C53` against exact bound word `967F` on exact equality, and on clamp force exact `2C53 = 967F`, exact `2C55 = 98`, and exact `X = FF` before exact `PLP ; RTS`.

Strongest safe reading: exact direct-call clone of the exact exact `98:967F` clamp/normalize helper for exact `2C53/2C55`, returning exact `X = FF` when it clamps.

### C2:FE58..C2:FE5C
This exact five-byte span freezes as exact overlap/noise tail between the two repeated clamp bodies.

Exact bytes: `B2 82 FE 28 60`. No exact direct call xref lands here, and the exact byte sequence does **not** decode as one exact balanced standalone owner at exact `FE58`.

Strongest safe reading: exact non-owner overlap/noise tail between exact clamp-helper bodies `FE2D` and `FE5D`.

### C2:FE5D..C2:FE87
This exact span freezes as one exact second local clone of the same exact clamp/normalize helper body.

Its exact body is byte-for-byte the same exact clamp shape as exact `FE2D` and exact `FEBE`: `PHP ; SEP #$30 ; LDX #$00`, exact compare against exact `98:967F`, exact clamp path forcing `2C53 = 967F`, `2C55 = 98`, and exact `X = FF`, then exact `PLP ; RTS`.

No exact hot direct caller is currently cached for exact `FE5D`, so this exact clone is still slightly less anchored than exact `FE2D` and exact `FEBE`.

Strongest safe reading: exact second local duplicate of the exact exact `98:967F` clamp/normalize helper body for exact `2C53/2C55`.

### C2:FE88..C2:FE99
This exact span freezes as one more exact overlap/tail island rather than a clean standalone owner.

No exact direct call xref lands at exact `FE88`, and the exact front bytes do not decode cleanly as one exact balanced entry. The exact readable tail writes one exact candidate high byte into exact `2C55`, saturates exact `2C55` to exact `98` on exact carry/borrow failure, then runs exact helper `FEBE` and exits through exact `PLP ; RTS`.

Strongest safe reading: exact overlap/tail normalizer island that feeds the downstream exact clamp helper `FEBE`, not one exact independent callable owner rooted at exact `FE88`.

### C2:FE9A..C2:FEBD
This exact span freezes as one exact subtract/update helper clone of already-frozen exact helper `FDBB`.

It begins `PHP ; REP #$20`, loads exact live exact low word `2C53`, subtracts exact staged exact low word `1044`, stores the exact result back to exact `2C53`, narrows through exact `SEP #$20`, then subtracts exact staged exact high byte `1046` from exact live exact high byte `2C55` and stores the exact result back to exact `2C55`. On exact borrow it forces exact byte `2C55 = 98`. The tail then runs exact helper `FEBE` and exits through exact `PLP ; RTS`.

Strongest safe reading: exact duplicate staged-subtract updater that subtracts exact `1044/1046` from exact `2C53/2C55`, repairs/saturates exact high byte `2C55` to exact `98` on borrow, and reruns downstream exact clamp helper `FEBE`.

### C2:FEA2..C2:FEBD
This exact overlapping entry is structurally real because exact caller `C2:C5B5` directly runs exact `JSR FEA2`.

It lands inside the exact subtract helper tail after the exact widened accumulator/setup from exact `FE9A`, beginning with exact `SEC ; SBC $1044 ; STA $2C53`, then performing the exact 8-bit high-byte subtract against exact `1046`, the exact high-byte repair/saturation to exact `98`, the exact call to exact helper `FEBE`, and exact `PLP ; RTS`.

Strongest safe reading: exact overlapping late/local entry into the shared exact subtract/normalize tail of exact owner `FE9A`.

### C2:FEBE..C2:FEE8
This exact span freezes as one more exact direct-call clone of the exact clamp/normalize helper family.

Real exact callers are exact `C2:FE95` and exact `C2:FEB9`. Exact body again matches the exact `98:967F` clamp shape used by exact `FDDF` and exact `FE2D`: it checks exact `2C55` against exact `98`, checks exact `2C53` against exact `967F` on equality, and on clamp forces exact `2C53 = 967F`, exact `2C55 = 98`, and exact `X = FF` before exact `PLP ; RTS`.

Strongest safe reading: exact direct-call clone of the exact exact `98:967F` clamp/normalize helper for exact `2C53/2C55`.

### C2:FEE9..C2:FEF9
This exact span freezes as one exact overlap/tail island, not one exact clean standalone owner.

No exact direct call xref is currently cached for exact `FEE9`, and the exact front bytes do not form one exact clean callable head. The readable exact back half performs two exact local exact `JSR 8385` packet submissions and exits through exact jump `E77B`, but the exact lead-in still looks like exact overlap/tail bytes rather than one exact owner head.

Strongest safe reading: exact overlap/tail island ending in two exact `8385` submissions and exact jump `E77B`, not one exact independent callable owner rooted at exact `FEE9`.

## Honest remaining gap

- exact `C2:FE0A..C2:FEF9` is now honestly split and closed into repeated exact helper clones plus exact overlap/tail islands
- the next clean forward callable owner begins at exact `C2:FEFA`
- exact `C2:FEFA..` should be taken as the next pass rather than guessed from the middle of the exact repeated tail islands
