# Chrono Trigger Labels — Pass 125

## Purpose

Pass 125 closes the exact helper chain under the `C2:C2FF` owner and freezes the next continuation-family bridge after the pass-124 `FF`-record loader.

## Strong labels

### C2:B48E..C2:B4DA  ct_c2_0d1d_gated_continuation_bridge_owner_with_bit6_prep_lane_and_bit7_jump_into_b4db   [strong structural]
- Runs exact helpers `E984` and `B823`, then tests exact status byte `0D1D`.
- Clear `0D1D.bits7/6` path returns immediately.
- Exact bit-6 path reruns exact helper `EAC2`, mirrors exact byte `0F48 -> 54`, decrements exact byte `68`, reruns exact helper `F566`, seeds exact compare byte `71 = 0419 + 041A`, reruns exact settlement/search service `8820`, writes exact byte `0D75 = 02`, increments exact byte `D0`, runs exact helper `8255` with `A = 40`, shifts exact `0x0016` bytes `5DE0 -> 5DE2`, then exits through exact selectors `FBE3 -> 8385` and `FC3E -> 8385`.
- Exact bit-7 path jumps into the downstream exact lane at `B4DB`.
- Strongest safe reading: exact `0D1D`-gated continuation bridge owner choosing an immediate return, a fixed bit-6 prep lane, or the downstream exact bit-7 lane at `B4DB`.

### C2:B4DB..C2:B518  ct_c2_0dbc_gated_table_and_threshold_lane_using_b519_table_then_subtracting_0f4f_before_be79   [strong structural]
- Exits through exact helper `EACC` when exact byte `0DBC == 0`.
- Otherwise writes exact byte `19D1 = 90`, selects exact byte `19E1 = B519[19C0]`, runs exact helpers `822B` and `8F55`, then clears exact byte `19D1`.
- Seeds exact compare byte `71 = 0F4D`, reruns exact settlement/search service `8820`, subtracts exact byte `0F4F` from exact slot byte `0007,X`, stores the result back, and exits through exact jump `BE79`.
- Strongest safe reading: exact `0DBC`-gated downstream table/threshold lane using a local selector byte table, exact compare seed `0F4D`, exact subtract/result byte `0F4F`, and fixed exact jump `BE79`.

### C2:B519..C2:B520  ct_c2_eight_byte_local_selector_table_03_05_04_00_03_06_04_08_for_b4db   [strong]
- Exact bytes: `03 05 04 00 03 06 04 08`.
- Consumed directly by `B4DB` as `B519 + 19C0`.
- The final exact byte `08` overlaps the first opcode byte at `B520`.
- Strongest safe reading: exact eight-byte local selector table for the `B4DB` continuation lane.

### C2:B520..C2:B567  ct_c2_low2bit_steered_0418_adjuster_and_continuation_dispatcher_around_ea53_b568_bc6f_b6ae_be16   [strong structural]
- In 8-bit mode, loads exact byte `0418` into `X`.
- When exact `5A.low2 != 0`, exact bit `0` chooses signed step `-1` or `+1`, then clamps exact byte `0418` into range `0..2`.
- Runs exact helper `EA53`, clears exact byte `0D18`, conditionally enters exact helper `B568`, seeds exact byte `0419 = 54 - 0B`, and runs exact helper chain `BC6F -> B6AE -> BE16`.
- Finishes through exact selector `FBE3 -> 8385` and exact `PLP ; RTS`.
- Strongest safe reading: exact low-2-bit-steered `0418` adjuster and continuation dispatcher around `EA53`, optional helper `B568`, and the fixed `BC6F/B6AE/BE16` tail chain.

### C2:B568..C2:B5C7  ct_c2_bit2_gated_041a_bidirectional_adjuster_choosing_one_of_two_preset_b5c8_builds   [strong structural]
- Tests exact control bit `5A.bit2`.
- Clear path decrements exact byte `041A`; rejects when negative; then seeds exact values `22 = 0003`, `26 = 2605`, `61 = 364A`, `0D22 = FFFC`, and `24 = 211F` before running exact helper `B5C8`.
- Set path rejects when exact byte `041A + 03 >= 85`; then increments exact byte `041A`, seeds exact values `22 = 0004`, `26 = 2005`, `61 = 3ACA`, `0D22 = 0004`, and `24 = 20EF`, then runs exact helper `B5C8`.
- Strongest safe reading: exact bit-2-gated bidirectional `041A` adjuster that chooses one of two presetized build lanes rooted at `B5C8`.

### C2:B5C8..C2:B6A5  ct_c2_twelve_step_mirrored_5d44_5dc4_builder_with_bafc_ba2f_front_end_ef05_refill_and_three_row_tail_emit   [strong structural]
- Writes exact byte `0D13 = 6B`, seeds exact compare byte `71 = 0419 + 041A`, reruns exact settlement/search service `8820`, runs exact helper `BAFC`, clears exact word `9890`, and runs exact compare gate `BA2F`.
- Seeds exact `EF05` parameter block from exact values `61 = 2E00`, `5B = 0205`, `5D = 26`, and `5F = 120A`, then runs exact helper `EF05` and exact selector `FBEA -> 8385`.
- Clears exact word `0DAB`, seeds exact loop word `0D24 = 000C`, and enters an exact twelve-step loop updating exact words `0D30/0DAB/24`, mirroring exact carry through exact word `0D95`, and writing exact word `24` into mirrored lanes `5D44,X` and `5DC4,X`.
- After each exact strip build, dispatches exact selector `FC3E -> 8385`; if exact loop word `0D24` remains nonzero, reruns exact helper `821E` and continues.
- Final phase flips exact word `5B` with `EOR #0600`, reruns exact helper `EF05`, writes exact word `21FF` to `5D44`, shifts exact bytes `5D44 -> 5D46`, copies exact bytes `5D44 -> 5DC4`, dispatches exact selector `FC3E -> 8385`, clears exact word `0D30`, reruns exact helper `F566`, then emits an exact three-row tail through exact helper `BAFC`.
- Finishes by writing exact byte `0D13 = 6D`, decrementing exact byte `0D18`, and returning.
- Strongest safe reading: exact twelve-step mirrored `5D44/5DC4` builder with `BAFC/BA2F` front-end, `EF05` refill phase, and exact three-row tail emission.

### C2:B6AE..C2:B6D2  ct_c2_0418_indexed_table_exporter_using_base_2ee4_and_fixed_ecac_targets_150a_1102   [strong structural]
- Seeds exact source base word `61 = 2EE4`.
- Calls exact helper `ECAC` with exact target word `150A`.
- Uses exact byte `0418` to compute an exact stride of `8 * 0418`, adds that stride into exact base word `61`, then calls exact helper `ECAC` again with exact target word `1102`.
- Strongest safe reading: exact `0418`-indexed table exporter using base `2EE4` and fixed `ECAC` targets `150A` and `1102`.

### C2:C43A..C2:C455  ct_c2_ten_byte_mirror_from_0d86_to_0f09_with_tail_clears_of_0f0d_0f0e_0f0f   [strong]
- In 16-bit mode, copies exact `0x000A` bytes from exact source block `0D86..0D8F` into exact mirror block `0F09..0F12` with same-bank `MVN`.
- Returns to 8-bit mode and clears exact bytes `0F0D`, `0F0E`, and `0F0F`.
- Strongest safe reading: exact ten-byte mirror from `0D86` into `0F09`, with fixed tail clears of `0F0D/0F0E/0F0F`.

### C2:C456..C2:C494  ct_c2_three_lane_low3bit_table_emitter_from_0d8b_0d90_0d8c_via_bases_2ea6_2f66_2fe6   [strong structural]
- Builds three exact table lanes in sequence.
- Lane 1 uses exact base word `2EA6` and exact state byte `0D8B`.
- Lane 2 uses exact base word `2F66` and exact state byte `0D90`.
- Lane 3 uses exact base word `2FE6` and exact state byte `0D8C`.
- Final exact lane computes `61 += 2 * (state & 07)` and runs exact helper `ECAC` with exact targets `0C08` and `0001`.
- Strongest safe reading: exact three-lane low-3-bit table emitter keyed by exact bytes `0D8B/0D90/0D8C` and base tables `2EA6/2F66/2FE6`.

### C2:C495..C2:C4F8  ct_c2_0417_indexed_window_seed_and_0dce_0dcf_loader_using_ff_d562_and_local_tables_then_f943   [strong structural]
- Uses exact byte `0417` as the controlling index.
- In 16-bit mode, loads one exact word from `FF:D562 + 2*0417`, writes that exact word to `3446`, then writes the next three consecutive exact words to `3448`, `3486`, and `3488`.
- Returns to 8-bit mode, mirrors exact byte `0417` into exact byte `0DCE`, then uses exact local tables `C4F9` and `C505` to build exact byte `0DCF` from exact source block `0D86..`.
- Finishes through exact helper `F943`.
- Strongest safe reading: exact `0417`-indexed window seed and `0DCE/0DCF` loader using `FF:D562` and local byte tables before the fixed `F943` tail.

### C2:C4F9..C2:C504  ct_c2_twelve_byte_local_offset_table_for_c495_0d86_source_selection   [strong]
- Exact bytes: `00 03 02 07 08 0B 06 04 01 09 05 0A`.
- Consumed directly by `C495` as the exact byte offset selector into exact source block `0D86..`.
- Strongest safe reading: exact twelve-byte local offset table for the `C495` source-byte selection step.

### C2:C505..C2:C510  ct_c2_twelve_byte_local_addend_table_for_c495_0dcf_builder   [strong]
- Exact bytes: `28 18 0C 1C 0C 1E 0E 1F 16 1A 20 2A`.
- Consumed directly by `C495` as the exact additive byte table before storing the final result into exact byte `0DCF`.
- Strongest safe reading: exact twelve-byte local addend table for the `C495` `0DCF` builder.

### C2:C511..C2:C548  ct_c2_0d8b_high3bit_0280_stride_ff_9e10_block_importer_into_7e_8800_then_962e_selector_c548_and_ed08   [strong structural]
- Writes exact word `9890 = 3DC0`.
- Uses exact high three bits of exact word lane `0D8B & 0700` to compute an exact source base of `FF:9E10 + 0x0280 * index`.
- Copies exact `0x0281` bytes from that exact `FF` source block into exact WRAM destination `7E:8800`.
- Runs exact helper `962E` with exact `X = 8800` and exact `Y = 0014`.
- Dispatches exact selector/data packet `C548 -> 8385` and then runs exact helper `ED08`.
- Strongest safe reading: exact `0D8B.high3bit` block importer from `FF:9E10` into `7E:8800`, followed by the fixed `962E`, `C548`, and `ED08` tail chain.

### C2:C548..C2:C54E  ct_c2_seven_byte_local_selector_packet_for_c511   [strong]
- Exact bytes: `C0 3D 00 88 7E 80 02`.
- Consumed directly by `C511` through exact selector call `LDX #C548 ; JSR 8385`.
- Strongest safe reading: exact seven-byte local selector/data packet for the `C511` importer tail.

### C2:C54F..C2:C554  ct_c2_c555_then_c57a_wrapper   [alias wrapper]
- Exact body: `JSR C555 ; JMP C57A`.
- Strongest safe reading: exact wrapper that seeds exact `2993` staging through `C555` and then immediately enters the downstream exact descriptor writer at `C57A`.

### C2:C555..C2:C579  ct_c2_2993_staging_seed_from_rom_fca9_with_optional_live_0408_override_gated_by_0d87   [strong structural]
- In 16-bit mode, copies exact `0x0009` bytes from exact ROM template `C2:FCA9` into exact WRAM staging block `2993`.
- When exact word `0D87 != 0`, overwrites the same exact `0x0009` bytes at `2993` with live bytes from exact source block `0408`.
- Returns through exact `PLP ; RTS`.
- Strongest safe reading: exact `2993` staging seed from ROM template `FCA9`, with an optional live `0408` override gated by exact word `0D87`.

### C2:C57A..C2:C5A6  ct_c2_six_entry_2993_descriptor_writer_using_c5a7_destinations_c5b3_lookup_and_ff_fill_words   [strong structural]
- Runs an exact six-entry loop for exact indices `0 .. 5`.
- Uses exact local word table `C5A7 + 2*index` to choose one exact destination offset.
- Loads one exact staging byte from exact block `2993 + index`, converts that byte through exact helper `C5B3`, and writes the returned exact word to `2E00 + destination`.
- Then writes exact fill word `00FF` to `2E02 + destination` and `2E04 + destination`.
- Strongest safe reading: exact six-entry descriptor writer that consumes staged bytes from `2993`, uses exact destination table `C5A7`, converts each byte through `C5B3`, and fills the trailing two words with exact `00FF`.

### C2:C5A7..C2:C5B2  ct_c2_six_word_destination_table_0374_03f4_0474_04f4_0574_05f4_for_c57a   [strong]
- Exact little-endian words: `0374 03F4 0474 04F4 0574 05F4`.
- Consumed directly by `C57A` as the exact destination-offset table.
- Strongest safe reading: exact six-word destination table for the `C57A` descriptor writer.

### C2:C5B3..C2:C5C6  ct_c2_highest_set_bit_word_lookup_helper_using_ff_d554   [strong]
- In 8-bit mode, seeds exact `X = FFFE` and exact carry `= 1`.
- Repeatedly advances exact `X` by `2` and rotates exact byte `A` left until the carry becomes set.
- Returns to 16-bit mode, loads one exact word from `FF:D554 + X`, and returns through exact `PLP ; RTS`.
- Strongest safe reading: exact highest-set-bit word lookup helper using exact table `FF:D554`.

## Alias / wrapper / caution labels

### 7E:0D8B  ct_c2_primary_three_lane_cyclic_state_byte_and_high3bit_block_import_selector   [caution strengthened]
- `C456..C494` uses its exact low three bits to select one of the exact `2EA6` lane entries.
- `C511..C548` uses its exact high three bits to choose one exact `0x0280`-stride block from `FF:9E10`.
- Strongest safe reading: exact primary three-lane cyclic state byte whose low bits feed the local table emitter and whose high bits select the imported `FF:9E10` block.

### 7E:0D8C  ct_c2_tertiary_three_lane_cyclic_state_byte_shared_by_c456_and_c12c   [caution strengthened]
- `C456..C494` uses its exact low three bits for the third exact local table-emission lane.
- `C12C..C163` already proved it is the exact `X` target for the shared low-3-bit cyclic adjust helper at `C164`.
- Strongest safe reading: exact tertiary three-lane cyclic state byte shared by the `C456` emitter and the `C12C/C164` worker family.

### 7E:0D90  ct_c2_secondary_three_lane_cyclic_state_byte_for_c456_emitter   [caution strengthened]
- `C456..C494` uses its exact low three bits for the second exact local table-emission lane rooted at exact base `2F66`.
- Strongest safe reading: exact secondary three-lane cyclic state byte for the `C456` emitter family.

### 7E:0F48  ct_c2_continuation_selector_byte_mirrored_into_54_by_the_b48e_bridge_and_b3e6_loader   [caution strengthened]
- `B48E..B4DA` mirrors it into exact selector byte `54` in the exact bit-6 bridge lane.
- `B3E6..B48D` already mirrors it into exact selector byte `54` before the `FF`-record loader checks.
- Strongest safe reading: exact continuation selector byte mirrored into `54` by the bridge/loader family.

### 7E:0F49  ct_c2_nonzero_gate_byte_for_the_b365_negative_lane   [caution strengthened]
- `B365..B3AD` checks it before choosing between exact helper `EACC` and the exact `EAC2 -> 0F48 -> B9E1/BB50` lane.
- Strongest safe reading: exact nonzero gate byte for the `B365` negative-lane continuation path.

### 7E:0F4C  ct_c2_ff_record_index_byte_for_the_b3e6_loader_family   [caution strengthened]
- `B3AE..B3E5` clears it on the overflow path before running exact helper `BA4F`.
- `B3E6..B48D` multiplies it by exact stride `0x0C` to choose one exact `FF` record.
- Strongest safe reading: exact `FF`-record continuation index byte for the `B3E6` loader family.

### 7E:0F4D  ct_c2_continuation_compare_seed_byte_from_0419_plus_041a   [caution strengthened]
- `B3E6..B48D` seeds it as exact byte `0419 + 041A`, mirrors it into exact compare byte `71`, and reuses it in the downstream exact threshold lane at `B4DB`.
- Strongest safe reading: exact continuation compare-seed byte built from `0419 + 041A`.

### 7E:0F4F  ct_c2_threshold_result_byte_from_bc22_subtracted_by_b4db_before_be79   [caution strengthened]
- `B3E6..B48D` stores the exact `BC22` result here.
- `B4DB..B518` subtracts it from exact byte lane `0007,X` immediately before the fixed `BE79` tail.
- Strongest safe reading: exact threshold/result byte produced by `BC22` and consumed by the downstream `B4DB` lane.

## Honest remaining gap

- `C2:B6D3..C2:BA2E` is now the next real continuation-family owner seam after the newly closed bridge and builder lane.
- `C2:C5C7..C2:C67A` is now the next live post-substitution / descriptor-normalization seam after the newly closed `C57A/C5B3` family.
- stronger gameplay-facing nouns are still open for `0F0F/0D1F`, the broader gameplay/system role of `0D8B/0D8C/0D90`, and the broader top-level family noun for `C2:A886..AA30`.
