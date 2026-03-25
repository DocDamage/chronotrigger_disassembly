# Chrono Trigger Disassembly — Pass 132

## Focus of this pass

Pass 132 closes the downstream callable setup / export seam that pass 131 left open at `C2:D065..C2:D0C5`. The biggest correction this pass makes is boundary-related: `D065` does **not** stop at `D0C5`; it runs cleanly through `PLP ; RTS` at `D0DD`, followed by a tiny `D0DE` wrapper, a sibling callable owner at `D0E5`, a real 3-pass helper chain at `D10D`, and one easy extra owner at `D156` that becomes obvious once the helper flow is decoded.

## What this pass closes

### 1. exact callable setup / export owner at `C2:D065..C2:D0DD`

This owner begins `PHP ; SEP #$20` and runs a real multi-stage setup lane:

- emits exact selector `FC53` through exact helper `ED31`
- runs exact local helper `D10D`
- tail-emits exact selector `FC53` through exact helper `8385`
- clears exact byte `0D15`
- seeds exact byte `C9 = 03`
- runs exact helper `821E`
- in 16-bit mode clears exact word `3000` and performs exact overlapping same-bank move `3000 -> 3002` for exact length `05FE`
- stores the post-MVN exact accumulator into exact word `0D77`, yielding the usual `FFFF` tail state
- in 8-bit mode mirrors exact byte `0414 -> 79` and `0414 -> 7F`
- runs exact helper `D36C`
- emits exact selector `FC1B` through exact helper `8385`
- clears exact byte `0D15` again and reruns exact helper `821E`
- seeds exact word `0D0E = FFFF`
- copies exact `0010` bytes from exact source `FF:CC74` into exact destination `7E:94C0`
- increments exact byte `0D15`
- runs exact helpers `984A` and `86DD`
- seeds exact byte/word `0D13 = 19`
- emits exact selector tail `FBE3 -> 8385` and `FBFF -> 8385`
- exits `PLP ; RTS`

Strongest safe reading: exact callable setup / export owner that emits the `FC53` setup lane, runs the local `D10D` helper family, shifts the live `3000` strip forward by two bytes, mirrors exact selector/state byte `0414` into `79/7F`, imports exact block `FF:CC74 -> 7E:94C0`, and finishes through the fixed `984A / 86DD / FBE3 / FBFF` tail.

### 2. exact `0D13 = 19` wrapper at `C2:D0DE..C2:D0E4`

Exact bytes decode to:

- `PHP`
- `SEP #$20`
- `LDA #$19`
- `STA $0D13`
- `PLP`
- `RTS`

Strongest safe reading: exact local wrapper that only seeds exact byte/word `0D13 = 19` and returns.

### 3. exact sibling callable owner at `C2:D0E5..C2:D10C`

This owner is the clear downstream callable target used by both the already-frozen `CEDC` owner and the external callsite at `D4FE`.

It does the following exactly:

- begins `PHP ; SEP #$20`
- mirrors exact byte `7F -> 54`
- emits exact selector `C138` through exact helper `ED31`
- increments exact byte `0D15`
- seeds exact byte/word `0D13 = 19`
- runs exact helper `CFFB`
- emits exact selector tail `FBE3 -> 8385` and `FBFF -> 8385`
- exits through exact `PLP ; JMP E923`

Strongest safe reading: exact sibling callable owner that mirrors exact selector byte `7F -> 54`, emits exact selector `C138`, bumps exact byte `0D15`, reruns the exact callable initializer `CFFB`, then rejoins the broader service tail at exact jump `E923` after the fixed `FBE3 / FBFF` selector pair.

### 4. exact 3-pass source-page / destination-window driver at `C2:D10D..C2:D130`

This helper resolves cleanly into a counted 3-pass driver:

- seeds exact direct-page pointer `61/62 = 4EC6`
- clears exact byte `79`
- seeds exact byte `0DC7 = 20`
- loops exactly three times:
  - `JSR D131`
  - `INC 62` (advancing the exact source pointer page from `4EC6` to `4FC6` to `50C6`)
  - adds exact `20` to exact byte `0DC7`
  - increments exact byte `79`
- exits once exact byte `79 == 03`

Strongest safe reading: exact 3-pass driver that walks three consecutive exact source pages through `61/62` while stepping the exact destination/window byte `0DC7` through `20 / 40 / 60` before returning.

### 5. exact 3-entry row/descriptor writer at `C2:D131..C2:D155`

This helper is called only from `D10D`, and its body is structurally clean:

- loads exact source pointer from exact direct-page word `61/62` into `X`
- seeds exact `Y = 0002`
- in 8-bit mode constructs the exact staged selector words `3001`, `3003`, and `3005` through the sequence `LDA #30 ; XBA ; LDA 79 ; ASL ; INC`
- runs exact helper `FBB4`
- advances exact source pointer `X` by ten exact bytes through ten exact `INX`
- seeds exact `Y = 0010`
- loads exact byte `0DC7`
- runs exact helper `FB97`
- exits through exact jump `D32C`

Strongest safe reading: exact 3-entry row/descriptor writer that consumes the current exact source pointer in `61/62`, feeds one of the exact staged selector words `3001 / 3003 / 3005` into `FBB4`, advances the source pointer by exact `0x0A`, then uses exact destination/window byte `0DC7` in `FB97` before tailing into exact helper `D32C`.

### 6. exact 3-slot `FFF9C4` poll / service owner at `C2:D156..C2:D197`

This owner is externally callable from `C2:8127` and resolves cleanly enough to freeze now:

- begins `PHP ; SEP #$20`
- seeds exact bytes:
  - `0D79 = 51`
  - `79 = 51`
  - `0D7B = 00`
  - `0D4C = FF`
- loops across three exact slots (`79 = 00..02` after entry normalization):
  - clears exact byte `0D49[79]`
  - runs exact long helper `FFF9C4`
  - when exact result byte `00 != 0`:
    - seeds exact byte `020C = 1A`
    - runs exact helper `D296`
  - when exact result byte `00 == 0`:
    - increments exact byte `0D49[79]`
    - runs exact helper `D19F`
  - runs exact helper `D2C4`
  - increments exact byte `79`
- after the 3-slot sweep, emits exact local selector packet `D198` through exact helper `8385`
- exits `PLP ; RTS`

Strongest safe reading: exact 3-slot `FFF9C4` poll / service owner that clears and conditionally marks exact slot bytes `0D49[79]`, chooses either the exact `020C = 1A -> D296` lane or the exact `INC 0D49[79] -> D19F` lane, always runs exact helper `D2C4`, then emits the exact local packet at `D198`.

### 7. exact local selector descriptor packet at `C2:D198..C2:D19E`

Exact 7-byte local descriptor used by the `D156` owner tail:

- exact bytes: `00 70 00 6E 7E 00 02`

Strongest safe reading: exact local selector descriptor packet for the `D156` 3-slot poll / service owner.

## Net effect of pass 132

The old seam at `C2:D065..C2:D0C5` is no longer open. It resolves into:

- one exact callable setup / export owner that actually runs through `D0DD`
- one tiny exact `0D13 = 19` wrapper
- one exact sibling callable owner at `D0E5`
- one exact 3-pass driver
- one exact 3-entry writer/helper
- one exact 3-slot externally-callable poll / service owner
- one exact local selector descriptor packet

## Remaining honest gaps after this pass

- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
- the next real code seam now moves naturally to `C2:D19F..C2:D2C3`
