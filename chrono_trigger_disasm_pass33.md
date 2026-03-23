# Chrono Trigger (USA) — Disassembly Pass 33

## Scope
This pass continues directly from pass 32 and stays inside the remaining high-value unresolved **bank `C1` group-2 cluster**:

- `0x10 -> C1:9E78`
- `0x11 -> C1:9F5A`
- `0x12 -> C1:9FD2`
- `0x16 -> C1:A396`

The goal of this pass was to replace the remaining “opaque body” labels with structurally honest handler families and to identify the scratch/finalization helpers they share.

## Baseline carried forward from pass 32
Pass 32 had already established:
- `C1:B88D` as the real group-2 command table
- `$AF24` as the short-circuit / abort-style flag
- `$B3B8` as the post-handler continuation selector
- `C1:9DCE`, `C1:9E63`, `C1:A14E`, and `C1:A3D1` as meaningful solved bodies/helpers

This pass picks up where pass 32 left off instead of reopening already-solved ground.

## What was done in this pass
1. Linearly decoded `C1:9E78`, `C1:9F5A`, `C1:9FD2`, and `C1:A396`
2. Followed the local helper chain through:
   - `C1:AC14`
   - `C1:AC46`
   - `C1:AD09`
   - `C1:AD35`
3. Cross-checked the bank-`FD` long helpers used by this cluster:
   - `FD:A990`
   - `FD:AAD2`
   - `FD:B438`
4. Split the remaining unresolved group-2 cluster into two real subfamilies:
   - **table-selected byte-writer handlers**
   - **eligible-slot selector / finalizer handlers**

---

## Core results

### 1. `C1:AC46` is a real scratch-list initializer, not filler noise
`C1:AC46` clears two parallel scratch arrays by filling them with `#$FF` across `0x0B` entries:

- `$AECC..$AED6`
- `$AD8E..$AD98`

This matters because later handlers use those arrays as live selection/candidate buffers. Pass 32 treated the downstream logic structurally; pass 33 now pins the scratch-list reset that precedes it.

Best current reading:
- `C1:AC46` = **selection scratch-list init (`AECC` + `AD8E` := `FF`)**

### 2. `C1:AD09` and `C1:AD35` are bitmask builders over the current selection list
These two helpers are not generic bookkeeping.

#### `C1:AD09`
- uses `$AECB` as current list count gate
- uses the first entry in `$AECC`
- converts that entry into a shifting `#$8000 >> index` style mask
- ORs the result into `$AE95`

Best current reading:
- `C1:AD09` = **build first-selected-entry mask into `$AE95`**

#### `C1:AD35`
- iterates over the current `$AECC` list using `$AECB`
- converts each entry into the same `#$8000 >> index` style mask
- accumulates the result into `$AE99`

Best current reading:
- `C1:AD35` = **build full selected-list mask into `$AE99`**

This is a strong structural upgrade because it explains why the selector-family handlers call both helpers before final return.

### 3. Group-2 opcode `0x10` (`C1:9E78`) is now a real eligible-slot selector/finalizer command
Pass 32 left `0x10` mostly opaque. This pass resolves the main shape.

#### Input/early setup
- operand 1 (`CC:0001,x`) -> `$0E`
- operand 2 (`CC:0002,x`) -> `$12`
- operand 3 (`CC:0003,x`) -> `$B3C7`
- calls `C1:AC46` to reset selection scratch lists

#### Main scan loop
The handler scans **8 candidate entries** (`X = 0..7`) and accepts an entry only when all of the following are true:
- `$AF0D,x != #$FF`
- `$AF02,x == #$FF`
- bit 7 of `$AF15,x` is clear

For each accepted entry it does all of the following:
- appends `x + 3` into the live selection list at `$AECC[count]`
- mirrors `$AF0D,x -> $AF02,x`
- mirrors `$B15B,x -> $AFAE,x`
- stores `#$FF` into `$B26B,x`
- stores `x` into `$AE6D,x`
- clears `$AE85,x`
- calls `JSL $FDB438`

So this is not a single-slot setter. It is a **scan-select-materialize** style command over an 8-entry runtime slot set.

#### Operand-1 mode behavior
After each accepted slot, operand 1 selects a small per-slot field transform on the `$5FB0/$5FB2` family:
- mode `1` -> `$5FB0 = $5FB2 >> 1`
- mode `2` -> `$5FB0 = $5FB2 >> 2`
- mode `3` -> `$5FB0 = 1`
- other values -> no special field rewrite observed in this handler body

The safest current reading is **mode-selected per-slot field initialization**. Do not hard-name `$5FB0/$5FB2` yet.

#### Finalization
After the 8-entry scan completes:
- `$AECB = accepted_count`
- `$AE91 = $B18B`
- `$AE92 = 2`
- `$AE93 = operand 2`
- `$AE94 = 0`
- `JSR $AD09`
- `JSR $AD35`
- optional `JSL $CD0033` if `$B3C7 != 0`
- returns with `$B3B8 = 1`

Best current reading:
- group-2 opcode `0x10` = **eligible-slot scan / select / finalize command with mode-selected field init**

This is strong enough to retire the old generic `body` label.

### 4. Group-2 opcode `0x11` (`C1:9F5A`) is a table-selected 4-pair byte writer
This handler does not scan slots at all.

#### Base selection
It uses `$B18B` to index the 16-bit table at `FD:A80B` and loads a base offset into `Y`.

That means this handler is selecting a **group-dependent WRAM base** first.

#### Write pattern
It then performs four repeated operations of the form:
- odd operand -> pointer / offset source (`$0E`)
- even operand -> value
- `STA ($0E),Y`

The concrete pairs are:
- operands `1/2`
- operands `3/4`
- operands `5/6`
- operands `7/8`

Then:
- optional `JSL $CD0033` if operand 9 (`$B3C7`) is nonzero
- returns with `$B3B8 = 2`

Best current reading:
- group-2 opcode `0x11` = **group-base-selected 4-pair byte writer**

This is a meaningful family separation from the selector-style handlers.

### 5. Group-2 opcode `0x12` (`C1:9FD2`) is a table-selected 5-pair byte writer plus selector/validation follow-up
This handler starts in the same family as `0x11`, then branches into a heavier follow-up stage.

#### Shared front half with `0x11`
Like `0x11`, it:
- uses `$B18B` to select a base offset from `FD:A80B`
- writes repeated odd/even operand pairs via `STA ($0E),Y`

Here the pairs are:
- operands `5/6`
- operands `7/8`
- operands `9/10`
- operands `11/12`
- operands `13/14`

So `0x12` is structurally a **5-pair** member of the same byte-writer family.

#### Additional side effects before follow-up
After those writes it also:
- clears bit 1 of `$B1FC` via `AND #$FD`
- advances the command pointer and consumes extra inline bytes
- seeds scratch state including:
  - `$AEE4`
  - `$B18C`
  - `$AECC`
  - `$AD8E`
  - `$AD8D = 1`
  - `$AECB = 1`
  - `$AE97 = $FF`
  - `$AE98 = $FF`

#### Optional dual-selector phase
It then consumes up to two extra inline selector bytes.
For each nonzero selector byte it:
- preserves current `$AECC` in `$10`
- calls `JSR $AC14`
- stores the resulting selection into `$AE97` or `$AE98`
- restores original `$AECC`

`C1:AC14` itself resets the scratch lists, consumes one inline selector control byte, and either:
- uses a preset value path, or
- dispatches through `JSR ($B8BB,X)`
then mirrors the resulting list into `$AD8E` and stores `$B2AE = $AECC`.

So the second half of `0x12` is explicitly **selector-driven**, not just a blind writer.

#### Validation / commit phase
After the two optional selector resolutions:
- `$B2EB = $AEFF[$AE97]`
- `$B2EC = $AEFF[$AE98]`
- `$B2AE = $AECC`
- `JSR $C1DD`

If `$AF23 != 0` after that validation call:
- sets `$AF24 = 2`
- still returns through the normal handler exit with `$B3B8 = 0`

If validation succeeds:
- `$AEE3 = 2`
- copies `$AD8E` back into `$AECC`
- `$AECB = $AD8D`
- if `$AD8E[0] < 3`, sets `$B3B9 = 1`
- rebuilds masks via `JSR $AD09` and `JSR $AD35`
- `JSL $FDAAD2`
- runs follow-up helpers `JSR $AC89` and `JSR $ACCE`
- optional `JSL $CD0033` if `$B3C7 != 0`
- returns with `$B3B8 = 0`

Best current reading:
- group-2 opcode `0x12` = **group-base-selected 5-pair byte writer with dual-selector validation/commit follow-up**

This is the strongest single gain of pass 33 because it turns one of the ugliest remaining opaque bodies into a recognizable two-stage command.

### 6. Group-2 opcode `0x16` (`C1:A396`) is a thin wrapper around a fused long helper at `FD:A990`
`C1:A396` is much thinner than it first looked.

Observed behavior:
- operand 1 -> `$0E`
- operand 2 -> `$12`
- operand 11 -> `$B3C7`
- `JSR $AC46`
- `JSL $FDA990`
- `JSR $AD09`
- `JSR $AD35`
- optional `JSL $CD0033` if `$B3C7 != 0`
- returns with `$B3B8 = 1`

The important gain is what `FD:A990` looks like.

### 7. `FD:A990` fuses the two family shapes together
The long helper at `FD:A990` begins by doing the same **table-selected byte-write pattern** seen in `0x11/0x12`, then drops directly into the same **eligible-slot scan/materialize shape** seen in `0x10`.

So `0x16` is not its own unrelated mystery blob. It is best treated as a **long-form fused helper command** that combines:
- the group-base byte-writer family, and
- the eligible-slot selector/finalizer family

Best current reading:
- group-2 opcode `0x16` = **wrapper around fused long helper (`FD:A990`) for table-write + eligible-slot select/finalize**

This is a strong structural label even though the exact gameplay-facing purpose is still open.

---

## What changed in the understanding of the unresolved cluster
Before this pass, the remaining cluster was still mostly:
- `0x10 -> body`
- `0x11 -> body`
- `0x12 -> body`
- `0x16 -> body`

After this pass:
- `0x10` is clearly a selector/finalizer command over an 8-entry candidate set
- `0x11` is clearly a group-base-selected 4-pair byte writer
- `0x12` is clearly a group-base-selected 5-pair byte writer with selector/validation follow-up
- `0x16` is clearly a wrapper into a fused long helper that combines both families
- `AC46`, `AD09`, and `AD35` are now strong shared helper labels

That is a real reduction in opacity.

---

## Confidence notes

### Strong enough to keep
- `C1:AC46` as scratch-list init for `$AECC` / `$AD8E`
- `C1:AD09` as first-selected-entry mask builder into `$AE95`
- `C1:AD35` as full-selection-list mask builder into `$AE99`
- group-2 `0x10` as eligible-slot scan/select/finalize command
- group-2 `0x11` as table-selected 4-pair byte writer
- group-2 `0x12` as table-selected 5-pair byte writer plus selector/validation follow-up
- group-2 `0x16` as wrapper around fused long helper `FD:A990`
- `FD:A990` as a fused helper bridging the writer family and selector family

### Still provisional / intentionally not overclaimed
- exact gameplay-facing names for `$AECC`, `$AD8E`, `$AE95`, `$AE99`, `$B2EB`, `$B2EC`, `$B2AE`
- exact real-world meaning of the `$5FB0/$5FB2` field adjusted by `0x10`
- exact user-facing purpose of `JSL $CD0033`
- exact semantic names for the validation/commit helpers `C1:C1DD`, `C1:AC89`, and `C1:ACCE`
- exact meaning of `$B3B9`, `$AEE3`, `$AEE4`, `$AF23`

---

## Best next pass from here
The remaining unresolved front of group 2 is now mostly concentrated in the older pair:

- `0x01 -> C1:99BE`
- `0x02 -> C1:9A39`

Those should be attacked next with the new helper labels in hand, because pass 33 has now stabilized the later cluster enough that the center of uncertainty has shifted earlier in the table.
