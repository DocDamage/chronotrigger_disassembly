# Chrono Trigger (USA) — Labels Added / Strengthened in Pass 39

This file contains labels newly added or materially strengthened in pass 39.

Status tags:
- **[strong]** = safe to carry forward unless contradicted by later control-flow proof
- **[provisional]** = useful working label, but still open to rename/refinement
- **[alias]** = intentional alias/stub label for a table entry landing in shared code or wrapper logic

## New / strengthened code labels

```text
C1:1FF8  ct_c1_service7_wrapper_opcode_table                    [strong]
         33-entry outer wrapper table indexed by ($960D & 7Fh),
         clamped at 20h, then JSR'd through via abs,X indirect.

C1:203A  ct_c1_service7_bounded_eligible_collector             [strong]
         Shared collector body used by multiple wrapper-table entries.
         Caller supplies start/end range and optional whole-vector mirror.
         Preserves $960F specially into $99C0 and appends others into $99C1+.

C1:209A  ct_c1_service7_first3_eligible_collect_mirror_all     [strong]
         Wrapper variant of 203A.
         Scans slots 0..2 and enables whole-vector mirror via $960C.7.

C1:20A9  ct_c1_service7_late_partition_eligible_collect        [strong]
         Wrapper variant of 203A.
         Scans slots 3..10 without forcing whole-vector mirror.

C1:20B6  ct_c1_service7_late_partition_collect_mirror_all      [strong]
         Wrapper variant of 203A.
         Scans slots 3..10 and enables whole-vector mirror via $960C.7.

C1:20C6  ct_c1_service7_full_range_collect_mirror_all          [strong]
         Wrapper variant of 203A.
         Starts at slot 0, upper bound 11, and enables whole-vector mirror.

C1:20D6  ct_c1_service7_direct_passthrough_via_95d5            [strong]
         Direct scalar-result wrapper.
         Copies $95D5 into both $99C0 and $A62D.

C1:20E0  ct_c1_service7_first3_negative_flag_scan              [provisional]
         Fixed first-three-slot scan using sign bits from
         $5E4A/$5ECA/$5F4A under additional per-slot gates.

C1:2136  ct_c1_service7_first3_class5_selector                 [strong]
         First-three-slot selector for the first slot with $2980 == 05h.

C1:2163  ct_c1_service7_first3_class4_selector                 [strong]
         First-three-slot selector for the first slot with $2980 == 04h.

C1:2169  ct_c1_service7_rotated_dual_anchor_wrapper_toggle0    [provisional]
         Builds a later-partition candidate vector, optionally rotates
         the cursor, then preloads $9604..$9608 for 25A3 with $9608 = 0.

C1:21AF  ct_c1_service7_class3_anchor_dual_anchor_wrapper      [provisional]
         Uses the first first-three slot with $2980 == 03h as the
         primary anchor, then builds the 25A3 packet.

C1:2203  ct_c1_service7_rotated_dual_anchor_wrapper_toggle1    [provisional]
         Same broad structure as 2169, but preloads $9608 = 01h for 25A3.

C1:224B  ct_c1_service7_seed960f_radius16_wrapper              [strong]
         Direct packet wrapper for 2701.
         Uses $960F as seed slot and threshold 10h.

C1:225F  ct_c1_service7_rotated_seeded_radius_wrapper          [provisional]
         Builds a later-partition vector, optionally rotates the cursor,
         then seeds 2701 from $99C0[$9614] with threshold 09h or 19h.

C1:22A4  ct_c1_service7_class3_seeded_radius_wrapper           [provisional]
         Seeds 2701 from the first first-three slot with $2980 == 03h,
         with threshold 10h or 19h depending on wrapper opcode.

C1:22D3  ct_c1_service7_class6_seeded_radius19_wrapper         [strong]
         Seeds 2701 from the first first-three slot with $2980 == 06h,
         using threshold 19h.

C1:22F5  ct_c1_service7_rotated_seeded_band_wrapper            [provisional]
         Builds a later-partition vector, optionally rotates the cursor,
         then seeds 2332 from $99C0[$9614].

C1:232A  ct_c1_service7_direct_triangle_wrapper                [provisional]
         Direct wrapper for 23A4:
         STZ $9604 ; JSR $23A4 ; JMP $27E8.
         Real code, but not yet proven to be a 1FF8 table entry.

C1:27FA  ct_c1_service7_result_cursor_next_live                [strong]
         Advances $9614 to the next non-negative $99C0 entry with wraparound.

C1:2814  ct_c1_service7_result_cursor_prev_live                [strong]
         Moves $9614 to the previous non-negative $99C0 entry with wraparound.

C1:282D  ct_c1_service7_result_vector_any_live                 [strong]
         Returns Z set if all entries in $99C0..$99CA are FFh/negative,
         otherwise returns Z clear.
```

## New / strengthened WRAM / state labels

```text
7E:960A  ct_c1_service7_query_epoch_or_scan_counter            [provisional]
         Incremented by the bounded collector and several scalar wrappers.
         Explicitly cleared before cursor-rotation-driven wrapper reuse.

7E:960C  ct_c1_service7_result_vector_mirror_flags             [provisional]
         Sign/bit7 controls whole-vector mirror behavior in the shared
         collector, and 27E8 also sets it before mirroring 99C0.. -> A62D...

7E:960D  ct_c1_service7_wrapper_opcode                         [strong]
         Low 7 bits index the 33-entry wrapper opcode table at C1:1FF8.

7E:960F  ct_c1_service7_preferred_seed_slot                    [provisional]
         Preferred/seed slot used by the common collector and by several
         geometry-packet wrappers.

7E:9613  ct_c1_service7_first_live_result_or_fail_marker       [provisional]
         Outer wrapper tail caches the first non-negative mirrored result
         from A62D.. here, or leaves a negative marker when no result exists.

7E:9614  ct_c1_service7_result_cursor_index                    [strong]
         Cursor index over the live service-7 result vector.
         Rotated by 27FA / 2814.

7E:2980  ct_c1_slot_class_or_discriminator                     [provisional]
         Slot discriminator byte searched explicitly for values
         03h, 04h, 05h, and 06h by wrapper-layer selectors.
```

## Opcode-table aliases worth carrying forward

```text
wrapper opcode 00 -> ct_c1_service7_bounded_eligible_collector                [alias]
wrapper opcode 01 -> ct_c1_service7_first3_eligible_collect_mirror_all        [alias]
wrapper opcode 02 -> ct_c1_service7_direct_passthrough_via_95d5               [alias]
wrapper opcode 03 -> ct_c1_service7_first3_negative_flag_scan                 [alias]
wrapper opcode 04 -> ct_c1_service7_first3_eligible_collect_mirror_all        [alias]
wrapper opcode 05 -> ct_c1_service7_first3_class5_selector                    [alias]
wrapper opcode 06 -> ct_c1_service7_first3_class4_selector                    [alias]
wrapper opcode 07 -> ct_c1_service7_late_partition_eligible_collect           [alias]
wrapper opcode 08 -> ct_c1_service7_late_partition_collect_mirror_all         [alias]
wrapper opcode 09 -> ct_c1_service7_full_range_collect_mirror_all             [alias]
wrapper opcode 0A -> ct_c1_service7_late_partition_collect_mirror_all         [alias]
wrapper opcode 0B -> ct_c1_service7_rotated_dual_anchor_wrapper_toggle0       [alias]
wrapper opcode 0C -> ct_c1_service7_rotated_dual_anchor_wrapper_toggle1       [alias]
wrapper opcode 0D -> ct_c1_service7_class3_anchor_dual_anchor_wrapper         [alias]
wrapper opcode 0E -> ct_c1_service7_bounded_eligible_collector                [alias]
wrapper opcode 0F -> ct_c1_service7_rotated_seeded_band_wrapper               [alias]
wrapper opcode 10 -> ct_c1_service7_bounded_eligible_collector                [alias]
wrapper opcode 11 -> ct_c1_service7_seed960f_radius16_wrapper                 [alias]
wrapper opcode 12 -> ct_c1_service7_rotated_seeded_radius_wrapper             [alias]
wrapper opcode 13 -> ct_c1_service7_class3_seeded_radius_wrapper              [alias]
wrapper opcode 14 -> ct_c1_service7_class3_seeded_radius_wrapper              [alias]
wrapper opcode 15 -> ct_c1_service7_bounded_eligible_collector                [alias]
wrapper opcode 16 -> ct_c1_service7_bounded_eligible_collector                [alias]
wrapper opcode 17 -> ct_c1_service7_bounded_eligible_collector                [alias]
wrapper opcode 18 -> ct_c1_service7_wrapper_noop_rts_2329                     [alias]
wrapper opcode 19 -> ct_c1_service7_bounded_eligible_collector                [alias]
wrapper opcode 1A -> ct_c1_service7_rotated_seeded_radius_wrapper             [alias]
wrapper opcode 1B -> ct_c1_service7_class6_seeded_radius19_wrapper            [alias]
wrapper opcode 1C -> ct_c1_service7_bounded_eligible_collector                [alias]
wrapper opcode 1D -> ct_c1_service7_bounded_eligible_collector                [alias]
wrapper opcode 1E -> ct_c1_service7_bounded_eligible_collector                [alias]
wrapper opcode 1F -> ct_c1_service7_bounded_eligible_collector                [alias]
wrapper opcode 20 -> ct_c1_service7_bounded_eligible_collector                [alias]
```

## Notes worth carrying forward
- The service-7 bodies themselves are no longer the main ambiguity; the wrapper opcode layer is now mostly classified.
- `$9614` is now a real result cursor, not disposable scratch.
- `$960C.7` is materially tied to whole-vector mirror/valid behavior.
- `$2980` has crossed the threshold from “unknown byte” to “real slot discriminator/class field,” even though the human-facing names for its values are still open.
- The best next move is above this layer: trace who preloads `$960D`, `$960F`, `$9614`, and `$EF`.
