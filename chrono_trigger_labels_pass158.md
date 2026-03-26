# Chrono Trigger Labels — Pass 158

## Purpose

Pass 158 closes the repeated exact clamp/update family after exact `C2:FE09`, including the exact overlap/tail islands between those repeated helper clones.

## Strong labels

### C2:FE2D..C2:FE57  ct_c2_duplicate_98_967f_clamp_normalizer_for_2c53_2c55_called_from_fe28   [strong structural]
- Real exact caller is exact `C2:FE28`.
- Exact body matches the earlier exact clamp helper family rooted at exact `FDDF`.
- Begins `PHP ; SEP #$30 ; LDX #$00`.
- Compares exact high byte `2C55` against exact `98`, compares exact low word `2C53` against exact `967F` on equality, and on clamp forces exact `2C53 = 967F`, exact `2C55 = 98`, and exact `X = FF`.
- Strongest safe reading: exact direct-call clone of the exact exact `98:967F` clamp/normalize helper for exact `2C53/2C55`.

### C2:FE9A..C2:FEBD  ct_c2_duplicate_subtract_staged_1044_1046_from_2c53_2c55_then_run_febe_clamp   [strong structural]
- Exact body is the same structural subtract/update shape as already-frozen exact helper `FDBB`.
- Begins `PHP ; REP #$20`, subtracts exact staged exact low word `1044` from exact live exact low word `2C53`, then in exact 8-bit mode subtracts exact staged exact high byte `1046` from exact live exact high byte `2C55`.
- On exact borrow forces exact byte `2C55 = 98`.
- Runs exact helper `FEBE` and exits through exact `PLP ; RTS`.
- Strongest safe reading: exact duplicate staged-subtract updater that subtracts exact `1044/1046` from exact `2C53/2C55`, repairs/saturates exact high byte `2C55` to exact `98` on borrow, and reruns downstream exact clamp helper `FEBE`.

### C2:FEBE..C2:FEE8  ct_c2_duplicate_98_967f_clamp_normalizer_for_2c53_2c55_called_from_fe95_and_feb9   [strong structural]
- Real exact callers are exact `C2:FE95` and exact `C2:FEB9`.
- Exact body again matches the earlier exact clamp helper family rooted at exact `FDDF`.
- Begins `PHP ; SEP #$30 ; LDX #$00`.
- Checks exact `2C55` against exact `98`, checks exact `2C53` against exact `967F` on equality, and on clamp forces exact `2C53 = 967F`, exact `2C55 = 98`, and exact `X = FF`.
- Strongest safe reading: exact direct-call clone of the exact exact `98:967F` clamp/normalize helper for exact `2C53/2C55`.

## Alias / wrapper / caution labels

### C2:FEA2..C2:FEBD  ct_c2_fea2_alias_entry_into_shared_subtract_normalize_tail_reached_from_c5b5   [alias late entry]
- Real exact caller is exact `C2:C5B5`.
- Lands inside exact owner `FE9A` after the exact front `PHP ; REP #$20 ; LDA 2C53` setup.
- Begins `SEC ; SBC $1044 ; STA $2C53`, then performs the exact high-byte subtract/repair lane, exact `JSR FEBE`, and exact `PLP ; RTS`.
- Strongest safe reading: exact overlapping late/local entry into the shared exact subtract/normalize tail of exact owner `FE9A`.

### C2:FE0A..C2:FE2C  ct_c2_overlap_tail_island_ending_in_local_subtract_normalize_then_fe2d_clamp   [caution structural]
- No exact direct call xref currently lands on exact `FE0A`.
- The exact front bytes do **not** decode as one exact balanced standalone owner.
- The readable exact back half stores exact low-word state into exact `2C53`, subtracts exact staged exact high byte `1046` from exact `2C55`, repairs/saturates exact `2C55` to exact `98`, then runs exact helper `FE2D` before exact `PLP ; RTS`.
- Strongest safe reading: exact overlap/tail island feeding downstream exact clamp helper `FE2D`, not one exact independent owner rooted at exact `FE0A`.

### C2:FE58..C2:FE5C  ct_c2_overlap_noise_tail_between_fe2d_and_fe5d_clamp_clones   [caution structural]
- Exact bytes: `B2 82 FE 28 60`.
- No exact direct call xref currently lands here.
- The exact byte sequence does **not** decode as one exact balanced standalone owner at exact `FE58`.
- Strongest safe reading: exact overlap/noise tail between exact clamp-helper bodies `FE2D` and `FE5D`.

### C2:FE5D..C2:FE87  ct_c2_second_local_duplicate_98_967f_clamp_normalizer_for_2c53_2c55   [caution structural]
- Exact body is byte-for-byte the same clamp/normalize shape as exact `FE2D` and exact `FEBE`.
- Begins `PHP ; SEP #$30 ; LDX #$00`, checks exact `2C55` against exact `98`, checks exact `2C53` against exact `967F`, and on clamp forces exact `2C53 = 967F`, exact `2C55 = 98`, and exact `X = FF`.
- No exact hot direct caller is currently cached for exact `FE5D`.
- Strongest safe reading: exact second local duplicate of the exact exact `98:967F` clamp/normalize helper body for exact `2C53/2C55`.

### C2:FE88..C2:FE99  ct_c2_overlap_tail_storing_2c55_then_normalizing_through_febe   [caution structural]
- No exact direct call xref currently lands on exact `FE88`.
- The exact front bytes do **not** decode as one exact balanced standalone owner.
- The readable exact tail writes one exact candidate high byte into exact `2C55`, repairs/saturates exact `2C55` to exact `98`, then runs exact helper `FEBE` before exact `PLP ; RTS`.
- Strongest safe reading: exact overlap/tail normalizer island feeding downstream exact clamp helper `FEBE`, not one exact independent owner rooted at exact `FE88`.

### C2:FEE9..C2:FEF9  ct_c2_overlap_tail_emitting_two_8385_packets_then_jumping_e77b   [caution structural]
- No exact direct call xref is currently cached for exact `FEE9`.
- The exact front bytes do **not** form one exact clean standalone owner.
- The readable exact back half performs two exact local exact `JSR 8385` submissions and then exact-jumps to exact `E77B`.
- Strongest safe reading: exact overlap/tail island ending in two exact `8385` submissions and exact jump `E77B`, not one exact independent owner rooted at exact `FEE9`.

## Honest remaining gap

- exact `C2:FE0A..C2:FEF9` is now honestly split and closed into repeated exact helper clones plus exact overlap/tail islands
- the next clean forward callable owner begins at exact `C2:FEFA`
- exact `C2:FEFA..` should be taken next instead of reopening the repeated exact tail islands
