# Chrono Trigger Labels — Pass 80

## Purpose
This file records the label upgrades justified by pass 80.

Pass 79 proved that the optional `CD:0018` side was a two-slot auxiliary descriptor stream interpreter, but the big `16B5..` command space still had no real sub-families.

Pass 80 closes the first important chunk of that seam:

- `1654` is now pinned as a real **one-token auxiliary stream interpreter**
- raw bytes `< 0x7F` now tie directly to a derived `D0`-side tile-block source pointer
- `0x7F` is an exact **advance/skip token**
- the first real command families under `0x80..0xFF` are now pinned as:
  - extended sub-dispatch
  - countdown seed
  - paired-delta transform
  - repeat/rewind loop control
  - immediate absolute write
  - indexed 2-word pair copy
  - conditional rewind
  - direct staging writes

This still does **not** freeze the full final noun of the downstream `4500.. -> 5D00..` emit family, but the optional auxiliary stage is now much more clearly a graphics/tile-support VM.

---

## Strengthened helper labels

### CD:1654..CD:169F  ct_cd_interpret_one_auxiliary_stream_token_and_derive_d0_tile_block_request_or_dispatch_command   [strong structural]
- Pulls one byte from the current active auxiliary runtime-slot stream.
- `0x7F` increments the stream pointer only.
- `< 0x7F` biases the token by `CA3A,X`, derives a `D0`-rooted tile-block source pointer into `CA18`, and increments `CA17`.
- `>= 0x80` dispatches through the command-token table at `16B5`.
- Strongest safe reading: one-token interpreter for the auxiliary stream VM.

### CD:16A6..CD:16B4  ct_cd_dispatch_one_auxiliary_command_token_80_ff_by_low7_id   [strong]
- Saves the active slot base in `$43`.
- Advances the stream pointer by one byte.
- Dispatches command tokens `0x80..0xFF` through `16B5` using the token's low 7 bits.

### CD:16B5..CD:17A6  ct_cd_auxiliary_command_token_ptr_table_80_ff   [strong correction]
- This is not just a generic dispatch table anymore.
- It is now pinned as the main 128-command token pointer table for the auxiliary stream VM.

### CD:2A4A..CD:2A8E  ct_cd_auxiliary_token_80_extended_subopcode_dispatcher_32way   [strong structural]
- Token `0x80` reads the following stream byte, doubles it, and dispatches through the local table at `2A51`.
- Strongest safe reading: extended/meta command family with 32 secondary sub-opcodes.

### CD:2DCB..CD:2DD5  ct_cd_auxiliary_token_81_seed_slot_reload_and_current_countdown   [strong]
- Writes the same immediate byte to `CA38,X` and `CA39,X`.
- Exact role: seed reload + current countdown for the active auxiliary runtime slot.

### CD:2DD6..CD:2E9F  ct_cd_auxiliary_token_82_apply_one_of_eight_paired_16bit_delta_ops_to_ca5e_ca60   [strong structural]
- Low 5 bits + 1 of the immediate byte become the magnitude.
- High 3 bits select one of eight local sub-ops through `2DEA`.
- Those sub-ops apply all sign-combination variants over the paired 16-bit fields at `CA5E,X` and `CA60,X`.
- Strongest safe reading: paired-delta operator token for the auxiliary VM.

### CD:2DEA..CD:2DF9  ct_cd_auxiliary_token_82_paired_delta_subop_ptr_table_8   [strong]
- Exact eight-entry local pointer table used by token `0x82`.
- Dispatches the paired add/subtract variants over `CA5E/CA60`.

### CD:2EA2..CD:2EB4  ct_cd_auxiliary_token_83_seed_repeat_resume_pointer_and_repeat_count   [strong]
- Stores the current stream pointer to `CA72,X`.
- Stores `immediate + 1` to `CA74,X`.
- Exact role: repeat-loop seed token.

### CD:2EB5..CD:2EC7  ct_cd_auxiliary_token_84_repeat_until_countdown_exhausted_then_consume_trailing_byte   [strong structural]
- Decrements `CA74,X`.
- While nonzero, rewinds the stream pointer back to `CA72,X`.
- When exhausted, consumes one trailing byte and falls through.

### CD:2EC8..CD:2EDD  ct_cd_auxiliary_token_85_seed_repeat_resume_pointer_and_clear_ca3a   [strong structural]
- Same repeat-loop seed pattern as token `0x83`.
- Also clears `CA3A,X`.

### CD:2EDE..CD:2EF6  ct_cd_auxiliary_token_86_repeat_with_iteration_counter_in_ca3a   [strong structural]
- Same repeat-loop behavior as token `0x84`.
- Increments `CA3A,X` each loop iteration.
- Clears `CA3A,X` when the loop terminates.

### CD:17A9..CD:17BD  ct_cd_auxiliary_token_f9_write_immediate_byte_to_absolute_target   [strong]
- Reads one immediate byte and the following absolute 16-bit destination address.
- Writes the byte directly to that destination.

### CD:17BE..CD:17DE  ct_cd_auxiliary_token_f8_copy_one_indexed_2word_pair_between_2000_2200_tables   [strong structural]
- Reads a source index and destination index from the stream.
- Copies one 2-word record from the `$2000/$2200` table families at the source index to the destination index.

### CD:17DF..CD:17E4  ct_cd_auxiliary_token_f7_store_immediate_to_ce0e   [strong]
- Exact tiny handler: store next stream byte to `CE0E`.

### CD:17E5..CD:17FE  ct_cd_auxiliary_token_f6_conditional_stream_rewind_by_immediate_when_ce10_allows   [strong structural]
- Uses `CE10` as a one-shot latch/gate.
- If the gate condition passes, subtracts the immediate byte from the stream pointer and then clears `CE10`.

### CD:17FF..CD:1804  ct_cd_auxiliary_token_f5_store_immediate_to_cd46   [strong]
- Exact tiny handler: store next stream byte to `CD46`.

### CD:1805..CD:1809  ct_cd_auxiliary_token_f4_call_d1_ebff   [strong]
- Exact wrapper token: `JSL D1:EBFF ; RTS`.

### CD:180A..CD:1812  ct_cd_auxiliary_token_f3_store_immediate_to_cd45_and_increment_cd44   [strong]
- Stores the immediate byte to `CD45`.
- Increments `CD44`.
- Strongest safe reading: seed the one-shot rewind/gate state later consumed by token `0xF2`.

### CD:1813..CD:1829  ct_cd_auxiliary_token_f2_conditional_stream_rewind_by_immediate_when_cd44_allows   [strong structural]
- Structural sibling of token `0xF6`.
- Uses `CD44` as the latch/gate and subtracts the immediate byte from the stream pointer when active.

### CD:182A..CD:1830  ct_cd_auxiliary_token_f1_copy_5d8f_into_indexed_caa4_slot   [strong]
- Reads one immediate slot index byte.
- Copies stage/global byte `5D8F` into `CAA4 + index`.

### CD:184B..CD:184F  ct_cd_auxiliary_token_f0_call_d1_efd0   [strong]
- Exact wrapper token: `JSL D1:EFD0 ; RTS`.

---

## Strengthened RAM/state labels

### 7E:CA17  ct_cd_auxiliary_pending_d0_tile_block_request_count_or_flag   [strong structural]
- Incremented by the raw-data token path in `1654`.
- Cleared/consumed by the `06xx` auxiliary graphics-side follow-up.
- Strongest safe reading: pending auxiliary tile-block request count/flag.

### 7E:CA18..7E:CA19  ct_cd_auxiliary_current_derived_d0_tile_block_source_ptr   [strong structural]
- Written by the raw-data token path in `1654` after biasing the token with `CA3A`.
- Consumed by the `06xx` auxiliary graphics-side follow-up.
- Strongest safe reading: current derived `D0` tile-block source pointer.

### 7E:CA3A..7E:CA49  ct_cd_auxiliary_runtime_slot_stream_bias_or_iteration_bytes_2x16   [provisional strengthened]
- `1654` adds `CA3A,X` to raw data-token values before deriving the `D0`-side source pointer.
- Token `0x86` increments `CA3A,X` per loop iteration and clears it on termination.
- Strongest safe reading: slot-local stream bias / iteration side-effect bytes.

### 7E:CA5E..7E:CA71  ct_cd_auxiliary_runtime_slot_paired_16bit_accumulator_fields   [strong structural]
- Token `0x82` applies eight exact paired add/subtract variants over `CA5E,X` and `CA60,X`.
- That proves these are real 16-bit accumulator-like fields, not generic scratch.
- Final gameplay-facing noun still needs another pass.

### 7E:CA72..7E:CA85  ct_cd_auxiliary_runtime_slot_repeat_resume_ptr_and_repeat_count_fields   [strong structural]
- Tokens `0x83..0x86` prove the role of these fields.
- `CA72,X` = loop resume pointer.
- `CA74,X` = repeat countdown.

### 7E:CD44  ct_cd_auxiliary_token_f2_rewind_latch_count   [provisional strengthened]
- Incremented by token `0xF3`.
- Consumed and cleared by token `0xF2` after conditional rewind.

### 7E:CD45  ct_cd_auxiliary_token_f3_rewind_immediate_staging_byte   [provisional strengthened]
- Written by token `0xF3`.
- Structural sibling state for the `0xF2` conditional rewind family.

### 7E:CD46  ct_cd_auxiliary_token_f5_immediate_staging_byte   [provisional strengthened]
- Directly written by token `0xF5`.
- Final gameplay-facing noun still open.

### 7E:CE0E  ct_cd_auxiliary_token_f7_immediate_staging_byte   [provisional strengthened]
- Directly written by token `0xF7`.
- Final gameplay-facing noun still open.

### 7E:CE10  ct_cd_auxiliary_token_f6_rewind_gate_latch   [provisional strengthened]
- Consumed and cleared by token `0xF6` after the conditional rewind path.
- Strongest safe reading: one-shot rewind gate/latch for the `0xF6` token.

---

## Honest caution
Even after this pass:

- I have **not** finished the full `0x80..0xFF` token table.
- I have **not** decoded all 32 sub-ops under token `0x80`.
- I have **not** frozen the final player-facing noun of the downstream `4500.. -> 5D00.. -> A07B` family.
- I have **not** frozen the exact final noun of the paired `CA5E/CA60` accumulator fields.
- I have **not** frozen the exact gameplay meaning of the `CD44/CD45/CD46` and `CE0E/CE10` latch bytes.
