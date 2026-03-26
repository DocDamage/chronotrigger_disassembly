# Chrono Trigger Disassembly — Pass 157

## Summary

Pass 157 closes the exact selector-packet data island immediately after exact `C2:FBD0`, then carries the next exact callable/helper family forward through exact `C2:FE09`.

The clean split is:

- one exact local selector/descriptor packet family at `C2:FBD1..C2:FCB1`
- one exact outside-called exact `6E00`/`2C53` quotient-prep owner at `C2:FCB2..C2:FCE0`
- one exact outside-called exact `7800`/`51` sibling quotient-prep owner at `C2:FCE1..C2:FD1C`
- one exact shared exact 24-step divider/helper at `C2:FD1D..C2:FD57`
- one exact exact two-byte multiply wrapper at `C2:FD58..C2:FD67`
- one exact shared exact hardware-multiply accumulation helper at `C2:FD68..C2:FD96`
- one exact staged-add updater at `C2:FD97..C2:FDBA`
- one exact staged-subtract updater at `C2:FDBB..C2:FDDE`
- one exact clamp/normalize helper at `C2:FDDF..C2:FE09`

This pass does **not** force the awkward exact overlap/noise immediately after exact `FE09`.
The next clean forward target should start at the exact follow-on callable family beginning `C2:FE2D`.

## Exact closures

### C2:FBD1..C2:FCB1
This exact span freezes as a local exact selector/descriptor packet family, not live linear code.

The exact byte island is now structurally anchored by repeated exact selector roots already used elsewhere through exact helper `8385`, including exact packet starts `FBCE`, `FBE3`, `FBEA`, `FBFF`, `FC06`, `FC14`, `FC1B`, `FC37`, `FC3E`, `FC45`, `FC4C`, `FC53`, and `FC61`. Earlier exact pass notes and exact caller comments already refer to these exact addresses as selector packets for the downstream exact setup/export/materializer owners, and the exact island itself has no hot direct call entry inside it.

Strongest safe reading: exact local selector/descriptor packet family consumed by the exact packet-emission helpers rooted at exact `8385` and, for at least the exact `FC53` packet, exact helper `ED31`.

### C2:FCB2..C2:FCE0
This exact span freezes as the exact outside-called helper reached from exact `C2:D5B1`.

It begins `PHP ; SEP #$20`, seeds exact byte `04CB = 01`, clears exact byte `1046`, clears exact accumulator through exact `TDC`, then loads exact source byte `04C9`. In exact `REP #$30` mode it doubles that exact source byte into exact index `X`, loads exact word `6E00,X`, and mirrors that exact word into exact `1044`, exact `1047`, and exact direct-page word `04`.

The tail stages exact long-source family `2C53 -> 00` and exact `2C55 -> 02`, then runs exact helper `FD1D` and exits through exact `PLP ; RTS`.

Strongest safe reading: exact exact `6E00[04C9]` quotient-prep owner that seeds exact `04CB`, stages exact divisor/state into exact `1044/1047/04`, stages exact long source `2C53/2C55` into exact `00/02`, and then runs exact divider/helper `FD1D` to derive the exact result bytes later consumed by the caller’s exact compare lane.

### C2:FCE1..C2:FD1C
This exact span freezes as the exact sibling outside-called helper reached from exact `C2:D661`.

Its front half mirrors the exact earlier owner structurally: it seeds exact byte `04CB = 01`, clears exact byte `1046`, loads exact source byte `04C9`, doubles it into exact index `X`, then loads exact word `7800,X`, shifts it right once, adds exact base word `51`, and stores that exact derived word into exact `1044`, exact `1047`, and exact direct-page word `04`.

The second half stages one exact complemented source value instead of the direct exact `2C53/2C55` family. It clears exact word `00`, loads exact constant word `967F`, subtracts exact word `2C53`, stores the exact result into exact `00`, then in exact 8-bit accumulator mode loads exact constant byte `98`, subtracts exact byte `2C55`, stores the exact result into exact byte `02`, and only when that exact subtraction did **not** underflow runs exact helper `FD1D`.

Strongest safe reading: exact sibling quotient-prep owner that derives exact divisor/state from exact `7800[04C9]` plus exact base `51`, stages the exact complemented long-source family `967F:98 - 2C53:2C55` into exact `00/02`, and conditionally runs exact divider/helper `FD1D` only when the exact complemented source stayed in range.

### C2:FD1D..C2:FD57
This exact span freezes as the exact shared exact 24-step divider/helper used by exact `FCB2` and exact `FCE1`.

It begins `PHP ; REP #$30`, stages the exact dividend family from exact `00/02` into the exact work lanes rooted at exact `37/39`, clears the exact higher work lanes `3A/3C`, seeds exact loop count `X = 0018`, and then enters one exact 24-step shift/compare/subtract loop.

Per exact step it shifts exact working lanes `36/38/3A/3C`, checks the exact current high work against the staged exact divisor `04`, conditionally subtracts that exact divisor from the exact `3A/3C` remainder lanes, then rotates the exact quotient lanes again before the exact `DEX ; BNE` loop-back.

Strongest safe reading: exact exact 24-step restoring divider that consumes the staged exact dividend in exact `00/02` and the staged exact divisor in exact `04`, producing the exact result bytes in the exact `36/37/38` family while leaving exact remainder state in the exact higher work lanes `3A/3C`.

### C2:FD58..C2:FD67
This exact span freezes as the exact exact two-byte multiply wrapper called from exact `C2:DBC1`.

It begins `PHP ; JSR FD68`, so it first runs the shared exact multiply/accumulate helper in its exact low-byte form. After that it narrows to exact `SEP #$30`, loads exact byte `01`, writes that exact byte into exact hardware multiply register `4202`, seeds exact `Y = 01`, and branches directly into the shared exact inner loop at exact `FD79`.

Strongest safe reading: exact exact two-byte multiply wrapper that runs the shared exact low-byte exact `FD68` accumulation pass first, then reseeds exact hardware multiply state for the exact second staged byte and rejoins the shared exact accumulation loop at exact `FD79`.

### C2:FD68..C2:FD96
This exact span freezes as the exact shared exact hardware-multiply accumulation helper.

It begins `PHP ; REP #$30`, loads exact start index `Y = 51`, clears exact accumulation words `3E` and `40`, then narrows through exact `SEP #$30`, loads exact staged byte `00`, and writes that exact byte into exact hardware multiply register `4202`.

The exact inner loop at exact `FD79` loads exact source index `X = 51`, reads exact source byte `04,X`, writes that exact byte into exact hardware multiply register `4203`, then in exact widened mode adds exact hardware result word `4216` into exact accumulation word `003E,Y`. After each exact add it advances exact `Y` and exact `X` by one and repeats while exact `X != 02`.

Strongest safe reading: exact shared exact byte-by-byte hardware multiply/accumulate helper that multiplies one exact staged multiplicand byte (`00` or, through exact wrapper `FD58`, exact `01`) against the exact source byte strip rooted at exact `04,X`, adding the exact per-byte hardware product words into the exact accumulation band rooted at exact `3E,Y`.

### C2:FD97..C2:FDBA
This exact span freezes as the exact staged-add updater called from exact `C2:D6A5`.

It begins `PHP ; REP #$20`, loads exact word `2C53`, adds exact staged exact low word `1044`, and stores the exact sum back into exact `2C53`. In exact 8-bit accumulator mode it then loads exact byte `2C55`, adds exact staged exact high/overflow byte `1046`, and stores the exact result back into exact `2C55`. On exact carry it forces exact byte `2C55 = 98`.

The tail then runs exact helper `FDDF` and exits through exact `PLP ; RTS`.

Strongest safe reading: exact staged-add updater that adds the exact staged delta `1044/1046` into the live exact long-source family `2C53/2C55`, saturates the exact high byte to `98` on carry, and then reruns exact clamp/normalize helper `FDDF`.

### C2:FDBB..C2:FDDE
This exact span freezes as the exact staged-subtract updater called from exact `C2:D62D`.

It mirrors the exact prior helper structurally but uses exact subtract instead of add: exact `2C53 - 1044`, then exact `2C55 - 1046`. On exact borrow it forces exact byte `2C55 = 98`, then runs exact helper `FDDF` and exits.

Strongest safe reading: exact staged-subtract updater that subtracts the exact staged delta `1044/1046` from the live exact long-source family `2C53/2C55`, repairs the exact high byte to `98` on borrow, and then reruns exact clamp/normalize helper `FDDF`.

### C2:FDDF..C2:FE09
This exact span freezes as the exact clamp/normalize helper used by exact `FD97` and exact `FDBB`.

It begins `PHP ; SEP #$30 ; LDX #$00`, then checks the exact high byte `2C55` against exact bound byte `98`. Exact values below `98` return immediately. Exact values above `98` clamp immediately. Exact equality continues into one exact low-word compare against exact bound word `967F`.

The exact clamp path writes exact word `2C53 = 967F`, writes exact byte `2C55 = 98`, seeds exact `X = FF`, and exits through exact `PLP ; RTS`. The exact unclamped path returns with exact `X = 00`.

Strongest safe reading: exact exact `98:967F` clamp/normalize helper for the live exact long-source family `2C53/2C55`, returning exact `X = FF` when it had to force the exact bound and exact `X = 00` otherwise.

## Honest remaining gap

- exact `C2:FBD1..C2:FE09` is now honestly separated into one exact packet-data island plus one exact callable/helper cluster
- the awkward exact overlap/noise immediately after exact `FE09` is still not frozen
- the next clean forward target should start at the exact follow-on callable family beginning `C2:FE2D`
