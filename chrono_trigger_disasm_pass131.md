# Chrono Trigger Disassembly — Pass 131

## Focus of this pass

Pass 131 closes the downstream callback / dispatch seam that pass 130 left open at `C2:CED2..C2:CF92`, and it tightens the immediately-following callable initializer at `C2:CFFB..C2:D048` because the newly-frozen `CFA2` owner calls it directly.

## What this pass closes

### 1. callback entry / dispatch table root at `C2:CED2`

The seam does **not** open with plain code. It opens with one real entry stub and a local dispatch table:

- `C2:CED2..C2:CED3` is just `BRA $CEC2`, a local entry stub that falls back into the already-frozen `0D13.bit10` wrapper.
- `C2:CED4..C2:CEDB` is a local 4-word dispatch table with exact entries:
  - `CEDC`
  - `CEFD`
  - `CF61`
  - `CF92`

That means the real downstream owners in this seam are `CEDC`, `CEFD`, `CF61`, and `CF92`, not one undifferentiated blob.

### 2. exact bit-6 OR gate owner at `C2:CEDC..C2:CEFC`

This owner ORs exact bytes/words `0D34`, `0294`, `0299`, and `029E`, keeps only exact bit `0x40`, and splits:

- set path:
  - `STZ 67`
  - `68 = 01`
  - `JMP EACC`
- clear path:
  - `JSR EAC2`
  - `INC 68`
  - `JMP D0E5`

Strongest safe reading: exact bit-6 gate owner that either arms the `67/68` immediate lane into `EACC` or falls through the `EAC2 -> D0E5` counted path.

### 3. exact `0D1D`-gated dispatcher at `C2:CEFD..C2:CF2F`

This owner starts with the familiar exact prologue `JSR E984 ; BIT 0D1D` and splits three ways:

- negative path (`BMI`):
  - indexes exact byte `0D49,X` with `X = 79`
  - when that exact byte is nonzero:
    - `JSR EAC2`
    - mirrors exact byte `54 -> 0F00`
    - `INC 68`
    - `JMP D4BB`
  - when that exact byte is zero:
    - `JSR CF37`
    - `JSR D32C`
    - emits exact selector `FC0D` through `8385`
    - tail-emits local selector `CF30` through `8385`
- overflow path (`BVS`): exact jump tail `9A98`
- clear path: exact jump into sibling owner `CFA2`

Strongest safe reading: exact `0D1D`-gated dispatcher with a negative-path slot test on `0D49[79]`, a clear-path handoff into `CFA2`, and an overflow jump to `9A98`.

### 4. local selector packet at `C2:CF30..C2:CF36`

Exact 7-byte local descriptor consumed by the zero-slot negative path above:

- exact bytes: `00 79 00 70 7E 00 06`

### 5. exact immediate packet / service owner at `C2:CF37..C2:CF5D`

This helper:

- seeds exact bytes:
  - `1E00 = 19`
  - `1E01 = 8A`
  - `1E02 = 80`
- runs exact long helper `C7:0004`
- indexes exact slot byte `0D49,X` using exact index `79` and forces that exact slot byte to `FF`
- runs exact long helper `FFF9FB`
- runs exact helper chain `821E -> D19F -> 821E`

Strongest safe reading: exact immediate `1E00/1E01/1E02` packet emitter plus service tail that marks exact slot `0D49[79] = FF` and then runs the fixed `FFF9FB / 821E / D19F / 821E` chain.

### 6. exact overflow jump tail at `C2:CF5E..C2:CF60`

- exact bytes decode to `JMP 9A98`
- this is the overflow landing pad used by the `CEFD` dispatcher

### 7. exact sibling `0D1D`-gated owner at `C2:CF61..C2:CF91`

This sibling also starts with `JSR E984 ; BIT 0D1D` and resolves cleanly:

- clear/non-overflow path:
  - compares exact byte `54` against exact byte `81`
  - when unequal, runs exact helper `EAC2`
  - then returns `RTS`
- negative path when exact byte `54 == 03`:
  - `JSR CF37`
  - `68 = 01`
  - `JSR D4D5`
  - `JMP CF21` (reusing the already-frozen `D32C -> 8385` negative-path tail)
- all other negative/overflow cases:
  - `JSR EAC2`
  - `68 = 01`
  - `JMP D4D5`

Strongest safe reading: exact sibling `0D1D`-gated owner that either returns after a `54 vs 81` compare, or routes through the `CF37 / D4D5` negative-family service lane.

### 8. exact decrementing wrapper at `C2:CF92..C2:CFA1`

This helper:

- decrements exact byte `0D9B`
- runs exact helper `E984`
- tests exact status byte `0D1D`
- when neither negative nor overflow are set, returns immediately
- when either negative or overflow is active, branches into exact shared tail `CF88`

Strongest safe reading: exact `0D9B`-decrementing wrapper that conditionally reuses the shared `CF88` negative/overflow service tail.

### 9. exact state-refresh / strip-expansion owner at `C2:CFA2..C2:CFFA`

This owner begins `PHP ; SEP #$20` and does a real multi-stage refresh:

- mirrors exact byte `54 -> 79`
- compares exact byte `54` against exact byte `7F`, then mirrors exact byte `54 -> 7F`
- when the exact value changed, runs exact helper `EAC2`
- runs exact helper `CFFB`
- in 16-bit mode:
  - clears exact word `3200`
  - performs exact overlapping same-bank block move `3200 -> 3202` for exact length `023E`
  - copies exact `0012` bytes from exact source `3200` into exact destination `5248`
  - then copies the next exact `0012` bytes into exact destination `5288`
- back in 8-bit mode:
  - when exact byte `0D49[79] != 0`, runs exact helper `D36C`
  - emits exact selectors `FC0D`, `FBDC`, and `FC29` through exact helper `8385`
- exits `PLP ; RTS`

Strongest safe reading: exact state-refresh / strip-expansion owner that refreshes the `54/79/7F` state, runs exact initializer `CFFB`, expands the exact `3200` work strip into downstream exact buffers `5248/5288`, optionally runs `D36C`, then emits three exact selector packets.

### 10. exact callable block/template initializer at `C2:CFFB..C2:D048`

This callable helper is used directly by `CFA2` and other already-live callers.

It does the following exactly:

- begins `PHP ; REP #$30`
- copies exact `0021` bytes from embedded exact source `C2:D044..C2:D064` into exact WRAM destination `7E:9720`
- copies exact `0010` bytes from exact source `7E:9710` into exact destination `7E:969A`
- seeds exact words:
  - `9694 = 969A`
  - `9696 = 9300`
  - `9698 = 0010`
- in 8-bit mode derives exact index `X = 7F * 3`
- writes exact byte `20` into exact slot `969D,X`
- sets exact bits `0xC0` in exact word/byte `0D13`
- in 16-bit mode writes exact word `9740` into exact slot `969E,X`
- exits `PLP ; RTS`

Strongest safe reading: exact callable block/template initializer that copies one embedded exact 0x21-byte template into `9720`, mirrors a 16-byte exact WRAM strip into `969A`, seeds exact metadata words `9694/9696/9698`, and stamps a per-slot exact 3-byte descriptor keyed by exact byte `7F` while arming exact bits `0xC0` in `0D13`.

## Net effect of pass 131

The old seam at `C2:CED2..C2:CF92` is no longer open. It resolves into:

- one local entry stub
- one exact 4-word dispatch table
- four exact downstream owners / wrappers
- one exact local selector packet
- one exact immediate packet / service helper
- one exact overflow jump tail
- one exact state-refresh / strip-expansion owner
- one exact callable block/template initializer

## Remaining honest gaps after this pass

- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
- the next real code seam now moves to `C2:D065..C2:D0C5`
