# Pass 191 — C3:2800..C3:28FF

## Objective
Continue forward from `C3:2800` using the upgraded xref/anchor workflow and only promote executable structure that survives both caller-quality review and local byte-level sanity checks.

## Result
Closed:
- `C3:2800..C3:28FF`

Next live seam:
- `C3:2900..`

## Workflow used first
1. raw caller review across `C3:2800..C3:28FF`
2. local byte inspection on the visible raw targets (`2802`, `2809`, `2813`, `2820`, `282D`, `2835`, `2848`, `288E`, `28B0`)
3. manual follow-up on the unsupported return-stub-looking bytes at `285A`, `286D`, and `287C`

## What changed
### `C3:2800..C3:28FF`
Treated as:
- `ct_c3_inline_branch_heavy_mixed_control_blob_with_double_low_bank_2809_hits_but_no_defendable_true_start_before_2900_candidate`

Why:
- this page produces more visible raw targets than the immediately previous page, but most of that support is still weak or caller-invalid under inspection
- the strongest caller pressure is into `2809`, which receives two same-bank `JSR` calls from low-bank `C3:0CC9` and `C3:0CF4`; those caller neighborhoods look substantially more code-like than the false data-side hits driving recent pages
- even so, `2809` still does not stabilize into a defendable routine start: the target opens directly into a branch-heavy control blob and quickly degrades into unsupported interior landings instead of a clean owner/helper body
- the other visible targets are worse: `2835` is only hit from obvious ASCII/text material at `C3:0EE1`, `282D` is only hit from a clearly mixed/data-side `JMP` at `C3:D4DF`, and the visible callers into `2802`, `2848`, `288E`, and `28B0` are either mixed-content or too structurally weak to rescue those starts
- the page does contain several lone return-looking bytes at `285A`, `286D`, and `287C`, but none of them has a caller-backed true start and all are embedded inside unstable mixed byte streams rather than forming defensible stubs or wrappers
- because the best caller-backed target (`2809`) is still structurally bad and the later return-looking splinters are unsupported interior bytes, the honest move is to freeze the whole `2800..28FF` page and advance to `2900`

## Practical interpretation
This pass is useful because it shows real improvement on the caller side without changing the structural verdict.
`2809` has better raw support than the false targets in the recent freeze streak, but the target bytes still do not hold up well enough to justify promotion.

## Next-pass caution
Resume at `C3:2900`.
Treat it only as the next in-order seam, not as solved code.
The first job there is to determine whether the post-`28FF` page finally contains a caller-backed start that holds up better than the rejected `2809` control blob.
