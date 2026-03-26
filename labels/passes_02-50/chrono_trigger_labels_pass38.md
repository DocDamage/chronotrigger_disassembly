# Chrono Trigger (USA) — Labels Added / Strengthened in Pass 38

This file contains labels newly added or materially strengthened in pass 38.

Status tags:
- **[strong]** = safe to carry forward unless contradicted by later control-flow proof
- **[provisional]** = useful working label, but still open to rename/refinement
- **[alias]** = intentional alias/stub label for a table entry landing in shared code or wrapper logic

## Strengthened service-7 packet-byte labels

```text
7E:9604  ct_c1_service7_candidate_partition_select              [strong]
         Service-7 partition selector.
         Proven behavior:
           00h -> scan slots 3..10
           !=00h -> scan slots 0..2

7E:9605  ct_c1_service7_primary_slot_param                      [strong]
         Primary service-7 slot parameter.
         Used as the seed slot in modes 6 and 1/2,
         and as the first anchor slot in modes 0/4.

7E:9606  ct_c1_service7_secondary_slot_param                    [provisional]
         Secondary service-7 slot/anchor parameter.
         Used directly by modes 0/4 as the second anchor / preserved slot.

7E:9607  ct_c1_service7_extent_threshold_param                  [strong]
         Generic service-7 extent/threshold parameter.
         Proven uses:
           - direct compare threshold in mode 1/2
           - scaled by *8 as construction magnitude in mode 0/4

7E:9608  ct_c1_service7_anchor_toggle_param                     [provisional]
         Mode-0/4 construction toggle.
         Switches one side of the dual-anchor geometry between
         the 9605-based and 9606-based anchor path.
```

## Strengthened service-7 handler labels

```text
C1:2332  ct_c1_service7_mode6_seeded_1d23_band_scan             [strong]
         Seeded half-open band scan using 1D23[seed] +/- 20h.
         Accepted matches are written to 99C1+ and the seed slot is stored in 99C0.

C1:23A4  ct_c1_service7_mode3_5_three_vertex_inclusion_scan     [strong]
         Three-vertex inclusion scan using coordinates from slots 0/1/2.
         Orders the three vertices, derives wrapped edge-angle sectors,
         and accepts candidates only if they pass all three sector tests.

C1:25A3  ct_c1_service7_mode0_4_dual_anchor_oriented_inclusion  [provisional]
         Dual-anchor oriented inclusion scan derived from the
         9605 -> 9606 direction, with extent (9607 * 8) and toggle 9608.
         Exact outward shape naming still needs one more proof pass.

C1:2701  ct_c1_service7_mode1_2_seeded_cell_radius_scan         [strong]
         Seeded radius scan in 16-unit cell space.
         Uses abs(dx)>>4 / abs(dy)>>4, maps both through the square table
         at CC:FB6F, and accepts iff dx^2 + dy^2 < 9607.
```

## Newly named shared-tail helpers

```text
C1:27AD  ct_c1_service7_optionally_preserve_slot92_by_partition [strong]
         Conditional seed-preserve tail.
         Stores slot 92 into 99C0 only if it belongs to the partition selected by 9604.

C1:27C5  ct_c1_service7_left_compact_results_if_slot0_empty     [strong]
         If 99C0 is still empty/negative, shifts 99C1+ left into 99C0+.
```

## Newly strengthened helper/data labels

```text
C1:011A  ct_c1_divide_a_by_16                                   [strong]
         Four LSR operations; used by mode 1/2 to normalize coordinates into cell space.

CC:FB6F  ct_cc_square_lookup_table                              [strong]
         Lookup table beginning 00,01,04,09,10,19... .
         Used by mode 1/2 as a square table for coarse-radius comparison.
```

## Notes worth carrying forward
- Service-7 is no longer just “spatial query family” in the abstract.
  The core geometric families are now materially pinned.
- `$9604` is now a strong service-7 partition selector, not just a generic packet byte.
- `23A4` is the strongest structural win of the pass: it is a real three-vertex inclusion test over fixed slots 0/1/2.
- `2701` is now firmly a squared-distance cell-radius scan, not merely a transformed delta compare.
- `25A3` still needs one more semantics pass for the cleanest human-readable shape name, but its dual-anchor oriented construction is now real.
