# Chrono Trigger Labels — Pass 133

## Purpose

Pass 133 closes the downstream callable poll / row-build seam that pass 132 left open at `C2:D19F..C2:D2C3`, and it freezes the always-used shared helpers that the seam actually depends on.

## Strong labels

### C2:D19F..C2:D265  ct_c2_three_row_template_export_owner_deriving_7600_rows_from_78_and_negative_gated_bank30_template_imports_then_d266   [strong structural]
- Begins `PHP ; REP #$30`.
- Derives exact destination row base `61 = 7600 + ((78 & FF00) >> 2)`.
- Mirrors exact selector word `7B -> 22` and seeds exact row count byte `24 = 03`.
- Across three exact rows:
  - fills exact row-start byte `[61] = FF`
  - loads exact signed selector byte `30:0580[x]`
  - when non-negative, seeds exact multiplier registers `4202/4203`, builds exact source offsets from `7B + 0200 + 4216` and `7B + 05B0 + 4216`, and copies exact `0009` bytes plus exact `0006` bytes from bank `30` into the current exact row tail
  - advances exact row base `61` by exact `10`
  - increments exact mirrored selector word `22`
- After the 3-row loop, writes exact row/export fields from exact sources `30:059C`, `30:05F3`, `30:05E0`, and `30:059E` into the current exact row.
- Checks exact high bit of exact word `30:0793[x]` and, when set, mirrors exact byte `51` into exact row bytes `[61+0004]` and `[61+0005]`.
- Runs exact helper `D266` and exits `PLP ; RTS`.
- Strongest safe reading: exact 3-row template/export owner that derives an exact `7600`-based row window from `78`, fills three exact rows with negative-gated template imports from bank `30`, then writes the exact `059C / 05F3 / 05E0 / 059E / 0793` export fields for the current selector word `7B` before tailing into exact helper `D266`.

### C2:D266..C2:D28C  ct_c2_per_slot_threshold_setup_helper_seeding_0d79_79_from_300591_bucketizing_300603_against_ffd024_then_running_d296   [strong structural]
- Begins `PHP ; SEP #$20`.
- Uses exact selector byte `7B` and exact slot byte `79`.
- Stores exact low 3 bits of exact byte `30:0591[x]` into exact slot byte `0D79[79]`.
- Loads exact comparison byte `30:0603[x]`.
- Runs an exact descending threshold search over exact table `FF:D024`, starting at exact index `1A` and decrementing until the compare becomes `>= table[x]`.
- Stores the exact winning threshold index into exact byte `020C`.
- Runs exact helper `D296` and exits `PLP ; RTS`.
- Strongest safe reading: exact per-slot threshold/setup helper that derives exact low-3-bit slot state `0D79[79]` from `30:0591[x]`, bucketizes exact byte `30:0603[x]` against exact table `FF:D024`, stores the exact winning index in `020C`, and then tail-calls exact helper `D296`.

### C2:D28D..C2:D295  ct_c2_local_020c_1a_wrapper_falling_directly_into_d296   [strong structural]
- Exact bytes decode to `PHP ; SEP #$20 ; LDA #$1A ; STA $020C ; PLP` and then direct fallthrough into exact helper `D296`.
- Strongest safe reading: exact local wrapper that only seeds exact byte `020C = 1A` before falling into the shared exact helper at `D296`.

### C2:D296..C2:D305  ct_c2_shared_block_shift_service_helper_deriving_0dc5_from_78_opening_a_01fe_byte_window_then_repeating_d306_by_d329_79   [strong structural]
- Begins `PHP ; SEP #$20`.
- Seeds exact byte `020F = FF` and exact word `020D = D03E`.
- Derives exact word `0DC5 = 7000 + ((78 & 0300) << 1)`.
- Clears the first exact word at the active exact `0DC5`-based block head.
- Performs exact overlapping same-bank move `7E -> 7E` for exact length `01FE`, effectively opening the active exact block by two bytes.
- Runs exact helper `F90C`.
- Loads exact repeat count from exact local table `D329[79]` and repeats exact helper `D306` that exact many times.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact shared block-shift / service helper that seeds exact service bytes `020D/020F`, derives the active exact `0DC5` block from the high bits of `78`, performs an exact in-place 2-byte opening shift over exact length `01FE`, runs exact helper `F90C`, then repeats exact helper `D306` according to exact local table `D329[79]`.

### C2:D306..C2:D328  ct_c2_repeated_four_strip_bit_shift_helper_walking_sixteen_columns_from_0dc5_over_0000_0010_0100_0110   [strong structural]
- Loads exact block base word `X = 0DC5`.
- Seeds exact loop count `Y = 0010`.
- Per exact iteration performs exact `LSR 0000,x ; ROR 0010,x ; LSR 0100,x ; ROR 0110,x`, then `INX`.
- Repeats for exact `0x10` iterations and exits `RTS`.
- Strongest safe reading: exact repeated four-strip bit-shift helper that walks sixteen exact columns from exact base `0DC5`, shifting and rotating the paired exact rows at offsets `0000 / 0010 / 0100 / 0110`.

### C2:D329..C2:D32B  ct_c2_local_repeat_count_table_for_d296_by_slot_79   [strong]
- Exact 3-byte local table used by `D296`.
- Exact bytes: `03 02 02`.
- Strongest safe reading: exact local repeat-count table keyed by exact slot byte `79` for the shared exact helper `D296`.

### C2:D32C..C2:D36B  ct_c2_externally_callable_0d8c_refresh_owner_running_ecdb_edf6_ee7f_from_0d79_79_and_2991_07   [strong structural]
- Has real outside callers at exact `CF21`, `D153`, and `E90F`.
- Begins `PHP ; SEP #$30`.
- Mirrors exact byte `0D79[79] -> 0D8C`.
- In 16-bit mode derives exact word `63 = 3E8C + (78 & 0300)` and seeds exact word `5F = 0418`.
- Runs exact helper `ECDB`.
- Rewrites exact word `63 = (63 & FFC0) | 0004` and exact word `5F = 0404`.
- Runs exact helpers `EDF6` and `EE7F`.
- In 8-bit mode masks exact byte `2991 & 07` and stores the exact result back into exact byte `0D8C`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact externally-callable `0D8C` refresh owner that seeds exact byte `0D8C` from exact per-slot state byte `0D79[79]`, runs the fixed exact `ECDB / EDF6 / EE7F` helper chain using exact words `63` and `5F`, then finalizes `0D8C` from exact byte `2991 & 07`.

## Alias / wrapper / caution labels

## Honest remaining gap

- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
- the next real code seam now moves naturally to `C2:D36C..C2:D520`
