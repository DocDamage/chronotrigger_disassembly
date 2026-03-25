# Chrono Trigger Labels — Pass 140

## Purpose

Pass 140 closes the exact follow-on callable/helper family that session-7 left open at `C2:DE98..C2:DF76`, with one final back-edge correction: `C2:DF76` is the first byte of the next live callable owner, so the clean closure stops at `C2:DF75`. The resolved family is one exact sibling refresh owner, one shared exact `5600/5700` build-refresh helper, one shared exact eight-pass export driver, and one shared exact `5600` entry loader/materializer helper.

## What this pass closes

### C2:DE98..C2:DECB  ct_c2_0d88_checked_sibling_refresh_owner_using_1042_1043_decc_df31_8b93_and_fbe3_tail   [strong structural]
- Begins `PHP ; SEP #$20`.
- Seeds exact word `0D92 = 2AF0` and emits exact selector packet `C2CB` through exact helper `ED31`.
- When exact byte `0D88` is zero, clears exact bytes `1042` and `1043`.
- Mirrors exact byte `1042 -> 54`.
- Runs exact shared helper `DECC`.
- Seeds exact byte `0D78 = FF`.
- Runs exact shared helper `DF31`, then exact helper `8B93`.
- Restores flags with exact `PLP` and exits through exact selector tail `X = FBE3 ; JMP 8385`.
- Strongest safe reading: exact `0D88`-checked sibling refresh owner that normalizes exact bytes `1042/1043`, runs the shared exact `DECC` strip/build refresh helper, reruns the shared exact `DF31` export driver, and exits through exact selector `FBE3`.

### C2:DECC..C2:DF30  ct_c2_shared_5600_5700_build_refresh_helper_using_2400_2500_7700_dd40_and_1043_window_update   [strong structural]
- Begins `PHP ; REP #$20`.
- Clears exact word `5600`, then uses overlapping exact `MVN 7E,7E` from `5600 -> 5602` with exact count `0005`, yielding an exact zero-seeded startup band across `5600..5607`.
- Reenters exact `SEP #$30`, seeds exact byte `0DDC = 07`, clears exact `X`/`Y`, and scans exact paired tables `2500,X` and `2400,X`.
- Always stages exact byte `2500,X -> 5700,Y` first.
- Exact byte `2400,X == 00` ends the scan.
- Exact byte `2400,X >= F2` discards the candidate without advancing exact destination index `Y`.
- Exact byte `2400,X < F2` is accepted into exact strip `5600,Y`; the exact acceptance byte then indexes exact table `7700`, and exact destination index `Y` advances only when exact bit `7700[accepted] & 04` is clear.
- Stores exact final destination index `Y -> 1049`, writes exact terminator byte `00 -> 5600,Y`, runs exact helper `DD40`, clamps exact byte `54` against exact byte `0DDC = 07`, then conditionally raises exact byte `1043` from direct-page exact byte `57` and mirrors the final exact value into exact bytes `0DD9` and `0D95`.
- Exits `PLP ; RTS`.
- Strongest safe reading: shared exact `5600/5700` build-refresh helper that zero-seeds exact strip `5600`, filters/stages exact candidates out of paired tables `2400/2500`, records the exact resulting strip length in `1049`, reruns exact helper `DD40`, clamps exact byte `54`, and updates the exact `1043 / 0DD9 / 0D95` window-latch bytes from the downstream direct-page result.

### C2:DF31..C2:DF50  ct_c2_shared_eight_pass_0x80_stride_export_driver_using_df51_over_2f5c_through_32dc   [strong structural]
- Begins `PHP ; REP #$30`.
- Seeds exact word `61 = 2F5C` and clears exact word `22`.
- Repeatedly runs exact helper `DF51`, then advances exact word `61 += 0080` and increments exact word `22`.
- Loops for exact eight passes, producing exact destinations `2F5C, 2FDC, 305C, 30DC, 315C, 31DC, 325C, 32DC`.
- Exits `PLP ; RTS`.
- Strongest safe reading: shared exact eight-pass `0x80`-stride export driver over exact destination band `2F5C..32DC`, using exact helper `DF51` as the per-pass materializer.

### C2:DF51..C2:DF75  ct_c2_shared_5600_entry_loader_into_04c9_1044_then_dd56_materializer_using_7800   [strong structural]
- Begins `PHP ; REP #$31`.
- Computes exact source index `Y = (1043 + 22) & 00FF`.
- Loads exact byte `5600,Y -> 04C9`.
- Doubles the accepted exact source byte into `X`.
- Loads exact word `7800,X`, shifts it right once, adds exact word `51`, and stores the exact result into exact word `1044`.
- Runs exact helper `DD56`.
- Exits `PLP ; RTS`.
- Strongest safe reading: shared exact `5600` strip-entry loader that stages exact byte `04C9` from exact strip `5600`, derives exact word `1044` from exact table `7800` plus exact base word `51`, and then enters the shared exact `DD56` hardware-math materializer.

## Alias / wrapper / caution labels

## Honest remaining gap

- the old seam `C2:DE98..C2:DF76` is now closed, but `C2:DF76` itself is the first byte of the next live callable owner
- the next follow-on family visibly begins with an exact owner at `DF76`, a local exact pointer table rooted at `DFC5`, a shared helper at `DFCF`, and more downstream callable/helper code through at least `E070`
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
