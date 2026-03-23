# Chrono Trigger Labels — Pass 65

## Purpose
This file records the label upgrades justified by pass 65.

The biggest result is the split inside the early master-opcode seam:
- `0C/0D/0E/0F/10` are relation-query wrappers / gates
- `11/12` are not; they are direct current-slot quad-record gates over `B19E/B19F + 4*B252`

---

## Strong structural labels

### C1:925D..C1:92A2  ct_global_opcode_0C_gate_tail_replay_on_relation_mode04_current_subject_vs_selection_head   [strong structural]
- Calls `AC14`.
- Empty selection -> `AF24 = 1`.
- Seeds relation-query mode `04` with:
  - `986F = B252 + 3`
  - `9870 = AECC[0]`
- Calls service `5` through `JSR $0003`.
- Operand `+1` selects the final zero/nonzero polarity of `9872`.
- Success writes `AECB = 1` and continues through `8C3E`.

### C1:938D..C1:93E5  ct_global_opcode_0F_gate_tail_replay_on_relation_mode08_current_subject_vs_selection_head   [strong structural]
- Calls `AC14`.
- Empty selection -> `AF24 = 1`.
- Seeds relation-query mode `08` with:
  - `986F = B252 + 3`
  - `9870 = AECC[0]`
  - `9871 = (operand2 << 2) | 1`
- Operand `+1` selects the final zero/nonzero polarity of `9872`.
- Success continues through `8C3E`.
- Pre-write `9872 = 05` is dead for normal service-5 flow because `2986` clears `9872` before dispatch.

### C1:93E6..C1:9429  ct_global_opcode_10_gate_tail_replay_on_current_subject_row_column_band_query   [strong structural]
- Does not call `AC14`.
- Selects relation mode `09/0A/0B/0C` from operands `+2/+3`.
- Uses current subject slot `986F = B252 + 3`.
- Succeeds only when the chosen mode leaves `9872 == 0`.
- Effective success regions are:
  - mode `09`: `Y>>4 >= 0x08`
  - mode `0A`: `Y>>4 < 0x08`
  - mode `0B`: `X>>4 >= 0x0B`
  - mode `0C`: `X>>4 < 0x05`

### C1:942A..C1:9473  ct_global_opcode_11_gate_tail_replay_on_current_b19e_upper_nibble_class   [strong structural]
- Direct current-slot gate, not a relation-query wrapper.
- Computes `X = B252 * 4`.
- Reads `B19E[X] & 0xF0`.
- Operand `+1` selects target class `0x40` vs `0x50`.
- Operand `+3` selects equality vs inequality.
- Success continues through `8C3E`; failure sets `AF24 = 1`.

### C1:9474..C1:94D1  ct_global_opcode_12_gate_tail_replay_on_current_b19e_b19f_pair_mode   [strong structural]
- Direct current-slot gate, not a relation-query wrapper.
- Computes `X = B252 * 4`.
- Reads:
  - `B19E[X] & 0xF0`
  - `B19F[X]`
- Operand `+1` selects target high nibble `0x40` vs `0x50`.
- Operand `+2` selects exact second-byte compare value.
- Operand `+3 == 0` -> both comparisons must match.
- Operand `+3 != 0` -> both comparisons must differ.

---

## Provisional structural labels

### C1:92A3..C1:9313  ct_global_opcode_0D_mark_non_subject_selected_entries_by_relation_mode05_zero_then_reduce   [provisional structural]
- Calls `AC14`.
- Sets current subject slot `986F = B252 + 3`.
- Uses relation-query mode `05`.
- Skips the subject slot if it appears in the selected list.
- Marks selected entries whose mode-`05` result leaves `9872 == 0`.
- Mode `05` is now known strongly enough to be the close-Y / `abs(subject_y - arg_y) < 0x20` predicate.
- Marked candidates are reduced through `AE21`.
- Final replay gate still depends on residual `9872` plus operand `+1`, so the top-level human-facing contract should stay provisional.

### C1:9314..C1:938C  ct_global_opcode_0E_mark_non_subject_selected_entries_by_parameterized_relation_mode_zero_then_reduce   [provisional structural]
- Same structural family as `0D`.
- Seeds relation mode with `986E = operand2 + 0x06`.
- Skips the current subject slot.
- Marks selected entries whose query leaves `9872 == 0`.
- Reduces them through `AE21`.
- Final replay gate still depends on residual `9872` plus operand `+1`.

---

## Supporting interpretation upgrades

### C1:2BBC  relation-query mode `05`   [strong structural support]
- Absolute Y-delta test over `1D23`.
- Leaves `9872 = 00` when `abs(subject_y - arg_y) < 0x20`.
- Leaves `9872 = FF` otherwise.

### C1:2BDA  relation-query mode `06`   [strong structural support]
- Vertical ordering test over `1D23`.
- Leaves `9872 = 00` when `subject_y < arg_y`.
- Leaves `9872 = FF` otherwise.

### C1:2CA7 / C1:2CBA / C1:2CCD / C1:2CE0   relation-query modes `09..0C`   [strong structural support]
- These are coarse row/column band predicates over the current subject slot.
- `09/0A` use `1D23 >> 4`.
- `0B/0C` use `1D0C >> 4`.

---

## Corrections to carry forward
- Do not keep describing opcode `0E` as a fixed mode-`06` wrapper. It is parameterized by operand `+2`.
- Do not keep extending the relation-query family through opcode `12`. That overstates the shared structure. `11/12` are direct record gates.
- Opcode `10` is now stronger than “mode picker” wording; it is a real current-subject row/column band gate.
