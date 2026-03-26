# Chrono Trigger (USA) — Labels Added / Strengthened in Pass 37

This file contains labels newly added or materially strengthened in pass 37.

Status tags:
- **[strong]** = safe to carry forward unless contradicted by later control-flow proof
- **[provisional]** = useful working label, but still open to rename/refinement
- **[alias]** = intentional alias/stub label for a table entry landing in shared code or wrapper logic

## Bank-C1 local service dispatch labels

```text
C1:0003  ct_c1_local_service_dispatch_entry                     [strong]
         Entry veneer used by in-bank callers. Immediately jumps to C1:0045.

C1:0045  ct_c1_local_service_dispatch_body                      [strong]
         Saves A/X/Y, doubles selector A, dispatches through JSR ($0051,x),
         then restores registers and returns.

C1:0051  ct_c1_local_service_table                              [strong]
         Primary 8-entry local-service jump table.
         Proven entries:
           0 -> 0023
           1 -> 1B19
           2 -> 1BAA
           3 -> 106E
           4 -> 4058
           5 -> 2986
           6 -> 006D
           7 -> 1FDD
```

## Strengthened descriptor-trigger wrapper labels

```text
C1:C736  ct_c1_store_query_mode_to_986e_and_dispatch_service5   [strong]
         Stores descriptor byte0 (3D) into 986E and dispatches
         local service selector A=#05, which lands at C1:2986.

C1:C741  ct_c1_store_query_mode_to_99cc_and_dispatch_service7   [strong]
         Stores descriptor byte0 (3D) into 99CC and dispatches
         local service selector A=#07, which lands at C1:1FDD.
```

## Selector-7 dispatch labels

```text
C1:1FDD  ct_c1_service7_subdispatch_via_99cc                    [strong]
         Secondary submode dispatcher for local service #07.
         Uses 99CC as a 0..6 selector and dispatches via C1:1FEA.

C1:1FEA  ct_c1_service7_mode_table                              [strong]
         7-entry submode table for service #07.
         Proven entries:
           0 -> 25A3
           1 -> 2701
           2 -> 2701
           3 -> 23A4
           4 -> 25A3
           5 -> 23A4
           6 -> 2332

7E:99CC  ct_c1_service7_mode_99cc                               [strong]
         Submode selector register for local service #07.
```

## Selector-7 result-buffer lifecycle labels

```text
C1:27D9  ct_c1_clear_service7_result_vectors_99c0_a62d          [strong]
         Clears 99C0..99CB and A62D..A638 to FF.

C1:27E8  ct_c1_finalize_service7_results_and_mirror_to_a62d     [strong]
         Sets 960C to 80h and mirrors 99C0..99CA into A62D..A637.

7E:99C0  ct_c1_service7_result_slots_99c0                       [strong]
         Bounded result vector produced by service-7 query families.
         Uses FF as empty/terminator marker.

7E:A62D  ct_c1_service7_result_shadow_a62d                      [strong]
         Shadow/mirror vector for service-7 results.
         Cleared in lockstep with 99C0.. and refreshed from it by 27E8.

7E:960C  ct_c1_service7_result_finalize_flags_960c              [provisional]
         Service-7 result/finalization flag byte.
         27E8 stores 80h here before mirroring 99C0 -> A62D.
```

## Service-7 handler family labels

```text
C1:2332  ct_c1_service7_mode6_seeded_axis_window_scan           [provisional]
         Uses 9605 as seed slot, derives a simple +-20h window on one axis,
         scans qualifying slots, appends matches to 99C1+, and stores the
         seed slot in 99C0.

C1:23A4  ct_c1_service7_mode3_5_geometry_scan_family            [provisional]
         Loads multiple coordinates from 1D0C/1D23, orders local bounds,
         performs repeated geometry/math helper calls, and materializes
         qualifying slot indices into 99C0.. .

C1:25A3  ct_c1_service7_mode0_4_extended_spatial_metric_scan    [provisional]
         Consumes the wider 9605/9606/9607/9608 packet set,
         derives several local metrics, and materializes qualifying slot
         indices into 99C0.. .

C1:2701  ct_c1_service7_mode1_2_transformed_delta_threshold_scan [provisional]
         Normalizes coordinates, computes absolute deltas, maps them through
         CC:FB6F, combines the mapped deltas, and keeps candidates whose
         transformed metric compares favorably against 9607.
```

## Notes worth carrying forward
- Service selector #05 and service selector #07 are now cleanly separated.
- Service #05 remains the relation-query subsystem already established earlier.
- Service #07 is a separate candidate-list materialization family keyed by 99CC and fed by 9604..9608.
- Do not over-name the exact gameplay meaning of service-7 submodes yet.
- 99C0/A62D are now strong vector labels; they are not generic scratch anymore.
