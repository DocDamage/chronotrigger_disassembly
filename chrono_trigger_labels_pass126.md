# Chrono Trigger Labels — Pass 126

## Purpose

Pass 126 closes the next continuation-family owner chain after the pass-125 bridge and freezes the next post-substitution / descriptor-normalization family under the `C2:C20F` local substitution path.

## Strong labels

### C2:B6D3..C2:B72E  ct_c2_0f4a_gated_continuation_owner_mirroring_into_0dd9_0f48_then_running_bb1f_be01_bdeb_and_fbe3   [strong structural]
- In 8-bit mode, seeds exact compare byte `71 = 0419 + 041A` and reruns exact settlement/search service `8820`.
- Mirrors exact byte `0F4A -> 0DD9`, runs exact helper `93BF`, and tests the returned exact byte `A`.
- Nonzero path rewrites exact byte `0D95` through exact helper `8BA6`, restores exact byte `0F4A = 0DD9`, mirrors exact selector byte `0F4A -> 00`, then runs exact helper chain `BD6B -> 821E`.
- Zero path reruns exact helper `EA53` and, when the result is negative, enters exact local guard/helper `B72F` before continuing.
- Always mirrors exact selector byte `54 -> 0F48`, conditionally reruns exact helper `EAC2` when exact byte `54 != 81`, then runs exact helper chain `BB1F -> BE01 -> BDEB` and exits through exact selector `FBE3 -> 8385`.
- Strongest safe reading: exact `0F4A`-gated continuation owner that snapshots into `0DD9`, restores/mirrors selector state into `0F48`, and finishes through the fixed `BB1F/BE01/BDEB/FBE3` tail chain.

### C2:B72F..C2:B741  ct_c2_local_selector_guard_requiring_nonzero_54_or_0f4a_at_least_57_before_b742_work   [strong]
- Returns immediately when exact byte `54 == 0` and exact byte `0F4A == 0`.
- Otherwise allows the downstream exact lane when `54 != 0` and exact byte `0F4A >= 57`, or when exact byte `54 == 0` and exact byte `0F4A != 0`.
- Strongest safe reading: exact local selector/threshold guard deciding whether the downstream `B742` worker may proceed.

### C2:B742..C2:B7CB  ct_c2_signed_0f4a_step_adjuster_then_0f4c_loader_and_twelve_step_0dab_ramp_finalizer   [strong structural]
- Seeds exact setup words `9696 = 9303` and `9698 = 0022`, writes exact byte `0DAA = 09`, and runs exact helper `EB9B`.
- Exact control bit `5A.bit2` decrements or increments exact byte `0F4A` by one.
- Builds exact index `Y = 54 + 0F4A`, loads exact byte `0F00[Y]`, and stores that exact byte into `0F4C`.
- Seeds exact source word `61 = 3424`, runs exact helper `BD99`, emits exact selector `FBE3 -> 8385`, and reruns exact helper `EAC2`.
- In 16-bit mode, seeds exact loop word `0DAB = 0`, accumulates exact step word `0D22` into it, mirrors sign-dependent carry through exact word `0D95`, decrements exact loop word `0D24`, and reruns exact helper `EB1F` until the exact countdown completes.
- Finishes through exact helper `B7CC`, clears exact word `0D22`, clears exact byte `0D11`, rewrites exact byte `0D95` through exact helper `8BA6` from exact byte `0F4A`, seeds exact word `9694 = 9710`, sets exact bit `0x80` in exact word `0D13`, and returns.
- Strongest safe reading: exact signed `0F4A` step adjuster feeding exact byte `0F4C`, followed by a twelve-step exact `0DAB` ramp/finalizer lane.

### C2:B7CC..C2:B822  ct_c2_sign_split_staging_block_mover_using_0d21_to_choose_ef2b_or_repeated_same_bank_block_copies   [strong structural]
- Tests exact word `0D21` in 16-bit mode.
- Nonnegative path seeds exact words `63 = 3064`, `65 = 2FE4`, `8C = 0010`, and `8A = 0015`, then runs exact helper `EF2B`.
- Negative path seeds exact words `00 = 3338`, `02 = 33B8`, and exact loop count `04 = 000E`, then performs repeated same-bank block copies of exact length `0x0015` while subtracting exact stride `0x0040` from both source words each pass.
- After the repeated loop, runs one final same-bank block copy of exact length `0x007F` from exact block `33C0` into exact block `2FC0`.
- Strongest safe reading: exact sign-split staging/block mover that uses exact word `0D21` to choose between the `EF2B` lane and a repeated exact same-bank block-copy lane.

### C2:B823..C2:B83D  ct_c2_b83e_probe_wrapper_rechecking_0f4d_then_clearing_0dbc_when_9a97_lt_0f4f   [strong structural]
- Runs exact local helper `B83E` first.
- Seeds exact compare byte `71 = 0F4D`, reruns exact settlement/search service `8820`, then compares exact byte `9A97` against exact byte `0F4F`.
- Clears exact byte `0DBC` when `9A97 < 0F4F` and otherwise leaves the exact probe result live.
- Strongest safe reading: exact wrapper around `B83E` that rechecks the continuation compare seed and conditionally clears exact probe/result byte `0DBC`.

### C2:B83E..C2:B86F  ct_c2_0dbd_bit3_and_0dbb_73_gated_selector_recentering_helper_then_b870_and_phase_02   [strong structural]
- Tests exact control bit `0DBD.bit3`.
- When that exact bit is clear, compares exact delta `54 - 0DBB` against exact byte `73`.
- Exact control bit `5A.bit3` chooses whether the fallback selector becomes exact byte `0DBB` or exact byte `0DBB + (2*73 - 1)`.
- Stores the chosen exact selector back into exact byte `54`, runs exact helper `B870`, writes exact phase byte `0D75 = 02`, and returns.
- Strongest safe reading: exact selector recentering helper gated by exact mode bit `0DBD.bit3` and exact compare inputs `0DBB/73`, followed by the shared `B870` probe and exact phase write `02`.

### C2:B870..C2:B8D8  ct_c2_continuation_probe_loop_building_two_bit_result_in_0dbc_from_x_plus_03_3f_and_07_09_compares   [strong structural]
- Clears exact probe/result byte `0DBC` before every pass.
- Seeds exact compare byte `71 = 54 - 0DBB`, mirrors that exact byte into exact byte `0DBE`, and conditionally reruns exact helper `EAC2` when the mirrored value changed and exact mode bit `0DBD.bit3 == 0`.
- Runs exact settlement/search service `8820`; exact mode bit `0DBD.bit3` chooses whether the pass count is exact `01` or exact byte `73`.
- In the exact high-bit lane, compares exact words `0003,X` and `003F,X` and contributes exact value `0x02` into exact byte `0DBC` when the compare fails.
- In the exact second lane, compares exact bytes `0007,X` and `0009,X` and contributes exact value `0x01` into exact byte `0DBC` when the compare fails.
- When exact byte `0DBC` stayed zero, increments exact compare byte `71`, decrements the local pass counter, and repeats.
- Strongest safe reading: exact continuation probe loop that builds a two-bit probe/result byte in `0DBC` from the paired `X+03/X+3F` and `X+07/X+09` threshold checks.

### C2:B8D9..C2:B95C  ct_c2_ba4f_b6ae_driven_packet_import_finalizer_copying_exact_ff_blocks_into_94c0_9510_then_signaling_0d13_eq_01   [strong structural]
- Emits exact selector packet `BFA0 -> ED31`, clamps exact byte `0419` against exact byte `73`, then runs exact helper chain `F5A7 -> 821E -> F643 -> BA4F -> B6AE`.
- In 16-bit mode, performs six exact block copies from bank `FF` into exact WRAM destinations `94C0`, `94C8`, `94E0`, `94E8`, `9520`, and `9500` using exact source bases `CBB4`, `CBB4`, `9C70`, `9C70`, `CE04`, and `CDF4`.
- Returns to 8-bit mode, writes exact byte `0D13 = 01`, runs exact helper `86DD`, emits exact selectors `FBE3 -> 8385` and `FBFF -> 8385`, and returns.
- Strongest safe reading: exact packet/import finalizer that feeds `BA4F/B6AE`, copies six exact `FF` blocks into WRAM staging bands `94C0..952F`, and signals completion with exact byte `0D13 = 01`.

### C2:B95D..C2:B977  ct_c2_short_f643_and_c037_emit_wrapper_signaling_0d13_eq_01_then_fbe3   [alias wrapper]
- Exact body runs `F643`, emits exact selector packet `C037 -> ED31`, writes exact byte `0D13 = 01`, and exits through exact selector `FBE3 -> 8385`.
- Strongest safe reading: exact short wrapper used when only the compact `F643/C037/FBE3` emit path is needed.

### C2:B978..C2:B9E0  ct_c2_overflow_tail_seeding_54_from_0419_plus_0b_bumping_0d15_then_building_mirrored_5d44_5dc4_blocks_before_e923   [strong structural]
- Emits exact selector packet `BFDA -> ED31`, seeds exact selector byte `54 = 0419 + 0B`, increments exact byte `0D15`, and forces exact bytes `84 = FF` and `0D78 = FF`.
- Writes exact byte `0D13 = 6D`, emits exact selector chain `FC3E -> 8385`, `FBFF -> 8385`, `FC1B -> 8385`, then runs exact helper `82E1`.
- In 16-bit mode, copies exact `0x0005` bytes from exact block `2857` into exact block `7F20`.
- Seeds exact word `5D44 = 21FF`, copies exact `0x0016` bytes `5D44 -> 5D46`, then copies exact `0x0018` bytes `5D44 -> 5DC4`.
- Runs exact helper `8B93`, restores flags, and exits through exact jump `E923`.
- Strongest safe reading: exact overflow tail that reseeds exact selector `54`, bumps exact byte `0D15`, builds mirrored exact `5D44/5DC4` blocks, and rejoins the shared tail at `E923`.

### C2:B9E1..C2:BA08  ct_c2_phase_02_packet_prep_clearing_19d1_19c1_19d8_seeding_19ce_1c38_then_entering_ba09   [strong structural]
- Writes exact phase byte `0D75 = 02`.
- Seeds exact compare byte `71 = 0419 + 041A`, reruns exact settlement/search service `8820`, clears exact bytes `19D1`, `19C1`, and `19D8`, seeds exact word `19CE = 1C38`, then runs exact helper `BA09`.
- Strongest safe reading: exact phase-02 packet-prep wrapper clearing the live `19D1/19C1/19D8` state and seeding exact word `19CE = 1C38` before the local `BA09` packet helper.

### C2:BA09..C2:BA2E  ct_c2_9a90_derived_packet_byte_loader_writing_19da_from_181a_0d2c_and_conditionally_running_f422   [strong structural]
- Uses exact byte `9A90` to derive one exact selector byte through exact helper `F626`.
- Loads exact byte `181A[0D2C]` into exact byte `19DA`.
- Uses exact temporary direct-page push/pop around exact value `19C0`.
- When exact byte `9A90 != 00`, rewrites exact local byte `00` and runs exact helper `F422`.
- Returns through exact `PLP ; PLD ; RTS`.
- Strongest safe reading: exact local packet-byte loader deriving one selector from `9A90`, writing `19DA` from `181A[0D2C]`, and conditionally running exact helper `F422`.

### C2:C5C7..C2:C618  ct_c2_six_entry_post_substitution_descriptor_normalizer_comparing_0f00_against_staged_9890_then_writing_2e02_2e04   [strong structural]
- In 16-bit mode, copies exact `0x0008` bytes from exact source block `0408` into exact staging block `9890`.
- Seeds exact countdown byte `00 = 05`, then in 8-bit mode marks exact byte `9890[(54 - 0F)] = FF`.
- Runs an exact six-entry reverse loop over exact bytes `0F00[5..0]` and exact staged bytes `9890[5..0]`.
- Uses exact destination word table `C5A7`, writes exact word `0031` to both `2E02+dest` and `2E04+dest` when the compared bytes differ, and otherwise leaves the exact default marker live.
- When the compared exact byte is nonnegative, converts that exact byte through exact helper `C5B3` and writes the returned exact word to `2E04+dest`.
- Strongest safe reading: exact six-entry post-substitution descriptor normalizer that compares exact local work bytes `0F00` against a staged exact `0408` copy in `9890` and rewrites exact descriptor words under `2E02/2E04`.

### C2:C619..C2:C61E  ct_c2_three_word_local_dispatch_table_c627_c65d_c6b9_for_the_post_substitution_worker_family   [strong]
- Exact little-endian word entries: `C627`, `C65D`, `C6B9`.
- Strongest safe reading: exact three-word local dispatch table for the downstream post-substitution worker family.

### C2:C61F..C2:C648  ct_c2_preentry_wrapper_above_c627_gating_on_0f0b_plus_0f0c_then_selecting_next_clear_slot_via_c649_before_caf3   [strong structural]
- In 8-bit mode, preloads exact index byte `X = 7F`.
- Tests exact sum `0F0B + 0F0C`.
- When that exact sum is `< 02`, clears exact byte `67`, increments exact byte `68`, and exits through exact jump `EACC`.
- Otherwise runs exact helper `C649`, reruns exact helper `EAC2`, and exits through exact jump `CAF3`.
- Strongest safe reading: exact pre-entry wrapper above the `C627` dispatch target, gating on exact sum `0F0B + 0F0C` before selecting the next clear slot and rejoining the shared `CAF3` tail.

### C2:C649..C2:C65C  ct_c2_next_clear_slot_scanner_over_0f02_high_bits_latching_x_into_54_and_forcing_0f00_0f01_to_ff   [strong]
- Increments exact index `X` until exact byte `0F02[X] & C0 == 0`.
- Latches that exact index back into exact selector byte `54`.
- Forces exact bytes `0F00 = FF` and `0F01 = FF`, increments exact byte `68`, and returns.
- Strongest safe reading: exact next-clear-slot scanner over exact byte lane `0F02`, latching the selected exact slot into `54` and forcing exact bytes `0F00/0F01` to `FF`.

### C2:C65D..C2:C6B8  ct_c2_0d1d_gated_post_selection_owner_with_clear_return_negative_ef05_lane_and_overflow_jump_9a98   [strong structural]
- Runs exact helper `E984` and tests exact status byte `0D1D`.
- Clear path runs exact helper `C805`; when exact byte `81 != 54`, reruns exact helper `EAC2`; otherwise returns immediately.
- Negative path reruns exact helper `EAC2`, mirrors exact bytes `80 -> 0DA8` and `7F -> 54/0D9C`, derives an exact size/offset pair from `54 - 03`, seeds exact `EF05` parameter words `5B/5C/5D/5F` and exact source word `61 = 2E00`, runs exact helper `EF05`, copies exact byte `0F0D -> 0F00`, increments exact byte `68`, and exits through exact jump `8A31`.
- Overflow path enters exact local helper `C6E7` and then exits through exact jump `9A98`.
- Strongest safe reading: exact `0D1D`-gated post-selection owner with a clear-return lane, a negative exact `EF05` staging lane, and an overflow escape into exact jump `9A98`.

### C2:C6B9..C2:C6E6  ct_c2_0d1d_gated_sibling_post_selection_owner_optionally_mirroring_0f0d_into_0f01_then_running_c70c   [strong structural]
- Runs exact helper `E984` and tests exact status byte `0D1D`.
- Clear path matches the earlier exact `C805` / optional `EAC2` / return behavior.
- Negative path tests exact byte `0F0D`; when exact bit `0x40` is clear, mirrors exact byte `0F0D -> 0F01` before running exact helper `C70C`.
- Both the exact negative and exact overflow paths rerun exact helper `EAC2`, restore exact selector byte `54 = 7F`, decrement exact byte `68`, and fall into the shared exact helper `C6E7`.
- Strongest safe reading: exact sibling `0D1D`-gated post-selection owner that optionally mirrors exact byte `0F0D` into `0F01`, then enters the shared exact `C6E7` tail.

### C2:C6E7..C2:C70B  ct_c2_shared_packet_flag_clear_helper_forcing_0f00_0f01_to_ff_then_clearing_1811_in_0x40_strides   [strong]
- Forces exact bytes `0F00 = FF` and `0F01 = FF`.
- Runs exact helper `8255` with `A = 40`.
- Uses exact starting index byte `51` and clears exact byte lane `1811,X`, advancing `X` by exact stride `0x0040` until `X >= 01C0`.
- Strongest safe reading: exact shared packet-flag clear helper that forces exact bytes `0F00/0F01` to `FF`, then clears exact byte `1811` across exact `0x40` strides.

### C2:C70C..C2:C783  ct_c2_0f00_0f01_swap_normalizer_adjusting_0d9c_via_c784_then_running_f378_fbe3_cd2b_cde3   [strong structural]
- In 8-bit mode, swaps exact bytes `2980[0F00]` and `2980[0F01]`, then runs exact helper `816A`.
- When exact byte `0D9C >= 03`, builds a new exact byte `0D9C = 0D9C + 0DA8 - 80 - 03`, and clamps the exact small-result case into exact bytes `5B = 02` and `5C = 20`.
- Otherwise derives exact bytes `5B/5C` from exact helper `C784` using first exact byte `0D9C` and then exact byte `7F`, and mirrors the second result into exact bytes `005D/005E`.
- In 16-bit mode, seeds exact words `61 = 2E00` and `5F = 050A`, runs exact helper `F378`, emits exact selector `FBE3 -> 8385`, then runs exact helpers `CD2B` and `CDE3`.
- Strongest safe reading: exact `0F00/0F01` swap/normalizer that adjusts exact byte `0D9C`, derives exact `5B/5C/5D/5E` descriptor parameters, and finishes through the fixed `F378/FBE3/CD2B/CDE3` tail chain.

### C2:C784..C2:C7A5  ct_c2_local_descriptor_parameter_helper_reducing_values_mod_03_and_emitting_small_5b_5c_pairs   [strong]
- Uses exact threshold `03` to split values into low and high bands.
- Exact high-band path subtracts `03` and seeds exact local byte `00 = 13`; exact low-band path seeds exact local byte `00 = 03`.
- Masks the remaining exact value with `07`, derives a second exact parameter byte into exact local byte `01`, and when exact word `0D36 != 0` forces exact local byte `00 = 09`.
- Returns the exact low byte pair through exact locals `00/01`.
- Strongest safe reading: exact local descriptor-parameter helper that reduces values around threshold `03` and emits a small exact `00/01` parameter pair for `C70C`.

## Alias / wrapper / caution labels

### 7E:0F4A  ct_c2_signed_continuation_delta_byte_snapshotted_through_0dd9_and_adjusted_by_b742   [caution strengthened]
- `B6D3..B72E` snapshots it into exact byte `0DD9`, restores it, and mirrors it into exact selector byte `0F48`.
- `B742..B7CB` increments or decrements it by one based on exact control bit `5A.bit2`, then uses the result to build exact byte `0F4C` through exact index `54 + 0F4A`.
- Strongest safe reading: exact signed continuation-delta byte snapshotted through `0DD9` and adjusted by the `B742` worker family.

### 7E:0DBC  ct_c2_two_bit_continuation_probe_result_byte_built_from_the_b870_dual_compare_loop   [caution strengthened]
- `B823..B83D` can clear it after the final `9A97 < 0F4F` threshold recheck.
- `B870..B8D8` rebuilds it from two exact compare lanes: the exact word compare `0003,X` vs `003F,X` contributes exact value `0x02`, and the exact byte compare `0007,X` vs `0009,X` contributes exact value `0x01`.
- Strongest safe reading: exact two-bit continuation probe/result byte built by the `B870` dual-compare loop.

## Honest remaining gap

- `C2:BA2F..C2:BEE5` is now the next real continuation-family seam after the newly closed owner chain at `B6D3..BA2E`.
- `C2:C7A6..C2:C8AF` is now the next live post-substitution / descriptor-normalization seam after the newly closed `C5C7..C783` family.
- stronger gameplay-facing nouns are still open for `0F0F/0D1F`, the broader gameplay/system role of `0D8B/0D8C/0D90`, and the broader top-level family noun for `C2:A886..AA30`.
