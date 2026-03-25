# Chrono Trigger Disassembly Labels — Pass 43

This file contains labels newly added or materially strengthened in pass 43.

As in prior passes:
- **strong** = control flow and data role are directly supported by the ROM work in this pass
- **provisional** = structurally useful but still not safe as a final gameplay-facing name

---

## Strong labels

### C1:1B19  ct_c1_service1_enqueue_lane_and_mark_record_active           [strong]
- Local service-1 entry for the 3-lane controller.
- If the current lane is not already active in `A6D9[x]`, maps it through `CC:FAF0`,
  sets `93EE.bit7` for the matching emitted record, appends the lane into
  `95D6 + pending_count`, seeds `95DC[current_lane]`, and increments `95DA`.

### C1:1B69  ct_c1_promote_pending_lane_into_active_roster               [strong]
- Pulls the head of the pending lane queue at `95D6` into the active roster.
- Clears `9F38[lane]`, seeds small per-lane state bytes, stores the lane into
  `A6D9[lane]`, compacts `95D6..95D8`, decrements `95DA`, increments `A6DE`,
  and seeds `A6DD` if no current active lane exists.

### C1:1BAA  ct_c1_service2_remove_lane_and_reseat_active_controller      [strong]
- Local service-2 entry for the same 3-lane controller.
- Deletes the input lane from either:
  - the pending-admission queue (`95D6..95D8`), or
  - the active roster (`A6D9` / `A6DE`)
- If the removed lane was the current active lane (`A6DD`), also clears/reseats
  outer selection state (`9609 / 960E / 9614 / 95DB / 99E0`), rescans the next
  live active lane, updates `A6DD` and `95D5`, then falls through to `1C3A`.

### C1:1C3A  ct_c1_service2_restore_workspace_template_0b40              [strong]
- Common tail reached from service 2.
- Copies `0x180` bytes from `D1:5800` into WRAM rooted at `0B40`.
- Exact high-level meaning of the workspace is still open, but the template-restore
  role is direct ROM proof.

### 7E:A6D9  ct_c1_active_lane_roster_marker_per_lane                    [strong]
- Three-entry per-lane active-roster membership marker.
- `FF` = absent/inactive.
- Nonnegative = lane is present in the local active controller.

### 7E:A6DD  ct_c1_current_active_lane                                   [strong]
- Current active lane for the local 3-lane controller.
- Reseated by service 2 when the current lane is removed.

### 7E:A6DE  ct_c1_active_lane_count                                     [strong]
- Active-lane count for the local 3-lane controller.
- Incremented when a pending lane is promoted; decremented when an active lane is removed.

### 7E:95D6  ct_c1_pending_lane_admission_queue                          [strong]
- Root of the 3-entry pending-admission queue consumed by `1B69` and compacted by `1BAA`.

### 7E:95DA  ct_c1_pending_lane_admission_count                          [strong]
- Pending queue count / append index for `95D6..95D8`.

### 7E:B188  ct_c1_lane_occupied_refresh_latch                           [strong]
- Per-lane occupied/refresh-required latch.
- Directly gates whether the lane-clear path at `FD:A8FE` escalates into local service 2.

---

## Provisional labels

### 7E:A6DF  ct_c1_lane_roster_change_sentinel                           [provisional]
- Forced to `FEh` in both the pending->active promotion path and the active-lane removal path.
- Structurally real, but exact downstream meaning still needs more proof.

### 7E:B158  ct_c1_lane_primary_carried_value                            [provisional]
- Per-lane carried scalar maintained beside the canonical-record lane system.
- Mirrored into `AFAB`, and exported to `99DD` / `9F22` in the clear/update families.

### 7E:AFAB  ct_c1_lane_primary_carried_value_shadow                     [provisional]
- Per-lane shadow/mirror of `B158`.

### 7E:99DD  ct_c1_lane_primary_value_export_a                           [provisional]
- Export mirror updated from the same lane-carried value family as `B158/AFAB`.

### 7E:9F22  ct_c1_lane_primary_value_export_b                           [provisional]
- Second export mirror updated from the same lane-carried value family as `B158/AFAB`.

### 7E:B03A  ct_c1_lane_secondary_dirty_latch                            [provisional]
- Secondary per-lane latch cleared beside `B188` in the lane-reset families.
- Structurally part of the same carried-state bundle, but exact semantics remain open.

### 7E:9F38  ct_c1_lane_emitted_aux_or_mask                              [provisional]
- Lane-side aux bits ORed into emitted record aux state at `93EF + record_offset`.
- Only the clear path is directly proved this pass; the positive writer is still unresolved.

---

## Strengthened existing labels

### FD:A8FE  ct_fd_service7_clear_occupied_lane_and_refresh_service2     [strong]
- Strengthened by pass 43.
- The “refresh service 2” half is now specifically understood as callback into the
  local 3-lane roster-removal/reseat controller at `C1:1BAA`.

### C1:B961  ct_c1_local_service2_wrapper                                [strong]
- Strengthened by pass 43.
- Exact wrapper into the lane-roster removal/reseat service.

