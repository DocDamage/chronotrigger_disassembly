# Chrono Trigger Labels - Pass 61

## Purpose
This file records the architectural correction justified by pass 61.

Pass 61 proves that `C1:B80D` is the real master bank-C1 opcode dispatcher, and that the previously-carried command/selector tables are interior slices of that same master table.

It also corrects the provisional meaning of `B242[x]`.

---

## Strong labels

### C1:B80D..C1:B95F  ct_c1_master_opcode_dispatch_table                               [strong architectural]
- Root indexed `JSR` table used by the late-pack executor.
- Interior slices line up exactly with the previously solved local tables.
- Current proven slice offsets:
  - global `0x29..0x3F` -> `B85F..B88C`
  - global `0x40..0x52` -> `B88D..B8BA`
  - global `0x57..0xA9` -> `B8BB..B95F`

### C1:B85F..C1:B88C  ct_c1_group1_opcode_dispatch_slice                              [strong correction]
- Keep the useful local group-1 numbering from earlier passes.
- But this is now proved to be a slice entrypoint inside `ct_c1_master_opcode_dispatch_table`, not an independent root table.

### C1:B88D..C1:B8BA  ct_c1_group2_opcode_dispatch_slice                              [strong correction]
- Same correction as the group-1 table.
- Useful local numbering remains valid.
- Root ownership now belongs to `ct_c1_master_opcode_dispatch_table`.

### C1:B8BB..C1:B95F  ct_c1_inline_selector_control_dispatch_slice                    [strong correction]
- Same correction again for the selector-control table.
- `AC14` still dispatches here by local selector-control byte.
- But this slice is inside the same master dispatch table rooted at `B80D`.

### 7E:B242..7E:B249  ct_tail_last_executed_global_opcode_bytes                       [strong]
- Directly proved by:
  - `LDA B239`
  - `STA B242,X`
- Holds the per-tail last executed global opcode byte.
- This corrects the older provisional “nonzero result mark” read.

### C1:8C0A..C1:8CF7  ct_replay_tail_pack_segments_and_record_per_tail_state          [strong structural]
- Front-end clears/rebuilds per-tail replay state for the live, unwithheld tail map.
- Records executed global opcode bytes into `ct_tail_last_executed_global_opcode_bytes`.
- Records result/status bytes into `B24A[x]`.
- Records whether additional FE-delimited work remains into `B263[x]`.
- Advances/resumes execution from later CC bytes after segment completion.
- Proven to resume through the group-1 dispatch slice when the next resumed byte is non-negative.

---

## Strong label upgrades

### 7E:B239  ct_current_c1_master_opcode_byte                                         [strengthened]
- Previously carried as a late-pack subopcode byte.
- Pass 61 proves the stronger architectural read:
  - it is the current opcode byte fed into the master C1 dispatcher.
- In the late-pack flow, it is the current pack-sourced global opcode byte.

### 7E:B24A..7E:B251  ct_tail_last_opcode_result_status_bytes                         [strengthened]
- Pass 60 already proved these bytes capture `AF24` after execution.
- Pass 61 strengthens the surrounding controller context by pairing them directly with:
  - `ct_tail_last_executed_global_opcode_bytes`
  - `B263[x]`
- Best safe read now: per-tail last-op result/status bytes.

### 7E:B263..7E:B26A  ct_tail_has_additional_pack_segment_flags                       [strengthened]
- Still not fully finalized as a gameplay-facing noun.
- But pass 61 strengthens the structural role:
  - controller-managed per-tail flag/counter for whether later FE-delimited work remains after the current executed segment.

---

## Important corrections to older wording

### Do **not** keep calling `B80D` a dedicated late-pack subopcode table
That is now too narrow.

Use:
- **master C1 opcode dispatch table**

### Do **not** keep treating `B85F`, `B88D`, and `B8BB` as independent top-level root tables
They are still useful local slice entrypoints, but the stronger architectural ownership is now:
- all three are slices inside `ct_c1_master_opcode_dispatch_table`

### Do **not** keep the old provisional label for `B242[x]`
The bytes prove it stores the executed opcode byte itself, not a boolean/nonzero result mark.

---

## Best current architecture statement
The late-tail executor should now be described as:

- pointer-record selected (`CC:8B08`)
- FE/FF-delimited pack execution (`AFD7..B08E`)
- replay/control and per-tail state recording (`8C0A..8CF7`)
- all running over the shared `ct_c1_master_opcode_dispatch_table`

That is the cleanest carry-forward model after pass 61.

---

## Suggested next seam
1. decode the early global opcode band inside `ct_c1_master_opcode_dispatch_table`
2. pin the exact resume conditions that choose:
   - group-1 slice continuation
   - selector-control slice continuation
3. then re-open deferred-tail reinsertion from the corrected dispatcher model
