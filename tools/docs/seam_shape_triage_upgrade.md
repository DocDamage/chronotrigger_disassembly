# Seam-shape triage upgrade

## Why this upgrade exists

Recent conservative C3 passes exposed three repeated review problems that were still too manual:

- raw xrefs landing from caller neighborhoods that are really text, table, or script-like inline data
- local helper-looking islands ending in `RTS` / `RTL` that look promising but have no caller-backed true start
- pages that feel more executable than pointer tables, yet still fail because the caller side and the local byte side disagree

The older repo-native xref upgrade already solved bank-mismatch mistakes and made caller provenance visible.
This upgrade adds two new lightweight triage helpers to make page-level rejection faster and more explicit.

## New scripts

### `tools/scripts/score_raw_xref_context_v1.py`
Scores every raw incoming hit into a seam using neighborhood heuristics around both the caller and the target.

What it adds:
- printable ASCII ratio around the caller and target
- `00` / `FF` density around the caller and target
- repeated little-endian pair score for spotting pointer/table-like neighborhoods
- caller-side and target-side data-risk labels (`low`, `medium`, `high`, `very_high`)
- downgraded `effective_strength` that can demote a nominally interesting xref when the bytes around it still look data-side

Practical use:
- reject false hits like text-side `JSR` / `JMP` patterns faster
- separate truly caller-backed starts from xrefs that only look strong on paper

### `tools/scripts/find_local_code_islands_v1.py`
Scans a seam for return-anchored local islands that look more executable than the surrounding bytes.

What it adds:
- identifies local windows that terminate in `RTS`, `RTL`, or `RTI`
- scores branch density, call density, stack-ish setup bytes, and barrier bytes
- penalizes ASCII-heavy and repeated-pair-heavy windows
- surfaces unsupported helper/stub candidates for manual follow-up instead of forcing a full page reread

Practical use:
- quickly surface pockets like unsupported helper islands ending in a lone return opcode
- make it easier to say "this page has a real-looking splinter, but it is still unsupported" without rediscovering that by hand every time

### `tools/scripts/run_c3_candidate_flow_v2.py`
One-shot seam triage wrapper.

What it runs:
1. `detect_tiny_veneers_v1.py`
2. `scan_range_entry_callers_v2.py`
3. `score_raw_xref_context_v1.py`
4. `find_local_code_islands_v1.py`

What it outputs:
- raw target count
- xref hit count
- effective strong/weak hit count after context downgrades
- suspect-hit count
- local island count
- tiny-veneer count

Practical use:
- fast first-pass triage for mixed `C3` seams before deeper manual inspection

## Recommended workflow now

For shaky forward pages:

1. run `run_c3_candidate_flow_v2.py`
2. inspect downgraded xrefs from `score_raw_xref_context_v1.py`
3. inspect any surfaced local islands from `find_local_code_islands_v1.py`
4. only promote code when caller quality and local structure still agree
5. if they disagree, freeze the page honestly and move the seam

## Honest limitation

These helpers are still heuristic.
They do **not** replace real disassembly semantics, control-flow recovery, or assembler-backed verification.
They are meant to reduce wasted manual time on obviously bad caller neighborhoods and unsupported local splinters, not to auto-label code.
