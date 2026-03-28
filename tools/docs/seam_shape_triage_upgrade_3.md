# Seam-shape triage upgrade 3

## Why this upgrade exists

Recent forward seam work kept hitting the same repeated judgment calls:

- raw outside pressure landing on obvious garbage first bytes like `00`, `02`, `60`, `6B`, `80`, or `FF`
- callers repeatedly landing inside already-proven dead territory like `C3:7A00..7FFF`
- hot interior targets that might only be the middle of a wider routine/control pocket
- multiple overlapping return-anchored splinters that are really one broader local cluster
- tiny wrappers that point into dead or non-owning territory
- pages that need a quick coarse family tag before deeper review

The earlier seam upgrades made caller context, local islands, and page-level risk more visible.
This upgrade pushes more of the repeated rejection logic into the toolkit so the same false dawns stop being argued by hand every pass.

## New files

### `tools/config/c3_dead_ranges_v1.json`
Registry for known dead seam lanes.

What it adds:
- a persistent place to record ranges already proven to be dead or zero-filled
- current seed entry for `C3:7A00..C3:7FFF`

Practical use:
- callers into proven dead territory can be auto-suppressed instead of wasting manual review time

### `tools/scripts/seam_triage_utils_v1.py`
Shared helper module for new seam scripts.

What it adds:
- bad-start byte classification
- dead-range loading and matching
- page metrics and page-family classification
- shared branch/call/return/stack-ish constants
- neighborhood helpers

Practical use:
- keeps the new seam tools consistent instead of duplicating heuristics

### `tools/scripts/classify_page_family_v1.py`
Coarse page-family classifier.

Families:
- `dead_zero_field`
- `text_ascii_heavy`
- `branch_fed_control_pocket`
- `mixed_command_data`
- `candidate_code_lane`

Practical use:
- fast first read of what kind of page you are in before spending time on targets

### `tools/scripts/score_raw_xref_context_v2.py`
Upgraded raw-xref scorer.

What it adds on top of v1:
- bad-start byte gate
- dead-lane suppression from the dead-range registry
- coarse page-family tagging in every hit record
- reason flags for why a hit was downgraded

Practical use:
- stop re-litigating false dawns that land on obviously bad first bytes
- auto-suppress callers into already-proven dead zones

### `tools/scripts/find_local_code_islands_v2.py`
Merged local-island finder.

What it adds on top of v1:
- overlapping / near-adjacent return-anchored windows are merged into broader local clusters
- cluster-level scores and child-window lists

Practical use:
- makes it obvious when several little splinters are really one larger local control pocket

### `tools/scripts/score_target_owner_backtrack_v1.py`
Owner-boundary backtracker.

What it adds:
- walks backward from each hot target to score nearby plausible true starts
- reports best candidate start, score, and distance back from the target

Practical use:
- helps separate interior-byte landings from plausible owner boundaries without forcing a full reread by hand

### `tools/scripts/detect_wrapper_target_quality_v1.py`
Wrapper-target quality checker.

What it adds:
- detects tiny `JSR/RTS` and `JSL/RTS` wrappers
- scores whether their targets land in dead lanes or on bad-start bytes

Practical use:
- stops tiny wrappers into garbage from being mistaken for evidence that the target lane is promotable

### `tools/scripts/run_c3_candidate_flow_v5.py`
New one-shot seam triage wrapper.

What it runs:
1. `classify_page_family_v1.py`
2. `detect_tiny_veneers_v1.py`
3. `scan_range_entry_callers_v2.py`
4. `score_raw_xref_context_v2.py`
5. `score_target_owner_backtrack_v1.py`
6. `find_local_code_islands_v2.py`
7. `detect_wrapper_target_quality_v1.py`

What it outputs:
- page family
- raw target count
- xref hit count
- strong/weak surviving xrefs
- dead-lane suppressed hit count
- hard/soft bad-start hit count
- owner-backtrack candidate count
- local island and cluster counts
- wrapper bad-target count
- review posture hint (`dead_lane_reject`, `bad_start_or_dead_lane_reject`, `local_control_only`, `manual_owner_boundary_review`, `mixed_lane_continue`)

Practical use:
- gives one quick seam summary that now includes both “why this is bad” and “where the nearest plausible owner boundary would even be”

## Additional beneficial upgrades that were folded in

Beyond the originally requested items, two more upgrades were worth doing immediately:

### 1) Dead-range registry
This was necessary because the same dead lanes were still consuming review time.
A config-backed registry makes those suppressions portable across passes.

### 2) Shared seam helper module
The new logic would have been duplicated across several scripts.
A shared helper makes future tuning much easier and keeps the scoring rules aligned.

## Recommended workflow now

For shaky forward pages:

1. run `run_c3_candidate_flow_v5.py`
2. check the coarse `page_family`
3. inspect downgraded xrefs from `score_raw_xref_context_v2.py`
4. inspect `score_target_owner_backtrack_v1.py` for plausible true-start boundaries
5. inspect merged local clusters from `find_local_code_islands_v2.py`
6. inspect wrapper target quality when tiny wrappers appear
7. only promote code when caller quality, start-byte quality, dead-range status, and local structure still agree
8. if they do not agree, freeze the page honestly and move the seam

## Honest limitation

These helpers are still heuristic.
They do **not** replace real semantic disassembly, control-flow recovery, or assembler-backed validation.
They exist to reduce repeated manual arguments over obvious false dawns and to make the seam reports sharper and faster.
