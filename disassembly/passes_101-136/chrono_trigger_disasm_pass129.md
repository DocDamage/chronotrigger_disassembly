# Chrono Trigger Disassembly — Pass 129

## Scope
- close the remaining continuation-family descriptor/entry seam at `C2:BECE..C2:BEE5`
- close the downstream post-substitution dispatch-target seam at `C2:CA67..C2:CC0D`

## Starting point
- previous top-of-stack: pass 128 froze `C2:BC6F..C2:BECD` and `C2:C949..C2:CA66`
- live seam packet still had two open bands: `C2:BECE..C2:BEE5` and `C2:CA67..C2:CC0D`

## Work performed
- decoded the remaining local descriptor/data bytes after the new `BE79` owner and proved that `BEDC` is a seeded entry stub falling directly into the already-frozen `BEE6` row loop
- reconstructed both exact dispatch targets behind the `CA63` root and split the larger `CA67..CC0D` band into owner / wrapper / descriptor / scheduled-poller / packet-emitter pieces
- validated the internal split points with direct call hits where available (`CAF3`, `CB8C`, `CBEB`, `CBF7`) and with exact `RTS/JMP` boundaries where they were not directly called

## Findings

### 1. `C2:BECE..C2:BEE5` is not mystery code; it is two local selector descriptors plus one seeded fallthrough entry into `BEE6`
The remaining bytes after `BE79` break cleanly into three exact pieces:

#### `C2:BECE..C2:BED4`
- exact 7-byte local selector descriptor consumed by `BE79` through exact helper `8385`
- exact bytes: `40 58 80 2E 7E 00 02`

#### `C2:BED5..C2:BEDB`
- second exact 7-byte local selector descriptor consumed by `BE79` through exact helper `8385`
- exact bytes: `00 5C 00 36 7E 00 04`

#### `C2:BEDC..C2:BEE5`
- exact callable entry used by `BE79`
- begins with `PHP ; REP #$30`
- seeds exact packet base word `61 = 3662`
- clears exact row/index word-byte `71 = 0000`
- then falls directly into the already-frozen `BEE6` settlement row packet loop

So the open continuation-family seam was not hiding new worker logic after all; it was just the final local descriptors plus one short seeded entry that reuses the proven `BEE6` loop.

### 2. `C2:CA67..C2:CAD8` is the first real dispatch target behind `CA63`
This target:
- runs exact selector packet `ED31` with exact selector word `BF05`
- seeds exact base word `61 = 2E00`
- writes exact byte `020C = 04`, or exact byte `020C = 05` when exact word `0D7C != 0`
- writes exact word `0DC5 = 5E00`, exact word `020D = CF3B`, and exact byte `020F = FF`
- runs exact helper `F905`
- copies exact `0x0018` bytes from exact block `9600 -> 9580`
- temporarily switches the direct page to exact `19C0`, seeds exact local parameters `00/01 = 0148`, `0E = 20CA`, `1A = 20`, and runs exact helper `F422`
- in 16-bit mode runs exact helper `FBB4` twice to write exact values `0100` into exact base `334C` and `0121` into exact base `33CC`
- emits exact local descriptor `CAD9` through exact helper `8385`

Strongest safe reading: exact first dispatch target that seeds `020C/020D/020F`, copies the `9600 -> 9580` local block, runs one `19C0` direct-page helper setup, fills the `334C/33CC` work bases, and then emits exact local descriptor `CAD9`.

### 3. `C2:CAD9..C2:CADF` is exact local descriptor data for the previous target
The bytes immediately after the first dispatch target are not code.
They are one exact 7-byte local descriptor packet consumed by `CA67`:
- exact bytes: `00 10 00 5E 7E 00 10`

### 4. `C2:CAE0..C2:CAF2` breaks into one dispatch wrapper plus one tiny mode wrapper
This band resolves into two exact pieces:

#### `C2:CAE0..C2:CAE5`
- exact second dispatch target reached through the `CA63` table
- loads exact selector word `BF48` into `X`
- jumps exact helper `ED31`
- strongest safe reading: exact dispatch-target wrapper that immediately tail-jumps into the fixed `BF48` selector packet service

#### `C2:CAE6..C2:CAF2`
- exact tiny wrapper: `PHP ; SEP #$20 ; LDA #$01 ; STA 0D13 ; JSR F643 ; PLP ; RTS`
- strongest safe reading: exact mode-`01` wrapper that only seeds `0D13` and runs `F643`

### 5. `C2:CAF3..C2:CB8B` is a real post-substitution owner, not spillover from the wrappers
This owner:
- begins `PHP ; SEP #$20`
- runs exact selector packet `ED31` with exact selector word `BF7B`
- runs exact helper `984A`
- seeds exact byte `0D13 = 01`
- seeds exact word `0D0E = 01F0`
- runs exact helpers `F5A7` and `CC4F`
- increments exact byte `0D15`
- when exact byte `0D36 != 0`, writes exact byte `38` into exact bytes `9380`, `9386`, and `938C`, then writes exact word `BF40 -> 9683`
- seeds exact math register word `$4204 = A400`
- computes exact byte `0D94 = 0F0C - 04`; when that exact result is nonnegative, widens it into the exact `5*x` form, stores it back to exact byte `0D94`, derives a second exact `5*x` value into exact byte `0D95`, and runs exact helper `8B93`
- seeds exact word `0D92 = 12EC`
- mirrors exact math result `$4214 -> 0D98`
- runs exact helpers `A0E7` with exact `Y = 9500`, then `C805`
- emits exact selector chain `FBE3 -> FC37 -> FBFF` through exact helper `8385`
- exits `PLP ; RTS`

Strongest safe reading: exact post-substitution owner that seeds the `BF7B` selector path, refreshes `0D13/0D0E/0D15`, performs one exact `0F0C`-derived math/setup lane into `0D94/0D95/0D92/0D98`, then runs `A0E7`, `C805`, and the fixed `FBE3/FC37/FBFF` selector tail.

### 6. `C2:CB8C..C2:CBEA` is one owner with an inline scheduled poller body
The band beginning at `CB8C` is real code and resolves into two connected exact pieces:

#### `C2:CB8C..C2:CBBE`
- clears exact latch byte `0F0F`
- tests exact bit `0x40` from exact long byte `7F:01CF`
- when that exact bit is set, branches directly into the downstream exact poller body at `CBBF`
- otherwise loads exact byte `0F0E` from exact byte `02AE`, or from exact table `29AE,X` when exact word `0D32 != 0`
- when exact byte `0F0E == 3E`, skips the scheduled path
- otherwise increments exact latch byte `0F0F`, seeds exact word `02 = 0108`, runs exact helper `CBF7`, then in 16-bit mode seeds exact callback pointer `A = CBBF`, exact delay/count `X = 0010`, and runs exact helper `8249`
- returns with exact `RTS`

#### `C2:CBBF..C2:CBEA`
- exact scheduled poller / wait body
- waits until exact long hardware/status byte `002141 == 0`
- then writes exact packet bytes `1E00 = 14`, `1E01 = 3E`, seeds exact word `02 = FF01`, and runs exact helper `CBEB`
- then loops until exact low nibble of exact long hardware/status byte `002143` becomes nonzero
- exits through exact jump `8216`

Strongest safe reading: exact `0F0F/0F0E` owner that either schedules or directly enters a hardware/status poller body rooted at `CBBF`.

### 7. `C2:CBEB..C2:CC0D` is the exact two-stage packet emitter used by the previous owner and later callers
This helper:
- seeds exact bytes `1E02 = 80` and `1E03 = 80`
- runs exact long helper `C7:0004`
- then seeds exact byte `1E00 = 81`
- mirrors exact local word `02/03` into exact packet bytes `1E01/1E02/1E03`
- runs exact long helper `C7:0004` again
- exits `RTS`

So this is the exact two-stage packet emitter that materializes the staged `1Exx` packet fields built by `CB8C` and reused later.

## Strong labels / semantics added
- exact local descriptor packets at `BECE` and `BED5`
- exact seeded fallthrough entry at `BEDC`
- exact first/second dispatch targets behind `CA63`
- exact local descriptor packet at `CAD9`
- exact post-substitution owner at `CAF3`
- exact `0F0F/0F0E` owner plus inline scheduled poller at `CB8C`
- exact two-stage packet emitter at `CBEB`

## Still unresolved
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B/0D8C/0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
- the next code seam now naturally moves downstream from the newly closed `CA67..CC0D` band

## Next recommended target
- `C2:CC0E..C2:CD2A`
- `C2:CD2B..C2:CE85`
- broader nouns for `7E:0F0F`, `7E:0D1F`, and the `0D8B/0D8C/0D90` family
