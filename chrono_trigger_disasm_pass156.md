# Chrono Trigger Disassembly — Pass 156

## Summary

Pass 156 closes the old live seam rooted at exact `C2:F943`, and the seam turns out to be a whole local callback family rather than one flat owner.

The clean split is:

- one exact outside-called change-gated scheduler owner at `C2:F943..C2:F9B1`
- one exact dual-phase bootstrap owner at `C2:F9B2..C2:FA47`
- one exact overlapping late entry into that second-phase tail at `C2:FA06..C2:FA47`
- one exact active-block opener/scheduler owner at `C2:FA48..C2:FA9D`
- one exact scheduled local wrapper at `C2:FA9E..C2:FAA3`
- one exact iterative packet/service driver at `C2:FAA4..C2:FAE8`
- one exact `0217`-change-gated rebuild/submit helper at `C2:FAE9..C2:FB96`
- one exact externally-used word-stamping helper at `C2:FB97..C2:FBB6`
- one exact structurally-clear alternate word-stamping helper at `C2:FBB7..C2:FBD0`

Right after that, exact `C2:FBD1...` turns into a local selector/data island instead of continuing as obvious linear code, so I stopped at the honest structural boundary.

## Exact closures

### C2:F943..C2:F9B1
This span freezes as the exact outside-called exact `0DCE/0DCF` change-gated owner reached from exact `C2:C4F4`.

It begins `PHP ; SEP #$20` and seeds exact packet/service state `0214 = 00`, `0212 = 7E`, `020F = FF`, `0DC9 = 01`, `020D = D3FE`, and `0DCC = 6900`. It then compares exact byte `0DCE` against exact cached byte `0D77`.

On exact change it mirrors exact `0DCE -> 0D77 / 020C`, widens through exact `REP #$30`, clears exact word `4E00`, and performs one exact overlapping same-bank move from exact `7E:4E00` into exact `7E:4E02` for exact count `007D`, which is the exact two-byte opening shift of that exact `4E00` work band. After that exact shift it loads exact local callback pointer `A = F9B2`, exact count/delay `X = 0010`, and runs exact helper `8249`.

On exact no-change it stays in exact 8-bit accumulator mode and tests exact byte `00C0`. Exact nonzero exits immediately. Exact zero continues into one more compare lane `0DCF` against exact cached byte `0D78`. When those exact bytes differ, it widens through exact `REP #$30`, uses exact current offset word `0DC1`, and clears exact paired word bands `4E0A,X` and `4E4A,X` in exact `X += 2` steps while exact `X < 0040`. That exact lane then loads exact local callback pointer `A = FA06`, exact count/delay `X = 0010`, and again runs exact helper `8249`.

It exits through exact `PLP ; RTS`.

Strongest safe reading: exact outside-called owner that watches exact change bytes `0DCE/0DCF`, seeds the live packet family, opens or clears exact `4E00`-family work bands, and schedules either exact callback `F9B2` or exact shared late-entry callback `FA06` through exact helper `8249`.

### C2:F9B2..C2:FA47
This span freezes as the exact first/full owner reached through the exact scheduled local callback pointer `F9B2` from exact owner `F943`.

It begins `REP #$30` and seeds exact bootstrap state:
- exact `0DD0 = 0080`
- exact `0DC5 = 4E0A`
- exact `0DC3 = 0000`
- exact `0DC1 = 0000`
- exact `0210 = 5E00`
- exact `0DD2 = 0008`
- exact `0DD4 = 7800`
- exact `0DD6 = 5E00`
- exact `0DC7 = 3101`

It then runs exact `JSL C2:0003` and exact helper `FAA4`.

After that exact first phase it restores exact `X` through exact `PLX`, narrows to exact 8-bit accumulator mode, derives exact byte `0DC1` from exact `0DD2`, snapshots exact word `0DC5 -> 26`, derives exact nibble byte `28 = (0DC7 - 1) & 0F`, mirrors exact byte `0DCF -> 020C / 0D78`, widens again, and uses exact saved base `26` plus exact nibble byte `28` to restage exact `0DC5`.

That shared second-phase tail then seeds exact `0DC7 = 3941`, `0DD2 = 0008`, `0DD4 = 7A00`, `0DD6 = 6200`, and exact packet base `0210 = 6200`, runs exact `JSL C2:0003`, exact helper `FAA4`, and exits through exact jump `8216`.

Strongest safe reading: exact dual-phase bootstrap owner whose first phase seeds the exact `5E00 / 7800 / 3101` packet family and whose second shared phase restages exact `0DC5 / 0DC7 / 0DD2 / 0DD4 / 0DD6 / 0210` for the exact `6200 / 7A00 / 3941` follow-up before exact jump `8216`.

### C2:FA06..C2:FA47
This exact overlapping callable late entry is structurally real because exact owner `F943` directly schedules exact callback pointer `A = FA06`.

It lands inside the exact second-phase tail of exact owner `F9B2`, starting with the exact mirror `0DCF -> 020C / 0D78`, clearing exact `0DC3`, restaging exact `0DC5`, seeding exact `0DC7 = 3941`, exact `0DD2 = 0008`, exact `0DD4 = 7A00`, exact `0DD6 = 6200`, exact `0210 = 6200`, then running exact `JSL C2:0003`, exact helper `FAA4`, and exact jump `8216`.

Strongest safe reading: exact overlapping scheduled late entry into the shared exact second-phase tail of exact owner `F9B2`.

### C2:FA48..C2:FA9D
This span freezes as the exact second scheduler owner in the family.

It begins `PHP ; SEP #$20`, seeds exact packet bytes `0214 = 00`, `0212 = 7E`, clears exact `0DC3`, then widens through exact `REP #$30`. In that widened lane it clears exact `0DC1`, derives exact active block base `X = Y = (0DC5 & FFC0)`, zeroes the first exact word at that block base, and performs one exact overlapping same-bank move from exact `7E:[base]` into exact `7E:[base+2]`. Because the exact move count is derived from exact `0DD0` through three decrements before `MVN`, that exact move is the exact two-byte opening shift of the current active block size.

The tail reseeds exact packet/setup words `0210 = 5E00`, `0DC7 = 3101`, `0DD2 = 0008`, `0DD4 = 7800`, and `0DD6 = 5E00`, then schedules exact local callback `FA9E` through exact helper `8249` and exact `X = 0010`. After that exact schedule it runs exact `JSL C2:0003` and exits through exact `PLP ; RTS`.

Strongest safe reading: exact owner that opens the exact active `0DC5` block by two bytes, reseeds the exact `5E00 / 7800 / 3101` packet family, schedules exact local callback `FA9E`, and runs exact `C2:0003`.

### C2:FA9E..C2:FAA3
This short exact wrapper is a real scheduled entry because exact owner `FA48` loads exact callback pointer `A = FA9E` into exact helper `8249`.

Exact body: `JSR FAA4 ; JMP 8216`.

Strongest safe reading: exact scheduled local wrapper that runs exact helper `FAA4` and then exact-jumps through exact common tail `8216`.

### C2:FAA4..C2:FAE8
This span freezes as the exact iterative packet/service driver shared by exact `F9B2`, exact `FA48`, and exact local wrapper `FA9E`.

It begins with exact `JSR 821E`, then `REP #$10 ; SEP #$20`, mirrors exact `0DC9 -> 0213`, runs exact `JSL C2:0009`, and then exact local helper `FAE9`.

After that exact helper it checks exact status byte `0215`.

- exact `0215 == 00` returns immediately
- exact `0215 != 05` retries from the exact `821E` head
- exact `0215 == 05` advances exact byte `0DC1 = (0DC1 & E0) + 80`, exact byte `0DC7 = (0DC7 & C0) + 41`, clears exact `0DC3`, increments exact `0DD5` twice, restores exact `0DD2 = 08`, and loops back to the exact `821E` head

Strongest safe reading: exact shared iterative service driver that yields through exact `821E`, runs exact `C2:0009` plus exact helper `FAE9`, and on exact continuation code `0215 == 05` advances the exact `0DC1 / 0DC7 / 0DD5` cursor family before retrying.

### C2:FAE9..C2:FB96
This span freezes as the exact `0217`-change-gated rebuild/submit helper called from exact `FAA4`.

It begins `PHP ; SEP #$20` and compares exact byte `0217` against exact cached byte `0DC3`. Exact equality skips directly to the exact tail rooted at exact `FB72`. Exact inequality mirrors exact `0217 -> 0DC3`, widens through exact `REP #$20`, seeds exact submit block `9890 = 0DD4`, `9892 = 0DD6`, `9894 = 007E`, `9895 = 0400`, and runs exact helper `838E`.

Then, in a mixed exact 8/16-bit lane, it derives one exact loop count from exact byte `0234` through the repeated exact rounding lane `LSR ; ADC #00`, computes the exact destination base `X = (((0DD2 & 00F8) >> 2) + 0DC1 + 0DC5)`, and uses one exact `Y`-counted loop to stamp paired exact word tables at exact `0000,X` and exact `0040,X` from the running exact source word `((count - 1) + 0DC7 + 0010) & FFEF`.

After that exact rebuild loop it restores exact byte `0DD2 = 0234`, seeds one exact trailing exact submit block `9890 = 0DCC`, `9892 = (0DC5 & FFC0)`, `9894 = 007E`, `9895 = 0DD0`, runs exact helper `838E`, and exits through exact `PLP ; RTS`.

Strongest safe reading: exact helper that optionally rebuilds paired exact `4E00`-family word bands when exact `0217` changes, then always emits one exact trailing exact submit rooted at exact `0DCC` and the current exact `0DC5` block.

### C2:FB97..C2:FBB6
This exact helper is clean and externally anchored, with real exact callers at exact `C2:D150`, exact `C2:D3FB`, exact `C2:E4F1`, and exact `C2:E4FC`.

Exact body:
- exact `PHP ; REP #$30`
- exact `AND #00EF ; ORA #3100`
- exact `STA 0000,X`
- exact `ORA #0010 ; STA 0040,X`
- exact `INC A ; AND #FFEF`
- exact `INX #2 ; DEY ; BNE`

Strongest safe reading: exact masked word-stamping helper that writes one exact `3100`-tagged word stream into exact table `X` and one exact `+0010` mirrored partner into exact table `X + 0x40`.

### C2:FBB7..C2:FBD0
This exact helper is structurally clear but still less anchored than exact `FB97`, because there is no direct exact caller in the current call-xref cache.

Its exact loop shape is the same paired-table writer as exact `FB97`, but the first exact mask is `AND #33EF` instead of exact `AND #00EF`, after which it writes the exact word to `0000,X`, writes exact `(word | 0010)` to `0040,X`, then does the same exact `INC / AND #FFEF / INX += 2 / DEY / BNE` progression.

Strongest safe reading: exact alternate paired-table word-stamping helper with the same exact two-table mirror shape as exact `FB97`, but preserving the broader exact `33EF` mask family.

## Honest remaining gap

- exact `C2:F943..C2:FBD0` is now honestly split and closed
- exact `C2:FBD1...` immediately becomes a local selector/data island, not more clean linear code
- the next clean callable seam should be taken after that exact table island instead of guessed from the middle of the exact `FBD1` data
