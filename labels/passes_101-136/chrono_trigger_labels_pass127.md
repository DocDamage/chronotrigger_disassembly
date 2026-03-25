# Chrono Trigger Labels — Pass 127

## Purpose

Pass 127 closes the live post-substitution / descriptor-normalization seam at `C2:C7A6..C2:C946` and freezes the first exact continuation-family helper chain behind the newly closed `B6D3` owner.

## Strong labels

### C2:C7A6..C2:C7AB  ct_c2_three_word_local_dispatch_table_c7ac_c7e0_c6b9_for_the_post_substitution_family   [strong]
- Exact little-endian word entries: `C7AC`, `C7E0`, `C6B9`.
- Strongest safe reading: exact three-word local dispatch root for the downstream post-substitution / descriptor-normalization family.

### C2:C7AC..C2:C7DF  ct_c2_prep_scan_owner_mirroring_71_into_0d36_0d37_then_looping_c649_caf3_ce86_until_00c0_clears   [strong structural]
- Mirrors exact byte `71` into exact bytes `0D36/0D37`.
- Runs exact helper chain `CB8B -> C9E5`, forces exact index `X = 00`, and runs exact helper `C649`.
- In 16-bit X, loops exact helper chain `CAF3 -> CE86` until exact word `00C0` clears; when the exact word is still nonzero, reruns exact helper `821E` and repeats.
- When the exact word clears, writes exact byte `9689 = 17`, runs exact helper `CE9D`, and exits through exact jump `83B2`.
- Strongest safe reading: exact prep/scan owner that selects the next clear slot and repeatedly advances the shared descriptor machinery until exact word `00C0` clears.

### C2:C7E0..C2:C804  ct_c2_0d1d_gated_sibling_dispatcher_choosing_c805_c674_or_cc0e_82b2   [strong structural]
- Runs exact helper `E984` and tests exact status byte `0D1D`.
- Clear path runs exact helper `C805`; when exact byte `81 != 54`, reruns exact helper `EAC2`; otherwise returns.
- Negative path tests exact byte `0F0D`; when exact bit `0x40` is set, returns immediately; otherwise exits through exact jump `C674`.
- Overflow path runs exact helper `CC0E` and exits through exact jump `82B2`.
- Strongest safe reading: exact sibling `0D1D`-gated dispatcher above the `C805` normalization owner.

### C2:C805..C2:C85A  ct_c2_post_selection_normalization_owner_optionally_recentering_via_c85b_then_scanning_0f02_for_clear_high_bits   [strong structural]
- Clears exact byte/word `0D9E`.
- When exact byte `0F0C >= 05` and exact control byte `5A` is negative, runs exact local helper `C85B`.
- When exact OR-combine `0F0B | 0F0C` is zero, clears exact selector byte `54` and seeds exact mode byte `80 = 40`.
- Otherwise builds exact index `X` from exact selector byte `54` (plus exact mode byte `80` when `54 >= 03`) and loops exact helper `C9AE` until exact byte `0F02[X] & C0 == 0`.
- Stores the exact selected state into exact byte `0F0D`, runs exact helper `C973`, clears exact bit `0x04` in exact word/byte `0D13`, mirrors exact selector `54 -> 7F`, computes exact byte `56`, and exits through exact selector `FC37 -> 8385`.
- Strongest safe reading: exact post-selection normalization owner above the new `C85B/C88D` reseed helpers.

### C2:C85B..C2:C88C  ct_c2_bit3_gated_reseed_helper_setting_54_eq_03_and_signed_step_0d22_eq_fff8_before_c8ba   [strong structural]
- Requires exact control bit `5A.bit3`.
- Seeds exact selector byte `54 = 03`.
- When exact byte `80 != 00`, decrements exact byte `80`.
- Writes exact byte `0D9E = D0`.
- In 16-bit mode seeds exact word `24 = 2613`, exact signed step word `0D22 = FFF8`, and exact word `22 = 000E`.
- Runs exact shared helper `C8BA`.
- Strongest safe reading: exact reseed/setup helper for the descending/signed-step `C8BA` lane.

### C2:C88D..C2:C8B9  ct_c2_threshold_reseed_helper_setting_54_eq_06_and_signed_step_0d22_eq_0008_before_c8ba   [strong structural]
- Computes exact threshold byte `00 = 0F0C - 03`.
- Seeds exact selector byte `54 = 06`.
- Repeatedly increments exact byte `80` until exact byte `80 + 1 >= 0F0C - 03`.
- Writes exact byte `0D9E = 30`.
- In 16-bit mode seeds exact word `24 = 2013`, exact signed step word `0D22 = 0008`, and exact word `22 = 0010`.
- Runs exact shared helper `C8BA`.
- Strongest safe reading: exact reseed/setup helper for the ascending/signed-step `C8BA` lane.

### C2:C8BA..C2:C946  ct_c2_shared_six_step_staged_builder_adjusting_0d9e_0d95_through_c949_then_clearing_0d22_and_0d9e   [strong structural]
- Computes exact compare byte `71 = (54 - 03) + 80 + 73`, runs exact helper `8820`, and then exact helper `CD9B`.
- Sets exact bit `0x04` in exact word/byte `0D13`.
- In 16-bit mode seeds exact `EF05` parameter words `61 = 2E00`, `5B = 0213`, `5D = 24`, and `5F = 180A`, then runs exact helper `EF05`.
- Clears exact word `0DAB`, seeds exact loop word `0D24 = 0006`, and adjusts exact byte/word `25` from the sign of exact word `0D22`.
- Subtracts exact signed step word `0D22` from exact word `0D9E`; when the subtract borrows, net-decrements exact word `0D95`.
- Runs exact helper `C949`, reseeds exact `EF05` parameters as `61 = 2E00`, `5B = 24`, and `5D = 0213`, reruns exact helper `EF05`, and emits exact selector `FBE3 -> 8385`.
- Repeats while exact loop word `0D24` remains nonzero, rerunning exact helper `821E` between iterations.
- Final phase clears exact words `0D9E` and `0D22`, runs exact helpers `CDE3` and `EAC2`, restores flags, and returns.
- Strongest safe reading: exact shared six-step staged builder/finalizer for the `C805` family.

### C2:BB1F..C2:BBCF  ct_c2_three_row_continuation_packet_owner_using_bbd6_bc22_bafc_ba2f_and_fbe3   [strong structural]
- Exact called entry is `BB1F`; the preceding byte at `BB1E` is not the called entry point.
- Front phase runs exact helpers `BBD6` and `BC22`, mirrors the returned exact threshold/value byte into exact byte `0F6F`, compares exact byte `9A97` against exact word/byte `9890`, and conditionally writes exact byte `7E = 04`.
- Copies exact `0x0019` bytes from exact source block `2F9A` into exact destination block `9890` through exact helper `F114`.
- Hardware/setup lane rewrites exact words `0D95/0D94` through exact helper `8BA6` from exact bytes `0F4A/0F49`, seeds exact word `0D92 = 32E8`, reruns exact helper `BBD6`, seeds exact packet base `61 = 2ECA`, mirrors exact byte `17 -> 0F51`, and clears exact byte `7D`.
- Exact row loop either emits exact selector packet `C030 -> ED31` for negative entries in exact byte lane `16,X`, or else runs exact helper `8816`, exact packet-row helper `BAFC`, exact helper `BC22`, mirrors the result into exact byte lane `0F6F[X]`, and runs exact compare gate `BA2F`.
- Advances exact packet base `61 += 0180`, increments exact row counter `71`, and repeats while `71 < 0003`.
- Finishes through exact selector `FBE3 -> 8385`.
- Strongest safe reading: exact three-row continuation packet owner behind the helper slot consumed by the pass-126 `B6D3` owner.

### C2:BBD6..C2:BC20  ct_c2_continuation_mask_expander_deriving_0f4c_then_expanding_fff9bb_mask_bits_into_17_slots   [strong structural]
- Seeds exact word `17 = FFFF` and runs exact helper `F566`.
- Builds exact index `X = 0F48 + 0F4A`, loads exact byte `0F00[X] -> 0F4C`, then uses exact byte `0F30[X]` to index exact table `CC:2963`.
- Combines exact bytes `0419 + 041A` with exact table `0D5F` to derive a second exact index.
- Loads one exact bitmask byte from exact table `FF:F9BB`, repeatedly shifts it through exact local byte `00`, and whenever a mask bit is set writes the current exact slot byte into exact byte lane `17,X`.
- Strongest safe reading: exact continuation helper that derives `0F4C`, selects one exact mask byte, and expands that exact mask into the live exact row-index list at `17..`.

### C2:BC22..C2:BC58  ct_c2_threshold_lookup_helper_combining_0418_9a8f_and_0f4c_then_loading_cc253b_through_bc59_into_9890   [strong structural]
- When exact byte `0418 == 00`, uses exact byte `0F4C` directly as its base index.
- Otherwise uses exact high nibble `9A8F & 0F00`, shifts it down, combines it with exact byte `0F4C` through the stack, then uses exact table `1607` to derive a second exact index.
- Loads one exact value from exact table `CC:253B`, runs exact helper `BC59`, and writes the result into exact word/byte `9890`.
- Strongest safe reading: exact threshold/value lookup helper consumed by the continuation-family owners at `BB1F`, `B427`, and `BE8B`.

### C2:BC59..C2:BC70  ct_c2_conditional_quarter_round_up_helper_for_the_bc22_threshold_value_when_9aba_is_a2_or_a3   [strong]
- Tests exact byte `9ABA`.
- When the exact byte is `A2` or `A3`, quarter-scales the exact accumulator through two rounds of `LSR` with carry compensation.
- Otherwise returns the exact accumulator unchanged.
- Strongest safe reading: exact conditional quarter-round-up helper for the `BC22` threshold/value byte.

## Alias / wrapper / caution labels

## Honest remaining gap

- the wider continuation-family seam remains open after the newly closed helper root, especially beyond `C2:BC71..C2:BEE5`
- the next post-substitution/helper seam remains open after the newly closed staged builder, especially beyond `C2:C947..C2:CA40`
- broader gameplay/system nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B/0D8C/0D90`
- the broader top-level family noun for `C2:A886..AA30` is still not tight enough
