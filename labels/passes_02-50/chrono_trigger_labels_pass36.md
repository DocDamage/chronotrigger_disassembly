# Chrono Trigger (USA) — Labels Added / Strengthened in Pass 36

This file contains labels newly added or materially strengthened in pass 36.

Status tags:
- **[strong]** = safe to carry forward unless contradicted by later control-flow proof
- **[provisional]** = useful working label, but still open to rename/refinement
- **[alias]** = intentional alias/stub label for a table entry landing in shared code or wrapper logic

## Common-tail pipeline labels

```text
C1:C55F  ct_c1_expand_and_finalize_ad8e_via_cc2ab0_descriptors   [strong]
         Common downstream pipeline reached from multiple C1DD type families.
         Uses mode byte 3A, descriptor index 0C, pointer table CC:2AB0,
         per-record packet emitters/services, bounded result merging from
         99C0 into AD8E/AECC, then final AD8E compaction/count derivation.

C1:C659  ct_c1_handle_empty_query_result_before_local_fail       [provisional]
         Empty-result special handler used when common-tail query results are
         empty and mode != 4. Prepares AE91..AE96 context, chooses AE93 from
         fixed values {7B,7C,7D}, calls AC57, then fails through C72B.

C1:C6D9  ct_c1_compact_ad8e_against_aeff_and_set_ad8d            [strong]
         Final compaction/count phase:
           - removes AD8E entries whose AEFF[entry] == FF by shifting left
           - derives AD8D from first FF terminator
           - sets AF23=1 if bounded list has no terminator
```

## Descriptor pipeline helper labels

```text
C1:C74C  ct_c1_load_seed_selector_context_to_dp00_dp0c           [strong]
         Loads working scratch for the common descriptor pipeline:
           00/02/04 from selector-related state
           06 = B2AE
           0C = B18B
         also mirrors selector bytes into AE97/AE98 when applicable.

C1:C95C  ct_c1_9604_packet_writer_table                          [strong]
         Word table of packet-writer subroutines selected by
         (descriptor_byte1 & 0x7F) * 2.

C1:C78D  ct_c1_emit_9604_packet_mode0                            [strong]
         Writes packet bytes from dp0A/dp00/dp06/dp08/dp0E.

C1:C7A7  ct_c1_emit_9604_packet_mode1                            [strong]
         Writes reduced packet bytes from dp0A/dp06/dp08.

C1:C7BD  ct_c1_emit_9604_packet_mode2                            [strong]
         Writes reduced packet bytes from dp0A/dp08.

C1:C7D1  ct_c1_emit_9604_packet_mode3                            [strong]
         Writes packet bytes from dp00/dp06/dp02.

C1:C7E7  ct_c1_emit_9604_packet_mode4                            [strong]
         Writes packet bytes from dp0A/dp02/dp08.

C1:C7FD  ct_c1_emit_9604_packet_mode5                            [strong]
         Writes packet bytes from dp0A/dp0C/dp08.

C1:C813  ct_c1_emit_9604_packet_mode6                            [strong]
         Writes packet bytes from dp0A/dp0C/dp06/dp08/dp0E.

C1:C736  ct_c1_store_3d_to_986e_and_call_service5                [provisional]
         Descriptor-selected trigger wrapper:
           986E = 3D
           A = 05
           JSR $0003

C1:C741  ct_c1_store_3d_to_99cc_and_call_service7                [provisional]
         Descriptor-selected trigger wrapper:
           99CC = 3D
           A = 07
           JSR $0003
```

## Type-family notes strengthened in this pass

```text
C1:C431  ct_c1dd_type08_tail_aeff_index_materializer            [provisional]
         Builds AD8E from later AEFF-index positions and enters common tail
         with 3A = 1.

C1:C478  ct_c1dd_type09_random_four_bucket_splitter             [provisional]
         Randomized 4-bucket dispatcher using AF22(#64), bytes 00:00FA/00:00FB,
         and delegated jumps into C82D / earlier shared list-builder paths.

C1:C4FA  ct_c1dd_type0b_0c_0d_0e_0f_12_1a_delegate_to_c82d      [strong]
         Shared family:
           JSR C82D
           if AF23!=0 -> fail
           else 3A=2 -> C55F

C1:C51C  ct_c1dd_type10_11_13_14_15_1b_direct_common_tail       [strong]
         Shared family:
           3A=3
           -> C55F

C1:C53C  ct_c1dd_type0a_direct_common_tail_mode1                [strong]
         Shared family:
           3A=1
           -> C55F

C1:C546  ct_c1dd_type32_single_mapped_entry_mode4               [strong]
         Maps B2AE through C8F7, seeds AD8E[0], AD8D=1, 3A=4, 0A=1,
         then enters C55F.
```

## State labels strengthened in this pass

```text
7E:003A  ct_c1_common_tail_mode_3a                              [strong]
         Common-tail post-materialization mode selector.

7E:000C  ct_c1_cc2ab0_descriptor_index                          [strong]
         Nonzero selector used by C55F to index the CC:2AB0 descriptor table.

7E:003B  ct_c1_current_cc2ab0_descriptor_base                   [strong]
         16-bit base pointer loaded from CC:2AB0[0C].

7E:003C  ct_c1_descriptor_service_selector_flag                 [provisional]
         Local boolean derived from descriptor byte1 bit7;
         chooses between C736 vs C741.

7E:003D  ct_c1_descriptor_service_arg0                          [provisional]
         Local byte loaded from descriptor byte0 and consumed by C736/C741.

7E:9604  ct_c1_service_packet_byte0                             [provisional]
7E:9605  ct_c1_service_packet_byte1                             [provisional]
7E:9606  ct_c1_service_packet_byte2                             [provisional]
7E:9607  ct_c1_service_packet_byte3                             [provisional]
7E:9608  ct_c1_service_packet_byte4                             [provisional]
         Packet bytes emitted by the C78D..C813 writer family.

7E:99C0  ct_c1_common_tail_query_result_slots                   [provisional]
         Bounded result vector consumed by C55F and merged into AD8E/AECC.

7E:AD8E  ct_c1_candidate_list_ad8e                              [strong]
7E:AD8D  ct_c1_candidate_count_ad8d                             [strong]

7E:AECC  ct_c1_common_tail_candidate_mirror                     [provisional]
         Parallel mirror of currently accepted common-tail query entries.
```

## Notes worth carrying forward
- Do not assign final subsystem names to the service/query engine behind `JSR $0003` yet.
- Do not assign gameplay semantics to descriptor bytes until the service engine and `$9604..$9608` consumers are traced.
- Type `9` is structurally real but still semantically incomplete.
- The `C1DD -> C55F` seam is now strong enough that future work should focus downstream rather than repeatedly reopening the type dispatch itself.
