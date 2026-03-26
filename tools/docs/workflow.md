# Repo-First Workflow

## Branching
- `main` should stay mergeable and understandable
- live pass work happens on the active working branch
- toolkit upgrades should be committed clearly and not buried

## Pass discipline
Every pass should do all of the following before it is treated as complete:
1. close ranges honestly
2. write/update pass manifest
3. update bank progress index
4. run label validation
5. publish pass bundle into the repo
6. update workspace/completion snapshots

## Preferred sequence
- derive next target with `find_next_callable_lane.py`
- run `build_call_anchor_report.py`
- classify uncertain bytes with `classify_c3_ranges.py`
- perform the pass
- run `validate_labels.py`
- publish artifacts with `publish_pass_bundle.py`
- refresh `bank_c3_progress.json`
