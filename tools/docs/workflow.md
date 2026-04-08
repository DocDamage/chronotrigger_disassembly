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
- derive next target with `find_next_callable_lane.py --rom "rom/Chrono Trigger (USA).sfc"`
- build anchor evidence with `build_call_anchor_report.py --rom "rom/Chrono Trigger (USA).sfc" --target C3:1817`
- classify uncertain bytes with `classify_c3_ranges.py --rom "rom/Chrono Trigger (USA).sfc" --range C3:1300..C3:13FF`
- perform the pass
- validate manifests with `validate_labels.py --manifests-dir passes/manifests`
- publish artifacts with `publish_pass_bundle.py --manifest path/to/pass.json --repo-root .`
- refresh generated bank progress with `update_bank_progress.py --bank C3`
- run `toolkit_doctor.py`

## Notes
- The stable entrypoints above now forward to the newest maintained implementations, so older session notes can keep using the historical command names.
- `update_bank_progress.py` writes a generated progress snapshot by default so it does not clobber the hand-curated tracked bank state files.
