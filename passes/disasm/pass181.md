# Pass 181 — C3:1AF0..C3:1BFF

## Objective
Continue forward from the weak `RTL` candidate at `1AF0` using the upgraded xref/anchor workflow and only promote a new seam when the local bytes look more coherent than the caller noise around them.

## Result
Closed:
- `C3:1AF0..C3:1BFF`

Next live seam:
- `C3:1C00..`

## Workflow used first
1. `detect_tiny_veneers_v1.py` on `C3:1AF0..C3:1BFF`
2. `scan_range_entry_callers_v1.py` on the same seam
3. manual follow-up on the strongest raw targets in the pocket (`1AF0`, `1B70`, `1BF7`, `1C00`)

## What changed
### `C3:1AF0..C3:1BFF`
Treated as:
- `ct_c3_inline_mixed_opcode_cluster_with_weak_rtl_stub_and_unstable_multi_target_pocket_before_1c00_candidate`

Why:
- the veneer detector found the obvious leading `RTL` at `1AF0` plus several small branch-pad patterns later in the pocket
- unlike the earlier `1880` case, `1AF0` does not have caller-quality evidence strong enough to justify promoting it as a real stub; its visible raw caller still lives in unresolved higher-bank `C3`
- `1B70` is not rescued either: its raw same-bank caller lands in the already frozen post-marker data region, which makes that target suspect rather than strong
- `1BF7` is the busiest raw target in this pocket because several same-bank `JMP` patterns converge there, but the local bytes around `1BF7` still do not stabilize into a trustworthy entry body under cautious inspection
- `1C00` is the first later target in-order whose local byte structure begins to read more coherently than the noisy lead-in, so the honest move is to freeze `1AF0..1BFF` and hand the next pass a cleaner candidate seam there

## Practical interpretation
This pass is another cleanup-forward move rather than a code-claim move.
The upgraded flow did exactly what it was supposed to do: it stopped weak caller patterns from turning a noisy pocket into fake executable structure, and it helped identify a better handoff seam at `1C00`.

## Next-pass caution
Resume at `C3:1C00`.
Treat it as a better-supported candidate seam, not yet as confirmed code.
The first job there is to decide whether the apparent coherence at `1C00` survives caller/context review or collapses into another mixed-content island.
