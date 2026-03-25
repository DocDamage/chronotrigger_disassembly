# Chrono Trigger Disassembly — Pass 130

## Scope
- close the downstream post-substitution helper/owner seam at `C2:CC0E..C2:CD2A`
- close the next helper/data band at `C2:CD2B..C2:CE85`
- tighten the directly-called follow-on helper at `C2:CE86..C2:CEC1`

## Starting point
- previous top-of-stack: pass 129 froze `C2:CA67..C2:CC0D`
- the live seam packet still had two open bands: `C2:CC0E..C2:CD2A` and `C2:CD2B..C2:CE85`
- direct xref checks showed real callable entries at `CC0E`, `CC4F`, `CCDB`, `CD2B`, `CD9B`, `CDE3`, `CE2A`, `CE49`, `CE86`, and `CE9D`

## Work performed
- split the full `CC0E..CE85` band by exact xref-backed entry points and by clean `RTS` / table boundaries instead of treating it like one blob
- decoded the post-substitution packet/service lane into a latch-aware immediate emitter, one three-slot packet writer, one high-byte strip clearer, one dual three-slot exporter, one list-builder, one exact row builder, one two-phase row-owner, one local direct-page helper, and one single-slot row writer
- extended one small step past the original seam to freeze the directly-called `CE86`/`CE9D` helpers that the already-frozen `C7AC` owner depends on

## Findings

### 1. `C2:CC0E..C2:CC4E` is a real latch-aware immediate packet emitter, not leftover tail bytes
This callable entry is hit directly from the already-frozen `C7E0` overflow path.
It:
- begins in 8-bit A with no wrapper `PHP`
- tests exact latch byte `0F0F`
- when that latch is nonzero, seeds exact local bytes `02 = 08`, `03 = 01`, runs exact helper `CBF7`, then exact helper `83CA`
- retests exact latch byte `0F0F`; when it is now zero, exits early
- otherwise waits until exact long hardware/status byte `002141 == 0`, looping through exact helper `821E`
- then writes exact packet byte `1E01 = 0F0E`, exact packet byte `1E00 = 11`, seeds exact local byte `02 = 10`, and seeds exact local byte `03 = FF` only when exact byte `04FB == 0`
- runs exact helper `CBEB`
- exits `RTS`

Strongest safe reading: exact `0F0F`-aware immediate `11/0F0E` packet emitter that optionally primes `CBF7/83CA`, waits on `2141`, and then emits through the already-frozen `CBEB` service.

### 2. `C2:CC4F..C2:CCB0` is the exact three-slot packet writer above `CCB1`
This callable owner:
- begins `PHP ; SEP #$20`
- seeds exact base pair `04 = 2E84`, `02 = 100E`
- when exact byte `0D36 != 0`, switches the base pair to exact `04 = 2E90`, `02 = 1010`, and writes exact byte `38` into exact bytes `9380`, `9386`, and `938C`
- enters 16-bit A/X/Y mode, loops over exact words `0F02`, `0F03`, and `0F04`
- masks exact bits `0x00C0`; when clear, skips the paired write for that slot
- otherwise runs exact helper `CCB1`, seeds exact base word `61 = 04`, and twice runs exact helper `EC93` with exact `X = 0006`, first from exact base `02`, then from exact base `02 + 1000`
- after every slot, increments exact base word `04` by `0180`
- exits `PLP ; RTS`

Strongest safe reading: exact three-slot high-bit packet writer that conditionally expands the `0F02` strip through `CCB1` and emits paired `100E/200E`-style rows through exact helper `EC93`.

### 3. `C2:CCB1..C2:CCD8` is the exact negative-gated `95A2` strip clearer used by the previous owner
This helper:
- begins `PHP ; SEP #$30`
- clears exact bit `0x40` from the incoming `A`
- when the resulting exact byte is negative, returns immediately
- otherwise uses the exact input byte as an index into exact word table `297F`
- keeps only the exact high byte from that word, shifts it right three times, and uses that exact result as a `Y` base
- iterates exact count `X = 000F`
- for each exact word in `95A2,Y`, shifts right once, masks exact word `3DEF`, stores it back, then advances `Y` by 2
- exits `PLP ; RTS`

Strongest safe reading: exact negative-gated `95A2` word-strip clearer / normalizer derived from the exact `297F` high-byte lane.

### 4. `C2:CCDB..C2:CD2A` is the exact dual three-slot exporter above `CD9B`
This owner:
- begins `PHP ; REP #$30`
- seeds exact local word `22 = 0006`, clears exact local byte `24`, then in 8-bit mode seeds exact compare byte `71 = 73 + 80`
- first loop: visits exact bytes `0F05`, `0F07`, `0F09`; when exact bits `0xC0` are clear, runs exact helper `CD9B`; advances exact local word `22` by 2 and exact slot byte `24` by 1 until three slots are handled
- when exact byte `0D36 != 0`, reseeds exact local word `22 = 0012`
- clears exact bytes `71` and `24`
- second loop: visits exact bytes `0F02`, `0F03`, `0F04`; when the exact slot byte is nonnegative, runs exact helper `CD9B`; advances exact local word `22` by 2 and exact slot byte `24` by 1 until three slots are handled
- exits `PLP ; RTS`

Strongest safe reading: exact dual three-slot exporter that walks the `0F05` lane and then the `0F02` lane, conditionally handing each accepted slot to the exact `CD9B` row-builder.

### 5. `C2:CD2B..C2:CD9A` is the exact compact-state scanner that builds the `0F02/0F05` lists and the exact count bytes `0F0B/0F0C`
This callable helper is already used by the earlier-frozen `C70C` swap/normalizer and by the `C9E5` import/setup owner.
It:
- begins `PHP ; REP #$30`
- seeds exact word `0F02 = 8080`
- performs exact overlapping same-bank block move `0F02.. -> 0F04..` for `0007` bytes through `MVN 7E,7E`
- clears exact byte `0F0B`
- in 8-bit mode loops exact indexes `0`, `1`, `2` over exact table `2980`
- when an exact table byte is nonnegative, increments exact count byte `0F0B`, probes exact long byte `7F:01DF` through exact long indexed mask table `FFF9BB,X`, conditionally decrements exact count byte `0F0B`, ORs in exact flag byte `40` when the exact probe failed, and stores the exact result into exact bytes `0F02`, `0F03`, `0F04`
- when exact byte `0D36 == 0`, performs a second loop over exact indexes `3..8`, collecting exact nonnegative `2980` entries into exact bytes `0F05+Y`
- when the exact phase-flag byte does not carry exact bit `0x40`, writes the final exact `Y` count into exact byte `0F0C`
- exits `PLP ; RTS`

Strongest safe reading: exact compact-state scanner that compresses accepted exact `2980` state bytes into the live `0F02` and `0F05` lists while tracking exact counts `0F0B` and `0F0C`.

### 6. `C2:CD9B..C2:CDC9` is the exact `1800/180E` row builder used by both later owners
This callable helper:
- begins `PHP ; REP #$30`
- runs exact helper `8820`
- ORs exact bytes `51` into the accumulator and, when the exact result is nonzero, skips the row write
- otherwise loads an exact base word from exact local table `CDCB,X` into exact word `61`
- runs exact helper `A216`
- loads exact word `9A90`, runs exact helper `F626`, and stores the exact result into exact row slot `180E,Y` using exact local word table `CE6E,X`
- in 8-bit mode mirrors exact byte `9A90` into exact slot `1800,Y`
- increments exact compare byte `71`
- exits `PLP ; RTS`

Strongest safe reading: exact conditional `1800/180E` row builder using the exact local base-word table at `CDCB` and the exact row-word table at `CE6E`.

### 7. `C2:CDCB..C2:CDE2` and `C2:CE6E..C2:CE85` are the exact local tables feeding the previous helper family
#### `C2:CDCB..C2:CDE2`
Exact little-endian word table used by `CD9B`:
- `2E00`
- `2F80`
- `3100`
- `2E20`
- `2FA0`
- `3120`
- `32A0`
- `35A0`
- `0C3B`
- `0C2E`
- `0831`

#### `C2:CE6E..C2:CE85`
Exact little-endian word table used by `CD9B` and `CE49`:
- `7438`
- `7468`
- `7498`
- `8C38`
- `8C68`
- `8C98`
- `8CC8`
- `8C08`
- `8CF8`
- `A838`
- `A868`
- `A898`

These are real local data tables, not code.

### 8. `C2:CDE3..C2:CE28` is the exact two-phase `CE49` scan owner
This callable helper is already used by the earlier-frozen `C70C` family.
It:
- begins `PHP ; REP #$30`
- seeds exact local word `02` from exact byte `0D36`, but forces exact `02 = 0012` when that exact byte is nonzero
- clears exact local byte `00`
- switches to 8-bit A and runs exact helper `CE2A`
- then repeatedly runs exact helper `CE49`
- after each exact `CE49` call, ORs exact byte `00`; when the exact result is zero, bumps exact local word `02` by 2 twice
- first phase continues until exact local byte `00 == 03`
- when exact byte `0D36 == 0`, seeds exact local byte `02 = 06`, exact local byte `00 = 80 + 03`, reruns exact helper `CE49`, bumps exact local byte `02` by 2 twice each time, and continues until exact local byte `02 == 0E`
- exits `PLP ; RTS`

Strongest safe reading: exact two-phase owner that repeatedly invokes the exact `CE49` row writer over the compacted `0F02` lists, with one phase gated by exact byte `0D36`.

### 9. `C2:CE2A..C2:CE48` and `C2:CE49..C2:CE6D` are the exact helper pair under the previous owner
#### `C2:CE2A..C2:CE48`
This helper:
- begins `PHP ; PHD ; PEA 1980 ; PLD`
- switches to 8-bit A/X, seeds exact byte `00 = FF`, and clears exact bytes `11` and `18`
- returns to 16-bit A with carry clear, repeatedly transfers the direct-page value into `A`, subtracts exact `003F+1`, transfers the exact result back into direct page, and loops until the exact result drops below `1800`
- restores the previous direct page and flags, then returns

Strongest safe reading: exact `1980`-seeded direct-page stepping helper that walks the exact direct-page work base downward in exact `0x40` steps until it falls below exact `1800`.

#### `C2:CE49..C2:CE6D`
This helper:
- begins `PHP ; TDC`
- uses exact slot byte `00` as an index into exact byte strip `0F02`
- when the exact slot byte is negative, skips the row write
- otherwise clears exact bit `0x40`, uses the resulting exact byte as an index into exact table `2980`, runs exact helper `F626`, and stores the exact result into exact byte `1800,Y`
- then uses exact word table `CE6E,X` to seed exact row word `180E,Y`
- clears the accumulator, increments exact slot byte `00`, restores flags, and returns

Strongest safe reading: exact single-slot `1800/180E` row writer over the compacted `0F02` strip.

### 10. `C2:CE86..C2:CEC1` closes one more directly-called helper pair used by already-frozen callers
#### `C2:CE86..C2:CE95`
This callable helper is hit directly from the earlier-frozen `C7AC` prep/scan owner.
It:
- runs exact long helper `FFF677`
- seeds exact selector word `X = CE96`, runs exact helper `8385`
- then seeds exact selector word `X = FC14` and exits through exact jump `8385`

Strongest safe reading: exact selector-emitter helper that runs `FFF677` and then emits the exact `CE96` local descriptor plus one fixed `FC14` descriptor through exact helper `8385`.

#### `C2:CE96..C2:CE9C`
Exact 7-byte local descriptor packet consumed by `CE86`:
- exact bytes: `00 70 00 B0 7E 00 06`

#### `C2:CE9D..C2:CEC1`
This callable helper is hit directly from the earlier-frozen `C7AC` owner.
It:
- begins `PHP ; SEP #$20`
- writes exact byte `68` into exact long hardware register `002109`
- switches to 16-bit A/X/Y, clears exact word `0F10`, seeds exact callback pointer `A = CECE`, exact delay/count `X = 0010`, and runs exact helper `8249`
- then copies exact `000C` bytes from exact source `D57A` into exact destination `0F12`
- exits `PLP ; RTS`

Strongest safe reading: exact `2109 = 68` initializer that schedules the downstream exact `CECE` callback body and copies the exact `D57A` descriptor strip into exact `0F12`.

#### `C2:CEC2..C2:CED1`
This tiny wrapper:
- switches to 8-bit A
- sets exact bit `0x10` in exact word/byte `0D13`
- loads exact byte `02` and runs exact helper `822B`
- runs exact long helper `FFF716`
- branches directly to the previous helper’s exact `RTS`

Strongest safe reading: exact `0D13.bit10` wrapper around the fixed `822B -> FFF716` service lane.

## Strong labels / semantics added
- exact `0F0F`-aware immediate packet emitter at `CC0E`
- exact three-slot packet writer at `CC4F`
- exact negative-gated `95A2` strip clearer at `CCB1`
- exact dual three-slot exporter at `CCDB`
- exact compact-state scanner at `CD2B`
- exact `1800/180E` row builder at `CD9B`
- exact local row tables at `CDCB` and `CE6E`
- exact two-phase `CE49` scan owner at `CDE3`
- exact direct-page stepping helper at `CE2A`
- exact single-slot row writer at `CE49`
- exact selector/helper pair at `CE86` and `CE9D`
- exact local descriptor packet at `CE96`
- exact tiny `0D13.bit10` wrapper at `CEC2`

## Still unresolved
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B/0D8C/0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
- the next code seam now moves naturally to the downstream callback/dispatch band beginning at `C2:CED2`

## Next recommended target
- `C2:CED2..C2:CF92`
- broader nouns for `7E:0F0F`, `7E:0D1F`, and the `0D8B/0D8C/0D90` family
- broader top-level family noun for `C2:A886..C2:AA30`
