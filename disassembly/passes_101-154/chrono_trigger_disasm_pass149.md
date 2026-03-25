# Chrono Trigger Disassembly — Pass 149

## Summary

Pass 149 closes the callable/helper family that pass 148 left open at `C2:EF65..C2:F00F`, and it also closes the immediate callable spillover through exact `C2:F113`.

The resolved family is:

- one exact shared FF-bank script/template interpreter front-end at `C2:EF65..C2:EF7D`
- one exact byte-token interpreter loop at `C2:EF7E..C2:EF96`
- one exact paired-byte writer with optional sentinel shadow mirror at `C2:EF97..C2:EFBD`
- one exact local opcode-dispatch helper at `C2:EFBE..C2:EFD3`
- one exact local 16-word opcode-handler table at `C2:EFD4..C2:EFF3`
- one exact signed-mode write-pointer step helper at `C2:EFF4..C2:F004`
- one exact inline offset-to-write-pointer helper at `C2:F005..C2:F010`
- one exact two-word wrapper into exact helper `F114` at `C2:F011..C2:F021`
- one exact 24-bit pointed-script wrapper into exact helper `EF7E` at `C2:F022..C2:F035`
- one exact local `7E`-bank five-step subscript expander at `C2:F036..C2:F067`
- one exact single-byte latch helper at `C2:F068..C2:F070`
- one exact pointed-word importer/writer at `C2:F071..C2:F08C`
- one exact repeated sentinel-pair emitter at `C2:F08D..C2:F0A1`
- one exact masked-flag import helper at `C2:F0A2..C2:F0B7`
- one exact mode/flag latch helper at `C2:F0B8..C2:F0C0`
- one exact two-word wrapper into exact helper `F227` at `C2:F0C1..C2:F0CF`
- one exact indexed-threshold gate owner with exact fallback packet materializer at `C2:F0D0..C2:F113`

## Exact closures

### C2:EF65..C2:EF7D

This span freezes as the exact shared front-end that prepares one FF-bank script/template decode pass and then enters exact helper `EF7E`.

Key facts now pinned:
- Begins `PHB ; PHP ; SEP #$20`.
- Stores the exact caller-supplied parameter byte into exact bytes `88` and masked-count byte `87`.
- Mirrors exact caller-owned destination pointer `X -> 65`.
- Uses exact accumulator high byte as the exact data-bank source by exact `XBA ; PHA ; PLB`.
- Runs exact helper `EF7E`.
- Clears exact bits `0xDC` from exact byte `7E` through exact `TRB 7E`.
- Returns through exact `PLP ; PLB ; RTS`.

Strongest safe reading: exact shared FF-bank script/template interpreter front-end that latches exact parameter byte `88/87`, latches exact source data bank from the accumulator high byte, runs exact helper `EF7E`, and then clears exact control bits `0xDC` from exact byte `7E`.

### C2:EF7E..C2:EF96

This span freezes as the exact byte-token interpreter loop immediately behind exact front-end `EF65`.

Key facts now pinned:
- Runs in exact 8-bit accumulator mode.
- Reads one exact token byte from exact `DB:[Y]`.
- Exact token `00` terminates the exact loop immediately.
- Exact tokens `< 0x10` dispatch through exact helper `EFBE`.
- Exact tokens `>= 0x10` route through exact helper `EF97`, then decrement exact count byte `87`.
- Loops until the exact token stream terminates or exact count byte `87` reaches zero.

Strongest safe reading: exact byte-token interpreter loop that reads exact `DB:[Y]`, routes low tokens through exact opcode-dispatch helper `EFBE`, routes higher tokens through exact write helper `EF97`, and stops on exact `00` or exhausted exact count byte `87`.

### C2:EF97..C2:EFBD

This span freezes as the exact paired-byte writer used by exact interpreter `EF7E`.

Key facts now pinned:
- Begins `PHP ; SEP #$20`.
- Uses exact mode/flag byte `88`.
- Exact negative exact `88` bypasses the exact sentinel-shadow lane.
- Exact nonnegative exact `88` plus exact token byte `FF` mirrors one exact two-byte pair into exact long addresses `7D:FFC0+X` and `7D:FFC1+X`.
- Always writes one exact two-byte pair into exact `7E:0000+X` and `7E:0001+X`.
- Advances exact destination pointer `X += 2`.

Strongest safe reading: exact paired-byte writer that materializes one exact token/high-byte pair into exact `7E:0000+X`, and under the exact nonnegative-flag plus exact `FF` token case also mirrors that exact pair into exact `7D:FFC0+X`.

### C2:EFBE..C2:EFD3

This span freezes as the exact local opcode-dispatch helper for exact interpreter `EF7E`.

Key facts now pinned:
- Begins `PHX ; REP #$20`.
- Masks the exact incoming token down to one exact 16-bit index and doubles it.
- Selects one exact handler word from the exact local 16-word table at `EFD4`.
- Uses exact `PER + JMP (8A)` to enter the exact selected handler while preserving exact `RTS` return behavior.
- Exact `RTS` stub at `EFD3` is the exact default/no-op lane.

Strongest safe reading: exact local opcode-dispatch helper using exact local 16-word handler table `EFD4..EFF3` and exact `PER / JMP (8A)` dispatch mechanics.

### C2:EFD4..C2:EFF3

This span freezes as the exact local 16-word opcode-handler table consumed by exact helper `EFBE`.

Exact table words now pinned:
- `EFD3`
- `EFF4`
- `F005`
- `F011`
- `F022`
- `F036`
- `F0A2`
- `F071`
- `F08D`
- `F0B8`
- `F068`
- `F0C1`
- `F0D1`
- `EFD3`
- `EFD3`
- `EFD3`

Strongest safe reading: exact local 16-word opcode-handler table for exact opcode-dispatch helper `EFBE`.

### C2:EFF4..C2:F004

This span freezes as the exact signed-mode write-pointer step helper.

Key facts now pinned:
- Begins in exact 16-bit accumulator mode.
- Starts from exact step word `0x0080`.
- Tests the exact sign-bearing mode word at exact `87/88`.
- Switches to exact step word `0x0040` when the exact negative mode bit is active.
- Adds that exact step into exact destination base word `65`.
- Mirrors the exact result back into exact `X`.

Strongest safe reading: exact signed-mode write-pointer step helper selecting exact `0x0080` or exact `0x0040` and then advancing exact destination word `65/X`.

### C2:F005..C2:F010

This span freezes as the exact inline offset-to-write-pointer helper.

Key facts now pinned:
- Reads one exact 16-bit offset word from exact `[Y]`.
- Adds that exact offset to exact base word `61`.
- Stores the exact result into exact destination word `65`.
- Mirrors the exact result into exact `X`.
- Advances exact `Y += 2`.
- Returns immediately.

Strongest safe reading: exact inline offset-to-write-pointer helper deriving exact destination word `65/X` from exact `[Y] + 61`.

### C2:F011..C2:F021

This span freezes as the exact four-byte two-word wrapper that enters exact helper `F114`.

Key facts now pinned:
- Saves exact caller-owned `Y`.
- Reads one exact 16-bit word from exact `[Y]` and one exact 16-bit word from exact `[Y+2]`.
- Routes that exact two-word argument pair into exact helper `F114`.
- Reuses the exact shared four-byte skip tail through exact branch into exact `F00E`.

Strongest safe reading: exact four-byte two-word wrapper that marshals two exact words from exact `[Y]`/`[Y+2]` into exact helper `F114`, then reuses the exact shared four-byte skip tail.

### C2:F022..C2:F035

This span freezes as the exact 24-bit pointed-script wrapper that enters exact helper `EF7E`.

Key facts now pinned:
- Saves exact caller-owned `Y` and exact data bank.
- Reconstructs one exact 24-bit pointed script source from exact bytes rooted at exact `[Y]`.
- Rebinds the exact data bank from that exact pointed source.
- Runs exact helper `EF7E`.
- Restores exact caller-owned bank and `Y`.
- Reuses the exact shared three-byte skip tail through exact branch into exact `F00E`.

Strongest safe reading: exact 24-bit pointed-script wrapper that reconstructs one exact far script/template source from exact record bytes at exact `[Y]`, runs exact helper `EF7E`, and then reuses the exact shared three-byte skip tail.

### C2:F036..C2:F067

This span freezes as the exact local `7E`-bank five-step subscript expander.

Key facts now pinned:
- Saves and restores the exact incoming mode/count word at exact `87/88`.
- Saves and later restores one exact adjusted destination pointer through exact `TXA ; ADC #$000A ; PHA`.
- Forces exact local mode/count word `87/88 = 0x8005`.
- Rebinds the exact data bank to exact `7E`.
- Runs exact helper `EF7E` on one exact local pointed subscript source from exact `[Y]`.
- After that exact subscript returns, emits exact `FF` sentinel pairs through exact helper `EF97` until exact count word `87` is exhausted.
- Restores the exact original mode/count word and reuses the exact shared two-byte skip tail.

Strongest safe reading: exact local `7E`-bank five-step subscript expander that forces exact work word `0x8005`, runs one exact local subscript through exact helper `EF7E`, emits exact `FF` sentinel pairs until the exact forced count is spent, then restores the exact original mode/count state.

### C2:F068..C2:F070

This span freezes as the exact single-byte latch helper.

Key facts now pinned:
- Runs in exact 8-bit accumulator mode.
- Copies one exact byte from exact `[Y]` into exact byte `7E`.
- Advances exact `Y += 1`.
- Returns immediately.

Strongest safe reading: exact single-byte latch helper copying one exact byte from exact `[Y]` into exact byte `7E`.

### C2:F071..C2:F08C

This span freezes as the exact pointed-word importer/writer behind exact local opcode slot `07`.

Key facts now pinned:
- Saves exact caller-owned `Y` and exact data bank.
- Rebinds the exact data bank to exact `7E`.
- Uses one exact pointed source word rooted at exact `[Y]`.
- Imports one exact 16-bit word from exact `7E:[pointer]`.
- Stores that exact word into exact destination `[X]`.
- Advances exact destination pointer `X += 2`.
- Decrements exact count byte `87`.
- Reuses the exact shared two-byte skip tail through exact jump into exact `F00E`.

Strongest safe reading: exact pointed-word importer/writer that reads one exact 16-bit word from exact `7E:[pointer]`, writes it to exact destination `[X]`, decrements exact count byte `87`, and then reuses the exact shared two-byte skip tail.

### C2:F08D..C2:F0A1

This span freezes as the exact repeated sentinel-pair emitter.

Key facts now pinned:
- Reads one exact low-byte count from exact `[Y]`.
- Advances exact `Y += 1` before the exact emission loop.
- Emits exact sentinel byte `FF` through exact helper `EF97`.
- Repeats until the exact requested count reaches zero.
- Restores exact caller-owned `Y`.

Strongest safe reading: exact repeated sentinel-pair emitter that uses the exact low byte at exact `[Y]` as an exact loop count and emits that many exact `FF` pairs through exact helper `EF97`.

### C2:F0A2..C2:F0B7

This span freezes as the exact masked-flag import helper.

Key facts now pinned:
- Runs in exact 8-bit accumulator mode.
- Loads one exact pointer word from exact `[Y]`.
- Advances exact `Y += 2`.
- Clears exact mask bits `0x1C` from exact byte `7E`.
- Loads one exact source byte from exact `7E:[pointer]`.
- Masks that exact source byte down to exact bits `0x1C`.
- ORs those exact masked bits back into exact byte `7E`.

Strongest safe reading: exact masked-flag import helper that clears exact bits `0x1C` from exact byte `7E`, imports those exact bits from one exact `7E:[pointer]` source byte, and consumes one exact 16-bit pointer operand.

### C2:F0B8..C2:F0C0

This span freezes as the exact mode/flag latch helper.

Key facts now pinned:
- Runs in exact 8-bit accumulator mode.
- Copies one exact byte from exact `[Y]` into exact byte `88`.
- Advances exact `Y += 1`.
- Returns immediately.

Strongest safe reading: exact mode/flag latch helper copying one exact byte from exact `[Y]` into exact byte `88`.

### C2:F0C1..C2:F0CF

This span freezes as the exact four-byte two-word wrapper that enters exact helper `F227`.

Key facts now pinned:
- Saves exact caller-owned `Y`.
- Reads one exact 16-bit word from exact `[Y]` and one exact 16-bit word from exact `[Y+2]`.
- Routes that exact argument pair into exact helper `F227`.
- Reuses the exact shared four-byte skip tail through exact jump into exact `F01E`.

Strongest safe reading: exact four-byte two-word wrapper that marshals two exact words from exact `[Y]`/`[Y+2]` into exact helper `F227`, then reuses the exact shared four-byte skip tail.

### C2:F0D0..C2:F113

This span freezes as the exact indexed-threshold gate owner with exact fallback packet materializer.

Key facts now pinned:
- Saves exact caller-owned bank, `Y`, and `X`.
- Uses one exact selector/index byte from exact `[Y]`.
- Uses one exact pointed source rooted at exact `[Y+1]`.
- Rebinds the exact data bank to exact `7E`.
- Reads one exact comparison source word from that exact pointed source.
- Compares that exact source word against one exact threshold from exact FF-bank table `FF:CF33[index]`.
- When the exact comparison does not pass, enters exact helper `F114` with exact `A` rebuilt as exact `0x7E11`.
- When the exact comparison does pass, materializes one exact four-byte fallback packet at exact destination `[X]` using exact byte `0x2F` and the exact current byte `7E`.
- Advances exact destination pointer `X += 4`.
- Reuses the exact shared three-byte skip tail before returning.

Strongest safe reading: exact indexed-threshold gate owner that compares one exact `7E`-bank source word against exact FF-bank threshold table `FF:CF33[index]`, then either routes into exact helper `F114` with exact rebuilt `0x7E11` state or emits one exact four-byte fallback packet into exact destination `[X]`.

## Honest remaining gap

- the old seam `C2:EF65..C2:F00F` was too short
- the honest closure for this pass runs through exact `C2:F113`
- the next clean follow-on callable/helper family now begins at exact `C2:F114`
- the next obvious callable band is `C2:F114..C2:F24A`
- exact helper/owner anchors already visible there are:
  - exact shared owner entry `C2:F114`
  - exact derived accumulator/tile helper entry `C2:F13F`
  - exact local bank-7E decode helper entry `C2:F1DA`
  - exact nibble/flag materializer helper entry `C2:F20B`
  - exact sibling shared owner entry `C2:F227`
