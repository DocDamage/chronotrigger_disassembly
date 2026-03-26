# Chrono Trigger (USA) — Labels Added / Strengthened in Pass 33

This file contains labels newly added or materially strengthened in pass 33.

Status tags:
- **[strong]** = safe to carry forward unless contradicted by later control-flow proof
- **[provisional]** = useful working label, but still open to rename/refinement
- **[alias]** = intentional alias/stub label for a table entry landing in shared code or padding-style exits

## Shared helper labels strengthened in this pass

```text
C1:AC46  ct_c1_sel_scratch_init_aecc_ad8e_ff                  [strong]
         Fills $AECC.. and $AD8E.. with #$FF across 0x0B entries.

C1:AC14  ct_c1_inline_selector_resolve_to_aecc_ad8e           [provisional]
         Consumes one inline selector control byte, resolves a selection
         path (including JSR ($B8BB,X) path), mirrors resulting list into
         $AD8E, and stores $B2AE = $AECC.

C1:AD09  ct_c1_first_selected_mask_to_ae95                    [strong]
         Builds a #$8000 >> index style mask from the first $AECC entry.

C1:AD35  ct_c1_selected_list_mask_to_ae99                     [strong]
         Iterates the $AECC list and accumulates masks for all selected entries.
```

## Group-2 labels upgraded in this pass

```text
C1:9E78  ct_c1_g2_op10_select_eligible_slots_finalize         [strong]
         Scans 8 candidate entries using AF0D/AF02/AF15 gates,
         appends accepted entries to $AECC, materializes per-slot side effects,
         applies operand-1 field-init mode, builds masks, optional CD0033,
         returns with $B3B8 = 1.

C1:9F5A  ct_c1_g2_op11_group_base_write4_pairs                [strong]
         Uses $B18B to select a base offset from FD:A80B, then writes
         four odd/even operand pairs via STA ($0E),Y. Optional CD0033.

C1:9FD2  ct_c1_g2_op12_group_base_write5_pairs_validate       [strong]
         Uses $B18B to select a base offset from FD:A80B, writes five
         odd/even operand pairs, then performs selector-driven validation/
         commit follow-up using AC14, C1DD, AD09, AD35, FDAAD2, AC89, ACCE.

C1:A396  ct_c1_g2_op16_wrapper_fused_fd_a990                  [strong]
         Thin wrapper around FD:A990 plus AC46/AD09/AD35 and optional CD0033.
```

## Bank-FD helper labels strengthened in this pass

```text
FD:A990  ct_fd_fused_group_base_write_and_slot_select_helper  [strong]
         Long helper combining the table-selected byte-write family with the
         eligible-slot scan/materialize family.

FD:A80B  ct_fd_group_base_offset_table                        [strong]
         16-bit base-offset table indexed by $B18B for the writer-family handlers.
```

## Scratch / state labels newly worth carrying forward

```text
7E:AE95  ct_c1_first_selected_mask                            [provisional]
7E:AE99  ct_c1_selected_list_mask                             [provisional]
7E:AECB  ct_c1_selected_count                                 [provisional]
7E:AECC  ct_c1_selected_list                                  [provisional]
7E:AD8D  ct_c1_saved_selected_count                           [provisional]
7E:AD8E  ct_c1_saved_selected_list                            [provisional]
7E:AE97  ct_c1_selector_result_a                              [provisional]
7E:AE98  ct_c1_selector_result_b                              [provisional]
7E:B3C7  ct_c1_group2_optional_cd0033_flag                    [provisional]
```

## Notes for next pass
- Do not over-name `$AECC` / `$AD8E` beyond “selected list” yet.
- Do not assign a gameplay-facing meaning to `$5FB0/$5FB2` from `0x10` without cross-caller proof.
- Do not rename `C1:C1DD`, `C1:AC89`, or `C1:ACCE` aggressively yet; they are clearly part of the `0x12` commit path, but their exact subsystem role still needs proof.
- Next highest-value targets are still `C1:99BE` and `C1:9A39`.
