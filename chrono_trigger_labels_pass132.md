# Chrono Trigger Labels — Pass 132

## Purpose

Pass 132 closes the downstream callable setup / export seam that pass 131 left open at `C2:D065..C2:D0C5`, and it freezes one easy additional callable owner at `C2:D156` once the helper chain becomes visible.

## Strong labels

### C2:D065..C2:D0DD  ct_c2_callable_fc53_setup_export_owner_running_d10d_d36c_and_ffcc74_import_then_984a_86dd_fbe3_fbff   [strong structural]
- Begins `PHP ; SEP #$20`.
- Emits exact selector `FC53` through exact helper `ED31`.
- Runs exact local helper `D10D`, then tail-emits exact selector `FC53` through exact helper `8385`.
- Clears exact byte `0D15`, seeds exact byte `C9 = 03`, and runs exact helper `821E`.
- In 16-bit mode clears exact word `3000` and performs exact overlapping same-bank move `3000 -> 3002` for exact length `05FE`.
- Stores the post-MVN exact accumulator into exact word `0D77`, yielding the exact `FFFF` tail state.
- Mirrors exact byte `0414 -> 79` and exact byte `0414 -> 7F`, then runs exact helper `D36C`.
- Emits exact selector `FC1B` through exact helper `8385`.
- Clears exact byte `0D15`, reruns exact helper `821E`, and seeds exact word `0D0E = FFFF`.
- Copies exact `0010` bytes from exact source `FF:CC74` into exact destination `7E:94C0`.
- Increments exact byte `0D15`, runs exact helpers `984A` and `86DD`, seeds exact byte/word `0D13 = 19`, and emits exact selector tail `FBE3 -> 8385` and `FBFF -> 8385`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact callable setup / export owner that emits the `FC53` setup lane, runs the local `D10D` helper family, shifts the live `3000` strip forward by two bytes, mirrors exact selector/state byte `0414` into `79/7F`, imports exact block `FF:CC74 -> 7E:94C0`, and finishes through the fixed `984A / 86DD / FBE3 / FBFF` tail.

### C2:D0DE..C2:D0E4  ct_c2_local_0d13_19_wrapper_returning_immediately   [strong structural]
- Exact bytes decode to `PHP ; SEP #$20 ; LDA #$19 ; STA $0D13 ; PLP ; RTS`.
- Strongest safe reading: exact local wrapper that only seeds exact byte/word `0D13 = 19` and returns.

### C2:D0E5..C2:D10C  ct_c2_sibling_callable_c138_owner_mirroring_7f_to_54_then_running_cffb_and_fbe3_fbff_before_e923   [strong structural]
- Begins `PHP ; SEP #$20`.
- Mirrors exact byte `7F -> 54`.
- Emits exact selector `C138` through exact helper `ED31`.
- Increments exact byte `0D15`.
- Seeds exact byte/word `0D13 = 19`.
- Runs exact helper `CFFB`.
- Emits exact selector tail `FBE3 -> 8385` and `FBFF -> 8385`.
- Exits through exact `PLP ; JMP E923`.
- Strongest safe reading: exact sibling callable owner that mirrors exact selector byte `7F -> 54`, emits exact selector `C138`, bumps exact byte `0D15`, reruns the exact callable initializer `CFFB`, then rejoins the broader service tail at exact jump `E923` after the fixed `FBE3 / FBFF` selector pair.

### C2:D10D..C2:D130  ct_c2_three_pass_source_page_and_0dc7_window_driver_stepping_4ec6_4fc6_50c6_and_20_40_60   [strong structural]
- Seeds exact direct-page pointer `61/62 = 4EC6`.
- Clears exact byte `79`.
- Seeds exact byte `0DC7 = 20`.
- Loops exactly three times:
  - `JSR D131`
  - `INC 62` to advance the exact source page from `4E` to `4F` to `50`
  - adds exact `20` to exact byte `0DC7`
  - increments exact byte `79`
- Returns once exact byte `79 == 03`.
- Strongest safe reading: exact 3-pass driver that walks three consecutive exact source pages through `61/62` while stepping the exact destination/window byte `0DC7` through `20 / 40 / 60` before returning.

### C2:D131..C2:D155  ct_c2_three_entry_row_descriptor_writer_using_61_source_pointer_0dc7_window_and_staged_3001_3003_3005_words   [strong structural]
- Loads exact source pointer from exact direct-page word `61/62` into `X`.
- Seeds exact `Y = 0002`.
- In 8-bit mode constructs the exact staged selector words `3001`, `3003`, and `3005` through the sequence `LDA #30 ; XBA ; LDA 79 ; ASL ; INC`.
- Runs exact helper `FBB4`.
- Advances exact source pointer `X` by ten exact bytes through ten exact `INX`.
- Seeds exact `Y = 0010`.
- Loads exact byte `0DC7` and runs exact helper `FB97`.
- Exits through exact jump `D32C`.
- Strongest safe reading: exact 3-entry row/descriptor writer that consumes the current exact source pointer in `61/62`, feeds one of the exact staged selector words `3001 / 3003 / 3005` into `FBB4`, advances the source pointer by exact `0x0A`, then uses exact destination/window byte `0DC7` in `FB97` before tailing into exact helper `D32C`.

### C2:D156..C2:D197  ct_c2_three_slot_fff9c4_poll_service_owner_clearing_or_marking_0d49_then_running_d296_or_d19f_and_d2c4   [strong structural]
- Begins `PHP ; SEP #$20`.
- Seeds exact bytes `0D79 = 51`, `79 = 51`, `0D7B = 00`, and `0D4C = FF`.
- Across three exact slots, clears exact byte `0D49[79]`, runs exact long helper `FFF9C4`, and branches on exact result byte `00`.
- Nonzero-result lane seeds exact byte `020C = 1A` and runs exact helper `D296`.
- Zero-result lane increments exact byte `0D49[79]` and runs exact helper `D19F`.
- Both lanes run exact helper `D2C4`, increment exact byte `79`, and continue until the exact 3-slot sweep is complete.
- Tail-emits exact local selector packet `D198` through exact helper `8385`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact 3-slot `FFF9C4` poll / service owner that clears and conditionally marks exact slot bytes `0D49[79]`, chooses either the exact `020C = 1A -> D296` lane or the exact `INC 0D49[79] -> D19F` lane, always runs exact helper `D2C4`, then emits the exact local packet at `D198`.

### C2:D198..C2:D19E  ct_c2_local_selector_descriptor_packet_for_d156_three_slot_poll_service_owner   [strong]
- Exact 7-byte local descriptor used by the `D156` owner tail.
- Exact bytes: `00 70 00 6E 7E 00 02`.
- Strongest safe reading: exact local selector descriptor packet for the `D156` 3-slot poll / service owner.

## Alias / wrapper / caution labels

## Honest remaining gap

- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
- the next real code seam now moves naturally to `C2:D19F..C2:D2C3`
