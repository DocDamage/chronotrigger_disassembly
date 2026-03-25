# Chrono Trigger Labels — Pass 137

## Purpose

Pass 137 closes the exact status/selector family that pass 136 left open at `C2:DA00..C2:DACA`, with one structural correction up front: `C2:DA00` is only the terminal exact `RTS` byte of the already-frozen `D995..D9FF` helper. The real callable family begins at `C2:DA01` and resolves into one exact dispatch owner, one exact local 4-word table, four exact bounded step/clamp handlers, one exact shared decrement-prep helper, and one exact shared `FD68` accumulator tail.

## What this pass closes

### C2:DA01..C2:DA34  ct_c2_0d1e_selector_step_dispatch_owner_with_four_local_modes_and_postchange_e001_eac2_reconcile   [strong structural]
- Entry begins `PHP ; REP #30`.
- Seeds exact word `04 = 1047`, exact byte `06 = 00`, exact word `02 = 0003`, and exact byte `0D1F = FF` before dispatch.
- Exact signed byte `0D1E` is the mode selector; negative exact values return immediately through exact `PLP ; RTS`.
- Non-negative path doubles exact selector byte `0D1E`, uses it as exact `X`, mirrors exact byte `04CB -> 83`, and dispatches through exact local indirect table `JSR ($DA35,X)`.
- After the selected exact handler returns, the owner always runs exact helper `E001`.
- If exact byte `04CB` changed against staged exact byte `83`, it reruns exact helper `EAC2` before exact `PLP ; RTS`.
- Strongest safe reading: exact selector-step dispatch owner that stages exact control words from `1047`, dispatches through the exact 4-entry local table keyed by exact byte `0D1E`, always runs exact helper `E001`, and only reruns exact helper `EAC2` when the chosen exact handler changed exact byte `04CB`.

### C2:DA35..C2:DA3C  ct_c2_local_four_word_step_mode_dispatch_table_for_da01_selector_owner   [strong structural]
- Exact local word entries resolve to `DA3D`, `DA50`, `DA83`, and `DA64`.
- Exact mode order is therefore structural rather than address-order: selector `0 -> +1`, selector `1 -> -1`, selector `2 -> -10`, selector `3 -> +10`.
- Strongest safe reading: exact local 4-word step-mode dispatch table used only by the exact selector-step owner at `DA01`.

### C2:DA3D..C2:DA4F  ct_c2_bounded_plus_one_selector_step_handler_into_shared_positive_fd68_tail   [strong structural]
- Seeds exact byte `00 = 01`.
- Increments exact byte `04CB` by one and compares the exact result against exact bound byte `04CA`.
- Exact results reaching or exceeding exact byte `04CA` return immediately through the local exact `RTS`.
- Otherwise stores the incremented exact value back into exact byte `04CB` and branches into the shared exact positive accumulator tail at `DAB1`.
- Strongest safe reading: exact bounded `+1` selector-step handler that advances exact byte `04CB` by one when still below the exact upper-exclusive bound `04CA`, seeds exact step count `00 = 01`, and then enters the shared exact positive accumulator tail.

### C2:DA50..C2:DA63  ct_c2_bounded_minus_one_selector_step_handler_into_shared_negative_fd68_prep   [strong structural]
- Seeds exact byte `00 = 01`.
- Decrements exact byte `04CB` by one.
- Exact zero result returns immediately, enforcing exact floor `01`.
- Exact decremented results still greater than or equal to exact bound byte `04CA` also return immediately.
- Otherwise stores the decremented exact value back into exact byte `04CB` and branches into the shared exact signed-negate preparer at `DA9F`.
- Strongest safe reading: exact bounded `-1` selector-step handler that only accepts decremented exact values still inside the live exact `01 .. 04CA-1` range, seeds exact step count `00 = 01`, and then enters the shared exact negative accumulator prep lane.

### C2:DA64..C2:DA82  ct_c2_bounded_plus_ten_selector_step_clamp_handler_into_shared_positive_fd68_tail   [strong structural]
- Seeds exact byte `00 = 0A`.
- Adds exact decimal step `0x0A` to exact byte `04CB` and compares the exact result against exact bound byte `04CA`.
- When the exact tentative result stays below exact byte `04CA`, the handler stores it back into exact byte `04CB` and branches into the shared exact positive accumulator tail at `DAB1`.
- Otherwise clamps exact byte `04CB` to exact byte `04CA - 01`.
- On that exact clamp path, recomputes exact byte `00` as the exact remaining forward distance from the old exact value of `04CB` to the exact clamp value.
- Strongest safe reading: exact bounded `+10` selector-step/clamp handler that either advances exact byte `04CB` by ten or clamps it to exact ceiling `04CA - 01`, while updating exact byte `00` to the exact accepted forward distance before the shared exact positive accumulator tail.

### C2:DA83..C2:DA9E  ct_c2_bounded_minus_ten_selector_step_clamp_handler_into_shared_negative_fd68_prep   [strong structural]
- Seeds exact byte `00 = 0A`.
- Subtracts exact decimal step `0x0A` from exact byte `04CB` through exact `ADC #F6` in exact 8-bit mode.
- Exact zero result does not store zero; it enters the exact clamp path.
- Exact tentative results still below exact bound byte `04CA` store directly back into exact byte `04CB`.
- Otherwise the exact clamp path reloads the old exact value of `04CB`, decrements it by one into exact byte `00`, forces exact byte `04CB = 01`, and then falls into the shared exact signed-negate preparer at `DA9F`.
- Strongest safe reading: exact bounded `-10` selector-step/clamp handler that either moves exact byte `04CB` backward by ten when the exact result stays inside the live range, or clamps exact byte `04CB` to exact floor `01` while recomputing exact byte `00` as the accepted backward distance before the shared exact negative accumulator prep lane.

### C2:DA9F..C2:DAB0  ct_c2_shared_decrement_lane_signed_negate_and_sign_extend_prep_for_fd68_tail   [strong structural]
- Switches into exact 16-bit accumulator mode through `REP #20`.
- Loads exact word `04`, bit-inverts it through exact `EOR #FFFF`, increments it, and stores the exact 2's-complement result back into exact word `04`.
- Returns to exact 8-bit accumulator mode through `SEP #20`.
- When the exact negated result is nonzero, seeds exact byte `06 = FF`; otherwise exact byte `06` remains `00`.
- Falls straight into the shared exact accumulator tail at `DAB1`.
- Strongest safe reading: exact shared decrement-lane preparer that converts staged exact word `04` into its exact signed negative form and seeds exact byte `06` as the corresponding exact sign-extension byte before the common `FD68` update tail.

### C2:DAB1..C2:DACA  ct_c2_shared_fd68_accumulator_tail_adding_3e_40_delta_into_1044_1046   [strong structural]
- Begins with exact helper `FD68`.
- Reenters exact 16-bit accumulator mode through `REP #20`.
- Loads exact word `1044`, adds exact word `3E`, and stores the exact sum back into exact word `1044`.
- Returns to exact 8-bit accumulator mode through `SEP #20`.
- Loads exact byte `1046`, adds exact byte `40` with carry from the prior exact word addition, and stores the exact result back into exact byte `1046`.
- Exits `RTS`.
- Strongest safe reading: exact shared `FD68` accumulator/update tail that consumes the staged exact step parameters in direct page, then adds the resulting exact signed delta from exact `3E/40` into the live exact accumulator pair `1044/1046`.

## Alias / wrapper / caution labels

## Honest remaining gap

- the next clean seam now starts at the exact follow-on callable family beginning `C2:DACB..C2:DB30`
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
