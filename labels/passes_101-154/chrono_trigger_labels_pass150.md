# Chrono Trigger Labels — Pass 150

## Purpose

Pass 150 closes the callable/helper family that pass 149 left open at `C2:F114..C2:F24A`, with the structural correction that the old seam end was too short. The honest closure for this family runs through exact `C2:F2F2`.

## Strong labels

### C2:F114..C2:F13E  ct_c2_db_y_packed_bitfield_to_bcd_front_end_owner_deriving_8e_8f_92_93_then_materializing_to_7e_x   [strong structural]
- Rebinds the exact data bank from the exact accumulator high byte.
- Mirrors exact destination pointer `X -> 90`.
- Uses the exact accumulator low byte to seed exact work bytes `92` and `93`.
- Runs exact helper `F13F`, then exact helper `F1DA`.
- Strongest safe reading: exact `DB:[Y]` packed-bitfield-to-BCD front-end owner deriving exact `8E/8F/92/93` and then materializing exact tile pairs into exact bank-`7E` destination `[X]`.

### C2:F13F..C2:F177  ct_c2_db_y_packed_bitfield_to_bcd_accumulator_helper_using_f178_table_and_8a_8c   [strong structural]
- Clears exact work words `8A` and `8C`.
- Reads one exact source byte from exact `DB:[Y]` on each outer pass.
- Walks exact 8 bit lanes per exact source byte.
- Under exact set-bit lanes, adds one exact packed-BCD long from exact table `F178` into exact work words `8A/8C`.
- Strongest safe reading: exact packed-bitfield-to-BCD accumulator helper using exact table `F178` and exact work words `8A/8C`.

### C2:F178..C2:F1D7  ct_c2_local_27_long_packed_bcd_powers_of_two_table_for_f13f   [strong structural]
- Exact local packed-BCD powers-of-two table consumed by exact helper `F13F`.
- Exact entries begin `00000001`, `00000002`, `00000004`, `00000008`, `00000016`, `00000032`, `00000064`, `00000128`.
- Strongest safe reading: exact local 27-long packed-BCD powers-of-two table for exact helper `F13F`.

### C2:F1DA..C2:F20A  ct_c2_bank_7e_bcd_nibble_decode_materialize_helper_using_8a_8e_8f_and_f20b   [strong structural]
- Rebinds the exact data bank to exact `7E`.
- Seeds exact destination pointer `Y` from exact word `90`.
- Uses exact selector byte `8E` to derive exact starting byte index and one exact optional-high-nibble-first lane.
- Routes exact packed nibbles from exact work bytes `8A+X` through exact helper `F20B`.
- Strongest safe reading: exact bank-`7E` BCD nibble-decode/materialize helper using exact `8A/8E/8F` and exact nibble writer `F20B`.

### C2:F20B..C2:F226  ct_c2_nibble_blank_flag_tile_pair_writer_using_8f_d4_and_7e   [strong structural]
- Masks one exact incoming nibble down to exact `0x0F`.
- Exact zero nibble plus exact negative exact flag byte `8F` emits exact blank/sentinel byte `FF`.
- Otherwise clears exact flag byte `8F`, adds exact tile-base constant `0xD4`, and writes one exact tile pair into exact destination `[Y]`.
- Strongest safe reading: exact nibble/blank-flag tile-pair writer using exact `8F`, exact tile-base `0xD4`, and exact paired high byte `7E`.

### C2:F227..C2:F24B  ct_c2_sibling_fixed_value_writer_owner_loading_8a_8c_from_y_then_materializing_via_f24c   [strong structural]
- Rebinds the exact data bank from the exact accumulator high byte.
- Mirrors exact destination pointer `X -> 90`.
- Loads exact words `[Y] -> 8A` and `[Y+2] -> 8C`.
- Rebinds the exact data bank to exact `7E` and runs exact helper `F24C`.
- Strongest safe reading: exact sibling fixed-value writer owner loading exact `8A/8C` from exact `[Y]` and then materializing exact tile pairs through exact helper `F24C`.

### C2:F24C..C2:F268  ct_c2_fixed_width_bank_7e_nibble_tile_materializer_helper_using_8e_and_f269   [strong structural]
- Uses exact selector byte `8E` to derive exact starting byte index and one exact optional-high-nibble-first lane.
- Reads exact packed nibbles from exact work bytes `8A+X`.
- Routes each exact nibble through exact helper `F269`.
- Strongest safe reading: exact fixed-width bank-`7E` nibble/tile materializer helper using exact `8E` and exact nibble writer `F269`.

### C2:F269..C2:F27C  ct_c2_local_nibble_to_tile_pair_writer_helper_using_f27d   [strong structural]
- Masks one exact incoming nibble down to exact `0x0F`.
- Uses that exact nibble as one exact index into exact local table `F27D`.
- Writes one exact tile pair into exact destination `[Y]`.
- Strongest safe reading: exact local nibble-to-tile-pair writer helper using exact table `F27D`.

### C2:F27D..C2:F28C  ct_c2_local_16_byte_nibble_tile_table_for_f269   [strong structural]
- Exact bytes now pinned: `73 74 75 76 77 78 79 7A 7B 7C F1 F2 36 7D 38 34`.
- Strongest safe reading: exact local 16-byte nibble/tile table for exact helper `F269`.

### C2:F28D..C2:F2CB  ct_c2_two_field_formatter_owner_deriving_22_23_then_rendering_twice_via_f114_with_separator   [strong structural]
- Seeds exact scratch bytes `22 = 0x63` and `23 = 0x3B`.
- Under the exact zero override lane, runs exact helper `F2CC` twice to derive exact bytes `23` and `22` from exact decimal-byte pairs rooted at exact `Y`.
- Runs exact helper `F114` twice with exact accumulator word `0x7E91` and exact bank-`7E` scratch sources `0x0022` and `0x0023`.
- Inserts one exact separator tile pair formed from exact byte `7D` and exact low byte `0x2D` between those two exact renders.
- Strongest safe reading: exact two-field formatter owner deriving exact scratch bytes `22/23`, rendering them through exact `F114`, and inserting one exact separator tile pair.

### C2:F2CC..C2:F2DB  ct_c2_two_decimal_byte_to_binary_helper_combining_y_y_plus_1_into_a   [strong structural]
- Reads exact byte `[Y+1]`.
- Builds one exact `*10` product through exact shift/add mechanics.
- Adds exact byte `[Y]`.
- Advances exact `Y += 2`.
- Strongest safe reading: exact two-decimal-byte-to-binary helper combining exact decimal-byte pair `[Y]/[Y+1]` into one exact accumulator byte.

### C2:F2DC..C2:F2E1  ct_c2_indexed_local_wrapper_selecting_7d00_pointer_then_tail_jumping_into_ef65   [strong structural]
- Runs exact helper `F2E2`.
- Tail-jumps directly into exact script front-end `EF65`.
- Strongest safe reading: exact indexed local wrapper selecting one exact `7D00`-table pointer and then tail-jumping into exact `EF65`.

### C2:F2E2..C2:F2F2  ct_c2_7d00_table_selector_helper_returning_y_pointer_and_constant_cc0b   [strong structural]
- Masks one exact incoming selector down to exact `0x00FF`, doubles it, and uses that exact offset into exact table `7D00`.
- Loads one exact 16-bit pointer from exact `7D00+2*A` into exact `Y`.
- Seeds the exact accumulator with exact constant word `0xCC0B`.
- Strongest safe reading: exact `7D00`-table selector helper returning one exact `Y` pointer plus exact constant word `0xCC0B`.

## Honest remaining gap

- the old seam `C2:F114..C2:F24A` is now honestly closed through exact `C2:F2F2`
- the next clean follow-on owner starts at exact `C2:F2F3`
- the next obvious callable band is `C2:F2F3..C2:F360`
