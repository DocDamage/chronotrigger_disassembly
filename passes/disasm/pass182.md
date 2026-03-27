# Pass 182 — C3:1C00..C3:1FFF

## Objective
Continue forward from `C3:1C00` using the upgraded xref/anchor workflow and only promote executable structure that survives both local byte inspection and caller-context reality checks.

## Result
Closed:
- `C3:1C00..C3:1FFF`

Next live seam:
- `C3:2000..`

## Workflow used first
1. `detect_tiny_veneers_v1.py` on `C3:1C00..C3:1FFF`
2. `scan_range_entry_callers_v2.py` on the same seam
3. manual follow-up on the strongest-looking survivors and traps (`1C00`, `1C80`, `1DDF`, `1DFD`, `1E29`, `2000`)

## What changed
### `C3:1C00..C3:1FFF`
Treated as:
- `ct_c3_inline_mixed_control_table_false_entry_and_false_wrapper_cluster_before_2000_candidate`

Why:
- `1C00` does look more structured than the `1AF0..1BFF` lead-in, but its visible raw same-bank caller does not survive caller-context inspection cleanly enough to justify promoting a real owner start there
- the other early raw targets in the pocket (`1C80`, `1C83`, `1CAD`, `1CC4`, `1CC5`) land on unstable entry bytes and do not settle into trustworthy local starts under cautious inspection
- the veneer scan finds a tempting tiny wrapper shape at `1DDF..1DE2`, but it is false: the bytes read as `JSR $1150 ; RTL`, and `$1150` falls back into the already frozen post-marker data region rather than live executable structure
- the later `JSL ... ; RTS` shape at `1DFD..1E01` is also rejected as a false veneer signature because the long target is not backed by trustworthy executable context and the surrounding bytes remain unstable
- the apparent low-bank-looking raw hits to `1E29` collapse under manual review because the most tempting examples are produced by operand bytes inside already-plausible local instruction streams rather than by defensible opcode starts
- after the long mixed pocket is frozen honestly, `2000` is the next cleaner in-order seam to test instead of forcing a shaky split somewhere inside `1C00..1FFF`

## Practical interpretation
This pass is another conservative cleanup-forward move.
The upgraded workflow again did the right thing: it surfaced several tempting shapes, but local byte reality kept those shapes from turning into fake code claims.

## Next-pass caution
Resume at `C3:2000`.
Treat it as only the next better seam, not yet as solved code.
The first job there is to decide whether the early `2000` pocket survives caller/context review or whether it also collapses into another mixed-content cluster.
