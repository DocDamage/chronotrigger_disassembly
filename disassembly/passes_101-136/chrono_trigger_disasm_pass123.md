# Chrono Trigger Disassembly Progress — Pass 123

This pass stayed on the exact seam left by pass 122 and closed two real ownership gaps instead of just renaming callsites.

## 1. `C2:B17F..C2:B1F7` is the signed-`0DBD` continuation tail worker, and `C2:B200..C2:B35C` is the real loader/probe/builder/finalizer chain behind it

The first thing that snapped into place is that `B17F` is not a random loose tail. It is the exact signed continuation worker that seeds `0DBF`, runs the shared `821E -> E984 -> B83E` loop, watches exact status bits in `0D1D`, and only exits on the exact bit6 case.

The proof is direct in the bytes:

```asm
C2:B17F  LDA #$B2
C2:B181  BIT $0DBD
C2:B184  BMI $B188
C2:B186  LDA #$8A
C2:B188  STA $0DBF
...
C2:B1A5  JSR $821E
C2:B1A8  JSR $E984
C2:B1AB  JSR $B83E
C2:B1AE  BIT $0D1D
C2:B1B1  BVS $B1C7
C2:B1B3  BPL $B1A5
```

That freezes the sign split:
- negative `0DBD` keeps exact tail byte `B2`
- non-negative `0DBD` forces exact tail byte `8A`

Then the status flow freezes too:
- `bit6 == 0` and `bit7 == 0` loops immediately
- `bit6 == 0` and `bit7 != 0` falls into the `0DBC` gate
- `bit6 != 0` exits through the shared tail

The `0DBC` gate is also exact now:
- zero runs exact helper `EACC`
- nonzero runs exact helpers `8F55` and `B31C`
- both paths loop back into the same `821E/E984/B83E` body

The end tail is exact too, not fuzzy:
- `54 = 0415`
- clear bit `0x04` from `0D13`
- clear `0D9A`
- run `F566`
- run `8255` with `A = 40`
- zero-fill exact WRAM window `7E:5080..7E:547F`
- exit through exact selector `FBFF -> 8385`

That already closes one big ownership hole.

### The other half of that seam is now exact too

`B1F8` is just an exact wrapper:

```asm
C2:B1F8  LDA #$CA
C2:B1FA  STA $0DBD
C2:B1FD  JMP $B18B
```

And `B200` is the real `04C9`-driven sibling loader, not generic continuation glue.

It seeds `0DBD` from `04C9` exactly:
- `CD -> 01`
- `CE -> 06`
- otherwise `02`

Then it runs the same basic loop frame:
- setup through `AF42`
- `821E`
- `E984`
- exact local helper `B24A`
- status test on `0D1D`
- zero/nonzero split through exact probe byte `0DBC`
- nonzero path into exact helpers `B2A7` and `B31C`
- bit6 exit into the already-frozen shared tail at `B1C7`

So the continuation lane is no longer “B17F plus some mystery nearby code.” It is now a real exact family:
- `B17F..B1F7` = signed tail worker
- `B1F8..B1FF` = fixed wrapper into the common body
- `B200..B249` = `04C9`-driven sibling loader
- `B24A..B2A6` = span/probe subhelpers
- `B2A7..B35C` = builder/finalizer continuation

## 2. `C2:B24A..C2:B2A6` closes as the exact span-clamp and probe lane

`B24A` turned out to be much cleaner than expected.

It computes exact byte delta `54 - 0DBB`, compares that against exact limit byte `73`, and only clamps when the delta is too large. The clamp branch is chosen by exact `5A.bit3`:

- set -> force `54 = 0DBB`
- clear -> force `54 = (73 - 1) + 0DBB`

Then it runs exact helper `B275` and always writes exact phase byte `0D75 = 02`.

That makes `B24A` the exact pre-probe span clamp for the sibling loop, not generic arithmetic.

`B275` is exact too:
- clears `0DBC`
- mirrors exact byte `54 - 0DBB` into `71`
- compares the same byte against `0DBE`
- mirrors the current byte into `0DBE`
- reruns `EAC2` only when that mirrored byte changed
- always reruns exact settlement/search service `8820`

Then it has a second exact gate:
- if `0DBD == 0`, return immediately
- otherwise compare exact source byte `9A9B[FF:CF2B,X]` against exact threshold byte `FF:CF32,X`
- failing that compare forces exact probe byte `0DBC = 02`

That is enough to freeze the actual meanings of the nearby WRAM bytes much harder:
- `0DBC` is the probe/result gate byte for this lane
- `0DBE` is the mirrored delta/span byte from `54 - 0DBB`
- `0D75` is the phase byte that flips between the probe and finalizer stages

## 3. `C2:B2A7..C2:B35C` closes as the accepted-slot builder plus post-accept finalizer

`B2A7` is not vague builder glue anymore.

It does all of this exactly:
- copies exact `0x0008` bytes from `FF:CBAC -> 7E:9588`
- fills the exact `0F63` marker band with `FFFF`
- writes exact word `0001` into `0F63 + 2*(0DBE & 3)`
- runs exact helper `8F6C`
- reruns exact settlement/search service `8820` with `71 = 0DBE`
- uses exact local remap table `B315 = 00 02 01 03 04 05`
- uses exact long table `FF:CF2B,X` plus exact byte `6F`
- increments one exact slot field `002F,X`, but only below exact hard cap `63`
- reruns `8820`
- commits through exact helper `9137`

So that routine is now an exact accepted-slot builder / selected-slot updater.

`B31C` is the exact finalizer that comes after it:
- `04CB = 01`
- `04C9 = 2400[0F00]`
- if that byte is exact `C9`, rerun exact preset chooser `B10D`
- always run exact helpers `87D5` and `AE20`
- if exact byte `2500[0F00] == 0`, clear exact mode byte `0DBD`
- reload exact byte `2400[0F00]`
- run exact helpers `F2F3` and `AFED`
- leave the lane in exact phase `0D75 = 01`

That means the whole mid-lane is now mechanically exact instead of hand-wavy.

## 4. `C2:C20F..C2:C2F9` is a real local substitution helper family, not just “the called finalizer under C184”

The second big closure this pass is the helper rooted at `C20F`.

Pass 122 already proved `C184` calls it. Pass 123 closes what it actually is.

### `C20F..C239` is the exact driver

The driver body is direct:

```asm
C2:C20F  REP #$30
C2:C211  LDX #$0408
C2:C214  LDY #$0F00
C2:C217  LDA #$0008
C2:C21A  MVN $7E,$7E
C2:C21D  SEP #$30
C2:C21F  STZ $04
C2:C221  LDA $54
C2:C223  SEC
C2:C224  SBC #$0F
C2:C226  TAX
C2:C227  JSR $C23A
...
C2:C231  JSR $C23A
C2:C234  JSR $C286
C2:C237  JMP $C5C7
```

That freezes the high-level role:
- exact `0408 -> 0F00` seed
- first local substitution pass using `X = 54 - 0F`
- second local substitution pass using the `04` slot captured by the first pass
- exact `C286` normalization
- fixed tail to `C5C7`

So `C20F` is an exact two-pass local substitution driver over the `0F00` work buffer.

### `C23A..C26B` and `C26C..C285` are the real worker pair

`C23A`:
- uses exact local identity map `C2BD = 00 01 02 03 04 05 06 07`
- stores exact byte `00` into `0F00[Y]`
- loads exact replacement byte `01` from `2993[Y]`
- uses exact seven-entry pointer table `C2C5`
- pulls one exact variable-length sequence from bank `C2`
- copies that sequence into exact staging buffer `969A`
- then runs exact helper `C26C`

`C26C`:
- walks the staged sequence backward
- treats each sequence byte as exact `Y`
- when `0F00[Y]` still equals the original exact source byte `00`, rewrites it to exact replacement byte `01`
- records the last rewritten slot into exact local byte `04`

That makes the family much more concrete:
- `C23A` loads one substitution rule
- `C26C` applies it backward over the staged slot list
- `04` captures the last affected slot for the second pass

### `C286..C2BC` is the special-bit reconciler

This helper is exact too:
- compute `00 = 0F00 | 0F01`
- reconcile exact bytes `0F06` and `0F07`
- preserve / restore the special exact values `10` and `20`
- force `0F06 = 10` when bit `0x10` is absent
- force `0F07 = 20` when bit `0x20` is absent

That is enough to call it what it is: a local special-bit reconciliation helper for the `0F00` substitution buffer.

### The tables are frozen too

- `C2BD..C2C4` = exact eight-byte identity slot map
- `C2C5..C2D2` = exact seven-entry substitution sequence pointer table
- `C2D3..C2F9` = exact variable-length substitution sequences consumed by the rule loader

That means the whole `C20F` family is now properly owned instead of hanging around as a black box called by `C184`.

## What pass 123 honestly did **not** finish

I did not overclaim the next adjacent blocks.

The real next seams now are:
- `C2:B35D..C2:B48D`
- `C2:C2FA..C2:C340`

And the broader noun hunt is still open for:
- `0D8B / 0D8C / 0D90`
- `0F0F / 0D1F`
- `0DBD / 0DC0 / 0DBF`
- the higher system-facing name for `C2:A886..AA30`
