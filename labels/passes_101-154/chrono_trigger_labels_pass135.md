# Chrono Trigger Labels — Pass 135

## Purpose

Pass 135 closes the downstream dispatch / packet-build seam that pass 134 left open at `C2:D51A..C2:D715`. The boundary correction matters here: the seam actually begins with an exact local 9-word dispatch table at `C2:D519..C2:D52A`, and the callable/dispatch targets under it resolve into one short exact setup/export wrapper, five exact status-gated owners, one shared exact overflow/service body, one exact descending helper at `D605`, and one larger exact compare/build/export owner at `D715`.

## What this pass closes

### C2:D519..C2:D52A  ct_c2_local_nine_word_dispatch_table_for_d52b_d546_d58b_d645_d690_d618_d6c3_d715_and_d778   [strong]
- Exact local 9-word dispatch table.
- Exact entries: `D52B`, `D546`, `D58B`, `D645`, `D690`, `D618`, `D6C3`, `D715`, `D778`.
- Strongest safe reading: exact local 9-word dispatch table that groups the newly-closed exact service targets `D52B / D546 / D58B / D618 / D645 / D690 / D6C3 / D715` with the still-downstream exact sibling at `D778`.

### C2:D52B..C2:D545  ct_c2_setup_export_wrapper_running_daca_8a98_then_seeding_0d9c_0da6_0da1_and_inc68_before_83b2   [strong structural]
- Runs exact helpers `DACA` and `8A98`.
- Seeds exact byte `0D9C = 0B`.
- Seeds exact byte `0DA6 = F8`.
- Seeds exact word `0DA1 = B022`.
- Increments exact byte `68`.
- Exits through exact jump `83B2`.
- Strongest safe reading: exact setup/export wrapper that runs the fixed `DACA -> 8A98` setup lane, seeds exact bytes/words `0D9C / 0DA6 / 0DA1`, increments exact byte `68`, and exits through exact jump `83B2`.

### C2:D546..C2:D58A  ct_c2_0d75_01_status_gated_selector_owner_with_optional_e017_clear_lane_negative_subtract8_tail_and_82b2_overflow   [strong structural]
- Seeds exact phase/state byte `0D75 = 01`.
- Runs exact helper `E984` and exact `BIT 0D1D`.
- Clear path masks exact bits `5A & 0C`, optionally clears exact byte `E0` and runs exact helper `E017`, compares exact bytes `81` and `54`, and only runs exact helper `EAC2` when the exact bytes differ.
- Negative path clears exact byte `E0`, forces exact byte `83 = FF`, reruns exact helper `EAC2`, subtracts exact `08` from exact selector byte `54`, then chooses exact `68 = 02 -> DC7B` when the exact result is zero or exact `68 = 03 -> DE98` otherwise.
- Overflow path exits immediately through exact jump `82B2`.
- Strongest safe reading: exact `0D75 = 01` status-gated selector owner with a clear-path optional `E017` service, a negative subtract-by-8 lane that chooses exact `68 = 02` vs `68 = 03`, and a direct exact overflow escape to `82B2`.

### C2:D58B..C2:D5D8  ct_c2_threshold_compare_owner_using_1040_04ca_0d82_fcb2_and_shared_d5d9_service_tail   [strong structural]
- Begins `JSR E984 ; BIT 0D1D`.
- Clear path exits immediately through exact jump `D7CF`.
- Negative path mirrors exact byte `1040 -> 54`, derives exact compare/clamp byte from exact bytes `04CA + 0D82`, reruns exact helper `FCB2`, compares exact result bytes `36/37/38` against exact byte `04CA`, conditionally stores back into exact byte `04CA`, runs exact helper `EAC2`, increments exact byte `04CA`, decrements exact byte `0D9A`, seeds exact byte `68 = 05`, and exits through exact jump `DF76`.
- Underflow in that exact clamp lane exits instead through exact jump `EACC`.
- Overflow path seeds exact byte `54 = 08` and enters the shared exact service body at `D5D9`.
- Strongest safe reading: exact threshold / compare owner that either jumps clear to `D7CF`, runs an exact negative clamp/compare lane around exact bytes `1040 / 04CA / 0D82` and fixed helper `FCB2`, or seeds exact selector byte `54 = 08` before entering the shared exact service body at `D5D9`.

### C2:D5D9..C2:D604  ct_c2_shared_overflow_service_body_with_primary_54_08_entry_and_secondary_d5dd_midbody_entry   [strong structural]
- Primary exact entry at `D5D9` seeds exact byte `54 = 08`.
- Secondary exact entry at `D5DD` skips that seed and uses the caller-provided exact selector byte instead.
- Common body clears exact byte `04C9`, runs exact helpers `DD7C`, `EAC2`, and `D605`, emits exact selector `C2B0` through exact helper `ED31`, emits exact selector `FBE3` through exact helper `8385`, runs exact helper `8255` with exact accumulator `10`, seeds exact byte `E0 = 02`, seeds exact byte `68 = 01`, and exits through exact jump `E012`.
- Strongest safe reading: exact shared overflow/service body with a primary exact `54 = 08` entry at `D5D9`, a caller-provided-selector entry at exact `D5DD`, and a fixed exact `DD7C -> EAC2 -> D605 -> ED31 -> 8385 -> 8255` tail before exact jump `E012`.

### C2:D605..C2:D617  ct_c2_descending_seven_step_f626_and_1811_clear_helper   [strong structural]
- Seeds exact byte `00 = 06`.
- Walks exact byte `00` downward from `06` to `00`.
- On each exact step, reruns exact helper `F626` and clears exact destination byte `[1811,Y]`.
- Exits `RTS`.
- Strongest safe reading: exact descending 7-step helper that reruns exact helper `F626` while walking exact loop byte `00` from `06` down to `00`, clearing exact destination byte `[1811,Y]` on each exact step.

### C2:D618..C2:D644  ct_c2_0d1f_ff_status_dispatcher_with_negative_8791_fdbb_dcda_eaba_prep_and_shared_dfcf_tail   [strong structural]
- Seeds exact byte `0D1F = FF`.
- Runs exact helper `E984` and exact `BIT 0D1D`.
- Clear path exits immediately through exact jump `DA01`.
- Negative path runs exact helpers `8791`, `FDBB`, and `DCDA`, then exact helper `EABA` with exact accumulator `55` before entering the shared tail.
- Overflow path skips that exact negative prep and enters the shared tail directly.
- Shared tail runs exact helper `EAC2`, clears exact byte `0D9A`, seeds exact byte `68 = 02`, and exits through exact jump `DFCF`.
- Strongest safe reading: exact `0D1F = FF` status dispatcher that jumps clear to `DA01`, uses the exact negative prep chain `8791 -> FDBB -> DCDA -> EABA(55)` before the common `EAC2 / 68 = 02 / DFCF` tail, and lets the overflow case enter that common tail directly.

### C2:D645..C2:D68F  ct_c2_sibling_threshold_compare_owner_using_1042_04c9_04ca_fce1_and_shared_d5dd_service_entry   [strong structural]
- Begins `JSR E984 ; BIT 0D1D`.
- Clear path exits immediately through exact jump `D8B2`.
- Negative path mirrors exact byte `1042 -> 54`, requires exact bytes `04C9` and `04CA` to be nonzero, reruns exact helper `FCE1`, compares exact result bytes `36/37/38` against exact byte `04CA`, conditionally stores back into exact byte `04CA`, runs exact helper `EAC2`, increments exact byte `04CA`, decrements exact byte `0D9A`, seeds exact byte `68 = 04`, and exits through exact jump `DF76`.
- Exact zero guards on `04C9` or `04CA` exit through exact jump `EACC`.
- Overflow path seeds exact byte `54 = 09` and exits through the shared secondary exact service entry `D5DD`.
- Strongest safe reading: exact sibling threshold / compare owner that jumps clear to `D8B2`, runs an exact negative compare lane around exact bytes `1042 / 04C9 / 04CA` and fixed helper `FCE1`, or seeds exact selector byte `54 = 09` before entering the shared exact service body at `D5DD`.

### C2:D690..C2:D6C2  ct_c2_0d1f_ff_sibling_dispatcher_with_negative_87d5_fd97_eaba_prep_and_shared_df31_tail   [strong structural]
- Seeds exact byte `0D1F = FF`.
- Runs exact helper `E984` and exact `BIT 0D1D`.
- Clear path exits immediately through exact jump `DA01`.
- Negative path runs exact helpers `87D5` and `FD97`, then exact helper `EABA` with exact accumulator `55` before entering the shared tail.
- Overflow path skips that exact negative prep and enters the shared tail directly.
- Shared tail clears exact byte `0D97`, runs exact helper `EAC2`, seeds exact byte `68 = 03`, clears exact byte `0D9A`, runs exact helpers `DFCF` and `DECC`, and exits through exact jump `DF31`.
- Strongest safe reading: exact `0D1F = FF` sibling dispatcher that jumps clear to `DA01`, uses the exact negative prep chain `87D5 -> FD97 -> EABA(55)` before the common `STZ 0D97 / EAC2 / 68 = 03 / DFCF / DECC / DF31` tail, and lets the overflow case enter that common tail directly.

### C2:D6C3..C2:D714  ct_c2_status_gated_compare_owner_with_e0a5_negative_lane_and_f5a7_e058_overflow_export_tail   [strong structural]
- Begins `JSR E984 ; BIT 0D1D`.
- Clear path masks exact bits `5A & 0C`; when that exact masked value is zero, compares exact bytes `81` and `54` and only reruns exact helper `EAC2` when the exact bytes differ; when the exact masked value is nonzero, it enters the overflow build/export tail instead.
- Negative path runs exact helpers `EAC2` and `E0A5`, increments exact byte `68`, and returns.
- Overflow / forced-build path runs exact helpers `EAC2`, `F5A7`, and `E058`, clears exact byte `00`, seeds exact word `02 = 001C`, increments exact byte `0D15`, mirrors exact byte `54 -> 79`, mirrors exact byte `80 -> 54`, seeds exact byte `E0 = 02`, seeds exact byte `68 = 01`, emits exact selector `C2B0` through exact helper `ED31`, and emits exact selector `FBE3` through exact helper `8385`.
- Strongest safe reading: exact status-gated compare owner that either returns after the optional `81/54` compare, takes a short exact negative `E0A5` lane that bumps exact byte `68`, or enters a larger exact overflow/forced-build export tail around exact helpers `F5A7`, `E058`, `ED31`, and `8385`.

### C2:D715..C2:D777  ct_c2_status_gated_compare_owner_with_negative_0fc6_gate_and_overflow_9990_to_9380_blockmove_tail   [strong structural]
- Begins `JSR E984 ; BIT 0D1D`.
- Clear path runs exact helpers `9F05` and `E162`, compares exact bytes `81` and `54`, reruns exact helper `EAC2` only when the exact bytes differ, and returns.
- Negative path mirrors exact byte `81 -> 54`, tests exact byte `0FC6`, exits through exact jump `EACC` when that exact byte is zero, otherwise runs exact helper `EAC2`, seeds exact byte `54 = 04`, increments exact byte `68`, and returns.
- Overflow path runs exact helper `EAC2`, clears the exact accumulator, copies exact `0x48` bytes from exact block `9990 -> 9380` through exact `MVN 7E,7E`, seeds exact word `02 = 0004`, runs exact helper `E072`, derives exact selector byte `54 = 71 + 0C`, decrements exact byte `68`, seeds exact byte `0D13 = 2F`, increments exact byte `0D0B`, runs exact helper `8255` with exact accumulator `50`, and emits exact selector `FBE3` through exact helper `8385`.
- Strongest safe reading: exact status-gated compare / block-move export owner that either returns after the clear compare lane, uses a negative exact `0FC6` gate to choose `EACC` vs `EAC2 + 54 = 04 + INC 68`, or enters a larger exact overflow lane that copies exact block `9990 -> 9380`, derives exact selector byte `54` from exact byte `71`, stamps exact byte `0D13 = 2F`, increments exact byte `0D0B`, and exits through exact selector `FBE3`.

## Alias / wrapper / caution labels

## Honest remaining gap

- the downstream exact dispatch sibling at `C2:D778..` is still open
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
- the next real code seam now moves naturally to `C2:D778..C2:D8B1`
