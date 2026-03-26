# Chrono Trigger Labels - Pass 59

## Purpose
This file records the label corrections and upgrades justified by pass 59.

Pass 59 resolves the structural ownership problem left open in pass 58:

- `B8F3` is **not** a separate table candidate
- it is part of the already-live `AC14` dispatch table rooted at `B8BB`
- the pass-58 selector-wrapper family is now mapped to exact selector-control byte values

---

## Retired / corrected labels

### Retire
`C1:B8F3..C1:B92B  ct_selector_wrapper_table_candidate`

### Reason
This is no longer the correct structural model.
`B8F3` is not the start of an independent table.
It is the `0x1C` entry position inside the larger `AC14` dispatch table rooted at `B8BB`.

---

## Strong labels

### C1:B8BB..C1:B95F  ct_inline_selector_control_dispatch_table    [strong]
- Directly dispatched by `C1:AC2E  JSR ($B8BB,X)`.
- `X` is formed from the non-negative inline selector-control byte read by `AC14`.
- Proven table span in this pass runs from selector-control byte `0x00` through `0x52`.
- Includes the previously isolated pass-58 selector-wrapper family as the `0x27..0x38` subrange.

### C1:AC14..C1:AC45  ct_resolve_inline_selector_control_byte_into_selection_result    [strengthened]
- Reads the next selector-control byte from the CC stream.
- If negative, uses the preset path through `AED8`.
- Otherwise dispatches through `ct_inline_selector_control_dispatch_table`.
- Mirrors the resulting selection scratch from `AECC` into `AD8E` and records `B2AE = AECC`.

---

## Strong opcode-context upgrades inside the selector-control table

### selector-control `0x27..0x2E`  ct_fixed_single_entry_selector_wrappers_3_through_10    [strong]
- Exact control-byte mapping is now proved:
  - `0x27 -> AAAB`
  - `0x28 -> AAB6`
  - `0x29 -> AAC1`
  - `0x2A -> AACC`
  - `0x2B -> AAD7`
  - `0x2C -> AAE2`
  - `0x2D -> AAED`
  - `0x2E -> AAF8`

### selector-control `0x2F`  ct_build_withheld_tail_candidate_list_and_random_reduce_to_one    [strengthened]
- `AB03` is now not only structurally understood, but also placed at an exact selector-control byte value.

### selector-control `0x30..0x36`  ct_fixed_single_entry_selector_wrappers_0_through_6    [strong]
- Exact control-byte mapping is now proved:
  - `0x30 -> AB4E`
  - `0x31 -> AB59`
  - `0x32 -> AB64`
  - `0x33 -> AB6F`
  - `0x34 -> AB7A`
  - `0x35 -> AB85`
  - `0x36 -> AB90`

### selector-control `0x37`  ct_select_one_visible_entry_0_1_2_by_min_lane_value    [strengthened]
- `AB9B` now has an exact selector-control byte value.

### selector-control `0x38`  ct_build_live_tail_slot_candidate_list_and_random_reduce_to_one    [strengthened]
- `ABC9` now has an exact selector-control byte value.

---

## Important interpretation correction

### Old narrow label: “group-3 table at `B8BB`”
This wording is now too narrow.

What is directly proved is broader:
- `B8BB..B95F` is a selector-control dispatch table
- `AC14` uses it to resolve inline selector-control bytes
- the pass-58 wrapper family is simply one mid-table subrange

So future passes should stop describing `B8F3` as a separate table candidate.

---

## Still open

### `$0E` feeder into `AED3`
Pass 59 does **not** fully pin the wrapper that translates selected slot indices into the occupant ID consumed by `AED3`.

But the structural search space is now much smaller:
- ownership is confirmed under `AC14 -> B8BB`
- the best remaining candidate range is the late selector-control family:
  - `0x46..0x52`
  - `AFB6..B03A`

---

## Suggested next seam
1. decode selector-control bytes `0x39..0x52`
2. prioritize `0x46..0x52` because they are the strongest current bridge candidates toward deferred reinsertion semantics
3. then revisit the `$0E -> AED3` problem with the corrected one-table model
