# Chrono Trigger Labels — Pass 144

## Purpose

Pass 144 closes the callable/helper family that pass 143 left open at `C2:E60B..C2:E760`, with the structural correction that the seam begins with an exact local 4-word dispatch table and actually runs cleanly through `C2:E840`.

## Strong labels

### C2:E60B..C2:E612  ct_c2_local_4_word_dispatch_table_e613_e61b_e6ae_e705   [strong]
- Exact words: `E613`, `E61B`, `E6AE`, `E705`.
- Strongest safe reading: exact local 4-word dispatch table for the four downstream callable entries resolved in this pass.

### C2:E613..C2:E61A  ct_c2_short_wrapper_calling_e7c3_then_incrementing_68_then_jumping_83b2   [strong structural]
- Runs exact helper `E7C3`.
- Increments exact byte `68`.
- Exits through exact jump `83B2`.
- Strongest safe reading: exact short wrapper into the downstream exact setup/export owner.

### C2:E61B..C2:E682  ct_c2_0420_0d1d_gated_dispatcher_with_e891_fast_lane_fffaa3_negative_lane_and_956e_307fe1_e841_service_lane   [strong structural]
- When exact byte `0420 == 30` and exact selector byte `54 < 03`, seeds exact byte `68 = 03`, reruns exact helper `EAC2`, and exits through exact jump `E891`.
- Otherwise runs exact helper `E984`, then on the clear lane runs exact helper `E743`, compares exact bytes `81` and `54`, reruns exact helper `EAC2` only on mismatch, and returns.
- Negative lane always reruns exact helper `EAC2`.
- Negative exact `54 < 03` path mirrors exact byte `54 -> 79` and `54 -> 0414`, runs exact long helper `FF:FAA3`, and rejoins the shared exact `E694` service tail.
- Negative exact `54 >= 03` path runs exact helper `956E`, seeds exact long byte `7F:0061 = 01`, mirrors exact long byte `30:7FE1 -> 299E`, and either:
  - clears exact byte `0D4C`, runs exact helper `E841`, and increments exact byte `68` when exact long byte `30:7FE2 != 0` and exact byte `9392 == 78`
  - or falls through the shared exact `E683` service tail otherwise.
- Strongest safe reading: exact front dispatcher combining one exact `0420 == 30` fast lane, one clear exact `E743` compare lane, and a negative exact service lane split between exact `FF:FAA3` and exact `956E / 30:7FE1 / E841`.

### C2:E683..C2:E6AD  ct_c2_shared_slot_scan_immediate_1e00_1e01_packet_emitter_c70004_service_tail_and_0d00_to_29ad_mirror   [strong structural]
- Scans exact slot bytes `0D49[0..2]` for the first exact nonzero entry; falls back to exact slot `00` when none are set.
- Mirrors the chosen exact slot index into exact byte/word `0414`.
- Seeds exact bytes `1E00 = F3` and `1E01 = (2990 & 08)`.
- Runs exact long helper `C7:0004`.
- Mirrors exact byte `0D00 -> 29AD`.
- Exits through exact jump `8320`.
- Strongest safe reading: exact shared slot-scan / immediate packet emitter plus exact `C70004` service tail.

### C2:E6AE..C2:E6DC  ct_c2_sibling_0d1d_gated_dispatcher_with_fffaed_negative_lane_shared_e683_tail_and_e6df_overflow_handoff   [strong structural]
- Begins `JSR E984 ; BIT 0D1D`.
- Clear / non-overflow path runs exact helper `E743`, compares exact bytes `81` and `54`, reruns exact helper `EAC2` only on mismatch, and returns.
- Negative lane reruns exact helper `EAC2`, then:
  - exact `54 >= 03` exact-jumps into shared service tail `E683`
  - exact `54 < 03` mirrors exact byte `54 -> 79` and `54 -> 0414`, runs exact long helper `FF:FAED`, and exact-jumps into shared exact `E694` packet/service tail
- Overflow path hands off into exact wrapper `E6DF`.
- Strongest safe reading: exact sibling `0D1D`-gated dispatcher around the same shared exact service tails.

### C2:E6DF..C2:E704  ct_c2_overflow_clear_reset_wrapper_decrementing_68_0d4c_zeroing_52c0_band_clearing_0d84_then_emitting_fc1b   [strong structural]
- Reruns exact helper `EAC2`.
- Decrements exact bytes `68` and `0D4C`.
- Forces exact selector byte `54 = 03`.
- Zeroes the exact `52C0`-family work band through exact overlapping same-bank clear-propagation move `52C0 -> 52C2` for exact length `00FD`.
- Clears exact byte/word `0D84`.
- Emits exact selector `FC1B` through exact helper `8385`.
- Strongest safe reading: exact overflow clear/reset wrapper.

### C2:E705..C2:E742  ct_c2_0d1d_gated_service_owner_forcing_54_05_on_overflow_optionally_running_e8b7_then_setting_0d13_5b_and_exiting_fc0d   [strong structural]
- Begins `JSR E984 ; BIT 0D1D`.
- Clear / non-overflow path compares exact bytes `54` and `81`, reruns exact helper `EAC2` only on mismatch, and returns.
- Overflow path forces exact selector byte `54 = 05`.
- Shared negative/overflow lane emits exact selector `C191`, optionally runs exact helper `E8B7` when exact selector byte `54 == 04`, seeds exact byte `0D13 = 5B`, mirrors exact byte `0F00 -> 54`, seeds exact byte `68 = 01`, reruns exact helper `EAC2`, and exits through exact selector `FC0D`.
- Strongest safe reading: exact `0D1D`-gated service owner for the negative/overflow lane.

### C2:E743..C2:E7C2  ct_c2_cyclic_occupied_slot_search_state_refresh_and_strip_expansion_owner_using_5a_bit3_then_d36c_fbdc_fc0d_fc29   [strong structural]
- Repeatedly probes exact slot bytes `0D49[54]` until one exact nonzero slot is found.
- Uses exact bit test `5A & 08` to choose whether the exact cyclic slot step is `+1 mod 4` or `-1 mod 4`.
- When exact long byte `30:7FE2 != 0`, exact selector byte `54 == 03`, and exact low bits `5A & 03 != 0`, flips exact byte `9392 ^= 70` and reruns exact helper `EAC2`.
- Mirrors exact byte `54 -> 79`, derives exact next-slot byte `7F = (54 + 1) & 03`, and runs exact helper `CFFB`.
- Rebuilds and shifts the exact `3200` strip, expands exact downstream buffers `5248/5288`, runs exact helper `D36C`, and emits exact selector chain `FBDC -> FC0D -> FC29`.
- Strongest safe reading: exact cyclic occupied-slot search / state-refresh / strip-expansion owner.

### C2:E7C3..C2:E840  ct_c2_307fe0_indexed_setup_export_owner_running_d10d_d36c_e743_staging_cc74_to_94c0_ce30_to_9560_then_emitting_fc53_fbce_fbf8_fc14   [strong structural]
- Emits exact selector `C0ED` through exact helper `ED31` and runs exact helper `D10D`.
- Mirrors exact long byte `30:7FE0 -> 79`.
- ORs exact slot bytes `0D49 / 0D4A / 0D4B`; when they are all zero, forces exact slot byte `79 = 03`.
- Mirrors exact byte `79 -> 54`, runs exact helper `D36C`, clears exact byte `7E`, emits exact selector `C322`, and runs exact helper `E743`.
- Runs exact helper `86DD`.
- When exact long byte `30:7FE2 != 0`, emits exact selector `C36B`.
- Increments exact byte `0D15`, seeds exact byte `0D13 = 1B`, stages exact blocks `FF:CC74 -> 94C0` and `FF:CE30 -> 9560`, and emits exact selector chain `FC53 -> FBCE -> FBF8 -> FC14`.
- Strongest safe reading: exact `30:7FE0`-indexed setup/export owner for the downstream refresh/export lane.

## Honest remaining gap

- the old seam `C2:E60B..C2:E760` is now closed more honestly as `C2:E60B..C2:E840`
- the old seam start at `C2:E60B` was not one strange code opener; it begins with an exact local 4-word dispatch table at `C2:E60B..C2:E612`
- the old seam end at `C2:E760` cut the exact `E743` owner in half
- the next clean follow-on family now begins at `C2:E841`
