# Chrono Trigger (USA) — Labels Added / Strengthened in Pass 40

This file contains labels newly added or materially strengthened in pass 40.

Status tags:
- **[strong]** = safe to carry forward unless contradicted by later control-flow proof
- **[provisional]** = useful working label, but still open to rename/refinement
- **[alias]** = intentional alias/stub label for wrapper or branch-entry landing in shared logic

## New / strengthened code labels

```text
C1:1153  ct_c1_service7_outer_current_slot_controller                    [strong]
         Top local controller above service 7.
         Branches between fresh-launch, replay/finalize, and follow-up families.

C1:129C  ct_c1_service7_state0_fixed_wrapper07_launch                    [strong]
         Local state-0 launch branch.
         Writes $960D = 07h, clears $9615, then launches through $1F79.

C1:12BC  ct_c1_service7_state1_followup_setup                            [strong]
         Local state-1 deferred follow-up setup.
         Seeds $95DB = 1 and $9615 = 1; does not call $1F79 directly.

C1:12ED  ct_c1_service7_state2_followup_setup                            [strong]
         Local state-2 deferred follow-up setup.
         Seeds $95DB = 2 and $9615 = 2; does not call $1F79 directly.

C1:1369  ct_c1_service7_dynamic_opcode_launch_from_9ee4                 [strong]
         Follow-up family that gates on $A099/$9EE5 and writes $960D from $9EE4.

C1:1498  ct_c1_service7_table_driven_entry_launch                        [strong]
         Follow-up family that computes 5*($95E6 + $95E5), reads entry fields
         rooted at C1:1580, latches aux/opcode into $9F35/$960D, and launches.

C1:1561  ct_c1_service7_replay_finalize_controller                       [strong]
         Shared replay/finalize path entered when $9609 != 0 or after a
         successful fresh wrapper launch.

C1:176C  ct_c1_service7_outer_cursor_next_commit                         [strong]
         Outer controller helper that advances $9614 to the next live $99C0 entry,
         exports it to $A62D, then returns through common cleanup.

C1:1786  ct_c1_service7_outer_cursor_prev_commit                         [strong]
         Outer controller helper that moves $9614 to the previous live $99C0 entry,
         exports it to $A62D, then returns through common cleanup.

C1:179C  ct_c1_service7_outer_option_cleanup                             [strong]
         Common cleanup tail for the outer controller.
         Clears DP option bytes $EE and $EF, then returns.

C1:1F79  ct_c1_service7_common_launch_init                               [strong]
         Common launch initializer above the wrapper-opcode table.
         Injects current slot into $960F, clears result state, and dispatches via $1FF8.
```

## New / strengthened data / state labels

```text
7E:9609  ct_c1_service7_replay_phase_counter                             [strong]
         Outer in-progress / replay counter for the service-7 controller.
         Fresh launches increment it; replay/finalize paths decrement it.

7E:960F  ct_c1_service7_preferred_source_slot                            [strong]
         Current/preferred source slot for the next wrapper launch.
         Written by $1F79 from $95D5.

7E:95DB  ct_c1_service7_followup_family                                  [strong]
         Outer follow-up family selector.
         Observed values: 0 = local/plain, 1 = dynamic-opcode family,
         2 = table-driven family.

7E:95DC  ct_c1_service7_local_submode_per_slot                           [strong]
         Per-slot 3-state local query/selection submode index.
         Values cycle 0..2 and choose the 129C / 12BC / 12ED branches.

7E:95E5  ct_c1_service7_outer_index_component_lo                         [provisional]
         Outer cursor/index component clamped through a 0..2 band.
         Participates in the summed table-entry index used by 1498.

7E:95E6  ct_c1_service7_outer_index_component_hi                         [provisional]
         Outer cursor/index component adjusted in ±1 and ±3 steps.
         Participates in the summed table-entry index used by 1498.

7E:9615  ct_c1_service7_launch_family_tag                                [provisional]
         Outer launch-family tag carried into emitted record field 93F0.
         Observed values in this controller: 0, 1, 2.

7E:9F35  ct_c1_service7_table_entry_aux_byte                             [strong]
         Latched auxiliary payload byte from the selected 5-byte launch entry.

7E:9F36  ct_c1_service7_table_entry_offset                               [strong]
         Saved byte offset of the selected 5-byte launch entry rooted at C1:1580.

DP:EE    ct_c1_service7_outer_option_flags_a                             [provisional]
         Caller-provided outer option byte consumed by the current-slot controller
         and the replay/finalize path. Producers still unresolved.

DP:EF    ct_c1_service7_outer_option_flags_b                             [provisional]
         Caller-provided outer option byte spanning both local-state branches
         and result-cursor rotation. Producers still unresolved.
```

## New / strengthened inline-table labels

```text
C1:1580  ct_c1_service7_table_launch_entry_bytes                         [provisional]
         Root of the 5-byte entry table consumed by the table-driven launch family.
         Entry index = 5 * ($95E6 + $95E5).

entry +0 -> auxiliary payload latched into $9F35                         [strong]
entry +1 -> wrapper opcode latched into $960D                            [strong]
entry +2 -> sign/validity gate (BMI = reject)                            [strong]
entry +3 -> remaining-count / enabled gate (BEQ = reject)                [strong]
entry +4 -> unresolved                                                   [provisional]
```

## Notes worth carrying forward
- The outer controller above service 7 is now meaningfully classified; the ambiguity has moved downstream into the emitted `93EE..93F4` records and upstream into the producers of `EE/$EF`.
- `$960F` is no longer vague: it is the current/preferred source slot injected by the common launch initializer.
- `$9609` is now clearly a replay/follow-up counter, not scratch.
- The `1498` family proved that `$95E5/$95E6` are real index components and that the bytes rooted at `1580` are a deliberate 5-byte entry table, even though that table overlaps code bytes structurally.
- Best next move: decode the `16DA..1713` record sink and then trace its consumers.
