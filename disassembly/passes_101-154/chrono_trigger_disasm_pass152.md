# Chrono Trigger Disassembly — Pass 152

## Summary

Pass 152 closes the next owner family after pass 151 at `C2:F3CB..C2:F421` and opportunistically pulls in the immediately xrefed follow-on owner at `C2:F422..C2:F547`, because the seam edge scan already proved `F422` was a real callable start reached from three sites.

The resolved band is:

- one exact eight-row direct-page strip/import owner at `C2:F3CB..C2:F421`
- one exact bank-`E4` header-decode / strip-import / optional unpack-submit owner at `C2:F422..C2:F547`

A small exact data-table island now sits immediately after that owner at `C2:F548..C2:F569`; the next obvious callable band starts at exact `C2:F56A`.

## Exact closures

### C2:F3CB..C2:F421
This span freezes as the exact eight-row direct-page strip/import owner. It temporarily rebinds the exact direct page to `0x1800`, clears exact global loop byte `0022`, and then walks exact row records at direct-page bases `1800`, `1840`, `1880`, `18C0`, `1900`, `1940`, `1980`, and `19C0-0x40` by adding exact `0x0040` to `D` after each iteration. On each exact row, it mirrors exact loop byte `0022 -> 00`, selects one exact 16-bit word from the exact local table rooted at `F548` into exact row field `19/1A`, clears exact row byte `11`, seeds exact row byte `17 = 01`, runs exact helper `F422`, then runs exact helper `F69D`. After the eight exact row iterations, it seeds one exact trailer state with exact word `19/1A = 20E8`, exact byte `00 = FF`, exact byte `11 = 00`, exact byte `17 = 01`, exact byte `40 = FF`, exact byte `51 = 00`, and exact byte `57 = 01`, then returns.

### C2:F422..C2:F547
This span freezes as the exact bank-`E4` header-decode / strip-import / optional unpack-submit owner. It begins `PHP ; SEP #$30`, clears exact byte `18`, seeds exact bytes `12 = FF` and `03 = FF`, seeds exact bank bytes `1D = E4` and `20 = E4`, and increments exact global byte `0D15`. It uses the exact SNES multiplication registers: exact byte `00 -> $4202`, exact factor `05` or `0A` -> `$4203` depending on exact selector byte `01`, then adds the exact multiplication result `$4216` to one exact local base word from the exact table rooted at `F55C`. That exact computed bank-`E4` source offset is used to copy an exact 5-byte header block into exact WRAM scratch `7E:9890..9894` through exact `MVN 7E,E4`. It then masks exact byte `9894` down to its preserved bit-4 lane, derives exact selector byte `02` from the exact local table rooted at `F562`, bails out immediately when exact byte `9890 == FF`, otherwise performs a table-driven exact decode of bytes `9890..9893` through exact bank-`E4` roots at `E4:FFE0`, `E4:FFE2`, `E4:FFE4`, `E4:FFE6`, and `E4:FFE8`, seeding exact words/bytes `04/05`, `07/08`, `0A`, `0C`, and exact width byte `14`. From that exact decode, it selects one exact bank-`E4` source strip, derives one exact WRAM destination band `Y = 9582 + ((19 & 0E00) >> 4)`, and copies an exact `0x0018`-byte strip into exact bank-`7E` through exact `MVN 7E,E4`. When exact byte `01` is nonzero, it then stages exact unpack parameters into exact words/bytes `0300`, `0302`, `0303`, and `0305`, mirroring the exact computed destination word into exact `04`, and calls exact packed-stream veneer `C3:0002`.
