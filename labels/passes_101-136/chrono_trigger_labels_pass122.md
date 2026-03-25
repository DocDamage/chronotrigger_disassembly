# Chrono Trigger Labels — Pass 122

## Purpose

Pass 122 closes the exact last `BFD4` worker lane and the first real `B0AB` continuation-family loader/preset chooser left open after pass 121.

## Strong labels

### C2:C12C..C2:C163  ct_c2_0f0f_0d8c_dispatch_worker_with_optional_c164_stage_c511_call_conditional_toggle_and_0d1f_mirror   [strong structural]
- If `0F0F != 0`, calls `C164` with `X = 0D8C`, seeds exact word `0D47 = 0010`, and runs fixed helper `C511`.
- Checks `0D1D & C0`.
- When `0D1D & C0 != 0`, toggles exact latch byte `0F0F ^= 01`, writes exact word `93A4 = 3B38` when the new `0F0F == 0`, or exact word `93A4 = 3788` when the new `0F0F != 0`, then runs exact helper `EAC2`.
- Always mirrors final `0F0F` into `0D1F`.
- Strongest safe reading: exact `0F0F/0D8C` dispatch worker behind the last unresolved `BFD4` jump-table leg, with an optional `C164` stage, fixed `C511` call, conditional toggle under `0D1D & C0`, exact `93A4` word selection, and final `0D1F` mirror.

### C2:C164..C2:C183  ct_c2_shared_low3bit_cyclic_adjust_helper_for_x_targeted_state_keyed_by_5a_low2bits   [strong]
- Reads the exact byte at `X`.
- If `5A.low2 != 0`, uses exact `5A.bit0` to choose direction, applies exact `-1` when clear or exact `+1` when set, masks the result to `& 07`, stores it back through `X`, then runs exact helpers `C456` and `EAC2` and returns.
- If `5A.low2 == 0`, falls through into the downstream template-stage path at `C184` instead of returning locally.
- Strongest safe reading: exact shared low-3-bit cyclic adjust helper for the `0D8B/0D8C/0D90` worker family, keyed by `5A.low2`.

### C2:C184..C2:C206  ct_c2_template_stage_and_mask_select_finalizer_reached_from_the_zero_control_c164_path   [strong structural]
- If `F0.bit0 != 0`, runs `EAC2`, copies exact `0x09` bytes from ROM template `C2:FCA9` into `0408`, copies the same exact `0x09` bytes from that ROM template into `0F00`, and runs fixed helper `C54F`.
- Otherwise, if `5A & 0C != 0`, runs `EAC2`, copies exact `0x09` bytes from `0F00` into `0408`, and runs fixed helper `C54F`.
- Then always enters the exact local mask-selection stage using `Y = 54 - 0F`.
- Scans exact local table `C207` against `0F00,Y` until mismatch or exact sentinel `FF`.
- If mismatch occurs and `0D1E < 2`, uses a bounded local fallback chooser before loading the final mask byte.
- Stores the chosen mask byte into direct page `00`, runs exact helper `C20F`, reruns `EAC2`, and exits through exact selector `FBE3` via `8385`.
- Strongest safe reading: exact template-stage / mask-select finalizer reached from the zero-control `C164` path.

### C2:C207..C2:C20E  ct_c2_eight_byte_local_mask_priority_table_80_08_40_04_10_20_02_ff_for_c184_finalizer   [strong]
- Exact bytes: `80 08 40 04 10 20 02 FF`.
- Consumed directly by `C184..C206`.
- Scanned linearly until mismatch or exact sentinel `FF`.
- Strongest safe reading: exact eight-byte local mask-priority table for the `C184` finalizer.

### C2:B0AB..C2:B106  ct_c2_cc_record_preset_loader_and_shift_walk_dispatch_selector_above_the_post_b04b_builder_lane   [strong structural]
- Reads exact selector `04C9` and fans through exact helpers `8881` and `88D8`.
- Uses exact long-table roots `CC:1BB5,X`, `CC:0001,X`, `CC:0002,X`, and `CC:0000,X`.
- Builds exact control byte `0DBD` as `((CC:1BB5,X & 03) << 2) | CC:0001,X`.
- Builds exact companion control byte `0DC0` as `CC:0002,X & 0F`, with exact remap `0F -> 40`.
- Passes exact source byte `CC:0000,X` into local helper `B0FA`.
- `B0FA` shift-walks that byte left until carry sets, advancing `X` by exact two-byte steps starting from exact seed `51`.
- Resulting `X` is used as the local indirect-dispatch selector for `JSR ($B0EE,X)`.
- Strongest safe reading: exact `CC`-record preset loader and shift-walk dispatch selector above the post-`B04B` builder lane.

### C2:B10D..C2:B17E  ct_c2_multiplier_threshold_bucket_chooser_writing_exact_presets_into_0dbd_0dc0_and_0dbf   [strong structural]
- Writes exact constant `64` into hardware multiplier input `4202`.
- Multiplies it by exact table byte `C0:FE00[0D00]` and reads the exact result byte from `4217`.
- Buckets that result against the exact local thresholds `05`, `14`, `32`, and `64`.
- Dispatches through the exact four-entry local jump table at `B141`.
- Exact preset outcomes now frozen:
- case 0 -> `0DBD = C2`, `0DC0 = 40`
- case 1 -> `0DBD = 82`, `0DC0 = 40`
- case 2 -> `0DBD = 41`, `0DC0 = 03`, `0DBF = 8A`
- case 3 -> `0DBD = 80`, `0DC0 = 01`, `0DBF = B2`
- Strongest safe reading: exact multiplier/threshold bucket chooser reused inside the post-`B04B` continuation family.

## Alias / wrapper / caution labels

### 7E:0F0F  ct_c2_toggle_latch_byte_for_the_c12c_worker_and_c184_template_stage_family   [caution strengthened]
- `C12C..C163` tests it, conditionally toggles it under `0D1D & C0`, and mirrors the final value into `0D1F`.
- `C184..C206` compares local mask-table bytes against `0F00[54 - 0F]` after exact `0F00` template staging.
- Strongest safe reading: exact toggle latch byte for the `C12C` worker / `C184` template-stage family.

### 7E:0D1F  ct_c2_mirror_latch_byte_of_0f0f_written_by_the_c12c_worker   [caution]
- `C12C..C163` always writes final `0F0F` into `0D1F` just before return.
- Strongest safe reading: exact mirror latch byte of `0F0F` written by the `C12C` worker.

### 7E:0D47  ct_c2_exact_0010_stage_word_seeded_before_the_fixed_c511_call_in_c12c   [caution]
- `C12C..C163` seeds exact word `0D47 = 0010` immediately before calling `C511` when `0F0F != 0`.
- Strongest safe reading: exact stage/countdown word seeded before the fixed `C511` call in `C12C`.

### 7E:0DBD  ct_c2_settlement_export_mode_control_byte_assembled_from_cc_records_and_threshold_presets   [caution strengthened]
- `B0AB..B106` assembles it from `((CC:1BB5,X & 03) << 2) | CC:0001,X`.
- `B10D..B17E` can overwrite it with exact presets `C2`, `82`, `41`, or `80`.
- Earlier pass-118 evidence shows `8E2D..8E81` consuming `0DBD.bit7`, `0DBD.bit6`, and `0DBD.bit3` to select export/clamp behavior.
- Strongest safe reading: exact settlement/export mode control byte assembled from `CC` records and threshold presets.

### 7E:0DC0  ct_c2_companion_mode_control_byte_for_the_b0ab_b10d_preset_family   [caution]
- `B0AB..B106` seeds it from `CC:0002,X & 0F` with exact remap `0F -> 40`.
- `B10D..B17E` overwrites it with exact presets `40`, `40`, `03`, or `01`.
- Strongest safe reading: exact companion mode/control byte for the `B0AB/B10D` preset family.

### 7E:0DBF  ct_c2_optional_high_bucket_preset_tail_byte_for_the_b10d_preset_family   [caution]
- Only the upper exact `B10D` buckets write it: case 2 -> `8A`, case 3 -> `B2`.
- Strongest safe reading: exact optional high-bucket preset tail byte for the `B10D` preset family.

## Honest remaining gap

This pass closes the main seams from pass 121, but these honest holes remain:

- `C2:B17F..B24A` is now the real continuation lane of the `B0AB` handler family
- `C2:C20F..` still deserves its own exact helper ownership instead of only being carried as the called finalizer under `C184`
- broader gameplay-facing nouns are still open for:
- `0D8B/0D8C/0D90`
- `0F0F/0D1F`
- `0DBD/0DC0/0DBF`
- the overall `A886..AA30` stream/template/update family
