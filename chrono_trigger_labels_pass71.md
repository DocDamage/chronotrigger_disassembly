# Chrono Trigger Labels — Pass 71

## Purpose
This file records the label upgrades justified by pass 71.

Pass 71 closes the promoted selector-control master band:

- global `70..7D`

It also promotes the matching selector-control locals:

- selector `19..26`

---

## Strong global labels

### C1:A765..C1:A7A8  ct_global_opcode_70_select_one_nonhead_occupied_live_slot_by_min_nonzero_fd_record_word_03   [strong structural]
- Scans occupied live slots `3..10`.
- Resolves each slot through `FD:A80B + slot*2`.
- Compares the 16-bit word at `record + 3`.
- Keeps the smallest nonzero value and stores the corresponding slot into `AECC[0]`.
- Forces `AECB = 1`.

### C1:A7A9..C1:A7E4  ct_global_opcode_71_select_nonhead_occupied_live_slots_excluding_primary_seed_by_positive_fd_record_byte_1D   [strong structural]
- Nonhead counterpart of the pass-70 visible FD-byte selector family.
- Scans live slots `3..10`.
- Skips the primary-seed slot indexed by `B18B`.
- Uses `AE70 -> ADA1` to select/reduce candidates.

### C1:A7E5..C1:A818  ct_global_opcode_72_select_nonhead_occupied_live_slots_by_positive_fd_record_byte_1D   [strong structural]
- Nonhead counterpart of global `60`.
- Scans occupied live slots `3..10` through `AE70 -> ADA1`.
- No `B18B` exclusion.

### C1:A819..C1:A854  ct_global_opcode_73_select_nonhead_occupied_live_slots_excluding_primary_seed_by_nonzero_fd_record_byte_1E   [strong structural]
- Tests `record[+1E]` through the shared `AE70 -> ADA1` reducer path.
- Also inherits the shared nonnegative `record[+1D]` gate.
- Skips the primary-seed slot indexed by `B18B`.

### C1:A855..C1:A888  ct_global_opcode_74_select_nonhead_occupied_live_slots_by_nonzero_fd_record_byte_1E   [strong structural]
- Nonhead counterpart of global `61`.
- Uses the shared `AE70 -> ADA1` reducer path.
- No `B18B` exclusion.

### C1:A889..C1:A8C4  ct_global_opcode_75_select_nonhead_occupied_live_slots_excluding_primary_seed_by_nonzero_fd_record_byte_1F   [strong structural]
- Tests `record[+1F]` through the shared `AE70 -> ADA1` reducer path.
- Skips the primary-seed slot indexed by `B18B`.

### C1:A8F9..C1:A934  ct_global_opcode_77_select_nonhead_occupied_live_slots_excluding_primary_seed_by_fd_record_byte_1E_mask_02   [strong structural]
- Uses the shared nonhead FD-offset/mask pipeline.
- Tests `record[+1E] & 0x02`.
- Skips the primary-seed slot indexed by `B18B`.

### C1:A935..C1:A970  ct_global_opcode_78_select_nonhead_occupied_live_slots_excluding_primary_seed_by_fd_record_byte_1E_mask_80   [strong structural]
- Uses the shared nonhead FD-offset/mask pipeline.
- Tests `record[+1E] & 0x80`.
- Skips the primary-seed slot indexed by `B18B`.

### C1:A971..C1:A9AC  ct_global_opcode_79_select_nonhead_occupied_live_slots_excluding_primary_seed_by_fd_record_byte_1E_mask_04   [strong structural]
- Uses the shared nonhead FD-offset/mask pipeline.
- Tests `record[+1E] & 0x04`.
- Skips the primary-seed slot indexed by `B18B`.

### C1:A9AD..C1:A9E8  ct_global_opcode_7A_select_nonhead_occupied_live_slots_excluding_primary_seed_by_fd_record_byte_21_mask_40   [strong structural]
- Uses the shared nonhead FD-offset/mask pipeline.
- Tests `record[+21] & 0x40`.
- Skips the primary-seed slot indexed by `B18B`.

### C1:A9E9..C1:AA24  ct_global_opcode_7B_select_nonhead_occupied_live_slots_excluding_primary_seed_by_fd_record_byte_1D_mask_02   [strong structural]
- Uses the shared nonhead FD-offset/mask pipeline.
- Tests `record[+1D] & 0x02`.
- Skips the primary-seed slot indexed by `B18B`.

### C1:AA25..C1:AA60  ct_global_opcode_7C_select_nonhead_occupied_live_slots_excluding_primary_seed_by_fd_record_byte_19_mask_01   [strong structural]
- Uses the shared nonhead FD-offset/mask pipeline.
- Tests `record[+19] & 0x01`.
- Skips the primary-seed slot indexed by `B18B`.

### C1:AA61..C1:AAAA  ct_global_opcode_7D_select_one_nonhead_occupied_live_slot_excluding_primary_seed_by_min_nonzero_fd_record_word_03   [strong structural]
- Same minimum-word selector family as global `70`.
- Scans occupied live slots `3..10`.
- Skips the primary-seed slot indexed by `B18B`.
- Chooses the smallest nonzero `record_word(+3)` candidate and stores its slot into `AECC[0]`.

---

## Provisional global label

### C1:A8C5..C1:A8F8  ct_global_opcode_76_select_nonhead_occupied_live_slots_by_nonzero_fd_record_byte_1F   [provisional structural]
- Structurally matches the no-exclusion sibling of global `75`.
- Intended to test `record[+1F]` through the shared `AE70 -> ADA1` reducer path.
- But the loop update stores back into `$0E` with `STA $0E` at `C1:A8E9` instead of the expected `STX $0E`.
- Keep the family interpretation, but preserve explicit caution until runtime confirms the practical behavior.

---

## Strong promoted selector-control locals

### selector `19`  ct_select_one_nonhead_occupied_live_slot_by_min_nonzero_fd_record_word_03   [strong structural]
- Local selector-control ownership of global `70`.

### selector `1A`  ct_select_nonhead_occupied_live_slots_excluding_primary_seed_by_positive_fd_record_byte_1D   [strong structural]
- Local selector-control ownership of global `71`.

### selector `1B`  ct_select_nonhead_occupied_live_slots_by_positive_fd_record_byte_1D   [strong structural]
- Local selector-control ownership of global `72`.

### selector `1C`  ct_select_nonhead_occupied_live_slots_excluding_primary_seed_by_nonzero_fd_record_byte_1E   [strong structural]
- Local selector-control ownership of global `73`.

### selector `1D`  ct_select_nonhead_occupied_live_slots_by_nonzero_fd_record_byte_1E   [strong structural]
- Local selector-control ownership of global `74`.

### selector `1E`  ct_select_nonhead_occupied_live_slots_excluding_primary_seed_by_nonzero_fd_record_byte_1F   [strong structural]
- Local selector-control ownership of global `75`.

### selector `20`  ct_select_nonhead_occupied_live_slots_excluding_primary_seed_by_fd_record_byte_1E_mask_02   [strong structural]
- Local selector-control ownership of global `77`.

### selector `21`  ct_select_nonhead_occupied_live_slots_excluding_primary_seed_by_fd_record_byte_1E_mask_80   [strong structural]
- Local selector-control ownership of global `78`.

### selector `22`  ct_select_nonhead_occupied_live_slots_excluding_primary_seed_by_fd_record_byte_1E_mask_04   [strong structural]
- Local selector-control ownership of global `79`.

### selector `23`  ct_select_nonhead_occupied_live_slots_excluding_primary_seed_by_fd_record_byte_21_mask_40   [strong structural]
- Local selector-control ownership of global `7A`.

### selector `24`  ct_select_nonhead_occupied_live_slots_excluding_primary_seed_by_fd_record_byte_1D_mask_02   [strong structural]
- Local selector-control ownership of global `7B`.

### selector `25`  ct_select_nonhead_occupied_live_slots_excluding_primary_seed_by_fd_record_byte_19_mask_01   [strong structural]
- Local selector-control ownership of global `7C`.

### selector `26`  ct_select_one_nonhead_occupied_live_slot_excluding_primary_seed_by_min_nonzero_fd_record_word_03   [strong structural]
- Local selector-control ownership of global `7D`.

---

## Provisional promoted selector-control local

### selector `1F`  ct_select_nonhead_occupied_live_slots_by_nonzero_fd_record_byte_1F   [provisional structural]
- Local selector-control ownership of global `76`.
- Carries the same explicit caution about the anomalous `STA $0E` loop-update byte.

---

## Honest caution
Two details should stay explicitly attached to this band:

- globals `70` and `7D` do not show an explicit empty/no-hit failure path
- global `76` / selector `1F` has a real byte-level loop-update anomaly at `C1:A8E9`

That means the overall family is strong, but those exact edge behaviors still deserve runtime confirmation.

---

## Suggested next seam
- revisit the late promoted band at global `90..A9`
- keep global `76` / selector `1F` on the runtime shortlist
