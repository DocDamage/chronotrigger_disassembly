# Chrono Trigger Labels — Pass 159

## Purpose

Pass 159 closes the exact end-of-bank exact callable family after pass 158, and it corrects the exact prior seam heads from exact `FEFA/FF27` to the real exact starts `FEFB/FF26`.

## Strong labels

### C2:FEFB..C2:FF25  ct_c2_clear_upper_0101_bits_then_select_fffbea_slot_from_54_mark_2e01_and_emit_fa3c_packet   [strong structural]
- Real exact callable head is exact `FEFB`, not exact `FEFA`.
- Begins `PHP ; SEP #$20 ; LDA #$FE ; TRB $0101`.
- Runs exact helper `EB89` with exact `X = BFE8`.
- Uses exact byte `54` as one exact exact `FF:FBEA` table selector, doubles it, loads one exact table word/entry into exact `X`, writes exact byte `04` into exact `2E01,X`, and emits one exact packet through exact helper `8385` with exact pointer `FA3C`.
- Exits through exact `PLP ; RTL`.
- Strongest safe reading: exact selector/mark/packet owner that clears upper exact bits in exact `0101`, selects one exact `FF:FBEA` entry from exact byte `54`, marks exact `2E01,X`, and emits the exact `FA3C` packet.

### C2:FF26..C2:FF86  ct_c2_mirror_0f02_0f00_0f01_into_1800_1900_then_copy_40_byte_row_and_store_0f05   [strong structural]
- Real exact callable head is exact `FF26`, not exact `FF27`.
- Begins `PHP ; SEP #$20`.
- Mirrors exact `0F02 -> 1800` and exact `0F02 -> 1900`, runs exact helpers `F46F` and exact local helper `FF87`, then increments exact byte `0D15`.
- Mirrors exact `0F00 -> 1811` and exact `0F01 -> 1817`, temporarily binds direct page to exact `1800`, and runs exact helper `F292`.
- Copies one exact `0x40`-byte work block `1800 -> 1900` through exact `MVN 7E,7E`, restages exact `190E/1919`, then derives exact byte `0F05` from exact word `1814 >> 2`.
- Exits through exact `PLP ; RTS`.
- Strongest safe reading: exact row/work-block rebuilder over exact `1800/1900` that seeds row state, runs exact preparation helpers, mirrors one exact 64-byte block, and stores exact derived byte `0F05`.

### C2:FF87..C2:FFA3  ct_c2_local_six_byte_import_from_d1_to_95ba_then_mirror_to_963a_and_inc_0d15   [strong structural]
- Real exact caller is exact `C2:FF35`.
- Begins `PHP ; REP #$30`.
- Imports one exact 6-byte source block from exact bank `D1` into exact WRAM `95BA` through exact `MVN 7E,D1`.
- Mirrors that exact 6-byte block from exact `95BA` into exact `963A` through exact `MVN 7E,7E`.
- Increments exact byte `0D15` and exits through exact `PLP ; RTS`.
- Strongest safe reading: exact local import-and-mirror helper used by exact owner `FF26`.

## Alias / wrapper / caution labels

### C2:FFA4..C2:FFA7  ct_c2_overlap_tail_after_ff87_helper   [caution structural]
- Exact bytes: `15 0D 28 60`.
- No exact direct caller lands here.
- Strongest safe reading: exact overlap tail after exact helper `FF87`, not one exact owner.

### C2:FFA8..C2:FFC0  ct_c2_late_tail_clone_of_ff26_restage_and_0f05_finalize_lane   [caution structural]
- Exact body matches the exact tail of exact owner `FF26`.
- Restages exact `190E = C898` and exact `1919 = 40`, then derives exact `0F05` from exact `1814 >> 2`.
- Ends `PLP ; RTS`.
- No exact direct caller is currently cached for exact `FFA8`.
- Strongest safe reading: exact late exact tail clone of the exact `FF26` finalize lane, not one independently proven owner.

### C2:FFC1..C2:FFDD  ct_c2_local_duplicate_of_ff87_six_byte_import_and_mirror_helper   [caution structural]
- Exact body is byte-for-byte the same structural helper as exact `FF87..FFA3`.
- Performs the exact 6-byte `D1 -> 95BA` import, the exact 6-byte `95BA -> 963A` mirror, and exact `INC 0D15`.
- No exact hot direct caller is currently cached for exact `FFC1`.
- Strongest safe reading: exact local duplicate of exact helper `FF87`, but not one currently-proven hot entry.

### C2:FFDE..C2:FFDF  ct_c2_tiny_overlap_tail_after_ffc1_helper_clone   [caution structural]
- Exact bytes: `28 60`.
- Strongest safe reading: exact tiny exact overlap tail, not one exact owner.

### C2:FFE0..C2:FFED  ct_c2_late_copy_tail_mirroring_95ba_to_963a_and_incrementing_0d14   [caution structural]
- Exact body begins `LDY #$963A ; LDA #$0005 ; MVN 7E,7E`.
- Reuses the exact `95BA -> 963A` mirror lane but increments exact byte `0D14` instead of exact `0D15`.
- Ends `PLP ; RTS`.
- No exact direct caller is currently cached for exact `FFE0`.
- Strongest safe reading: exact late exact copy tail / local overlap entry, not one independently anchored top-level owner.

## Honest remaining gap

- exact seam heads `FEFA` and `FF27` were one byte early; the real exact callable starts are exact `FEFB` and exact `FF26`
- exact `C2:FFEE..C2:FFFF` still does not decode as one clean exact owner and sits at the exact bank-end cliff
- the next pass should close the exact bank-end tail honestly instead of pretending those final exact bytes are already understood
