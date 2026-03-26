# Chrono Trigger Labels — Pass 166

## Strong labels
- `C3:0A90..C3:0AFE`  `ct_c3_nmi_gated_input_display_blackout_check_with_alternating_7e377a_service_dispatch`
- `C3:0AFF..C3:0B02`  `ct_c3_stream_interpreter_jsr_rtl_veneer`
- `C3:0B03..C3:0C91`  `ct_c3_stream_bytecode_interpreter_updating_0920_0940_and_dispatching_apu_command_words`
- `C3:0C92..C3:0CB0`  `ct_c3_nibble_slot_update_helper_with_pointer_advance_path`
- `C3:0CB1..C3:0CB7`  `ct_c3_stream_word_fetch_helper_advancing_20_and_caching_fetched_word`
- `C3:0CB8..C3:0CCC`  `ct_c3_first_free_slot_clear_helper_for_table_0920`
- `C3:0CCD..C3:0CE1`  `ct_c3_first_free_slot_clear_helper_for_table_0940`
- `C3:0CE2..C3:0CF7`  `ct_c3_first_free_slot_write_helper_for_table_0920`
- `C3:0CF8..C3:0D0C`  `ct_c3_first_free_slot_write_helper_for_table_0940`
- `C3:0D0D..C3:0D5B`  `ct_c3_wram_data_quad_writer_to_0700_with_duplicated_sample_bytes_and_shift_decay_update`
- `C3:0D5C..C3:0DBB`  `ct_c3_wram_data_quad_writer_variant_with_clamped_first_coordinate_and_rotate_decay_update`
- `C3:0DBC..C3:0DF1`  `ct_c3_7e_pointer_quad_writer_to_0700_with_shift_update_through_13`
- `C3:0DF2..C3:0E27`  `ct_c3_7e_pointer_quad_writer_to_0700_with_rotate_update_through_13`
- `C3:0E2A..C3:0E37`  `ct_c3_increment_compare_tail_helper_looping_until_14_falls_below_00f4`

## Notes
- exact `0CB1..0CB7` stays separate because exact `C3:48FD` calls into it directly
- exact `0B03..0C91` is one owner with an internal exact jump-table dispatch rooted at `0B74`
- next live downstream seam is exact `C3:0EFA..C3:10B6`
