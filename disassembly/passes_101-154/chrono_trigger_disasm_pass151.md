# Chrono Trigger Disassembly — Pass 151

## Summary

Pass 151 closes the callable/helper family that pass 150 left open at `C2:F2F3..C2:F360`, with the structural correction that the old seam end was too short. The honest closure for this family runs through exact `C2:F3CA`.

The resolved family is:

- one exact latched-byte change-handler / refresh owner at `C2:F2F3..C2:F331`
- one exact short word-copy helper at `C2:F332..C2:F336`
- one exact zero-bank record-builder owner at `C2:F337..C2:F360`
- one exact short wrapper that forces exact index width before a shared late entry at `C2:F361..C2:F363`
- one exact FF-bank length-prefixed block importer late entry at `C2:F364..C2:F377`
- one exact coordinate-to-coordinate multi-row word-swap owner at `C2:F378..C2:F3CA`

## Exact closures

### C2:F2F3..C2:F331
This span freezes as the exact latched-byte change-handler / refresh owner that checks exact incoming accumulator byte `A` against exact latch byte `0D77`, unless exact byte `0D78` is negative. On exact change or forced refresh, it mirrors exact byte `A -> 0D77 / 020C`, clears exact byte `0D78`, seeds exact workspace fields `0DC5 = 4E84`, `0DCC = 6840`, `020D = 2EB1`, `020F = CC`, `0DC9 = 01`, `0DD0 = 0080`, and then runs exact helper `FA49`.

### C2:F332..C2:F336
This span freezes as the exact short helper that copies exact word `5B -> 61` and returns immediately.

### C2:F337..C2:F360
This span freezes as the exact zero-bank record-builder owner that temporarily rebinds the data bank to exact `00`, uses exact word `5B` as the exact destination record pointer `Y`, writes exact bank byte `7E` into exact offsets `+4` and `+7`, writes exact source word `5D -> [Y+0]`, derives exact word `61 = 9000 + ((5B & 00F0) << 3)`, mirrors that exact derived word into exact `[Y+2]`, and returns with exact word `61` preserved.

### C2:F361..C2:F363
This span freezes as the exact short wrapper that forces exact `X/Y` into 16-bit mode, saves flags, and falls through into exact shared late entry `F364`.

### C2:F364..C2:F377
This span freezes as the exact FF-bank length-prefixed block importer late entry. It rebinds the data bank to exact `FF`, treats exact word `5B` as one exact FF-bank source pointer, reads the exact first byte there as the exact transfer count seed, advances past that count byte, and copies the requested exact block into exact bank-`7E` destination word `61` through exact `MVN 7E,FF`.

### C2:F378..C2:F3CA
This span freezes as the exact coordinate-to-coordinate multi-row word-swap owner. It uses exact helper `ED90` twice to derive exact row pointers `63` and `65` from exact packed coordinates `5D` and `5B` relative to exact base word `61`, derives exact horizontal and vertical extents from exact bytes `5F` and `60`, swaps exact 16-bit cells between those two exact row bands, advances both exact row pointers by exact `0x0040` per row, and repeats for the exact requested height.
