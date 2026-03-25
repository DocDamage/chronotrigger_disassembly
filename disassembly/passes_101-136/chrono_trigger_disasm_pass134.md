# Chrono Trigger Disassembly — Pass 134

## Focus of this pass

Pass 134 closes the downstream callable refresh / packet-build seam that pass 133 left open at `C2:D36C..C2:D520`. The main correction is boundary-related again: this seam is not one long callable owner. It resolves cleanly into one externally-called three-slot refresh/build owner, one exact local selector packet, one shared row/descriptor writer, one local byte table, two short exact service wrappers, one local four-word dispatch table, one dispatch-target wrapper, and one exact `E984`-status dispatcher.

## What this pass closes

### 1. exact externally-called three-slot refresh/build owner at `C2:D36C..C2:D45E`

This owner has real outside callers at exact `C2:CFE4`, `C2:D09E`, `C2:E7AC`, and `C2:E7E8`.

It begins `PHP ; SEP #$30` and immediately performs two exact guard tests:

- clears exact byte `0D5D`
- loads exact slot byte `79`
- when exact slot byte `79 == 03`, exits immediately through the exact `D45D` tail
- otherwise loads exact byte `0D49[79]`
- when that exact byte is zero, exits through the same exact `D45D` tail

When the exact guard passes, the body splits into two exact stages.

Stage one is an exact `7600`-window refresh plus an optional changed-`0D77` service lane:

- in 16-bit mode derives exact destination `X = 7600 + ((78 & FF00) >> 2)`
- copies exact `0040` bytes from exact source `7E:9890` into that exact `7600`-family window
- checks exact word `0D84`
- when exact word `0D84 == 0000`:
  - emits exact selector `C15E` through exact helper `ED31`
  - runs exact helper `F28D` with exact `X = 3310` and exact `Y = 98C9`
  - loads exact word `98C2`
  - halves that exact word into the exact `FFD296` lookup index
  - preserves the original low-bit carry from that exact halving step
  - loads exact lookup word `FFD296[x]`
  - masks exact bits with `01FF`
  - when the original exact low-bit carry was set, right-shifts the exact fetched word three more times
  - keeps only the exact low nibble
  - compares that exact nibble against exact byte `0D77`
  - when the exact nibble changed:
    - stores it into exact bytes `0D77` and `020C`
    - seeds exact word `0DC5 = 5E00`
    - seeds exact word `020D = D396`
    - seeds exact byte `020F = FF`
    - runs exact helper `F90C`
    - copies exact byte `0234 -> 26`
    - derives an exact repeat/count byte by repeated carry-preserving divide-by-two steps on exact byte `26`
    - runs exact helper `FB97`
    - emits exact local selector packet `D45F` through exact helper `8385`

Stage two is an exact three-slot refresh/build loop:

- seeds exact row base `61 = 3200`
- seeds exact source pointer `02 = 9890`
- clears exact loop bytes `24/25`
- across three exact `0x10`-byte source slots:
  - loads exact lead byte `[02]`
  - when that exact lead byte is non-negative:
    - copies exact `0009` bytes from the current exact source slot into exact work window `9A90`
    - copies exact `0006` bytes from the immediately-following exact source bytes into exact work window `9AE0`
    - mirrors the exact following word into exact `9AA2`
    - emits exact selector `C168` through exact helper `ED31`
    - runs exact helper `D466`
  - advances exact row base `61` by exact `00C0`
  - advances exact source pointer `02` by exact `0010`
  - increments exact loop byte `24`
- when the exact three-slot loop finishes, increments exact byte `0D15` and exits `PLP ; RTS`

Strongest safe reading: exact externally-called three-slot refresh/build owner that validates exact slot state `79 / 0D49[79]`, seeds an exact `7600` mirror window from `9890`, optionally refreshes exact nibble/state `0D77` through the `D396/F90C/FB97/D45F` service lane, then walks three exact `9890`-family slots and uses exact helper `D466` to build/export the live exact row/descriptor outputs.

### 2. exact local selector packet at `C2:D45F..C2:D465`

This span is not code. It is the exact local 7-byte selector/descriptor packet used only by exact owner `D36C` when the exact changed-`0D77` service lane fires.

Exact bytes:

- `08 78 00 5E 7E F0 01`

Strongest safe reading: exact local selector descriptor packet for the changed-`0D77` service lane inside exact owner `D36C`.

### 3. exact shared row/descriptor writer at `C2:D466..C2:D4B3`

This helper has a real exact caller at `C2:D43D`.

It begins `PHP ; SEP #$20` and uses exact row base `61`, exact slot counter byte `24`, and exact source selector byte `00`.

The exact work splits into three pieces:

First piece: four exact lane-tag writes.

- derives exact packed lane byte `((24 << 2) | 11)`
- writes that exact byte to exact row offsets:
  - `[61+005F]`
  - `[61+0061]`
  - `[61+009F]`
  - `[61+00A1]`

Second piece: four exact base/increment row-byte writes.

- clears exact byte `01`
- uses exact selector byte `00` as the index into exact local table `D4B4`
- loads the exact selected base byte from `D4B4[x]`
- writes that exact base byte to exact row offset `[61+005E]`
- increments exact `A` and writes the next three exact bytes to:
  - `[61+0060]`
  - `[61+009E]`
  - `[61+00A0]`

Third piece: exact template import into the `9500`-family window.

- in 16-bit mode derives exact source `X = FF:CC84 + (00 << 5)`
- derives exact destination `Y = 7E:9500 + (24 << 5)`
- copies exact `0x20` bytes from that exact source slot into the exact destination slot
- exits `PLP ; RTS`

Strongest safe reading: exact shared three-slot row/descriptor writer that stamps four exact lane-tag bytes into the current `61`-based row, expands one exact base byte from local table `D4B4` into four exact neighboring row bytes, and imports one exact `0x20`-byte template from exact source family `FF:CC84` into the exact slot-selected `9500` work window.

### 4. exact local base-byte table at `C2:D4B4..C2:D4BB`

This is the exact 8-byte local table used only by exact helper `D466`.

Exact bytes:

- `E0 E4 E8 EC F0 F4 F8 08`

Strongest safe reading: exact local base-byte table for the shared exact row/descriptor writer at `D466`.

### 5. exact local service wrapper at `C2:D4BC..C2:D4D4`

This wrapper is short and exact:

- begins `PHP ; SEP #$20`
- seeds exact byte `54 = 03`
- emits exact selector `C16F` through exact helper `ED31`
- seeds exact byte `0D13 = 75`
- emits exact selector `FBFF` through exact helper `8385`
- exits `PLP ; RTS`

Strongest safe reading: exact local service wrapper that seeds exact selector byte `54 = 03`, emits exact setup selector `C16F`, stamps exact service/state byte `0D13 = 75`, then exits through exact selector `FBFF`.

### 6. exact shared `0F00`-mirror service wrapper at `C2:D4D5..C2:D4EF`

This wrapper has real outside callers at exact `C2:CF82` and exact `C2:CF8F`.

Its exact body is:

- `PHP ; SEP #$20`
- emit exact selector `C191` through exact helper `ED31`
- seed exact byte `0D13 = 59`
- mirror exact byte `0F00 -> 54`
- emit exact selector `FBFF` through exact helper `8385`
- `PLP ; RTS`

Strongest safe reading: exact shared service wrapper that emits exact selector `C191`, mirrors exact byte `0F00` into exact selector/state byte `54`, stamps exact byte `0D13 = 59`, and then exits through exact selector `FBFF`.

### 7. exact local four-word dispatch table at `C2:D4F0..C2:D4F7`

This span is not code. It is an exact local four-word dispatch table.

Exact entries:

- `D4F8`
- `D506`
- `CF61`
- `CF92`

It also appears as a bank-local exact word match inside the generic exact dispatcher table at `C2:82A8`.

Strongest safe reading: exact local four-word dispatch table that groups the two newly-closed exact service targets `D4F8 / D506` with the already-frozen exact siblings `CF61 / CF92`.

### 8. exact dispatch-target wrapper at `C2:D4F8..C2:D505`

This exact target is reached through local exact dispatch table `D4F0`.

Its exact body is only five instructions:

- `JSR 9AAD`
- `JSR D065`
- `JSR D0E5`
- `INC 68`
- `JMP 83B2`

Strongest safe reading: exact dispatch-target wrapper that runs the fixed exact `9AAD -> D065 -> D0E5` service chain, increments exact byte `68`, and exits through exact jump `83B2`.

### 9. exact `E984`-status dispatcher at `C2:D506..C2:D519`

This exact target is also reached through local exact dispatch table `D4F0`.

Its body is a clean exact status dispatcher:

- begins `JSR E984 ; BIT 0D1D`
- when the exact negative flag is set, exits immediately through exact jump `CF0A`
- when the exact negative flag is clear and the exact overflow flag is clear, exits through exact jump `CFA2`
- when the exact negative flag is clear and the exact overflow flag is set, exits through exact jump `82B2`

Strongest safe reading: exact `E984`-status dispatcher that routes the negative path to exact jump `CF0A`, the clean non-negative/non-overflow path to exact jump `CFA2`, and the exact overflow case to exact jump `82B2`.

## Net effect of pass 134

The old seam at `C2:D36C..C2:D520` is no longer open. It resolves into:

- one exact externally-called three-slot refresh/build owner
- one exact local selector packet
- one exact shared row/descriptor writer
- one exact local byte table
- two short exact service wrappers
- one exact local four-word dispatch table
- one exact dispatch-target wrapper
- one exact `E984`-status dispatcher

## Remaining honest gaps after this pass

- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
- the next real code seam now moves naturally to `C2:D51A..C2:D715`
