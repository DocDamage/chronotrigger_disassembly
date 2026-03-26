# Chrono Trigger Labels - Pass 57

## Purpose
This file records the label upgrades justified by pass 57.

Pass 57 materially strengthens the `AF15.bit7` branch.
The new result is not just that bit 7 marks a canonical entry that is absent from the live tail map.
It now proves a **deferred selection + materialization** flow:

- flagged tail entries are collected into a candidate list
- multiple candidates are randomly reduced to one
- a later helper materializes the chosen canonical entry back into the live tail map and clears bit 7
- normal tail consumers/count gates ignore flagged entries

---

## Strong labels

### C1:AB03..C1:AB49  ct_build_withheld_tail_candidate_list_and_random_reduce_to_one  [strong]
- Scans all 8 tail entries.
- Collects slot indices with `AF15.bit7` set into `AECC`.
- Stores the candidate count in `AECB`.
- If `AECB >= 2`, uses the existing RNG helper at `AF22` to choose one candidate, stores it in `AECC[0]`, fills the rest of `AECC[1..]` with `FF`, and forces `AECB = 1`.
- This is a real deferred-tail candidate selector, not a generic scan.

### C1:AED3..C1:AEFB  ct_materialize_deferred_tail_entry_by_canonical_occupant_id      [strong]
- Scans tail slots `0..7`.
- Matches target occupant ID in `$0E` against the canonical tail map `AF0D[x]`.
- Requires that the live tail map `AF02[x]` does not already hold the same occupant.
- On match:
  - writes the occupant into `AF02[x]`
  - clears `AF15.bit7`
- On failure sets `AF24 = 1`.
- Strongest safe reading: explicit deferred-tail materialization helper.

### 7E:AF15 bit 7  ct_tail_deferred_materialization_flag                              [strengthened]
- Stronger than pass 56's “canonical present but not live” wording.
- Bit 7 now sits inside a proved selection/materialization flow:
  - collected by `AB03`
  - ignored by ordinary live-tail consumers
  - cleared by `AED3` when the entry is materialized into `AF02`
- Safest current noun: deferred / withheld-from-live tail materialization flag.

---

## Strong structural label upgrades

### C1:8C0A..C1:8C37  ct_iterate_live_unwithheld_tail_entries_for_dispatch             [strong]
- Consumes tail entries only when:
  - `AF15.bit7` is clear
  - `AF02[x] != FF`
  - `B2B6[x] == 0`
- Passes the live occupant ID in `AF02[x]` to `AFD2`.
- Confirms withheld entries are excluded from normal live-tail dispatch.

---

## Provisional-but-useful labels

### C1:9012..C1:9043  ct_gate_tail_dispatch_by_live_unwithheld_count                  [provisional]
- Counts tail entries where:
  - `AF02[x] != FF`
  - `AF15[x] == 0`
- Compares that count against a descriptor byte from `CC:[B1D2 + 1]`.
- Dispatches to `8C3E` on one compare outcome; otherwise sets `AF24 = 1`.
- The exact human-facing noun for the descriptor byte remains open, so this should stay provisional.

---

## Contextual notes (do not globalize yet)

### 7E:AECB / 7E:AECC  global labels should remain cautious
Earlier passes already proved these are reused as general selection/candidate scratch in multiple flows.
Pass 57 adds a new **contextual** use:

- in `AB03`, `AECC` temporarily holds withheld tail-slot indices
- in `AB03`, `AECB` temporarily holds the count of those withheld candidates

Do **not** rename them globally to only the withheld-tail meaning.

---

## Cautions still in force
Do **not** over-freeze the following yet:

1. the descriptor byte at `CC:[B1D2 + 1]` as specifically a min-count or max-count field
   - the compare/gate exists
   - the final noun still wants wrapper proof
2. `AF15.bit7` as a highly flavored gameplay term
   - the mechanical meaning is now strong
   - the exact scenario/use case still wants caller proof
3. `B2B6[x]` beyond “separate per-tail gate byte”
   - this pass proves it suppresses dispatch in `8C0A`
   - the exact state meaning remains open

---

## Suggested next seam
The best next continuation point after pass 57 is:

1. identify the callers that feed `$0E` before `ct_materialize_deferred_tail_entry_by_canonical_occupant_id`
2. identify which wrapper family owns `ct_build_withheld_tail_candidate_list_and_random_reduce_to_one`
3. then return to the earlier readiness seam with the stronger tail-state model in hand
