# Chrono Trigger Resume Checklist — `C6:E000..C6:E9FF`

## Current resume state
- working branch: `live-work-from-pass166`
- ROM: `rom/Chrono Trigger (USA).sfc`
- practical live seam: `C6:E000..`
- last continuation note in force: `docs/sessions/chrono_trigger_session15_continue_notes_55.md`
- last master handoff in force: `docs/handoffs/chrono_trigger_master_handoff_session16.md`
- last manifest-backed canonical state: `passes/manifests/pass191.json`
- effective closed-range snapshot after refresh: `tools/cache/closed_ranges_snapshot_v1.json`

Important reality:
- the continuation frontier is note-backed, not manifest-backed
- frozen continuation-note pages feed caller-context scoring through the seam snapshot layer
- the long run from `C5:3B00` through `C6:DFFF` has still produced **0 promotions**
- do **not** go into `C6:E000..E9FF` assuming the lane is about to turn clean

## Session goal
Process exactly one ten-page seam block:
- `C6:E000..C6:E9FF`

Acceptable outcomes:
- all ten pages freeze honestly and the seam advances to `C6:EA00..`
- one or more **narrow exact** splits survive, the rest of the block freezes honestly, and the seam still advances past the block

Unacceptable outcomes:
- page-wide or block-wide promotions driven only by weak callers
- promoting interior landings because backtrack score is high
- pretending the manifest layer is current past pass `191`

## Preflight checklist
Run these before manual page review:

```bash
python3 tools/scripts/audit_branch_state_v1.py
python3 tools/scripts/audit_pass_manifests_v1.py
python3 tools/scripts/ensure_seam_cache_v1.py --rom 'rom/Chrono Trigger (USA).sfc'
python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:E000 --pages 10 --json > reports/c6_e000_e9ff_seam_block.json
python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_e000_e9ff_seam_block.json --output reports/c6_e000_e9ff_seam_block.md
```

## Work order for the block
1. Read `reports/c6_e000_e9ff_seam_block.md` first.
2. Freeze obvious `bad_start_or_dead_lane_reject` and `local_control_only` pages quickly.
3. Only deep-read pages marked `manual_owner_boundary_review`.
4. For each manual-review page, run:
   ```bash
   python3 tools/scripts/score_target_owner_backtrack_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --range 'C6:XXXX..C6:XXFF' --json > reports/c6_xx00_xxff_backtrack.json
   ```
5. Run anchor reports only for targets that still look structurally defensible after byte review:
   ```bash
   python3 tools/scripts/build_call_anchor_report_v3.py --rom 'rom/Chrono Trigger (USA).sfc' --target C6:XXXX --manifests-dir passes/manifests --closed-ranges-snapshot tools/cache/closed_ranges_snapshot_v1.json --only-valid
   ```
6. If the page still collapses under weak-only callers, invalid overlap, or contaminated body bytes, freeze it and move on.

## Practical stop rule
Stop the session as soon as one of these is true:
- all ten pages are honestly frozen or split
- one narrow exact promotion is found and the rest of the block is still documented honestly
- the block yields no promotions and the new live seam is cleanly `C6:EA00..`

Do **not** stretch into the next block until this one is written up.

## Minimum outputs for this block
- `reports/c6_e000_e9ff_seam_block.json`
- `reports/c6_e000_e9ff_seam_block.md`
- any page-specific backtrack and anchor artifacts for manual-review pages
- `docs/sessions/chrono_trigger_session15_continue_notes_56.md`

## Writing rule for the note
The note should explicitly record:
- the block range
- whether promotions were zero or exact/narrow
- the strongest honest near-miss page
- the strongest reject signal in the block
- the new live seam after closure

## Manifest discipline
Do **not** create a new canonical pass manifest as part of this block.
Safe default:
- keep the work note-backed
- preserve the generated reports
- leave manifest backfill for a separate repo-state repair task
- rely on the refreshed seam snapshot for caller-context repair during active seam work
