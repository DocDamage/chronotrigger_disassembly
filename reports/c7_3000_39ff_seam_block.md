# Seam block report — C7:3000 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 2, "candidate_code_lane": 3, "mixed_command_data": 5}`
- review postures: `{"bad_start_or_dead_lane_reject": 3, "local_control_only": 3, "manual_owner_boundary_review": 2, "mixed_lane_continue": 2}`

## Page breakdown

### `C7:3000..C7:30FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=6, xref_hits=6, strong_or_weak=3, hard_bad=1, soft_bad=0, clusters=1
- best targets: C7:3023 (weak, hits=1); C7:30B0 (weak, hits=1); C7:30EC (weak, hits=1)
- owner backtracks: C7:301B->C7:3023 (score=4); C7:30A0->C7:30B0 (score=4); C7:30E5->C7:30EC (score=4)
- local clusters: C7:30EC..C7:30FE

### `C7:3100..C7:31FF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:3120 (weak, hits=1); C7:31FE (weak, hits=1) [boundary_bait]; C7:3133 (suspect, hits=1)
- owner backtracks: C7:3110->C7:3120 (score=4); C7:312F->C7:3133 (score=2); C7:31F2->C7:31FE (score=2)
- local clusters: C7:31AD..C7:31B6

### `C7:3200..C7:32FF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=6, xref_hits=7, strong_or_weak=2, hard_bad=1, soft_bad=0, clusters=3
- best targets: C7:3222 (weak, hits=1); C7:32CE (weak, hits=1); C7:3258 (suspect, hits=2)
- owner backtracks: C7:32C2->C7:32CE (score=6); C7:321E->C7:3222 (score=4); C7:3250->C7:3258 (score=4)
- local clusters: C7:3282..C7:3292; C7:32B9..C7:32C7

### `C7:3300..C7:33FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=10, xref_hits=11, strong_or_weak=3, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:3312 (weak, hits=2); C7:330E (weak, hits=1); C7:33CF (weak, hits=1)
- owner backtracks: C7:3300->C7:330E (score=2); C7:3301->C7:3311 (score=2); C7:3302->C7:3312 (score=2)
- local clusters: none

### `C7:3400..C7:34FF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:34EE (weak, hits=1); C7:3402 (suspect, hits=1); C7:34DE (suspect, hits=1)
- owner backtracks: C7:34D8->C7:34DE (score=4); C7:3401->C7:3402 (score=2); C7:34DE->C7:34EE (score=2)
- local clusters: none

### `C7:3500..C7:35FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=3
- best targets: C7:350E (suspect, hits=1); C7:35CA (suspect, hits=1); C7:3524 (invalid, hits=1)
- owner backtracks: C7:3500->C7:350E (score=2); C7:3523->C7:3524 (score=2); C7:35C1->C7:35CA (score=2)
- local clusters: C7:354C..C7:3564; C7:3574..C7:358A

### `C7:3600..C7:36FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C7:36E3..C7:36EB

### `C7:3700..C7:37FF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=4
- best targets: none
- owner backtracks: none
- local clusters: C7:374A..C7:3769; C7:3729..C7:3741

### `C7:3800..C7:38FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=1, clusters=0
- best targets: C7:3816 (weak, hits=1); C7:38A3 (suspect, hits=1)
- owner backtracks: C7:3806->C7:3816 (score=2); C7:38A3->C7:38A3 (score=-6)
- local clusters: none

### `C7:3900..C7:39FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C7:39D3..C7:39EB
