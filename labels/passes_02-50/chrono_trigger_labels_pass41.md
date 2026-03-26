# Chrono Trigger (USA) — Labels Added / Strengthened in Pass 41

This file contains labels newly added or materially strengthened in pass 41.

Status tags:
- **[strong]** = safe to carry forward unless contradicted by later control-flow proof
- **[provisional]** = useful working label, but still open to rename/refinement
- **[alias]** = intentional alias/stub label for wrapper or branch-entry landing in shared logic

## New / strengthened code labels

```text
C1:16DA  ct_c1_service7_emit_record_and_enqueue_pending_slot             [strong]
         Shared sink reached after a successful outer service-7 path.
         Appends current slot into the small pending FIFO at 99D4..99D8,
         then remaps that slot through CC:FAF0 and emits per-record metadata
         into the larger table rooted at 93EE.

C1:1750  ct_c1_service7_ring_unlink_slot_clear_record_active_bit         [strong]
         Removes a slot from the 3-entry A6D9 ring and clears bit 7 in the
         corresponding emitted record status byte at 93EE + record_offset.

C1:1B17  ct_c1_service7_ring_link_slot_set_record_active_bit             [strong]
         Links a slot through the A6D9 ring and sets bit 7 in the matching
         emitted record status byte at 93EE + record_offset.

C1:B6D1  ct_c1_service7_release_record_table_reservation                 [strong]
         Uses record index * 7 to reach 93EF/93F4, clears the reservation
         latch in 93EF.bit6, and refunds one unit to entry+3 in the 5-byte
         launch table at 1580 when 93F4 matches entry+0.

C1:B96A  ct_c1_service7_consume_canonical_record_pending_and_dispatch    [strong]
         Checks the three canonical fixed records rooted at 93EE / 93F5 /
         93FC, consumes the first pending status bit (bit 6), then dispatches
         on the packed category pair from 93F3 + 7*record_index.

C1:8590  ct_c1_service7_pending_slot_fifo_pop_front                      [strong]
         Pops the front entry from the small pending-slot FIFO:
         99D4 -> out, 99D5 -> 99D4, 99D6 -> 99D5, FF -> 99D6, DEC 99D8.
```

## New / strengthened data / state labels

```text
7E:99D4  ct_c1_service7_pending_slot_fifo                                [strong]
         Root of the 3-entry visible pending-slot FIFO maintained by the
         outer sink and consumed by the pop/shift logic at 8590.

7E:99D8  ct_c1_service7_pending_slot_count                               [strong]
         Pending-slot count / append index for the FIFO at 99D4..99D6.
         Used as the write index by 16DA and decremented by the pop path.

CC:FAF0  ct_c1_service7_slot_to_record_offset_map                        [strong]
         Lookup map translating current slot IDs into record offsets for the
         emitted metadata table rooted at 93EE.

7E:93EE  ct_c1_service7_record_status_flags                              [strong]
         Status byte of emitted records.
         bit 6 = pending/consumable record flag
         bit 7 = linked/active ring marker tied to A6D9 membership

7E:93EF  ct_c1_service7_record_aux_flags_and_reservation                 [strong]
         Emitted record aux/option byte.
         Low bits come from per-slot byte 9F38[x]; bit 6 is a reservation/
         consumption latch tied to the 5-byte launch table refund path.

7E:93F0  ct_c1_service7_record_launch_family_tag                         [strong]
         Emitted launch-family tag copied from 9615 into the per-record table.

7E:93F1  ct_c1_service7_record_primary_result_slot                       [strong]
         Emitted primary result slot copied from A62D into the per-record table.

7E:93F3  ct_c1_service7_record_category_pair                             [strong]
         Packed pair of downstream dispatch categories in low/high 4-bit nibbles.
         Consumed by B580 and B96A-family logic.

7E:93F4  ct_c1_service7_record_table_entry_token                         [strong]
         Record-side copy of the 5-byte launch-table entry+0 token.
         Used later by B6D1 to locate the source table record and refund entry+3.

7E:9F38  ct_c1_service7_slot_aux_flags_for_emitted_records               [provisional]
         Per-slot aux/option byte copied into emitted record field 93EF.
         Structural role is strong; exact human-facing semantics remain open.
```

## New / strengthened record-layout notes

```text
first canonical fixed record  -> 93EE .. 93F4                              [strong]
second canonical fixed record -> 93F5 .. 93FB                              [strong]
third canonical fixed record  -> 93FC .. 9402                              [strong]

These three fixed records are the canonical trio checked by the B96A dispatcher.
They coexist with a broader record-offset space addressed through CC:FAF0.
```

## Notes worth carrying forward
- The `16DA` sink is now proven to be two coordinated write systems: a small pending-slot FIFO and a broader emitted-record table.
- `93EE.bit6` and `93EE.bit7` now have distinct, real meanings; they are not generic flag clutter.
- `93EF.bit6` is a different latch entirely, tied to refunding counts in the 5-byte launch-entry table.
- `93F3` is now structurally solved as a nibble pair even though the nibble-value meanings still need one more pass.
- Best next move: trace the producers of 9F38[x] and the downstream category-dispatch consumers behind the B96A path.
