# Chrono Trigger Disassembly — Pass 153

## Summary

Pass 153 continues the family immediately after the pass-152 `F422` importer, but the first useful result is a correction: the old seam front at `C2:F56A..C2:F587` is **not** safe to freeze yet as a clean callable owner. It still reads like code-shaped bytes, but it does not currently balance as a standalone stack-clean entry and still has no direct call xrefs.

The real clean progress this pass is the solid callable/helper block immediately after that suspicious span. The resolved band is:

- one exact eight-row direct-page row-clear helper at `C2:F588..C2:F5A6`
- one exact two-phase strip staging/import owner at `C2:F5A7..C2:F5EC`
- one exact bank-`D1` source-derivation helper at `C2:F5ED..C2:F625`
- one exact `A * 0x40` row-offset helper at `C2:F626..C2:F642`
- one exact fixed scheduler wrapper around local callback `F657` at `C2:F643..C2:F656`

That means pass 152’s seam text was slightly too optimistic at the front, but the shared helpers behind it are real and now honestly frozen.

## Exact closures

### C2:F588..C2:F5A6
This span freezes as the exact eight-row direct-page row-clear helper. It begins `PHP ; PHD ; PEA $19C0 ; PLD ; SEP #$30`, seeds exact row byte `00 = FF`, clears exact row bytes `11` and `18`, then widens to exact 16-bit accumulator mode while also clearing the exact carry through `REP #$21`. It snapshots the current exact direct-page base through `TDC`, subtracts exact `0x0040`, writes the exact new direct-page value back through `TCD`, and repeats while the exact resulting direct-page base remains `>= 1800`. The exact loop therefore clears row records rooted at exact bases `19C0`, `1980`, `1940`, `1900`, `18C0`, `1880`, `1840`, and `1800`, then restores exact direct page and flags and returns.

### C2:F5A7..C2:F5EC
This span freezes as the exact two-phase strip staging/import owner. It begins `PHP ; REP #$30`, loads exact word `E4:FFE8 -> 00`, and seeds exact destination `Y = 95A2`. In its first exact phase, it repeatedly loads one exact source word through exact bank-`E4` pointer list `[00]`, copies exact `0x0018` bytes from that exact bank-`E4` source into exact bank-`7E`, advances exact source pointer word `00 += 0002`, and advances the exact destination band by exact `0x0020`, materializing exact strip starts `95A2`, `95C2`, `95E2`, `9602`, `9622`, `9642`, and `9662` before the exact `Y < 9680` guard fails. In its second exact phase, it seeds exact destination `Y = 95BA`, clears exact loop word `00`, then for exact loop values `00 = 0000..0006` runs exact helper `F5ED` to derive one exact bank-`D1` source, copies exact `0x0006` bytes from that exact derived source into exact bank `7E`, and again advances the exact destination band by exact `0x0020`, materializing exact second-phase strip starts `95BA`, `95DA`, `95FA`, `961A`, `963A`, `965A`, and `967A`, then returns.

### C2:F5ED..C2:F625
This span freezes as the exact bank-`D1` source-derivation helper used by the second phase at exact `F5A7`. In exact 8-bit accumulator mode it preserves the incoming exact byte, writes exact multiplicand `50` to exact hardware register `$4202`, writes the preserved exact input byte to exact `$4203`, then reenters exact 16-bit mode. On the exact non-negative path used by the observed callers, it snapshots the exact multiplication result from exact `$4216` into `X`, loads one exact byte from exact table `2629,X`, mirrors that exact byte into exact word/byte `041B`, uses that exact byte as an index into exact table `CD:6CEC`, keeps only the exact low byte, and transforms it into exact source word `X = 4B00 + 6*v`. It returns exact transfer length `A = 0005`, making the downstream `MVN` copy exact `0x0006` bytes. Strongest safe reading: exact bank-`D1` strip-source helper that maps one exact small selector byte into one exact `D1:4B00 + 6*v` source plus fixed exact copy length `0005`.

### C2:F626..C2:F642
This span freezes as the exact `A * 0x40` hardware-multiply helper. It preserves the incoming exact accumulator, switches to exact 8-bit accumulator mode, writes the exact incoming byte to exact hardware multiplicand register `$4202`, writes exact factor byte `40` to exact `$4203`, reenters exact 16-bit mode, snapshots exact hardware product `$4216 -> 0D2C`, mirrors that exact result into exact `Y`, restores exact flags and the exact original accumulator, and returns. Strongest safe reading: exact helper that derives one exact row/base offset `0D2C/Y = 0x40 * input_byte` while preserving the caller’s exact accumulator value.

### C2:F643..C2:F656
This span freezes as the exact fixed scheduler wrapper around local callback `F657`. It begins `PHP ; REP #$30`, clears exact words `0D2E` and `0D30`, seeds exact callback pointer `A = F657`, seeds exact delay/count `X = 0028`, runs exact helper `8249`, restores flags, and returns. Strongest safe reading: exact fixed `8249` scheduler/setup wrapper for the downstream local callback/service owner rooted at exact `F657`.

## Honest remaining gap

- exact `C2:F56A..C2:F587` is **still not honestly closed**; it currently looks more like an unresolved pre-owner/helper-or-data crossover than a proven standalone callable entry
- the next clean forward callable band now begins at exact `C2:F657`
- immediate next structural anchors are exact local helper `F69B`, exact shared helper `F69D`, and the exact local table/continuation material beginning around exact `F6D0`
