# Pass 180 — C3:1A60..C3:1AEF

## Objective
Continue forward from `C3:1A60` using the upgraded xref/anchor workflow and only promote the parts of the seam that survive both the veneer scan and caller-context checks.

## Result
Closed:
- `C3:1A60..C3:1AD5`
- `C3:1AD6..C3:1ADA`
- `C3:1ADB..C3:1AEF`

Next live seam:
- `C3:1AF0..`

## Workflow used first
1. `detect_tiny_veneers_v1.py` on `C3:1A60..C3:1AEF`
2. `scan_range_entry_callers_v1.py` on the same seam
3. `build_call_anchor_report_v3.py` on the strongest-looking surviving targets (`1A60`, `1A7B`, `1AD6`, `1AF0`)

## What changed
### `C3:1A60..C3:1AD5`
Treated as:
- `ct_c3_inline_mixed_opcode_cluster_with_resolved_low_bank_call_targets_before_confirmed_0d0e_wrapper`

Why:
- the upgraded caller scan found two better raw entry candidates than the previous pass had: `1A60` from `C3:0CAA` and `1A7B` from `C3:0232`
- both caller sites live in already closed low-bank `C3` code, which makes those targets more interesting than the unresolved higher-bank pattern hits that dominated earlier seams
- even so, the local bytes from `1A60..1AD5` still do not settle into a trustworthy owner/helper breakdown under cautious inspection
- rather than inventing a shaky split simply because the callers look better, the lead-in cluster is frozen honestly as mixed opcode-looking content

### `C3:1AD6..C3:1ADA`
Treated as:
- `ct_c3_tiny_long_wrapper_calling_c30d0e_then_returning`

Why:
- the veneer detector flagged this slice cleanly
- the bytes are `JSL $C30D0E ; RTS`
- `C3:0D0E` lands inside the already closed `C3:0D0D..C3:0D5B` owner, so this wrapper is structurally much stronger than the surrounding bytes

### `C3:1ADB..C3:1AEF`
Treated as:
- `ct_c3_inline_table_like_data_block_after_0d0e_wrapper_before_unproven_rtl_stub_candidate`

Why:
- immediately after the confirmed veneer, the byte pattern shifts back into table-like inline material
- there is no defensible executable owner start before the `RTL` byte at `1AF0`
- freezing the post-wrapper block keeps the seam clean and hands the next pass a much smaller candidate boundary

## Practical interpretation
This is a good example of the upgraded workflow doing real work.
It did not magically turn the whole `1A60` pocket into a solved routine, but it did prevent overclaiming the unstable lead-in while extracting one real wrapper that can be defended cleanly.

## Next-pass caution
Resume at `C3:1AF0`.
It is tempting because the byte is `RTL`, but it should still be treated as only a weak candidate until the caller context is better than the current unresolved `C3:3FA6` hit.
