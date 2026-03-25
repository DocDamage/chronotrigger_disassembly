# Chrono Trigger Labels — Pass 67

## Purpose
This file records the label upgrades justified by pass 67.

Pass 67 closes the master-table seam immediately after global opcode `22`:

- exact alias run `23..28 -> 95FA`
- promotion of old group-1 local `00..06` into real global-master opcodes `29..2F`
- stronger bridge labels for the saved-seed writers feeding later seeded group-2 families

---

## Strong labels

### C1:9810..C1:9839  ct_global_opcode_29_persist_selected_head_and_inline_param_to_current_5e15_5e0d   [strong structural]
- Advances the stream, calls `AC14`, reads one inline byte, and stores:
  - `AEE5 -> 5E0D[current]`
  - `AECC[0] -> 5E15[current]`
- Strong bridge to later seeded group-2 opcode `01`.

### C1:983A..C1:98C3  ct_global_opcode_2A_2B_ordered_first_choice_persist_shared_body   [strong structural]
- Calls `AC14`.
- If multiple selected entries exist, collapses them to the first entry matching the external priority list in `B23A[0..7]`.
- Copies the chosen entry into `AECC[0]`.
- Then splits on `AEE3`:
  - non-`2` path persists into `5E0D[current] / 5E15[current]`
  - `2` path persists into `B16E[current]`
- Failure writes `B242[current] = FF` and `AF24 = 2`.

### C1:98C4..C1:98C4  ct_global_opcode_2C_rts_noop_alias   [strong]
- Exact single-byte `RTS`.

### C1:98C5..C1:995F  ct_global_opcode_2D_random_4way_stream_advance   [strong]
- Promoted global-master ownership of the already-solved group-1 random 4-way stream-control body.
- Uses RNG split ranges and `FD:BA4A`-driven stream advance.

### C1:9960..C1:9960  ct_global_opcode_2E_rts_noop_alias   [strong]
- Exact single-byte `RTS`.

### C1:9961..C1:9961  ct_global_opcode_2F_rts_noop_alias   [strong]
- Exact single-byte `RTS`.

---

## Exact opcode-alias entries

### Global `23..28`
All six master-table entries point directly to the existing opcode-`18` body at `C1:95FA`.

Carry-forward aliases:
- `23` = `ct_global_opcode_18_reduce_selected_entries_by_indirect_table_byte_equals_immediate`   [exact alias]
- `24` = same   [exact alias]
- `25` = same   [exact alias]
- `26` = same   [exact alias]
- `27` = same   [exact alias]
- `28` = same   [exact alias]

---

## Split labels inside the shared `2A/2B` body

### global opcode `2A`
Working global label:
- `ct_global_opcode_2A_reduce_selection_by_b23a_priority_then_persist_to_current_5e15_5e0d`   [strong structural]

Why:
- ordered-first-choice collapse through `B23A`
- stores chosen entry to `5E15[current]`
- stores one inline byte to `5E0D[current]`

### global opcode `2B`
Working global label:
- `ct_global_opcode_2B_reduce_selection_by_b23a_priority_then_persist_to_current_b16e`   [strong structural]

Why:
- ordered-first-choice collapse through `B23A`
- stores chosen entry to `B16E[current]`
- skips two stream bytes
- strong bridge to later seeded group-2 opcode `02`

---

## Important carry-forward notes

### `23..28`
Do not create six fake semantic labels here.
They are exact table aliases of opcode `18`.

### `2A/2B`
Do not flatten these into one final noun without mentioning the `AEE3` split.
The entrypoint is shared, but the persistent target differs in a way that matters:
- `5E15/5E0D`
- versus `B16E`

### `2D`
Do not leave this behind under old “group-1 opcode `04`” wording in later reports.
Its correct master-table identity is now:
- global opcode `2D`

---

## Suggested next seam
- promote / remap the rest of old group-1 local `07..16` into global `30..3F`
- then do the same ownership cleanup for old group-2 local `00..12` into global `40..52`
