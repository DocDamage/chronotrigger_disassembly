# Chrono Trigger Labels — Pass 149

## Purpose

Pass 149 closes the callable/helper family that pass 148 left open at `C2:EF65..C2:F00F`, and it also closes the immediate callable spillover through exact `C2:F113`.

## Strong labels

### C2:EF65..C2:EF7D  ct_c2_ff_bank_script_template_interpreter_front_end_latching_88_87_and_65_then_running_ef7e   [strong structural]
- Latches exact parameter byte into exact `88` and masked count byte `87`.
- Mirrors exact destination pointer `X -> 65`.
- Rebinds the exact data bank from the exact accumulator high byte.
- Runs exact helper `EF7E`.
- Clears exact bits `0xDC` from exact byte `7E`.
- Strongest safe reading: exact FF-bank script/template interpreter front-end latching exact `88/87/65`, rebinding the exact source bank, and then running exact helper `EF7E`.

### C2:EF7E..C2:EF96  ct_c2_db_y_byte_token_interpreter_loop_dispatching_low_tokens_via_efbe_and_high_tokens_via_ef97   [strong structural]
- Reads one exact token byte from exact `DB:[Y]`.
- Exact token `00` terminates immediately.
- Exact tokens `< 0x10` dispatch through exact helper `EFBE`.
- Exact tokens `>= 0x10` route through exact helper `EF97` and decrement exact count byte `87`.
- Strongest safe reading: exact `DB:[Y]` byte-token interpreter loop dispatching low tokens via exact `EFBE` and higher tokens via exact `EF97`.

### C2:EF97..C2:EFBD  ct_c2_paired_byte_writer_with_optional_ff_shadow_mirror_to_7dffc0_plus_x   [strong structural]
- Uses exact mode/flag byte `88`.
- Exact nonnegative exact `88` plus exact `FF` token mirrors one exact pair into exact `7D:FFC0+X`.
- Always writes one exact pair into exact `7E:0000+X`.
- Advances exact destination pointer `X += 2`.
- Strongest safe reading: exact paired-byte writer with optional exact `FF` sentinel shadow mirror to exact `7D:FFC0+X`.

### C2:EFBE..C2:EFD3  ct_c2_local_opcode_dispatch_helper_using_per_jmp_and_efd4_table   [strong structural]
- Masks and doubles one exact incoming opcode/token.
- Selects one exact handler word from exact local table `EFD4`.
- Uses exact `PER / JMP (8A)` dispatch mechanics.
- Exact `EFD3` is the exact default/no-op return lane.
- Strongest safe reading: exact local opcode dispatch helper using exact `PER / JMP` and exact handler table `EFD4`.

### C2:EFD4..C2:EFF3  ct_c2_local_16_word_opcode_handler_table_for_efbe   [strong structural]
- Exact local 16-word opcode-handler table consumed by exact helper `EFBE`.
- Table words now pinned: `EFD3`, `EFF4`, `F005`, `F011`, `F022`, `F036`, `F0A2`, `F071`, `F08D`, `F0B8`, `F068`, `F0C1`, `F0D1`, `EFD3`, `EFD3`, `EFD3`.
- Strongest safe reading: exact local 16-word opcode-handler table for exact helper `EFBE`.

### C2:EFF4..C2:F004  ct_c2_signed_mode_write_pointer_step_helper_selecting_0080_or_0040_into_65_x   [strong structural]
- Starts from exact step word `0x0080`.
- Uses the exact sign-bearing mode word at exact `87/88`.
- Switches to exact step word `0x0040` when the exact negative mode bit is active.
- Adds that exact step into exact destination word `65/X`.
- Strongest safe reading: exact signed-mode write-pointer step helper selecting exact `0x0080` or `0x0040` into exact `65/X`.

### C2:F005..C2:F010  ct_c2_inline_offset_to_65_x_write_pointer_helper_using_y_and_61   [strong structural]
- Reads one exact 16-bit offset from exact `[Y]`.
- Adds that exact offset to exact base word `61`.
- Stores the exact result into exact `65/X`.
- Advances exact `Y += 2`.
- Strongest safe reading: exact inline offset-to-write-pointer helper using exact `[Y]` and exact base word `61`.

### C2:F011..C2:F021  ct_c2_four_byte_two_word_wrapper_into_f114_then_shared_skip_tail   [strong structural]
- Reads one exact 16-bit word from exact `[Y]` and one exact 16-bit word from exact `[Y+2]`.
- Routes that exact pair into exact helper `F114`.
- Reuses the exact shared four-byte skip tail.
- Strongest safe reading: exact four-byte two-word wrapper into exact `F114` and then the exact shared skip tail.

### C2:F022..C2:F035  ct_c2_three_byte_far_script_wrapper_rebinding_bank_then_running_ef7e   [strong structural]
- Reconstructs one exact far script/template source from exact record bytes rooted at exact `[Y]`.
- Rebinds the exact source data bank from that exact far source.
- Runs exact helper `EF7E`.
- Reuses the exact shared three-byte skip tail.
- Strongest safe reading: exact three-byte far-script wrapper rebinding the exact bank and then running exact `EF7E`.

### C2:F036..C2:F067  ct_c2_local_7e_bank_five_step_subscript_expander_using_forced_8005_then_ff_fill_tail   [strong structural]
- Saves and restores the exact incoming mode/count word at exact `87/88`.
- Forces exact work word `87/88 = 0x8005`.
- Rebinds the exact data bank to exact `7E`.
- Runs one exact local subscript through exact helper `EF7E`.
- Emits exact `FF` sentinel pairs through exact helper `EF97` until the forced exact count is exhausted.
- Strongest safe reading: exact local `7E`-bank five-step subscript expander using exact forced work word `0x8005` and an exact `FF` fill tail.

### C2:F068..C2:F070  ct_c2_single_byte_latch_helper_copying_y_to_7e   [strong structural]
- Copies one exact byte from exact `[Y]` into exact byte `7E`.
- Advances exact `Y += 1`.
- Strongest safe reading: exact single-byte latch helper copying exact `[Y]` into exact byte `7E`.

### C2:F071..C2:F08C  ct_c2_7e_pointed_word_importer_writer_decrementing_87_then_shared_skip_tail   [strong structural]
- Rebinds the exact data bank to exact `7E`.
- Reads one exact pointed source word rooted at exact `[Y]`.
- Imports one exact 16-bit word from exact `7E:[pointer]`.
- Stores that exact word into exact destination `[X]`.
- Decrements exact count byte `87`.
- Reuses the exact shared two-byte skip tail.
- Strongest safe reading: exact `7E`-pointed word importer/writer decrementing exact `87` and then reusing the exact shared skip tail.

### C2:F08D..C2:F0A1  ct_c2_repeated_ff_sentinel_pair_emitter_using_low_byte_count_at_y   [strong structural]
- Uses the exact low byte at exact `[Y]` as the exact loop count.
- Emits exact sentinel byte `FF` through exact helper `EF97`.
- Repeats until the exact requested count reaches zero.
- Strongest safe reading: exact repeated `FF` sentinel-pair emitter using the exact low byte count at exact `[Y]`.

### C2:F0A2..C2:F0B7  ct_c2_masked_0x1c_flag_import_helper_into_7e_from_7e_pointer   [strong structural]
- Clears exact bits `0x1C` from exact byte `7E`.
- Loads one exact source byte from exact `7E:[pointer]`.
- Masks that exact source byte down to exact bits `0x1C`.
- Merges those exact bits back into exact byte `7E`.
- Strongest safe reading: exact masked exact `0x1C` flag import helper into exact byte `7E` from one exact `7E` pointer operand.

### C2:F0B8..C2:F0C0  ct_c2_mode_flag_latch_helper_copying_y_to_88   [strong structural]
- Copies one exact byte from exact `[Y]` into exact byte `88`.
- Advances exact `Y += 1`.
- Strongest safe reading: exact mode/flag latch helper copying exact `[Y]` into exact byte `88`.

### C2:F0C1..C2:F0CF  ct_c2_four_byte_two_word_wrapper_into_f227_then_shared_skip_tail   [strong structural]
- Reads one exact 16-bit word from exact `[Y]` and one exact 16-bit word from exact `[Y+2]`.
- Routes that exact pair into exact helper `F227`.
- Reuses the exact shared four-byte skip tail.
- Strongest safe reading: exact four-byte two-word wrapper into exact `F227` and then the exact shared skip tail.

### C2:F0D0..C2:F113  ct_c2_indexed_ffcf33_threshold_gate_owner_with_7e11_route_or_2f_fallback_packet   [strong structural]
- Uses one exact selector/index byte from exact `[Y]`.
- Uses one exact pointed source rooted at exact `[Y+1]`.
- Compares one exact `7E`-bank source word against exact FF-bank threshold table `FF:CF33[index]`.
- On one exact lane, routes into exact helper `F114` with exact rebuilt `0x7E11` state.
- On the other exact lane, materializes one exact four-byte fallback packet at exact destination `[X]` using exact byte `0x2F` and exact byte `7E`.
- Strongest safe reading: exact indexed exact `FF:CF33` threshold gate owner with exact `0x7E11` route or exact `0x2F` fallback packet materializer.

## Honest remaining gap

- the old seam `C2:EF65..C2:F00F` is now honestly closed through exact `C2:F113`
- the next clean follow-on owner starts at exact `C2:F114`
- the next obvious callable band is `C2:F114..C2:F24A`
