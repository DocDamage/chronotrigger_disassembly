# Chrono Trigger Disassembly — Pass 163

## Scope
Pass 163 closes the exact downstream worker reached by exact low-bank veneer `C3:000E` more honestly: one exact top-level 32-step selected-`7E/7F` band worker at `C3:01E4..C3:02DC`, plus one exact externally callable byte-mix helper at `C3:02DD..C3:0306`.

## Starting point
- previous top-of-stack: exact `C3:0077..C3:01C5` worker plus exact `01C6..01E3` helper family were already frozen
- current target seam on entry to this pass: exact `C3:01E4..C3:0306`

## Work performed
- decoded the exact body at `C3:01E4..C3:0306` instruction-by-instruction
- verified the exact shared return path through prior exact epilogue `C3:01BD..C3:01C5`
- checked exact call edges into `C3:000E`, exact direct `JSL C3:01E4`, and exact direct `JSL C3:02DD`
- dumped exact ROM table bytes in exact bank `C0:FEC0..FFFF` to verify the exact chained-byte source feeding the worker

## Findings

### 1) `C3:01E4..C3:02DC` is one exact selected-`7E/7F` 224-byte band initializer and 32-step saturating add/subtract WRAM stream worker

The exact owner:

- saves exact `B/D/P/A/X/Y`
- installs exact direct page `0300`
- tests exact mode byte `50`
  - exact `50 == 0` clears exact `50/51` and exits through exact shared epilogue `01BD..01C5`
- tests exact phase byte `51`
  - exact `51 == 0` performs one exact first-activation seed stage
  - exact `51 != 0` skips directly to the exact per-step stream stage

On the exact first activation (`51 == 0`), the owner:

- seeds exact byte `F0 = 00` when exact mode byte `50 == 01`
- otherwise seeds exact byte `F0 = FF`
- in exact 16-bit mode derives exact base span start `X = 52 + 01C0`
- chooses exact destination bank `7E` vs exact `7F` from exact low bit of exact byte `54`
- writes the exact seed word at exact selected-bank offset `X`
- performs one exact overlapping same-bank move with exact `A = 00DE`

That exact `STA` + overlapping exact `MVN` proves the first-activation stage seeds and propagates one exact byte value across one exact selected-bank band of exact length `00DF+1 = 00E0` bytes.

After that, the exact owner increments exact phase byte `51` once per call and enforces one exact 32-step lifetime:

- exact `INC 51`
- exact `CMP #20`
- when the exact phase reaches `20`, clears exact `51` and exact `50`, then exits through exact shared epilogue

That proves this is one exact persistent multi-call worker, not one exact single-shot blob.

### 2) each active step streams one exact `0xE0`-byte band through exact WRAM port `$2180` while updating the source band in place

For each active call, the exact owner:

- seeds exact long pointer bytes `56/57 = FE/C0`
- calls exact helper `C3:02DD`
- stores the returned exact byte into exact `55`
- rebuilds exact working span:
  - exact `X = 52 + 01C0`
  - exact end word `F4 = 52 + 02A0`
- computes one exact WRAM destination address for `$2181/$2183`
  - exact word comes from exact `52` with one exact parity-dependent `+00E0` adjustment based on exact phase byte `51`
  - exact bank byte comes from exact `54`
- loads exact bank byte `54` into exact data bank via `PHA ; PLB`

The exact inner loop then repeatedly:

- walks one exact chained-byte source through exact long indirect pointer `[55]`, which means exact bank `C0:FE??` because exact `56/57` are fixed to `FE/C0`
- derives one exact small bias value from two successive exact chained bytes:
  - one exact `AND #1F ; ADC #03` lane producing an exact short countdown in `Y`
  - one exact `AND #03 ; ADC #08` lane producing exact bias byte `F2`
- loads one exact byte from exact selected-bank source `0000,X`
- either exact adds or exact subtracts the exact bias byte `F2`
- clamps the exact result to exact `FF` on overflow or exact `00` on underflow
- writes the exact clamped byte to exact WRAM port `$2180`
- stores the exact same clamped byte back to exact selected-bank source `0000,X`
- advances until exact `X == F4`

That proves the owner is one exact selected-`7E/7F` 224-byte band stream/update worker with exact saturating arithmetic, not one exact generic copy path.

### 3) exact mode byte `50` selects the exact arithmetic direction

The exact branch at `027C..027E` is the clean split:

- exact `50 == 02` enters the exact subtract-and-clamp-to-zero loop at `02AE..02D9`
- all other surviving nonzero modes enter the exact add-and-clamp-to-FF loop at `0280..02A9`

Combined with the exact first-activation seed stage:

- exact mode `01` seeds exact `00` then uses exact saturating-add updates
- exact mode `02` seeds exact `FF` then uses exact saturating-subtract updates

Strongest safe reading:
- exact two-mode 32-step brighten/darken band worker, or one exact equivalent paired ramp family, implemented as exact saturating add/subtract updates over one exact selected-bank `0xE0`-byte band while streaming the evolving bytes to exact WRAM through `$2180`

### 4) `C3:02DD..C3:0306` is one exact externally callable byte-mix helper feeding the exact `C0:FE??` chained-byte walk

The exact helper:

- begins at one exact externally called `JSL` target `C3:02DD`
- ends exact `RTL`
- updates exact state byte/word rooted at exact `0386`
- mixes in exact `X`, exact `0008`, exact `F0`, exact `F2`, exact `F4`, and exact reads from exact PPU registers `2137 / 213C / 213D`
- returns the final exact mixed byte in exact accumulator and stores it back into exact `0386`

Strongest exact usage proof:

- exact caller `01E4` immediately stores the returned exact byte into exact `55`
- with exact `56/57 = FE/C0`, that returned exact byte becomes the low byte of one exact long indirect pointer rooted in exact ROM bank `C0:FE??`
- the downstream exact `LDA [55]` byte-chase loop proves the helper is producing or perturbing the exact start byte for that exact chained ROM-table walk

Additional exact edge proof:

- exact `C3:15E4` also calls exact `JSL C3:02DD`, proving `02DD..0306` is not merely one exact private fallthrough tail of the `01E4` owner

## Strong labels / semantics added
- exact selected-`7E/7F` `0xE0`-byte band initializer + 32-step saturating add/subtract WRAM stream worker at `C3:01E4..C3:02DC`
- exact externally callable byte-mix helper updating exact `0386` and feeding the exact `C0:FE??` chained-byte walk at `C3:02DD..C3:0306`

## Corrections made this pass
- the old seam `C3:01E4..C3:0306` is real work, but it is **not** one exact monolithic owner
- the honest split is:
  - exact top-level owner `C3:01E4..C3:02DC`
  - exact callable helper `C3:02DD..C3:0306`
- exact `02DD..0306` must not be buried as one exact anonymous internal tail because it has one exact second direct caller at `C3:15E4`

## Still unresolved
- the broader exact semantic role of the streamed band inside the higher-level rendering/effect pipeline is still not fully named
- exact callers that preload exact bytes `50 / 52 / 54` still need more bank-`C3` closure work before promoting a more thematic noun than the present exact structural one
- exact unresolved gap after these closures remains the broad exact bank-`C3` body between exact `0307` and the next already-frozen exact owner at `0529`

## Next recommended target
- exact next manual/raw seam: `C3:0307..C3:0528`
- exact reason: pass 163 closes the exact `000E -> 01E4` family honestly, and the next unfrozen exact body before the already-frozen exact temporary trampoline code at `0529` begins immediately after the exact callable helper at `0306`
