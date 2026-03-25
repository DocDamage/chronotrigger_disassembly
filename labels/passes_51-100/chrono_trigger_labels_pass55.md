# Chrono Trigger Disassembly Labels — Pass 55

This file contains labels newly added, replaced, or materially strengthened in pass 55.

As in prior passes:
- **strong** = directly supported by control flow and data flow in this pass
- **strengthened** = previously useful label materially tightened by new proof
- **provisional** = structurally useful but not yet safe as a final frozen gameplay-facing name

---

## Strong labels

### 7E:AEFF..7E:AF09  ct_battle_slot_occupant_index_map                           [strong]
- Slot-indexed map.
- Each non-`FF` entry names the battler/participant currently assigned to that slot.
- `FF` means the slot is unoccupied.
- Proven by:
  - direct slot initialization at `FD:B24D..B27E`
  - alternate rebuild at `C1:FB06..FB2C`
  - inverse-map construction into `B1BE` at `FD:B28F..B2A3`
  - battler-structured downstream consumption at `FD:B363...`

### 7E:AF0A..7E:AF14  ct_battle_slot_default_occupant_index_map                    [strong]
- Initialized in lockstep with `AEFF`.
- Used by `C1:B279..B28E` to restore live slot occupancy.
- Shares the same `FF` empty sentinel semantics.

### 7E:B1BE..          ct_battler_to_visible_head_slot_inverse_map                 [strong]
- Rebuilt from `AEFF[0..2]` at `FD:B28F..B2A3`.
- Semantics: `B1BE[battler] = visible head slot`.
- Consumed directly by `C1:BE50..BF24`.

### 7E:AEC5           ct_visible_head_occupied_slot_count                          [strong]
- Incremented when canonical head-slot rebuilds admit a valid visible occupant.
- Reset and rebuilt in both:
  - `FD:B24D..B27E`
  - `C1:FB06..FB2C`

---

## Strengthened labels

### 7E:AEFF..7E:AF09  ct_battle_slot_active_entry_gate_array                       [replaced]
- Too weak after pass 55.
- Replaced by:
  - `ct_battle_slot_occupant_index_map`
- The gating behavior from pass 54 remains true, but it is now clearly a consequence of slot occupancy, not the primary noun.

### 7E:AF0A..7E:AF14  ct_battle_slot_occupant_index_mirror                         [strengthened]
- Pass 55 shows this is not just a mirror.
- It is the remembered/default occupant map used for restoration.

### 7E:AEC5           ct_visible_head_active_slot_count                            [strengthened]
- Tightened from generic “active slot count” wording.
- Specifically counts admitted visible-head occupants during head-map rebuild.

### 7E:B1BE..         ct_visible_lane_inverse_lookup                               [strengthened]
- Pass 55 makes the direction exact:
  - battler index -> visible head slot
- Used by targeted readiness/gauge helpers after `B2EB/B2EC` selection.

### FD:B28F..FD:B2A3  ct_fd_rebuild_visible_head_battler_to_slot_inverse_map       [strengthened]
- Previously only loosely understood as a small inverse/lookup rebuild.
- Pass 55 freezes the exact source and direction:
  - source: `AEFF[0..2]`
  - destination: `B1BE[battler] = slot`

---

## Provisional labels

### C1:B279..C1:B2C0  ct_c1_restore_or_clear_live_battle_slot_occupant_from_default_map   [provisional]
- Strong structure:
  - restores `AEFF[Y]` from `AF0A[Y]` when a remembered occupant exists
  - later clears `AEFF[Y] = FF` on failure/removal path
- Kept provisional because the exact higher-level gameplay trigger for this restore/remove operation still wants one more caller-context pass.

### FD:B24D..FD:B27E  ct_fd_initialize_head_battle_slot_occupant_maps_from_party_state     [provisional]
- The head-map construction is strong.
- The exact upstream gameplay noun for the `2980` validity source is still left slightly cautious.

### C1:FB06..C1:FB2C  ct_c1_rebuild_head_battle_slot_occupant_maps_with_extra_guard         [provisional]
- Same structural model as `FD:B24D..B27E`.
- Extra exclusion via `A09B[X]` is proven.
- Final caller-facing subsystem name still wants one more pass.

---

## Replaced / retired wording

### 7E:AEFF..7E:AF09  “active-entry gate array”                                    [retired as primary noun]
- Still true in pass-54 arithmetic terms.
- No longer the best primary label after pass 55.

### 7E:AF0A..7E:AF14  “occupant mirror”                                            [retired as primary noun]
- Too weak after restore-path proof.
- Replace with “default / remembered occupant index map”.

---

## Exact mapping model now safe to carry forward

Head rebuild:
```text
for slot in 0..2:
  if source entry valid:
    AEFF[slot] = battler_index
    AF0A[slot] = battler_index
    AEC5++
```

Inverse rebuild:
```text
for slot in 0..2:
  battler = AEFF[slot]
  if battler != FF:
    B1BE[battler] = slot
```

Restore path:
```text
if AF0A[slot] != FF:
  AEFF[slot] = AF0A[slot]
```

Clear path:
```text
AEFF[slot] = FF
```

Downstream targeting:
```text
battler = B2EB / B2EC
slot    = B1BE[battler]
operate on slot-local readiness/gauge state
```

---

## Notes for next pass
- Trace direct producer paths for tail-slot occupants beyond the visible-head rebuilders.
- Re-check the ready-transition helpers with the now-frozen occupant-map model.
- Target the downstream logic that distinguishes:
  - occupied-but-zero readiness
  - occupied-and-one-step-away readiness
  - occupied-and-larger-positive readiness
