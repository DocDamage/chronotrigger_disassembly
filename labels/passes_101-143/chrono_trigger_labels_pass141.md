# Chrono Trigger Labels — Pass 141

## Purpose

Pass 141 closes the exact follow-on callable/helper family that pass 140 left open at `C2:DF76..C2:E095`, with the same structural correction again: the old seam end was short. The exact callable/helper closure here runs through `C2:E162` and resolves into one shared threshold-recovery owner, one local 5-word selector table, three shared wrappers/helpers, one `104D`-window export owner, one shared bounded export helper, one negative refresh/export owner, one short marker/finalizer wrapper, one cyclic selector-step owner, and one short latched-selector marker-writer wrapper.

## What this pass closes

### C2:DF76..C2:DFC4  ct_c2_shared_threshold_recovery_owner_using_7c00_dfc5_e001_and_fc3e_tail   [strong structural]
- Begins `PHP ; SEP #$30`.
- Loads exact byte `7C00[04C9] -> 0D4D`, snapshots exact byte `54 -> 7F`, and seeds exact byte `54 = 0A`.
- Reenters exact `REP #$30`, seeds exact word `5D5A = 216F`, and uses overlapping exact `MVN 7E,7E` from `5D5A -> 5D5C` with exact count `001D`, yielding a repeated exact `216F` work band downstream in exact `5D5x`.
- Runs exact helper `F2DC` from exact `X = 3BDE` and exact byte `04C9`, then always exact shared helper `E001`.
- Reruns exact helper `8881` from exact byte `04C9`.
- Uses exact local table `DFC5` keyed by exact word `04CC` to load one exact selector root and emits it through exact helper `ED31`.
- Finishes through exact selector tail `X = FC3E ; JSR 8385`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact shared threshold-recovery owner that snapshots exact byte `7C00[04C9]` into `0D4D`, saves exact selector context through exact byte `7F`, seeds a repeated exact `216F` work band in `5D5A..`, reruns exact shared helper `E001`, emits one exact selector chosen from exact local table `DFC5`, and exits through exact selector `FC3E`.

### C2:DFC5..C2:DFCE  ct_c2_local_five_word_selector_table_for_df76_keyed_by_04cc   [strong structural]
- Exact words: `C2E8, C2F5, C2F5, C302, C302`.
- Strongest safe reading: exact local 5-word selector table keyed by exact word `04CC` for the exact `DF76` owner.

### C2:DFCF..C2:E000  ct_c2_shared_restore_clear_import_helper_using_7f_5d5a_f114_fc3e_and_fbe3   [strong structural]
- Begins `PHP`.
- Restores exact byte `7F -> 54`.
- Reenters exact `REP #$30`, clears exact word `5D5A`, then uses overlapping exact `MVN 7E,7E` from `5D5A -> 5D5C` with exact count `001D`, yielding an exact zero-filled downstream exact `5D5x` work band.
- Stores exact word `FFFF -> 83` after the exact block-copy count exhausts.
- Seeds exact `X = 3046`, exact `Y = 2C53`, exact source descriptor `A = 7E63`, and runs exact helper `F114`.
- Emits exact selectors `FC3E` and `FBE3` through exact helper `8385`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact shared restore/clear/import helper that restores exact selector byte `54`, zero-fills the exact `5D5x` work band, seeds exact word `83 = FFFF`, imports one exact block through exact helper `F114`, and exits through exact selectors `FC3E` then `FBE3`.

### C2:E001..C2:E011  ct_c2_shared_selector_packet_wrapper_emitting_c2de_then_fbea   [strong structural]
- Begins `PHP ; REP #$30`.
- Emits exact selector `C2DE` through exact helper `ED31`.
- Emits exact selector `FBEA` through exact helper `8385`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact shared selector-packet wrapper that emits exact selector `C2DE` and then exact selector `FBEA`.

### C2:E012..C2:E016  ct_c2_shared_direct_tail_wrapper_loading_51_then_jumping_f2f3   [strong structural]
- Loads exact accumulator from exact word `51`.
- Tail-jumps directly to exact helper `F2F3`.
- Strongest safe reading: exact one-shot direct tail wrapper that forwards exact word `51` into exact helper `F2F3`.

### C2:E017..C2:E057  ct_c2_104d_window_export_owner_using_79_1055_f628_e058_and_c2d5   [strong structural]
- Begins `PHP ; SEP #$20`.
- Snapshots exact byte `54 -> 80`, seeds exact byte `68 = 06`, and mirrors exact byte `79 -> 54`.
- Seeds exact direct-page exact word `02 = 1004` and exact loop index `04 = 85`.
- Walks compact exact list `104D[04]` until the exact negative terminator or exact bound `04 == 1055`.
- Per exact live entry, stages exact entry `104D[04] -> 00`, runs exact helper `FFF628`, mirrors exact loop index `04 -> 00`, and runs exact shared helper `E058`.
- Finishes by emitting exact selectors `C2D5` and `FBE3`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact `104D`-window export owner that walks the compact exact `104D` list from exact start index `85` up to exact bound `1055`, runs exact helper `FFF628` on each live entry, materializes the matching exact `3404` row slot through exact helper `E058`, and exits through exact selectors `C2D5` then `FBE3`.

### C2:E058..C2:E071  ct_c2_shared_row_pointer_helper_mapping_00_to_3404_plus_8x_and_calling_ec93   [strong structural]
- Begins `PHP ; REP #$30`.
- Maps exact byte `00` to exact row base `3404 + 8*00` and stores the exact result into exact word `61`.
- Seeds exact `X = 0002`, loads exact descriptor word `02`, and runs exact helper `EC93`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact shared row-pointer helper that maps exact byte `00` to exact destination base `3404 + 8*00`, stages that exact row base into exact word `61`, and then runs exact helper `EC93` from exact descriptor word `02`.

### C2:E072..C2:E0A4  ct_c2_shared_bounded_104d_export_helper_from_51_to_85_using_e058_and_f628   [strong structural]
- Begins `PHP ; SEP #$20`.
- Seeds exact byte `22 = 51` and snapshots exact byte `03 -> 05`.
- When exact byte `22 == 71`, clears exact byte `03` for that exact slot pass.
- Per exact slot, stages exact byte `22 -> 00`, runs exact shared helper `E058`, stages exact byte `104D[22] -> 00`, and runs exact helper `FFF628`.
- Restores exact byte `05 -> 03`, increments exact byte `22`, and loops while exact byte `22 < 85`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact shared bounded export helper that iterates exact slot byte `22` from exact start `51` up to exact bound `85`, temporarily clears exact byte `03` only on the exact slot matching exact byte `71`, materializes one exact `3404` row through exact helper `E058`, and then stages the matching exact compact-list entry `104D[22]` through exact helper `FFF628`.

### C2:E0A5..C2:E0F0  ct_c2_negative_refresh_export_owner_using_71_eq_54_minus_0c_c309_3664_e0f1_and_e072   [strong structural]
- Begins `PHP ; REP #$30`.
- Clears exact local work band `0D4D..0D51` through exact `STZ 0D4D` plus overlapping exact `MVN 7E,7E` from `0D4D -> 0D4F` with exact count `0004`.
- Reenters exact `SEP #$20`, derives exact start byte `71 = 54 - 0C`, and runs exact helper `8820`.
- Emits exact selector `C309`, runs exact helper `A6F0` with exact `X = 3664`, then exact helper `821E`, then exact shared helper `E0F1`.
- Seeds exact byte `0D13 = 55`, clears exact byte `0D0B`, decrements exact byte `0D78`, reruns exact helper `F2F3` with exact accumulator `00`, seeds exact direct-page exact word `02 = 1004`, and runs exact shared helper `E072`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact negative refresh/export owner that clears exact local work band `0D4D..0D51`, derives exact start slot `71 = 54 - 0C`, reruns the exact `8820 / C309 / 3664 / 821E` service chain, then exact helper `E0F1`, signals exact byte `0D13 = 55`, decrements exact byte `0D78`, reruns exact helper `F2F3(00)`, and exports the exact `104D` window through exact helper `E072`.

### C2:E0F1..C2:E107  ct_c2_short_marker_finalizer_wrapper_using_e150_0d92_2a68_a463_and_fbf1   [strong structural]
- Begins `PHP ; REP #$30`.
- Runs exact shared helper `E150`.
- Seeds exact word `0D92 = 2A68`.
- Runs exact helper `A463`.
- Exits through exact selector tail `X = FBF1 ; JSR 8385`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact short marker/finalizer wrapper that refreshes the exact `77`-latched marker lane through exact helper `E150`, seeds exact word `0D92 = 2A68`, runs exact helper `A463`, and exits through exact selector `FBF1`.

### C2:E108..C2:E14F  ct_c2_low2bit_gated_cyclic_selector_step_owner_for_71_using_e072_e150_and_821e   [strong structural]
- Begins `PHP ; SEP #$30`.
- Uses exact byte `71` as the current exact step index and exact byte `0D1D & 03` as the activity/direction gate.
- Exact zero returns immediately.
- Exact bit `0D1D.bit1` selects direction: one exact lane steps exact byte `71` backward with wrap to exact byte `84`, the other steps it forward with wrap to exact byte `00` once exact bound `85` is reached.
- When the stepped exact index matches the old exact `71`, returns immediately.
- Otherwise stores the stepped exact index back into exact byte `71`, reruns exact helpers `EAC2`, `8820`, `ED31(C309)`, and `A6F0(3664)`, seeds exact direct-page exact word `02 = 1004`, then runs exact shared helper `E072`, exact shared helper `E150`, and exact helper `821E`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact low-2-bits-gated cyclic selector-step owner that moves exact byte `71` one step backward or forward inside exact range `00..84`, reruns the exact `EAC2 / 8820 / C309 / 3664` service chain whenever the exact step actually changes the exact index, exports the exact active window through exact helper `E072`, refreshes the exact `77`-latched marker lane through exact helper `E150`, and finishes with exact helper `821E`.

### C2:E150..C2:E162  ct_c2_short_latched_selector_marker_writer_wrapper_mirroring_54_to_77_then_running_a3ed_3624   [strong structural]
- Begins `PHP ; SEP #$20`.
- Mirrors exact byte `54 -> 0077`.
- Reenters exact `REP #$30`, seeds exact `X = 3624`, and runs exact helper `A3ED`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact short wrapper that mirrors exact selector byte `54` into exact latch byte `0077` and reruns exact helper `A3ED` with exact descriptor `3624`.

## Alias / wrapper / caution labels

## Honest remaining gap

- the old seam `C2:DF76..C2:E095` is now closed more honestly as `C2:DF76..C2:E162`
- the next follow-on family begins at exact owner `C2:E163` and visibly continues into downstream local tables and helper/dispatch code beyond the old `E095` seam hint
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
