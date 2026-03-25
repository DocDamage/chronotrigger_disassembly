# Chrono Trigger Labels — Pass 128

## Purpose

Pass 128 closes the open continuation-family seam at `C2:BC6F..C2:BECD` and the post-substitution helper seam at `C2:C949..C2:CA66`.

## Strong labels

### C2:BC6F..C2:BCAD  ct_c2_composite_state_change_owner_rebuilding_0f00_lanes_when_0418_0419_041a_composite_changes   [strong structural]
- Exact called entry is `BC6F`; the earlier pass-127 seam start at `BC71` was two bytes late.
- Builds an exact composite byte from `0419 + 041A` in the high nibble path plus exact byte `0418`, compares it against exact cache byte `84`, updates exact cache byte `84`, and returns immediately when the exact composite did not change.
- On change, clears exact bytes `0F4A` and `0F48`, emits exact selector `FBE3 -> 8385`, mirrors exact byte `0419 + 041A -> 71`, runs exact helper `8820`, runs exact local rebuild wrapper `BCAE`, mirrors exact byte `0F4A -> 00`, and runs exact helper `BD6B`.
- Strongest safe reading: exact change-detect owner that only rebuilds the downstream continuation/export lanes when the exact `0418/0419/041A` composite state changes.

### C2:BCAE..C2:BCCC  ct_c2_shift_copy_wrapper_moving_0f00_to_0f02_then_rebuilding_9890_and_0f00_0f30   [strong structural]
- In 16-bit mode seeds exact word `0F00 = FFFF`, then copies exact `0x0016` bytes from exact block `7E:0F00` into exact block `7E:0F02`.
- Restores 8-bit A/X, then runs exact helpers `BCCD` and `BD00`.
- Strongest safe reading: exact local rebuild wrapper that first shifts the live `0F00` lane into `0F02`, then regenerates the exact `9890` list and the exact `0F00/0F30` export lanes.

### C2:BCCD..C2:BCFF  ct_c2_mask_selected_9890_builder_using_9a90_fff9bb_cc2963_and_bd65_lane_spans   [strong structural]
- Loads exact selector byte `9A90` into `X`, uses exact table `FF:F9BB[X]` as a bitmask seed, and stores the exact mask into local byte `00`.
- Uses exact byte `0418` to select one exact 16-bit span descriptor from exact local table `BD65..BD6A`.
- Walks exact table `CC:2963` from the selected base, masks each exact candidate byte with local mask `00`, and whenever the masked value is nonzero writes the exact current table index into exact byte lane `9890,Y`.
- Terminates the exact `9890` list with exact byte `FF`.
- Strongest safe reading: exact mask-selected list builder that materializes the live `9890` selector list from `9A90`, `FF:F9BB`, `CC:2963`, and the exact `BD65` span descriptors.

### C2:BD00..C2:BD3F  ct_c2_9890_expander_building_0f00_0f30_and_0f49_from_local_span_tables   [strong structural]
- Clears local byte `00`, then walks exact byte list `9890` until the exact negative terminator.
- For each exact selector byte, loads one exact byte from exact table `7F:0000,X` and one exact low/high span pair from the exact local table family at `BD40`.
- Repeatedly writes the exact current span byte into exact byte lane `0F00,Y` and the exact selector byte into exact byte lane `0F30,Y` until the exact local end byte is reached.
- When the exact expansion completes, writes exact byte `0F49 = Y`, terminates exact byte lane `0F00[Y] = FF`, and returns.
- Strongest safe reading: exact list expander that turns the exact compact `9890` selector list into the live exact `0F00/0F30` lane pair and exact count byte `0F49`.

### C2:BD40..C2:BD64  ct_c2_local_interleaved_span_byte_tables_for_the_bd00_9890_expander   [strong]
- Exact byte table consumed by `BD00` through long loads at exact addresses `BD40` and `BD41`.
- Strongest safe reading: exact interleaved local start/end span-byte tables for the `BD00` list-expansion loop.

### C2:BD65..C2:BD6A  ct_c2_three_word_lane_span_descriptor_table_for_the_bccd_9890_builder   [strong]
- Exact little-endian word entries: `0700`, `0F07`, `0F16`.
- Strongest safe reading: exact three-word local span-descriptor table selected by exact byte `0418` inside `BCCD`.

### C2:BD6B..C2:BD98  ct_c2_nine_row_0f00_export_loop_copying_selected_entries_through_bd99_into_3024_pages   [strong structural]
- Seeds exact packet base word `61 = 3024` and exact loop word `02 = 0008`.
- For each exact byte `0F00[Y]`, mirrors the exact byte into exact byte `0F4C`, then runs exact helper `BD99`.
- After each exact row, advances exact packet base `61 += 0080`, increments exact local source index byte `00`, decrements exact loop word `02`, and repeats until the loop reaches zero.
- Strongest safe reading: exact nine-row exporter that feeds selected exact `0F00` entries through `BD99` into the exact `3024` packet-page strip.

### C2:BD99..C2:BDB1  ct_c2_sign_split_0f4c_exporter_calling_bdb2_or_jumping_ef65_with_9b76   [strong structural]
- Tests exact byte `0F4C`.
- Nonnegative path runs exact helper `BDB2` and returns.
- Negative path seeds exact `Y = 9B76`, exact accumulator bank/source bytes `7E:0B`, restores flags, and jumps exact helper `EF65`.
- Strongest safe reading: exact sign-split exporter for the current exact `0F4C` lane.

### C2:BDB2..C2:BDEA  ct_c2_77xx_flag_sensitive_row_template_exporter_using_0f4c_times_0b_and_ef65   [strong structural]
- Writes exact byte `0F4C -> $4202`, exact byte `0B -> $4203`, and uses the exact multiply result at `$4216`.
- Tests exact source byte `7700,Y` for exact bits `0x40` and `0x80`, with a secondary exact `BIT 78` gate controlling exact byte `7E = 00` vs `08`.
- In 16-bit mode adds exact multiply result `$4216` to exact base word `15C4`, mirrors the result into `Y`, mirrors exact packet base word `61 -> X`, seeds exact length byte `0B`, and jumps exact helper `EF65`.
- Strongest safe reading: exact row-template exporter that chooses one exact `77xx` flag mode, derives one exact source row from `0F4C * 0B`, and exports that row through `EF65`.

### C2:BDEB..C2:BDFD  ct_c2_bit6_probe_gate_emitting_c026_through_ed31_when_0418_is_zero   [strong structural]
- Runs only when exact byte `0418 == 00`.
- Uses exact byte `0F4C` as an index into exact byte lane `7700`, and when exact bit `0x40` is set loads exact selector word `C026` and runs exact helper `ED31`.
- Otherwise returns immediately.
- Strongest safe reading: exact bit-6 probe gate for the live exact `0F4C` selector lane.

### C2:BDFE..C2:BE15  ct_c2_0f4c_change_watcher_calling_be33_when_0d78_is_clear_and_0d77_differs   [strong structural]
- Tests exact byte `0F4C` against exact latch byte `0D77`.
- When exact word/byte `0D78` is negative, returns immediately.
- When exact byte `0F4C == 0D77`, returns immediately.
- Otherwise runs exact helper `BE33` and returns.
- Strongest safe reading: exact change watcher guarding the `BE33` refresh path.

### C2:BE16..C2:BE32  ct_c2_alternate_seed_wrapper_setting_0d13_6d_0dc5_5356_0dc9_0a_then_branching_into_the_be33_common_body   [strong structural]
- Seeds exact word/byte `0D13 = 6D`, exact word `0DC5 = 5356`, and exact byte `0DC9 = 0A`.
- Loads exact accumulator as `0418 + 76` and branches into the common exact `BE33` body at the shared exact update/check path.
- Strongest safe reading: exact alternate seed wrapper for the `BE33` common change-handler body.

### C2:BE33..C2:BE78  ct_c2_0f4c_or_seeded_a_change_handler_refreshing_0d77_020c_0dcc_0f73_020d_020f_0dd0_then_fa49   [strong structural]
- Seeds exact word `0DC5 = 5344` and exact byte `0DC9 = 01` before entering the common body.
- Common body compares the exact accumulator against exact latch byte `0D77`, unless exact word/byte `0D78` is negative.
- On change, mirrors the exact accumulator into exact bytes/words `0D77` and `020C`, clears exact word/byte `0D78`, seeds exact words `0DCC = 6AA0`, `0F73 = 0F75`, `020D = 3A09`, `020F = 00CC`, `0DD0 = 0080`, and runs exact helper `FA49`.
- Strongest safe reading: exact change-handler body for the live exact `0F4C` lane or the alternate seeded-accumulator path from `BE16`.

### C2:BE79..C2:BECD  ct_c2_continuation_owner_running_bc22_ba2f_then_copying_5de0_block_and_emitting_three_selector_packets   [strong structural]
- Mirrors exact byte `0419 + 041A -> 71`, runs exact helper `8820`, then exact helper `BC22`.
- Clears exact byte `7D`, seeds exact packet base `61 = 2ECA`, runs exact helper `BA2F`, and then exact helper `821E`.
- Stores exact word `20C7 -> 5DE0`, copies exact `0x0016` bytes from exact block `5DE0 -> 5DE2`, seeds exact phase word/byte `0D75 = 0003`, and runs exact helper `BEDC`.
- Clears exact word/byte `0DBC`, then emits three exact selector packets through `8385` using exact local descriptors `BECE`, `BED5`, and exact descriptor `FC3E`.
- Strongest safe reading: exact continuation owner that reuses the `BC22/BA2F` threshold path, stages an exact local block at `5DE0`, then emits three exact selector packets.

### C2:C949..C2:C972  ct_c2_indexed_180e_step_subtractor_clearing_1811_for_each_0f04_slot   [strong structural]
- Loads exact count/index byte `0F0C -> X`.
- For each exact selector byte in exact lane `0F04,X`, moves that exact selector into `Y`, runs exact helper `F626`, subtracts exact signed step word `0D22` from exact word `180E,Y`, and clears exact byte `1811,Y`.
- Decrements exact `X` until zero, then restores state and returns.
- Strongest safe reading: exact indexed subtract/clear helper that applies the current exact signed step word `0D22` to each live exact `0F04` slot.

### C2:C973..C2:C9AD  ct_c2_two_phase_1811_marker_writer_scanning_2980_descriptors_then_0f00   [strong structural]
- First phase runs exact `X = 08 .. 00`, exact `Y = 00`, and repeatedly calls exact helper entry `C997`.
- Second phase runs exact `Y = 01`, exact `X = 0D0F`, and reuses exact helper `C997`.
- When exact byte `0F00` is nonnegative, falls through into a final exact phase with exact `Y = 0B`, exact `X = 0F00`, and the same exact helper `C997`.
- Strongest safe reading: exact two-phase marker writer that uses exact descriptor bytes from `2980` plus the live exact `0F00` selector byte to populate the exact `1811` marker lane.

### C2:C997..C2:C9AD  ct_c2_descriptor_to_1811_writer_helper_using_c22980_and_y_as_the_exact_marker_byte   [strong structural]
- Exact called entry is `C997`.
- Loads one exact descriptor byte from exact table `C2:2980,X`; when that exact descriptor is negative, returns immediately.
- Otherwise widens to 16-bit A/X, keeps only the exact low byte, swaps it high with `XBA`, shifts right twice, uses the exact result as `X`, restores 8-bit A, and writes the exact incoming `Y` marker byte into exact lane `1811,X`.
- Strongest safe reading: exact helper that maps one exact descriptor byte into one exact `1811` slot and writes the exact current marker byte `Y` there.

### C2:C9AE..C2:C9E4  ct_c2_selector_recentering_helper_adjusting_54_by_low2_of_5a_or_93xx_lookup   [strong structural]
- When exact low 2 bits of exact control byte `5A` are nonzero, conditionally adjusts exact selector byte `54` by `+03` or `-03` using exact bytes `0F0B/0F0C` as gates.
- Otherwise runs exact helper `EA27` and then uses exact local lookup bytes from `9382/9383`, gated by exact control bit `5A.bit3`, to derive the exact low nibble stored back to exact selector byte `54`.
- Strongest safe reading: exact selector recentering helper for the post-substitution family.

### C2:C9E5..C2:CA61  ct_c2_dispatch_rooted_import_owner_copying_cc64_cbb4_9480_blocks_then_running_cd2b_ccdb_f643_cc4f_86dd   [strong structural]
- Seeds exact byte `C9 = 03`, clears exact accumulator through `TDC`, derives exact dispatch index `X = (0D36 & 02)`, runs exact helper `F588`, and then performs exact `JSR ($CA63,X)`.
- Copies exact block `FF:CC64 -> 7E:9540` (`0x0010` bytes), exact block `FF:CBB4 -> 7E:94C0` (`0x0008` bytes), and exact block `7E:9480 -> 7E:9500` (`0x0020` bytes).
- Runs exact helpers `F5A7`, `A0E7`, `CD2B`, `821E`, `CCDB`, `821E`, seeds exact word/byte `0D75 = 0002`, then runs exact helpers `F643`, `CC4F`, and `86DD`.
- Final phase increments exact byte `0D15`, seeds exact byte/word `0D13 = 01`, and emits exact selector chain `FBE3 -> FBFF -> FC37 -> 8385`.
- Strongest safe reading: exact dispatch-rooted import/setup owner for the downstream post-substitution packet family.

### C2:CA63..C2:CA66  ct_c2_two_word_local_dispatch_table_ca67_cae0_for_the_c9e5_import_owner   [strong]
- Exact little-endian word entries: `CA67`, `CAE0`.
- Strongest safe reading: exact two-word local dispatch root for the `C9E5` import/setup owner.

## Alias / wrapper / caution labels

## Honest remaining gap

- the continuation-family seam is now substantially tighter, but exact local descriptor/data bytes after the new `BE79` owner still remain open, especially `C2:BECE..C2:BEE5`
- the post-substitution family now reaches its exact `CA63` dispatch root, but the two downstream exact dispatch targets remain open, especially `C2:CA67..C2:CC0D`
- broader gameplay/system nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B/0D8C/0D90`
- the broader top-level family noun for `C2:A886..AA30` is still not tight enough
