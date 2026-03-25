# Chrono Trigger Labels — Pass 116

## Purpose

Pass 115 froze the sign/zero dispatcher at `C0:8A6C..8A9D`, but the eight selected bodies were still open.

Pass 116 closes the shared validator, the quick rejection helper, and the eight-body family structure without overclaiming the whole enclosing solver.

## Strong labels

### C0:8A9E..C0:8AB4  ct_c0_shared_candidate_validator_entry_with_70c0_gate_then_9ad3_9c37_path   [strong structural]
- Shared validator entry used by all eight downstream search bodies selected at `8A6C..8A9D`.
- Reads the candidate already staged in local `66/68` (through low bytes `67/68`).
- Calls exact helper `9AA1`.
- `9AA1` masks `67` by `1E`, indexes `7E:70C0`, and returns:
  - carry set when the table byte is nonnegative
  - carry clear when the table byte is negative
- On carry clear from `9AA1`, the body immediately returns failure.
- On carry set, the body runs exact shared path:
  - `9AD3`
  - `9C37`
- Returns with the later carry result still live.
- Strongest safe reading: shared candidate-validator entry with an early occupancy/class-table gate before a heavier classifier/final gate path.

### C0:9923..C0:99D9  ct_c0_shared_quick_nearby_slot_rejection_scan_over_candidate_pair_66_68   [strong structural]
- Shared helper called from the branch roots before the slower validator path.
- Loads exact slot-count byte `7F:2000`.
- Scans slot records backward in 2-byte steps.
- Skips entries whose `0F00,X` byte is zero.
- Skips:
  - current slot `0197`
  - exact slots `0199`
  - exact slot `019B`
- Checks exact flag bit `1B01,X.bit0`.
- Compares candidate pair `66/68` against slot coordinate words `1800/1880`.
- Reject condition is exact:
  - `abs(1880,X - 68) < 0x00E0`
  - `abs(1800,X - 66) < 0x00E0`
- Carry behavior is exact:
  - carry set = reject candidate
  - carry clear = no rejecting slot found
- Strongest safe reading: shared quick nearby-slot rejection scan over the current candidate coordinate pair.

### C0:8AB5..C0:916F  ct_c0_mirrored_candidate_search_family_over_current_slot_coords_1800_1880_and_signed_offset_pair_2e_30   [strong structural]
- Exact family selected by the sign/zero dispatcher at `8A6C..8A9D`.
- Collapses into:
  - two X-only / `30 == 0` roots
  - two Y-only / `2E == 0` roots
  - four full quadrant bodies when both `2E` and `30` are nonzero
- Shared exact mechanics across the family:
  - cache current slot coordinate words from `1800,X` and `1880,X`
  - build candidate pair in local `66/68`
  - fold signed working pair `2E/30` into those candidate words
  - use fixed bias constants `0x70`, `0x40`, and later `0x100`
  - call quick rejection helper `9923`
  - retry through shared validator entry `8A9E`
  - clear whichever working component(s) were consumed when a candidate is accepted
- Strongest safe reading: exact mirrored candidate-search family over current slot coordinates and the later signed offset pair.

### C0:8AB5..C0:8BF8  ct_c0_two_mirrored_x_only_candidate_search_roots_for_30_zero_case   [strong structural]
- Covers the two roots entered when `30 == 0`.
- Entry sign-marker seeds differ:
  - one clears `2F` and `31`
  - one sets `2F = 0xFF` and clears `31`
- Both roots:
  - use `2E` on the `1800` side
  - use fixed `1880`-side bias
  - try `9923` first
  - then retry through `8A9E`
- Strongest safe reading: exact mirrored X-only candidate-search roots for the zero-`30` case.

### C0:8BF9..C0:8E20  ct_c0_two_mirrored_y_only_candidate_search_roots_for_2e_zero_case   [strong structural]
- Covers the two roots entered when `2E == 0`.
- Entry sign-marker seeds differ:
  - one sets `31 = 0xFF` and clears `2F`
  - one clears both `31` and `2F`
- Both roots:
  - use `30` on the `1880` side
  - use fixed `1800`-side bias
  - try `9923` first
  - then retry through `8A9E`
- Strongest safe reading: exact mirrored Y-only candidate-search roots for the zero-`2E` case.

### C0:8E21..C0:916F  ct_c0_four_full_quadrant_candidate_search_bodies_for_nonzero_nonzero_2e_30_case   [strong structural]
- Covers the four roots used when both `2E` and `30` are nonzero:
  - `8E21..8EF0`
  - `8EF1..8FC0`
  - `8FC1..909B`
  - `909C..916F`
- Entry sign-marker seeds `2F/31` as one of the four exact combinations:
  - `00 / FF`
  - `FF / FF`
  - `FF / 00`
  - `00 / 00`
- All four bodies:
  - stage both `2E` and `30` into the initial candidate pair
  - use the same fixed bias vocabulary
  - call `9923`
  - then retry through `8A9E`
- Strongest safe reading: exact mirrored quadrant search family for the nonzero/nonzero case.

## Caution-strengthened locals

### 7E:012E  ct_c0_local_signed_candidate_offset_component_on_1800_coordinate_side_in_later_search_lane   [caution strengthened]
- Pass 115 proved `2A -> 2E` and that later helpers shift `2E`.
- Pass 116 proves the eight search bodies add exact local `2E` on the same coordinate side sourced from slot word `1800,X` when building candidate `66`.
- Strongest safe reading: signed candidate-offset component on the `1800` side of the later mirrored search lane.
- Honest limit: final player-facing noun of that offset is still open.

### 7E:0130  ct_c0_local_signed_candidate_offset_component_on_1880_coordinate_side_in_later_search_lane   [caution strengthened]
- Pass 115 proved `2B -> 30` and that later helpers shift `30`.
- Pass 116 proves the eight search bodies add exact local `30` on the same coordinate side sourced from slot word `1880,X` when building candidate `68`.
- Strongest safe reading: signed candidate-offset component on the `1880` side of the later mirrored search lane.
- Honest limit: final player-facing noun still open.

## Honest remaining gap

- I am intentionally **not** freezing the exact gameplay noun of the enclosing solver entry at `8820..8857`.
- I am intentionally **not** freezing the final meaning of sign-marker bytes `2F/31`.
- I am intentionally **not** freezing the exact gameplay noun of the `7E:70C0` table.
