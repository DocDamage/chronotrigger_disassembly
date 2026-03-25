# Chrono Trigger Disassembly Labels — Pass 54

This file contains labels newly added, replaced, or materially strengthened in pass 54.

As in prior passes:
- **strong** = directly supported by control flow and arithmetic in the ROM work of this pass
- **strengthened** = previously useful label materially tightened by new proof
- **provisional** = structurally useful but still not safe as a final frozen gameplay-facing name

---

## Strong labels

### FD:B8F7..FD:B93A  ct_fd_normalize_active_battle_slot_readiness_to_minimum_one_before_head_export   [strong]
- Real post-seed normalization body.
- Scans the unified work array `AFAB..AFB5`.
- Selects the smallest eligible **positive** entry.
- Computes subtractive delta = `(min - 1)`.
- Subtracts that delta from every eligible positive entry.
- Leaves zero entries unchanged.
- Leaves `AEFF == FF` entries unchanged.
- Runs immediately before the head export at `B93B..B94F`.

---

## Strengthened labels

### 7E:AFAB..7E:AFB5  ct_battle_slot_readiness_work_array                         [strengthened]
- Pass 53 proved this is one unified 11-entry work array.
- Pass 54 proves it is also the target of a **minimum-positive subtractive normalization**.
- Smallest eligible positive value is forced to `1` before head export.
- Zero entries are preserved.
- `AEFF == FF` entries are preserved.

### 7E:AFAB..7E:AFAD  ct_visible_head_lane_readiness_work_array                   [strengthened]
- Still the visible head partition.
- Pass 54 proves these values are exported **after unified 11-slot normalization**, not as raw seeded values.

### 7E:AFAE..7E:AFB5  ct_runtime_tail_slot_readiness_work_array                   [strengthened]
- Tail partition still not exported directly here.
- Pass 54 proves it still participates in the same shared normalization pass as the visible head.
- This is strong evidence that head and tail are one readiness/countdown space, not parallel unrelated arrays.

### 7E:AEFF..7E:AF09  ct_battle_slot_active_entry_gate_array                      [strengthened / provisional]
- In this pass the array is used as a hard `FF`-sentinel eligibility gate.
- Entries with `AEFF[X] == FF` are excluded from:
  - minimum selection
  - subtractive normalization
- Final gameplay-facing noun is still not frozen, so keep the label slightly provisional even though the gating role here is strong.

### 7E:99DD..7E:99DF  ct_visible_head_lane_readiness_current_export               [strengthened]
- Pass 51 already pinned this as current/fill export.
- Pass 54 proves the exported values are specifically the **post-normalized head work values**.

### 7E:9F22..7E:9F24  ct_visible_head_lane_readiness_goal_export                  [strengthened]
- Pass 51 already pinned this as goal/cap export in the gauge-facing path.
- Pass 54 proves this mirror copy at `B93B..B94F` receives the same **post-normalized head work values** in this initializer path.

---

## Provisional labels

### 7E:AFAB value `0`  ct_battle_slot_readiness_zero_special_state                [provisional]
- In this routine, zero values are:
  - excluded from minimum selection
  - excluded from subtractive normalization
  - preserved across the pass
- Strong structural meaning: not an active positive countdown participant.
- Final gameplay-facing noun still wants one more downstream confirmation.

### FD:B91B..FD:B939  ct_fd_subtract_selected_minimum_minus_one_from_active_positive_readiness_entries   [provisional]
- This is the arithmetic heart of the normalization routine.
- Useful as an internal sublabel if the disassembly later wants finer block labels.
- Semantics are already well understood; kept provisional only because the project has not yet frozen sub-block naming style consistently.

---

## Replaced / retired wording

### FD:B8F5..FD:B93A  ct_fd_normalize_head_readiness_work_before_visible_export    [replaced]
- Too vague after pass 54.
- Replaced by:
  - `ct_fd_normalize_active_battle_slot_readiness_to_minimum_one_before_head_export`

### “minimum/subtractive semantics unresolved”                                   [retired]
- No longer true after the byte-level decode of `B8F7..B939`.

---

## Exact arithmetic model now safe to carry forward

Selection phase:
```text
scan AFAB..AFB5
candidate must be:
  - nonzero
  - AEFF != FF
choose the smallest such value
```

Delta:
```text
delta = selected_minimum - 1
```

Apply phase:
```text
for each slot 0..10:
  if AEFF == FF -> skip
  if AFAB == 0  -> skip
  else AFAB -= delta
```

Postcondition:
```text
smallest eligible positive AFAB entry becomes 1
zeros remain 0
AEFF==FF entries remain unchanged
```

Export:
```text
AFAB..AFAD -> 99DD..99DF and 9F22..9F24
```

---

## Notes for next pass
- Trace producers/owners of `AEFF` hard enough to freeze its noun beyond “active-entry gate”.
- Re-check the later ready-transition helpers (`BDE0`, `BE50`, `BED0`) against the newly solved subtract-to-one normalization model.
- Look for the downstream consumer that distinguishes:
  - zero
  - one
  - larger positive readiness values
