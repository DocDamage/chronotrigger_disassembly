# Chrono Trigger Labels — Pass 129

## Purpose

Pass 129 closes the final continuation-family descriptor/entry seam at `C2:BECE..C2:BEE5` and the downstream post-substitution dispatch-target seam at `C2:CA67..C2:CC0D`.

## Strong labels

### C2:BECE..C2:BED4  ct_c2_first_local_selector_descriptor_packet_for_be79_three_packet_tail   [strong]
- Exact 7-byte local descriptor emitted by `BE79` through exact helper `8385`.
- Exact bytes: `40 58 80 2E 7E 00 02`.
- Strongest safe reading: exact first local selector descriptor packet for the three-packet `BE79` tail.

### C2:BED5..C2:BEDB  ct_c2_second_local_selector_descriptor_packet_for_be79_three_packet_tail   [strong]
- Exact 7-byte local descriptor emitted by `BE79` through exact helper `8385`.
- Exact bytes: `00 5C 00 36 7E 00 04`.
- Strongest safe reading: exact second local selector descriptor packet for the three-packet `BE79` tail.

### C2:BEDC..C2:BEE5  ct_c2_seeded_entry_stub_setting_61_3662_and_clearing_71_before_falling_into_bee6   [strong structural]
- Exact called entry is `BEDC` from the already-frozen `BE79` owner.
- Begins with exact `PHP ; REP #$30`.
- Seeds exact packet base word `61 = 3662`.
- Clears exact row/index word-byte `71 = 0000`.
- Falls directly into the already-frozen `BEE6` settlement row packet loop.
- Strongest safe reading: exact seeded entry stub that initializes the `BEE6` row-loop state before falling through into that proven loop.

### C2:CA67..C2:CAD8  ct_c2_first_ca63_dispatch_target_seeding_020c_020d_020f_copying_9600_to_9580_running_f422_and_filling_334c_33cc_then_cad9_dispatch   [strong structural]
- Exact dispatch target selected through exact local table `CA63`.
- Runs exact selector packet `ED31` with exact selector word `BF05`.
- Seeds exact base word `61 = 2E00`.
- Writes exact byte `020C = 04`, or exact byte `020C = 05` when exact word `0D7C != 0`.
- Writes exact word `0DC5 = 5E00`, exact word `020D = CF3B`, and exact byte `020F = FF`.
- Runs exact helper `F905`.
- Copies exact `0x0018` bytes from exact block `9600 -> 9580`.
- Temporarily switches direct page to exact `19C0`, seeds exact local parameters `00/01 = 0148`, `0E = 20CA`, `1A = 20`, and runs exact helper `F422`.
- In 16-bit mode runs exact helper `FBB4` twice to write exact values `0100` into exact base `334C` and `0121` into exact base `33CC`.
- Emits exact local descriptor `CAD9` through exact helper `8385`.
- Strongest safe reading: exact first dispatch target behind `CA63`, owning the `020C/020D/020F` seed lane, the `9600 -> 9580` local copy, the `19C0` direct-page helper setup, the `334C/33CC` fill pair, and the exact `CAD9` descriptor emit.

### C2:CAD9..C2:CADF  ct_c2_local_selector_descriptor_packet_for_the_ca67_dispatch_target   [strong]
- Exact 7-byte local descriptor emitted by `CA67` through exact helper `8385`.
- Exact bytes: `00 10 00 5E 7E 00 10`.
- Strongest safe reading: exact local selector descriptor packet for the `CA67` dispatch target.

### C2:CAE0..C2:CAE5  ct_c2_second_ca63_dispatch_target_wrapper_loading_bf48_and_tail_jumping_ed31   [strong structural]
- Exact dispatch target selected through exact local table `CA63`.
- Loads exact selector word `BF48` into `X`.
- Tail-jumps exact helper `ED31`.
- Strongest safe reading: exact second dispatch-target wrapper behind `CA63`, reduced to a fixed `BF48 -> ED31` tail-jump.

### C2:CAE6..C2:CAF2  ct_c2_php_wrapped_mode_01_wrapper_setting_0d13_then_running_f643   [strong]
- Exact body: `PHP ; SEP #$20 ; LDA #$01 ; STA 0D13 ; JSR F643 ; PLP ; RTS`.
- Strongest safe reading: exact `0D13 = 01` wrapper around the fixed `F643` call.

### C2:CAF3..C2:CB8B  ct_c2_post_substitution_owner_running_bf7b_984a_cc4f_math_setup_a0e7_c805_then_fbe3_fc37_fbff   [strong structural]
- Begins with exact `PHP ; SEP #$20`.
- Runs exact selector packet `ED31` with exact selector word `BF7B`.
- Runs exact helper `984A`.
- Seeds exact byte `0D13 = 01` and exact word `0D0E = 01F0`.
- Runs exact helpers `F5A7` and `CC4F`, then increments exact byte `0D15`.
- When exact byte `0D36 != 0`, writes exact byte `38` into exact bytes `9380`, `9386`, and `938C`, then writes exact word `BF40 -> 9683`.
- Seeds exact math-register word `$4204 = A400`.
- Computes exact byte `0D94 = 0F0C - 04`; when the exact result is nonnegative, widens it into the exact `5*x` form, stores it back to exact byte `0D94`, derives a second exact `5*x` value into exact byte `0D95`, and runs exact helper `8B93`.
- Seeds exact word `0D92 = 12EC`, mirrors exact math result `$4214 -> 0D98`, runs exact helper `A0E7` with exact `Y = 9500`, then runs exact helper `C805`.
- Emits exact selector chain `FBE3 -> FC37 -> FBFF` through exact helper `8385` and exits `PLP ; RTS`.
- Strongest safe reading: exact post-substitution owner that refreshes the `BF7B` selector path, seeds `0D13/0D0E/0D15`, performs one exact `0F0C`-derived math/setup lane into `0D94/0D95/0D92/0D98`, then runs `A0E7`, `C805`, and the fixed `FBE3/FC37/FBFF` selector tail.

### C2:CB8C..C2:CBBE  ct_c2_0f0f_0f0e_owner_optionally_scheduling_cbbf_through_8249_and_using_cbf7_packet_seed   [strong structural]
- Clears exact latch byte `0F0F`.
- Tests exact bit `0x40` from exact long byte `7F:01CF`; when that exact bit is set, branches directly into the downstream exact poller body at `CBBF`.
- Otherwise loads exact byte `0F0E` from exact byte `02AE`, or from exact table `29AE,X` when exact word `0D32 != 0`.
- When exact byte `0F0E == 3E`, skips the scheduled path.
- Otherwise increments exact latch byte `0F0F`, seeds exact word `02 = 0108`, runs exact helper `CBF7`, then in 16-bit mode seeds exact callback pointer `A = CBBF`, exact delay/count `X = 0010`, and runs exact helper `8249`.
- Exits `RTS` when the immediate/scheduled work is armed.
- Strongest safe reading: exact `0F0F/0F0E` owner that either schedules or directly enters the downstream status-poller body rooted at `CBBF`.

### C2:CBBF..C2:CBEA  ct_c2_scheduled_status_poller_waiting_on_2141_then_emitting_143e_packet_and_jumping_8216   [strong structural]
- Waits until exact long hardware/status byte `002141 == 0`.
- Then writes exact packet bytes `1E00 = 14`, `1E01 = 3E`, seeds exact word `02 = FF01`, and runs exact helper `CBEB`.
- Loops until the exact low nibble of exact long hardware/status byte `002143` becomes nonzero.
- Exits through exact jump `8216`.
- Strongest safe reading: exact scheduled status-poller body that waits on exact long hardware/status bytes `2141/2143`, emits one staged exact `14/3E` packet, and then exits through `8216`.

### C2:CBEB..C2:CC0D  ct_c2_two_stage_1exx_packet_emitter_using_local_02_03_and_c70004   [strong structural]
- Seeds exact bytes `1E02 = 80` and `1E03 = 80`.
- Runs exact long helper `C7:0004`.
- Then seeds exact byte `1E00 = 81`.
- Mirrors exact local word `02/03` into exact packet bytes `1E01/1E02/1E03`.
- Runs exact long helper `C7:0004` again and exits `RTS`.
- Strongest safe reading: exact two-stage `1Exx` packet emitter that materializes the staged local `02/03` payload through exact helper `C7:0004`.

## Alias / wrapper / caution labels

## Honest remaining gap

- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B/0D8C/0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
- the next real code seam now moves naturally to `C2:CC0E..C2:CE85`
