# Chrono Trigger Labels — Pass 69

## Purpose
This file records the label upgrades justified by pass 69.

Pass 69 promotes the selector-control slice at `C1:B8BB..C1:B95F` into its correct master-table range:

- global `57..A9`

It also materially decodes the first promoted selector band:

- global `57..5F`

and carries forward already-earned selector results into their proper master identities.

---

## Strong labels

### C1:A3F6  ct_global_opcode_57_rts_noop_alias   [strong]
- Exact single-byte RTS alias.
- First entry in the promoted selector-control master slice.

### C1:A3F7..C1:A410  ct_global_opcode_58_select_visible_head_occupied_live_slots   [strong structural]
- Scans `AEFF[0..2]`.
- Appends occupied visible-head live slot indices into `AECC`.
- Stores the resulting count in `AECB`.

### C1:A411..C1:A42D  ct_global_opcode_59_select_all_occupied_live_slots   [strong structural]
- Calls the `57/58`-band visible selector first.
- Then appends occupied live slots `3..10` from `AEFF`.
- Stores the final count in `AECB`.

### C1:A42E..C1:A43C  ct_global_opcode_5A_select_current_tail_local_live_slot   [strong structural]
- Writes `B252 + 3` into `AECC[0]`.
- Forces `AECB = 1`.

### C1:A43D..C1:A451  ct_global_opcode_5B_select_current_quad_record_low_nibble_entry   [strong structural]
- Reads `B19E + 4*B252`.
- Masks to the low nibble.
- Stores that value into `AECC[0]`.
- Forces `AECB = 1`.

### C1:A4AF..C1:A4DF  ct_global_opcode_5D_select_target_relation_mode_00   [strong structural]
- Promoted master/global ownership of the pass-30 relation-query target selector for mode `00`.

### C1:A4E0..C1:A507  ct_global_opcode_5E_select_target_relation_mode_01   [strong structural]
- Promoted master/global ownership of the pass-30 relation-query target selector for mode `01`.

### C1:A508..C1:A540  ct_global_opcode_5F_select_one_visible_entry_0_1_2_by_min_current_hp   [strong structural]
- Compares visible-head lane values at `5E30`, `5EB0`, and `5F30`.
- Selects exactly one visible entry index `0..2` with the minimum current-HP value.
- Stores that result into `AECC[0]`.
- Forces `AECB = 1`.

### C1:A6ED..C1:A708  ct_global_opcode_6D_select_nonhead_occupied_live_slots   [strong structural]
- Scans `AEFF[3..10]`.
- Appends occupied non-head live slot indices into `AECC`.
- Stores the resulting count in `AECB`.

### C1:A709..C1:A736  ct_global_opcode_6E_select_target_relation_mode_02   [strong structural]
- Promoted master/global ownership of the pass-30 relation-query target selector for mode `02`.

### C1:A737..C1:A764  ct_global_opcode_6F_select_target_relation_mode_03   [strong structural]
- Promoted master/global ownership of the pass-30 relation-query target selector for mode `03`.

### C1:AB03..C1:AB49  ct_global_opcode_86_build_withheld_tail_candidate_list_and_random_reduce_to_one   [strong]
- Promoted master/global ownership of the pass-57 withheld-tail selector body.

### C1:AB9B..C1:ABC8  ct_global_opcode_8E_select_one_visible_entry_0_1_2_by_min_lane_value   [strong structural]
- Promoted master/global ownership of the pass-58 visible min selector.

### C1:ABC9..C1:AC13  ct_global_opcode_8F_build_live_tail_slot_candidate_list_and_random_reduce_to_one   [strong]
- Promoted master/global ownership of the pass-58 live-tail selector body.

### C1:AFD7..C1:B08E  ct_global_opcode_A0_execute_late_selector_pack_and_capture_tail_result   [strong structural]
- Promoted master/global ownership of the pass-60 late selector-pack executor.

---

## Provisional labels

### C1:A452..C1:A4AE  ct_global_opcode_5C_select_random_visible_head_live_slot_after_optional_refresh   [provisional structural]
- If DP scratch `$24` is zero, runs `B279` across visible entries `0..2` before the selection attempt.
- Then randomly chooses one occupied visible-head live slot.
- Exposes the chosen visible slot in `AECC[0]`.
- Leaves `AECB = 0` on failure.
- The exact higher-level noun of the `$24` gate still wants one more caller-context pass.

---

## Exact promoted fixed-selector globals

### global `7E..85`  fixed single-entry selectors `3..10`   [strong]
- `7E` = literal entry `3`
- `7F` = literal entry `4`
- `80` = literal entry `5`
- `81` = literal entry `6`
- `82` = literal entry `7`
- `83` = literal entry `8`
- `84` = literal entry `9`
- `85` = literal entry `10`

### global `87..8D`  fixed single-entry selectors `0..6`   [strong]
- `87` = literal entry `0`
- `88` = literal entry `1`
- `89` = literal entry `2`
- `8A` = literal entry `3`
- `8B` = literal entry `4`
- `8C` = literal entry `5`
- `8D` = literal entry `6`

---

## Important carry-forward notes

### `57..5F`
These are no longer just “selector-control locals.”
Their correct master identities are now:

- global `57..5F`

### `5C`
Do not over-rename the DP `$24` gate yet.
The safe frozen fact is:
- optional pre-refresh path through `B279`
- then random visible-head occupied-slot selection

### `6D/6E/6F`
These were already effectively solved in earlier selector work.
Pass 69 mainly corrects their **master ownership**, not just their local naming.

### `86/8E/8F/A0`
Same story:
- the semantics were already earned
- the new part is their correct position in the master `B80D` space

---

## Toolkit correction
Pass 69 also updates the worksheet generator so master opcode coverage is no longer truncated at `0x3F`.

The generator now matches the currently proved master span:

- `00..A9`

That prevents future workspace refreshes from silently dropping promoted master rows.

---

## Suggested next seam
- decode the parameterized selector family at global `60..6C`
- then tighten the still-open promoted selector globals at `70..7D`
- then revisit the late promoted range `90..A9`
