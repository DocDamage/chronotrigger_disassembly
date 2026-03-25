# Chrono Trigger Labels - Pass 58

## Purpose
This file records the label upgrades justified by pass 58.

Pass 58 does **not** fully pin the final caller chain into `AED3`.
But it materially improves ownership:

- `AB03` is no longer an orphan helper
- it belongs to a real late local selector-wrapper family
- `ABC9` is now proved as its live-tail sibling
- two fixed single-entry selector-wrapper runs are now obvious
- the pointer run at `B8F3` is strong enough to label provisionally

---

## Strong labels

### C1:ABC9..C1:AC13  ct_build_live_tail_slot_candidate_list_and_random_reduce_to_one    [strong]
- Scans the unified live occupant map starting at slot index `3`.
- Uses `B252 + 3` as the upper live-tail bound.
- Appends non-`FF` live slot indices into `AECC`.
- If multiple candidates exist, uses `AF22` to choose one and exposes the chosen slot at `AECC[0]`.
- Forces `AECB = 1`.
- Strong structural sibling to pass 57's `AB03`, but over the live-tail side.

### C1:AAAB..C1:AAF8  ct_fixed_single_entry_selector_wrappers_3_through_10               [strong]
- Family of tiny wrappers:
  - `AECC = literal`
  - `AECB = 1`
  - `RTS`
- Covered literal values: `3..10`.

### C1:AB4E..C1:AB90  ct_fixed_single_entry_selector_wrappers_0_through_6                [strong]
- Family of tiny wrappers:
  - `AECC = literal`
  - `AECB = 1`
  - `RTS`
- Covered literal values: `0..6`.

---

## Strong structural label upgrades

### C1:AB9B..C1:ABC8  ct_select_one_visible_entry_0_1_2_by_min_lane_value               [strong structural]
- Compares three lane-local values:
  - `5E30`
  - `5EB0`
  - `5F30`
- Selects exactly one visible entry index:
  - `0`, `1`, or `2`
- Stores that selected entry into `AECC`
- Forces `AECB = 1`
- Exact branch polarity / final gameplay noun should still stay cautious, but the structural selector role is now strong.

### C1:AED3..C1:AEFB  ct_materialize_deferred_tail_entry_by_canonical_occupant_id      [strengthened context]
- Keep the pass-57 label.
- Pass 58 strengthens the context:
  - this helper is **not** the only tail materialization path
  - it is best treated as the **occupant-ID keyed deferred reinsertion helper**
  - slot-indexed materializers exist elsewhere (`9E78`, `86BC` style copy path)

---

## Provisional labels

### C1:B8F3..C1:B92B  ct_selector_wrapper_table_candidate                               [provisional]
- Coherent pointer run of 29 entries:
  - dynamic selector wrappers
  - fixed single-entry wrappers
  - `AB03`
  - `AB9B`
  - `ABC9`
- Strongly looks like a real local selector-wrapper table.
- The dispatch site into this table is still not pinned, so keep this provisional.

### C1:AB03..C1:AB49  ct_build_withheld_tail_candidate_list_and_random_reduce_to_one    [context strengthened]
- Keep the pass-57 label.
- Pass 58 now places it inside the same selector-wrapper family as:
  - fixed single-entry wrappers
  - the visible-slot min selector
  - the live-tail selector at `ABC9`

---

## Important corrections / caution notes

### `AECC` tail clearing in `AB03` / `ABC9`
Do **not** keep over-claiming that these routines necessarily clear the whole remainder of `AECC[1..]`.

What is definitely proved is:
- chosen result -> `AECC[0]`
- one following `FF` write
- `AECB = 1`

Because `AECB = 1`, the rest of the scratch entries are no longer semantically live anyway.

### `B8F3` should not yet be renamed as a confirmed CC-stream command table
This pass proves a coherent pointer family.
It does **not** yet prove a dispatcher equivalent to:
- `874E -> B80D`
- `8CE7 -> B85F`
- `8D88 -> B88D`
- `AC2E -> B8BB`

So keep `B8F3` as a selector-wrapper table **candidate** until the entry path is pinned.

---

## Suggested next seam
The best next continuation point after pass 58 is:

1. pin the real dispatcher into `ct_selector_wrapper_table_candidate`
2. trace which wrapper translates `AECC`-style selected slot indices into `$0E`
3. then revisit deferred-tail reinsertion with that stronger wrapper-family model
