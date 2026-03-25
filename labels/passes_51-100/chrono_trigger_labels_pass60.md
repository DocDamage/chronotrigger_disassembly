# Chrono Trigger Labels - Pass 60

## Purpose
This file records the label upgrades and caution corrections justified by pass 60.

Pass 60 proves that the late selector-control band is not simply “more selector wrappers.”
It opens a distinct **late selector-pack executor** centered on:

- `AFD7..B08E`
- `CC:8B08`
- `B4AA`
- `B80D`

It also tightens the caution around the mechanically parsed tail of the `B8BB` table.

---

## Strong labels

### CC:8B08..CC:8C53  ct_late_selector_control_pointer_records                          [strong structural]
- Indexed at 4-byte stride by the late selector-control family.
- `AFD7` proves the first word of each record is used as a pointer seed.
- For `0x49..0x52`, the first-word pointers land in `CC:A77B`, `A7E5`, `A8E5`, `A96A`, `AA1F`, `AAE2`, `ABB5`, `ACDD`, `AD5B`, and `ADFF`.
- The second word of each 4-byte record remains unresolved and should not be named yet.

### C1:AFD7..C1:B08E  ct_execute_late_selector_pack_and_capture_tail_result            [strong structural]
- Top-level late-family executor proved in this pass.
- Loads a pointer from `ct_late_selector_control_pointer_records`.
- Uses `B4AA` to select/adjust the current FE/FF-delimited segment.
- Reads the current sub-op byte into `B239`.
- Dispatches the sub-op through `B80D`.
- Optionally dispatches a second chained sub-op at `+4` when `B1CF != 0`.
- Captures the resulting `AF24` status into tail-local scratch/status arrays.
- May chain to another FE-delimited segment.

### 7E:B239  ct_current_late_selector_pack_subopcode                                  [strong]
- Loaded from `CC:[B1D2 + 0]` immediately before the `B80D` dispatch.
- This is the current sub-op byte executed by the late selector-pack executor.

### 7E:B1CF  ct_late_selector_segment_has_chained_second_subopcode_flag               [strong]
- Set when `CC:[current_segment + 4] != FE`.
- Governs whether the late executor dispatches a second 4-byte sub-op from `+4`.

---

## Strong label upgrades

### C1:B4AA..C1:B4E6  ct_select_tail_local_segment_within_late_selector_pack          [strengthened structural]
- Previously just an opaque helper reached from the late family.
- Pass 60 proves it is the segment-selection / pointer-adjust helper that sits between:
  - the pointer-record seed at `AFD7`
  - and the `B80D` sub-op dispatch.
- Exact gameplay-facing noun remains open, but “late selector pack segment selector” is now justified.

### 7E:B24A..7E:B251  ct_tail_late_selector_result_status_bytes                        [strengthened structural]
- `B24A[B252]` captures `AF24` after the current late-pack sub-op execution.
- The exact meaning of each result code is still open.
- Structural role as per-tail late-executor status capture is now strong.

---

## Provisional but useful labels

### 7E:B263..7E:B26A  ct_tail_late_selector_has_following_segment_flags                [provisional]
- Incremented when another FE-delimited segment is found and execution chains forward.
- Cleared when no following segment remains.
- Strongest safe reading so far: per-tail “has additional late-pack segment / chained segment present” flag or counter.

### 7E:B242..7E:B249  ct_tail_late_selector_nonzero_result_mark_bytes                  [provisional]
- Set to `FF` on the nonzero-`AF24` path inside `ct_execute_late_selector_pack_and_capture_tail_result`.
- Exact higher-level noun remains unresolved.

---

## Important caution corrections

### Do **not** globalize late selector-control bytes `0x46..0x48` as normal standalone handlers yet
Pass 60 shows these entries land in stack-sensitive/common-tail code without enough local setup to promote them as ordinary top-level selector-control handlers.

Keep them as:
- late-range alias candidates
- overrun candidates
- or context-dependent entrypoints

but **not** as globally promoted normal standalone selectors.

### Do **not** globalize late selector-control bytes `0x51..0x52` as normal standalone handlers yet
These land deep inside the status/continuation logic of the late-pack executor and are not yet justified as clean standalone top-level control bytes.

Keep them provisional.

---

## Interpretation upgrade

### Old broad reading from pass 59
“late selector-control range `0x46..0x52` is the best bridge candidate into `$0E -> AED3` reinsertion semantics”

### New stronger reading after pass 60
The late band instead opens a different subsystem seam:

- pointer-record lookup at `CC:8B08`
- FE/FF-delimited late-pack execution
- secondary sub-op dispatch through `B80D`
- per-tail result capture in `B24A/B242/B263`

So future passes should stop treating this band as the most likely direct reinsertion bridge.

---

## Suggested next seam
1. decode the `B80D` late-pack sub-op family
2. identify downstream consumers of `B24A`, `B242`, and `B263`
3. only then re-open the deferred-tail materialization search with this late-pack executor separated out cleanly
