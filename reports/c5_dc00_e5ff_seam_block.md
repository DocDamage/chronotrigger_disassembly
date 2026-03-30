# Seam block report — C5:DC00 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 5, "candidate_code_lane": 5}`
- review postures: `{"bad_start_or_dead_lane_reject": 5, "local_control_only": 1, "manual_owner_boundary_review": 3, "mixed_lane_continue": 1}`

## Page breakdown

### `C5:DC00..C5:DCFF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=1, soft_bad=0, clusters=5
- best targets: C5:DCBC (weak, hits=1); C5:DC00 (invalid, hits=1)
- owner backtracks:  (score=6);  (score=-4)
- local clusters: C5:DC49..C5:DC55; C5:DCCF..C5:DCDD

### `C5:DD00..C5:DDFF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=3
- best targets: C5:DD0F (weak, hits=1); C5:DD1F (weak, hits=1)
- owner backtracks:  (score=3);  (score=3)
- local clusters: C5:DD1F..C5:DD2D; C5:DD40..C5:DD4A

### `C5:DE00..C5:DEFF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=2
- best targets: C5:DE1C (weak, hits=1); C5:DEA2 (weak, hits=1); C5:DE02 (suspect, hits=1)
- owner backtracks:  (score=4);  (score=2);  (score=2)
- local clusters: C5:DE2B..C5:DE3E; C5:DECF..C5:DED7

### `C5:DF00..C5:DFFF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=6, xref_hits=7, strong_or_weak=3, hard_bad=1, soft_bad=2, clusters=0
- best targets: C5:DF0B (weak, hits=1); C5:DF23 (weak, hits=1); C5:DF71 (weak, hits=1)
- owner backtracks:  (score=6);  (score=5);  (score=3)
- local clusters: none

### `C5:E000..C5:E0FF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=10, xref_hits=15, strong_or_weak=11, hard_bad=1, soft_bad=0, clusters=6
- best targets: C5:E01F (weak, hits=3); C5:E020 (weak, hits=3); C5:E000 (weak, hits=2)
- owner backtracks:  (score=6);  (score=6);  (score=6)
- local clusters: C5:E0BE..C5:E0C2; C5:E021..C5:E02D

### `C5:E100..C5:E1FF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=2, soft_bad=0, clusters=4
- best targets: C5:E132 (invalid, hits=1); C5:E1E0 (invalid, hits=1)
- owner backtracks:  (score=-2);  (score=-2)
- local clusters: C5:E117..C5:E11D; C5:E158..C5:E160

### `C5:E200..C5:E2FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=1, soft_bad=0, clusters=3
- best targets: C5:E2C0 (weak, hits=1); C5:E2F3 (invalid, hits=1)
- owner backtracks:  (score=4);  (score=2)
- local clusters: C5:E201..C5:E21E; C5:E2C2..C5:E2D4

### `C5:E300..C5:E3FF`
- page family: `candidate_code_lane`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=1
- best targets: C5:E3B8 (weak, hits=1)
- owner backtracks:  (score=2)
- local clusters: C5:E3CD..C5:E3DD

### `C5:E400..C5:E4FF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=0
- best targets: C5:E43B (weak, hits=1); C5:E4F0 (weak, hits=1)
- owner backtracks:  (score=6);  (score=2)
- local clusters: none

### `C5:E500..C5:E5FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=3
- best targets: none
- owner backtracks: none
- local clusters: C5:E59D..C5:E5A6; C5:E5BB..C5:E5C4
