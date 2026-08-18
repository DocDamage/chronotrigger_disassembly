# Chrono Trigger Resume Checklist — `C5:3B00..C5:44FF`

## Current resume state
- working branch: `live-work-from-pass166`
- ROM: `rom/Chrono Trigger (USA).sfc`
- practical live seam: `C5:3B00..`
- last continuation note in force: `chrono_trigger_session15_continue_notes_13.md`
- last manifest-backed canonical state: `passes/manifests/pass191.json`

Important reality:
- do **not** trust `README.md` for the live seam; it is stale
- do **not** treat the old completion percentage as a decision input here; the later continuation notes explicitly mark it as saturated
- do **not** pretend the manifest layer is current past pass `191`

## Session goal
Process exactly one ten-page block:
- `C5:3B00..C5:44FF`

Primary question:
- does anything inside `C5:4000..C5:43FF` survive as a real owner/helper split once caller quality, start-byte quality, and local structure are checked together?

Acceptable outcomes:
- no promotions survive, the whole block is frozen honestly, and the live seam advances to `C5:4500..`
- one or more **narrow exact** splits survive inside `C5:4000..43FF`, the rest of the block is frozen honestly, and the live seam still advances past the block

Unacceptable outcomes:
- broad page-wide promotions driven only by weak callers from unresolved pages
- promoting an interior landing because the page is hot
- reopening already-preserved near-miss territory from earlier `C5` notes unless new evidence actually appears

## Preflight checklist
Run these before manual page review:

```bash
python3 tools/scripts/audit_branch_state_v1.py
python3 tools/scripts/audit_pass_manifests_v1.py
python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:3B00 --pages 10 --json > reports/c5_3b00_44ff_seam_block.json
python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_3b00_44ff_seam_block.json --output reports/c5_3b00_44ff_seam_block.md
```

Targeted anchor checks for the current best-looking entries:

```bash
python3 tools/scripts/build_call_anchor_report_v3.py --rom 'rom/Chrono Trigger (USA).sfc' --target C5:4098 --manifests-dir passes/manifests --only-valid
python3 tools/scripts/build_call_anchor_report_v3.py --rom 'rom/Chrono Trigger (USA).sfc' --target C5:40F0 --manifests-dir passes/manifests --only-valid
python3 tools/scripts/build_call_anchor_report_v3.py --rom 'rom/Chrono Trigger (USA).sfc' --target C5:4192 --manifests-dir passes/manifests --only-valid
python3 tools/scripts/build_call_anchor_report_v3.py --rom 'rom/Chrono Trigger (USA).sfc' --target C5:4208 --manifests-dir passes/manifests --only-valid
python3 tools/scripts/build_call_anchor_report_v3.py --rom 'rom/Chrono Trigger (USA).sfc' --target C5:43DB --manifests-dir passes/manifests --only-valid
```

## Work order for the block
1. Freeze-likely pages first so time does not get burned on obvious reject territory.
2. Deep-read the three manual-review pages in priority order:
   - `C5:4200..42FF`
   - `C5:4000..40FF`
   - `C5:4100..41FF`
3. Treat `C5:4300..43FF` as carry-forward review only after the three pages above.
4. Close `C5:4400..44FF` last unless earlier review unexpectedly points into it.

## Page-by-page decision criteria

### `C5:3B00..C5:3BFF`
- current posture: `bad_start_or_dead_lane_reject`
- default action: freeze the page
- inspect only these pockets before freezing:
  - `C5:3B7D..C5:3B98`
  - `C5:3BCD..C5:3BE8`
- only promote if:
  - one of those ranges gives a clean top boundary
  - the candidate is **not** just an interior landing for `C5:3B7E` or `C5:3B80`
  - the body reads as coherent code rather than ASCII-heavy or local-control splinter material
- freeze immediately if:
  - the hard-bad-start finding still holds
  - the best support is still only the weak unresolved caller into `C5:3B7E`
  - the `C5:3B83..C5:3B89` pocket still looks like bait rather than a true start

### `C5:3C00..C5:3CFF`
- current posture: `bad_start_or_dead_lane_reject`
- default action: freeze the page
- inspect only these entry ideas before freezing:
  - `C5:3C10`
  - `C5:3C18`
  - `C5:3CB9..C5:3CDC`
- only promote if:
  - `C5:3C10` or `C5:3C18` survives as a real start rather than a hot interior byte
  - the page no longer collapses under the existing hard-bad and soft-bad starts
  - the later `C5:3CC4` lure clearly resolves as downstream body and not a separate data-side trap
- freeze immediately if:
  - hard-bad or soft-bad start pressure remains visible
  - all backtracks stay weak score-2 material
  - `C5:3C97..C5:3C9F` still reads as local control only

### `C5:3D00..C5:3DFF`
- current posture: `local_control_only`
- default action: freeze as local control / mixed content
- only inspect:
  - `C5:3D62..C5:3D67`
  - `C5:3D93..C5:3DAE`
- only promote if:
  - a resolved caller appears into a clean start
  - the page stops looking like unsupported local-control islands
- otherwise freeze without spending more time here

### `C5:3E00..C5:3EFF`
- current posture: `local_control_only`
- default action: freeze as local control / mixed content
- only inspect:
  - `C5:3E00`
  - `C5:3EF4..C5:3EFF`
- only promote if:
  - either location proves to be a true page-top or near-page-top owner with real outside support
  - the `C5:3E09..C5:3E13` and `C5:3E9A..C5:3EA1` islands stop looking like isolated control fragments
- otherwise freeze quickly

### `C5:3F00..C5:3FFF`
- current posture: `bad_start_or_dead_lane_reject`
- default action: freeze the page
- inspect only:
  - `C5:3F00`
  - `C5:3F38..C5:3F57`
  - `C5:3FEB..C5:3FFF`
- only promote if:
  - `C5:3F00` is a real owner boundary, not just a hot page-top bait byte
  - the hard-bad-start finding goes away under byte review
  - the page proves cleaner than the current single weak caller suggests
- freeze immediately if:
  - `C5:3F00` still reads as bait
  - the `C5:3FA7..C5:3FB1` cluster is still the cleanest thing on the page

### `C5:4000..C5:40FF`
- current posture: `manual_owner_boundary_review`
- default action: deep manual read
- inspect in this order:
  - `C5:40D6..C5:40F0`
  - `C5:405C..C5:4079`
  - `C5:405F..C5:4087`
  - page-top lead-in `C5:4000..C5:401B`
- caller-backed targets to reconcile:
  - `C5:4098`
  - `C5:40F0`
  - lower-value heat at `C5:4006`, `C5:4008`, `C5:400B`
- only promote if:
  - one exact start explains both the local backtrack and at least one caller landing
  - the chosen start is not just an interior landing inside the `C5:4052..4063` local-control area
  - the body after the start is coherent enough to justify a real owner/helper claim
- freeze the page if:
  - `C5:4098` and `C5:40F0` still resolve to unrelated or interior starts
  - the support remains only weak callers from unresolved pages
  - the page stays hot but fragmented

### `C5:4100..C5:41FF`
- current posture: `manual_owner_boundary_review`
- default action: deep manual read after `C5:4000..40FF`
- inspect in this order:
  - `C5:4191..C5:41AA`
  - `C5:4120..C5:4138`
  - `C5:41DA..C5:41F7`
- caller-backed targets to reconcile:
  - `C5:4192`
  - `C5:4120`
  - secondary suspect `C5:41DF`
- only promote if:
  - `C5:4191` or `C5:4120` is a defensible top boundary with a coherent body
  - the page remains clean under byte review instead of collapsing into mixed local control
  - the start survives without relying on unresolved-caller wishful thinking
- freeze the page if:
  - `C5:4192` remains only a one-byte interior landing
  - `C5:413A..414A` and `C5:41A6..41AE` continue to dominate the page as small islands

### `C5:4200..C5:42FF`
- current posture: `manual_owner_boundary_review`
- default action: highest-priority deep manual read in the block
- inspect in this order:
  - `C5:4206..C5:4220`
  - `C5:422F..C5:4239`
  - `C5:4288..C5:428C`
- caller-backed targets to reconcile:
  - `C5:4208`
  - `C5:4200`
- only promote if:
  - `C5:4206` or `C5:4208` is a true start rather than a page-top bait continuation
  - the score-6 backtrack survives full byte review
  - the wrapper-bad-target warning resolves harmlessly
  - the page forms one real owner/helper body rather than a stack of local clusters
- freeze the page if:
  - `C5:4208` remains only weakly anchored from unresolved caller `C5:C51B`
  - the page breaks back down into local cluster fragments
  - the `C5:422F..4239` and `C5:4288..428C` pockets look better than the supposed main start

### `C5:4300..C5:43FF`
- current posture: `mixed_lane_continue`
- default action: carry-forward review only after the three manual-review pages above
- inspect only:
  - `C5:43D9..C5:43F3`
  - `C5:4387..C5:438E`
- only promote if:
  - `C5:43DB` proves to be a real clean start with better byte structure than `C5:4000..42FF`
  - the body is coherent enough to justify a promotion despite the single weak caller
- otherwise keep it as the least-bad carry-forward page and move on

### `C5:4400..C5:44FF`
- current posture: `local_control_only`
- default action: freeze as local control / mixed content
- only inspect:
  - `C5:44BF..C5:44D8`
  - `C5:44D6..C5:44E1`
- only promote if:
  - some earlier page review produces resolved caller support into this page
  - the page stops behaving like a local-control tail
- otherwise freeze without extended analysis

## Practical session stop rule
Stop the session as soon as one of these is true:
- all ten pages are honestly frozen or split
- one narrow exact promotion is found and the remainder of the block is still classifiable
- the block clearly yields no promotion and the next seam is cleanly `C5:4500..`

Do **not** stretch the session into `C5:4500..` unless the entire block is already documented and written up.

## Output checklist for this session
Minimum required outputs:
- `reports/c5_3b00_44ff_seam_block.json`
- `reports/c5_3b00_44ff_seam_block.md`
- `chrono_trigger_session15_continue_notes_14.md`

Recommended content if there is **no** surviving promotion:
- state that `C5:3B00..C5:44FF` was closed conservatively
- identify the strongest honest near-miss page of the block
- identify the hottest trap page of the block
- set new live seam to `C5:4500..`

Recommended content if there **is** a surviving promotion:
- record the exact split range
- explain why the start survived both caller and byte review
- freeze the remainder of the page/block honestly
- set new live seam to the first unresolved byte after the closed block

## Manifest discipline for this session
Do **not** write a new canonical manifest unless you also decide how to bridge the missing pass history between manifest-backed pass `191` and the later continuation-note frontier.

For this session, the safe default is:
- keep the work note-based
- preserve the generated block report
- leave manifest reconciliation as a separate repo-state repair task

## Pass-note template
Use this exact skeleton for `chrono_trigger_session15_continue_notes_14.md`:

```md
# Chrono Trigger continuation notes after Session 15 handoff — pass set 14

## What was done
- Resumed at the live seam **`C5:3B00..`**.
- Swept one additional 10-page ROM-first seam block:
  - `C5:3B00..C5:44FF`
- Kept the same conservative rule: no code promotion without caller quality, start-byte quality, and local structure all converging.
- Result: **[no new promotions / exact split at ...]**

## Method note
- Manifest-backed canonical state still stops earlier, so this continuation remains note-backed.
- Used:
  - `reports/c5_3b00_44ff_seam_block.json`
  - `reports/c5_3b00_44ff_seam_block.md`
  - targeted `build_call_anchor_report_v3.py` checks for the strongest candidate entries
- Same rule as before: weak callers from unresolved pages are not enough by themselves.

## Why this block did or did not promote code
- `C5:4000..40FF` — [summary]
- `C5:4100..41FF` — [summary]
- `C5:4200..42FF` — [summary]
- `C5:4300..43FF` — [summary]
- `C5:3B00..3FFF` and `C5:4400..44FF` — [freeze summary]

## Most important near-miss / trap pages
- strongest honest near-miss: **`[page]`**
- hottest trap page: **`[page]`**
- dirtiest poison page: **`[page]`**

## Seam movement
- Previous live seam: `C5:3B00..`
- Newly swept through: `[range closed this session]`
- New live seam: **`[next seam]`**

## Pass / completion estimate
- Previous latest completed pass estimate: **721**
- New latest completed pass estimate: **[estimate if still being tracked]**
- Completion estimate: **do not treat the old coarse metric as reliable without rescoping**

## Recommended next move
1. Resume at `[next seam]`.
2. Preserve `[near-miss pages]` as reference territory only.
3. Do not let heat alone force an early promotion.
```
