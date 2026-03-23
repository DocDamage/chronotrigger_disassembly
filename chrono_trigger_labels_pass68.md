# Chrono Trigger Labels — Pass 68

## Purpose
This file records the label upgrades justified by pass 68.

Pass 68 finishes the promotion of the old local `B85F` and `B88D` slices into their correct master-table globals:

- global `30..3F`
- global `40..56`

It also materially strengthens two old provisional bodies:

- `C1:9967`
- `C1:9981`

---

## Strong labels

### C1:9967..C1:9977  ct_global_opcode_32_capture_inline_param1_to_aee4   [strong structural]
- Reads the current stream byte at `CC:[B1D2 + 1]`.
- Stores it into `AEE4`.
- Does not locally advance `B1D2`.
- Best current reading: tiny inline-parameter capture body for later follow-up state.

### C1:9981..C1:99B3  ct_global_opcode_39_3F_gate_on_materializable_canonical_tail_slot_exists   [strong structural]
- Scans 8 tail slots.
- Accepts only when:
  - `AF0D[x] != FF`
  - `AF02[x] == FF`
  - `AF15.bit7` clear
- Success clears `AF24`; zero accepted entries force `AF24 = 2`.
- Exact alias body for global opcodes `39` and `3F`.

### C1:99B8..C1:99BD  ct_global_opcode_40_set_group2_continuation_2   [strong]
- Writes `B3B8 = 2` and returns.

### C1:99BE..C1:9A38  ct_global_opcode_41_seed_single_from_5e15_finalize   [strong structural]
- Promoted master ownership of the old group-2 `01` body.
- Seeds one entry from `5E15[current]`.
- Captures inline parameters into `AEE4/AEE5`.
- Uses unique long helper `FD:AB01`.
- Finalizes through `AC89/ACCE` with `B3B8 = 0`.

### C1:9A39..C1:9B45  ct_global_opcode_42_seed_from_b16e_validate_commit   [strong structural]
- Table-entry wrapper lands in `9A3D`.
- Seeds one entry from `B16E[current]`.
- Optionally resolves inline selectors through `AC14`.
- Validates through `C1DD` and commits through `AD09/AD35/FDAAD2/AC89/ACCE`.

### C1:9DCE..C1:9E61  ct_global_opcode_4D_bitmask_state_control   [strong]
- Promoted master ownership of the old group-2 `0D` state-control body.
- Operand bits drive a mix of per-slot and global control writes.

### C1:9E63..C1:9E77  ct_global_opcode_4F_optional_cd0033_then_set_continuation_2   [strong]
- If operand 1 is nonzero, calls `JSL $CD0033`.
- Then writes `B3B8 = 2` and returns.

### C1:9E78..C1:9F59  ct_global_opcode_50_materialize_tail_slots_from_canonical_map_finalize   [strong]
- Promoted master ownership of the old group-2 `10` body.
- Scans canonical/live/deferred tail state through `AF0D/AF02/AF15`.
- Builds selected entries and follow-up masks.
- Best current noun: materialize eligible tail slots from canonical map, then finalize.

### C1:9F5A..C1:9FD1  ct_global_opcode_51_group_base_write4_pairs   [strong]
- Promoted master ownership of the old group-2 `11` writer body.

### C1:9FD2..C1:A14D  ct_global_opcode_52_group_base_write5_pairs_validate   [strong]
- Promoted master ownership of the old group-2 `12` writer-plus-validation body.

### C1:A14E..C1:A187  ct_global_opcode_53_sat_signed_delta_to_current_b158   [strong]
- Promoted master ownership of the old group-2 `13` saturating signed-delta body.

### C1:A396..C1:A3D0  ct_global_opcode_56_wrapper_fused_fd_a990   [strong]
- Promoted master ownership of the old group-2 `16` thin wrapper around `FD:A990`.

---

## Exact alias / stub labels

### pure `RTS`
- `31` = `ct_global_opcode_31_rts_noop_alias`   [exact alias]
- `33` = `ct_global_opcode_33_rts_noop_alias`   [exact alias]
- `35` = `ct_global_opcode_35_rts_noop_alias`   [exact alias]
- `36` = `ct_global_opcode_36_rts_noop_alias`   [exact alias]
- `37` = `ct_global_opcode_37_rts_noop_alias`   [exact alias]
- `38` = `ct_global_opcode_38_rts_noop_alias`   [exact alias]
- `43` = `ct_global_opcode_43_rts_noop_alias`   [exact alias]
- `4E` = `ct_global_opcode_4E_rts_noop_alias`   [exact alias]

### `STZ AF24 ; RTS`
- `30` = `ct_global_opcode_30_clear_short_circuit_and_return`   [exact alias]
- `34` = `ct_global_opcode_34_clear_short_circuit_and_return`   [exact alias]
- `3A` = `ct_global_opcode_3A_clear_short_circuit_and_return`   [exact alias]
- `3B` = `ct_global_opcode_3B_clear_short_circuit_and_return`   [exact alias]
- `3C` = `ct_global_opcode_3C_clear_short_circuit_and_return`   [exact alias]
- `3D` = `ct_global_opcode_3D_clear_short_circuit_and_return`   [exact alias]
- `3E` = `ct_global_opcode_3E_clear_short_circuit_and_return`   [exact alias]

### exact shared body
- `39` = `ct_global_opcode_39_gate_on_materializable_canonical_tail_slot_exists`   [exact shared-body alias]
- `3F` = same body as `39`   [exact shared-body alias]

---

## Promoted-but-still-provisional master labels
These are useful ownership corrections, but not strong enough yet for flavored subsystem names.

- `44` = `ct_global_opcode_44_varctrl_shared_entry_a`   [provisional]
- `45` = `ct_global_opcode_45_varctrl_shared_entry_b`   [provisional]
- `46` = `ct_global_opcode_46_body`   [provisional]
- `47` = `ct_global_opcode_47_body`   [provisional]
- `48` = `ct_global_opcode_48_body`   [provisional]
- `49` = `ct_global_opcode_49_body`   [provisional]
- `4A` = `ct_global_opcode_4A_body`   [provisional]
- `4B` = `ct_global_opcode_4B_body`   [provisional]
- `4C` = `ct_global_opcode_4C_body`   [provisional]
- `54` = `ct_global_opcode_54_multi_target_sat_adjust`   [provisional]
- `55` = `ct_global_opcode_55_multi_target_sat_adjust`   [provisional]

---

## Important carry-forward notes

### `32`
Do not over-rename this to a gameplay-facing noun.
The strong fact is narrower and safer:
- it captures the current inline byte into `AEE4`

### `39 / 3F`
Do not blur these back into generic “slot available” wording.
The proved gate is specifically on:
- canonical tail present
- live tail absent
- deferred-materialization bit clear

### `40..56`
Do not keep referring to these as only old group-2 locals in later reports.
Their correct master identities are now:
- global `40..56`

### `44..4C`
Promotion does **not** mean those bodies are newly solved.
Keep the provisional tone until caller/state evidence tightens them.

---

## Suggested next seam
- promote global `57..5F` into master ownership
- then continue through the early `B8BB` slice
- with special focus on whether `44..4C` can be renamed more strongly from caller evidence
