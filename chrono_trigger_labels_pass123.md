# Chrono Trigger Labels — Pass 123

## Purpose

Pass 123 closes the exact continuation lane behind `B10D/B17F` and the exact helper family rooted at `C20F` that pass 122 only carried as a called finalizer.

## Strong labels

### C2:B17F..C2:B1F7  ct_c2_signed_0dbd_tail_worker_seeding_0dbf_then_looping_821e_e984_b83e_until_bit6_exit_with_5080_zero_fill   [strong structural]
- Seeds exact tail byte `0DBF` from the sign bit of `0DBD`: negative keeps exact value `B2`, non-negative forces exact value `8A`.
- Seeds exact byte `54 = 0C`, then mirrors that same exact byte into `0D9C`, `0DBB`, and `0D9A`.
- Runs exact setup helper `AF42`.
- If `0DBD.bit3 != 0`, runs exact helper `8AD5`.
- Then loops exact helpers `821E`, `E984`, and `B83E`.
- After each loop body, tests exact status byte `0D1D`.
- If `0D1D.bit6 == 0` and `0D1D.bit7 == 0`, repeats the loop immediately.
- If `0D1D.bit6 == 0` and `0D1D.bit7 != 0`, checks exact probe byte `0DBC`: zero runs exact helper `EACC` before repeating, nonzero runs exact helpers `8F55` and `B31C` before repeating.
- Exit only occurs when `0D1D.bit6 != 0`; on that exit it runs exact helper `EAC2`, loads exact byte `54 = 0415`, clears exact bit `0x04` from `0D13`, clears exact byte `0D9A`, runs exact helper `F566`, runs exact helper `8255` with `A = 40`, then zero-fills exact WRAM window `7E:5080..7E:547F` via same-bank propagating `MVN`, and exits through exact selector `FBFF -> 8385`.
- Strongest safe reading: exact signed-`0DBD` continuation tail worker that seeds `0DBF`, loops the `821E/E984/B83E` body under `0D1D` status bits, and finishes with an exact `5080..547F` zero-fill on the bit6 exit.

### C2:B1F8..C2:B1FF  ct_c2_wrapper_seeding_exact_mode_ca_into_0dbd_then_tail_jumping_into_b18b_common_body   [alias wrapper]
- Exact body: `LDA #CA ; STA 0DBD ; JMP B18B`.
- Strongest safe reading: exact wrapper that forces continuation mode `CA` and reuses the common body starting at `B18B`.

### C2:B200..C2:B249  ct_c2_04c9_driven_mode_loader_and_status_gated_loop_using_b24a_b2a7_and_b31c   [strong structural]
- Reads exact selector byte `04C9`.
- Seeds exact mode byte `0DBD` as:
- `01` when `04C9 == CD`
- `06` when `04C9 == CE`
- `02` otherwise
- Then seeds exact byte `54 = 0C`, mirrors it into exact bytes `0D9C`, `0DBB`, and `0D9A`, and runs exact setup helper `AF42`.
- Loops exact helpers `821E`, `E984`, and exact local helper `B24A`.
- After each loop body, tests exact status byte `0D1D`.
- If `0D1D.bit6 == 0` and `0D1D.bit7 == 0`, repeats the loop immediately.
- If `0D1D.bit6 == 0` and `0D1D.bit7 != 0`, checks exact probe byte `0DBC`: zero runs exact helper `EACC` before repeating, nonzero runs exact helpers `B2A7` and `B31C` before repeating.
- When `0D1D.bit6 != 0`, exits through the already-frozen shared tail at `B1C7`.
- Strongest safe reading: exact `04C9`-driven continuation-family loader that selects one of three small `0DBD` modes, then runs the same status-gated loop pattern with `B24A`, `B2A7`, and `B31C`.

### C2:B24A..C2:B274  ct_c2_54_minus_0dbb_span_clamp_helper_with_5a_bit3_override_then_b275_probe_and_0d75_eq_02   [strong]
- Computes exact byte delta `54 - 0DBB`.
- If that exact delta is below exact limit byte `73`, keeps `54` unchanged.
- Otherwise uses exact `5A.bit3` to choose the replacement:
- when set, forces `54 = 0DBB`
- when clear, forces `54 = (73 - 1) + 0DBB`
- Then runs exact helper `B275`.
- On return, writes exact phase byte `0D75 = 02`.
- Strongest safe reading: exact span-clamp helper for the continuation lane, with a `5A.bit3` override and fixed post-probe phase write `0D75 = 02`.

### C2:B275..C2:B2A6  ct_c2_delta_probe_against_0dbe_with_8820_refresh_and_optional_ffcf_threshold_compare_setting_0dbc_eq_02_on_fail   [strong structural]
- Clears exact probe/result byte `0DBC`.
- Computes exact delta byte `71 = 54 - 0DBB`.
- Compares that same exact delta against exact byte `0DBE`, mirrors the new delta back into `0DBE`, and reruns exact helper `EAC2` only when the mirrored value changed.
- Always runs exact settlement/search service `8820` afterward.
- If exact mode byte `0DBD == 0`, returns immediately with `0DBC` still clear.
- Otherwise indexes exact long tables `FF:CF2B,X` and `FF:CF32,X` using `X = 0DBD`.
- Loads exact compare source byte `9A9B[FF:CF2B,X]`.
- If that source byte is below exact threshold byte `FF:CF32,X`, writes exact probe/result byte `0DBC = 02`.
- Returns either way.
- Strongest safe reading: exact delta-probe helper that mirrors `54 - 0DBB` into `0DBE`, refreshes `8820`, and sets `0DBC = 02` on the failing `FF:CF` threshold case.

### C2:B2A7..C2:B31B  ct_c2_cbac_seed_copy_0f63_marker_band_builder_then_selected_slot_increment_and_9137_commit   [strong structural]
- Copies exact `0x0008` bytes from ROM `FF:CBAC` into exact WRAM target `7E:9588`.
- Seeds exact marker band at `0F63..` with `FFFF`, then uses overlapping same-bank `MVN` to propagate that sentinel across the exact 10-byte band.
- Reads exact word `0DBE & 0003`, doubles it, and writes exact word `0001` into `0F63 + 2*(0DBE & 3)`.
- Runs exact helper `8F6C`.
- Then returns to 8-bit mode, seeds exact byte `71 = 0DBE`, reruns exact settlement/search service `8820`, and zeros `A` with exact `TDC`.
- Uses exact local remap table `B315` indexed by exact mode byte `0DBD`.
- Adds the remapped byte to exact direct-page byte `6F`, stores the result in direct page `00`, uses exact long table `FF:CF2B,X` plus the same exact byte `6F` to choose an index, and increments exact word `000B,X`.
- Loads exact slot index from direct page `00`, reads exact byte `002F,X`, increments it only when it is still below exact cap `63`, reruns exact settlement/search service `8820`, then runs exact commit helper `9137`.
- Strongest safe reading: exact continuation-lane accepted-slot builder that seeds the `0F63` marker band, reruns `8820`, updates one selected slot field under a hard `63` cap, and commits through `9137`.

### C2:B315..C2:B31A  ct_c2_six_byte_local_mode_remap_table_00_02_01_03_04_05_for_b2a7   [strong]
- Exact bytes: `00 02 01 03 04 05`.
- Consumed directly by `B2A7`.
- Strongest safe reading: exact six-byte local mode-remap table for the `B2A7` builder helper.

### C2:B31C..C2:B35C  ct_c2_post_accept_slot_finalizer_loading_04c9_from_2400_0f00_optional_b10d_then_f2f3_afed_and_0d75_eq_01   [strong structural]
- Writes exact latch byte `04CB = 01`.
- Loads exact slot index from `0F00`.
- Reads exact byte `2400[0F00]` into `04C9`.
- If that exact byte is `C9`, runs exact preset chooser `B10D`.
- Always runs exact helpers `87D5` and `AE20`.
- Reloads exact slot index from `0F00`, reads exact byte `2500[0F00]`, and when that byte is zero clears exact mode byte `0DBD`.
- Reloads exact byte `2400[0F00]`, then runs exact helpers `F2F3` and `AFED`.
- Finishes by writing exact phase byte `0D75 = 01`.
- Strongest safe reading: exact post-accept slot finalizer that loads `04C9` from `2400[0F00]`, optionally reuses `B10D`, runs the fixed follow-up helpers, conditionally clears `0DBD` from `2500[0F00]`, and leaves the lane in phase `01`.

### C2:C20F..C2:C239  ct_c2_0408_to_0f00_seed_and_two_pass_local_substitution_driver_before_c286_and_c5c7   [strong structural]
- In 16-bit mode, copies exact `0x0009` bytes from `0408` into exact local work buffer `0F00`.
- Returns to 8-bit mode, clears exact local byte `04`, and seeds first exact index `X = 54 - 0F`.
- Runs exact local helper `C23A`.
- Then reloads `X = 04`, loads exact byte `00 = 0F00[X]`, reruns exact helper `C23A`, then runs exact helper `C286`, and exits through exact tail `C5C7`.
- Strongest safe reading: exact `0408 -> 0F00` seed plus two-pass local substitution driver before the shared `C286` normalizer and `C5C7` tail.

### C2:C23A..C2:C26B  ct_c2_local_substitution_rule_loader_using_identity_slot_map_pointer_table_and_969a_staging   [strong structural]
- Uses exact local identity map table `C2BD` to choose `Y`.
- Writes exact byte `00` into `0F00[Y]`.
- Loads exact replacement byte `01` from exact table `2993[Y]`.
- Uses exact local seven-entry pointer table `C2C5`.
- Pulls an exact variable-length sequence from bank `C2`; the first byte is treated as exact count-minus-one, then the remaining bytes are copied into exact WRAM staging buffer `969A`.
- Runs exact local helper `C26C` against that staged sequence.
- Strongest safe reading: exact local substitution-rule loader that uses an identity slot map, a pointer table, and a `969A` staging buffer before handing the sequence to `C26C`.

### C2:C26C..C2:C285  ct_c2_reverse_scan_replace_helper_over_969a_sequence_rewriting_matching_0f00_entries_from_00_to_01   [strong]
- Walks the exact staged sequence in `969A` backward from exact index `02`.
- Each sequence byte is treated as exact destination `Y`.
- When exact byte `0F00[Y]` still matches exact source byte `00`, rewrites that byte to exact replacement byte `01` and records that same `Y` into exact local byte `04`.
- Stops after the staged sequence is exhausted.
- Strongest safe reading: exact reverse-scan replace helper over the `969A` sequence, rewriting matching `0F00` entries from `00` to `01`.

### C2:C286..C2:C2BC  ct_c2_0f06_0f07_special_bit_reconciliation_helper_against_or_of_0f00_0f01   [strong]
- Builds exact local mask byte `00 = 0F00 | 0F01`.
- If exact byte `0F07 == 10`, copies exact byte `0F06 -> 0F07`.
- If exact bit `0x10` is absent from local mask byte `00`, forces exact byte `0F06 = 10`.
- If exact byte `0F06 == 20`, copies exact byte `0F07 -> 0F06`.
- If exact bit `0x20` is absent from local mask byte `00`, forces exact byte `0F07 = 20`.
- Strongest safe reading: exact special-bit reconciliation helper for `0F06/0F07`, keyed by the OR of `0F00` and `0F01`.

### C2:C2BD..C2:C2C4  ct_c2_eight_byte_local_identity_slot_map_00_01_02_03_04_05_06_07_for_c23a   [strong]
- Exact bytes: `00 01 02 03 04 05 06 07`.
- Consumed directly by `C23A`.
- Strongest safe reading: exact eight-byte local identity slot map for the `C23A` rule loader.

### C2:C2C5..C2:C2D2  ct_c2_seven_entry_local_substitution_sequence_pointer_table_for_c23a   [strong]
- Exact little-endian word pointers:
- `C2D3`
- `C2DB`
- `C2E2`
- `C2E8`
- `C2EC`
- `C2F1`
- `C2F7`
- Consumed directly by `C23A`.
- Strongest safe reading: exact seven-entry local substitution-sequence pointer table for the `C23A` helper family.

### C2:C2D3..C2:C2F9  ct_c2_local_variable_length_substitution_sequences_for_c23a_rule_loading   [strong]
- Exact sequences:
- `C2D3`: `07 01 02 03 04 05 06 07`
- `C2DB`: `06 00 02 04 05 06 07`
- `C2E2`: `05 00 01 03 04 05`
- `C2E8`: `03 00 02 05`
- `C2EC`: `04 00 01 02 05`
- `C2F1`: `05 00 01 03 02 04`
- `C2F7`: `03 00 01 07`
- Each sequence is consumed through the pointer table at `C2C5`.
- Strongest safe reading: exact local variable-length substitution sequences used by the `C23A` rule loader.

## Alias / wrapper / caution labels

### 7E:0DBC  ct_c2_continuation_family_probe_result_byte_left_clear_or_forced_to_02_by_b275   [caution]
- `B275..B2A6` clears it first.
- The same helper only ever forces exact value `02` on the failing `FF:CF` threshold case.
- Both continuation loops (`B17F` and `B200`) branch on whether it stayed clear or became nonzero.
- Strongest safe reading: exact continuation-family probe/result byte, left clear on the pass case or forced to `02` by `B275`.

### 7E:0DBE  ct_c2_continuation_family_delta_or_span_byte_mirrored_from_54_minus_0dbb_and_consumed_by_b2a7   [caution]
- `B275..B2A6` mirrors exact byte `54 - 0DBB` into it every time the probe helper runs.
- `B2A7..B31B` consumes it twice: once through exact low two bits for the `0F63` marker-band seed, and once again as exact byte `71` before rerunning `8820`.
- Strongest safe reading: exact continuation-family delta/span byte mirrored from `54 - 0DBB` and then consumed by `B2A7`.

### 7E:0D75  ct_c2_continuation_family_phase_byte_written_as_02_by_b24a_and_01_by_b31c   [caution]
- `B24A..B274` always leaves exact value `02`.
- `B31C..B35C` always leaves exact value `01`.
- Strongest safe reading: exact continuation-family phase byte toggled between the post-probe and post-finalizer stages.

## Honest remaining gap

This pass closes the exact continuation lane that pass 122 pointed at, but these honest holes remain:

- `C2:B35D..C2:B48D` is now the next continuation-family block immediately after the new `B31C` finalizer
- `C2:C2FA..C2:C340` is now the next obvious owner block above the newly-frozen `C20F` helper family
- stronger gameplay-facing nouns are still open for:
- `0D8B/0D8C/0D90`
- `0F0F/0D1F`
- `0DBD/0DC0/0DBF`
- the broader top-level noun for `C2:A886..AA30`
