# Chrono Trigger Disassembly — Pass 128

## Scope
- close the continuation-family seam at `C2:BC6F..C2:BECD`
- close the post-substitution helper seam at `C2:C949..C2:CA66`

## Starting point
- previous top-of-stack: pass 127 closed `C2:C7A6..C2:C946` and `C2:BB1F..C2:BC70`
- live seam packet still had two open bands: `C2:BC71..C2:BEE5` and `C2:C947..C2:CA40`

## Work performed
- corrected the exact callable entry from `C2:BC71` to `C2:BC6F` using live xref proof from `C2:B555`
- reconstructed the continuation-family owner/helper chain from `BC6F` through `BE78`, including the exact `9890 -> 0F00/0F30` rebuild lane and the exact `0F4C`-driven export lane
- reconstructed the post-substitution helper chain from `C949` through the exact `CA63` dispatch root
- proved that the open post-substitution seam does not stop at `CA40`; the exact owner at `C9E5` actually runs cleanly through `CA61`, and the next exact seam begins at the local dispatch table `CA63`

## Findings

### 1. `C2:BC6F..C2:BCAD` is the real callable owner behind the open continuation seam
Earlier seam text started at `BC71`, but that was wrong by two bytes. The exact caller at `C2:B555` targets `C2:BC6F`.

This owner:
- builds one exact composite byte from `0419 + 041A` in the high-path plus exact byte `0418`
- compares that exact composite against exact cache byte `84`
- when the exact composite did not change, returns immediately
- on change, clears exact bytes `0F4A` and `0F48`, emits exact selector `FBE3 -> 8385`, mirrors exact byte `0419 + 041A -> 71`, runs exact helper `8820`, then exact helper chain `BCAE -> BD6B`

So this is the real change-detect owner that decides when the downstream continuation/export lanes need to be rebuilt.

### 2. `C2:BCAE..C2:BD3F` is one exact rebuild lane: compact list build first, expanded live lane second
This resolves into three exact pieces:

#### `C2:BCAE..C2:BCCC`
This wrapper:
- seeds exact `0F00 = FFFF`
- copies exact `0x0016` bytes from exact block `7E:0F00 -> 7E:0F02`
- then runs exact helpers `BCCD` and `BD00`

#### `C2:BCCD..C2:BCFF`
This helper:
- uses exact byte `9A90` to select one exact mask byte from exact table `FF:F9BB`
- uses exact byte `0418` to choose one exact span descriptor from exact local table `BD65..BD6A`
- walks exact table `CC:2963`, masks each candidate byte with the selected exact mask, and writes the exact accepted table indices into exact byte lane `9890`
- terminates exact lane `9890` with exact byte `FF`

#### `C2:BD00..C2:BD3F`
This helper:
- walks exact byte lane `9890` until the exact negative terminator
- for each exact compact selector, expands one exact span into exact byte lanes `0F00` and `0F30`
- stores exact lane count `Y -> 0F49`
- terminates exact lane `0F00` with exact byte `FF`

So the real pattern here is: compact exact list build into `9890`, then exact live-lane expansion into `0F00/0F30`.

### 3. `C2:BD40..C2:BD6A` is real supporting data, not code
Two exact local data blocks are now tight enough to freeze:
- `BD40..BD64` is the exact interleaved span-byte table family consumed by `BD00`
- `BD65..BD6A` is the exact 3-word span-descriptor table consumed by `BCCD`

### 4. `C2:BD6B..C2:BE78` is the exact `0F4C` export / watcher / refresh family
This breaks cleanly into exact callable pieces:

#### `C2:BD6B..C2:BD98`
- exact 9-row export loop
- seeds exact packet base `61 = 3024`
- mirrors exact `0F00` entries into exact byte `0F4C`
- calls exact helper `BD99` once per row
- advances the exact packet base by `0x80` after each row

#### `C2:BD99..C2:BDB1`
- exact sign-split `0F4C` exporter
- nonnegative path runs exact helper `BDB2`
- negative path jumps exact helper `EF65` with exact source seed `9B76`

#### `C2:BDB2..C2:BDEA`
- exact row-template exporter using exact multiply `0F4C * 0x0B`
- exact `7700,Y` flag bits decide the exact export mode and exact byte `7E = 00/08`
- final export runs through exact helper `EF65`

#### `C2:BDEB..C2:BDFD`
- exact `0418 == 00` bit-6 probe gate
- when exact bit `0x40` is set in exact lane `7700[0F4C]`, emits exact selector word `C026` through exact helper `ED31`

#### `C2:BDFE..C2:BE15`
- exact change watcher for exact byte `0F4C`
- only calls exact helper `BE33` when exact word/byte `0D78` is clear and exact latch byte `0D77` differs

#### `C2:BE16..C2:BE78`
- exact alternate seeded path plus exact common change-handler body
- seeded path writes exact `0D13 = 6D`, exact `0DC5 = 5356`, exact `0DC9 = 0A`, then branches into the common body with exact accumulator `0418 + 76`
- common body writes exact `0DC5 = 5344`, exact `0DC9 = 01`, then on change refreshes exact latches/words `0D77`, `020C`, `0DCC`, `0F73`, `020D`, `020F`, `0DD0` and runs exact helper `FA49`

So this whole band is not vague glue anymore; it is the exact export/watch/refresh family around the live exact selector byte `0F4C`.

### 5. `C2:BE79..C2:BECD` is another real continuation owner
This owner:
- recomputes exact byte `71 = 0419 + 041A`
- reruns exact helper `8820`
- reruns exact helper `BC22`
- clears exact byte `7D`, seeds exact packet base `61 = 2ECA`, runs exact helpers `BA2F` and `821E`
- stages an exact local block through `5DE0/5DE2`
- seeds exact phase word/byte `0D75 = 0003`
- runs exact helper `BEDC`
- clears exact word/byte `0DBC`
- emits three exact selector packets through `8385`

This means the continuation-family seam does not stay “helper only” after `BC6F`; it grows into a second exact owner at `BE79` before the remaining exact local descriptor/data bytes take over.

### 6. `C2:C949..C2:CA66` is now a real post-substitution helper chain with an exact local dispatch root
This resolves into five exact pieces:

#### `C2:C949..C2:C972`
- exact indexed subtract/clear helper
- walks exact live selector lane `0F04`
- subtracts exact signed step word `0D22` from exact word `180E,Y`
- clears exact marker byte `1811,Y`

#### `C2:C973..C2:C9AD`
- exact two-phase marker writer
- first phase scans exact descriptor bytes for `X = 08 .. 00`
- second phase scans exact descriptor for exact byte `0D0F`
- when exact byte `0F00` is nonnegative, runs one final exact pass with exact marker byte `0B`

#### `C2:C997..C2:C9AD`
- exact callable helper entry inside the previous routine
- maps one exact descriptor byte from exact table `C2:2980,X` into one exact `1811` slot and writes the exact current marker byte `Y`

#### `C2:C9AE..C2:C9E4`
- exact selector recentering helper
- either adjusts exact selector byte `54` by `+03/-03` from exact low bits of `5A`, or derives the exact selector nibble from exact `9382/9383` lookup bytes after exact helper `EA27`

#### `C2:C9E5..C2:CA61` plus exact table `C2:CA63..C2:CA66`
- exact dispatch-rooted import/setup owner
- derives exact dispatch index `X = (0D36 & 02)`
- runs exact `JSR ($CA63,X)`
- copies exact blocks `CC64 -> 9540`, `CBB4 -> 94C0`, and `9480 -> 9500`
- runs exact helper chain `F5A7 -> A0E7 -> CD2B -> 821E -> CCDB -> 821E -> F643 -> CC4F -> 86DD`
- increments exact byte `0D15`, seeds exact `0D13 = 01`, and emits the exact selector chain `FBE3 -> FBFF -> FC37 -> 8385`
- exact local dispatch table at `CA63` contains exact entries `CA67` and `CAE0`

So the real next post-substitution seam now starts after that exact local dispatch root, not back in the middle of `C9E5`.

## Strong labels / semantics added
- exact callable continuation owner at `BC6F`
- exact `9890` rebuild lane at `BCAE/BCCD/BD00`
- exact local data tables at `BD40..BD6A`
- exact `0F4C` export/watch/refresh family at `BD6B..BE78`
- exact continuation owner at `BE79`
- exact subtract/marker/recenter/import helper chain at `C949..CA66`

## Corrections made this pass
- corrected the callable entry from `BC71` to exact `BC6F`
- corrected the post-substitution seam so it no longer stops mid-owner at `CA40`; the exact owner runs through exact `CA61`
- proved that `CA63..CA66` is an exact two-word local dispatch table, not inline code

## Still unresolved
- exact local descriptor/data bytes after the new `BE79` owner remain open, especially `C2:BECE..C2:BEE5`
- the two downstream exact dispatch targets after the new `CA63` root remain open, especially `C2:CA67..C2:CC0D`
- broader gameplay/system nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B/0D8C/0D90`
- the broader top-level family noun for `C2:A886..AA30` is still not tight enough

## Next recommended target
- `C2:BECE..C2:BEE5`
- `C2:CA67..C2:CC0D`
- broader nouns for `7E:0F0F`, `7E:0D1F`, and the `0D8B/0D8C/0D90` family
