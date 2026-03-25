# Chrono Trigger Disassembly — Pass 150

## Summary

Pass 150 closes the callable/helper family that pass 149 left open at `C2:F114..C2:F24A`, with the structural correction that the old seam end was too short. The honest closure for this family runs through exact `C2:F2F2`.

The resolved family is:

- one exact `DB:[Y]` packed-bitfield-to-BCD front-end owner at `C2:F114..C2:F13E`
- one exact packed-bitfield-to-BCD accumulator helper at `C2:F13F..C2:F177`
- one exact local 27-long packed-BCD powers-of-two table at `C2:F178..C2:F1D7`
- one exact bank-7E BCD nibble-decode/materialize helper at `C2:F1DA..C2:F20A`
- one exact nibble/blank-flag tile-pair writer at `C2:F20B..C2:F226`
- one exact sibling fixed-value writer owner at `C2:F227..C2:F24B`
- one exact fixed-width bank-7E nibble/tile materializer helper at `C2:F24C..C2:F268`
- one exact local nibble-to-tile-pair writer helper at `C2:F269..C2:F27C`
- one exact local 16-byte nibble/tile table at `C2:F27D..C2:F28C`
- one exact two-field formatter owner at `C2:F28D..C2:F2CB`
- one exact two-decimal-byte-to-binary helper at `C2:F2CC..C2:F2DB`
- one exact indexed local wrapper into exact script front-end `EF65` at `C2:F2DC..C2:F2E1`
- one exact `7D00`-table selector helper for that wrapper at `C2:F2E2..C2:F2F2`

## Exact closures

### C2:F114..C2:F13E
This span freezes as the exact shared front-end that converts one exact `DB:[Y]` packed-bitfield source into exact work words `8A/8C`, derives exact digit/lane selector bytes `8E/8F`, then materializes exact tile pairs into exact bank-`7E` destination `[X]`.

### C2:F13F..C2:F177
This span freezes as the exact packed-bitfield-to-BCD accumulator helper behind exact owner `F114`, using exact packed-BCD table `F178` and exact work words `8A/8C`.

### C2:F178..C2:F1D7
This span freezes as the exact local 27-long packed-BCD powers-of-two table consumed by exact helper `F13F`.

### C2:F1DA..C2:F20A
This span freezes as the exact bank-`7E` BCD nibble-decode/materialize helper using exact selector/flag bytes `8E/8F`, exact packed-BCD work bytes `8A/8C`, and exact nibble writer `F20B`.

### C2:F20B..C2:F226
This span freezes as the exact nibble/blank-flag tile-pair writer using exact flag byte `8F`, exact tile base `0xD4`, and exact paired high byte `7E`.

### C2:F227..C2:F24B
This span freezes as the exact sibling fixed-value writer owner that loads exact words `[Y]` / `[Y+2]` into exact work words `8A/8C`, then materializes exact tile pairs through exact helper `F24C`.

### C2:F24C..C2:F268
This span freezes as the exact fixed-width bank-`7E` nibble/tile materializer helper using exact selector byte `8E` and exact nibble writer `F269`.

### C2:F269..C2:F27C
This span freezes as the exact local nibble-to-tile-pair writer helper using exact local table `F27D`.

### C2:F27D..C2:F28C
This span freezes as the exact local 16-byte nibble/tile table consumed by exact helper `F269`.

Exact bytes now pinned:
- `73 74 75 76 77 78 79 7A 7B 7C F1 F2 36 7D 38 34`

### C2:F28D..C2:F2CB
This span freezes as the exact two-field formatter owner that prepares exact scratch bytes `22/23`, renders them through exact helper `F114` with exact mode word `0x7E91`, and inserts one exact separator tile pair formed from exact byte `7D` and exact low byte `0x2D` between the two exact rendered fields.

### C2:F2CC..C2:F2DB
This span freezes as the exact two-decimal-byte-to-binary helper combining exact decimal-byte pair `[Y]/[Y+1]` into one exact accumulator byte.

### C2:F2DC..C2:F2E1
This span freezes as the exact indexed local wrapper that prepares one exact `7D00`-table-selected script pointer through exact helper `F2E2` and then tail-jumps into exact script front-end `EF65`.

### C2:F2E2..C2:F2F2
This span freezes as the exact `7D00`-table selector helper returning one exact `Y` pointer plus exact constant word `0xCC0B` for the exact `EF65` wrapper lane.
