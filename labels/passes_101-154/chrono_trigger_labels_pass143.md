# Chrono Trigger Labels — Pass 143

## Purpose

Pass 143 closes the front callable/helper family that pass 142 left open at `C2:E34A..C2:E5F0`, with the important structural correction that the old seam end was too short: the exact callable/helper closure here stops at `C2:E60A` because `C2:E5CC..C2:E60A` is one complete callable owner.

## Strong labels

### C2:E34A..C2:E361  ct_c2_count_capped_offset_writer_mirroring_8_times_min_0f06_4_plus_9c_into_0880_0884   [strong structural]
- Caps the effective exact count byte `0F06` at exact max `04`.
- Shifts that exact capped value left three times and adds exact base byte `9C`.
- Mirrors the exact final byte into exact work/config bytes `0880` and `0884`.
- Strongest safe reading: exact count-capped offset writer for the live exact `0F06` count lane.

### C2:E362..C2:E38E  ct_c2_0f0c_selected_clear_then_e390_e3e0_normalize_compare_or_9890_fallback_copy_owner   [strong structural]
- Clears one exact byte in the exact `0F0C`-selected destination lane.
- Runs exact helpers `E390` and exact core entry `E3E0`.
- Returns exact nonzero immediately when exact helper `E3E0` matched.
- When exact helper `E3E0` returned zero and exact byte `9890` is also zero, forces exact return byte `FF`.
- Otherwise copies exact `0x0006` bytes from exact staging band `9890` into the exact `0F0C`-selected destination lane and returns exact zero.
- Strongest safe reading: exact normalize / compare / fallback-copy owner around the live exact `0F0C` destination lane.

### C2:E38F..C2:E3DD  ct_c2_compact_9890_list_normalizer_using_0f00_98a0_and_51_start_lane   [strong structural]
- Clears exact word `9890` and performs one exact overlapping same-bank block move `9890 -> 9892` for exact length `0003`.
- Copies exact `0x0006` bytes from exact work band `0F00` into exact staging band `98A0`.
- Clears any exact `EF` bytes out of the exact `98A0` copy.
- Starting from exact byte `51`, compacts the surviving exact nonzero / non-`EF` bytes back into exact staging band `9890`.
- Strongest safe reading: exact compact-list normalizer that rebuilds the exact `9890` list from exact work band `0F00`.

### C2:E3DE..C2:E40D  ct_c2_overlapping_row_match_helper_pair_scanning_9890_against_2c23_plus_6n_rows_then_eacc   [strong structural]
- Exact entry `E3DE` seeds exact work byte `00` from exact selector byte `51` and falls into the shared core at exact `E3E0`.
- Shared core scans exact five-byte rows in exact table family `2C23 + 6*n` against the live exact `9890` compact list.
- On exact row match, runs exact helper `EACC` and returns exact byte `FF`.
- On mismatch, advances the exact row-base selector by exact stride `06` and retries while the exact base stays below exact bound `30`.
- Otherwise returns exact zero through exact `TDC`.
- Strongest safe reading: exact overlapping row-match helper pair for the normalized exact `9890` list.

### C2:E40E..C2:E53D  ct_c2_large_setup_import_selector_emission_owner_materializing_9890_0f00_4e40_5e00_then_tail_jumping_e34a   [strong structural]
- Clears exact selector byte `54`, emits exact selector packet `C3BC`, and runs exact helper `E545`.
- Copies exact items from exact source family `30CC` into exact staging band `9890` through exact helper `EF65`.
- Seeds exact words/bytes `0D06 = 0003`, `0F0A = 00`, `0F0B = 53`, `0F08 = 51`, and `0D46 = 71`.
- Uses exact hardware-math lane `4202/4203/4216` to derive exact source base `2C23 + 6*71` and copies exact `0x0006` bytes from that exact row into exact work band `0F00`.
- Clears exact byte `0F06`, materializes exact `4E40` and `5E00` work bands through overlapping same-bank block moves, and seeds exact word `0D0E = 01F0`.
- Runs exact service chain `C41F -> ED31`, `86DD`, `F90C`, `FB97`, and exact long helper `FF:FC04`.
- Emits exact selector chain `FBCE -> FBF8 -> FC37 -> FC1B -> E53E` through exact helper `8385`.
- Seeds exact bytes `0D13 / 299F`, conditionally decrements exact byte `0D9A` when exact byte `299F == 00`, restores flags, and tail-jumps to exact helper `E34A`.
- Strongest safe reading: exact large setup / import / selector-emission owner for the nonzero lane chosen by exact owner `E1EE`.

### C2:E53E..C2:E544  ct_c2_local_selector_packet_blob_00_78_00_5e_7e_00_08_consumed_by_8385_from_e40e   [strong]
- Exact owner `E40E` loads exact `X = E53E` and emits the exact local object through exact helper `8385`.
- Exact bytes: `00 78 00 5E 7E 00 08`.
- Strongest safe reading: exact local selector packet / descriptor blob consumed by exact helper `8385` from exact owner `E40E`.

### C2:E545..C2:E575  ct_c2_ff_c9ac_stream_materializer_building_delimited_9890_groups_from_51_start_lane   [strong structural]
- Seeds exact inner count byte `00 = 0A` and exact outer count byte `01 = 08`.
- Starting from exact selector byte `51`, repeatedly loads exact bytes from exact long table `FF:C9AC,X`.
- Writes each exact fetched byte into exact staging band `9890,Y`, then writes one exact `FF` separator byte.
- After each exact ten-byte inner run, writes one exact `01` delimiter byte.
- Repeats the exact outer run eight times, then terminates the exact stream with exact byte `00`.
- Strongest safe reading: exact `9890` table-materialization helper producing delimiter-rich exact group output from exact long table `FF:C9AC`.

### C2:E576..C2:E5CB  ct_c2_zero_lane_import_staging_owner_copying_ff_f008_streams_and_ff_ce9a_into_wram_then_fc61_tail   [strong structural]
- Copies exact `0x0480` bytes from exact source block `FF:F008` into exact WRAM destination `7E:3600`.
- Runs an exact twelve-step follow-on import loop copying exact `0x0010`-byte source chunks from bank `FF` into the destination stream while inserting exact `0x0010` destination gaps.
- Emits exact selector `C429`, runs exact helper `86DD`, and copies exact `0x0020` bytes from exact source block `FF:CE9A` into exact WRAM destination `7E:9500`.
- Seeds exact word `0D0E = 0001`, increments exact byte `0D15`, seeds exact byte `0D13 = 05`, and emits exact selector chain `FBCE -> FBF8 -> FC61`.
- Strongest safe reading: exact zero-lane import / staging owner for the exact `E1EE` zero path.

### C2:E5CC..C2:E60A  ct_c2_54_plus_1_change_handler_refreshing_0d77_020c_5248_6a20_cf3b_0200_then_fa49   [strong structural]
- Loads exact byte `54`, increments the exact accumulator once, and compares the exact result against exact latch byte `0D77`.
- Returns immediately when the exact value is unchanged.
- On exact change, mirrors the exact accumulator into exact bytes `0D77` and `020C`.
- Seeds exact words/bytes `0DC5 = 5248`, `0DCC = 6A20`, `020D = CF3B`, `020F = FF`, `0DC9 = 02`, and `0DD0 = 0200`.
- Runs exact helper `FA49` and returns.
- Strongest safe reading: exact `(54 + 1)` change-handler / refresh owner for the live exact selector byte `54`.

## Honest remaining gap

- the old seam `C2:E34A..C2:E5F0` is now closed more honestly as `C2:E34A..C2:E60A`
- the old seam end at `C2:E5F0` cut the exact `E5CC` owner in half
- the next live family begins immediately at `C2:E60B`, where a strange stack-relative opener is followed by clearer downstream exact owners at `E61B`, `E6AE`, `E705`, and `E73F`
