# Chrono Trigger Tier-1 Revisit Audit — 2026-03-30

## Scope
This audit re-checked the Tier-1 revisit candidates from:
- `docs/handoffs/chrono_trigger_revisit_backlog_from_session15_notes.md`

Audited items:
- `C5:3600..36FF`
- `C5:4200..42FF`
- `C5:4387..438E` inside `C5:4300..43FF`
- `C5:4C00..4CFF`
- `C5:4821..482A` inside `C5:4800..48FF`
- `C5:5400..54FF`

Method used:
- fresh `run_c3_candidate_flow_v7.py` page scans
- fresh `score_target_owner_backtrack_v1.py` backtrack runs
- fresh `build_call_anchor_report_v3.py` anchor reports
- all runs used the repaired effective closed-range snapshot layer, so old weak/unresolved callers were re-scored against note-backed frozen pages

Bottom line:
- **none** of the Tier-1 candidates earned reopening
- the repaired snapshot made the evidence **stricter**, not looser
- every caller-backed Tier-1 target is now backed by **resolved-data / suspect** callers, not resolved-code callers

---

## High-Level Result

The important change since the earlier continuation notes is this:

Old interpretation:
- several Tier-1 candidates still had weak/unresolved caller support

Current interpretation after the snapshot bridge:
- those same callers now land inside already frozen note-backed pages
- they therefore downgrade to **`suspect / resolved_data`**
- no Tier-1 page gained a **`resolved_code`** caller

That means the revisit case is weaker than it looked when the backlog was first extracted.

---

## Candidate Findings

### `C5:3600..36FF`
- Current page family: `candidate_code_lane`
- Current posture: `local_control_only`
- Current target set: only `C5:36FF`
- Current caller support: `C5:8854 -> C5:36FF`, now **suspect / resolved_data** from `C5:8800..88FF`
- Current backtrack: `C5:36FC -> C5:36FF`, score `4`
- Byte-level blocker: target byte at `C5:36FF` is `8D` (`STA abs`), not a defensible owner start

Conclusion:
- this page no longer reads like an honest reopen candidate
- it has one suspect data-side caller and one backtrack alignment, but no resolved-code ingress and no good start byte

### `C5:4200..42FF`
- Current page family: `candidate_code_lane`
- Current posture: `local_control_only`
- Old posture from the continuation note: `manual_owner_boundary_review`
- Current targets: `C5:4200`, `C5:4208`
- Current caller support:
  - `C5:9CB2 -> C5:4200`, now **suspect / resolved_data** from `C5:9C00..9CFF`
  - `C5:C51B -> C5:4208`, now **suspect / resolved_data** from `C5:C500..C5:C5FF`
- Current backtracks:
  - `C5:4206 -> C5:4208`, score `6`
  - `C5:4200 -> C5:4200`, score `1`
- Byte-level blocker:
  - `C5:4200 = 0F` (`ORA long`)
  - `C5:4208 = F0` (`BEQ`)

Conclusion:
- this page is materially weaker than when it first entered the backlog
- the repaired caller-context layer removes the old weak/unresolved justification for a reopen
- the score-6 backtrack still does not rescue the bad start byte at `4208`

### `C5:4387..438E` inside `C5:4300..43FF`
- Current containing-page family: `candidate_code_lane`
- Current containing-page posture: `local_control_only`
- Current page-level target: `C5:43DB` only
- Current page-level caller support: `C5:12CC -> C5:43DB`, now **suspect / resolved_data** from `C5:1200..12FF`
- Current local cluster: `C5:4387..C5:438E`, cluster score `3`
- Exact caller audit for `C5:4387`: **0** valid callers
- Byte string at `C5:4387`: `20 F7 18 E3 1F 61 1F 60 ...`

Conclusion:
- the pocket still looks like a small executable splinter
- but it remains completely unsupported by direct callers
- because the containing page has no strong/weak ingress left, this island should stay closed unless exact new callers appear

### `C5:4C00..4CFF`
- Current page family: `branch_fed_control_pocket`
- Current posture: `mixed_lane_continue`
- Current targets: `C5:4C00`, `C5:4CDF`, `C5:4CFF`
- Current caller support:
  - `C5:DFF5 -> C5:4C00`, now **suspect / resolved_data** from `C5:DF00..DFFF`
  - `C5:3B9F -> C5:4CDF`, now **suspect / resolved_data** from `C5:3B00..3BFF`
  - `C5:135A -> C5:4CFF`, now **suspect / resolved_data** from `C5:1300..13FF`
- Current backtrack:
  - `C5:4C00 -> C5:4C00`, score `3`
- Byte-level blocker at page-top:
  - `C5:4C00` begins `62 91 7B 7B 9F FF 72 71 40 60 ...`
  - the old `RTI + RTS in the first 9 bytes` failure still stands

Conclusion:
- this remains the cleanest-looking Tier-1 page structurally
- but it still has zero resolved-code callers
- current evidence supports leaving it on the backlog, not reopening it

### `C5:4821..482A` inside `C5:4800..48FF`
- Current containing-page family: `candidate_code_lane`
- Current containing-page posture: `bad_start_or_dead_lane_reject`
- Current page targets: `C5:4805`, `C5:481E`, `C5:4837`, `C5:48C0`
- Current caller support:
  - `C5:EFF9 -> C5:4805`, now **suspect / resolved_data**
  - `C5:334C -> C5:481E`, now **suspect / resolved_data**
  - `C5:6576 -> C5:48C0`, now **suspect / resolved_data**
  - `C5:D0CF -> C5:4837`, now `suspect` anchor but `invalid` effective strength due `cop_barrier`
- Current local cluster: `C5:4821..C5:482A`, cluster score `3`
- Exact caller audit for `C5:4821`: **0** valid callers
- Byte string at `C5:4821`: `08 76 18 33 FB 25 66 9F 10 60 ...`

Conclusion:
- the island still has no direct caller support at all
- the containing page got worse under repaired caller scoring because its visible ingress is entirely suspect-only
- there is no evidence basis to reopen this pocket

### `C5:5400..54FF`
- Current page family: `candidate_code_lane`
- Current posture: `mixed_lane_continue`
- Current targets: `C5:543F`, `C5:54A2`, `C5:54C0`, `C5:54FF`
- Current caller support:
  - `C5:2268 -> C5:543F`, now **suspect / resolved_data** from `C5:2200..22FF`
  - `C5:D573 -> C5:54A2`, now **suspect / resolved_data** from `C5:D500..D5FF`
  - `C5:DE7C -> C5:54C0`, now **suspect / resolved_data** from `C5:DE00..DEFF`
  - `C5:18D3 -> C5:54FF`, now **suspect / resolved_data** from `C5:1800..18FF`
  - `C5:5293 -> C5:54FF`, now **suspect / resolved_data** from `C5:5200..52FF`
- Current backtracks:
  - `C5:543E -> C5:543F`, score `4`
  - `C5:549F -> C5:54A2`, score `4`
  - `C5:54F9 -> C5:54FF`, score `4`
  - `C5:54BE -> C5:54C0`, score `2`
- Byte-level blockers:
  - `C5:543F = D4` (`PEI`)
  - `C5:54A2 = 57` (not a function-entry style opcode)
  - `C5:54C0 = 8D` (`STA abs`)
  - `C5:54FF = DD` (`CMP abs,X`)

Conclusion:
- this page still looks clean by page metrics, but all visible support is now suspect-only
- the newly visible `54A2` candidate does not improve the page; its start byte is still not an owner prologue
- this remains backlog-only, not reopen-ready

---

## Audit Outcome

### Keep On Backlog
- `C5:4C00..4CFF`
- `C5:5400..54FF`

Reason:
- structurally they are still the cleanest Tier-1 pages
- but they still have no resolved-code callers

### Downgrade As Reopen Priorities
- `C5:3600..36FF`
- `C5:4200..42FF`
- `C5:4387..438E`
- `C5:4821..482A`

Reason:
- repaired caller-context scoring removed the old weak/unresolved ambiguity
- these now either collapse to suspect-only page support or still have zero direct callers

### Reopen Trigger Going Forward

Only reopen a Tier-1 candidate if one of these happens:
1. an exact target gains a **resolved-code** caller
2. an unsupported island gains a direct external caller
3. a later exact closure changes the nearby ownership graph enough to create genuine resolved-code ingress

Not enough:
- score-4 or score-6 backtracks by themselves
- suspect-only callers from pages already frozen as data
- local-island structure without external ingress

---

## Generated Audit Artifacts

Page-level audit files:
- `reports/c5_3600__c5_36ff_revisit_flow.json`
- `reports/c5_4200__c5_42ff_revisit_flow.json`
- `reports/c5_4300__c5_43ff_revisit_flow.json`
- `reports/c5_4800__c5_48ff_revisit_flow.json`
- `reports/c5_4c00__c5_4cff_revisit_flow.json`
- `reports/c5_5400__c5_54ff_revisit_flow.json`

Target/backtrack audit files:
- `reports/*_revisit_backtrack.json`
- `reports/C5_*_revisit_anchor.json`

These are intentionally separate from the original seam-history artifacts.
