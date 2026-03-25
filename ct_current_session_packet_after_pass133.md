# Current Session Packet

- Latest pass: **133**
- Source note: `notes/next_session_start_here.md`
- Extracted seam targets: **7**

## Live seam text

downstream callable refresh / packet-build seam: C2:D36C..C2:D520 broader gameplay-facing nouns: 7E:0F0F 7E:0D1F broader gameplay/system role of 7E:0D8B broader gameplay/system role of 7E:0D8C broader gameplay/system role of 7E:0D90 broader top-level family noun: C2:A886..C2:AA30

## Target packet

### C2:D36C..C2:D520

- Span: `C2:D36C .. C2:D520` (437 bytes)
- Start bytes ±8: `29 29 07 8D 8C 0D 28 60 08 E2 30 9C 5D 0D A6 79 E0`
- End bytes ±8: `82 2B D5 46 D5 8B D5 45 D6 90 D6 18 D6 C3 D6 15 D7`
- Overlapping labels:
  - none
- Nearby labels:
  - pass 133 [strong] `C2:D32C..C2:D36B` :: ct_c2_externally_callable_0d8c_refresh_owner_running_ecdb_edf6_ee7f_from_0d79_79_and_2991_07
- Xref summary:
  - no cached hot-xref targets inside span
- Note mentions:
  - `chrono_trigger_disasm_pass133.md`
  - `chrono_trigger_labels_pass133.md`

### C2:A886..C2:AA30

- Span: `C2:A886 .. C2:AA30` (427 bytes)
- Start bytes ±8: `86 30 A9 15 00 54 7E 7E 20 B2 A1 A2 EA FB 20 85 83`
- End bytes ±8: `00 8F 80 21 00 A5 01 8F 80 21 00 60 40 AA 4A AA 86`
- Overlapping labels:
  - pass 121 [strong] `C2:A886..C2:A969` :: ct_c2_two_phase_a970_driver_with_seeded_969a_stream_template_and_preseeded_5cc2_5d42_fills
  - pass 121 [strong] `C2:AA06..C2:AA18` :: ct_c2_nineteen_byte_rom_seed_template_copied_to_7e_969a_before_a970_stream_updates
  - pass 120 [strong] `C2:A970..C2:AA05` :: ct_c2_decrement_by_6_fill_and_wram_2180_stream_updater_for_5cc2_and_5d42
  - pass 120 [strong] `C2:AA19..C2:AA30` :: ct_c2_triplet_emitter_to_2180_using_a_and_00_01_with_split_negative_path
- Nearby labels:
  - pass 121 [strong] `C2:A886..C2:A969` :: ct_c2_two_phase_a970_driver_with_seeded_969a_stream_template_and_preseeded_5cc2_5d42_fills
- Xref summary:
  - no cached hot-xref targets inside span
- Note mentions:
  - `chrono_trigger_disasm_pass129.md`
  - `chrono_trigger_disasm_pass130.md`
  - `chrono_trigger_disasm_pass131.md`
  - `chrono_trigger_disasm_pass132.md`
  - `chrono_trigger_disasm_pass133.md`
  - `chrono_trigger_labels_pass129.md`

### 7E:0F0F

- ROM bytes: n/a (non-ROM-mapped address)
- Overlapping labels:
  - pass 122 [alias] `7E:0F0F` :: ct_c2_toggle_latch_byte_for_the_c12c_worker_and_c184_template_stage_family
  - pass 47 [provisional] `7E:0E80..7E:0FFF` :: ct_c1_companion_record_buffer_0x180
  - pass 47 [provisional] `7E:0E80..7E:0FFF` :: ct_c1_three_lane_marker_record_presentation_block
  - pass 46 [strong] `7E:0E80..7E:0FFF` :: ct_c1_companion_record_buffer_0x180
  - pass 46 [provisional] `7E:0E80..7E:0FFF` :: ct_c1_roster_presentation_companion_records
- Nearby labels:
  - pass 122 [alias] `7E:0F0F` :: ct_c2_toggle_latch_byte_for_the_c12c_worker_and_c184_template_stage_family
  - pass 125 [alias] `7E:0F48` :: ct_c2_continuation_selector_byte_mirrored_into_54_by_the_b48e_bridge_and_b3e6_loader
  - pass 125 [alias] `7E:0F49` :: ct_c2_nonzero_gate_byte_for_the_b365_negative_lane
  - pass 126 [alias] `7E:0F4A` :: ct_c2_signed_continuation_delta_byte_snapshotted_through_0dd9_and_adjusted_by_b742
  - pass 125 [alias] `7E:0F4C` :: ct_c2_ff_record_index_byte_for_the_b3e6_loader_family
  - pass 125 [alias] `7E:0F4D` :: ct_c2_continuation_compare_seed_byte_from_0419_plus_041a
- Xref summary:
  - no cached/live call hits
- Note mentions:
  - `chrono_trigger_disasm_pass127.md`
  - `chrono_trigger_disasm_pass128.md`
  - `chrono_trigger_disasm_pass129.md`
  - `chrono_trigger_disasm_pass130.md`
  - `chrono_trigger_disasm_pass131.md`
  - `chrono_trigger_disasm_pass132.md`

### 7E:0D1F

- ROM bytes: n/a (non-ROM-mapped address)
- Overlapping labels:
  - pass 122 [alias] `7E:0D1F` :: ct_c2_mirror_latch_byte_of_0f0f_written_by_the_c12c_worker
  - pass 50 [provisional] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 49 [unspecified] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 48 [unspecified] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 47 [unspecified] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 47 [provisional] `7E:0CC0..7E:0E08` :: ct_c1_three_lane_status_or_command_strip
- Nearby labels:
  - pass 122 [alias] `7E:0D1F` :: ct_c2_mirror_latch_byte_of_0f0f_written_by_the_c12c_worker
  - pass 121 [caution] `7E:0D24` :: ct_c2_loop_progress_word_shared_by_9daf_ramp_and_a886_a970_counted_update_driver
  - pass 120 [caution] `7E:0D24` :: ct_c2_exact_12_step_countdown_for_9daf_ramp_loop
  - pass 122 [alias] `7E:0D47` :: ct_c2_exact_0010_stage_word_seeded_before_the_fixed_c511_call_in_c12c
  - pass 119 [caution] `7E:0D4D` :: ct_c2_selector_low3bits_and_post_threshold_flag_word_for_a1ef_tail_gate
  - pass 119 [caution] `7E:0D5D` :: ct_c2_post_threshold_result_word_for_a1ef_tail_gate
- Xref summary:
  - no cached/live call hits
- Note mentions:
  - `chrono_trigger_disasm_pass127.md`
  - `chrono_trigger_disasm_pass128.md`
  - `chrono_trigger_disasm_pass129.md`
  - `chrono_trigger_disasm_pass130.md`
  - `chrono_trigger_disasm_pass131.md`
  - `chrono_trigger_disasm_pass132.md`

### 7E:0D8B

- ROM bytes: n/a (non-ROM-mapped address)
- Overlapping labels:
  - pass 125 [alias] `7E:0D8B` :: ct_c2_primary_three_lane_cyclic_state_byte_and_high3bit_block_import_selector
  - pass 50 [provisional] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 49 [unspecified] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 48 [unspecified] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 47 [unspecified] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 47 [provisional] `7E:0CC0..7E:0E08` :: ct_c1_three_lane_status_or_command_strip
- Nearby labels:
  - pass 125 [alias] `7E:0D8B` :: ct_c2_primary_three_lane_cyclic_state_byte_and_high3bit_block_import_selector
  - pass 125 [alias] `7E:0D8C` :: ct_c2_tertiary_three_lane_cyclic_state_byte_shared_by_c456_and_c12c
  - pass 125 [alias] `7E:0D90` :: ct_c2_secondary_three_lane_cyclic_state_byte_for_c456_emitter
  - pass 123 [caution] `7E:0D75` :: ct_c2_continuation_family_phase_byte_written_as_02_by_b24a_and_01_by_b31c
  - pass 121 [alias] `7E:0DAB` :: ct_c2_staged_decrement_step_word_for_9daf_ramp_and_a886_a970_update_driver
  - pass 120 [caution] `7E:0DAB` :: ct_c2_step_word_used_by_9daf_ramp_and_a970_fill_updater
- Xref summary:
  - no cached/live call hits
- Note mentions:
  - `chrono_trigger_disasm_pass127.md`
  - `chrono_trigger_disasm_pass128.md`
  - `chrono_trigger_disasm_pass129.md`
  - `chrono_trigger_disasm_pass130.md`
  - `chrono_trigger_disasm_pass131.md`
  - `chrono_trigger_disasm_pass132.md`

### 7E:0D8C

- ROM bytes: n/a (non-ROM-mapped address)
- Overlapping labels:
  - pass 125 [alias] `7E:0D8C` :: ct_c2_tertiary_three_lane_cyclic_state_byte_shared_by_c456_and_c12c
  - pass 50 [provisional] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 49 [unspecified] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 48 [unspecified] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 47 [unspecified] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 47 [provisional] `7E:0CC0..7E:0E08` :: ct_c1_three_lane_status_or_command_strip
- Nearby labels:
  - pass 125 [alias] `7E:0D8C` :: ct_c2_tertiary_three_lane_cyclic_state_byte_shared_by_c456_and_c12c
  - pass 125 [alias] `7E:0D8B` :: ct_c2_primary_three_lane_cyclic_state_byte_and_high3bit_block_import_selector
  - pass 125 [alias] `7E:0D90` :: ct_c2_secondary_three_lane_cyclic_state_byte_for_c456_emitter
  - pass 123 [caution] `7E:0D75` :: ct_c2_continuation_family_phase_byte_written_as_02_by_b24a_and_01_by_b31c
  - pass 121 [alias] `7E:0DAB` :: ct_c2_staged_decrement_step_word_for_9daf_ramp_and_a886_a970_update_driver
  - pass 120 [caution] `7E:0DAB` :: ct_c2_step_word_used_by_9daf_ramp_and_a970_fill_updater
- Xref summary:
  - no cached/live call hits
- Note mentions:
  - `chrono_trigger_labels_pass125.md`
  - `chrono_trigger_next_session_start_here_pass127.md`
  - `chrono_trigger_next_session_start_here_pass132.md`

### 7E:0D90

- ROM bytes: n/a (non-ROM-mapped address)
- Overlapping labels:
  - pass 125 [alias] `7E:0D90` :: ct_c2_secondary_three_lane_cyclic_state_byte_for_c456_emitter
  - pass 50 [provisional] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 49 [unspecified] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 48 [unspecified] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 47 [unspecified] `7E:0CC0..7E:0E08` :: ct_c1_companion_paired_byte_strip_buffer
  - pass 47 [provisional] `7E:0CC0..7E:0E08` :: ct_c1_three_lane_status_or_command_strip
- Nearby labels:
  - pass 125 [alias] `7E:0D90` :: ct_c2_secondary_three_lane_cyclic_state_byte_for_c456_emitter
  - pass 125 [alias] `7E:0D8C` :: ct_c2_tertiary_three_lane_cyclic_state_byte_shared_by_c456_and_c12c
  - pass 125 [alias] `7E:0D8B` :: ct_c2_primary_three_lane_cyclic_state_byte_and_high3bit_block_import_selector
  - pass 123 [caution] `7E:0D75` :: ct_c2_continuation_family_phase_byte_written_as_02_by_b24a_and_01_by_b31c
  - pass 121 [alias] `7E:0DAB` :: ct_c2_staged_decrement_step_word_for_9daf_ramp_and_a886_a970_update_driver
  - pass 120 [caution] `7E:0DAB` :: ct_c2_step_word_used_by_9daf_ramp_and_a970_fill_updater
- Xref summary:
  - no cached/live call hits
- Note mentions:
  - `chrono_trigger_disasm_pass121.md`
  - `chrono_trigger_labels_pass125.md`
  - `chrono_trigger_next_session_start_here_pass127.md`
  - `chrono_trigger_next_session_start_here_pass132.md`

