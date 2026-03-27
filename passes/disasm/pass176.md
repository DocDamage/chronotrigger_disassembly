# Pass 176 — C3:17BD..C3:1816

## Objective
Correct the prior seam assumption around `17BD` and preserve forward progress without baking a false caller anchor into the repo.

## Result
Closed:
- `C3:17BD..C3:1816`

Next live seam:
- `C3:1817..`

## What changed
### `C3:17BD..C3:1816`
Treated as:
- `ct_c3_mixed_opcode_looking_inline_blob_without_valid_c3_callers_before_isolated_1817_entry_candidate`

Why:
- the prior pass note claimed a caller at `C4:CE36`, but that pattern is a same-bank `JSR $17BD` inside bank `C4`, so it targets `C4:17BD`, not `C3:17BD`
- re-audit found no valid direct `JSL/JML` hits to `C3:17BD` and no same-bank `C3` `JSR/JMP` hits either
- the bytes from `17BD..1816` remain strongly opcode-looking, but cautious inspection still does not produce one trustworthy executable owner with defensible entry proof
- because the structure is suggestive yet unanchored, the safer repo move is to freeze this span as mixed inline code-looking data instead of inventing fake code ownership

## Practical interpretation
This is a cleanup/correction pass.
It removes a bad anchor assumption from the forward narrative and keeps the project honest.
The bytes here may still contain real code fragments, but they are not secure enough yet to claim as a clean owner from the current evidence.

## Next-pass caution
The next seam is the already-isolated `C3:1817` lane.
Do not trust raw byte-pattern xrefs alone there either.
Re-validate the external-entry story from caller context before taking `1817` as a real entry owner.
