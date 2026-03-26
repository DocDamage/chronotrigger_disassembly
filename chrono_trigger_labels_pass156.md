# Chrono Trigger Labels — Pass 156

## Purpose

Pass 156 closes the former exact `C2:F943` live seam and the immediately-following local callback/helper family through exact `C2:FBD0`.

## Strong labels

### C2:F943..C2:F9B1  ct_c2_0dce_0dcf_change_gated_4e00_block_opener_and_8249_callback_scheduler   [strong structural]
- Real exact outside caller is exact `C2:C4F4`.
- Begins `PHP ; SEP #$20`.
- Seeds exact packet/service fields `0214 = 00`, `0212 = 7E`, `020F = FF`, `0DC9 = 01`, `020D = D3FE`, and `0DCC = 6900`.
- Compares exact byte `0DCE` against exact cached byte `0D77`.
- On exact change, mirrors exact byte `0DCE -> 0D77 / 020C`, widens through exact `REP #$30`, clears exact word `4E00`, performs one exact overlapping same-bank move `7E:4E00 -> 7E:4E02` for exact move-count `007D`, then loads exact local callback pointer `A = F9B2`, exact count/delay `X = 0010`, and runs exact helper `8249`.
- On exact no-change, tests exact byte `00C0`; nonzero exits immediately through exact `PLP ; RTS`.
- On exact no-change with exact `00C0 == 00`, compares exact byte `0DCF` against exact cached byte `0D78`.
- When exact `0DCF != 0D78`, widens through exact `REP #$30`, uses exact current offset word `0DC1` to clear exact paired word bands `4E0A,X` and `4E4A,X` in exact `X += 2` steps while exact `X < 0040`, then loads exact local callback pointer `A = FA06`, exact count/delay `X = 0010`, and runs exact helper `8249`.
- Exits through exact `PLP ; RTS`.
- Strongest safe reading: exact `0DCE/0DCF` change-gated owner that seeds the live packet fields, opens or clears exact `4E00`-family work bands, and schedules either exact local callback `F9B2` or exact local late-entry callback `FA06` through exact helper `8249`.

### C2:F9B2..C2:FA47  ct_c2_dual_phase_packet_bootstrap_owner_running_faa4_then_shared_fa06_tail   [strong structural]
- Reached as an exact local scheduled callback from exact owner `F943` via exact pointer load `A = F9B2`.
- Begins `REP #$30`.
- Seeds exact setup/state words `0DD0 = 0080`, `0DC5 = 4E0A`, `0DC3 = 0000`, `0DC1 = 0000`, `0210 = 5E00`, `0DD2 = 0008`, `0DD4 = 7800`, `0DD6 = 5E00`, and `0DC7 = 3101`.
- Runs exact `JSL C2:0003`, then exact helper `FAA4`.
- After that exact first phase restores exact `X` with exact `PLX`, narrows to exact 8-bit accumulator mode, derives exact byte `0DC1` from exact `0DD2`, snapshots exact word `0DC5 -> 26`, derives exact nibble byte `28 = (0DC7 - 1) & 0F`, mirrors exact byte `0DCF -> 020C / 0D78`, then widens again.
- Uses exact derived nibble byte `28` and exact saved base word `26` to restage exact word `0DC5 = 2*28 + 26`.
- Seeds exact second-phase words `0DC7 = 3941`, `0DD2 = 0008`, `0DD4 = 7A00`, `0DD6 = 6200`, and exact packet base `0210 = 6200`.
- Runs exact `JSL C2:0003`, exact helper `FAA4`, and exact tail jump `JMP 8216`.
- Strongest safe reading: exact local dual-phase packet/bootstrap owner that runs one exact first setup/submit phase rooted at exact `5E00/7800/3101`, then rejoins the shared exact late-entry tail to restage exact `0DC5/0DC7/0DD2/0DD4/0DD6/0210` for the second exact `6200/7A00/3941` phase before exact jump `8216`.

### C2:FA48..C2:FA9D  ct_c2_active_block_two_byte_opener_then_8249_schedule_of_fa9e_callback_and_c2_0003_seed   [strong structural]
- Begins `PHP ; SEP #$20`.
- Seeds exact packet fields `0214 = 00`, `0212 = 7E`, and clears exact word/byte family `0DC3`.
- Widens through exact `REP #$30`, clears exact `0DC1`, derives exact active block base `X = Y = 0DC5 & FFC0`, zeroes the first exact word at that exact block base, then performs one exact overlapping same-bank move `7E:[base] -> 7E:[base+2]`.
- The exact move count is derived from exact word `0DD0` through three exact decrements before `MVN`, which makes the move length effectively the current exact block size minus two bytes.
- Reseeds exact packet/setup words `0210 = 5E00`, `0DC7 = 3101`, `0DD2 = 0008`, `0DD4 = 7800`, and `0DD6 = 5E00`.
- Loads exact local callback pointer `A = FA9E`, exact count/delay `X = 0010`, and runs exact helper `8249`.
- Then runs exact `JSL C2:0003` and exits through exact `PLP ; RTS`.
- Strongest safe reading: exact owner that opens the currently-active exact `0DC5` block by two bytes, reseeds the exact `5E00/7800/3101` packet family, schedules exact local callback `FA9E` through exact helper `8249`, then runs exact `C2:0003`.

### C2:FAA4..C2:FAE8  ct_c2_iterative_821e_0009_driver_advancing_0dc1_0dc7_0dd5_until_0215_finishes   [strong structural]
- Called from exact `F9E8`, exact `FA43`, and exact local wrapper `FA9E`.
- Begins `JSR 821E ; REP #$10 ; SEP #$20`.
- Mirrors exact byte `0DC9 -> 0213`.
- Runs exact `JSL C2:0009`, then exact helper `FAE9`.
- Checks exact status/result byte `0215`.
- When exact `0215 == 00`, exits immediately through exact `RTS`.
- When exact `0215 != 05`, branches back to the exact `821E` head and retries without restaging the exact `0DC1/0DC7/0DD5` family.
- When exact `0215 == 05`, advances exact byte `0DC1 = (0DC1 & E0) + 80`, advances exact byte `0DC7 = (0DC7 & C0) + 41`, clears exact word/byte family `0DC3`, increments exact byte `0DD5` twice, restores exact byte `0DD2 = 08`, and loops back to the exact `821E` head.
- Strongest safe reading: exact iterative driver that yields through exact `821E`, runs exact `C2:0009` plus exact helper `FAE9`, and on exact continuation code `0215 == 05` advances the exact `0DC1/0DC7/0DD5` cursor family before retrying.

### C2:FAE9..C2:FB96  ct_c2_0217_change_gated_table_rebuilder_using_838e_and_dual_4e00_word_bands_then_0dcc_submit   [strong structural]
- Reached from exact helper `FAA4` through exact local call `JSR FAE9`.
- Begins `PHP ; SEP #$20`.
- Compares exact byte `0217` against exact cached byte `0DC3`.
- When exact `0217 == 0DC3`, skips the rebuild lane and jumps directly to the exact tail rooted at exact `FB72`.
- When exact `0217 != 0DC3`, mirrors exact byte `0217 -> 0DC3`, widens through exact `REP #$20`, seeds exact `9890 = 0DD4`, exact `9892 = 0DD6`, exact `9894 = 007E`, and exact `9895 = 0400`, then runs exact helper `838E` with exact `X = 9890`.
- Narrows to exact 8-bit accumulator mode, derives exact byte `0000` from exact byte `0234` through the repeated exact lane `LSR ; ADC #00` three times, clears exact byte `0001`, then widens through exact `REP #$30`.
- Derives exact rebuild destination `X = (((0DD2 & 00F8) >> 2) + 0DC1 + 0DC5)` and exact loop count `Y = (0000 - ((0DD2 & 00F8) >> 3))`.
- In that exact `Y`-counted loop writes one exact masked/tagged word into exact table `0000,X` and one exact `| 0010` mirror word into exact table `0040,X`, using the exact running source word `((count-1) + 0DC7 + 0010) & FFEF`.
- After the rebuild loop restores exact byte `0DD2 = 0234`, seeds exact submit block `9890 = 0DCC`, `9892 = (0DC5 & FFC0)`, `9894 = 007E`, `9895 = 0DD0`, runs exact helper `838E`, and exits through exact `PLP ; RTS`.
- Strongest safe reading: exact `0217`-change-gated rebuild helper that optionally regenerates paired exact `4E00`-family word bands from exact packet/result byte `0234`, then always emits one exact trailing submit rooted at exact `0DCC` and the exact current `0DC5` block.

### C2:FB97..C2:FBB6  ct_c2_masked_3100_word_stamper_mirroring_to_x_and_x_plus_0040   [strong structural]
- Has real outside callers at exact `C2:D150`, exact `C2:D3FB`, exact `C2:E4F1`, and exact `C2:E4FC`.
- Exact body begins `PHP ; REP #$30`.
- On each exact `Y`-counted iteration masks the incoming exact word with exact `00EF`, forces exact bits `3100`, writes that exact word to exact `0000,X`, then writes exact `(word | 0010)` to exact `0040,X`.
- After each exact pair increments the exact source word by one exact `INC`, clears exact bit `0010` again through exact `AND #FFEF`, advances exact `X += 2`, decrements exact `Y`, and loops while exact `Y != 0`.
- Exits through exact `PLP ; RTS`.
- Strongest safe reading: exact masked word-stamping helper that writes one exact `3100`-tagged word stream into exact `X` and the exact `+0010` mirrored partner into exact `X + 0x40`.

## Alias / wrapper / caution labels

### C2:FA06..C2:FA47  ct_c2_shared_late_entry_restaging_0d78_0dc5_0dc7_then_running_faa4_and_jumping_8216   [alias late entry]
- Reached as an exact local scheduled callback from exact owner `F943` via exact pointer load `A = FA06`.
- Begins at the exact shared second-phase tail inside exact owner `F9B2`.
- Mirrors exact byte `0DCF -> 020C / 0D78`, clears exact `0DC3`, restages exact `0DC5` from exact saved base word `26` plus exact nibble byte `28`, then seeds exact second-phase words `0DC7 = 3941`, `0DD2 = 0008`, `0DD4 = 7A00`, `0DD6 = 6200`, and exact packet base `0210 = 6200`.
- Runs exact `JSL C2:0003`, exact helper `FAA4`, and exits through exact jump `8216`.
- Strongest safe reading: exact overlapping callable late entry into the shared exact second-phase tail of exact owner `F9B2`.

### C2:FA9E..C2:FAA3  ct_c2_fa9e_alias_wrapper_running_faa4_then_jumping_8216   [alias wrapper]
- Reached from exact owner `FA48` through exact scheduled callback pointer load `A = FA9E`.
- Exact body: `JSR FAA4 ; JMP 8216`.
- Strongest safe reading: exact scheduled local wrapper that runs exact helper `FAA4` and then exact-jumps through exact common tail `8216`.

### C2:FBB7..C2:FBD0  ct_c2_masked_33ef_word_stamper_mirroring_to_x_and_x_plus_0040   [caution structural]
- Exact body begins `PHP ; REP #$30`.
- On each exact `Y`-counted iteration masks the incoming exact word with exact `33EF`, writes that exact word to exact `0000,X`, then writes exact `(word | 0010)` to exact `0040,X`.
- After each exact pair increments the exact source word by one exact `INC`, clears exact bit `0010` again through exact `AND #FFEF`, advances exact `X += 2`, decrements exact `Y`, and loops while exact `Y != 0`.
- Exits through exact `PLP ; RTS`.
- No direct exact caller is currently cached in the call-xref scan.
- Strongest safe reading: exact alternate masked word-stamping helper with the same exact paired-table shape as exact `FB97`, but preserving the broader exact `33EF` mask family instead of forcing exact `3100`.

## Honest remaining gap

- exact `C2:F943..C2:FBD0` is now honestly split and closed
- exact `C2:FBD1...` immediately becomes a local selector/data island rather than more clean linear code
- the next clean follow-on callable band should be taken from the first post-table live seam, not guessed from the middle of the exact `FBD1` table data
