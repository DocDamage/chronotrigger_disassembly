# Chrono Trigger Labels — Pass 72

## Purpose
This file records the label upgrades justified by pass 72.

Pass 72 re-opened the promoted late selector-control master band:

- global `90..A9`
- selector-control locals `39..52`

The most important correction is that globals `9D..A9` are not clean standalone top-level bodies.
They are **internal alias entries** into the late-pack executor blob.

---

## Strong global labels

### C1:8876..C1:88C4  ct_global_opcode_90_update_lane_afb6_b045_and_release_5E4B_bit7_on_expiry   [strong structural]
- Uses `B179[0]` or fallback `AEC7`, then maps through `B163` to a lane ID.
- Sets `AFB6[lane] = 1` and copies `B0D4[lane] -> AF27[lane]`.
- Decrements `B045[lane]` and reloads it to `0x0A` on expiry.
- Clears `5E4B + lane*0x80` bit `0x80` and clears `AFB6[lane]` when the countdown expires.

### C1:88C5..C1:8974  ct_global_opcode_91_conditionally_seed_afc1_af32_and_ad9c_from_lane_geometry   [strong structural]
- Uses `B179[1]` or fallback `AEC7`, then maps through `B163` to a lane ID.
- Requires `5E4A.bit7` set and `5E4B.bit6` clear for the helper path.
- Sets `AFC1[lane] = 1`, computes `AF32[lane] = B0DF[lane] + 5E64[lane_block]`.
- Seeds `AD9C/AD9E` and runs the `EBF8` helper chain.
- Clears `B186` with `AND #$17FF` before return.

### C1:8975..C1:89B8  ct_global_opcode_92_update_lane_afcc_b05b_and_clear_afcc_on_expiry   [strong structural]
- Uses `B17B` or fallback `AEC7`, then maps through `B163` to a lane ID.
- Sets `AFCC[lane] = 1` and copies `B0EA[lane] -> AF3D[lane]`.
- Decrements `B05B[lane]` and reloads it to `0x0A` on expiry.
- Clears `AFCC[lane]` when the countdown expires.

### C1:89B9..C1:8A04  ct_global_opcode_93_update_lane_afd7_b066_and_release_5E4D_bit7_on_expiry   [strong structural]
- Uses `B17C` or fallback `AEC7`, then maps through `B163` to a lane ID.
- Sets `AFD7[lane] = 1` and copies `B0F5[lane] -> AF48[lane]`.
- Decrements `B066[lane]` and reloads it to `0x0A` on expiry.
- Clears `5E4D + lane*0x80` bit `0x80` and clears `AFD7[lane]` on expiry.

### C1:8A05..C1:8A50  ct_global_opcode_94_update_lane_afe2_b071_and_release_5E4D_bit6_on_expiry   [strong structural]
- Uses `B17D` or fallback `AEC7`, then maps through `B163` to a lane ID.
- Sets `AFE2[lane] = 1` and copies `B100[lane] -> AF53[lane]`.
- Decrements `B071[lane]` and reloads it to `0x0A` on expiry.
- Clears `5E4D + lane*0x80` bit `0x40` and clears `AFE2[lane]` on expiry.

### C1:8A51..C1:8A9C  ct_global_opcode_95_update_lane_afed_b07c_and_release_5E4E_bit6_on_expiry   [strong structural]
- Uses `B17E` or fallback `AEC7`, then maps through `B163` to a lane ID.
- Sets `AFED[lane] = 1` and copies `B10B[lane] -> AF5E[lane]`.
- Decrements `B07C[lane]` and reloads it to `0x0A` on expiry.
- Clears `5E4E + lane*0x80` bit `0x40` and clears `AFED[lane]` on expiry.

### C1:8A9D  ct_global_opcode_96_rts_alias   [strong]
- Exact `RTS` entry.

### C1:8A9E  ct_global_opcode_97_rts_alias   [strong]
- Exact `RTS` entry.

### C1:8A9F..C1:8B0F  ct_global_opcode_98_capture_lane_b12c_variant_into_af7f_and_optionally_run_ec7f   [strong structural]
- Uses `B179[8]` or fallback `AEC7`, then maps through `B163` to a lane ID.
- Sets `B00E[lane] = 1` and copies `B12C[lane] -> AF7F[lane]`.
- Applies status-based halve/double transforms from lane-block flags.
- Clears `B186` with `AND #$1FEF`.
- Optionally runs the `EBF8 -> EC7F` helper chain when `5E4B.bit4` is set.

### C1:8B10..C1:8BB8  ct_global_opcode_99_update_lane_b019_b0a8_and_on_expiry_conditionally_seed_ad9c   [strong structural]
- Uses `B179[9]` or fallback `AEC7`, then maps through `B163` to a lane ID.
- Sets `B019[lane] = 1` and copies `B137[lane] -> AF8A[lane]`.
- Applies status-based halve/double transforms from lane-block flags.
- Decrements `B0A8[lane]`.
- On expiry, conditionally seeds `AD9C/AD9E` through the helper chain when the lane-block gates allow it.

### C1:8BB9..C1:8C07  ct_global_opcode_9A_update_lane_b024_b0b3_and_release_5E4E_bit2_on_expiry   [strong structural]
- Uses `B179[0x0A]` or fallback `AEC7`, then maps through `B163` to a lane ID.
- Sets `B024[lane] = 1` and copies `B142[lane] -> AF95[lane]`.
- Decrements `B0B3[lane]` and reloads it to `0x0A` on expiry.
- Clears `5E4E + lane*0x80` bit `0x04` and clears `B024[lane]` on expiry.

### C1:8C08  ct_global_opcode_9B_rts_alias   [strong]
- Exact `RTS` entry.

---

## Provisional global label

### C1:8461..C1:8625  ct_global_opcode_9C_service7_lane_controller_and_active_time_update   [provisional structural]
- Large lane/service controller, not a tiny wrapper.
- Clears controller scratch, iterates lane-related state through the `B179/B163` mapping, checks occupancy/readiness bytes and lane-block state, and calls already-known service/readiness helpers like `BD6F`, `B575`, and `B725`.
- Writes readiness/active-time style state such as `B03A`.
- Final gameplay-facing noun intentionally left open until the helper chain around `8CF9 / B923 / BCE1 / B223` is decoded more tightly.

---

## Strong internal-alias global labels

### C1:AFB6..C1:AFC0  ct_global_opcode_9D_late_pack_helper_internal_alias_seed_dp28_from_fd_ba61   [strong structural]
- Internal helper/lead-in alias before the late-pack executor blob.
- Seeds scratch through `FD:BA61`, `DP28/29`, `C92A`, and a `PLX` return tail.
- Not a clean standalone top-level command body.

### C1:AFC1..C1:AFCB  ct_global_opcode_9E_late_pack_helper_internal_alias_call_c92a_and_plx_return   [strong structural]
- Internal alias into the same helper tail used by `9D`.
- Falls through to `PLX ; STX $2C ; RTS`.
- Not a clean standalone top-level command body.

### C1:AFCC..C1:AFD4  ct_global_opcode_9F_late_pack_helper_internal_alias_plx_return   [strong structural]
- Internal alias that lands directly in the `PLX` return tail ahead of the late-pack blob.
- Not a clean standalone top-level command body.

### C1:AFD7..C1:AFE1  ct_global_opcode_A0_late_pack_executor_internal_alias_after_cc_record_load   [strong correction]
- The master pointer lands two bytes inside the real `CC:8B08` pointer-load sequence.
- Keep as an internal late-pack executor alias, not as the clean top-level initializer.

### C1:AFE2..C1:AFEC  ct_global_opcode_A1_late_pack_executor_internal_alias_clear_af24_and_probe_second_subop   [strong structural]
- Internal alias in the common late-pack executor path.
- Clears `AF24`, probes byte `+4` for the `FE` chained-subop case, and falls into the shared segment selector path.

### C1:AFED..C1:AFF7  ct_global_opcode_A2_late_pack_executor_internal_alias_arm_second_subop_flag   [strong structural]
- Internal alias in the same common path.
- Lives inside the `CMP #$FE` / `B1CF` second-subop arming logic.

### C1:AFF8..C1:B002  ct_global_opcode_A3_late_pack_executor_internal_alias_after_segment_select   [strong structural]
- Internal alias after `B4AA` segment selection.
- Fetches the current opcode byte into `B239` and falls into the shared dispatch path.

### C1:B003..C1:B00D  ct_global_opcode_A4_late_pack_executor_internal_alias_dispatch_current_b239_opcode   [strong structural]
- Internal alias that dispatches the current `B239` opcode through the master table.

### C1:B00E..C1:B018  ct_global_opcode_A5_late_pack_executor_internal_alias_advance_to_second_subop   [strong structural]
- Internal alias for the chained second-subop advance path.
- Advances `B1D2` by `+4`, reloads `B239`, and falls back into the shared dispatch.

### C1:B019..C1:B023  ct_global_opcode_A6_late_pack_executor_internal_alias_dispatch_second_subop   [strong structural]
- Internal alias after the chained second-subop reload.
- Dispatches the second `B239` opcode and falls into result capture.

### C1:B024..C1:B02E  ct_global_opcode_A7_late_pack_executor_internal_alias_capture_af24_result   [strong structural]
- Internal alias at the result-capture start.
- Mirrors `AF24` into `B24A[tail]` and enters the special-case / nonzero-result logic.

### C1:B02F..C1:B039  ct_global_opcode_A8_late_pack_executor_internal_alias_special_case_af24_eq_02   [strong structural]
- Internal alias inside the result-capture tail.
- Special-cases `AF24 == 2` before the broader nonzero-result path.

### C1:B03A..C1:B08E  ct_global_opcode_A9_late_pack_executor_internal_alias_nonzero_af24_path   [strong structural]
- Internal alias into the nonzero-result handling and FE/FF continuation logic.
- Includes the path that marks `B242`, advances FE-delimited segments, and increments or clears `B263`.

---

## Strong promoted selector-control locals

### selector `39`  ct_update_lane_afb6_b045_and_release_5E4B_bit7_on_expiry   [strong structural]
- Local selector-control ownership of global `90`.

### selector `3A`  ct_conditionally_seed_afc1_af32_and_ad9c_from_lane_geometry   [strong structural]
- Local selector-control ownership of global `91`.

### selector `3B`  ct_update_lane_afcc_b05b_and_clear_afcc_on_expiry   [strong structural]
- Local selector-control ownership of global `92`.

### selector `3C`  ct_update_lane_afd7_b066_and_release_5E4D_bit7_on_expiry   [strong structural]
- Local selector-control ownership of global `93`.

### selector `3D`  ct_update_lane_afe2_b071_and_release_5E4D_bit6_on_expiry   [strong structural]
- Local selector-control ownership of global `94`.

### selector `3E`  ct_update_lane_afed_b07c_and_release_5E4E_bit6_on_expiry   [strong structural]
- Local selector-control ownership of global `95`.

### selector `3F`  ct_rts_alias   [strong]
- Local selector-control ownership of global `96`.

### selector `40`  ct_rts_alias_2   [strong]
- Local selector-control ownership of global `97`.

### selector `41`  ct_capture_lane_b12c_variant_into_af7f_and_optionally_run_ec7f   [strong structural]
- Local selector-control ownership of global `98`.

### selector `42`  ct_update_lane_b019_b0a8_and_on_expiry_conditionally_seed_ad9c   [strong structural]
- Local selector-control ownership of global `99`.

### selector `43`  ct_update_lane_b024_b0b3_and_release_5E4E_bit2_on_expiry   [strong structural]
- Local selector-control ownership of global `9A`.

### selector `44`  ct_rts_alias_3   [strong]
- Local selector-control ownership of global `9B`.

### selector `46`  ct_late_pack_helper_internal_alias_seed_dp28_from_fd_ba61   [strong structural]
- Local selector-control ownership of global `9D`.

### selector `47`  ct_late_pack_helper_internal_alias_call_c92a_and_plx_return   [strong structural]
- Local selector-control ownership of global `9E`.

### selector `48`  ct_late_pack_helper_internal_alias_plx_return   [strong structural]
- Local selector-control ownership of global `9F`.

### selector `49`  ct_late_pack_executor_internal_alias_after_cc_record_load   [strong correction]
- Local selector-control ownership of global `A0`.
- Carries the same explicit correction that this is not the clean top-level initializer.

### selector `4A`  ct_late_pack_executor_internal_alias_clear_af24_and_probe_second_subop   [strong structural]
- Local selector-control ownership of global `A1`.

### selector `4B`  ct_late_pack_executor_internal_alias_arm_second_subop_flag   [strong structural]
- Local selector-control ownership of global `A2`.

### selector `4C`  ct_late_pack_executor_internal_alias_after_segment_select   [strong structural]
- Local selector-control ownership of global `A3`.

### selector `4D`  ct_late_pack_executor_internal_alias_dispatch_current_b239_opcode   [strong structural]
- Local selector-control ownership of global `A4`.

### selector `4E`  ct_late_pack_executor_internal_alias_advance_to_second_subop   [strong structural]
- Local selector-control ownership of global `A5`.

### selector `4F`  ct_late_pack_executor_internal_alias_dispatch_second_subop   [strong structural]
- Local selector-control ownership of global `A6`.

### selector `50`  ct_late_pack_executor_internal_alias_capture_af24_result   [strong structural]
- Local selector-control ownership of global `A7`.

### selector `51`  ct_late_pack_executor_internal_alias_special_case_af24_eq_02   [strong structural]
- Local selector-control ownership of global `A8`.

### selector `52`  ct_late_pack_executor_internal_alias_nonzero_af24_path   [strong structural]
- Local selector-control ownership of global `A9`.

---

## Provisional promoted selector-control local

### selector `45`  ct_service7_lane_controller_and_active_time_update   [provisional structural]
- Local selector-control ownership of global `9C`.
- Large lane/service controller; final gameplay-facing noun still left open.

---

## Honest caution
Three things should stay explicit after this pass:

- global `9C` / selector `45` is still open even though it is clearly a real controller
- the `91 / 98 / 99` helper chain still lacks a final gameplay-facing noun
- globals `9D..A9` are **internal aliases**, so they should not be treated like ordinary standalone opcode bodies in future passes
