# Chrono Trigger Disassembly — Pass 135

## Focus of this pass

Pass 135 closes the downstream dispatch / packet-build seam that pass 134 left open at `C2:D51A..C2:D715`. The first correction is boundary-related again: the seam does **not** begin at exact code `D51A`. It starts with an exact local 9-word dispatch table at `C2:D519..C2:D52A`, and the real callable/dispatch targets under that table are `D52B`, `D546`, `D58B`, `D645`, `D690`, `D618`, `D6C3`, `D715`, and downstream `D778`.

Within the actual code span, the structure resolves into one exact local dispatch table, one short exact setup/export wrapper, five exact status-gated owners, one shared exact overflow/service body with a second mid-body entry, one exact descending helper at `D605`, and one larger exact compare/build/export owner at `D715`.

## What this pass closes

### 1. exact local 9-word dispatch table at `C2:D519..C2:D52A`

This span is not code. It is the exact local 9-word dispatch table immediately following the already-frozen dispatcher at `D506`.

Exact entries:

- `D52B`
- `D546`
- `D58B`
- `D645`
- `D690`
- `D618`
- `D6C3`
- `D715`
- `D778`

Strongest safe reading: exact local 9-word dispatch table that groups the newly-closed exact service targets `D52B / D546 / D58B / D618 / D645 / D690 / D6C3 / D715` with the still-downstream exact sibling at `D778`.

### 2. exact setup/export wrapper at `C2:D52B..C2:D545`

This short owner is exact and linear:

- begins `JSR DACA`
- seeds exact byte `0D9C = 0B`
- runs exact helper `8A98`
- seeds exact byte `0DA6 = F8`
- seeds exact word `0DA1 = B022`
- increments exact byte `68`
- exits through exact jump `83B2`

Strongest safe reading: exact setup/export wrapper that runs the fixed `DACA -> 8A98` setup lane, seeds exact bytes/words `0D9C / 0DA6 / 0DA1`, increments exact byte `68`, and exits through exact jump `83B2`.

### 3. exact `0D75 = 01` status-gated selector owner at `C2:D546..C2:D58A`

This owner begins by seeding exact phase/state byte `0D75 = 01`, then runs exact helper `E984` and exact `BIT 0D1D`.

Its three exact paths are:

Clear path:

- masks exact bits `5A & 0C`
- when that exact masked value is nonzero, clears exact byte `E0` and runs exact helper `E017`
- compares exact bytes `81` and `54`
- when those exact bytes differ, runs exact helper `EAC2`
- otherwise returns immediately

Negative path:

- clears exact byte `E0`
- forces exact byte `83 = FF`
- runs exact helper `EAC2`
- subtracts exact `08` from exact selector byte `54`
- when the exact result is zero, seeds exact byte `68 = 02` and exits through exact jump `DC7B`
- otherwise seeds exact byte `68 = 03` and exits through exact jump `DE98`

Overflow path:

- exits immediately through exact jump `82B2`

Strongest safe reading: exact `0D75 = 01` status-gated selector owner with a clear-path optional `E017` service, a negative subtract-by-8 lane that chooses exact `68 = 02` vs `68 = 03`, and a direct exact overflow escape to `82B2`.

### 4. exact threshold / compare owner at `C2:D58B..C2:D5D8`

This owner begins `JSR E984 ; BIT 0D1D` and splits three exact ways.

Clear path:

- exits immediately through exact jump `D7CF`

Negative path:

- mirrors exact byte `1040 -> 54`
- loads exact byte `04CA`
- adds exact byte `0D82`
- stores the exact sum in exact byte `00`
- derives exact compare/clamp byte `(62 - 00)` and, when nonnegative, increments it once and stores it back into exact byte `04CA`
- runs exact helper `FCB2`
- tests exact pair `37 | 38`
- when exact pair `37 | 38` is zero, also tests exact byte `36`
- when the exact compare result is below exact byte `04CA`, stores the exact result back into `04CA`
- runs exact helper `EAC2`
- increments exact byte `04CA`
- decrements exact byte `0D9A`
- seeds exact byte `68 = 05`
- exits through exact jump `DF76`
- when the exact derived clamp byte underflows, exits instead through exact jump `EACC`

Overflow path:

- seeds exact byte `54 = 08`
- falls into the shared exact service body at `D5D9`

Strongest safe reading: exact threshold / compare owner that either jumps clear to `D7CF`, runs an exact negative clamp/compare lane around exact bytes `1040 / 04CA / 0D82` and fixed helper `FCB2`, or seeds exact selector byte `54 = 08` before entering the shared exact service body at `D5D9`.

### 5. exact shared overflow/service body at `C2:D5D9..C2:D604`

This span is shared code, not private tail glue. It has two exact entry behaviors:

Primary entry at `D5D9`:

- seeds exact byte `54 = 08`
- continues into the common body

Secondary mid-body entry at exact `D5DD`:

- skips the exact `54 = 08` seed and uses the caller-provided exact selector byte instead

Common body:

- clears exact byte `04C9`
- runs exact helper `DD7C`
- runs exact helper `EAC2`
- runs exact helper `D605`
- emits exact selector `C2B0` through exact helper `ED31`
- emits exact selector `FBE3` through exact helper `8385`
- runs exact helper `8255` with exact accumulator `10`
- seeds exact byte `E0 = 02`
- seeds exact byte `68 = 01`
- exits through exact jump `E012`

Strongest safe reading: exact shared overflow/service body with a primary exact `54 = 08` entry at `D5D9`, a caller-provided-selector entry at exact `D5DD`, and a fixed exact `DD7C -> EAC2 -> D605 -> ED31 -> 8385 -> 8255` tail before exact jump `E012`.

### 6. exact descending `1811` writer helper at `C2:D605..C2:D617`

This helper is short and exact:

- seeds exact byte `00 = 06`
- loops exact byte `00` downward from `06` to `00`
- on each exact iteration:
  - loads the current exact loop byte `00`
  - runs exact helper `F626`
  - writes exact zero byte `00` to exact destination `[1811,Y]`
- exits `RTS`

Strongest safe reading: exact descending 7-step helper that reruns exact helper `F626` while walking exact loop byte `00` from `06` down to `00`, clearing exact destination byte `[1811,Y]` on each exact step.

### 7. exact `0D1F = FF` status dispatcher with negative prep lane at `C2:D618..C2:D644`

This owner starts by seeding exact byte `0D1F = FF`, then runs exact helper `E984` and exact `BIT 0D1D`.

Its exact paths are:

Clear path:

- exits immediately through exact jump `DA01`

Negative path:

- runs exact helpers `8791`, `FDBB`, and `DCDA`
- loads exact accumulator `55`
- runs exact helper `EABA`
- then continues into the shared tail below

Overflow path:

- skips the exact negative prep chain and enters directly into the shared tail below

Shared tail:

- runs exact helper `EAC2`
- clears exact byte `0D9A`
- seeds exact byte `68 = 02`
- exits through exact jump `DFCF`

Strongest safe reading: exact `0D1F = FF` status dispatcher that jumps clear to `DA01`, uses the exact negative prep chain `8791 -> FDBB -> DCDA -> EABA(55)` before the common `EAC2 / 68 = 02 / DFCF` tail, and lets the overflow case enter that common tail directly.

### 8. exact sibling threshold / compare owner at `C2:D645..C2:D68F`

This owner is the structural sibling of exact owner `D58B`.

It begins `JSR E984 ; BIT 0D1D` and splits three exact ways.

Clear path:

- exits immediately through exact jump `D8B2`

Negative path:

- mirrors exact byte `1042 -> 54`
- requires both exact bytes `04C9` and `04CA` to be nonzero; otherwise it exits through exact jump `EACC`
- runs exact helper `FCE1`
- tests exact pair `37 | 38`
- when exact pair `37 | 38` is zero, also tests exact byte `36`
- when the exact compare result is below exact byte `04CA`, stores the exact result back into `04CA`
- runs exact helper `EAC2`
- increments exact byte `04CA`
- decrements exact byte `0D9A`
- seeds exact byte `68 = 04`
- exits through exact jump `DF76`

Overflow path:

- seeds exact byte `54 = 09`
- exits through the shared secondary entry exact jump `D5DD`

Strongest safe reading: exact sibling threshold / compare owner that jumps clear to `D8B2`, runs an exact negative compare lane around exact bytes `1042 / 04C9 / 04CA` and fixed helper `FCE1`, or seeds exact selector byte `54 = 09` before entering the shared exact service body at `D5DD`.

### 9. exact `0D1F = FF` sibling dispatcher with direct overflow entry at `C2:D690..C2:D6C2`

This owner again begins by seeding exact byte `0D1F = FF`, then runs exact helper `E984` and exact `BIT 0D1D`.

Its exact paths are:

Clear path:

- exits immediately through exact jump `DA01`

Negative path:

- runs exact helpers `87D5` and `FD97`
- loads exact accumulator `55`
- runs exact helper `EABA`
- then continues into the shared tail below

Overflow path:

- skips the exact negative prep chain and enters the shared tail directly at exact `D6AD`

Shared tail:

- clears exact byte `0D97`
- runs exact helper `EAC2`
- seeds exact byte `68 = 03`
- clears exact byte `0D9A`
- runs exact helpers `DFCF` and `DECC`
- exits through exact jump `DF31`

Strongest safe reading: exact `0D1F = FF` sibling dispatcher that jumps clear to `DA01`, uses the exact negative prep chain `87D5 -> FD97 -> EABA(55)` before the common `STZ 0D97 / EAC2 / 68 = 03 / DFCF / DECC / DF31` tail, and lets the overflow case enter that common tail directly.

### 10. exact status-gated compare owner with overflow build/export tail at `C2:D6C3..C2:D714`

This owner begins `JSR E984 ; BIT 0D1D`.

Its exact paths are:

Clear path:

- masks exact bits `5A & 0C`
- when the exact masked value is nonzero, enters the overflow build/export tail below
- otherwise compares exact bytes `81` and `54`
- when the exact bytes differ, runs exact helper `EAC2`
- returns immediately

Negative path:

- runs exact helper `EAC2`
- runs exact helper `E0A5`
- increments exact byte `68`
- returns immediately

Overflow / forced-build path:

- runs exact helper `EAC2`
- runs exact helper `F5A7`
- clears exact byte `00`
- seeds exact word `02 = 001C`
- runs exact helper `E058`
- increments exact byte `0D15`
- mirrors exact byte `54 -> 79`
- mirrors exact byte `80 -> 54`
- seeds exact byte `E0 = 02`
- seeds exact byte `68 = 01`
- emits exact selector `C2B0` through exact helper `ED31`
- emits exact selector `FBE3` through exact helper `8385`

Strongest safe reading: exact status-gated compare owner that either returns after the optional `81/54` compare, takes a short exact negative `E0A5` lane that bumps exact byte `68`, or enters a larger exact overflow/forced-build export tail around exact helpers `F5A7`, `E058`, `ED31`, and `8385`.

### 11. exact status-gated compare / block-move export owner at `C2:D715..C2:D777`

This owner begins `JSR E984 ; BIT 0D1D`.

Its exact paths are:

Clear path:

- runs exact helpers `9F05` and `E162`
- compares exact bytes `81` and `54`
- when the exact bytes differ, runs exact helper `EAC2`
- returns immediately

Negative path:

- mirrors exact byte `81 -> 54`
- tests exact byte `0FC6`
- when exact byte `0FC6 == 0`, exits through exact jump `EACC`
- otherwise runs exact helper `EAC2`
- seeds exact byte `54 = 04`
- increments exact byte `68`
- returns immediately

Overflow path:

- runs exact helper `EAC2`
- clears the exact accumulator (`TDC`)
- copies exact `0x48` bytes from exact block `9990 -> 9380` through exact `MVN 7E,7E`
- seeds exact word `02 = 0004`
- runs exact helper `E072`
- derives exact selector byte `54 = 71 + 0C`
- decrements exact byte `68`
- seeds exact byte `0D13 = 2F`
- increments exact byte `0D0B`
- runs exact helper `8255` with exact accumulator `50`
- emits exact selector `FBE3` through exact helper `8385`

Strongest safe reading: exact status-gated compare / block-move export owner that either returns after the clear compare lane, uses a negative exact `0FC6` gate to choose `EACC` vs `EAC2 + 54 = 04 + INC 68`, or enters a larger exact overflow lane that copies exact block `9990 -> 9380`, derives exact selector byte `54` from exact byte `71`, stamps exact byte `0D13 = 2F`, increments exact byte `0D0B`, and exits through exact selector `FBE3`.

## Net effect of pass 135

The old seam at `C2:D51A..C2:D715` is now closed more honestly as `C2:D519..C2:D777`.

It resolves into:

- one exact local 9-word dispatch table
- one short exact setup/export wrapper
- five exact status-gated owners
- one shared exact overflow/service body with a second mid-body entry
- one exact descending helper at `D605`
- one larger exact compare/build/export owner at `D715`

## Remaining honest gaps after this pass

- the downstream exact dispatch sibling at `C2:D778..` is still open
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
- the next real code seam now moves naturally to `C2:D778..C2:D8B1`
