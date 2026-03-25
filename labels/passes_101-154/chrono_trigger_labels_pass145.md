# Chrono Trigger Labels — Pass 145

## Purpose

Pass 145 closes the callable/helper family that pass 144 left open at `C2:E841..C2:E923`, with the structural correction that the old seam end was too short and the honest closure actually runs through `C2:EAC1`.

## Strong labels

### C2:E841..C2:E889  ct_c2_setup_owner_calling_84ee_seeding_020c_020d_020f_materializing_52c8_5348_work_bands_then_emitting_local_e88a_packet_and_fc1b   [strong structural]
- Runs exact helper `84EE`.
- Seeds exact fields `020C = 03`, `0DC5 = 5E00`, `020D = CF3B`, and `020F = FF`.
- Runs exact helper `F90C`.
- Materializes exact propagated work bands `3021 -> 52C8` for exact length `0008` and `3062 -> 5348` for exact length `0009` through exact helper `FBB4`.
- Emits exact local selector packet `E88A`, then exact selector `FC1B`, through exact helper `8385`.
- Strongest safe reading: exact setup owner that seeds the fixed exact packet/work-band state before the exact `E88A -> FC1B` selector tail.

### C2:E88A..C2:E890  ct_c2_local_7_byte_selector_packet_08_71_00_5e_7e_00_06   [strong]
- Exact bytes: `08 71 00 5E 7E 00 06`.
- Strongest safe reading: exact local 7-byte selector packet emitted through exact helper `8385`.

### C2:E891..C2:E8B6  ct_c2_carry_sensitive_fast_lane_owner_mirroring_54_to_79_then_optionally_forcing_0f00_54_04_0d13_7f_and_emitting_c391_fbea_fbff   [strong structural]
- Mirrors exact selector byte `54 -> 79`.
- Exact set-carry path returns immediately.
- Exact clear-carry path clears exact byte `0F00`, forces exact selector byte `54 = 04`, seeds exact byte `0D13 = 7F`, emits exact selector `C391` through exact helper `ED31`, and emits exact selector pair `FBEA -> FBFF` through exact helper `8385`.
- Strongest safe reading: exact carry-sensitive fast-lane owner behind the `E61B` exact `0420 == 30` branch.

### C2:E8B7..C2:E913  ct_c2_selected_slot_clear_and_307ff8_9890_9892_9894_9895_pointer_builder_then_d28d_821e_838e_d32c   [strong structural]
- Clears exact bytes `0D49[X]` and `0D79[X]` using exact slot index byte `79`.
- Stores exact doubled selector byte `79 * 2` into exact long table `30:7FF8,X`.
- Seeds exact byte/word `9894 = 7E` and `9895 = 0200`.
- When exact slot bytes `0D49 / 0D4A / 0D4B` are all zero, clears exact long byte `30:7FE2` and seeds exact byte `9392 = 08`.
- Derives exact words `9892 = 7000 + ((78 & 0300) << 1)` and `9890 = 7900 + (78 & 0300)`.
- Runs exact helper chain `D28D -> 821E -> 838E(X=9890) -> D32C`.
- Strongest safe reading: exact selected-slot clear / pointer-build owner for the downstream exact `9890/9892/9894/9895` lane.

### C2:E8E8..C2:E913  ct_c2_overlapping_9895_9892_9890_pointer_builder_tail_then_d28d_821e_838e_d32c   [strong structural]
- Exact overlapping callable late entry.
- Seeds exact word `9895 = 0200`.
- Derives exact words `9892` and `9890` from exact byte/word `78 & 0300`.
- Rejoins exact helper chain `D28D -> 821E -> 838E(X=9890) -> D32C`.
- Strongest safe reading: exact overlapping late entry into the shared exact pointer-build tail.

### C2:E8FA..C2:E913  ct_c2_overlapping_9890_finalizer_tail_then_d28d_821e_838e_d32c   [strong structural]
- Exact overlapping callable late entry.
- Seeds exact word `9890 = 7900 + (78 & 0300)` after exact `X/Y` have already been staged.
- Rejoins exact helper chain `D28D -> 821E -> 838E(X=9890) -> D32C`.
- Strongest safe reading: exact shortest overlapping late entry into the shared exact pointer-build tail.

### C2:E914..C2:E91A  ct_c2_local_7_byte_data_40_58_80_2e_7e_80_00   [strong]
- Exact bytes: `40 58 80 2E 7E 80 00`.
- Strongest safe reading: exact local 7-byte data span immediately ahead of exact wrapper `E91B`.

### C2:E91B..C2:E922  ct_c2_poll_loop_wrapper_repeatedly_calling_e92d_then_821e   [strong structural]
- Repeatedly runs exact owner `E92D`.
- Runs exact helper `821E` after each pass.
- Exact `BRA -08` loops back to the wrapper head.
- Strongest safe reading: exact poll/wait wrapper around exact owner `E92D`.

### C2:E923..C2:E92C  ct_c2_short_wrapper_calling_984a_clearing_56_then_branching_into_e92d_shared_tail   [strong structural]
- Runs exact helper `984A`.
- Clears exact byte `56`.
- Exact `BRA +27` enters the shared tail inside exact owner `E92D`.
- Strongest safe reading: exact short wrapper proving that the old seam end at `E923` was too short.

### C2:E92D..C2:E97D  ct_c2_workspace_reset_and_0770_0773_seed_owner_zero_filling_0740_band_seeding_0904_pattern_then_indexing_9380   [strong structural]
- Seeds exact word `0740 = E000`.
- Propagates exact same-bank bands `0740 -> 0742` for exact length `013D` and `0904 -> 0906` for exact length `0011`.
- Seeds exact word `0904 = AAAA` before the second exact propagation.
- Uses exact `TSB 0D9B` with exact mask `FF`.
- On the fresh-set lane, runs exact helper `EA27`, loads exact word `9380,X -> 0770`, mirrors exact byte `58 -> 0772`, and conditionally sets exact bit `40` in exact byte `0773` when exact byte `56 != 0`.
- Strongest safe reading: exact workspace reset / propagated-pattern owner that seeds exact `0770/0773` from exact local table `9380`.

### C2:E97E..C2:E985  ct_c2_wait_loop_calling_e984_then_821e   [strong structural]
- Repeatedly runs exact helper `E984`.
- Runs exact helper `821E` after each pass.
- Exact `BRA -08` loops back to the wrapper head.
- Strongest safe reading: exact wait loop around exact helper `E984`.

### C2:E986..C2:E9D8  ct_c2_0d1d_rebuilder_from_68_snapshot_e9d9_table_2993_probes_29f4_masks_and_0d83   [strong structural]
- Clears exact status byte `0D1D`.
- Mirrors exact byte `68 -> 0D17` and compares against the exact prior snapshot.
- When exact byte `68` is unchanged, uses exact local table bytes from `E9D9` to probe exact bytes `2993[Y]` and contribute exact mask bits into exact byte `0D1D`.
- Also contributes exact mask bits into exact byte `0D1D` from exact `29F4 & 2999`, exact `29F4 & 299A`, and exact byte `0D83`.
- Strongest safe reading: exact local status-byte rebuilder for exact byte `0D1D`.

### C2:E9D9..C2:E9E1  ct_c2_local_9_byte_table_00_01_00_00_00_08_06_07_ff   [strong]
- Exact bytes: `00 01 00 00 00 08 06 07 FF`.
- Strongest safe reading: exact local 9-byte table/data span whose leading bytes are consumed by exact owner `E986`.

### C2:E9E2..C2:EA1D  ct_c2_f5_bit_scan_and_4_way_local_dispatch_owner_using_ea27_ea1e_table_then_clearing_0d1f   [strong structural]
- Mirrors exact selector byte `54 -> 81`.
- Seeds exact byte `0D1E = 80`, then exact-shifts exact byte `F5` until the first exact set bit is found or exact `X` reaches `04`.
- Mirrors the found exact index into exact byte `0D1E`.
- When exact byte `0D1F == 0`, runs exact helper `EA27`, mirrors the exact record offset into exact `Y`, mirrors exact selector byte `54 -> 55`, and dispatches one exact byte-loader leg through exact local table `EA1E`.
- Clears exact byte `0D1F` before exit.
- Strongest safe reading: exact `F5`-bit scan / mode-dispatch owner.

### C2:EA1E..C2:EA25  ct_c2_local_4_word_dispatch_table_ea45_ea40_ea3b_ea36   [strong]
- Exact words: `EA45`, `EA40`, `EA3B`, `EA36`.
- Strongest safe reading: exact local 4-word dispatch table for the overlapping exact byte-loader quartet.

### C2:EA26..C2:EA35  ct_c2_low_byte_times_6_to_x_helper   [strong structural]
- Masks exact accumulator to exact low byte with `AND #$00FF`.
- Computes exact `X = A * 6` through exact `ASL / PHA / ASL / ADC 1,S / TAX`.
- Restores exact stack/flags through exact `PLA ; PLP ; RTS`.
- Strongest safe reading: exact low-byte-times-6 helper producing one exact 6-byte local record offset in exact `X`.

### C2:EA36..C2:EA52  ct_c2_overlapping_9382_9383_9384_9385_y_table_byte_loader_quartet_into_54_with_5a_sign_latch   [strong structural]
- Exact entry `EA36` loads exact byte `9382,Y`.
- Exact entry `EA3B` loads exact byte `9383,Y`.
- Exact entry `EA40` loads exact byte `9384,Y`.
- Exact entry `EA45` loads exact byte `9385,Y`.
- All exact entries converge on the shared exact tail that mirrors the loaded exact byte into exact selector byte `54`, optionally latches exact sign into exact byte `5A`, and normalizes exact selector byte `54` before exact `RTS`.
- Strongest safe reading: exact overlapping byte-loader quartet for the exact local record bytes at `9382..9385,Y`.

### C2:EA53..C2:EA80  ct_c2_sign_and_bounds_helper_using_57_5a_0d18_0ddb_0ddc_to_normalize_54   [strong structural]
- Uses exact byte `57` as the first gate.
- Conditionally decrements exact byte `0D18` from exact `00F2.bit0`.
- Uses exact sign/control byte `5A` to choose between immediate exit, exact zero exit through `TDC`, or the exact bound-normalization lane.
- In the exact bound-normalization lane chooses between exact bytes `0DDB` and `0DDC`, mirrors the chosen exact byte into exact selector byte `54`, and repeats until the exact `0DDC >= 54` bound is satisfied.
- Strongest safe reading: exact sign/bounds helper around exact bytes `57`, `5A`, `0D18`, `0DDB`, and `0DDC`.

### C2:EA81..C2:EABC  ct_c2_delta_and_hw_division_helper_staging_0dd8_0ddc_57_0d94_0dda_0d98_from_00_y_and_4214   [strong structural]
- Mirrors exact direct-page byte `00 -> 0DD8`.
- Computes exact delta `Y - 00` and writes it to exact hardware register `$4206`.
- Saturates exact sign/borrow byte `01` on borrow.
- Derives exact byte `0DDC` from exact byte `00` and exact bound byte `0DDB`.
- Mirrors exact byte `01` into exact bytes `57`, `0D94`, and `0DDA`.
- Reads exact hardware result `$4214 -> 0D98` in exact 16-bit accumulator mode.
- Strongest safe reading: exact delta / hardware-division helper reused by multiple earlier families.

### C2:EABD..C2:EAC1  ct_c2_short_wrapper_calling_eb03   [strong structural]
- Runs exact helper `EB03`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact short wrapper into the next exact `EB03` owner.

## Honest remaining gap

- the old seam `C2:E841..C2:E923` is now closed more honestly as `C2:E841..C2:EAC1`
- the old seam end at `C2:E923` was not a stop; it is the first byte of the exact short wrapper at `C2:E923..C2:E92C`
- the next clean follow-on family now begins at exact `C2:EAC2`
