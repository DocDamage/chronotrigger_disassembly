# Chrono Trigger Disassembly Progress — Pass 124

This pass stayed on the exact seams left by pass 123 and closed two real owner blocks: the next continuation-family lane after `B31C`, and the first actual caller/owner above the `C20F` substitution family.

## 1. `C2:B35D..C2:B48D` is not loose follow-up glue — it is the next exact continuation-family owner block

The first small closure is easy but important.

`B35D..B364` is an exact tail stub:

```asm
C2:B35D  JSR $EAC2
C2:B360  INC $68
C2:B362  JMP $B979
```

That matters because it proves the block immediately after `B31C` is not one monolithic mystery blob. The real owner starts at `B365`.

### `B365..B3AD` freezes as a status-gated progress watcher

The byte flow is direct:

```asm
C2:B365  LDX #$C042
C2:B368  JSR $ED31
C2:B36B  INC $68
C2:B36D  LDA $84
C2:B36F  STA $83
C2:B371  JSR $E984
C2:B374  BIT $0D1D
C2:B377  BMI $B38A
C2:B379  BVS $B3AB
```

That already splits the body into three exact lanes:
- clear path -> local watcher logic
- negative-bit path -> `0F48/0F49` lane
- overflow path -> exact jump `9A98`

The clear path is exact too:

```asm
C2:B37B  JSR $B520
C2:B37E  LDA $84
C2:B380  CMP $83
C2:B382  BEQ $B389
C2:B384  STA $83
C2:B386  JSR $EAC2
C2:B389  RTS
```

So the nonnegative/nonoverflow case is just a watcher:
- run exact helper `B520`
- compare exact byte `84` against the saved byte `83`
- only rerun `EAC2` when the byte changed

The negative-bit lane is also exact:
- if exact byte `0F49 == 0`, jump straight through `EACC`
- otherwise rerun `EAC2`
- load exact selector byte `54 = 0F48`
- increment exact byte `68`
- decrement exact byte `0D78`
- run exact helpers `B9E1` and `BB50`
- exit through exact selector `FBE3 -> 8385`

That is enough to freeze `B365..B3AD` as a real status-gated watcher block, not a random spillover after `B31C`.

### `B3AE..B3E5` is the dispatcher above the next loader

This piece turned out to be a tight three-way exact dispatcher:

```asm
C2:B3AE  LDA #$6D
C2:B3B0  STA $0D13
C2:B3B3  JSR $E984
C2:B3B6  BIT $0D1D
C2:B3B9  BMI $B3E6
C2:B3BB  BVS $B3C0
C2:B3BD  JMP $B6D3
```

So the split is exact:
- negative-bit path falls into the downstream table-loader at `B3E6`
- overflow path runs the local `BA4F` lane
- clear path jumps to already-visible owner `B6D3`

The overflow lane is exact too:
- `8255` with `A = 04`
- `EAC2`
- `68--`
- `F566`
- `1A18 = FF`
- `54 = 0419 + 0B`
- `0F4C = 00`
- `BA4F`
- exact selector tail `FBE3 -> 8385`

That freezes `B3AE` as the real dispatcher that chooses between the local overflow finalizer, the downstream `B6D3` lane, and the negative-bit record loader.

### `B3E6..B48D` is the exact `FF`-record loader that seeds `0DBD/0DC0/0DBF` before `BE79`

This was the big closure in the range.

The first part computes an exact record offset from exact byte `0F4C`:

```asm
C2:B3F2  LDA #$0C
C2:B3F4  STA.l $004202
C2:B3F8  TDC
C2:B3F9  LDA $0F4C
C2:B3FC  STA.l $004203
...
C2:B409  REP #$30
C2:B40B  LDA.l $004216
C2:B40F  STA $00
```

So this block multiplies exact byte `0F4C` by exact stride `0x0C`, stores the product in direct page `00`, and uses that as a table offset.

It then builds an exact compare gate:
- `0F4D = 0419 + 041A`
- mirror that same exact byte into `71`
- rerun exact settlement/search service `8820`
- `0F4E = FF`
- run exact helper `BC22`
- store the result into exact byte `0F4F`
- reject the lane when exact byte `9A97 < 0F4F`

Only after that exact gate passes does it seed the continuation/export control bytes:

```asm
C2:B43D  LDX $00
C2:B43F  LDA.l $CC2141,X
C2:B443  AND #$C0
C2:B445  STA $0DBD
C2:B448  LDA.l $CC2140,X
C2:B44C  AND #$1F
C2:B44E  STA $0DC0
```

Then it overlays one exact local mode bit pair from exact table `FF:1ACB[2*0F4C]`:
- mask low bit
- convert that exact bit into `04` or `08`
- OR the result into exact control byte `0DBD`

Then the tail is exact:
- `0DBF = 9AC9`
- `68++`
- `54 = 08`
- mirror exact `08` into `0D9C` and `0DBB`
- clear exact byte `0DBE`
- if `0DBD.bit3 != 0`, run exact helper `8AD5`
- run exact helper `BE79`
- increment exact byte `C1`
- return

That is enough to say this cleanly:

> **`C2:B3E6..C2:B48D` is the exact negative-bit continuation/export record loader that indexes fixed-size `FF` records from `0F4C`, validates one exact compare gate, seeds exact control bytes `0DBD/0DC0/0DBF`, seeds the continuation lane for exact span `08`, and hands off into `BE79`.**

### This pass also strengthens the meanings of `0DBD/0DC0/0DBF`

Pass 122 already proved those bytes matter. Pass 124 makes the ownership much stronger:
- `0DBD` is not just a bucket byte — it is assembled by multiple exact `CC/FF` record families plus exact overlay bits
- `0DC0` is not just a companion preset nibble — it is another exact low-field control byte pulled from multiple record families
- `0DBF` is not only a sign/bucket tail byte anymore — it is also seeded directly from exact record data in the new `B3E6` lane

## 2. The owner block above `C20F` starts at `C2:C2FF`, not somewhere vaguely “around C2FA”

The first important cleanup here is structural.

The bytes at `C2:C2FF` begin with an exact `PHP`, and the matching `PLP ; RTS` lands at `C394..C395`. That is the real owner boundary.

### `C2:C2FF..C2:C395` is the exact caller/owner above `C20F`

The first half of the body shows the shape immediately:

```asm
C2:C2FF  PHP
C2:C300  INC $C9
C2:C302  LDX #$C19C
C2:C305  JSR $ED31
C2:C308  REP #$30
C2:C30A  LDA #$21FF
C2:C30D  STA $4E44
...
C2:C31C  MVN $7E,$7E
```

Then it does the same thing again for exact window `4E5C/4E5E`.

So the front of the owner block is exact:
- increment exact byte `C9`
- emit exact selector packet `ED31` with `X = C19C`
- seed exact word `21FF` at `4E44` and shift exact `0x001A` bytes from `4E44 -> 4E46`
- seed exact word `21FB` at `4E5C` and shift exact `0x0002` bytes from `4E5C -> 4E5E`

Then the live helper chain freezes:

```asm
C2:C330  LDX #$FC4C
C2:C333  JSR $8385
C2:C336  JSR $C43A
C2:C339  JSR $821E
C2:C33C  LDX #$C1B9
C2:C33F  JSR $ED31
C2:C342  JSR $C3E4
C2:C345  JSR $C456
C2:C348  JSR $C495
C2:C34B  JSR $C57A
```

Then the imported block copies are exact, not approximate:
- exact `0x0008` bytes `FF:9C70 -> 7E:94E0`
- exact `0x0008` bytes `FF:9C70 -> 7E:94E8`
- exact `0x0008` bytes `FF:CBB4 -> 7E:94B0`
- exact `0x0030` bytes `FF:CBE4 -> 7E:9520`

And the tail is exact too:
- `SEP #$20`
- exact helper `86DD`
- exact byte `0D13 = 1C`
- exact helper `984A`
- exact selectors `FBE3 -> 8385` and `FBFF -> 8385`
- exact `PLP ; RTS`

That closes the owner above `C20F` in a real way instead of just carrying `C20F` as “the called helper under C184.”

### `C396..C3B3` and `C3B4..C3E0` are exact follow-up wrappers, not random adjacent glue

`C396..C3B3` is exact and tiny:
- `PHP ; SEP #$20`
- exact `0D13 = 1C`
- `REP #$30`
- exact clears of `3446`, `3448`, `3486`, and `3488`
- exact selector `FBE3 -> 8385`
- `PLP ; RTS`

`C3B4..C3E0` is the next exact wrapper:
- `PHP ; SEP #$20`
- latch exact selector byte `0417 -> 54/55`
- exact selector packet `ED31` with `X = C1F6`
- exact word `0D0E = 0189`
- exact word `0D77 = FFFF`
- exact byte `0D15++`
- exact selectors `FBE3 -> 8385` and `FBFF -> 8385`
- exact `PLP ; JMP E923`

So the `C2FF` owner does not just call one black box. It sits on top of a small exact wrapper family that is now bounded correctly.

### `C3E1..C417` is an exact ten-entry table-driven quad writer

This helper is precise enough to freeze too.

The loop shape is direct:

```asm
C2:C3E1  PHP
C2:C3E2  REP #$30
C2:C3E4  LDA #$0009
C2:C3E7  STA $00
...
C2:C414  BPL $C3E9
C2:C416  PLP
C2:C417  RTS
```

Inside the loop it does this exactly:
- use exact word table `C41B + 2*index` as destination `Y`
- read exact selector word `C42F + index`
- XOR that exact selector against exact mirror lane `0F09 + index`
- mask exact low bit
- choose exact base word `1530` or `1534`
- write one exact four-word pattern to `Y + 0000`, `Y + 0002`, `Y + 0040`, and `Y + 0042`

That freezes both the helper and its exact local tables:
- `C41B..C42E` = exact ten-word destination table
- `C42F..C438` = exact ten-byte selector/XOR table, currently all zero in ROM

## What pass 124 honestly did **not** finish

The next real seams are now:
- `C2:B48E..C2:B6D2`
- `C2:C439..C2:C57A`

And the broader noun hunt is still open for:
- `0D8B / 0D8C / 0D90`
- `0F0F / 0D1F`
- `0F48 / 0F49 / 0F4C / 0F4D / 0F4E / 0F4F`
- the higher system-facing name for `C2:A886..AA30`
