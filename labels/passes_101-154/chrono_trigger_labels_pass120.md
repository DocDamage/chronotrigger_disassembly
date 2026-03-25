# Chrono Trigger Labels — Pass 120

## Purpose

Pass 120 pushes directly into the same-bank caller seam left open after the bank-`C2` correction pass and freezes the helper family around `9DAF`, `9E76`, `A051`, `A970`, `AFED`, `BA2F`, `BAFC`, `BEE6`, and `BFD4`.

## Strong labels

### C2:9DAF..C2:9E75  ct_c2_settlement_tail_driven_dual_ef05_materializer_with_12_step_signed_ramp_and_mirrored_fill_finalizer   [strong structural]
- Seeds `71 = 54 + 0413`.
- Runs exact settlement/search service `8820` and exact gated post-settlement tail `A216`.
- Computes `04 = 61 + 0084` and runs shared helper `9EB0` with `Y = 100C`.
- Runs exact `EF05` materialization twice:
  - `61 = 2E00`, `5B = 0202`, `5D = 26`, `5F = 120C`
  - then `61 = 3E00`, `5D = 26`
- Fans out through exact service selectors `FBEA` and `FC06`.
- Then runs an exact 12-step loop using `0DAB`, `0D22`, `22`, `0D95`, and `51` to fill `5D42..5D58`, calling exact service selector `FC45` each step.
- After the 12-step loop, flips `5B` with `26 XOR 0600`, reruns `EF05`, propagates `61FF` across `5D42..5D58`, reruns `FC45`, and decrements `0D18`.
- Strongest safe reading: exact settlement-tail-driven dual-`EF05` materializer with a 12-step signed ramp writer and mirrored fill finalizer.

### C2:9E76..C2:9EAF  ct_c2_three_block_dual_page_ec93_emitter_over_2e84_stride_0180   [strong structural]
- Seeds `04 = 2E84` and `02 = 0412 & 00FF`.
- Walks exactly three slots with stride `0180`.
- Calls shared helper `9EB0` once per slot.
- Uses selector `Y = 100C` on the first two slots and `Y = 000C` on the third.
- Finishes through exact service selector `FBFF`.
- Strongest safe reading: exact three-block dual-page `EC93` emitter over `2E84 + n*0180`.

### C2:9EB0..C2:9ECC  ct_c2_paired_page_ec93_submit_helper_for_61_and_61_plus_1000   [strong]
- Stores incoming `Y -> 06`.
- Sets `61 = 04`, then runs `EC93` with `A = Y` and `X = 0006`.
- Sets `61 = 04 + 1000` and reruns `EC93` with the saved selector from `06`.
- Strongest safe reading: exact paired-page `EC93` submit helper for `61` and `61 + 1000`.

### C2:A051..C2:A0E6  ct_c2_clamped_sweep_materializer_bootstrap_with_dual_5d_fills_and_masked_strip_export   [strong structural]
- Increments `C9`.
- Computes exact clamp byte `0FC4 = max(85 - 3, 0)` and clamps `0413` downward to it when needed.
- Clamps `0412` against `73`, storing the chosen value into both `54` and `0412`.
- Runs exact common service `ED31` with `X = BD74`.
- Propagates `61FF` across both `5D42..5D58` and `5DC2..5DD8`.
- Runs exact service selector `FC3E`, then `821E`, then exact helper `F28D` with `X = 3390`, `Y = 0402`.
- Runs exact full-span settlement sweep `A1B2`, then `821E`, then `86DD`, then exact one-shot materializer `A22F`.
- Sets `0D13 = 64` and increments `0D15`.
- Copies exact `0x0007` bytes from `FF:CBAC` to `7E:94C8`, runs exact shared helper `9E76`, then runs exact masked strip exporter `A0E7` with `Y = 9500`.
- Strongest safe reading: exact clamp/bootstrap wrapper for this corrected settlement/materializer caller family.

### C2:A0E7..C2:A0F6  ct_c2_masked_strip_exporter_from_9480_plus_51_to_destination_y   [strong]
- Starts at `X = 51`.
- Reads words from `9480 + X`.
- Right-shifts each word once, masks by exact word `3DEF`, and stores the result to `Y`.
- Advances by exact word stride until `X == 0030`.
- Strongest safe reading: exact masked strip exporter from `9480 + 51` to the caller-supplied destination buffer in `Y`.

### C2:A970..C2:AA05  ct_c2_decrement_by_6_fill_and_wram_2180_stream_updater_for_5cc2_and_5d42   [strong structural]
- Subtracts exact step `0006` from `5CC2`, masks with `01FF`, retags with `6000`, and propagates the result across `5CC2..5CD8`.
- Subtracts exact step word `0DAB` from `5D42`, masks with `01FF`, retags with `6000`, and propagates the result across `5D42..5D58`.
- Sets WRAM stream address through `$2181 = 969A` and `$2183 = 7E`.
- Advances `22 += 6` and then moves the trailing bound down by `6` through `26` or `24`.
- Emits four exact `$2180` write groups through helper `AA19`.
- Finishes by writing `00` to `$2180`.
- Strongest safe reading: exact decrement-by-6 fill updater plus WRAM `$2180` stream writer for the `5CC2/5D42` family.

### C2:AA19..C2:AA30  ct_c2_triplet_emitter_to_2180_using_a_and_00_01_with_split_negative_path   [strong]
- For nonnegative `A`, writes exact triplet `A`, `$00`, `$01` to `$2180`.
- For negative `A`, first writes exact triplet `(A + 1) & 7F`, `$00`, `$01`, then writes a second exact triplet with leading byte `7F`.
- Strongest safe reading: exact `$2180` triplet emitter with a split negative-value path.

### C2:AFED..C2:B044  ct_c2_three_row_settlement_packet_loop_with_b045_word_table_and_0d5d_gate   [strong structural]
- Seeds `61 = 3580`, clears `7D`, and clears `71`.
- Repeatedly runs exact settlement/search service `8820`.
- Exits when `51 != 0`.
- Otherwise runs exact selector/threshold gate `A1EF` and exact common tail `ED31` with `X = BE0E`.
- Runs exact helper `F626` from `9A90`.
- Loads exact word from table `B045 + 2*71` into packet field `180E,Y`.
- Advances `61 += 0140`.
- Clears packet field `1818,Y`.
- Writes packet field `1811,Y` as `00` when `0D5D == 0`, else `12`.
- Increments `71` and loops while `71 < 73`.
- Finishes through exact service selector `FBEA`.
- Strongest safe reading: exact three-row settlement packet loop with the `B045` word table and `0D5D` gate.

### C2:B045..C2:B04A  ct_c2_three_entry_word_table_for_afed_settlement_packet_loop   [strong]
- Exact word table consumed by `AFED..B044` as `B045 + 2*71`.
- Current loop structure shows the first three entries are the live row-selector words for that packet loop.
- Strongest safe reading: exact three-entry word table for the `AFED` settlement packet loop.

### C2:BA2F..C2:BA4E  ct_c2_post_compare_gate_writing_0d5e_and_emitting_ed31_c01f   [strong structural]
- Runs exact selector/threshold gate `A1EF`.
- Clears `0D5E`.
- Compares `9A97` against `9890`.
- When `9A97 < 9890`, forces `0D5E = 4`.
- Clears `7E`.
- Runs exact common service `ED31` with `X = C01F`.
- Strongest safe reading: exact BA-side post-compare gate writing `0D5E` and emitting common tail selector `C01F`.

### C2:BA4F..C2:BAFB  ct_c2_capped_iterative_settlement_loop_with_bafc_ba2f_tails_and_hardware_math_finalizer   [strong structural]
- Runs exact front helper `F566`.
- Sets `19D8 = FF`.
- Clamps local loop-count byte `24 = min(3, 85)` and clears `25`.
- Seeds `71 = 041A`, clears `22`, clears `7D`, and seeds `61 = 2ECA`.
- Repeatedly runs exact settlement/search service `8820`.
- Exits the main loop when `51 != 0`.
- On each accepted pass, runs exact selector packet row builder `BAFC`, clears `9890`, runs exact compare gate `BA2F`, advances `61 += 0180`, increments `71`, and increments `22`.
- Continues while `22 < 24`.
- Then emits exact common tail `ED31` with `X = C030` for each remaining row.
- Finishes through an exact hardware-math finalizer that writes `09AA` to `$4204`, sets `0DDB = 0B`, runs `EA81` with `Y = 85`, seeds `0D92 = 1278`, and captures `$4216` into `0D95` and `0D94`.
- Strongest safe reading: exact capped iterative settlement loop with `BAFC/BA2F` tails and a hardware-math finalizer.

### C2:BAFC..C2:BB19  ct_c2_selector_packet_row_builder_with_bb1a_byte_table   [strong]
- Runs exact helper `F626` from the caller-supplied selector in `A`.
- Writes the returned selector byte to packet field `1800,Y`.
- Clears packet field `1818,Y`.
- Writes exact constant `1C` to packet field `180F,Y`.
- Uses exact byte table `BB1A + 22` for packet field `180E,Y`.
- Strongest safe reading: exact selector packet row builder using the `BB1A` byte table.

### C2:BB1A..C2:BB1C  ct_c2_three_entry_byte_table_for_bafc_selector_packet_rows   [strong]
- Exact byte table consumed by `BAFC` as `BB1A + 22`.
- Current main-loop usage shows the first three entries are the live row-selector bytes for `22 = 0/1/2`.
- Strongest safe reading: exact three-entry byte table for the BA-side selector packet rows.

### C2:BEE6..C2:BF2E  ct_c2_settlement_row_packet_loop_with_inline_threshold_compare_and_bf2f_word_table   [strong structural]
- Repeatedly runs exact settlement/search service `8820`.
- Exits when `51 != 0`.
- Otherwise runs exact selector/threshold gate `A1EF` and exact common tail `ED31` with `X = C056`.
- Runs exact helper `F626` from `9A90`.
- Loads exact word from table `BF2F + 2*71` into packet field `180E,Y`.
- Advances `61 += 0100`.
- Compares exact threshold word `0D38,X` against `9A93`.
- Clears packet field `1818,Y`.
- Writes packet field `1811,Y` as `00` when `0D38,X < 9A93`, else `12`.
- Increments `71` and continues while `71 != 73`.
- Strongest safe reading: exact settlement row packet loop with an inline threshold compare and the `BF2F` word table.

### C2:BFD4..C2:BFFE  ct_c2_selector_indexed_indirect_dispatch_wrapper_latching_54_into_0417_then_running_c4bc_c3e4_and_fbe3   [strong structural]
- Clears accumulator high byte with `TDC`.
- Latches selector `54 -> 0417`.
- Doubles that selector and uses it as exact index into a jump table rooted at `BFFF`.
- Runs one exact jump-table-selected worker through `JSR ($BFFF,X)`.
- Restores the latched selector into `7F`.
- Then runs fixed tail helpers:
  - `C4BC`
  - `C3E4`
  - `8385` with `X = FBE3`
- Conditionally runs `EAC2` when `0D1D` is negative.
- Strongest safe reading: exact selector-indexed indirect dispatch wrapper behind the `BEEF/BFxx` helper family.

## Caution-strengthened outputs

### 7E:0DAB  ct_c2_step_word_used_by_9daf_ramp_and_a970_fill_updater   [caution strengthened]
- `9DAF..9E75` clears `0DAB`, then repeatedly accumulates it by exact step word `0D22` during the 12-step ramp.
- `A970..AA05` subtracts exact step word `0DAB` from `5D42` before retagging and propagating that fill.
- Strongest safe reading: exact step word shared by the `9DAF` ramp and the `A970` fill updater.

### 7E:0D24  ct_c2_exact_12_step_countdown_for_9daf_ramp_loop   [caution strengthened]
- `9DAF..9E75` seeds `0D24 = 000C`.
- Decrements it once per ramp iteration and exits the loop exactly when it reaches zero.
- Strongest safe reading: exact 12-step countdown word for the `9DAF` ramp loop.

### 7E:0D5E  ct_c2_ba_side_post_compare_result_byte_for_ba2f_gate   [caution strengthened]
- Cleared at the front of `BA2F`.
- Forced to `04` when `9A97 < 9890`.
- Strongest safe reading: BA-side post-compare result byte for the `BA2F` gate.

### 7E:0FC4  ct_c2_clamp_byte_max_85_minus_3_used_to_limit_0413   [caution strengthened]
- `A051..A0E6` computes `0FC4 = max(85 - 3, 0)`.
- Then clamps `0413` downward to that byte when needed.
- Strongest safe reading: exact clamp byte used to limit `0413` inside the `A051` bootstrap wrapper.

## Honest remaining gap

This pass materially advanced the same-bank caller seam, but it did not finish the whole `C2` pocket.

The real next seam is now:
- the broader `A886..AA30` family that still needs a cleaner top-level noun and better worker/table ownership
- the `B04C..B05D` helper/table family behind `AFED..B044`
- the `BF2F..BFFF` table-and-worker family behind `BEE6..BFFE`
- stronger nouns for the newly strengthened WRAM outputs:
  - `0DAB`
  - `0D24`
  - `0D5E`
  - `0FC4`
