# Chrono Trigger (USA) — Labels Added / Strengthened in Pass 35

This file contains labels newly added or materially strengthened in pass 35.

Status tags:
- **[strong]** = safe to carry forward unless contradicted by later control-flow proof
- **[provisional]** = useful working label, but still open to rename/refinement
- **[alias]** = intentional alias/stub label for a table entry landing in shared code or wrapper logic

## Long-helper and follow-up packet labels

```text
FD:AB01  ct_fd_op01_resolve_followup_packet_from_b18c         [strong]
         Real linear long helper uniquely used by group-2 opcode 0x01.
         Uses B18C plus hardcoded secondary arg 0x0B through C1:FDBF,
         stores result index in B2C3, then materializes:
           B18E = CC:88CB[result]
           B18F = B18C
           B190 = CC:88CC[result]
           B191 = 0

C1:AC89  ct_c1_merge_opcode_mode_into_b18e_b18f_packet        [strong]
         Opcode-sensitive follow-up packet merger/finalizer.
         ORs (A+3) into B18E, always clears B191, then uses AEE3 to
         specialize the packet:
           op0 -> clear B18F
           op1 -> set B18E bit7, clear B18F, set AEEB=4
           op2 -> set B18E bit6, copy 0E -> B18F
         Returns final B18E in dp10.

C1:ACCE  ct_c1_normalize_aee5_to_dp0e                         [strong]
         Normalizes raw AEE5 into working scratch 0E:
           1/2 -> 04
           3/4 -> 0D
           other values unchanged.

C1:ACF2  ct_c1_snapshot_followup_context_to_ae90_ae93         [strong]
         Stores snapshot state:
           AE90 = 0
           AE91 = B18B
           AE92 = AEE3
           AE93 = AEE4
```

## Mask-builder labels

```text
C1:AD09  ct_c1_build_ae95_one_hot_from_aecc0                  [strong]
         Clears AE95, then if AECB>0 and AECC[0]!=FF, builds
         (0x8000 >> AECC[0]) into AE95.

C1:AD35  ct_c1_build_ae99_mask_from_aecc_list                 [strong]
         Clears AE99, then for each current selected entry in
         AECC[0..AECB-1], ORs (0x8000 >> entry) into AE99.
```

## Validation/materialization labels

```text
C1:C1DD  ct_c1_validate_and_materialize_ad8e_list             [provisional]
         Clears AF23, validates seed/selector context against per-entry
         5E4A/5E4B/5E4C/5E4E/5E53 flags, derives a type byte from
         context-dependent CC tables, then dispatches through a case tree
         that materializes candidate entries into AD8E/AD8D.

C1:C72B  ct_c1_set_af23_fail_and_return                       [strong]
         Shared local failure helper:
           AF23 = 1 ; RTS
```

## State labels strengthened in this pass

```text
7E:B18E  ct_c1_followup_packet_byte0_flags_or_descriptor      [provisional]
7E:B18F  ct_c1_followup_packet_byte1_param_or_descriptor      [provisional]
7E:B190  ct_c1_followup_packet_byte2_mode_or_descriptor       [provisional]
7E:B191  ct_c1_followup_packet_byte3_clear_or_reserved        [provisional]

7E:AE95  ct_c1_first_selected_one_hot_mask                    [strong]
7E:AE99  ct_c1_selected_list_mask                             [strong]

7E:AEE5  ct_c1_op01_raw_secondary_param                       [provisional]
7E:000E  ct_c1_normalized_secondary_param_dp0e                [provisional]
7E:AF23  ct_c1_validation_fail_flag                           [strong]
7E:B2C3  ct_fd_op01_resolved_followup_index                   [provisional]
```

## Type/case notes worth carrying forward for `C1:C1DD`

```text
type 0/5/6  -> single mapped entry from B2AE via C8F7         [provisional]
type 1      -> copy non-FF AEFF[0..2] into AD8E               [provisional]
type 3      -> single mapped entry + extra AF15 high-bit gate [provisional]
type 4      -> fixed AD8E = [0,1,2]                           [provisional]
type 7      -> delegated helper path through C82D             [provisional]
```

## Notes for next pass
- Continue through unresolved later `C1:C1DD` type cases before renaming the type byte or the auxiliary byte `0C`.
- Trace the common downstream path at `C1:C55F` to convert the current “follow-up packet” wording into real subsystem semantics.
- Trace consumers of `B18E..B191` and `AE90..AE93` before assigning gameplay-facing names.
