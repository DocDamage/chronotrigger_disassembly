# Chrono Trigger Labels — Pass 142

## Purpose

Pass 142 closes the exact follow-on callable/helper family that pass 141 left open at `C2:E163..C2:E34A`, with the structural correction that the old seam end was one byte too long: the exact callable/helper closure here stops at `C2:E349`, and `C2:E34A` is the first byte of the next live owner.

## Strong labels

### C2:E163..C2:E18A  ct_c2_selected_0f00_entry_loader_into_04c9_and_9a90_then_fbf1_tail   [strong structural]
- Runs exact helper `8820`.
- Derives one exact `0F00` source index from exact bytes `0FC8` and `54` using exact `+54 - 04` arithmetic.
- Loads exact byte `0F00,X -> 04C9` and mirrors that exact byte into exact table `9A90[0D26]`.
- Touches exact local landing byte `E18A`.
- Emits exact selector `FBF1` through exact helper `8385`.
- Strongest safe reading: exact selected-entry loader owner that stages one exact `0F00` byte into exact byte `04C9` and the exact `9A90[0D26]` mirror lane, then exits through exact selector `FBF1`.

### C2:E18B..C2:E1DB  ct_c2_partial_slot_reseed_and_marker_refresh_owner_using_e1dc_de21_c318_and_f2f3   [strong structural]
- Starts its exact loop from exact byte `51`.
- Uses exact local table `E1DC + index` to choose one exact selector byte per processed lane.
- Per exact lane, snapshots one exact byte from `9A90`, promotes the paired exact byte from `9AE6` back into `9A90`, and writes one exact marker byte `00/08/1C` into exact work byte `0D4D[index]`.
- Repeats while the exact processed index remains below exact bound `07`.
- Then derives exact row stride `Y = 8 * 71`, runs exact helper `DE21`, emits exact selector `C318` through exact helper `ED31`, and finishes through exact helper `F2F3(04C9)`.
- Strongest safe reading: exact partial slot-reseed / marker-refresh owner that promotes exact bytes from `9AE6` into `9A90`, records one exact per-lane marker into `0D4D`, refreshes one exact row through `DE21`, and exits through exact selector `C318` plus exact helper `F2F3`.

### C2:E1DC..C2:E1E3  ct_c2_local_eight_byte_selector_table_60_36_38_3b_39_37_3a_3c_for_e18b   [strong]
- Exact bytes: `60 36 38 3B 39 37 3A 3C`.
- Consumed directly by exact owner `E18B` through exact long indexed read `LDA $C2E1DC,X`.
- Strongest safe reading: exact local 8-byte selector table for the exact `E18B` partial slot-reseed / marker-refresh owner.

### C2:E1EE..C2:E209  ct_c2_299f_or_71_gate_owner_choosing_e576_zero_lane_vs_e40e_nonzero_lane_then_83b2   [strong structural]
- ORs exact byte `299F` with exact byte `71` and stores the exact result back into exact byte `299F`.
- Exact zero lane runs exact helper `E576`, seeds exact byte `68 = 02`, and jumps to exact tail `83B2`.
- Exact nonzero lane runs exact helper `E40E`, increments exact byte `68`, and jumps to exact tail `83B2`.
- Strongest safe reading: exact `299F|71`-gated owner that chooses exact zero-lane helper `E576` versus exact nonzero-lane helper `E40E` before shared exact tail `83B2`.

### C2:E20A..C2:E21E  ct_c2_00f0_gated_setup_tail_using_eac2_0d13_1d_and_0d9a_clear   [strong structural]
- Loads exact word `00F0 -> X` and returns immediately on exact zero.
- Nonzero path runs exact helper `EAC2`, seeds exact byte `0D13 = 1D`, clears exact byte `0D9A`, seeds exact byte `68 = 01`, and returns.
- Strongest safe reading: exact `00F0`-gated setup tail that conditionally reruns exact helper `EAC2` and then seeds exact bytes `0D13 / 0D9A / 68`.

### C2:E21F..C2:E235  ct_c2_e984_then_e267_poll_owner_waiting_for_e363_zero_before_82b2   [strong structural]
- Runs exact helpers `E984` and `E267`.
- Exact byte `00F0.bit0` clear returns immediately.
- Exact set path repeatedly runs exact helper `E363` until the exact returned accumulator becomes zero.
- Then jumps to exact tail `82B2`.
- Strongest safe reading: exact poll/wait owner that runs exact `E984/E267`, only continues when exact byte `00F0.bit0` is set, spins on exact helper `E363` until clear, and then exits through exact tail `82B2`.

### C2:E236..C2:E266  ct_c2_e984_e5d3_front_end_owner_with_negative_lane_2990_bit40_update_and_83ca_tail   [strong structural]
- Runs exact helpers `E984` and `E5D3`.
- Exact non-negative lane compares exact byte `0081` against exact selector byte `54`; when they differ, reruns exact helper `EAC2`, then returns.
- Exact negative lane uses exact `54.bit0` to choose exact `TSB 2990` versus exact `TRB 2990` with exact mask byte `40`.
- Then seeds exact byte `68 = 03`, runs exact helper `8255(74)`, and exits through exact tail `83CA`.
- Strongest safe reading: exact `E984/E5D3` front-end owner whose exact negative lane sets or clears exact bit `40` of exact config byte `2990` from exact `54.bit0`, then exits through exact helper `8255(74)` and exact tail `83CA`.

### C2:E267..C2:E297  ct_c2_0d1e_dispatch_owner_using_e298_e2f4_e34a_and_fbe3_tail   [strong structural]
- Snapshots exact byte `9380 -> 7F` and seeds exact hardware register `4202 = 10`.
- Uses exact byte `0D1E` as the exact dispatch state; exact negative skips the local dispatch.
- Non-negative path dispatches one exact state handler through exact local indirect table `E298`.
- Reruns exact helper `EAC2` only when the exact byte `9380` changed across the dispatch.
- Always runs exact helper pair `E2F4 -> E34A`, then emits exact selector `FBE3` through exact helper `8385`.
- Strongest safe reading: exact `0D1E`-dispatched owner that optionally runs one exact state handler out of exact local table `E298`, conditionally reruns exact helper `EAC2` when exact byte `9380` changes, then always runs `E2F4 -> E34A` before exact selector tail `FBE3`.

### C2:E298..C2:E2A1  ct_c2_local_five_word_indirect_dispatch_table_e2d6_e2cc_e2aa_e2a0_e2ad_for_e267   [strong]
- Exact words: `E2D6, E2CC, E2AA, E2A0, E2AD`.
- Consumed directly by exact owner `E267` through exact `JSR ($E298,X)`.
- Strongest safe reading: exact local 5-word indirect dispatch table for the exact `E267` owner.

### C2:E2A0..C2:E2CB  ct_c2_overlapping_decrement_increment_updater_pair_for_0f09_rebuilding_9381_and_0f0b   [strong structural]
- Exact entry `E2A0` decrements exact byte `0F09` with wrap to exact byte `07`.
- Exact entry `E2AA` increments exact byte `0F09` with wrap to exact byte `00` once exact bound `08` is reached.
- Both lanes mirror the exact final value into exact hardware register `4203`, clear exact byte `0F0A`, compute exact byte `9381 = 53 + 4216`, and mirror that exact result into exact byte `0F0B`.
- Strongest safe reading: exact overlapping decrement / increment updater pair for exact byte `0F09` that wraps inside exact range `00..07` and rebuilds exact bytes `9381 / 0F0B` from the SNES exact hardware-math result.

### C2:E2CC..C2:E2F3  ct_c2_overlapping_decrement_increment_updater_pair_for_0f08_rebuilding_9380   [strong structural]
- Exact entry `E2CC` decrements exact byte `0F08` with wrap to exact byte `09`.
- Exact entry `E2D6` increments exact byte `0F08` with wrap to exact byte `00` once exact bound `0A` is reached.
- Both lanes mirror the exact final value into exact hardware register `4203` and compute exact byte `9380 = 24 + 4216`.
- Strongest safe reading: exact overlapping decrement / increment updater pair for exact byte `0F08` that wraps inside exact range `00..09` and rebuilds exact byte `9380` from the SNES exact hardware-math result.

### C2:E2F4..C2:E315  ct_c2_0d1d_gated_tail_refill_dispatcher_using_0f06_e316_eac2_and_c41f   [strong structural]
- Tests exact status byte `0D1D` with `BIT`.
- Exact negative lane runs exact helper `E316`.
- Remaining exact update lane pops one exact entry out of exact buffer `0EFF,X` and decrements exact byte `0F06` when that exact byte is nonzero.
- Exact update lanes rerun exact helper `EAC2` before the final exact selector tail.
- Finishes through exact selector `C41F` via exact helper `ED31`.
- Strongest safe reading: exact `0D1D`-gated tail / refill dispatcher that chooses exact `E316` refill or exact `0F06` tail-pop work before exact selector tail `C41F`.

### C2:E316..C2:E349  ct_c2_lookup_backed_0f00_fill_helper_using_0f08_0f09_4216_and_ff_c9ac   [strong structural]
- Seeds exact hardware register `4202 = 0A` and mirrors exact byte `0F09 -> 4203`.
- Combines exact byte `0F08` with exact hardware-math result `4216` to derive exact lookup index `X`.
- Loads one exact byte from exact long table `FF:C9AC,X`.
- Appends that exact byte into exact buffer `0F00,Y` through the exact capped write index byte `0F06`.
- Strongest safe reading: exact lookup-backed `0F00` fill helper that uses exact bytes `0F08/0F09` plus the SNES exact hardware-math lane to fetch one exact byte out of exact long table `FF:C9AC` and append it into exact buffer `0F00`.

## Alias / wrapper / caution labels

### C2:E1E4..C2:E1ED  ct_c2_local_five_word_pointer_looking_table_between_e18b_and_e1ee_family   [caution]
- Exact words: `E1ED, E21E, E236, E201, E209`.
- The exact bytes are structurally isolated between the exact `E18B` owner and the exact `E1EE` owner.
- The clean exact local consumer is still unresolved in this pass.
- Strongest safe reading: exact local five-word pointer-looking table fragment between the `E18B` and `E1EE` family blocks; keep the exact consumer open.

## Honest remaining gap

- the old seam `C2:E163..C2:E34A` is now closed more honestly as `C2:E163..C2:E349`
- `C2:E34A` is the first byte of the next live callable owner, not part of the old family
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
