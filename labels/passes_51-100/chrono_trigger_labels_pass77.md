# Chrono Trigger Labels — Pass 77

## Purpose
This file records the label upgrades justified by pass 77.

Pass 76 proved that service `04` is a real local mode-dispatch family and that modes `1` and `2` both converge into the shared runner at `4833`.

Pass 77 closes the next exact seam:

- mode `0` is just `RTS`
- mode `3` is the missing high-range fixed-profile front end
- `48EC` parses a segmented CE stream into group start pointers and counts
- `4943` decodes one packed fragment batch into conditional 4-byte workspace records
- the `5D00..` output-slot stride is **8 bytes**, not the mistaken 6-byte wording from pass 76

That still stops short of a fully frozen player-facing noun, but the output family is now much less vague.

---

## Strengthened helper labels

### C1:475A..C1:475A  ct_c1_service04_mode0_noop_rts   [strong]
- Exact body is only `RTS`.
- This is the true mode-`0` target behind the `431D` service-04 dispatcher.
- Any `AE92 >= 4` fallback therefore collapses to no-op service-04 behavior.

### C1:475B..C1:4832  ct_c1_service04_mode3_load_high_range_fixed_followup_profiles_and_run_common_emit_tail   [strong structural]
- Computes `X = 7 * (AE93 - 0xBC)`.
- Loads a 7-byte profile record from `CD:5C26 + 7*(AE93 - 0xBC)` into the same working-byte family used by mode `2`: `9877 / 987A / 987B / 987E / 9881 / 9884 / 987C`.
- Runs the same shared derivation chain and falls into the common `4833` runner.
- Strongest safe reading: service-04 mode-3 high-range fixed-follow-up profile-loader front end.

### C1:48EC..C1:493F  ct_c1_service04_parse_segmented_ce_fragment_group_stream_into_a280_starts_and_a2a0_counts   [strong structural]
- Seeds `A280[0] = 9885`, clears local counters, then parses control classes from the top bits of the `CE:0000,X` stream.
- `0x00..0x1F` high-bit class ends the stream.
- Negative/high-bit tokens open new groups and seed their first counted 4-byte unit.
- `0x20`-class tokens commit a zero count to `A2A0[current_group]`.
- `0x40/0x60`-class tokens commit the accumulated 4-byte-unit count to `A2A0[current_group]`.
- Builds up to `0x10` group start pointers in `A280` and per-group counts in `A2A0`.
- Strongest safe reading: segmented CE fragment-group stream parser.

### C1:4943..C1:49FD  ct_c1_service04_decode_one_packed_fragment_batch_into_a2d3_and_a450_quad_workspace   [strong structural]
- Uses `A650` to choose the current output-row base through `CC:F7C0`.
- Uses `A652` as the current cursor into the packed `2D00..` stream.
- Splits the initial control byte into high/low nibble controls, copies the low-nibble-count compact bytes into `A2D3..`, then conditionally emits 4-byte records into the `4500..` workspace when shifted `A2D3` bytes carry out.
- Uses `CC:F820` lookup bytes while building those 4-byte records.
- Increments `A05B[current_row]` for each emitted record.
- Runs four internal subpasses per call before returning.
- Strongest safe reading: packed fragment/quad batch decoder into the service-04 working output workspace.

### C1:4833..C1:48E7  ct_c1_service04_common_output_materialization_and_emit_finalize_runner   [strong correction]
- Pass 76 already pinned this as the shared convergence tail for active service-04 modes.
- Pass 77 corrects one important detail: the `5D00..` output family is indexed by `JSR 0112`, and `0112 = ASL; ASL; ASL; RTS`, so the loop seeds **16 output slots at 8-byte stride**, not 6-byte records.
- The loop clears bytes `+0/+1`, seeds bytes `+2/+3` from the `D1:50A2 / D1:50A3` family, and marks `A07B[slot] = 1`.

---

## Strengthened RAM/state labels

### 7E:A280..7E:A29F  ct_c1_service04_ce_fragment_group_start_pointers_16_words   [strong structural]
- Seeded by `48EC`.
- Holds the parsed CE-stream start pointer for each fragment group.
- Initial entry `0` is seeded from `9885` before group parsing advances.

### 7E:A2A0..7E:A2AF  ct_c1_service04_ce_fragment_group_unit_counts_16_bytes   [strong structural]
- Written by `48EC` alongside `A280`.
- Holds the committed per-group count of 4-byte units derived from the segmented CE stream.

### 7E:A2D3..7E:A2E2  ct_c1_service04_current_packed_fragment_decode_bytes   [provisional strengthened]
- Filled by `4943` from the packed `2D00..` stream using the low-nibble count from the batch header byte.
- The bytes are shifted in-place and their carry result controls whether 4-byte records are emitted into the `4500..` workspace.

### 7E:A05B..7E:A07A  ct_c1_service04_per_row_emitted_fragment_record_counts   [provisional strengthened]
- `4943` clears `A05B[current_row]` on row start.
- It increments the same entry once for each emitted 4-byte workspace record.
- Strongest safe reading so far: per-row emitted fragment/quad record counts.

### 7E:A650  ct_c1_service04_current_fragment_output_row_index   [strong structural]
- Used by `4943` to choose a row base through `CC:F7C0`.
- Also indexes the `A05B` produced-record count family.

### 7E:A652  ct_c1_service04_current_packed_fragment_stream_cursor   [strong structural]
- The active `2D00..` cursor used by `4943`.
- Advanced repeatedly as compact fragment data and emitted-record payload bytes are consumed.

### 7E:5D00..7E:5D7F  ct_c1_service04_output_slot_records_16x8_stride   [provisional strengthened]
- Pass 77 corrects the stride math: this family is addressed at `5D00 + 8*slot`.
- The shared `4833` tail seeds bytes `+0/+1` to zero and bytes `+2/+3` from the `D1:50A2 / D1:50A3` family for sixteen slots.
- Final gameplay-facing noun of the slot record remains one notch below frozen.

### 7E:A07B..7E:A08A  ct_c1_service04_output_slot_active_flags_16_bytes   [provisional strengthened]
- The shared `4833` tail stores `1` here for each of the sixteen seeded output slots.
- Strongest safe reading so far: per-slot active/emit flags for the `5D00..` output record family.

---

## Honest caution
Even after this pass:

- I have **not** fully frozen the final player-facing noun of the emitted `4500.. -> 5D00..` object family.
- I have **not** decoded `C3:0002`, which still matters because it materializes the packed `2D00..` stream consumed by `4943`.
- I have **not** frozen the exact per-byte meanings of the 7-byte mode-2/mode-3 profile records.
- `A2D3` and `A05B` are materially tighter than before, but they still stop just short of a perfect final noun.
