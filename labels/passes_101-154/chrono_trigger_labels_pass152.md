# Chrono Trigger Labels — Pass 152

## Purpose

Pass 152 closes the next owner family after pass 151 at `C2:F3CB..C2:F421` and opportunistically closes the immediately xrefed follow-on owner at `C2:F422..C2:F547`.

## Strong labels

### C2:F3CB..C2:F421  ct_c2_eight_row_direct_page_strip_import_owner_over_1800_plus_40n_using_f548_then_f422_f69d   [strong structural]
- Begins `PHP ; PEA $1800 ; PLD` and clears exact global loop byte `0022`.
- Forces exact 8-bit accumulator/index mode for the row-entry setup.
- On each exact iteration, mirrors exact loop byte `0022 -> 00`, doubles it, and uses that exact doubled index to load one exact 16-bit word from the exact local table rooted at `F548` into exact row field `19/1A`.
- Clears exact row byte `11`, seeds exact row byte `17 = 01`, runs exact helper `F422`, then runs exact helper `F69D`.
- Reenters exact 16-bit accumulator mode, advances the exact direct-page base by exact `0x0040`, and repeats until the exact new direct-page value reaches `19C0`.
- After the eight exact row iterations, seeds one exact trailer state with exact word `19/1A = 20E8`, exact bytes `00 = FF`, `11 = 00`, `17 = 01`, `40 = FF`, `51 = 00`, and `57 = 01`.
- Strongest safe reading: exact eight-row direct-page strip/import owner over exact row records `1800 + 0x40*n` that selects one exact table word from `F548` per row, then runs exact helper pair `F422 -> F69D` before seeding one exact trailer state.

### C2:F422..C2:F547  ct_c2_bank_e4_header_decode_strip_import_and_optional_c3_unpack_submit_owner   [strong structural]
- Begins `PHP ; SEP #$30`, clears exact byte `18`, seeds exact bytes `12 = FF` and `03 = FF`, seeds exact bank bytes `1D = E4` and `20 = E4`, and increments exact global byte `0D15`.
- Uses exact byte `00` as one exact multiplicand through SNES register `$4202`, chooses exact factor `05` or `0A` for `$4203` from exact selector byte `01`, and adds exact result `$4216` to one exact local base word from the exact table rooted at `F55C`.
- Uses that exact computed bank-`E4` source offset to import one exact 5-byte header block into exact WRAM scratch `7E:9890..9894` through exact `MVN 7E,E4`.
- Reduces exact byte `9894` to its preserved bit-4 lane, derives exact selector byte `02` from the exact local table rooted at `F562`, and returns immediately when exact byte `9890 == FF`.
- Otherwise performs a table-driven exact decode of exact bytes `9890..9893` through exact bank-`E4` roots `E4:FFE0`, `E4:FFE2`, `E4:FFE4`, `E4:FFE6`, and `E4:FFE8`, seeding exact words/bytes `04/05`, `07/08`, `0A`, `0C`, and exact width byte `14`.
- Selects one exact bank-`E4` strip source from that decode, derives one exact WRAM destination band `Y = 9582 + ((19 & 0E00) >> 4)`, and copies one exact `0x0018`-byte strip into bank `7E` through exact `MVN 7E,E4`.
- When exact byte `01` is nonzero, stages exact unpack parameters into exact `0300`, `0302`, `0303`, and `0305`, mirrors the exact computed destination word into exact `04`, and calls exact packed-stream veneer `C3:0002`.
- Strongest safe reading: exact bank-`E4` header-decode / strip-import owner that uses exact local tables at `F55C` and `F562`, fills exact scratch `9890..9894`, copies one exact decoded strip into exact `95xx` WRAM, and optionally submits one exact unpack job through exact veneer `C3:0002`.

## Honest remaining gap

- the owner pair `C2:F3CB..C2:F547` is now honestly closed
- exact `C2:F548..C2:F569` is a local exact data-table island and should not be mistaken for code
- the next obvious callable band starts at exact `C2:F56A`
- the next clean follow-on seam is `C2:F56A..C2:F5A6`
