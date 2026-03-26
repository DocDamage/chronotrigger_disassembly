# Chrono Trigger Disassembly — Pass 162

## Purpose

Pass 162 closes the first real downstream worker reached by the exact low-bank veneer at `C3:0008`. The old seam `C3:0077..C3:01E3` was too wide as one monolithic owner: the exact worker itself ends cleanly at `RTL` `C3:01C5`, and the trailing bytes are one exact local fill helper with one exact overlapping late entry.

## What this pass actually proved

### 1) `C3:0077..C3:01C5` is one exact row-pair midpoint-circle/span builder, not one giant startup blob

The exact body:

- saves exact `B/D/P/A/X/Y`
- masks the incoming exact accumulator down to one exact low-byte mode/control value and keeps that exact value on stack for later post-processing
- installs exact direct page `0300`
- clears exact local words/bytes rooted at exact `51 / 53 / 55`
- chooses exact data bank `7E` vs exact data bank `7F` from exact low bit of exact byte `58`

After that exact setup, the owner uses exact bytes/words rooted at:

- exact `50` as the signed/biased horizontal center/input lane
- exact `52` as the vertical center/input lane
- exact `54` as the exact radius/extent lane
- exact `56` as the exact selected row-table base lane
- exact `58` as the exact `7E` vs `7F` destination-bank selector

The strongest proof that this is one exact midpoint-circle-style span owner is the exact arithmetic/control pattern:

- exact `X = 54`
- exact `Y = 0000`
- exact decision/error word seeded through exact `3 - 2*r` / bank-variant equivalent setup
- one exact loop that writes two exact clamped byte pairs per iteration around the exact center byte `50`
- one exact negative vs nonnegative update split that matches the classic midpoint-circle step family:
  - exact negative lane adds exact `4*x + 6`
  - exact nonnegative lane decrements the exact outer extent and adds the exact `4*(x-y) + 10` style update
- exact loop guard `CPX  F0 ; BPL` keeping the two exact symmetric extents walking until the exact inner/outer indices cross

Inside that exact loop, the owner writes clamped exact byte pairs of the form:

- exact `(50 - x)` / exact `(50 + x)`
- exact `(50 - y)` / exact `(50 + y)`

into two exact symmetric row slots derived from the exact `52/56` pair.

Strongest safe reading:
- exact selected-`7E/7F` row-pair midpoint-circle/span builder that materializes clamped left/right byte pairs around one exact center/radius input set rooted at exact `50/52/54/56/58`

### 2) exact zero-radius handling falls into one exact repeated-`0001` row-pair fill helper

When exact word `54 == 0000`, the owner does **not** enter the circle loop.

Instead it:

- restores the saved exact mode/control word from stack
- loads exact fill count `01C0`
- calls exact local helper `C3:01C6`
- exits through the exact shared epilogue at `01BD..01C5`

That proves the exact zero-radius case is one exact deliberate full-band fill path, not one exact malformed corner case.

### 3) post-loop control splits by exact low-byte mode, and exact bit `0x80` suppresses the outer-band fill tail

After the exact midpoint-circle loop, the owner restores the saved exact mode/control word from stack and branches on exact `A & 007F`.

Exact proven split:

- exact low-7-bits `!= 0` and exact `!= 1` returns immediately
- exact low-7-bits `== 0` enters one exact copy/densify lane at `0177..0183`
- exact low-7-bits `== 1` first enters one exact earlier copy/densify lane at `0153..0169`, then may also enter the exact `0177..0183` lane
- exact bit `0x80` in the restored exact control word suppresses the downstream exact leading/trailing repeated-`0001` fill work

Those exact copy lanes are not random tail garbage.
They copy exact row-pair words downward from the exact already-written symmetric rows, densifying the sparse exact midpoint-circle writes into one exact contiguous row-pair band.

Strongest safe reading:
- exact post-raster mode gates controlling whether the exact sparse midpoint-circle row writes stay sparse, are densified through one exact copy lane, or are densified through two exact copy lanes, with exact bit `0x80` suppressing the outer-band padding/fill stage

### 4) `C3:01C6..C3:01E3` is one exact repeated-`0001` row-pair fill helper, and `C3:01CA` is one exact overlapping late entry into it

The exact helper at `01C6`:

- stores the incoming exact 16-bit fill-count into exact word `F0`
- loads exact base pointer `56 -> X`
- derives exact `Y = X + 2`
- writes exact word `0001 -> 0000,X`
- chooses exact bank `7E` vs exact bank `7F` from exact low bit of exact byte `58`
- loads exact count from exact `F0`
- performs exact overlapping same-bank `MVN`:
  - either exact `MVN 7E,7E`
  - or exact `MVN 7F,7F`
- exits exact `RTS`

Because the exact move is overlapping and exact `Y = X + 2`, the helper does **not** behave like one exact generic copy. It seeds exact word `0001` and then propagates that exact seed forward across the downstream selected row-pair band.

The exact entry at `C3:01CA` is one exact overlapping callable late entry:

- it begins after exact `X` and exact fill-count `F0` have already been staged by the caller
- it rejoins the exact shared `TXY / INY / INY / LDA #0001 / STA 0000,X / bank-select / MVN / RTS` tail

Strongest safe reading:
- exact repeated-`0001` selected-row-pair fill helper with one exact overlapping late entry that reuses preseeded exact `X/F0`

## Exact closures frozen this pass

- exact midpoint-circle/span owner at `C3:0077..C3:01C5`
- exact repeated-`0001` selected-row-pair fill helper at `C3:01C6..C3:01E3`
- exact overlapping late entry into that exact helper at `C3:01CA..C3:01E3`

## Important correction to keep in mind

The old seam `C3:0077..C3:01E3` was real work, but it was **not** one exact single owner.

The honest split is:

- exact owner: `C3:0077..C3:01C5`
- exact local helper: `C3:01C6..C3:01E3`
- exact overlapping late entry: `C3:01CA..C3:01E3`

## Best next move after this pass

The next anchored exact downstream owner is still the one reached by the exact low-bank veneer at `C3:000E`:

- exact next manual/raw seam: `C3:01E4..C3:0306`

That keeps low-bank `C3` moving in exact callable-owner order:

- exact `0008 -> 0077` worker now closed
- exact `000E -> 01E4` worker is the next honest follow-on target
