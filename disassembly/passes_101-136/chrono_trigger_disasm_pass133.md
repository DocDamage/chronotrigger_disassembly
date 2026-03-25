# Chrono Trigger Disassembly — Pass 133

## Focus of this pass

Pass 133 closes the downstream callable poll / row-build seam that pass 132 left open at `C2:D19F..C2:D2C3`. The main structural correction here is that the seam does **not** stop at `D2C3`: once `D19F` and the always-called `D2C4` helper are decoded cleanly, the region naturally resolves as one 3-row template/export owner, one per-slot threshold/setup helper, one tiny `020C = 1A` wrapper, one block-shift/service helper, one repeated bit-shift helper, one 3-byte local repeat-count table, and one externally-callable `0D8C` refresh owner.

## What this pass closes

### 1. exact 3-row template/export owner at `C2:D19F..C2:D265`

This owner begins `PHP ; REP #$30` and runs in two clean stages.

Stage one is an exact 3-row initializer:

- derives exact destination row base `61 = 7600 + ((78 & FF00) >> 2)`
- mirrors exact word `7B -> 22`
- seeds exact row count byte `24 = 03`
- across three exact rows:
  - fills exact row start byte `[61] = FF`
  - loads exact signed selector byte `30:0580[x]`
  - when that exact selector byte is non-negative:
    - seeds exact multiplier registers `4202/4203`
    - builds an exact source offset from `7B + 0200 + 4216`
    - copies exact `0009` bytes from `30:0012+offset -> 7E:[61+000F]`
    - builds an exact second source offset from `7B + 05B0 + 4216`
    - copies exact `0006` bytes from that second source window into the same exact row tail
  - advances exact row base `61` by exact `10`
  - increments exact mirrored selector word `22`
- exits the 3-row loop when exact row count byte `24` reaches zero

Stage two is an exact per-row export/finalizer:

- reloads exact row base `61` and exact selector word `7B`
- copies exact word `30:059C[x]`, clamped to exact ceiling `03E7`, into exact row start
- copies exact masked exact word `30:05F3[x] & 01FF` into the next row word
- copies exact `000A` bytes from exact source `30:05E0+7B` into the row payload tail
- copies exact word `30:059E[x]` into the row tail word
- checks exact high bit of exact word `30:0793[x]`
  - when set, mirrors exact byte `51` into exact row bytes `[61+0004]` and `[61+0005]`
- runs exact helper `D266`
- exits `PLP ; RTS`

Strongest safe reading: exact 3-row template/export owner that derives an exact `7600`-based row window from `78`, fills three exact rows with negative-gated template imports from bank `30`, then writes the exact `059C / 05F3 / 05E0 / 059E / 0793` export fields for the current selector word `7B` before tailing into exact helper `D266`.

### 2. exact per-slot threshold/setup helper at `C2:D266..C2:D28C`

This helper is the exact local tail of `D19F`.

It does the following exactly:

- begins `PHP ; SEP #$20`
- loads exact selector index byte `7B` and exact slot byte `79`
- stores exact low 3 bits of exact byte `30:0591[x]` into exact slot byte `0D79[79]`
- loads exact comparison byte `30:0603[x]`
- enters an exact descending threshold search over exact table `FF:D024`
  - starts exact search index `X = 1A`
  - decrements until exact compare becomes `>= table[x]`
- stores the resulting exact threshold index into exact byte `020C`
- runs exact helper `D296`
- exits `PLP ; RTS`

Strongest safe reading: exact per-slot threshold/setup helper that derives exact low-3-bit slot state `0D79[79]` from `30:0591[x]`, bucketizes exact byte `30:0603[x]` against exact table `FF:D024`, stores the exact winning index in `020C`, and then tail-calls exact helper `D296`.

### 3. exact local `020C = 1A` wrapper at `C2:D28D..C2:D295`

Exact bytes decode to:

- `PHP`
- `SEP #$20`
- `LDA #$1A`
- `STA $020C`
- `PLP`

and then fall directly into exact helper `D296`.

Strongest safe reading: exact local wrapper that only seeds exact byte `020C = 1A` before falling into the shared exact helper at `D296`.

### 4. exact block-shift / service helper at `C2:D296..C2:D305`

This helper is the shared service target for both `D266` and `D28D`.

It does the following exactly:

- begins `PHP ; SEP #$20`
- seeds exact byte `020F = FF`
- in 16-bit mode seeds exact word `020D = D03E`
- derives exact word `0DC5 = 7000 + ((78 & 0300) << 1)`
- clears the first exact word at the active exact `0DC5`-based block head
- uses exact overlapping same-bank move `7E -> 7E` for exact length `01FE` starting at the exact `0DC5`-based block head, effectively shifting/opening the live block by exact two bytes
- runs exact helper `F90C`
- in 8-bit mode loads exact repeat count from exact local table `D329[79]`
- runs exact helper `D306` that exact many times
- exits `PLP ; RTS`

Strongest safe reading: exact shared block-shift / service helper that seeds exact service bytes `020D/020F`, derives the active exact `0DC5` block from the high bits of `78`, performs an exact in-place 2-byte opening shift over exact length `01FE`, runs exact helper `F90C`, then repeats exact helper `D306` according to exact local table `D329[79]`.

### 5. exact repeated four-strip bit-shift helper at `C2:D306..C2:D328`

This helper resolves cleanly into one exact counted loop:

- loads exact block base word `X = 0DC5`
- seeds exact loop count `Y = 0010`
- per exact iteration:
  - `LSR 0000,x`
  - `ROR 0010,x`
  - `LSR 0100,x`
  - `ROR 0110,x`
  - `INX`
- repeats for exact `0x10` iterations
- exits `RTS`

Strongest safe reading: exact repeated four-strip bit-shift helper that walks sixteen exact columns from exact base `0DC5`, shifting and rotating the paired exact rows at offsets `0000 / 0010 / 0100 / 0110`.

### 6. exact local repeat-count table at `C2:D329..C2:D32B`

Exact 3-byte local table used by `D296`:

- exact bytes: `03 02 02`

Strongest safe reading: exact local repeat-count table keyed by exact slot byte `79` for the shared exact helper `D296`.

### 7. exact externally-callable `0D8C` refresh owner at `C2:D32C..C2:D36B`

This owner has real outside callers at exact `CF21`, `D153`, and `E90F`.

It does the following exactly:

- begins `PHP ; SEP #$30`
- loads exact slot byte `79`
- mirrors exact byte `0D79[79] -> 0D8C`
- in 16-bit mode derives exact word `63 = 3E8C + (78 & 0300)`
- seeds exact word `5F = 0418`
- runs exact helper `ECDB`
- rewrites exact word `63 = (63 & FFC0) | 0004`
- seeds exact word `5F = 0404`
- runs exact helpers `EDF6` and `EE7F`
- in 8-bit mode masks exact byte `2991 & 07`
- stores the masked exact result back into exact byte `0D8C`
- exits `PLP ; RTS`

Strongest safe reading: exact externally-callable `0D8C` refresh owner that seeds exact byte `0D8C` from exact per-slot state byte `0D79[79]`, runs the fixed exact `ECDB / EDF6 / EE7F` helper chain using exact words `63` and `5F`, then finalizes `0D8C` from exact byte `2991 & 07`.

## Net effect of pass 133

The old seam at `C2:D19F..C2:D2C3` is no longer open. It resolves into:

- one exact 3-row template/export owner
- one exact per-slot threshold/setup helper
- one tiny exact `020C = 1A` wrapper
- one exact shared block-shift / service helper
- one exact repeated four-strip bit-shift helper
- one exact 3-byte local repeat-count table
- one exact externally-callable `0D8C` refresh owner

## Remaining honest gaps after this pass

- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
- the next real code seam now moves naturally to `C2:D36C..C2:D520`
