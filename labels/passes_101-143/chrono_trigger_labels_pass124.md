# Chrono Trigger Labels — Pass 124

## Purpose

Pass 124 closes the next exact continuation-family block after `B31C`, then freezes the first real owner block above the `C20F` local-substitution helper family.

## Strong labels

### C2:B35D..C2:B364  ct_c2_eac2_then_inc_68_tail_stub_jumping_into_b979   [alias wrapper]
- Exact body: `JSR EAC2 ; INC 68 ; JMP B979`.
- Strongest safe reading: exact tail stub that refreshes through `EAC2`, advances exact byte `68`, and rejoins the already-existing tail at `B979`.

### C2:B365..C2:B3AD  ct_c2_status_gated_b520_progress_watcher_with_negative_0f48_0f49_lane_bb50_tail_and_overflow_jump_9a98   [strong structural]
- Starts by emitting exact selector packet `ED31` with `X = C042`.
- Increments exact byte `68`, snapshots exact byte `84 -> 83`, then runs exact helper `E984`.
- Tests exact status byte `0D1D`.
- When `0D1D.bit7 == 0` and `0D1D.bit6 == 0`, runs exact helper `B520`, compares exact byte `84` against its snapshot in `83`, and only reruns exact helper `EAC2` when the byte changed.
- When `0D1D.bit7 != 0`, takes exact overflow exit `JMP 9A98`.
- When `0D1D.bit7 == 0` and `0D1D.bit6 != 0`, checks exact byte `0F49`: zero jumps through exact helper `EACC`, nonzero reruns `EAC2`, loads exact selector byte `54 = 0F48`, increments exact byte `68`, decrements exact byte `0D78`, runs exact helpers `B9E1` and `BB50`, and exits through exact selector `FBE3 -> 8385`.
- Strongest safe reading: exact status-gated progress watcher around `B520`, with a negative-bit lane driven by exact bytes `0F48/0F49` and `0D78`, plus a fixed overflow escape into `9A98`.

### C2:B3AE..C2:B3E5  ct_c2_0d1d_gated_dispatcher_setting_0d13_eq_6d_with_clear_path_to_b6d3_overflow_path_to_ba4f_and_negative_path_to_b3e6   [strong structural]
- Writes exact byte `0D13 = 6D`, then runs exact helper `E984`.
- Tests exact status byte `0D1D`.
- When `0D1D.bit7 == 0` and `0D1D.bit6 == 0`, exits through exact jump `B6D3`.
- When `0D1D.bit7 != 0`, runs exact helper `8255` with `A = 04`, reruns `EAC2`, decrements exact byte `68`, runs exact helper `F566`, writes exact byte `1A18 = FF`, seeds exact selector byte `54 = 0419 + 0B`, clears exact byte `0F4C`, runs exact helper `BA4F`, and exits through exact selector `FBE3 -> 8385`.
- When `0D1D.bit7 == 0` and `0D1D.bit6 != 0`, falls into the exact downstream loader at `B3E6`.
- Strongest safe reading: exact `0D1D`-gated dispatcher that chooses the clear-path `B6D3` lane, the overflow `BA4F` lane, or the negative-bit table-loader lane rooted at `B3E6`.

### C2:B3E6..C2:B48D  ct_c2_negative_bit_table_loader_indexing_ff_records_from_0f4c_then_seeding_0dbd_0dc0_0dbf_and_entering_be79   [strong structural]
- Loads exact selector byte `54 = 0F48`.
- If exact byte `78` is negative, exits immediately through exact helper `EACC`.
- Otherwise writes exact hardware-multiply seed `$4202 = 0C`, writes exact index byte `0F4C` to `$4203`, and rejects the lane when exact byte `7700[0F4C]` is negative.
- In 16-bit mode, reads exact product word `$4216 -> 00`.
- Seeds exact compare byte `0F4D = 0419 + 041A`, mirrors that exact byte into `71`, reruns exact settlement/search service `8820`, clears exact byte `0F4E = FF`, runs exact helper `BC22`, stores the result into exact byte `0F4F`, and rejects the lane when exact byte `9A97 < 0F4F`.
- After exact helper `EAC2`, uses the multiplied exact offset in `00` to read exact `FF:2141,X` and `FF:2140,X` record bytes.
- Builds exact control byte `0DBD` from `FF:2141,X & C0`, then ORs in exact mode bits `04` or `08` derived from `FF:1ACB[2*0F4C] & 01`.
- Builds exact companion control byte `0DC0 = FF:2140,X & 1F`.
- Loads exact tail byte `0DBF = 9AC9`.
- Increments exact byte `68`.
- Seeds exact bytes `54/0D9C/0DBB = 08` and clears exact byte `0DBE`.
- If exact control byte `0DBD.bit3 != 0`, runs exact helper `8AD5`.
- Then enters exact helper `BE79`, increments exact byte `C1`, and returns.
- Strongest safe reading: exact negative-bit continuation-family table loader that indexes `FF` record families from exact byte `0F4C`, derives exact preset bytes `0DBD/0DC0/0DBF`, seeds the continuation lane for exact span `08`, and hands control into `BE79`.

### C2:C2FF..C2:C395  ct_c2_php_wrapped_owner_block_above_c20f_shifting_4e44_4e5c_running_c3e4_c456_c495_c57a_and_copying_ff_blocks_into_94e0_9520   [strong structural]
- Begins with exact `PHP`, increments exact byte `C9`, and emits exact selector packet `ED31` with `X = C19C`.
- In 16-bit mode, writes exact word `21FF -> 4E44`, then uses overlapping same-bank `MVN` to shift exact `0x001A` bytes from `4E44 -> 4E46`.
- Writes exact word `21FB -> 4E5C`, then uses overlapping same-bank `MVN` to shift exact `0x0002` bytes from `4E5C -> 4E5E`.
- Runs exact selector `8385` with `X = FC4C`.
- Then runs exact helpers `C43A`, `821E`, exact selector packet `ED31` with `X = C1B9`, exact local helper `C3E4`, and exact helpers `C456`, `C495`, and `C57A`.
- Copies exact `0x0008` bytes `FF:9C70 -> 7E:94E0`.
- Copies the same exact `0x0008` bytes `FF:9C70 -> 7E:94E8`.
- Copies exact `0x0008` bytes `FF:CBB4 -> 7E:94B0`.
- Copies exact `0x0030` bytes `FF:CBE4 -> 7E:9520`.
- Returns to 8-bit mode, runs exact helper `86DD`, writes exact byte `0D13 = 1C`, runs exact helper `984A`, dispatches exact selectors `FBE3 -> 8385` and `FBFF -> 8385`, then exits through exact `PLP ; RTS`.
- Strongest safe reading: exact `PHP`-wrapped owner block above the `C20F` substitution family that shifts exact `4E44/4E5C` windows, runs the fixed local post-processing chain, imports exact `FF` data blocks into `94E0..9520`, and finishes with the exact `1C`-mode selector tail.

### C2:C396..C2:C3B3  ct_c2_php_wrapped_1c_mode_zero_clear_wrapper_for_3446_3448_3486_3488_then_fbe3_dispatch   [strong]
- Exact body:
- `PHP ; SEP #$20`
- `LDA #$1C ; STA 0D13`
- `REP #$30`
- `STZ 3446`
- `STZ 3448`
- `STZ 3486`
- `STZ 3488`
- `LDX #FBE3 ; JSR 8385`
- `PLP ; RTS`
- Strongest safe reading: exact `1C`-mode zero-clear wrapper for the two exact paired word lanes at `3446/3448` and `3486/3488`, followed by the fixed `FBE3` dispatch.

### C2:C3B4..C2:C3E0  ct_c2_php_wrapped_0417_latched_setup_wrapper_writing_0d0e_0189_0d77_ffff_inc_0d15_then_fbe3_fbff_and_e923   [strong structural]
- Begins with exact `PHP ; SEP #$20`.
- Loads exact selector byte `0417`, mirrors it into exact bytes `54` and `55`, and emits exact selector packet `ED31` with `X = C1F6`.
- Writes exact word `0D0E = 0189`.
- Writes exact word `0D77 = FFFF`.
- Increments exact byte `0D15`.
- Dispatches exact selectors `FBE3 -> 8385` and `FBFF -> 8385`.
- Exits through exact `PLP ; JMP E923`.
- Strongest safe reading: exact `0417`-latched setup wrapper that seeds `0D0E`, `0D77`, and `0D15` before the fixed `FBE3/FBFF` tail and exact jump into `E923`.

### C2:C3E1..C2:C417  ct_c2_php_wrapped_ten_entry_table_driven_quad_word_writer_using_c41b_c42f_and_0f09_low_bits   [strong structural]
- Begins with exact `PHP ; REP #$30` and seeds exact loop index byte `00 = 0009`.
- For exact indices `9 .. 0`, doubles the index, loads one exact destination word from local table `C41B + 2*index`, and uses that word as exact destination `Y`.
- Loads one exact selector word from local table `C42F + index`, XORs it against exact byte lane `0F09 + index`, masks the exact low bit, and chooses exact base word `1530` or `1534`.
- Writes one exact four-word pattern to `Y + 0000`, `Y + 0002`, `Y + 0040`, and `Y + 0042` using consecutive exact values from that chosen base.
- Loops until the exact index underflows, then exits through exact `PLP ; RTS`.
- Strongest safe reading: exact `PHP`-wrapped ten-entry table-driven quad-word writer keyed by local tables `C41B/C42F` and the low-bit state of exact mirror lane `0F09..0F12`.

### C2:C41B..C2:C42E  ct_c2_ten_word_local_destination_table_for_c3e1_quad_word_writer   [strong]
- Exact little-endian words consumed by `C3E1` as `C41B + 2*index`:
- `CA31`
- `CA30`
- `D62F`
- `D630`
- `D62E`
- `CA2F`
- `CA31`
- `D632`
- `0132`
- `0000`
- Strongest safe reading: exact ten-word local destination table for the `C3E1` quad-word writer.

### C2:C42F..C2:C438  ct_c2_ten_byte_local_selector_xor_table_for_c3e1_currently_all_zero   [strong]
- Exact bytes: `00 00 00 00 00 00 00 00 00 00`.
- `C3E1` reads it as exact selector source `C42F + index` before XORing against exact mirror lane `0F09 + index`.
- Strongest safe reading: exact ten-byte local selector/XOR table for `C3E1`; current ROM contents leave the low-bit choice entirely driven by the exact `0F09 + index` bytes.

## Alias / wrapper / caution labels

### 7E:0DBD  ct_c2_continuation_export_mode_control_byte_assembled_from_multiple_cc_ff_record_families_and_exact_mode_overlays   [caution strengthened]
- `B0AB..B106` already assembles it from exact `CC` records.
- `B10D..B17E` can overwrite it with exact bucket presets.
- `B3E6..B48D` now proves a second exact assembly lane from `FF:2141,X & C0` plus exact overlay bits `04/08` derived from `FF:1ACB[2*0F4C] & 01`.
- Earlier pass-118 evidence still shows exact bits `7/6/3` being consumed by the continuation/export sweep at `8E2D..8E81`.
- Strongest safe reading: exact continuation/export mode control byte assembled from multiple `CC/FF` record families and exact mode overlays.

### 7E:0DC0  ct_c2_companion_or_submode_control_byte_loaded_from_cc_ff_record_low_fields_for_the_continuation_export_family   [caution strengthened]
- `B0AB..B106` seeds it from exact `CC:0002,X` low bits with exact remap `0F -> 40`.
- `B3E6..B48D` seeds it from exact `FF:2140,X & 1F`.
- Strongest safe reading: exact companion/submode control byte loaded from low record fields for the continuation/export family.

### 7E:0DBF  ct_c2_continuation_tail_preset_byte_seeded_by_sign_bucket_and_ff_record_lanes   [caution strengthened]
- `B17F..B1F7` seeds it directly from the exact sign split of `0DBD` as `B2` or `8A`.
- `B10D..B17E` can seed it from exact bucket presets.
- `B3E6..B48D` seeds it from exact byte `9AC9` before entering `BE79`.
- Strongest safe reading: exact continuation-tail preset byte seeded by the sign lane, bucket lane, and exact `FF`-record lane.

## Honest remaining gap

This pass closes the first real owner above `C20F` and the next exact continuation-family block after `B31C`, but these honest holes remain:

- `C2:B48E..C2:B6D2` is now the next unresolved continuation-family owner seam bridging the new `B3E6` loader to the already-visible `B6D3` path
- `C2:C439..C2:C57A` still needs exact ownership for the helper chain now proven live under the new `C2FF` owner block
- stronger gameplay-facing nouns are still open for:
- `0D8B/0D8C/0D90`
- `0F0F/0D1F`
- `0F48/0F49/0F4C/0F4D/0F4E/0F4F`
- the broader top-level noun for `C2:A886..AA30`
