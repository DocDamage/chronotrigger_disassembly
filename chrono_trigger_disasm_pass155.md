# Chrono Trigger Disassembly — Pass 155

## Summary

Pass 155 closes the old live seam that began at exact `C2:F75C`, and it turns out that the seam was not one owner.

The clean split is:

- one exact local helper at `C2:F75C..C2:F870`
- one exact direct-page derived descriptor builder at `C2:F871..C2:F904`
- one exact alias entry at `C2:F905..C2:F90B`
- one exact shared dual-packet submit owner at `C2:F90C..C2:F942`

This pass does **not** force the next owner family at exact `C2:F943`; that band is clearly live and continues past the old seam, but it deserves its own pass.

## Exact closures

### C2:F75C..C2:F870
This span freezes as the exact local `9890`-driven row materializer and submit helper called from exact `F74D` in the downstream exact `F6E0` tail. It begins `PHP ; SEP #$30`, mirrors exact byte `06 -> 9692`, then widens through exact `REP #$31`. In that exact widened lane it derives exact word `9A8A = 8000 + ((0D72 << 1) & FF00)`, copies that exact word into `Y`, and derives the exact loop bound word `0002 = ((01 & 0F00) >> 3)`.

It then walks exact words `9890,X` in exact two-byte steps. When the current exact `9890,X` word is zero, it clears one exact `0x20`-byte row at exact destination `Y` by storing exact zero across offsets `0000..001E`. When the current exact `9890,X` word is nonzero, it masks that exact word to `07FF`, shifts it into one exact `0x20`-byte source stride, adds exact base `04`, and uses the resulting exact `X` plus exact `A = 001F` to run exact `JSL $7E9690`. After restoring the original exact selector word through `PLX`, it tests the original exact `9890,X` word with exact `BIT 9890,X`; when the exact `V` bit is set it performs one exact reverse `0x20`-byte byte-for-byte remap of the freshly materialized row through exact long table `C0:FD00`, otherwise it leaves the copied row unchanged.

After each exact row, it advances exact `Y += 0x20`, restores the exact source index progression `X += 2`, and repeats until exact `X >= 0002`.

The tail then seeds exact submit descriptor/state bytes and words `9A88/9A8C/9A8D/9A8E`, mirrors exact `02 -> 0000`, and advances exact global byte `0D73 += 02`. On the exact even lane `02 & 01 == 00`, it falls through the exact local tail rooted at `F864`, writes exact `9A8E = 2 * 02`, and performs one exact `JSR 838E`. On the exact odd lane `02 & 01 != 00`, it instead performs two exact `JSR 838E` submits while stepping exact descriptor bytes `9A88/9A89/9A8B` between the two submits. It exits through exact `PLP ; RTS`.

Strongest safe reading: exact local helper that walks the live exact `9890` selector words, materializes or clears exact `0x20`-byte rows, optionally remaps the produced bytes through exact table `C0:FD00`, then seeds exact `9A88`-family submit state and runs exact `838E` in one- or two-submit form depending on the exact parity of byte `02`.

### C2:F871..C2:F904
This span freezes as the exact direct-page-derived descriptor builder called from exact `F687` when the current exact row byte `18 == 00`. It begins `PHP ; REP #$20 ; TDC`, so it uses the caller’s exact current direct-page base as one of its exact inputs. From that exact direct-page base it derives one exact descriptor/output base in `Y` and one exact group/bit-index byte in exact `0002`, then widens through exact `REP #$30`.

In that exact widened lane it derives exact loop bound word `0004 = 8 * (02 & 000F)`, clears exact word `0008`, and seeds exact byte/word `0006 = 0F + 0D2E`. Returning to exact 8-bit accumulator mode, it rotates exact byte `0007` through exact `LSR 0007 ; ROR 0007`, seeds exact bitmask byte `0000 = 01`, and enters one exact `X += 2` loop.

On each exact loop pass it writes one exact four-byte descriptor at exact `0800,Y`:
- exact byte `0800,Y = 0006 + 22,X`
- exact byte `0801,Y = 0E + 23,X + 0D30`
- exact word `0802,Y = 0008 + 19`

It also derives one exact sign/parity test from the exact expression rooted at exact `ROR A`, exact `EOR 22,X`, and exact `EOR 0007`. When that exact test is negative, it uses exact group byte `0002` plus exact bitmask byte `0000` to set one exact bit in exact table byte `0910,Ygroup`.

After each exact descriptor it advances exact `Y += 4`, mutates exact byte `0008` through the exact lane `((0008 | 10) + 2) & EF`, shifts exact bitmask byte `0000` left twice, and repeats while exact `X < 0004`. It exits through exact `PLP ; RTS`.

Strongest safe reading: exact current-direct-page-derived descriptor/bitfield builder that writes exact four-byte records into exact `0800` and accumulates exact occupancy bits into exact `0910`, using exact local coordinate tables at exact `22/23`, exact row/state bytes `02/0E/0F/19`, and exact global bases `0D2E/0D30`.

### C2:F905..C2:F90B
This span freezes as the exact mode-`81` alias entry into the downstream exact shared packet submitter at `F90C`. Exact body: `PHP ; SEP #$20 ; LDA #$81 ; BRA $F911`. Strongest safe reading: exact wrapper entry that differs from exact `F90C` only by forcing exact packet mode byte `0214 = 81` before joining the shared exact submit body.

### C2:F90C..C2:F942
This span freezes as the exact shared dual-packet submit owner behind the exact alias entry at `F905`. It has real outside callers at exact `C2:D2BF`, `C2:D2F0`, `C2:D3DF`, `C2:E4E6`, and exact `C2:E85F`, while exact `C2:CA8F` reaches the exact `F905` alias entry.

The shared body begins `PHP ; SEP #$20 ; LDA #$80`, then seeds exact packet workspace bytes/words:
- exact `0214 = 80` for the shared entry or exact `0214 = 81` when entered through exact alias `F905`
- exact `0210 = 0DC5`
- exact `0212 = 7E`

It then runs exact `JSL C2:0003`, seeds exact byte `0213 = 20`, and runs exact `JSL C2:0009`. After that exact dual-call pair it checks exact status/result byte `0215`. When exact `0215 != 05`, it exits immediately through exact `PLP ; RTS`. When exact `0215 == 05`, it advances exact byte/word `0211 += 4` through four exact `INC` instructions and loops back to the exact `0213 / C2:0009 / 0215` check lane until exact `0215` changes.

Strongest safe reading: exact shared packet submitter that seeds exact `0210..0214`, runs the exact `C2:0003` then exact `C2:0009` packet/stream veneer pair, and when exact result byte `0215 == 05` repeatedly advances exact pointer/state byte `0211` by exact `4` before retrying the exact second-call lane.

## Honest remaining gap

- exact `C2:F75C..C2:F942` is now honestly split and closed
- the next clearly live callable/helper band begins at exact `C2:F943`
- that next owner family is already visibly real code, but it should be taken as its own pass rather than guessed from the middle
