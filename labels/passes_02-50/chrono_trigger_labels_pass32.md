# Chrono Trigger (USA) — Labels Added / Strengthened in Pass 32

This file contains the labels newly added or materially strengthened in pass 32.

Status tags:
- **[strong]** = safe to carry forward unless contradicted by later control-flow proof
- **[provisional]** = useful working label, but still open to rename/refinement
- **[alias]** = intentional alias/stub label for a table entry landing in shared code or padding-style exits

## New / strengthened command-table labels

```text
FD:BA4A  ct_c1_cmd_00_16_advance_ctrl_table              [provisional]
         First 23 bytes used by group-1 random stream-control path.
         Best current reading: command advance / stream-skip control table,
         not yet a fully solved universal operand-size table.

C1:B85F  ct_c1_group1_cmd_table                          [strong]
C1:B88D  ct_c1_group2_cmd_table                          [strong]
C1:8CE7  ct_c1_group1_dispatch_site                      [strong]
C1:8D88  ct_c1_group2_dispatch_site                      [strong]
```

## Dispatcher-state / interpreter-control labels

```text
7E:AF24  ct_c1_cmd_short_circuit_flag                    [provisional]
         Nonzero causes early handler/dispatch exit behavior.

7E:B3B8  ct_c1_group2_continuation_selector              [provisional]
         0 = fuller continuation path
         1 = alternate continuation path with extra helper stage
         2 = skip directly to common tail
```

## Group 1 labels

```text
C1:9810  ct_c1_g1_op00_body                              [provisional]
C1:983A  ct_c1_g1_op01_op02_shared_body                  [provisional]

C1:98C4  ct_c1_g1_op03_rts_stub                          [alias]
C1:98C5  ct_c1_g1_op04_random_4way_stream_advance        [strong]

C1:9960  ct_c1_g1_op05_rts_stub                          [alias]
C1:9961  ct_c1_g1_op06_rts_stub                          [alias]
C1:9962  ct_c1_g1_op07_clear_short_circuit_and_rts       [alias]
C1:9966  ct_c1_g1_op08_rts_stub                          [alias]
C1:9967  ct_c1_g1_op09_body                              [provisional]
C1:9978  ct_c1_g1_op0A_rts_stub                          [alias]
C1:9979  ct_c1_g1_op0B_clear_short_circuit_and_rts       [alias]
C1:997D  ct_c1_g1_op0C_rts_stub                          [alias]
C1:997E  ct_c1_g1_op0D_rts_stub                          [alias]
C1:997F  ct_c1_g1_op0E_rts_stub                          [alias]
C1:9980  ct_c1_g1_op0F_rts_stub                          [alias]
C1:9981  ct_c1_g1_op10_op16_shared_body                  [provisional]
C1:99B4  ct_c1_g1_op11_to_op15_clear_short_circuit_rts   [alias]
```

## Group 2 labels

```text
C1:99B8  ct_c1_g2_op00_set_continuation_2                [strong]
C1:99BE  ct_c1_g2_op01_body                              [provisional]
C1:9A39  ct_c1_g2_op02_body                              [provisional]
C1:9B46  ct_c1_g2_op03_rts_stub                          [alias]
C1:9B47  ct_c1_g2_op04_varctrl_shared_entry_a            [provisional]
C1:9B48  ct_c1_g2_op05_varctrl_shared_entry_b            [provisional]
C1:9B8C  ct_c1_g2_op06_body                              [provisional]
C1:9B8D  ct_c1_g2_op07_body                              [provisional]
C1:9C6E  ct_c1_g2_op08_body                              [provisional]
C1:9C6F  ct_c1_g2_op09_body                              [provisional]
C1:9CB3  ct_c1_g2_op0A_body                              [provisional]
C1:9D1B  ct_c1_g2_op0B_body                              [provisional]
C1:9D72  ct_c1_g2_op0C_body                              [provisional]
C1:9DCE  ct_c1_g2_op0D_bitmask_state_control             [strong]
C1:9E62  ct_c1_g2_op0E_rts_stub                          [alias]
C1:9E63  ct_c1_g2_op0F_optional_cd0033_then_cont2        [strong]
C1:9E78  ct_c1_g2_op10_body                              [provisional]
C1:9F5A  ct_c1_g2_op11_body                              [provisional]
C1:9FD2  ct_c1_g2_op12_body                              [provisional]
C1:A14E  ct_c1_g2_op13_sat_signed_delta_to_b158          [strong]
C1:A188  ct_c1_g2_op14_multi_target_sat_adjust           [provisional]
C1:A20B  ct_c1_g2_op15_multi_target_sat_adjust           [provisional]
C1:A396  ct_c1_g2_op16_body                              [provisional]
```

## Helper label strengthened in this pass

```text
C1:A3D1  ct_c1_sat_signed_byte_adjust_indirect_y         [strong]
         Adjusts byte at (0E),Y using signed delta in $10 with floor/clamp behavior.
```

## Notes for next pass
- Do not collapse `FD:BA4A` into a hard operand-size table yet.
- Do not assign battle-only or map-only ownership to `9E78/9F5A/9FD2/A396` without caller proof.
- Keep the `CD0033` callsite labels generic until the service role is proven from both caller and callee sides.
- Preserve alias labels; they matter because they keep table density honest.
