# Chrono Trigger Disassembly — Pass 154

## Summary

Pass 154 closes the front half of the scheduler-serviced row worker rooted at exact `C2:F657`, plus the exact local scale-dispatch material that pass 153 only knew was “some local table around `F6D0`.”

The clean result is:

- one exact persistent row-band service loop at `C2:F657..C2:F69A`
- one exact increment-and-fallthrough alias entry at `C2:F69B..C2:F69C`
- one exact row-change pointer/front-end owner at `C2:F69D..C2:F6CD`
- four exact local scale-return stubs at `C2:F6CE..C2:F6D7`
- one exact four-word dispatch table at `C2:F6D8..C2:F6DF`
- one exact stream-scan / WRAM-submit tail at `C2:F6E0..C2:F754`
- one exact four-byte factor table at `C2:F755..C2:F758`

This pass does **not** claim the large helper immediately after that at exact `C2:F75C`; it is clearly live code, but it continues well past the old seam and deserves its own pass.

## Exact closures

### C2:F657..C2:F69A
This span freezes as the exact persistent row-band service loop scheduled by exact wrapper `F643`. It begins `REP #$30 ; PEA $1800 ; PLD ; STZ $0D73 ; SEP #$30`, so each exact sweep rebinds direct page to exact `1800` and clears exact global byte `0D73`. On each exact row band it first bails around the inner compare/update lane when exact row byte `00` is negative or exact row byte `18` is negative. Otherwise it compares exact row byte `11` against exact row byte `12`; when they match and are nonzero it decrements exact row byte `13` and only falls through to the exact helper gate when that decrement underflows. On the exact helper gate, it compares exact global bytes `0D73` and `0D75`, and when exact `0D73 < 0D75` it runs exact helper entry `F69B`. When exact row byte `18 == 00` it also runs exact helper `F871`. It then widens through exact `REP #$21`, advances the exact direct-page base by exact `0x0040` through `TDC ; ADC #$0040 ; TCD`, and repeats while the exact resulting base remains `< 1A40`. After the eight exact row bases `1800`, `1840`, `1880`, `18C0`, `1900`, `1940`, `1980`, and `19C0`, it runs exact helper `821E` and loops back to exact `F657` through exact `BRA`. Strongest safe reading: exact persistent eight-row direct-page service loop over exact row bands `1800 + 0x40*n` that conditionally runs exact helper `F69B`, conditionally runs exact helper `F871`, yields through exact `821E`, and repeats.

### C2:F69B..C2:F69C
This span freezes as the exact increment-and-fallthrough alias entry into the downstream exact row-change front-end at `F69D`. Exact body: `INC $16` and immediate fallthrough into exact `F69D`.

### C2:F69D..C2:F6CD
This span freezes as the exact row-change pointer/front-end owner. It compares exact row byte `11` against exact row byte `12`, mirrors the exact current byte `11 -> 12`, and returns immediately when the exact values match. On the exact changed path it clears exact latch byte `16`, loads exact selector byte `17`, doubles it into exact dispatch-table index `X`, widens through `REP #$30`, loads exact width/base word `14`, and runs exact local scale dispatcher `JSR ($F6D8,X)`. It stores that exact returned base word into exact `1B`. It then masks exact row word `11` to exact `0x007F`, multiplies the exact result by `4`, mirrors that exact stride into exact `1E`, and derives exact paired pointer words `1B = returned_base + 4*(11 & 007F) + 0A` and `1E = 4*(11 & 007F) + 0C`. After restoring exact 8-bit accumulator/index mode through exact `SEP #$30`, it branches directly into the downstream exact tail at `F6F7`. Strongest safe reading: exact row-change front-end that notices exact `11 != 12`, resets exact latch `16`, uses exact `17/14` through the exact local dispatch table at `F6D8` to derive one exact base word, then derives exact paired stream-pointer words `1B/1E` from exact `0A/0C` and the exact low seven bits of exact row word `11`.

### C2:F6CE..C2:F6D0
This span freezes as one exact local scale-return alias stub. Exact body in the caller’s exact 16-bit mode: `LDA #$0000 ; RTS`.

### C2:F6D1
This address freezes as one exact local passthrough alias stub. Exact body: `RTS`.

### C2:F6D2..C2:F6D3
This span freezes as one exact local double-value alias stub. Exact body in the caller’s exact 16-bit mode: `ASL A ; RTS`.

### C2:F6D4..C2:F6D7
This span freezes as one exact local scale-plus-base alias stub. Exact body in the caller’s exact 16-bit mode: `ASL A ; ADC $14 ; RTS`. Strongest safe reading: exact local `2*A + 14` return stub under the caller’s exact flag state.

### C2:F6D8..C2:F6DF
This span freezes as the exact four-word dispatch table for the exact `JSR ($F6D8,X)` lane at `F6AF`. Exact little-endian words: `F6CE`, `F6D1`, `F6D2`, and `F6D4`. Strongest safe reading: exact four-entry local scale-dispatch table selecting the exact zero / passthrough / double / scale-plus-base stubs.

### C2:F6E0..C2:F754
This span freezes as the exact stream-scan / WRAM-submit tail reached from exact `F69D`. It starts by loading exact row byte `11`; when that exact byte is negative and the current exact stream-control byte `[1E],Y` is zero, it mirrors exact byte `21 -> 16` and retries. On the exact non-negative lane with zero exact control byte, it either clears exact `16` and retries or decrements exact `16` and returns. On the exact nonzero control-byte lane it mirrors exact `[1E],Y -> 13`, loads exact paired stream byte `[1B],Y`, and when that exact value differs from cached exact byte `03` it mirrors the exact new byte into `03`, writes that exact byte to exact SNES multiplier register `$4202`, mirrors exact byte `09 -> 9692`, writes exact literal byte `6B -> 9693`, selects one exact factor byte from the exact local table rooted at `F755` through exact index byte `02`, and writes that exact factor to exact `$4203`. In exact 16-bit mode it seeds exact word `9690 = 7E54`, derives exact scratch word `22 = 8*X`, exact secondary exact offset `Y = 32*X - 1`, exact `X = 07 + $4216`, and then performs two exact `JSL $7E9690` calls: first with exact `Y = 9890`, then with exact `Y = 0022` and exact `A = 22 - 1`. It then runs exact helper `F75C`, restores exact 8-bit mode, decrements exact countdown byte `13`, and returns. When the exact paired stream byte already matches cached exact byte `03`, it skips directly to the exact `DEC 13 ; RTS` tail. Strongest safe reading: exact row-stream scan / staged WRAM-submit tail that retries on exact zero control bytes, caches exact stream byte `03`, chooses one exact local factor from exact table `F755`, configures exact `9690/9692/9693`, performs two exact `JSL 7E:9690` submits, runs exact helper `F75C`, and decrements exact countdown byte `13`.

### C2:F755..C2:F758
This span freezes as the exact four-byte factor table consumed by exact `F6E0..F754`. Exact bytes: `00 28 50 78`. Strongest safe reading: exact four-entry factor byte table used to seed exact `$4203` before the exact `7E:9690` submit lane.

## Honest remaining gap

- exact `C2:F657..C2:F758` is now honestly closed
- the next clearly live callable/helper band begins at exact `C2:F75C`
- exact `C2:F75C...` is still one larger owner family and should be taken as the next forward seam rather than guessed from the middle
