# Chrono Trigger Disassembly — Pass 159

## Summary

Pass 159 closes the exact end-of-bank callable family after pass 158, and it fixes one important exact seam mistake from the prior handoff: the real exact callable heads are at `C2:FEFB` and `C2:FF26`, not at exact `C2:FEFA` and exact `C2:FF27`.

This pass freezes:

- exact `C2:FEFB..C2:FF25` as one exact `PHP ... RTL` owner that clears upper exact bits in `0101`, runs exact helper `EB89` with exact `X = BFE8`, indexes exact long selector table `FF:FBEA` through exact byte `54`, writes exact byte `04` into exact slot `2E01,X`, and emits one exact local exact `8385` packet using exact pointer `FA3C`
- exact `C2:FF26..C2:FF86` as one exact `PHP ... RTS` owner that mirrors exact bytes `0F02/0F00/0F01` into exact work rows `1800/1900/1811/1817`, runs exact helpers `F46F` and exact local helper `FF87`, bumps exact byte `0D15`, temporarily binds direct page to exact `1800`, runs exact helper `F292`, copies one exact `0x40`-byte block `1800 -> 1900` through exact `MVN 7E,7E`, restages exact word/byte state at `190E/1919`, and derives exact byte `0F05` from exact word `1814 >> 2`
- exact `C2:FF87..C2:FFA3` as one exact local helper that copies one exact 6-byte source block from exact bank `D1` into exact WRAM `95BA`, mirrors that exact 6-byte block into exact WRAM `963A`, increments exact byte `0D15`, and returns

This pass also freezes the exact repeated/overlap material immediately after that helper so it stops masquerading as new owners:

- exact `C2:FFA4..C2:FFA7` as one exact overlap tail, not one exact owner
- exact `C2:FFA8..C2:FFC0` as one exact late exact tail clone of the exact `FF26` restage/finalize lane
- exact `C2:FFC1..C2:FFDD` as one exact local duplicate of exact helper `FF87`
- exact `C2:FFDE..C2:FFDF` as one exact tiny exact overlap tail
- exact `C2:FFE0..C2:FFED` as one exact late exact copy tail that reuses the exact `95BA -> 963A` mirror lane but increments exact byte `0D14` instead of exact `0D15`

## Evidence and reasoning

### C2:FEFB..C2:FF25

This exact owner begins with an exact clean `PHP`, not at the previous exact seam byte `FEFA`. The exact body is balanced and exits through exact `RTL`.

Exact body:

- `PHP ; SEP #$20`
- `LDA #$FE ; TRB $0101`
- `REP #$30`
- `LDX #$BFE8 ; JSR $EB89`
- `LDA $54 ; AND #$00FF ; ASL ; TAX`
- `LDA $FF:FBEA,X ; TAX`
- `SEP #$20`
- `LDA #$04 ; STA $2E01,X`
- `LDX #$FA3C ; JSR $8385`
- `PLP ; RTL`

Strongest safe reading: exact selector/mark/packet owner that clears upper exact bits in exact `0101`, uses exact byte `54` to select one exact `FF:FBEA` table entry, writes exact byte `04` into exact `2E01,X`, and emits one exact `FA3C` packet through exact helper `8385`.

### C2:FF26..C2:FF86

This exact owner also begins one byte earlier than the previous exact handoff claimed: exact `FF26` is the real exact `PHP` head, not exact `FF27`.

Exact body:

- `PHP ; SEP #$20`
- mirror exact byte `0F02 -> 1800` and exact `0F02 -> 1900`
- `JSR F46F`
- `JSR FF87`
- `INC 0D15`
- mirror exact bytes `0F00 -> 1811` and `0F01 -> 1817`
- `PHD ; PEA $1800 ; PLD`
- `JSR F292`
- `STZ 16`
- `PLD`
- select exact word `190E = 8898` or exact `A8A8` depending on exact `1802 >= 06`
- `TDC ; LDX #$1800 ; LDY #$1900 ; LDA #$3F ; MVN 7E,7E`
- restage exact `190E = C898` and exact `1919 = 40`
- `REP #$20 ; LDA 1814 ; LSR ; LSR ; SEP #$20 ; STA 0F05`
- `PLP ; RTS`

Strongest safe reading: exact row/work-block rebuilder that seeds exact `1800/1900`, runs exact helper preparation, copies one exact 64-byte work block from exact `1800` into exact `1900`, then derives exact selector/count byte `0F05` from exact word `1814`.

### C2:FF87..C2:FFA3

Real exact caller is exact `C2:FF35`.

Exact body:

- `PHP ; REP #$30`
- `LDY #$95BA ; LDA #$0005 ; MVN 7E,D1`
- `LDX #$95BA ; LDY #$963A ; LDA #$0005 ; MVN 7E,7E`
- `INC 0D15`
- `PLP ; RTS`

The exact first `MVN` copies one exact 6-byte source block from exact bank `D1` into exact WRAM destination `95BA`. The exact second `MVN` mirrors that exact 6-byte block from exact `95BA` into exact `963A`.

Strongest safe reading: exact local six-byte import-and-mirror helper used by exact owner `FF26`.

### C2:FFA4..C2:FFA7

Exact bytes: `15 0D 28 60`.

No exact direct caller lands here, and the exact span is just the exact tail of the preceding exact helper/overlap material.

Strongest safe reading: exact overlap tail, not one exact standalone owner.

### C2:FFA8..C2:FFC0

This exact span is structurally identical to the exact back half of exact owner `FF26`, beginning at the exact restage lane:

- `LDX #$C898 ; STX $190E`
- `LDA #$40 ; STA $1919`
- `REP #$20 ; LDA $1814 ; LSR ; LSR`
- `SEP #$20 ; STA $0F05`
- `PLP ; RTS`

No exact direct caller currently lands on exact `FFA8`.

Strongest safe reading: exact late exact tail clone of the exact `FF26` finalize lane, not one exact independently proven owner.

### C2:FFC1..C2:FFDD

This exact span is byte-for-byte the same structural helper body as exact `FF87..FFA3`:

- `PHP ; REP #$30`
- exact 6-byte `D1 -> 95BA` import through exact `MVN 7E,D1`
- exact 6-byte `95BA -> 963A` mirror through exact `MVN 7E,7E`
- `INC 0D15`
- `PLP ; RTS`

No exact hot direct caller is currently cached for exact `FFC1`.

Strongest safe reading: exact local duplicate of exact helper `FF87`, but not one currently-proven hot entry.

### C2:FFDE..C2:FFDF

Exact bytes: `28 60`.

Strongest safe reading: exact tiny exact overlap tail, not one exact owner.

### C2:FFE0..C2:FFED

This exact tail is balanced only as a late-entry copy lane:

- `LDY #$963A ; LDA #$0005 ; MVN 7E,7E`
- `INC 0D14`
- `PLP ; RTS`

It reuses the exact `95BA -> 963A` copy shape but increments exact byte `0D14` instead of exact `0D15`. No exact direct caller is currently cached for exact `FFE0`.

Strongest safe reading: exact late exact copy tail / local overlap entry, not one independently anchored top-level owner.

## Honest remaining gap

- pass 158's exact seam heads were both off by one; this pass corrects them to exact `FEFB` and exact `FF26`
- exact `C2:FFEE..C2:FFFF` still does **not** decode as one clean exact owner and sits at the exact bank-end cliff
- the next pass should either close exact `C2:FFEE..C2:FFFF` as bank-end overlap/data or move to the next higher-confidence exact callable seam elsewhere after the exact bank-end cleanup
