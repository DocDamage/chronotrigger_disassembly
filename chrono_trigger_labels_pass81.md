# Chrono Trigger Labels — Pass 81

## Purpose
This file records the label upgrades justified by pass 81.

Pass 80 proved that token `0x80` inside the auxiliary `CD:0018` stream VM is a secondary sub-dispatch through `CD:2A51`, but the sub-op table still had no real internal structure.

Pass 81 closes the first strong chunk of that gap:

- the table is now pinned as a **29-entry live sub-op family (`0x00..0x1C`)**, not a clean 32-entry block
- the upper tail now contains several exact wrappers/latches
- `0x15..0x17` now read as a real **E500/E850 strided table-control band**
- `0x0F..0x14` now read as a real **state/preset-builder band**
- `0x00`, `0x0E`, and `0x13` now read as one shared **BB/BC parallel-table builder family**

I still do **not** freeze the final gameplay-facing noun of every affected table.
These labels stay structural where proof is still one notch short.

---

## Strengthened helper labels

### CD:2A51..CD:2A89  ct_cd_auxiliary_token_80_extended_subopcode_ptr_table_29_live_entries   [strong correction]
- The table reached from token `0x80` does **not** expose a clean 32-entry live namespace.
- Straight ROM parsing gives live sub-op targets for `0x00..0x1C` only.
- After that, the bytes are ordinary code, not more valid pointer entries.
- Strongest safe reading: 29-entry live extended sub-op family.

### CD:2AA5..CD:2AA9  ct_cd_auxiliary_token_80_subop_18_call_d1_e91a   [strong]
- Exact wrapper: `JSL D1:E91A ; RTS`.

### CD:2AA1..CD:2AA4  ct_cd_auxiliary_token_80_subop_19_increment_ce10_rewind_gate   [strong]
- Exact one-byte latch setter.
- Increments `CE10` and returns.
- Strongest safe reading: arm/set path for the rewind gate later consumed by token `0xF6`.

### CD:2A9C..CD:2AA0  ct_cd_auxiliary_token_80_subop_1a_call_d1_e899   [strong]
- Exact wrapper: `JSL D1:E899 ; RTS`.

### CD:2A8B..CD:2A96  ct_cd_auxiliary_token_80_subop_1b_increment_8byte_strip_at_9ffa   [strong structural]
- Starts with zeroed X and increments `9FFA,X` across eight consecutive byte positions.
- Final noun of the `9FFA..A001` strip is still open.

### CD:2A97..CD:2A9B  ct_cd_auxiliary_token_80_subop_1c_call_d1_e8c1   [strong]
- Exact wrapper: `JSL D1:E8C1 ; RTS`.

### CD:2AEF..CD:2B04  ct_cd_auxiliary_token_80_subop_15_clear_strided_e500_e502_pair_table   [strong structural]
- Walks in 4-byte steps and clears `E500,X` and `E502,X` until `X == 0x06A0`.
- Strongest safe reading: clear pass over a strided pair-table family.

### CD:2AC6..CD:2AEE  ct_cd_auxiliary_token_80_subop_16_run_tripled_setup_then_decrement_active_e500_by_10_where_e850_live   [strong structural]
- Calls the shared local setup helper three times.
- Walks the same strided family and subtracts `0x0010` from `E500,X` when `E850,X` is nonzero.
- Final gameplay-facing noun of the `E500/E850` families remains open.

### CD:2AAA..CD:2AC5  ct_cd_auxiliary_token_80_subop_17_d1_e984_anchored_local_setup_entry   [provisional strengthened]
- Anchored by the exact wrapper call to `D1:E984`.
- Also advances `CD3B` and falls into a local lookup/copy follow-up.
- Strongest safe reading so far: local setup entry belonging to the same `E500/E850`-side family as sub-ops `0x15/0x16`.

### CD:2B5C..CD:2B63  ct_cd_auxiliary_token_80_subop_0f_clear_99b5_at_index_from_cd00   [strong]
- Loads `CD00` into X and clears `99B5,X`.

### CD:2B45..CD:2B5B  ct_cd_auxiliary_token_80_subop_10_seed_e0_into_parallel_bb_bc_highbyte_tables   [strong structural]
- Writes `0xE0` into `BB07,Y`, `BB87,Y`, and `BC07,Y` in a repeated stride pattern.
- Strongest safe reading: preset builder for three parallel high-byte tables.

### CD:2B27..CD:2B44  ct_cd_auxiliary_token_80_subop_11_seed_mirrored_pair_around_80_and_arm_99d2_bit7   [strong structural]
- Sets `99D2.bit7`.
- Copies `99D3` into `05A5` and `0599`.
- Copies `0x80 - 99D3` into `05A6` and `059A`.
- Strongest safe reading: mirrored/complement pair seed around midpoint `0x80`.

### CD:2B12..CD:2B26  ct_cd_auxiliary_token_80_subop_12_clamp_5da1_to_31_d4   [strong]
- Exact clamp of `5DA1` into `[0x31, 0xD4]`.

### CD:2D39..CD:2DC9  ct_cd_auxiliary_token_80_subop_13_seed_5d9a_then_build_parallel_bb_bc_tables   [strong structural]
- Writes `5D9A = 1`.
- Seeds `A = 0x14`.
- Falls into the shared `2D53` parallel-table builder tail.

### CD:2B05..CD:2B11  ct_cd_auxiliary_token_80_subop_14_seed_cd3a_0060_and_007c_0040   [strong]
- Exact constant seeds:
  - `CD3A = 0x0060`
  - `$007C = 0x0040`

### CD:2D44..CD:2DC9  ct_cd_auxiliary_token_80_subop_0e_build_parallel_bb_bc_tables_fixed_a04   [strong structural]
- Seeds `A = 0x04` and falls into the shared `2D53` builder tail.

### CD:2D4A..CD:2DC9  ct_cd_auxiliary_token_80_subop_00_countdown_variant_of_parallel_bb_bc_table_builder   [strong structural]
- Clears/uses `CD04` and then enters the shared `2D53` builder tail.
- Strongest safe reading: countdown/variation member of the same table-builder family as `0x0E` and `0x13`.

### CD:2D53..CD:2DC9  ct_cd_auxiliary_token_80_shared_parallel_bb06_bb86_bc06_and_bb07_bb87_bc07_builder_tail   [strong structural]
- Shared convergence tail used by sub-ops `0x00`, `0x0E`, and `0x13`.
- Writes repeated-stride values into:
  - `BB06/BB07`
  - `BB86/BB87`
  - `BC06/BC07`
- Final gameplay-facing noun of these three parallel arrays remains one notch below frozen.

---

## Strengthened RAM/state labels

### 7E:CE10  ct_cd_auxiliary_token_f6_rewind_gate_latch   [stronger support]
- Pass 80 already proved that token `0xF6` consumes and clears this latch.
- Pass 81 adds the clean setter path: token `0x80:19` increments it directly.
- Strongest safe reading: rewind gate/latch, not generic scratch.

### 7E:9FFA..7E:A001  ct_cd_auxiliary_token_80_subop_1b_8byte_counter_or_flag_strip   [provisional strengthened]
- Incremented across eight consecutive byte positions by sub-op `0x1B`.
- Final noun remains open.

### 7E:E500..7E:EB9F (strided pair family)  ct_cd_auxiliary_token_80_strided_e500_e502_pair_table_family   [provisional strengthened]
- Sub-op `0x15` clears `E500/E502` in 4-byte steps.
- Sub-op `0x16` subtracts `0x0010` from active `E500` entries where companion `E850` markers are live.
- Strongest safe reading: linked strided pair-table family with an activity/marker companion table.

### 7E:E850..7E:EEEF (strided marker family)  ct_cd_auxiliary_token_80_strided_e850_activity_marker_family   [provisional strengthened]
- Read by sub-op `0x16` as the gate for whether the matching `E500` entry is decremented.
- Final noun still open.

### 7E:99B5..  ct_cd_auxiliary_token_80_indexed_clearable_state_bytes   [provisional strengthened]
- Sub-op `0x0F` clears one indexed byte chosen by `CD00`.

### 7E:99D2  ct_cd_auxiliary_token_80_mirrored_pair_arm_flags   [provisional strengthened]
- Sub-op `0x11` sets bit 7 before seeding the mirrored/complement pair around `99D3`.

### 7E:99D3  ct_cd_auxiliary_token_80_mirrored_pair_seed_byte   [provisional strengthened]
- Used by sub-op `0x11` as the source byte whose complement around `0x80` is also emitted.

### 7E:5DA1  ct_cd_auxiliary_token_80_clamped_state_byte_31_d4   [provisional strengthened]
- Sub-op `0x12` clamps this byte into `[0x31, 0xD4]`.

### 7E:5D9A  ct_cd_auxiliary_token_80_parallel_table_builder_arm_latch   [provisional strengthened]
- Set to `1` by sub-op `0x13` before entering the shared `2D53` builder tail.

### 7E:CD04  ct_cd_auxiliary_token_80_parallel_table_builder_countdown_or_variation_byte   [provisional strengthened]
- Cleared/updated by sub-op `0x00` before entering the shared `2D53` builder tail.

### 7E:CD3A  ct_cd_auxiliary_token_80_constant_seed_word_0060   [provisional strengthened]
- Set to `0x0060` by sub-op `0x14`.

### 7E:BB06.. / 7E:BB86.. / 7E:BC06.. and companions  ct_cd_auxiliary_token_80_parallel_bb_bc_builder_tables   [provisional strengthened]
- Sub-op `0x10` seeds the `+1` high-byte members with `0xE0`.
- Sub-ops `0x00`, `0x0E`, and `0x13` all converge into the shared `2D53` tail that writes the wider family.
- Final noun still open, but these are clearly parallel structured tables, not scratch.

---

## Honest caution
Even after this pass:

- I have **not** frozen the final noun of the `E500/E850` strided families.
- I have **not** frozen the final noun of the `BB06/07`, `BB86/87`, and `BC06/07` tables.
- I have **not** decoded the exact downstream helpers at `D1:E899`, `D1:E8C1`, `D1:E91A`, and `D1:E984`.
- I have **not** tied the newly-decoded `0x80` sub-op state all the way into the final `4500 -> 5D00 -> A07B` emit noun.
