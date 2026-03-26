# Chrono Trigger Disassembly — Pass 161

## Purpose

Pass 161 breaks the low-bank `C3` startup cluster open by hand instead of trusting the toolkit's current false "non-ROM-mapped" warning for `C3:0000`. The exact bank head is real ROM at payload/file offset `0x030000`, and this pass freezes the bank-head entry veneers, the duplicated embedded `C2:DECE` pointer constants between them, the exact launcher at `C3:0014`, and the two exact temporary RAM-trampoline bodies that launcher installs at `0504` and `0500`.

## What this pass actually proved

### 1) `C3:0000` is real mapped ROM, not a fake seam

The exact first bytes at payload/file offset `0x030000` are:

`80 12 4C 57 05 CE DE C2 4C 77 00 CE DE C2 4C E4 01 4C FA 0E`

That exact stream cleanly splits as:

- `C3:0000..0001` — `BRA $0014`
- `C3:0002..0004` — already-proven exact unpack veneer `JMP $0557`
- `C3:0005..0007` — exact raw long constant `CE DE C2` = `C2:DECE`
- `C3:0008..000A` — exact veneer `JMP $0077`
- `C3:000B..000D` — exact second raw long constant `CE DE C2` = `C2:DECE`
- `C3:000E..0010` — exact veneer `JMP $01E4`
- `C3:0011..0013` — exact veneer `JMP $0EFA`

So the honest correction is that low-bank `C3` is one exact real bank-head veneer/data cluster, not one exact unmapped ghost span.

### 2) `C3:0008`, `C3:000E`, and `C3:0011` are exact live entry veneers

Manual exact ROM-wide call-byte search shows:

- exact `JSL C3:0008` appears **11** times
- exact `JSL C3:000E` appears **3** times
- exact `JSL C3:0011` appears **1** time

That is enough to treat all three exact heads as deliberate callable entry veneers even before their downstream worker bodies are fully split.

### 3) `C3:0014..C3:0076` is one exact launcher that installs temporary RAM trampolines, stages one packed-stream load, and jumps into WRAM

The exact body begins:

`78 48 A9 5C 8D 00 05 8D 04 05 A2 29 05 8E 05 05 A2 48 05 8E 01 05 A9 C3 8D 03 05 8D 07 05 ...`

Exact proven structure:

- `SEI ; PHA`
- writes exact opcode byte `5C` to exact RAM trampoline heads `0500` and `0504`
- writes exact words `0548 -> 0501` and `0529 -> 0505`
- writes exact bank byte `C3 -> 0503` and `0507`

So the installed exact RAM trampolines are:

- exact `0500 = JML C3:0548`
- exact `0504 = JML C3:0529`

After that, the owner:

- writes exact caller/restored accumulator byte to exact `0384`
- tests exact bit `0x80`
- when that exact bit is set:
  - writes exact `0F -> $2100`
  - clears exact `$420C`
  - writes exact `A1 -> $4200`
  - writes exact `00D3 -> $4209`
  - reads exact `$4211`
  - runs exact `CLI`
- then switches exact accumulator to 16-bit
- loads one exact 16-bit source word from exact long address `FE:0003 -> 0300`
- seeds exact destination word `3000 -> 0303`
- seeds exact source bank byte `C3 -> 0302`
- clears exact destination bank byte `0305`
- calls exact unpack core `JSL C3:0557`
- tail-jumps exact `JML 7E:3000`

Strongest safe reading:
- exact bank-head launcher that installs temporary exact `C3` RAM interrupt trampolines, conditionally seeds exact display/NMI timing state, stages one exact packed-stream job from the exact source-word slot at `FE:0003` into exact WRAM destination `7E:3000`, then transfers control to exact `7E:3000`

### 4) the installed exact trampoline bodies are present and match the launcher

#### `C3:0529..C3:0547`

Exact body:

`E2 20 48 AF 11 42 00 AF 12 42 00 89 40 D0 F8 AF 12 42 00 89 40 F0 F8 A9 80 8F 00 21 00 68 40`

Exact proven structure:

- `SEP #$20 ; PHA`
- reads exact `$4211`
- polls exact `$4212` across an exact bit-`0x40` transition
- writes exact `80 -> $2100`
- restores `A`
- exits exact `RTI`

Strongest safe reading:
- exact temporary exact `C3` RAM-trampoline body that waits on exact `$4212` timing state, forces exact display blank through exact `$2100 = 0x80`, and returns via exact `RTI`

#### `C3:0548..C3:0556`

Exact body:

`E2 20 48 AF 10 42 00 A9 0F 8F 00 21 00 68 40`

Exact proven structure:

- `SEP #$20 ; PHA`
- reads exact `$4210`
- writes exact `0F -> $2100`
- restores `A`
- exits exact `RTI`

Strongest safe reading:
- exact temporary exact `C3` RAM-trampoline body that acknowledges exact NMI latch `$4210`, restores exact display state through exact `$2100 = 0x0F`, and returns via exact `RTI`

## Exact closures frozen this pass

- exact low-bank branch-over head at `C3:0000..C3:0001`
- exact duplicate raw long constants at `C3:0005..C3:0007` and `C3:000B..C3:000D`
- exact direct entry veneers at `C3:0008..C3:000A`, `C3:000E..C3:0010`, and `C3:0011..C3:0013`
- exact launcher owner at `C3:0014..C3:0076`
- exact temporary RAM-trampoline bodies at `C3:0529..C3:0547` and `C3:0548..C3:0556`

## Important correction to keep in mind

The current toolkit inspector's exact HiROM address guard is wrong for this exact low-bank case. For exact `C3:0000`, the tool says "non-ROM-mapped", but the exact payload bytes at `0x030000` prove otherwise. That is one exact toolkit limitation, not one exact reason to ignore the bank head.

## Best next move after this pass

The next clean exact callable worker band is the exact worker reached by the exact live entry veneer at `C3:0008`:

- exact next manual/raw seam: `C3:0077..C3:01E3`
- exact follow-on anchored owner right after it: `C3:01E4..`

That keeps the exact entry-veneer cluster honest while moving into the exact first real downstream worker body instead of stalling on the bank head.
