# Chrono Trigger Labels — Pass 157

## Purpose

Pass 157 closes the exact selector-packet data island at exact `C2:FBD1..C2:FCB1` and the immediately-following exact helper family through exact `C2:FE09`.

## Strong labels

### C2:FBD1..C2:FCB1  ct_c2_selector_descriptor_packet_family_for_8385_and_ed31_including_fbce_fbe3_fbea_fbff_fc06_fc14_fc1b_fc37_fc3e_fc45_fc4c_fc53_fc61   [strong structural]
- Exact span is a local exact data island, not live linear code.
- No hot exact direct-call entry is cached inside the exact span.
- Exact downstream owners already use exact packet roots inside this exact island through exact helper `8385`, including exact starts `FBCE`, `FBE3`, `FBEA`, `FBFF`, `FC06`, `FC14`, `FC1B`, `FC37`, `FC3E`, `FC45`, `FC4C`, `FC53`, and `FC61`.
- Exact packet `FC53` is also used through exact helper `ED31` in the already-frozen exact `CFFB` family.
- Strongest safe reading: exact local selector/descriptor packet family consumed by the exact packet-emission helpers rooted at exact `8385` and, for at least exact packet `FC53`, exact helper `ED31`.

### C2:FCB2..C2:FCE0  ct_c2_6e00_indexed_divisor_stager_loading_1044_1047_and_2c53_2c55_then_running_fd1d   [strong structural]
- Real exact outside caller is exact `C2:D5B1`.
- Begins `PHP ; SEP #$20`, seeds exact byte `04CB = 01`, and clears exact byte `1046`.
- Loads exact source byte `04C9`, doubles it into exact index `X`, loads exact word `6E00,X`, and mirrors that exact word into exact `1044`, exact `1047`, and exact direct-page word `04`.
- Stages exact long-source family `2C53 -> 00` and exact `2C55 -> 02`.
- Runs exact helper `FD1D`.
- Strongest safe reading: exact exact `6E00[04C9]` divisor/result-prep owner that stages exact state into exact `1044/1047/04` and exact `00/02`, then runs exact divider/helper `FD1D`.

### C2:FCE1..C2:FD1C  ct_c2_7800_halfword_plus_51_complement_divisor_stager_then_conditional_fd1d   [strong structural]
- Real exact outside caller is exact `C2:D661`.
- Begins like exact sibling `FCB2`: exact `PHP ; SEP #$20 ; 04CB = 01 ; STZ 1046`.
- Loads exact source byte `04C9`, doubles it into exact index `X`, loads exact word `7800,X`, shifts it right once, adds exact base word `51`, and mirrors that exact derived word into exact `1044`, exact `1047`, and exact direct-page word `04`.
- Stages the exact complemented source family `967F:98 - 2C53:2C55` into exact `00/02`.
- Runs exact helper `FD1D` only when the exact complemented source did not underflow.
- Strongest safe reading: exact sibling divisor/result-prep owner that derives its exact divisor/state from exact `7800[04C9]` plus exact base `51`, stages the exact complemented exact `2C53/2C55` source into exact `00/02`, and conditionally runs exact helper `FD1D`.

### C2:FD1D..C2:FD57  ct_c2_24step_restoring_divider_consuming_00_02_with_divisor_04_and_returning_result_in_36_37_38   [strong structural]
- Real exact callers are exact `C2:FCDC` and exact `C2:FD18`.
- Begins `PHP ; REP #$30`.
- Stages exact input family `00/02` into the exact work lanes rooted at exact `37/39`.
- Clears exact higher work lanes `3A/3C`.
- Seeds exact loop count `X = 0018`.
- Per exact loop step shifts exact work lanes `36/38/3A/3C`, compares exact remainder/high work against exact staged divisor `04`, conditionally subtracts exact divisor `04`, then rotates exact quotient lanes again before the exact `DEX ; BNE` loop-back.
- Strongest safe reading: exact exact 24-step restoring divider that consumes the staged exact input family `00/02` and exact divisor `04`, producing the exact caller-visible result bytes rooted at exact `36/37/38`.

### C2:FD58..C2:FD67  ct_c2_two_byte_multiply_wrapper_running_fd68_then_reentering_fd79_with_multiplicand_byte_01   [strong structural]
- Real exact outside caller is exact `C2:DBC1`.
- Begins `PHP ; JSR FD68`.
- After the exact first accumulation pass narrows to exact `SEP #$30`, loads exact byte `01`, writes that exact byte into exact hardware multiply register `4202`, seeds exact `Y = 01`, and branches directly into the shared exact inner loop at exact `FD79`.
- Strongest safe reading: exact exact two-byte multiply wrapper that runs the shared exact low-byte accumulation pass first, then reseeds the exact second multiplicand byte and rejoins the shared exact accumulation loop at exact `FD79`.

### C2:FD68..C2:FD96  ct_c2_shared_hardware_multiply_accumulator_using_4202_4203_4216_to_build_3e_40_word_band   [strong structural]
- Real exact callers are exact `C2:FD59` and exact `C2:DAB1`.
- Begins `PHP ; REP #$30`, seeds exact start index `Y = 51`, and clears exact accumulation words `3E` and `40`.
- Narrows through exact `SEP #$30`, loads exact staged byte `00`, and writes that exact byte into exact hardware multiply register `4202`.
- The shared exact inner loop reads exact byte `04,X`, writes it into exact hardware multiply register `4203`, then in exact widened mode adds exact hardware result word `4216` into exact accumulation word `003E,Y`.
- Advances exact `Y` and exact `X` by one per exact step and repeats while exact `X != 02`.
- Strongest safe reading: exact shared exact byte-by-byte hardware multiply/accumulate helper that multiplies one exact staged multiplicand byte against the exact source byte strip rooted at exact `04,X`, accumulating the exact product words into the exact work band rooted at exact `3E,Y`.

### C2:FD97..C2:FDBA  ct_c2_add_staged_1044_1046_into_2c53_2c55_then_run_fddf_clamp   [strong structural]
- Real exact outside caller is exact `C2:D6A5`.
- Adds exact staged exact low word `1044` into exact live exact word `2C53`.
- Adds exact staged exact high/overflow byte `1046` into exact live exact byte `2C55`.
- On exact carry forces exact byte `2C55 = 98`.
- Runs exact helper `FDDF`.
- Strongest safe reading: exact staged-add updater that adds exact `1044/1046` into exact `2C53/2C55`, saturates the exact high byte to `98` on carry, and reruns exact clamp/normalize helper `FDDF`.

### C2:FDBB..C2:FDDE  ct_c2_subtract_staged_1044_1046_from_2c53_2c55_then_run_fddf_clamp   [strong structural]
- Real exact outside caller is exact `C2:D62D`.
- Subtracts exact staged exact low word `1044` from exact live exact word `2C53`.
- Subtracts exact staged exact high/overflow byte `1046` from exact live exact byte `2C55`.
- On exact borrow forces exact byte `2C55 = 98`.
- Runs exact helper `FDDF`.
- Strongest safe reading: exact staged-subtract updater that subtracts exact `1044/1046` from exact `2C53/2C55`, repairs the exact high byte to `98` on borrow, and reruns exact clamp/normalize helper `FDDF`.

### C2:FDDF..C2:FE09  ct_c2_exact_98_967f_clamp_normalizer_for_2c53_2c55_returning_x_ff_on_clamp   [strong structural]
- Real exact callers are exact `C2:FDB6` and exact `C2:FDDA`.
- Begins `PHP ; SEP #$30 ; LDX #$00`.
- Compares exact high byte `2C55` against exact bound byte `98`.
- Exact values below exact `98` return immediately.
- Exact equality compares exact low word `2C53` against exact bound word `967F`.
- The exact clamp path forces exact `2C53 = 967F`, exact `2C55 = 98`, and exact `X = FF`.
- Strongest safe reading: exact exact `98:967F` clamp/normalize helper for exact `2C53/2C55`, returning exact `X = FF` on clamp and exact `X = 00` otherwise.

## Honest remaining gap

- exact `C2:FBD1..C2:FE09` is now honestly split and closed
- the exact overlap/noise immediately after exact `FE09` is still not frozen
- the next clean forward target should begin at exact `C2:FE2D`
