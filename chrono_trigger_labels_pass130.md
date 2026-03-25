# Chrono Trigger Labels — Pass 130

## Purpose

Pass 130 closes the downstream post-substitution helper/owner seam at `C2:CC0E..C2:CE85` and tightens the directly-called follow-on helper pair at `C2:CE86..C2:CEC1`.

## Strong labels

### C2:CC0E..C2:CC4E  ct_c2_0f0f_aware_immediate_110f_packet_emitter_waiting_on_2141_and_using_04fb_or_ff   [strong structural]
- Direct callable entry from the already-frozen `C7E0` overflow path.
- Tests exact latch byte `0F0F`.
- When that exact latch is nonzero, seeds exact local bytes `02 = 08`, `03 = 01`, runs exact helpers `CBF7` and `83CA`, then retests exact byte `0F0F`.
- When the exact latch remains nonzero, waits until exact long hardware/status byte `002141 == 0`, looping through exact helper `821E`.
- Then writes exact packet byte `1E01 = 0F0E`, exact packet byte `1E00 = 11`, seeds exact local byte `02 = 10`, and seeds exact local byte `03 = FF` only when exact byte `04FB == 0`.
- Runs exact helper `CBEB` and exits `RTS`.
- Strongest safe reading: exact `0F0F`-aware immediate `11/0F0E` packet emitter that optionally primes `CBF7/83CA`, waits on exact hardware/status byte `2141`, and then emits through exact helper `CBEB`.

### C2:CC4F..C2:CCB0  ct_c2_three_slot_highbit_packet_writer_using_ccb1_and_paired_ec93_rows   [strong structural]
- Begins `PHP ; SEP #$20`.
- Seeds exact base pair `04 = 2E84`, `02 = 100E`.
- When exact byte `0D36 != 0`, switches to exact `04 = 2E90`, `02 = 1010`, and writes exact byte `38` into exact bytes `9380`, `9386`, and `938C`.
- In 16-bit mode loops over exact words `0F02`, `0F03`, and `0F04`.
- When exact bits `0x00C0` are set, runs exact helper `CCB1`, seeds exact base word `61 = 04`, and twice runs exact helper `EC93` with exact `X = 0006`, first from exact base `02`, then from exact base `02 + 1000`.
- Advances exact base word `04` by `0180` after every slot and exits `PLP ; RTS`.
- Strongest safe reading: exact three-slot high-bit packet writer that conditionally expands the `0F02` strip through exact helper `CCB1` and emits paired exact rows through `EC93`.

### C2:CCB1..C2:CCD8  ct_c2_negative_gated_95a2_word_strip_clearer_from_297f_highbyte   [strong structural]
- Begins `PHP ; SEP #$30`.
- Clears exact bit `0x40` from the incoming `A`; when the resulting exact byte is negative, returns immediately.
- Otherwise uses the exact input byte as an index into exact word table `297F`.
- Keeps only the exact high byte from that word, shifts it right three times, and uses the exact result as a `Y` base.
- Iterates exact count `000F`, updating exact words `95A2,Y` as `LSR -> AND #3DEF`, advancing `Y` by 2 each time.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact negative-gated `95A2` word-strip clearer / normalizer derived from the exact `297F` high-byte lane.

### C2:CCDB..C2:CD2A  ct_c2_dual_three_slot_exporter_repeatedly_calling_cd9b_over_0f05_then_0f02   [strong structural]
- Begins `PHP ; REP #$30`.
- Seeds exact local word `22 = 0006`, clears exact local byte `24`, and in 8-bit mode seeds exact compare byte `71 = 73 + 80`.
- First loop visits exact bytes `0F05`, `0F07`, and `0F09`; when exact bits `0xC0` are clear, runs exact helper `CD9B`.
- When exact byte `0D36 != 0`, reseeds exact local word `22 = 0012`.
- Clears exact bytes `71` and `24`.
- Second loop visits exact bytes `0F02`, `0F03`, and `0F04`; when the exact slot byte is nonnegative, runs exact helper `CD9B`.
- Exits `PLP ; RTS` after three slots.
- Strongest safe reading: exact dual three-slot exporter that walks the exact `0F05` lane and then the exact `0F02` lane, conditionally handing each accepted slot to exact helper `CD9B`.

### C2:CD2B..C2:CD9A  ct_c2_compact_2980_state_scanner_building_0f02_0f05_lists_and_count_bytes_0f0b_0f0c   [strong structural]
- Begins `PHP ; REP #$30`.
- Seeds exact word `0F02 = 8080`, performs exact overlapping same-bank block move `0F02.. -> 0F04..` for exact length `0007`, and clears exact byte `0F0B`.
- In 8-bit mode loops exact indexes `0..2` over exact table `2980`.
- When an exact table byte is nonnegative, increments exact count byte `0F0B`, probes exact long byte `7F:01DF` through exact long indexed mask table `FFF9BB,X`, conditionally decrements exact count byte `0F0B`, ORs in exact flag byte `40` when the exact probe failed, and stores the exact result into exact bytes `0F02..0F04`.
- When exact byte `0D36 == 0`, performs a second loop over exact indexes `3..8`, collecting exact nonnegative `2980` entries into exact bytes `0F05+Y`.
- When the exact phase-flag byte does not carry exact bit `0x40`, writes the final exact `Y` count into exact byte `0F0C`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact compact-state scanner that compresses accepted exact `2980` state bytes into the live exact `0F02` and `0F05` lists while tracking exact counts `0F0B` and `0F0C`.

### C2:CD9B..C2:CDC9  ct_c2_exact_1800_180e_row_builder_using_cdcb_and_ce6e_tables   [strong structural]
- Begins `PHP ; REP #$30`.
- Runs exact helper `8820`.
- ORs exact bytes `51` into the accumulator and, when the exact result is nonzero, skips the row write.
- Otherwise loads an exact base word from exact local table `CDCB,X` into exact word `61`, runs exact helper `A216`, then converts exact word `9A90` through exact helper `F626`.
- Stores the converted exact result into exact row slot `180E,Y` using exact local word table `CE6E,X` and mirrors exact byte `9A90` into exact slot `1800,Y`.
- Increments exact compare byte `71` and exits `PLP ; RTS`.
- Strongest safe reading: exact conditional `1800/180E` row builder using the exact local base-word table at `CDCB` and the exact row-word table at `CE6E`.

### C2:CDCB..C2:CDE2  ct_c2_local_base_word_table_for_cd9b_row_builder   [strong]
- Exact little-endian word table used by `CD9B`.
- Exact entries: `2E00`, `2F80`, `3100`, `2E20`, `2FA0`, `3120`, `32A0`, `35A0`, `0C3B`, `0C2E`, `0831`.
- Strongest safe reading: exact local base-word table for the `CD9B` row builder.

### C2:CDE3..C2:CE28  ct_c2_two_phase_ce49_scan_owner_building_1800_180e_rows_from_0f02_lists   [strong structural]
- Begins `PHP ; REP #$30`.
- Seeds exact local word `02` from exact byte `0D36`, but forces exact `02 = 0012` when that exact byte is nonzero.
- Clears exact local byte `00`, runs exact helper `CE2A`, then repeatedly runs exact helper `CE49`.
- When exact `A | 00 == 0`, bumps exact local word `02` by 2 twice.
- First phase continues until exact local byte `00 == 03`.
- When exact byte `0D36 == 0`, reseeds exact local byte `02 = 06`, exact local byte `00 = 80 + 03`, reruns exact helper `CE49`, and continues until exact local byte `02 == 0E`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact two-phase owner that repeatedly invokes the exact `CE49` row writer over the compacted exact `0F02` lists, with one phase gated by exact byte `0D36`.

### C2:CE2A..C2:CE48  ct_c2_1980_seeded_direct_page_stepping_helper_descending_by_40_until_below_1800   [strong structural]
- Begins `PHP ; PHD ; PEA 1980 ; PLD`.
- In 8-bit mode seeds exact byte `00 = FF` and clears exact bytes `11` and `18`.
- In 16-bit mode repeatedly transfers the direct-page value into `A`, subtracts exact `003F+1`, transfers the exact result back into direct page, and loops until the exact result drops below `1800`.
- Restores the previous direct page and flags, then returns.
- Strongest safe reading: exact `1980`-seeded direct-page stepping helper that walks the exact direct-page work base downward in exact `0x40` steps until it falls below exact `1800`.

### C2:CE49..C2:CE6D  ct_c2_single_slot_1800_180e_row_writer_using_2980_and_ce6e   [strong structural]
- Begins `PHP ; TDC`.
- Uses exact slot byte `00` as an index into exact byte strip `0F02`.
- When the exact slot byte is nonnegative, clears exact bit `0x40`, uses the resulting exact byte as an index into exact table `2980`, runs exact helper `F626`, and stores the exact result into exact byte `1800,Y`.
- Then uses exact word table `CE6E,X` to seed exact row word `180E,Y`.
- Clears the accumulator, increments exact slot byte `00`, restores flags, and returns.
- Strongest safe reading: exact single-slot `1800/180E` row writer over the compacted exact `0F02` strip.

### C2:CE6E..C2:CE85  ct_c2_local_row_word_table_for_cd9b_and_ce49   [strong]
- Exact little-endian word table used by `CD9B` and `CE49`.
- Exact entries: `7438`, `7468`, `7498`, `8C38`, `8C68`, `8C98`, `8CC8`, `8C08`, `8CF8`, `A838`, `A868`, `A898`.
- Strongest safe reading: exact local row-word table for the `CD9B` / `CE49` writer family.

### C2:CE86..C2:CE95  ct_c2_selector_emitter_running_fff677_then_dual_8385_with_ce96_and_fc14   [strong structural]
- Direct callable entry from the already-frozen `C7AC` owner.
- Runs exact long helper `FFF677`.
- Seeds exact selector word `X = CE96`, runs exact helper `8385`.
- Then seeds exact selector word `X = FC14` and exits through exact jump `8385`.
- Strongest safe reading: exact selector-emitter helper that runs `FFF677` and then emits the exact `CE96` local descriptor plus one fixed `FC14` descriptor through exact helper `8385`.

### C2:CE96..C2:CE9C  ct_c2_local_selector_descriptor_packet_for_ce86   [strong]
- Exact 7-byte local descriptor packet consumed by `CE86`.
- Exact bytes: `00 70 00 B0 7E 00 06`.
- Strongest safe reading: exact local selector descriptor packet for the `CE86` helper.

### C2:CE9D..C2:CEC1  ct_c2_2109_68_initializer_scheduling_cece_and_copying_d57a_to_0f12   [strong structural]
- Direct callable entry from the already-frozen `C7AC` owner.
- Begins `PHP ; SEP #$20`.
- Writes exact byte `68` into exact long hardware register `002109`.
- In 16-bit mode clears exact word `0F10`, seeds exact callback pointer `A = CECE`, exact delay/count `X = 0010`, and runs exact helper `8249`.
- Then copies exact `000C` bytes from exact source `D57A` into exact destination `0F12`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact `2109 = 68` initializer that schedules the downstream exact `CECE` callback body and copies the exact `D57A` descriptor strip into exact `0F12`.

### C2:CEC2..C2:CED1  ct_c2_0d13_bit10_wrapper_running_822b_then_fff716   [strong structural]
- Switches to 8-bit A.
- Sets exact bit `0x10` in exact word/byte `0D13`.
- Loads exact byte `02` and runs exact helper `822B`.
- Runs exact long helper `FFF716`.
- Branches directly to the previous helper’s exact `RTS`.
- Strongest safe reading: exact `0D13.bit10` wrapper around the fixed `822B -> FFF716` service lane.

## Alias / wrapper / caution labels

## Honest remaining gap

- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B/0D8C/0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
- the next real code seam now moves naturally to `C2:CED2..C2:CF92`
