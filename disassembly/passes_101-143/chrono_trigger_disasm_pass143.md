# Chrono Trigger Disassembly — Pass 143

## Summary

Pass 143 closes the front callable/helper family that pass 142 left open at `C2:E34A..C2:E5F0`, and corrects the seam again: the old end was too short because `C2:E5CC..C2:E60A` is one complete callable owner. The exact callable/helper closure in this pass stops at `C2:E60A`.

The resolved family is:

- one exact count-capped offset writer at `C2:E34A..C2:E361`
- one exact normalize / compare / fallback-copy owner at `C2:E362..C2:E38E`
- one exact compact-list normalizer at `C2:E38F..C2:E3DD`
- one exact overlapping row-match helper pair at `C2:E3DE..C2:E40D`
- one exact large setup / import / selector-emission owner at `C2:E40E..C2:E53D`
- one exact local selector packet at `C2:E53E..C2:E544`
- one exact `9890` table-materialization helper at `C2:E545..C2:E575`
- one exact zero-lane import / staging owner at `C2:E576..C2:E5CB`
- one exact `(54 + 1)` change-handler / refresh owner at `C2:E5CC..C2:E60A`

## Exact closures

### C2:E34A..C2:E361

This span freezes as the exact count-capped offset writer at the front of the pass-142 live seam.

Key facts now pinned:
- Begins `PHP ; SEP #$20`.
- Loads exact byte `0F06`, caps the effective exact count at `04`, shifts the exact result left three times, adds exact base `9C`, and mirrors the exact final byte into exact words/bytes `0880` and `0884`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact count-capped offset writer that turns the live exact count byte `0F06` into one exact `8 * min(0F06, 4) + 9C` offset mirrored into exact work/config bytes `0880/0884`.

### C2:E362..C2:E38E

This span freezes as the exact normalize / compare / fallback-copy owner that drives the front half of the family.

Key facts now pinned:
- Begins `PHP ; SEP #$20`.
- Clears one exact byte in the exact `0F0C`-selected lane with exact `STZ $0000,X` after loading exact `X = 0F0C`.
- Runs exact helpers `E390` and exact core entry `E3E0`.
- When exact helper `E3E0` returns nonzero, returns immediately with that exact nonzero result still live.
- When the exact compare helper returned zero and exact byte `9890` is also zero, forces exact return byte `FF`.
- Otherwise, in 16-bit mode copies exact `0x0006` bytes from exact staging band `9890` into the exact `0F0C`-selected destination lane, clears the exact accumulator with `TDC`, and returns.

Strongest safe reading: exact normalize / compare / fallback-copy owner that clears one exact `0F0C`-selected byte, rebuilds/normalizes the exact `9890` compact list, probes it through exact helper `E3E0`, and on the unresolved exact path copies six exact bytes from `9890` into the exact `0F0C`-selected destination lane.

### C2:E38F..C2:E3DD

This span freezes as the exact compact-list normalizer feeding the `E362` owner.

Key facts now pinned:
- Begins `PHP ; REP #$30`.
- Clears exact word `9890`.
- Performs one exact overlapping same-bank block move `9890 -> 9892` for exact length `0003`, shifting the live exact header bytes upward.
- Copies exact `0x0006` bytes from exact work band `0F00` into exact staging band `98A0`.
- In 8-bit mode runs a reverse exact scan over `98A0[5..0]`, clearing any exact `EF` bytes in place.
- Starting from exact byte `51`, walks the cleaned exact `98A0` bytes and compacts every exact nonzero / non-`EF` value back into exact staging band `9890`, preserving order.
- Exits `PLP ; RTS`.

Strongest safe reading: exact compact-list normalizer that seeds `98A0` from `0F00`, strips exact `EF` placeholders, and compacts the surviving exact values back into the exact `9890` list from the exact `51`-selected start lane.

### C2:E3DE..C2:E40D

This span freezes as the exact overlapping row-match helper pair directly behind the `E38F` normalizer.

Key facts now pinned:
- Exact entry `E3DE` seeds exact work byte `00` from exact selector byte `51` and falls into the shared core at exact `E3E0`.
- Exact core entry `E3E0` treats exact work byte `00` as the current exact row-base selector.
- Compares exact bytes `9890,X` against exact table bytes `2C23,Y` across exact five-byte rows.
- On a full exact row match, runs exact helper `EACC`, returns exact byte `FF`, and exits.
- On mismatch, advances the exact row-base selector by exact stride `06`, retries while the exact base remains below exact bound `30`, and otherwise clears the exact accumulator with `TDC` and returns.

Strongest safe reading: exact overlapping row-match helper pair that optionally seeds its exact starting row from exact byte `51`, scans exact five-byte rows inside exact table family `2C23 + 6*n` against the live exact `9890` compact list, and returns exact `FF` only on an exact row match after exact helper `EACC`.

### C2:E40E..C2:E53D

This span freezes as the exact large setup / import / selector-emission owner chosen by the nonzero lane of exact owner `E1EE`.

Key facts now pinned:
- Begins `PHP ; SEP #$20`.
- Clears exact selector byte `54`, emits exact selector packet `C3BC` through exact helper `ED31`, and runs exact local helper `E545`.
- Clears exact byte `7E`.
- In 16-bit mode copies two exact items from exact source family `30CC` into exact staging band `9890` through exact helper `EF65`.
- Seeds exact word `0D06 = 0003`, exact byte `0F0A = 00`, exact byte `0F0B = 53`, exact word `0F08 = 51`, and exact byte `0D46 = 71`.
- When exact byte `71 >= 07`, emits exact selector `FC68` through exact helper `8385`.
- Seeds exact base word `61 = 2E96`, runs exact helper `EC38`, and writes exact descriptor words `169C / A022 / 2E9C / 2022` into exact work band `0880..0886`.
- Uses SNES exact hardware-math registers `4202/4203/4216` with exact multiplicand `71` and exact multiplier `06` to derive exact source base `2C23 + 6*71`, then copies exact `0x0006` bytes from that exact row into exact work band `0F00`.
- Clears exact byte `0F06`.
- Seeds exact word `4E40 = 61FF`, then performs one exact overlapping same-bank block move `4E40 -> 4E42` for exact length `003D`.
- Seeds exact word `0D0E = 01F0`.
- Clears exact block `5E00` and then performs one exact overlapping same-bank clear-propagation move `5E00 -> 5E02` for exact length `03FD`, materializing a zeroed exact `5E00`-family work band.
- Emits exact selector `C41F` through exact helper `ED31`, runs exact helper `86DD`, seeds exact words/bytes `020D = CF3B`, `020F = FF`, `020C = 00`, `0DC5 = 5E00`, and runs exact helper `F90C`.
- Runs exact helper `FB97` twice with exact parameter pairs `(X=50CA, Y=0018, A=00)` and `(X=514A, Y=0018, A=41)`.
- Seeds exact byte `59 = 20`, runs exact long helper `FF:FC04`, then emits exact selector chain `FBCE -> FBF8 -> FC37 -> FC1B -> E53E` through exact helper `8385`.
- Clears exact byte `0F06`, seeds exact byte `0D13 = 1D`, conditionally decrements exact byte `0D9A` only when exact byte `299F == 00`, mirrors exact final status byte into exact byte `299F`, restores flags, and tail-jumps to exact helper `E34A`.

Strongest safe reading: exact large setup / import / selector-emission owner that clears/initializes the live selector state, materializes exact `9890 / 0F00 / 4E40 / 5E00` work bands, drives the exact `F90C/FB97/FFFC04` service chain, emits a fixed exact selector packet chain ending in exact local packet `E53E`, stamps exact bytes `0D13 / 299F`, and then tail-jumps into exact helper `E34A`.

### C2:E53E..C2:E544

This span does not freeze as callable code in this pass. It freezes as the exact local selector packet invoked from exact owner `E40E`.

Key facts now pinned:
- Exact owner `E40E` loads exact `X = E53E` and emits the exact local object through exact helper `8385`.
- Exact bytes: `00 78 00 5E 7E 00 08`.
- The exact bytes sit directly after the terminal exact `PLP ; JMP E34A` tail of owner `E40E` and directly before the exact callable entry at `E545`.

Strongest safe reading: exact local selector packet / descriptor blob consumed by exact helper `8385` from the exact `E40E` owner.

### C2:E545..C2:E575

This span freezes as the exact `9890` table-materialization helper used by exact owner `E40E`.

Key facts now pinned:
- Begins `PHP ; SEP #$20`.
- Seeds exact inner count byte `00 = 0A` and exact outer count byte `01 = 08`.
- Starting from exact selector byte `51`, repeatedly loads exact bytes from exact long table `FF:C9AC,X`.
- Writes each exact fetched byte into exact staging band `9890,Y`, then writes one exact `FF` separator byte.
- After each exact ten-byte inner run, writes one exact `01` delimiter byte and repeats the exact outer run eight times.
- Terminates the exact stream with exact byte `00` and exits `PLP ; RTS`.

Strongest safe reading: exact `9890` table-materialization helper that expands one exact long-table stream from `FF:C9AC` into an exact delimiter-rich `9890` work list containing exact ten-byte inner groups, exact `FF` separators, exact `01` outer delimiters, and a final exact `00` terminator.

### C2:E576..C2:E5CB

This span freezes as the exact zero-lane import / staging owner chosen by the zero lane of exact owner `E1EE`.

Key facts now pinned:
- Begins `PHP ; REP #$30`.
- Copies exact `0x0480` bytes from exact source block `FF:F008` into exact WRAM destination `7E:3600`.
- Then runs an exact twelve-step loop that repeatedly copies exact `0x0010`-byte follow-on source chunks from bank `FF` into the exact destination stream while manually advancing exact destination `Y` by an extra `0x0010` between iterations.
- Emits exact selector `C429` through exact helper `ED31` and runs exact helper `86DD`.
- In 8-bit mode copies exact `0x0020` bytes from exact source block `FF:CE9A` into exact WRAM destination `7E:9500`.
- Seeds exact word `0D0E = 0001`, increments exact byte `0D15`, seeds exact byte `0D13 = 05`, and emits exact selector chain `FBCE -> FBF8 -> FC61` through exact helper `8385`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact zero-lane import / staging owner that imports one large exact `FF:F008` block plus follow-on exact `0x10`-byte slices into WRAM, stages exact block `FF:CE9A -> 7E:9500`, stamps exact bytes `0D0E / 0D15 / 0D13`, and exits through a fixed exact selector chain.

### C2:E5CC..C2:E60A

This span freezes as the exact `(54 + 1)` change-handler / refresh owner at the back edge of the pass.

Key facts now pinned:
- Begins `PHP ; SEP #$20`.
- Loads exact byte `54`, increments the exact accumulator once, and compares the exact result against exact latch byte `0D77`.
- When the exact value is unchanged, returns immediately.
- On exact change, mirrors the exact accumulator into exact bytes `0D77` and `020C`.
- Seeds exact words/bytes `0DC5 = 5248`, `0DCC = 6A20`, `020D = CF3B`, `020F = FF`, `0DC9 = 02`, and `0DD0 = 0200`.
- Runs exact helper `FA49` and exits `PLP ; RTS`.

Strongest safe reading: exact `(54 + 1)` change-handler / refresh owner that watches the live exact selector byte `54`, refreshes exact latch/output bytes `0D77 / 020C`, seeds an exact `5248 / 6A20 / CF3B / 0200` service block, and then reruns exact helper `FA49` only on exact value change.

## Honest remaining gap

- the old seam `C2:E34A..C2:E5F0` is now closed more honestly as `C2:E34A..C2:E60A`
- the old seam end at `C2:E5F0` cut the exact `E5CC` owner in half
- the next live family starts immediately after this pass at `C2:E60B`, and it already shows a mix of one strange stack-relative opener plus clearer downstream exact owners at `E61B`, `E6AE`, `E705`, and `E73F`
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
