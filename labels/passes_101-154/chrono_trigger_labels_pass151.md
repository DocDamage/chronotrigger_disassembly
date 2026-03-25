# Chrono Trigger Labels — Pass 151

## Purpose

Pass 151 closes the callable/helper family that pass 150 left open at `C2:F2F3..C2:F360`, with the structural correction that the old seam end was too short. The honest closure for this family runs through exact `C2:F3CA`.

## Strong labels

### C2:F2F3..C2:F331  ct_c2_a_or_forced_refresh_change_handler_seeding_0d77_020c_0dc5_0dcc_020d_020f_0dc9_0dd0_then_fa49   [strong structural]
- Begins `PHP ; SEP #$20 ; REP #$10`.
- Tests exact byte `0D78`; when exact byte `0D78` is negative, skips the equality guard and forces the exact refresh lane.
- Otherwise compares exact incoming accumulator byte `A` against exact latch byte `0D77` and returns immediately when they already match.
- On exact refresh, mirrors exact byte `A -> 0D77 / 020C`, clears exact byte `0D78`, seeds exact fields `0DC5 = 4E84`, `0DCC = 6840`, `020D = 2EB1`, `020F = CC`, `0DC9 = 01`, and `0DD0 = 0080`.
- Runs exact helper `FA49`, then exits `PLP ; RTS`.
- Strongest safe reading: exact accumulator-byte or forced-refresh change-handler that seeds exact `020C/020D/020F` workspace plus exact `0DC5/0DCC/0DC9/0DD0`, then runs exact helper `FA49`.

### C2:F332..C2:F336  ct_c2_short_word_copy_helper_mirroring_5b_into_61   [strong structural]
- Loads exact word `5B` into exact `X`.
- Stores that exact word into exact word `61`.
- Returns immediately.
- Strongest safe reading: exact short word-copy helper mirroring exact `5B -> 61`.

### C2:F337..C2:F360  ct_c2_zero_bank_record_builder_writing_5d_and_derived_9000_pointer_into_y_from_5b   [strong structural]
- Temporarily rebinds the exact data bank to exact `00`.
- Loads exact destination record pointer `Y` from exact word `5B`.
- Writes exact bank byte `7E` into exact offsets `[Y+4]` and `[Y+7]`.
- Reenters exact 16-bit accumulator mode, writes exact word `5D -> [Y+0]`, derives exact word `61 = 9000 + ((5B & 00F0) << 3)`, and mirrors that exact word into exact `[Y+2]`.
- Returns with exact word `61` preserved.
- Strongest safe reading: exact zero-bank record builder writing exact word `5D` plus one exact derived `9000`-based pointer into the exact record rooted at exact word `5B`.

### C2:F361..C2:F363  ct_c2_short_wrapper_forcing_x_y_16_bit_then_falling_into_f364   [strong structural]
- Runs exact `REP #$10`.
- Saves flags and falls through directly into exact late entry `F364`.
- Strongest safe reading: exact short wrapper forcing exact `X/Y` 16-bit state before exact shared late entry `F364`.

### C2:F364..C2:F377  ct_c2_ff_bank_length_prefixed_block_importer_from_5b_into_7e_61   [strong structural]
- Rebinds the exact data bank to exact `FF`.
- Uses exact word `5B` as one exact FF-bank source pointer.
- Reads the exact first byte at that source as the exact transfer count seed, decrements it for exact `MVN` semantics, then advances past that count byte.
- Uses exact word `61` as the exact bank-`7E` destination pointer.
- Runs exact `MVN 7E,FF`, then exits through exact shared `PLP ; RTS` tail.
- Strongest safe reading: exact FF-bank length-prefixed block importer from exact source pointer `5B` into exact bank-`7E` destination `61`.

### C2:F378..C2:F3CA  ct_c2_coordinate_to_coordinate_multi_row_word_swap_owner_using_ed90_5b_5d_5f_60_61   [strong structural]
- Begins `PHP ; REP #$30`.
- Runs exact helper `ED90` twice to derive exact row pointers `63` and `65` from exact packed coordinates `5D` and `5B` relative to exact base word `61`.
- Derives exact horizontal loop count from exact low 5-bit lane of exact byte `5F` and exact vertical loop count from exact low 6-bit lane of exact byte `60`.
- Swaps exact 16-bit cells between exact `[63]` and exact `[65]`, advancing exact `X/Y` by two bytes per cell.
- After each exact row, advances exact words `63` and `65` by exact `0x0040` and repeats until the exact height countdown reaches zero.
- Strongest safe reading: exact coordinate-to-coordinate multi-row word-swap owner using exact `ED90`, exact packed coordinates `5B/5D`, exact extents `5F/60`, and exact row base `61`.

## Honest remaining gap

- the old seam `C2:F2F3..C2:F360` is now honestly closed through exact `C2:F3CA`
- the old seam end at exact `C2:F360` cut live exact helper/owner code in half
- the next clean follow-on owner starts at exact `C2:F3CB`
- the next obvious callable band is `C2:F3CB..C2:F421`
