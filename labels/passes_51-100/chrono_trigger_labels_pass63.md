# Chrono Trigger Labels — Pass 63

## Purpose
This file records the label upgrades and one correction justified by pass 63.

The main result is that the early master-opcode band now contains a real selector/list-transform subfamily beside the simpler replay gates.

It also corrects one stale carry-forward mistake:
- global master opcode `04` is **not** the old slice-era `B815` body
- the real master-table entry for `04` is `C1:8FDA`

---

## Strong labels

### C1:8EAB..C1:8F10  ct_global_opcode_01_filter_selected_entries_by_fd_record_threshold   [strong structural]
- Calls `AC14`, so operand `+1` is an inline selector-control byte.
- Uses the resulting `AECC/AECB` selected list as input.
- For each selected entry:
  - resolves a structured-record base via `FD:A80B`
  - requires record byte `+1D` to be non-negative
  - accepts only when record byte `+3` is less than or equal to `(record byte +5) >> 1`
- Accepted entries are incremented in-place in `AECC`.
- Writes accepted-count back to `AECB`.
- Runs `AE21`, then if `AF24 == 0` runs `AEFD` and `8C3E`.
- Empty input selection does **not** force `AF24 = 1`.
- Best carried as a selector-driven filtered-list transform, not a pure boolean gate.

### C1:8F11..C1:8F81  ct_global_opcode_02_filter_head_or_nonhead_selected_entries_by_lane_flag_mask [strong structural]
- Operand `+1` chooses which fixed selector-control byte is dispatched through `AC2C`:
  - operand1 `== 0` -> selector-control `0x01` -> visible/head occupied entries (`A3F7`)
  - operand1 `!= 0` -> selector-control `0x16` -> non-head occupied entries (`A6ED`)
- Operands `+2/+3` are used as:
  - byte offset inside the lane block
  - required bitmask
- For each selected entry:
  - reads `5E4A + selected_entry*0x80 + operand2`
  - accepts only when `(byte & operand3) == operand3`
- Accepted entries are incremented in-place in `AECC`.
- Zero survivors -> `AF24 = 1`.
- Successful survivors finalize through `AE21`, `AEFD`, and `8C3E`.

### C1:8F87..C1:8FD9  ct_global_opcode_03_filter_selected_entries_by_occupant_index_equals_immediate [strong structural]
- Calls `AC14`, so operand `+1` is an arbitrary inline selector-control byte.
- Requires a non-empty selected list from `AECC/AECB`.
- Consumes the next immediate byte and accepts only selected entries where:
  - `AEFF[selected_entry] == immediate`
- Accepted entries are incremented in-place in `AECC`.
- Zero survivors -> `AF24 = 1`.
- Successful survivors finalize through `AE21`, `AEFD`, and `8C3E`.
- Strong structural sibling to opcode `02`, but using arbitrary `AC14` selection plus occupant-equality filtering.

### C1:8FDA..C1:9012  ct_global_opcode_04_gate_tail_replay_on_live_tail_occupant_presence_mode [strong]
- Scans live tail occupant map `AF02[0..AEC6-1]` for operand1.
- Operand2 selects the sense:
  - operand2 `== 0` -> success only when operand1 is present
  - operand2 `!= 0` -> success only when operand1 is absent
- Success -> `JSR $8C3E`
- Failure -> `AF24 = 1`
- This is the corrected master-table meaning of global opcode `04`.

---

## Strong correction

### Global master opcode `04` old carry-forward mapping should be retired
Retire the stale line that treated global opcode `04` as the old group-1 local `0x04` body at `C1:B815`.

The correct master-table mapping is:

- global opcode `04 -> C1:8FDA`

This matters because pass 61 proved `B80D` is the master table and later slice tables are not independent roots.

---

## Provisional / caution notes

### `01` still wants a final gameplay noun
The record test in `01` is strong mechanically.
It is suggestive that the `FD:A80B`-selected base plus offsets `+3/+5` line up with the already-solved lane block rooted at `5E2D`, but that final noun should stay open for now.

### Do not over-freeze the in-place increment yet
In all three list-transform bodies `01/02/03`, accepted entries are incremented in-place in `AECC` before finalization.
That behavior is real.
Its final higher-level meaning is still open.

### `AE21` still wants a dedicated pass
Pass 63 strengthens the caller context around `AE21`, but does not yet freeze its final noun.
Keep treating it as an existing finalize/reduction helper whose full human-facing meaning remains open.

---

## Carry-forward summary
The early master-opcode band now has a much cleaner structure:

- `00` unconditional replay
- `01/02/03` selector/list-transform bodies
- `04/05/06/07/20/21` hard replay gates

That is the main label-level gain from pass 63.
