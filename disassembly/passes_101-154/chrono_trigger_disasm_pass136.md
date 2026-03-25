# Chrono Trigger Disassembly Progress — Pass 136

## Summary

Pass 136 closes the downstream dispatch sibling seam that pass 135 left open at `C2:D778..C2:D8B1`, but the clean closure is wider than that old seam hint. The real callable/code units here are:

- one exact status-gated sibling owner at `C2:D778..C2:D7CE`
- one larger exact refresh/build owner at `C2:D7CF..C2:D8B1`
- one exact sibling refresh/build owner at `C2:D8B2..C2:D994`
- one shared exact sign-split block/template helper at `C2:D995..C2:D9FF`

The important correction is structural again: `C2:D778..C2:D8B1` was not one monolithic owner. It is one short sibling dispatch target followed by two larger exact owners that both reuse the same exact helper at `D995`.

## What this pass closes

### C2:D778..C2:D7CE

This span freezes as the exact status-gated sibling owner hanging off the pass-135 9-word local dispatch table entry `D778`.

Key facts now pinned:
- Begins with exact gate pattern `JSR E984 ; BIT 0D1D`.
- Clear path runs exact helpers `9F05` and `E162`, compares exact bytes `81` and `54`, reruns exact helper `EAC2` only when the exact bytes differ, and returns.
- Negative path seeds exact byte `04CB = 01`, uses exact index byte `0D26` as `Y`, stages exact byte `[6F],Y -> 04C9`, runs exact helper `8791`, loads exact table byte `9A90,Y -> 04C9`, stores that exact byte back through `[6F],Y`, then runs exact helpers `87D5`, `EABA(B5)`, `9137`, and `A6F0(3664)`.
- Overflow path does not start a separate owner; it enters the exact shared cleanup tail already used by the negative path.
- Shared tail runs exact helpers `EAC2`, `8820`, and `E18A`, clears exact byte `04C9`, decrements exact byte `68`, mirrors exact byte `77 -> 54`, and returns.

Strongest safe reading: exact status-gated sibling owner that either returns after the exact `81/54` compare lane, takes a negative indirect-slot refresh lane through exact bytes `[6F],Y`, `04C9`, and table `9A90,Y`, or enters the same exact `EAC2 -> 8820 -> E18A` cleanup tail directly from overflow.

### C2:D7CF..C2:D8B1

This span freezes as the first larger exact refresh/build owner that the earlier `D58B` clear-path hands off into.

Key facts now pinned:
- Entry begins `SEP #20 ; LDA 1041 ; STA 0DD9 ; JSR 93BF`.
- When exact helper `93BF` returns nonzero, the owner restores exact byte `0DD9 -> 1041`, runs exact helpers `DD02` and `821E`, and rejoins the main positive lane.
- Otherwise it probes exact helper `EA53`; the negative result does not return immediately but enters an exact retry / clamp sublane keyed by exact bytes `104A`, `54`, and `1041`.
- Main positive lane seeds exact byte `1040 = 54`, derives exact index byte/word `0D26 = 54 + 1041`, loads exact bytes `1020[X] -> 04CA` and `1000[X] -> 04C9`, runs exact helper `F2F3`, mirrors exact byte `0D26 -> 83`, conditionally reruns exact helper `DD7C` when exact byte `83` changed, compares exact bytes `54` and `81`, reruns exact helper `EAC2` only on mismatch, and exits through exact selector `FBE3` via exact helper `8385`.
- Retry / clamp sublane compares exact byte `104A - 02` against exact derived byte `54 + 1041 - 01`, loops back into the main positive lane while the exact bound still holds, and otherwise falls into the larger exact export tail.
- Larger exact export tail seeds exact words `9696 = 9083` and `9698 = 0025`, seeds exact byte `0DAA = 09`, runs exact helper `EB9B`, adjusts exact byte `1041` up or down based on exact bit test `5A & 04`, mirrors exact byte `1041 -> 0D95`, mirrors exact byte `54 -> 22`, seeds exact word `61 = 335C`, runs exact helper `DD20`, emits exact selector `FBE3` through exact helper `8385`, and reruns exact helper `EAC2`.
- Final exact post-export stage inspects the sign preserved from exact byte `0D18` across `REP #30`. When non-negative, it runs an exact stepped loop `0DAB += 0D22` for exact counter byte `0D24`, rerunning exact helper `EB1F` until the counter expires. Both sign cases then run exact shared helper `D995`, clear exact bytes `0D22` and `0D11`, seed exact word `9694 = 9710`, set exact bit `0D13 |= 80`, and jump back into the main positive lane.

Strongest safe reading: exact refresh/build owner that stages exact row bytes from `1000/1020`, conditionally refreshes the live index window around exact bytes `1040/1041/104A`, emits exact selector `FBE3` after exact `DD20`, and then optionally runs an exact stepped `0DAB/0D22/0D24` post-export loop before the shared exact `D995` block/template helper and restart.

### C2:D8B2..C2:D994

This span freezes as the sibling exact refresh/build owner that earlier exact owner `D645` clears into.

Key facts now pinned:
- Entry begins `SEP #20 ; LDA 1043 ; STA 0DD9 ; JSR 93BF`.
- Nonzero result from exact helper `93BF` restores exact byte `0DD9 -> 1043`, runs exact helpers `DF31` and `821E`, and rejoins the main positive lane.
- Otherwise the owner probes exact helper `EA53`; the negative result enters the exact retry / clamp sublane keyed by exact bytes `1049`, `54`, and `1043`.
- Main positive lane seeds exact byte `1042 = 54`, derives exact index byte/word `0D26 = 54 + 1043`, loads exact bytes `5700[X] -> 04CA` and `5600[X] -> 04C9`, runs exact helper `F2F3`, mirrors exact byte `0D26 -> 83`, conditionally reruns exact helper `DD7C` when exact byte `83` changed, compares exact bytes `54` and `81`, reruns exact helper `EAC2` only on mismatch, and exits through exact selector `FBE3` via exact helper `8385`.
- Retry / clamp sublane compares exact byte `1049 - 02` against exact derived byte `54 + 1043 - 01`, loops back into the main positive lane while the exact bound still holds, and otherwise falls into the larger exact export tail.
- Larger exact export tail mirrors the earlier owner structurally but uses exact helper `DF51` instead of `DD20`; it seeds exact words `9696 = 9083`, `9698 = 0025`, seeds exact byte `0DAA = 09`, runs exact helper `EB9B`, adjusts exact byte `1043` via exact bit test `5A & 04`, mirrors exact byte `1043 -> 0D95`, mirrors exact byte `54 -> 22`, seeds exact word `61 = 335C`, runs exact helper `DF51`, emits exact selector `FBE3` through exact helper `8385`, reruns exact helper `EAC2`, and then shares the same exact `0DAB / 0D22 / 0D24 / D995 / 9694 / 0D13.bit7` post-export structure.

Strongest safe reading: exact sibling refresh/build owner that stages exact row bytes from `5600/5700`, refreshes the live index window around exact bytes `1042/1043/1049`, emits exact selector `FBE3` after exact `DF51`, and then shares the same exact stepped post-export `D995` finalizer/restart structure as `D7CF`.

### C2:D995..C2:D9FF

This span freezes as the exact shared sign-split block/template copy helper used by both `D7CF` and `D8B2`.

Key facts now pinned:
- Begins by testing exact signed byte `0D21`.
- Non-negative path seeds exact pointers `00 = 2F9C`, `02 = 2F1C`, exact loop count `04 = 0010`, then copies exact `0x20`-byte slices forward via exact `MVN 7E,7E`, advancing both exact pointers by exact `0x40` each iteration until the exact 16-step count expires.
- Negative path seeds exact pointers `00 = 327B`, `02 = 32FB`, exact loop count `04 = 000E`, then copies exact `0x20`-byte slices backward via exact `MVP 7E,7E`, retreating both exact pointers by exact `0x40` each iteration until the exact 14-step count expires.
- After the backward exact slice loop, the negative path copies an additional exact `0x80` bytes from exact source `3300` to exact destination `2F00` through exact `MVN 7E,7E`.
- Exits `RTS`.

Strongest safe reading: exact shared sign-split block/template shuffler that either copies 16 exact forward slices between the `2Fxx` work bands or copies 14 exact reverse slices between the `32xx` bands before a final exact `3300 -> 2F00` block import.

## What remains after pass 136

- the next clean seam now starts at the exact status/selector family beginning `C2:DA00..`
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
