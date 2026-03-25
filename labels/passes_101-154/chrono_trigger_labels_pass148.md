# Chrono Trigger Labels — Pass 148

## Purpose

Pass 148 closes the callable/helper family that pass 147 left open at `C2:ED31..C2:EE7F`, and it also closes the immediate callable spillover through exact `C2:EF64`.

## Strong labels

### C2:ED31..C2:ED58  ct_c2_ff_command_stream_dispatcher_copying_records_to_7e005b_then_indirect_jsr_via_ed59   [strong structural]
- Reads one exact command byte from an exact FF-bank stream.
- Uses exact FF-bank table `FF:BD18[command]` as the exact import-size seed for the exact `MVN 7E,FF` lane into exact scratch band `7E:005B`.
- Uses the exact command byte itself as the exact byte offset into the local exact indirect-jump table at `ED59`.
- Loops until an exact negative command terminator is encountered.
- Strongest safe reading: exact FF-bank command-stream dispatcher copying exact command records into exact scratch band `7E:005B` and then dispatching through exact table `ED59`.

### C2:ED59..C2:ED6E  ct_c2_local_11_word_command_dispatch_table_for_ed31   [strong structural]
- Exact local 11-word indirect-dispatch table consumed by exact owner `ED31`.
- Table words now pinned: `ED77`, `EF05`, `EDAA`, `EF48`, `F332`, `F364`, `F337`, `F364`, `F378`, `EDB0`, `EDB6`.
- Strongest safe reading: exact local command dispatch table for exact owner `ED31`.

### C2:ED6F..C2:ED76  ct_c2_short_ff_to_7e_record_importer_late_entry_into_005b   [strong structural]
- Begins `INX ; LDY #$005B`.
- Runs exact `MVN 7E,FF`.
- Returns immediately through exact `RTS`.
- Strongest safe reading: exact short FF-to-7E record importer late entry into exact scratch band `005B`.

### C2:ED77..C2:ED8F  ct_c2_repeated_seed_word_strip_materializer_using_61_5d_and_5b   [strong structural]
- Seeds exact word `5D` into exact destination base word `[61]`.
- Uses exact self-overlapping `MVN 7E,7E` to replicate that exact seed word forward.
- Uses exact byte `5B` as the exact strip-span control.
- Strongest safe reading: exact repeated seed-word strip materializer using exact words `61/5D` and exact span byte `5B`.

### C2:ED90..C2:EDA9  ct_c2_packed_5d_row_column_to_63_pointer_builder_relative_to_61   [strong structural]
- Uses exact packed word `5D`.
- Combines the exact low 5-bit lane of `5D` with the exact high-byte lane of `5D` scaled into exact `0x40` row units.
- Adds that exact offset to exact base word `61`.
- Stores the exact result into exact pointer word `63`.
- Strongest safe reading: exact packed row/column-to-pointer builder deriving exact `63` relative to exact base word `61`.

### C2:EDAA..C2:EDAF  ct_c2_short_wrapper_running_edb0_then_ee7f   [strong structural]
- Runs exact helper `EDB0`.
- Tail-jumps into exact owner `EE7F`.
- Strongest safe reading: exact short wrapper running exact `EDB0` and then exact `EE7F`.

### C2:EDB0..C2:EDB5  ct_c2_short_wrapper_running_edd3_then_edf6   [strong structural]
- Runs exact helper `EDD3`.
- Tail-jumps into exact owner `EDF6`.
- Strongest safe reading: exact short wrapper running exact `EDD3` and then exact `EDF6`.

### C2:EDB6..C2:EDD2  ct_c2_derived_extent_owner_running_edd3_then_ee7f_with_8a_8c_from_5f_60   [strong structural]
- Runs exact helper `EDD3`.
- Derives exact local work words `8A/8C` from exact words `5F/60`.
- Runs exact owner `EE7F`.
- Strongest safe reading: exact derived-extent owner that stages through exact `EDD3` and then exact `EE7F`.

### C2:EDD3..C2:EDF5  ct_c2_packet_or_fallback_stage_owner_deriving_0d47_0d48_then_ed90   [strong structural]
- Uses exact packet byte `005B` when it is nonnegative, otherwise falls back to exact `(0D8C & 07)`.
- Derives exact stage word `0D47 = 20 * selector`.
- Copies exact packet byte `005C -> 0D48`.
- Runs exact helper `ED90`.
- Strongest safe reading: exact packet/fallback stage owner deriving exact `0D47/0D48` and then refreshing exact pointer word `63`.

### C2:EDF6..C2:EEE0  ct_c2_row_band_builder_owner_running_ee23_ee58_ee23_from_63_5f_60_and_0d47   [strong structural]
- Mirrors exact pointer `63 -> 65`.
- Derives exact local work words `06`, `8A`, and `8C` from exact words `5F/60`.
- Seeds exact stage word `08` from exact `0D47`.
- Runs exact helper sequence `EE23 -> EE58 -> EE23`.
- Strongest safe reading: exact row-band builder owner running exact `EE23 / EE58 / EE23` from exact words `63`, `5F`, `60`, and `0D47`.

### C2:EEE1..C2:EEF4  ct_c2_local_post_adjust_copy_helper_advancing_63_then_reusing_ef2b   [strong structural]
- Decrements exact row-count word `8C`.
- Retunes exact work word `8A`.
- Advances exact pointer word `63 += 0042`.
- Reuses exact helper `EF2B`.
- Strongest safe reading: exact local post-adjust copy helper advancing exact `63` and reusing exact `EF2B`.

### C2:EEF5..C2:EF04  ct_c2_local_16_byte_template_selector_table_for_ee7f   [strong structural]
- Exact local 16-byte selector/template table consumed by exact owner `EE7F`.
- Strongest safe reading: exact local template selector table for exact `EE7F`.

### C2:EF05..C2:EF2A  ct_c2_coordinate_to_coordinate_row_band_copy_owner_using_ed90_twice_then_ef2b   [strong structural]
- Derives exact row-count word `8C` from exact low byte of `60`.
- Derives exact per-row byte-count word `8A` from exact low byte of `5F`.
- Runs exact helper `ED90` twice with different exact packed coordinate words.
- Runs exact helper `EF2B`.
- Strongest safe reading: exact coordinate-to-coordinate row-band copy owner using exact `ED90` twice and then exact `EF2B`.

### C2:EF2B..C2:EF44  ct_c2_7e_to_7e_row_band_block_copier_with_0x40_stride_using_63_65_8a_8c   [strong structural]
- Uses exact source/destination pointers `63/65`.
- Uses exact work words `8A/8C`.
- Runs exact `MVN 7E,7E`.
- Advances both exact pointers by exact `0x0040` per row.
- Strongest safe reading: exact 7E-to-7E row-band block copier with exact `0x40` stride using exact words `63/65/8A/8C`.

### C2:EF45..C2:EF64  ct_c2_ff_table_selected_front_end_computing_63_from_5d_then_entering_ef65_with_5f   [strong structural]
- Runs exact helper `ED90` to refresh exact pointer word `63`.
- Uses exact word `5B` to select one exact FF-bank pointer from exact long table `FF:C457`.
- Reuses exact pointer word `63` as the exact destination-side `X`.
- Enters exact helper `EF65` with exact parameter byte `5F`.
- Strongest safe reading: exact FF-table selected front-end computing exact `63` from exact packed word `5D` and then entering exact helper `EF65` with exact byte `5F`.

## Honest remaining gap

- the old seam `C2:ED31..C2:EE7F` is now honestly closed through exact `C2:EF64`
- the next clean follow-on owner starts at exact `C2:EF65`
- the next obvious callable band is `C2:EF65..C2:F00F`
