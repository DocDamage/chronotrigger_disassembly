# Pass 172 — C3:1318..C3:13FB

## Objective
Take the first honest split inside the next open higher-bank callable lane instead of forcing `C3:1318..C3:1816` into one fake owner.

## Result
Closed:
- `C3:1318..C3:13F7`
- `C3:13F8..C3:13FB`

Next live seam:
- `C3:13FC..C3:1816`

## What changed
### `C3:1318..C3:13F7`
Treated as:
- `ct_c3_inline_mixed_control_dispatch_and_dma_setup_blob_preceding_tiny_eb7b_wrapper`

Why:
- the opening bytes do not stabilize as one credible owner under linear sweep
- several local slices look like partial control/dispatch fragments and hardware register setup rather than one contiguous callable body
- repeated decode breaks and mode-dependent nonsense show the same pattern seen in earlier bank `C3` mixed-content islands
- the region behaves more like an inline mixed blob than a clean owner/helper family

### `C3:13F8..C3:13FB`
Treated as:
- `ct_c3_tiny_local_wrapper_calling_eb7b_then_returning`

Why:
- this subrange resolves cleanly as a tiny wrapper veneer
- linear decode gives `JSR $EB7B` followed by `RTS`
- this is the first small executable closure in the lane that is structurally clean enough to take without overclaiming the surrounding bytes

## Practical interpretation
The handoff warning was correct.
This higher lane opens with mixed content, not with a nice monolithic owner.
The cautious move here was to freeze the messy opening blob honestly and only split out the tiny local wrapper that is actually clean.

## Next-pass caution
`C3:13FC..C3:148B` still looks table-heavy / mixed.
Do not assume the next bytes are one straight executable owner just because the seam advanced.
