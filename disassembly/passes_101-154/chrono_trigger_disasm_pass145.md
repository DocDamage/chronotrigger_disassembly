# Chrono Trigger Disassembly — Pass 145

## Summary

Pass 145 closes the callable/helper family that pass 144 left open at `C2:E841..C2:E923`, and it corrects the seam on the back edge again. The old seam end at `C2:E923` was not an honest stop. `C2:E923` is the first byte of a short wrapper that braids into a larger owner/helper cluster, and the clean closure for this pass runs through exact `RTS` at `C2:EAC1`.

The resolved family is:

- one exact setup owner at `C2:E841..C2:E889`
- one exact local 7-byte selector packet at `C2:E88A..C2:E890`
- one exact fast-lane owner at `C2:E891..C2:E8B6`
- one exact selected-slot clear / pointer-build owner at `C2:E8B7..C2:E913`, with two exact overlapping callable late entries at `C2:E8E8` and `C2:E8FA`
- one exact local 7-byte data span at `C2:E914..C2:E91A`
- one exact poll-loop wrapper at `C2:E91B..C2:E922`
- one exact short wrapper at `C2:E923..C2:E92C`
- one exact workspace reset / indexed seed owner at `C2:E92D..C2:E97D`
- one exact poll/wait loop at `C2:E97E..C2:E985`
- one exact `0D1D` rebuild owner at `C2:E986..C2:E9D8`
- one exact local 9-byte table at `C2:E9D9..C2:E9E1`
- one exact `F5`-bit scan / 4-way local dispatch owner at `C2:E9E2..C2:EA1D`
- one exact local 4-word dispatch table at `C2:EA1E..C2:EA25`
- one exact low-byte-times-6 index helper at `C2:EA26..C2:EA35`
- one exact overlapping local table-byte loader quartet at `C2:EA36..C2:EA52`
- one exact sign/bounds helper at `C2:EA53..C2:EA80`
- one exact delta / hardware-division helper at `C2:EA81..C2:EABC`
- one exact short wrapper at `C2:EABD..C2:EAC1`

## Exact closures

### C2:E841..C2:E889

This span freezes as the exact setup owner used by the `E61B` negative-service branch.

Key facts now pinned:
- Begins `PHP ; REP #$30 ; SEP #$20`.
- Runs exact helper `84EE`.
- Seeds exact bytes/words:
  - `020C = 03`
  - `0DC5 = 5E00`
  - `020D = CF3B`
  - `020F = FF`
- Runs exact helper `F90C`.
- In exact 16-bit accumulator mode, runs exact helper `FBB4` twice to materialize exact same-bank propagated bands:
  - `3021 -> 52C8` for exact length `0008`
  - `3062 -> 5348` for exact length `0009`
- Emits exact local selector packet `E88A` through exact helper `8385`.
- Emits exact selector `FC1B` through exact helper `8385`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact setup owner that seeds the `020C/020D/020F` packet fields, materializes exact `52C8/5348` propagated work bands, then emits the fixed exact `E88A -> FC1B` selector pair.

### C2:E88A..C2:E890

This span freezes as the exact local 7-byte selector packet consumed by the owner above.

Exact bytes now pinned:
- `08 71 00 5E 7E 00 06`

Strongest safe reading: exact local 7-byte selector packet emitted through exact helper `8385`.

### C2:E891..C2:E8B6

This span freezes as the exact fast-lane owner reached from the `0420 == 30` dispatcher lane in `E61B`.

Key facts now pinned:
- Begins `TDC`.
- Mirrors exact selector byte `54 -> 79`.
- If exact incoming carry is set, returns immediately.
- If exact incoming carry is clear, then:
  - clears exact byte `0F00`
  - forces exact selector byte `54 = 04`
  - seeds exact byte `0D13 = 7F`
  - emits exact selector `C391` through exact helper `ED31`
  - emits exact selector pair `FBEA -> FBFF` through exact helper `8385`
- Exits `RTS`.

Strongest safe reading: exact carry-sensitive fast-lane owner that mirrors exact selector byte `54 -> 79` and, on the clear-carry lane used by `E61B`, forces the exact `0F00 / 54 / 0D13` setup before the fixed exact `C391 / FBEA / FBFF` tail.

### C2:E8B7..C2:E913

This span freezes as the exact selected-slot clear / pointer-build owner used from the `E705` negative/overflow lane.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Loads exact slot index byte `79 -> X`.
- Clears exact bytes `0D49[X]` and `0D79[X]`.
- Doubles exact selector byte `79`, uses that doubled exact index as `X`, and stores the doubled exact selector into exact long table `30:7FF8,X`.
- Seeds exact byte/word `9894 = 7E`.
- ORs exact slot bytes `0D49 / 0D4A / 0D4B`; when they are all zero, clears exact long byte `30:7FE2` and seeds exact byte `9392 = 08`.
- In exact 16-bit accumulator mode seeds exact word `9895 = 0200`.
- Derives exact word `9892 = 7000 + ((78 & 0300) << 1)`.
- Derives exact word `9890 = 7900 + (78 & 0300)`.
- Runs exact helper chain `D28D -> 821E -> 838E(X=9890) -> D32C`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact selected-slot clear / long-table mirror owner that rebuilds exact pointer/state words `9890/9892/9894/9895` and then runs the fixed exact `D28D / 821E / 838E / D32C` tail.

### C2:E8E8..C2:E913

This exact overlapping callable late entry seeds exact word `9895 = 0200`, derives exact words `9892` and `9890` from exact byte/word `78 & 0300`, then rejoins the fixed exact `D28D / 821E / 838E / D32C` tail.

### C2:E8FA..C2:E913

This exact overlapping callable late entry begins after exact `X/Y` have already been staged from the exact `9892` lane, seeds exact word `9890 = 7900 + (78 & 0300)`, then rejoins the fixed exact `D28D / 821E / 838E / D32C` tail.

### C2:E914..C2:E91A

This span is not trustworthy as straight-line code. It freezes as exact local 7-byte data immediately before the exact poll-loop wrapper at `E91B`.

Exact bytes now pinned:
- `40 58 80 2E 7E 80 00`

Strongest safe reading: exact local 7-byte data span immediately ahead of exact wrapper `E91B`.

### C2:E91B..C2:E922

This span freezes as the exact poll-loop wrapper directly ahead of the next owner.

Key facts now pinned:
- Repeatedly runs exact helper/owner `E92D`.
- Runs exact helper `821E` after each exact `E92D` pass.
- Exact `BRA -08` loops back to the wrapper head.

Strongest safe reading: exact poll/wait wrapper repeatedly running exact owner `E92D` and exact helper `821E` until the downstream lane settles.

### C2:E923..C2:E92C

This span freezes as the exact short wrapper that proves the old seam end was too short.

Key facts now pinned:
- Begins `PHP ; SEP #$20`.
- Runs exact helper `984A`.
- Clears exact byte `56`.
- Exact `BRA +27` enters the shared tail inside exact owner `E92D`.

Strongest safe reading: exact short wrapper that clears exact byte `56` and then braids into the shared exact `E92D` tail.

### C2:E92D..C2:E97D

This span freezes as the exact workspace reset / indexed seed owner behind the wrapper above.

Key facts now pinned:
- Begins `PHP ; REP #$30`.
- Seeds exact word `0740 = E000`.
- Uses exact same-bank `MVN 7E,7E` propagation to expand exact work bands:
  - `0740 -> 0742` for exact length `013D`
  - `0904 -> 0906` for exact length `0011`
- Seeds exact word `0904 = AAAA` before the second exact propagation.
- In exact 8-bit mode uses exact `TSB 0D9B` with exact mask `FF`.
- On the fresh-set lane:
  - loads exact selector byte `54`
  - runs exact helper `EA27`
  - loads exact table word `9380,X -> 0770`
  - mirrors exact byte `58 -> 0772`
  - when exact byte `56 != 0`, sets exact bit `40` in exact byte `0773`
- Exits `PLP ; RTS`.

Strongest safe reading: exact workspace reset / propagated-pattern owner that seeds exact `0740/0904` work bands, then on the fresh-set lane indexes exact table `9380` into exact destination `0770/0773`.

### C2:E97E..C2:E985

This span freezes as the exact wait loop around the local status rebuilder.

Key facts now pinned:
- Repeatedly runs exact helper `E984`.
- Runs exact helper `821E` after each exact `E984` pass.
- Exact `BRA -08` loops back to the wrapper head.

Strongest safe reading: exact wait loop around local exact helper `E984`.

### C2:E986..C2:E9D8

This span freezes as the exact `0D1D` rebuild owner behind the wait loop above.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Clears exact status byte `0D1D`.
- Mirrors exact byte `68 -> 0D17` and compares against the exact prior value.
- When exact byte `68` did **not** change, uses exact local table bytes from `E9D9` to probe exact bytes `2993[Y]` and contribute exact mask bits into exact byte `0D1D`.
- Also contributes exact bits into exact byte `0D1D` from:
  - exact `29F4 & 2999` with exact mask `02`
  - exact `29F4 & 299A` with exact mask `01`
  - exact byte `0D83` with exact mask `40`
- Exits `PLP ; RTS`.

Strongest safe reading: exact local status-byte rebuilder that materializes exact byte `0D1D` from the exact `68` snapshot, exact local table `E9D9`, exact masks under `29F4/2999/299A`, and exact byte `0D83`.

### C2:E9D9..C2:E9E1

This span freezes as exact local 9-byte table/data.

Exact bytes now pinned:
- `00 01 00 00 00 08 06 07 FF`

Strongest safe reading: exact local 9-byte table/data span whose leading bytes are consumed by exact owner `E986`.

### C2:E9E2..C2:EA1D

This span freezes as the exact `F5`-bit scan / 4-way local dispatch owner.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Mirrors exact selector byte `54 -> 81`.
- Seeds exact byte `0D1E = 80` before scanning.
- Loads exact byte `F5 -> 5A`, then exact-shifts right until the first exact set bit is found or exact `X` reaches `04`.
- When an exact set bit is found, mirrors exact index `X -> 0D1E`.
- When exact byte `0D1F == 0`, then:
  - runs exact helper `EA27` on exact selector byte `54`
  - mirrors exact computed exact offset `X -> Y`
  - mirrors exact selector byte `54 -> 55`
  - doubles exact mode byte `0D1E` and dispatches through exact local table `JSR ($EA1E,X)`
- Clears exact byte `0D1F` before exit.
- Exits `PLP ; RTS`.

Strongest safe reading: exact `F5`-bit scan / mode-dispatch owner that computes one exact `0D1E` mode, derives one exact local record offset through `EA27`, then dispatches one exact byte-loader leg out of exact table `EA1E` before clearing exact byte `0D1F`.

### C2:EA1E..C2:EA25

This span freezes as the exact local 4-word dispatch table used by the owner above.

Exact words now pinned:
- `EA45`
- `EA40`
- `EA3B`
- `EA36`

Strongest safe reading: exact local 4-word dispatch table for the four overlapping exact byte-loader legs at `EA36/EA3B/EA40/EA45`.

### C2:EA26..C2:EA35

This span freezes as the exact low-byte-times-6 index helper.

Key facts now pinned:
- Begins `PHP ; REP #$30`.
- Masks exact accumulator to exact low byte with `AND #$00FF`.
- Computes exact `X = A * 6` through exact `ASL / PHA / ASL / ADC 1,S / TAX`.
- Restores exact stack and flags through exact `PLA ; PLP ; RTS`.

Strongest safe reading: exact low-byte-times-6 helper that converts one exact selector byte into one exact 6-byte record offset in exact `X`.

### C2:EA36..C2:EA52

This span freezes as the exact overlapping local table-byte loader quartet selected by the dispatch table above.

Key facts now pinned:
- Exact entry `EA36` loads exact byte `9382,Y`.
- Exact entry `EA3B` loads exact byte `9383,Y`.
- Exact entry `EA40` loads exact byte `9384,Y`.
- Exact entry `EA45` loads exact byte `9385,Y`.
- All four exact entries converge on the shared exact tail:
  - mirrors the loaded exact byte into exact selector byte `54`
  - when the loaded exact byte is negative, sets exact bit `80` in exact byte `5A` and clears exact bit `80` from exact selector byte `54`
  - exits `RTS`

Strongest safe reading: exact overlapping byte-loader quartet for the exact `9382..9385,Y` local record bytes, with one exact sign-latch into exact byte `5A` and one exact normalized exact selector write into exact byte `54`.

### C2:EA53..C2:EA80

This span freezes as the exact sign/bounds helper used both locally and from other families.

Key facts now pinned:
- Uses exact byte `57` as the first gate.
- When exact byte `57 != 0`, tests exact bit `00F2.bit0` and conditionally decrements exact byte `0D18`.
- Uses exact sign/control byte `5A` to choose whether to return immediately, zero the accumulator through exact `TDC`, or continue into the exact bound-normalization lane.
- In the exact bound-normalization lane chooses between exact bytes `0DDB` and `0DDC`, mirrors the chosen exact byte into exact selector byte `54`, compares exact `0DDC` against exact selector byte `54`, and repeats until the exact bound condition settles.
- Exact clear exit is `TDC ; RTS`.

Strongest safe reading: exact sign/bounds helper around exact bytes `57`, `5A`, `0D18`, `0DDB`, and `0DDC`, normalizing exact selector byte `54` and returning either exact zero or an immediate exact exit depending on the control state.

### C2:EA81..C2:EABC

This span freezes as the exact delta / hardware-division helper reused from multiple earlier families.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Mirrors exact direct-page byte `00 -> 0DD8`.
- Computes exact delta `Y - 00` and writes that exact byte to exact hardware register `$4206`.
- Mirrors the exact delta sign/borrow result into exact byte `01`, saturating exact byte `01 = 00` on borrow.
- Uses exact direct-page byte `00` and exact bound byte `0DDB` to derive exact byte `0DDC`.
- Mirrors exact byte `01` into exact bytes `57`, `0D94`, and `0DDA`.
- In exact 16-bit accumulator mode reads exact hardware result `$4214 -> 0D98`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact delta / hardware-division helper that stages exact bytes `0DD8/0DDC/57/0D94/0DDA` from exact `00/Y` and captures the exact `$4214` result into exact word `0D98`.

### C2:EABD..C2:EAC1

This span freezes as the exact short wrapper immediately ahead of the next live owner.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Runs exact helper `EB03`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact short wrapper into the next exact `EB03` owner.

## Honest remaining gap

- the old seam `C2:E841..C2:E923` is now closed more honestly as `C2:E841..C2:EAC1`
- the old seam end at `C2:E923` was not a stop; it is the first byte of the exact short wrapper at `C2:E923..C2:E92C`
- the next clean follow-on family now begins at exact `C2:EAC2`
- the strongest immediate anchors in that follow-on family are exact entries `EAC2`, `EACC`, `EAD6`, `EB03`, and the larger exact owner beginning at `EB21`
- broader gameplay-facing nouns are still not tight enough for exact bytes `0D8B / 0D8C / 0D90`, exact bytes `0D1F`, `0F0F`, and the broader top-level family at `C2:A886..C2:AA30`
