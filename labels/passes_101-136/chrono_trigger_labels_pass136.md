# Chrono Trigger Labels — Pass 136

## Purpose

Pass 136 closes the downstream dispatch sibling seam that pass 135 left open at `C2:D778..C2:D8B1`, with one important structural correction: the seam does **not** resolve as a single owner. It breaks into one exact status-gated sibling owner, two larger exact refresh/build owners, and one exact shared sign-split block/template helper.

## What this pass closes

### C2:D778..C2:D7CE  ct_c2_status_gated_sibling_owner_with_negative_indirect_slot_refresh_lane_and_shared_e18a_cleanup_tail   [strong structural]
- Begins `JSR E984 ; BIT 0D1D`.
- Clear path runs exact helpers `9F05` and `E162`, compares exact bytes `81` and `54`, reruns exact helper `EAC2` only when the exact bytes differ, and returns.
- Negative path seeds exact byte `04CB = 01`, uses exact index byte `0D26` as `Y`, stages exact byte `[6F],Y -> 04C9`, runs exact helper `8791`, loads exact table byte `9A90,Y -> 04C9`, stores that exact byte back through `[6F],Y`, then runs exact helpers `87D5`, `EABA(B5)`, `9137`, and `A6F0(3664)`.
- Overflow path enters the same exact cleanup tail already used by the negative path.
- Shared cleanup tail runs exact helpers `EAC2`, `8820`, and `E18A`, clears exact byte `04C9`, decrements exact byte `68`, mirrors exact byte `77 -> 54`, and returns.
- Strongest safe reading: exact status-gated sibling owner that either returns after the exact `81/54` compare lane, takes a negative indirect-slot refresh lane through exact bytes `[6F],Y`, `04C9`, and table `9A90,Y`, or enters the same exact `EAC2 -> 8820 -> E18A` cleanup tail directly from overflow.

### C2:D7CF..C2:D8B1  ct_c2_refresh_build_owner_using_1041_1040_1000_1020_dd20_and_shared_d995_postexport_finalizer   [strong structural]
- Entry begins `SEP #20 ; LDA 1041 ; STA 0DD9 ; JSR 93BF`.
- Nonzero exact result from `93BF` restores exact byte `0DD9 -> 1041`, runs exact helpers `DD02` and `821E`, and rejoins the main exact positive lane.
- Main exact positive lane seeds exact byte `1040 = 54`, derives exact index byte/word `0D26 = 54 + 1041`, loads exact bytes `1020[X] -> 04CA` and `1000[X] -> 04C9`, runs exact helper `F2F3`, mirrors exact byte `0D26 -> 83`, conditionally reruns exact helper `DD7C` when exact byte `83` changed, compares exact bytes `54` and `81`, reruns exact helper `EAC2` only on mismatch, and exits through exact selector `FBE3` via exact helper `8385`.
- Retry / clamp lane uses exact bytes `104A`, `54`, and `1041` to decide whether to re-enter the main lane or fall into the larger exact export tail.
- Larger exact export tail seeds exact words `9696 = 9083` and `9698 = 0025`, seeds exact byte `0DAA = 09`, runs exact helper `EB9B`, adjusts exact byte `1041` via exact bit test `5A & 04`, mirrors exact byte `1041 -> 0D95`, mirrors exact byte `54 -> 22`, seeds exact word `61 = 335C`, runs exact helper `DD20`, emits exact selector `FBE3` through exact helper `8385`, reruns exact helper `EAC2`, then shares the exact post-export stepped loop / finalizer structure around exact bytes `0DAB / 0D22 / 0D24` and exact helper `D995`.
- Strongest safe reading: exact refresh/build owner that stages exact row bytes from `1000/1020`, refreshes the live exact index window around exact bytes `1040/1041/104A`, emits exact selector `FBE3` after exact helper `DD20`, and then optionally runs an exact stepped `0DAB/0D22/0D24` post-export loop before the shared exact `D995` block/template helper and restart.

### C2:D8B2..C2:D994  ct_c2_sibling_refresh_build_owner_using_1043_1042_5600_5700_df51_and_shared_d995_postexport_finalizer   [strong structural]
- Entry begins `SEP #20 ; LDA 1043 ; STA 0DD9 ; JSR 93BF`.
- Nonzero exact result from `93BF` restores exact byte `0DD9 -> 1043`, runs exact helpers `DF31` and `821E`, and rejoins the main exact positive lane.
- Main exact positive lane seeds exact byte `1042 = 54`, derives exact index byte/word `0D26 = 54 + 1043`, loads exact bytes `5700[X] -> 04CA` and `5600[X] -> 04C9`, runs exact helper `F2F3`, mirrors exact byte `0D26 -> 83`, conditionally reruns exact helper `DD7C` when exact byte `83` changed, compares exact bytes `54` and `81`, reruns exact helper `EAC2` only on mismatch, and exits through exact selector `FBE3` via exact helper `8385`.
- Retry / clamp lane uses exact bytes `1049`, `54`, and `1043` to decide whether to re-enter the main lane or fall into the larger exact export tail.
- Larger exact export tail mirrors the earlier owner structurally but uses exact helper `DF51` instead of `DD20`; it seeds exact words `9696 = 9083` and `9698 = 0025`, seeds exact byte `0DAA = 09`, runs exact helper `EB9B`, adjusts exact byte `1043` via exact bit test `5A & 04`, mirrors exact byte `1043 -> 0D95`, mirrors exact byte `54 -> 22`, seeds exact word `61 = 335C`, runs exact helper `DF51`, emits exact selector `FBE3` through exact helper `8385`, reruns exact helper `EAC2`, and then shares the same exact stepped post-export `D995` finalizer/restart structure.
- Strongest safe reading: exact sibling refresh/build owner that stages exact row bytes from `5600/5700`, refreshes the live exact index window around exact bytes `1042/1043/1049`, emits exact selector `FBE3` after exact helper `DF51`, and then shares the same exact stepped post-export `D995` finalizer/restart structure as `D7CF`.

### C2:D995..C2:D9FF  ct_c2_shared_sign_split_block_template_shuffler_between_2fxx_32xx_and_3300_bands   [strong structural]
- Begins by testing exact signed byte `0D21`.
- Non-negative path seeds exact pointers `00 = 2F9C`, `02 = 2F1C`, exact loop count `04 = 0010`, then copies exact `0x20`-byte slices forward via exact `MVN 7E,7E`, advancing both exact pointers by exact `0x40` each iteration until the exact 16-step count expires.
- Negative path seeds exact pointers `00 = 327B`, `02 = 32FB`, exact loop count `04 = 000E`, then copies exact `0x20`-byte slices backward via exact `MVP 7E,7E`, retreating both exact pointers by exact `0x40` each iteration until the exact 14-step count expires.
- After the backward exact slice loop, the negative path copies an additional exact `0x80` bytes from exact source `3300` to exact destination `2F00` through exact `MVN 7E,7E`.
- Exits `RTS`.
- Strongest safe reading: exact shared sign-split block/template shuffler that either copies 16 exact forward slices between the `2Fxx` work bands or copies 14 exact reverse slices between the `32xx` bands before a final exact `3300 -> 2F00` block import.

## Alias / wrapper / caution labels

## Honest remaining gap

- the next clean seam now starts at the exact status/selector family beginning `C2:DA00..`
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
