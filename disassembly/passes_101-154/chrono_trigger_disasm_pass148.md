# Chrono Trigger Disassembly — Pass 148

## Summary

Pass 148 closes the callable/helper family that pass 147 left open at `C2:ED31..C2:EE7F`, and it also closes the immediate callable spillover through exact `C2:EF64`.

The resolved family is:

- one exact FF-bank command-stream dispatcher at `C2:ED31..C2:ED58`
- one exact local 11-word command dispatch table at `C2:ED59..C2:ED6E`
- one exact short FF-to-7E record importer late entry at `C2:ED6F..C2:ED76`
- one exact repeated seed-word strip materializer at `C2:ED77..C2:ED8F`
- one exact packed row/column-to-pointer builder at `C2:ED90..C2:EDA9`
- two exact short wrapper entries at `C2:EDAA..C2:EDAF` and `C2:EDB0..C2:EDB5`
- one exact derived-extent owner at `C2:EDB6..C2:EDD2`
- one exact packet/fallback staging owner at `C2:EDD3..C2:EDF5`
- one exact row-band builder owner at `C2:EDF6..C2:EEE0`
- one exact local spillover post-adjust copy helper at `C2:EEE1..C2:EEF4`
- one exact local 16-byte template selector table at `C2:EEF5..C2:EF04`
- one exact coordinate-to-coordinate row-band copy owner at `C2:EF05..C2:EF2A`
- one exact multi-row 7E-to-7E block copier at `C2:EF2B..C2:EF44`
- one exact FF-table selected front-end at `C2:EF45..C2:EF64`

## Exact closures

### C2:ED31..C2:ED58

This span freezes as the exact FF-bank command-stream dispatcher that feeds the rest of this family.

Key facts now pinned:
- Begins `PHB ; PHP ; SEP #$20 ; REP #$10`.
- Sets exact data bank `FF` at the top of each exact loop pass through `LDA #$FF ; PHA ; PLB`.
- Reads one exact command byte from exact FF-bank stream `FF:[X]`.
- Negative exact command bytes terminate the whole exact loop through exact `BMI -> PLP ; PLB ; RTS`.
- Uses the exact command byte as an exact byte offset into the local exact indirect-jump table at `ED59` through exact `TYX ; JSR (ED59,X)`.
- Uses exact FF-bank table `FF:BD18[command]` as the exact block-size/count seed for the exact `MVN 7E,FF` import into exact scratch band `7E:005B`.
- Preserves and restores the exact advanced FF-bank stream pointer across each exact dispatched sub-call with exact `PHX/PLX`.
- Loops until the exact negative-command terminator is encountered.

Strongest safe reading: exact FF-bank command-stream dispatcher that imports one exact command record at a time into exact scratch band `7E:005B`, then dispatches that record through the exact local indirect-jump table at `ED59`.

### C2:ED59..C2:ED6E

This span freezes as the exact local 11-word command dispatch table used by exact owner `ED31`.

Exact table contents now pinned:
- exact slot word `ED77`
- exact slot word `EF05`
- exact slot word `EDAA`
- exact slot word `EF48`
- exact slot word `F332`
- exact slot word `F364`
- exact slot word `F337`
- exact slot word `F364`
- exact slot word `F378`
- exact slot word `EDB0`
- exact slot word `EDB6`

Strongest safe reading: exact local 11-word command dispatch table indexed by the exact command byte that `ED31` turns into the exact `JSR (ED59,X)` lane.

### C2:ED6F..C2:ED76

This span freezes as the exact short late-entry record importer sitting immediately after the exact jump table.

Key facts now pinned:
- Begins `INX ; LDY #$005B`.
- Runs exact `MVN 7E,FF`.
- Returns immediately through exact `RTS`.
- No exact active direct callers are currently cached, so this is still best treated as an exact local late-entry/helper body.

Strongest safe reading: exact short FF-to-7E record importer late entry using exact caller-owned `A/X` and exact fixed destination `7E:005B`.

### C2:ED77..C2:ED8F

This span freezes as the exact repeated seed-word strip materializer.

Key facts now pinned:
- Begins `PHP ; REP #$20`.
- Uses exact destination base word `61`.
- Copies exact caller-owned seed word `5D` into exact work word `7D` and exact destination word `[61]`.
- Uses exact `TXY ; INY ; INY` and exact self-overlapping `MVN 7E,7E` to replicate that exact seed word forward across the destination strip.
- Uses exact byte `5B` to derive the exact overall materialized span length.
- Returns through exact `PLP ; RTS`.

Strongest safe reading: exact repeated seed-word strip materializer using exact base word `61`, exact seed word `5D`, and exact span byte `5B`.

### C2:ED90..C2:EDA9

This span freezes as the exact packed row/column-to-pointer builder.

Key facts now pinned:
- Begins `PHP ; REP #$20`.
- Uses exact packed word `5D`.
- Extracts the exact low 5-bit lane of `5D`, doubles it, and combines it with the exact high-byte lane of `5D` shifted into exact `0x40` row units.
- Adds that exact packed offset to exact base word `61`.
- Stores the exact result into exact pointer word `63`.
- Returns through exact `PLP ; RTS`.

Strongest safe reading: exact packed row/column-to-pointer builder that derives exact work pointer `63` relative to exact base word `61`.

### C2:EDAA..C2:EDAF

This span freezes as the exact short wrapper that chains exact `EDB0` into exact `EE7F`.

Key facts now pinned:
- Runs exact helper `EDB0`.
- Tail-jumps into exact owner `EE7F`.

Strongest safe reading: exact short wrapper that stages through `EDB0` and then enters the exact downstream `EE7F` builder lane.

### C2:EDB0..C2:EDB5

This span freezes as the exact short wrapper that chains exact `EDD3` into exact `EDF6`.

Key facts now pinned:
- Runs exact helper `EDD3`.
- Tail-jumps into exact owner `EDF6`.

Strongest safe reading: exact short wrapper that stages through `EDD3` and then enters the exact downstream `EDF6` builder lane.

### C2:EDB6..C2:EDD2

This span freezes as the exact derived-extent owner immediately behind the short wrappers above.

Key facts now pinned:
- Begins `PHP ; REP #$30`.
- Runs exact helper `EDD3`.
- Derives exact width/count work word `8A` from exact packet/state word `5F`.
- Derives exact row-count work word `8C` from exact packet/state word `60`.
- Runs exact downstream owner `EE7F`.
- Returns through exact `PLP ; RTS`.

Strongest safe reading: exact derived-extent owner that stages through `EDD3`, derives exact local extent words `8A/8C` from exact words `5F/60`, and then runs exact owner `EE7F`.

### C2:EDD3..C2:EDF5

This span freezes as the exact packet/fallback staging owner.

Key facts now pinned:
- Begins `PHP ; SEP #$20`.
- Reads exact packet byte `005B`.
- When exact `005B` is nonnegative, derives exact stage word `0D47 = 20 * 005B`.
- When exact `005B` is negative, falls back to exact `(0D8C & 07)` before deriving the same exact `20 * selector` stage word.
- Copies exact packet byte `005C` into exact stage byte/word `0D48`.
- Runs exact helper `ED90` to refresh exact pointer word `63`.
- Returns through exact `PLP ; RTS`.

Strongest safe reading: exact packet/fallback staging owner deriving exact stage words `0D47/0D48` and refreshing exact pointer word `63` before the downstream row-build lanes.

### C2:EDF6..C2:EEE0

This span freezes as the exact row-band builder owner.

Key facts now pinned:
- Begins `PHP ; REP #$30`.
- Mirrors exact base pointer `63 -> 65`.
- Derives exact local work words `06`, `8A`, and `8C` from exact packet/state words `5F/60`.
- Loads exact stage word `0D47 -> 08`.
- Runs exact helper sequence `EE23 -> EE58 -> EE23`.
- Returns through exact `PLP ; RTS`.

Strongest safe reading: exact row-band builder owner that seeds exact local width/count words from exact `5F/60`, seeds exact stage word `08` from exact `0D47`, and then runs the exact `EE23 / EE58 / EE23` helper sequence.

### C2:EEE1..C2:EEF4

This span freezes as the exact local spillover post-adjust copy helper immediately after exact `EDF6`.

Key facts now pinned:
- Decrements exact row-count word `8C`.
- When exact `8C == 0`, returns immediately through exact `PLP ; RTS`.
- Otherwise doubles exact work word `8A`, then decrements it once.
- Advances exact source/base pointer word `63 += 0042`.
- Reuses exact helper `EF2B`.
- Returns through exact `PLP ; RTS`.

Strongest safe reading: exact local spillover post-adjust copy helper that advances exact pointer word `63`, retunes exact width/count word `8A`, and then reuses exact helper `EF2B`.

### C2:EEF5..C2:EF04

This span freezes as the exact local 16-byte template selector table used by exact owner `EE7F`.

Exact table bytes now pinned:
- `0C 0D 10 11 0E 0F 12 13 10 11 0C 0D 12 13 0E 0F`

Strongest safe reading: exact local 16-byte template/selector table consumed by the exact `EE7F` builder lane.

### C2:EF05..C2:EF2A

This span freezes as the exact coordinate-to-coordinate row-band copy owner.

Key facts now pinned:
- Begins `PHP ; REP #$30`.
- Derives exact row-count word `8C` from exact low byte of `60`.
- Derives exact per-row byte-count word `8A` from exact low byte of `5F`.
- Runs exact helper `ED90`, then mirrors exact resulting pointer word `63 -> 65`.
- Rebinds exact packed coordinate word `5D = 5B`.
- Runs exact helper `ED90` again to derive the second exact pointer.
- Runs exact helper `EF2B`.
- Returns through exact `PLP ; RTS`.

Strongest safe reading: exact coordinate-to-coordinate row-band copy owner that derives two exact packed-coordinate pointers through exact helper `ED90` and then copies the exact row bands through exact helper `EF2B`.

### C2:EF2B..C2:EF44

This span freezes as the exact multi-row 7E-to-7E block copier.

Key facts now pinned:
- Uses exact source pointer word `63` and exact destination pointer word `65`.
- Uses exact byte-count word `8A`.
- Runs exact `MVN 7E,7E`.
- After each exact row pass, advances both exact source and destination pointers by exact stride `0x0040`.
- Decrements exact row-count word `8C` until exhausted.
- Returns through exact `RTS`.

Strongest safe reading: exact multi-row 7E-to-7E block copier with exact `0x40` row stride using exact pointers `63/65` and exact work words `8A/8C`.

### C2:EF45..C2:EF64

This span freezes as the exact FF-table selected front-end immediately before the next clean seam.

Key facts now pinned:
- Begins `PHP ; REP #$30`.
- Runs exact helper `ED90` to refresh exact pointer word `63`.
- Uses exact packet/control word `5B` to select one exact FF-bank pointer from exact long table `FF:C457`.
- Loads that exact FF-bank pointer into exact `Y`.
- Reuses exact pointer word `63` as exact `X`.
- Switches into exact 8-bit accumulator mode, seeds exact high byte `FF` through exact `XBA`, loads exact parameter byte `5F`, and enters exact helper `EF65`.
- Returns through exact `PLP ; RTS`.

Strongest safe reading: exact FF-table selected front-end that derives exact pointer word `63` from exact packed coordinate word `5D`, selects one exact FF-bank script/template pointer from exact table `FF:C457` by exact word `5B`, and then enters exact helper `EF65` with exact parameter byte `5F`.

## Honest remaining gap

- the old seam `C2:ED31..C2:EE7F` was too short
- the honest closure for this pass runs through exact `C2:EF64`
- the next clean follow-on callable/helper family now begins at exact `C2:EF65`
- the next obvious callable band is `C2:EF65..C2:F00F`
- exact helper/owner anchors already visible there are:
  - exact shared helper entry `C2:EF65`
  - exact helper/interpreter entry `C2:EF7E`
  - exact writer helper entry `C2:EF97`
  - exact opcode dispatcher entry `C2:EFBE`
