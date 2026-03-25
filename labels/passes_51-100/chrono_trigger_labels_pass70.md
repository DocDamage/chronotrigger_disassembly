# Chrono Trigger Labels — Pass 70

## Purpose
This file records the label upgrades justified by pass 70.

Pass 70 closes the promoted master/selector-control band:

- global `60..6C`
- selector-control local `09..15`

It also names the shared helper pipeline that those opcodes use.

---

## Strong labels

### C1:AD68..C1:ADA0  ct_build_visible_fd_offset_nonzero_candidates_and_reduce   [strong structural]
- Clears `AECB`, `AF20`, and `AF21`.
- Forces `AF1F = FF`.
- Runs `AE70` across visible entries `0`, `1`, and `2`.
- Then runs `ADA1` to reduce the resulting candidate list.

### C1:AE70..C1:AECF  ct_scan_one_visible_entry_for_fd_offset_mask_candidate   [strong structural]
- Scans one visible entry indexed by `AF1E`.
- Uses the FD record root table at `FD:A80B`.
- Tests `(record[offset_from_$0A] & AF1F) != 0`.
- Also requires `record[+1D]` to be nonnegative.
- Appends accepted visible entry indices into `AECC` and increments `AECB`.
- Annotates the stored candidate with `0x40` / `0x80` marks from `record[+20]` and tracks those counts in `AF20` / `AF21`.

### C1:ADA1..C1:AE20  ct_reduce_visible_fd_candidates_by_b23a_priority_and_optional_relation_redirect   [strong structural]
- Consumes candidate bytes already staged in `AECC/AECB`.
- Uses `B23A` as the ordered reduction stream.
- Prefers `0x80`-marked candidates when any are present.
- Falls back to the first ordinary `B23A` priority match otherwise.
- If the chosen candidate carries `0x40`, redirects through `A4E0`.
- Otherwise collapses to a single low-nibble entry in `AECC[0]` with `AECB = 1`.

### C1:A541..C1:A54A  ct_global_opcode_60_select_visible_entries_by_positive_fd_record_byte_1D   [strong structural]
- Sets selector offset `0x1D`.
- Uses the shared visible FD-offset family at `AD68`.
- Practical contract: positive `record[+1D]`, then reduce.

### C1:A54B..C1:A554  ct_global_opcode_61_select_visible_entries_by_nonzero_fd_record_byte_1E   [strong structural]
- Sets selector offset `0x1E`.
- Uses the shared visible FD-offset family at `AD68`.
- Also inherits the shared nonnegative `record[+1D]` gate.

### C1:A555..C1:A55E  ct_global_opcode_62_select_visible_entries_by_nonzero_fd_record_byte_1F   [strong structural]
- Sets selector offset `0x1F`.
- Uses the shared visible FD-offset family at `AD68`.
- Also inherits the shared nonnegative `record[+1D]` gate.

### C1:A55F..C1:A568  ct_global_opcode_63_select_visible_entries_by_nonzero_fd_record_byte_20   [strong structural]
- Sets selector offset `0x20`.
- Uses the shared visible FD-offset family at `AD68`.
- Also inherits the shared nonnegative `record[+1D]` gate.

### C1:A569..C1:A572  ct_global_opcode_64_select_visible_entries_by_nonzero_fd_record_byte_21   [strong structural]
- Sets selector offset `0x21`.
- Uses the shared visible FD-offset family at `AD68`.
- Also inherits the shared nonnegative `record[+1D]` gate.

### C1:A573..C1:A5A2  ct_global_opcode_65_select_visible_entries_by_fd_record_byte_1E_mask_02   [strong structural]
- Uses the shared visible FD-offset/mask pipeline.
- Tests `record[+1E] & 0x02`.
- Also inherits the shared nonnegative `record[+1D]` gate.

### C1:A5A3..C1:A5D2  ct_global_opcode_66_select_visible_entries_by_fd_record_byte_1E_mask_80   [strong structural]
- Uses the shared visible FD-offset/mask pipeline.
- Tests `record[+1E] & 0x80`.
- Also inherits the shared nonnegative `record[+1D]` gate.

### C1:A5D3..C1:A602  ct_global_opcode_67_select_visible_entries_by_fd_record_byte_1E_mask_04   [strong structural]
- Uses the shared visible FD-offset/mask pipeline.
- Tests `record[+1E] & 0x04`.
- Also inherits the shared nonnegative `record[+1D]` gate.

### C1:A603..C1:A632  ct_global_opcode_68_select_visible_entries_by_fd_record_byte_21_mask_04   [strong structural]
- Uses the shared visible FD-offset/mask pipeline.
- Tests `record[+21] & 0x04`.
- Also inherits the shared nonnegative `record[+1D]` gate.

### C1:A633..C1:A662  ct_global_opcode_69_select_visible_entries_by_fd_record_byte_21_mask_40   [strong structural]
- Uses the shared visible FD-offset/mask pipeline.
- Tests `record[+21] & 0x40`.
- Also inherits the shared nonnegative `record[+1D]` gate.

### C1:A663..C1:A692  ct_global_opcode_6A_select_visible_entries_by_fd_record_byte_20_mask_10   [strong structural]
- Uses the shared visible FD-offset/mask pipeline.
- Tests `record[+20] & 0x10`.
- Also inherits the shared nonnegative `record[+1D]` gate.

### C1:A693..C1:A6C2  ct_global_opcode_6B_select_visible_entries_by_fd_record_byte_01_mask_08   [strong structural]
- Uses the shared visible FD-offset/mask pipeline.
- Tests `record[+01] & 0x08`.
- Also inherits the shared nonnegative `record[+1D]` gate.

### C1:A6C3..C1:A6EC  ct_global_opcode_6C_select_occupied_live_tail_slots_except_current   [strong structural]
- Computes the current tail-local live slot as `B252 + 3`.
- Scans live slots `3..10`.
- Appends every occupied slot except that current one into `AECC`.
- Stores the resulting count in `AECB`.

---

## Strong promoted selector-control locals

### selector `09`  ct_select_visible_entries_by_positive_fd_record_byte_1D   [strong structural]
- Local selector-control ownership of global `60`.

### selector `0A`  ct_select_visible_entries_by_nonzero_fd_record_byte_1E   [strong structural]
- Local selector-control ownership of global `61`.

### selector `0B`  ct_select_visible_entries_by_nonzero_fd_record_byte_1F   [strong structural]
- Local selector-control ownership of global `62`.

### selector `0C`  ct_select_visible_entries_by_nonzero_fd_record_byte_20   [strong structural]
- Local selector-control ownership of global `63`.

### selector `0D`  ct_select_visible_entries_by_nonzero_fd_record_byte_21   [strong structural]
- Local selector-control ownership of global `64`.

### selector `0E`  ct_select_visible_entries_by_fd_record_byte_1E_mask_02   [strong structural]
- Local selector-control ownership of global `65`.

### selector `0F`  ct_select_visible_entries_by_fd_record_byte_1E_mask_80   [strong structural]
- Local selector-control ownership of global `66`.

### selector `10`  ct_select_visible_entries_by_fd_record_byte_1E_mask_04   [strong structural]
- Local selector-control ownership of global `67`.

### selector `11`  ct_select_visible_entries_by_fd_record_byte_21_mask_04   [strong structural]
- Local selector-control ownership of global `68`.

### selector `12`  ct_select_visible_entries_by_fd_record_byte_21_mask_40   [strong structural]
- Local selector-control ownership of global `69`.

### selector `13`  ct_select_visible_entries_by_fd_record_byte_20_mask_10   [strong structural]
- Local selector-control ownership of global `6A`.

### selector `14`  ct_select_visible_entries_by_fd_record_byte_01_mask_08   [strong structural]
- Local selector-control ownership of global `6B`.

### selector `15`  ct_select_occupied_live_tail_slots_except_current   [strong structural]
- Local selector-control ownership of global `6C`.

---

## Honest caution
Do not over-name these as concrete gameplay nouns yet:

- `B23A`
- the `0x40` redirect mark
- the `0x80` preferred mark

What pass 70 proves is the reducer mechanics, not the final human-facing noun.

---

## Suggested next seam
- decode the promoted selector-control master band at global `70..7D`
