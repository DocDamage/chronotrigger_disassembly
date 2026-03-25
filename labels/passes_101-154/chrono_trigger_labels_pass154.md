# Chrono Trigger Labels — Pass 154

## Purpose

Pass 154 closes the scheduler-serviced row worker rooted at exact `C2:F657` and freezes the exact local scale-dispatch material around exact `F6D8`.

## Strong labels

### C2:F657..C2:F69A  ct_c2_persistent_eight_row_direct_page_service_loop_conditionally_running_f69b_f871_then_821e   [strong structural]
- Begins `REP #$30 ; PEA $1800 ; PLD ; STZ $0D73 ; SEP #$30`.
- Rebinds exact direct page to exact `1800` at the start of each exact sweep and clears exact global byte `0D73`.
- On each exact row band, only reaches the exact helper gate when exact row byte `00` is non-negative, exact row byte `18` is non-negative, and either exact row byte `11 != 12` or exact countdown byte `13` underflows after exact `11 == 12 != 00`.
- At that exact helper gate, runs exact helper `F69B` only when exact `0D73 < 0D75`.
- Runs exact helper `F871` when exact row byte `18 == 00`.
- Advances the exact direct-page base by exact `0x0040` through `TDC ; ADC #$0040 ; TCD` and covers exact row bases `1800`, `1840`, `1880`, `18C0`, `1900`, `1940`, `1980`, and `19C0`.
- After the sweep runs exact helper `821E` and loops back to exact `F657` through exact `BRA`.
- Strongest safe reading: exact persistent eight-row direct-page service loop that conditionally runs exact helpers `F69B` and `F871`, yields through exact `821E`, and repeats.

### C2:F69D..C2:F6CD  ct_c2_row_change_front_end_deriving_exact_stream_pointer_words_1b_1e_from_17_14_0a_0c_and_low7_of_11   [strong structural]
- Compares exact row byte `11` against exact row byte `12`, mirrors exact `11 -> 12`, and returns immediately when the exact values match.
- On the exact changed path clears exact latch byte `16`, loads exact selector byte `17`, doubles it into exact dispatch index `X`, loads exact width/base word `14`, and runs exact `JSR ($F6D8,X)`.
- Mirrors the exact returned base word into exact `1B`.
- Uses the exact low seven bits of exact row word `11` to derive exact stride word `4*(11 & 007F)`.
- Derives exact paired stream-pointer words `1B = returned_base + 4*(11 & 007F) + 0A` and `1E = 4*(11 & 007F) + 0C`.
- Branches directly into the downstream exact tail at `F6F7`.
- Strongest safe reading: exact row-change front-end that derives exact stream-pointer words `1B/1E` from exact `17/14`, exact `0A/0C`, and the exact low seven bits of exact row word `11`.

### C2:F6D8..C2:F6DF  ct_c2_four_entry_local_scale_dispatch_table_for_f6af   [strong]
- Exact little-endian words: `F6CE F6D1 F6D2 F6D4`.
- Consumed directly by exact `JSR ($F6D8,X)` at exact `F6AF`.
- Strongest safe reading: exact four-entry local scale-dispatch table selecting the exact zero / passthrough / double / scale-plus-base stubs.

### C2:F6E0..C2:F754  ct_c2_row_stream_scan_and_wram_submit_tail_using_1b_1e_03_13_9690_9692_9693_and_local_factor_table_f755   [strong structural]
- On exact zero exact control byte `[1E],Y`, uses exact row byte `11` plus exact latch bytes `16/21` to choose between exact retry and exact return lanes.
- On exact nonzero exact control byte `[1E],Y`, mirrors that exact byte into exact countdown byte `13`.
- Loads exact paired stream byte `[1B],Y` and compares it against cached exact byte `03`.
- On exact change, mirrors the exact new byte into exact `03`, writes it to exact `$4202`, mirrors exact byte `09 -> 9692`, writes exact literal `6B -> 9693`, and seeds exact `$4203` from the exact four-byte factor table rooted at exact `F755` through exact index byte `02`.
- Seeds exact word `9690 = 7E54`, performs two exact `JSL $7E9690` submits, then runs exact helper `F75C`.
- Finishes through exact `SEP #$30 ; DEC 13 ; RTS`.
- Strongest safe reading: exact row-stream scan / WRAM-submit tail that retries on exact zero control bytes, caches exact stream byte `03`, configures exact `9690/9692/9693`, performs two exact `JSL 7E:9690` submits, runs exact helper `F75C`, and decrements exact countdown byte `13`.

### C2:F755..C2:F758  ct_c2_four_byte_factor_table_00_28_50_78_for_f6e0_submit_tail   [strong]
- Exact bytes: `00 28 50 78`.
- Consumed directly by exact `F6E0..F754` as the source of the exact `$4203` factor byte.
- Strongest safe reading: exact four-byte factor table for the downstream exact submit tail.

## Alias / wrapper / caution labels

### C2:F69B..C2:F69C  ct_c2_inc_16_alias_wrapper_falling_through_into_f69d   [alias wrapper]
- Exact body: `INC $16` and immediate fallthrough into exact `F69D`.
- Strongest safe reading: exact alias entry that increments exact latch byte `16` before entering the downstream exact row-change front-end.

### C2:F6CE..C2:F6D0  ct_c2_local_scale_dispatch_return_zero_stub   [alias]
- Exact body in the caller’s exact 16-bit mode: `LDA #$0000 ; RTS`.
- Strongest safe reading: exact zero-return stub for the exact local scale-dispatch table.

### C2:F6D1  ct_c2_local_scale_dispatch_passthrough_rts_stub   [alias]
- Exact body: `RTS`.
- Strongest safe reading: exact passthrough-return stub for the exact local scale-dispatch table.

### C2:F6D2..C2:F6D3  ct_c2_local_scale_dispatch_double_a_rts_stub   [alias]
- Exact body in the caller’s exact 16-bit mode: `ASL A ; RTS`.
- Strongest safe reading: exact doubled-value return stub for the exact local scale-dispatch table.

### C2:F6D4..C2:F6D7  ct_c2_local_scale_dispatch_asl_then_adc_14_rts_stub   [alias]
- Exact body in the caller’s exact 16-bit mode: `ASL A ; ADC $14 ; RTS`.
- Strongest safe reading: exact scale-plus-base return stub for the exact local scale-dispatch table.

## Honest remaining gap

- exact `C2:F657..C2:F758` is now honestly closed
- the next clearly live callable/helper band begins at exact `C2:F75C`
- exact `C2:F75C...` still needs its own pass and should not be guessed from the middle
