# Seam block report — C5:E600 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 5, "candidate_code_lane": 3, "mixed_command_data": 2}`
- review postures: `{"bad_start_or_dead_lane_reject": 2, "local_control_only": 3, "manual_owner_boundary_review": 2, "mixed_lane_continue": 3}`

## Page breakdown

### `C5:E600..C5:E6FF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C5:E6C8 (suspect, hits=1)
- owner backtracks:  (score=4)
- local clusters: C5:E65F..C5:E667

### `C5:E700..C5:E7FF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=4
- best targets: C5:E790 (weak, hits=1)
- owner backtracks:  (score=6)
- local clusters: C5:E77D..C5:E79B; C5:E7A4..C5:E7B1

### `C5:E800..C5:E8FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=1, clusters=3
- best targets: C5:E853 (suspect, hits=1)
- owner backtracks:  (score=-2)
- local clusters: C5:E8DE..C5:E8EC; C5:E8F4..C5:E8FF

### `C5:E900..C5:E9FF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=4
- best targets: C5:E902 (weak, hits=1); C5:E976 (weak, hits=1)
- owner backtracks:  (score=4);  (score=2)
- local clusters: C5:E9AC..C5:E9B0; C5:E9A3..C5:E9A7

### `C5:EA00..C5:EAFF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=2, soft_bad=0, clusters=2
- best targets: C5:EA87 (invalid, hits=1); C5:EA9F (invalid, hits=1)
- owner backtracks:  (score=2);  (score=2)
- local clusters: C5:EADF..C5:EAE6; C5:EA35..C5:EA3D

### `C5:EB00..C5:EBFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=0
- best targets: C5:EB23 (weak, hits=1)
- owner backtracks:  (score=2)
- local clusters: none

### `C5:EC00..C5:ECFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C5:ED00..C5:EDFF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C5:ED20..C5:ED2C; C5:ED88..C5:EDA2

### `C5:EE00..C5:EEFF`
- page family: `candidate_code_lane`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C5:EF00..C5:EFFF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=9, xref_hits=10, strong_or_weak=7, hard_bad=2, soft_bad=1, clusters=2
- best targets: C5:EF04 (weak, hits=2); C5:EF5B (weak, hits=1); C5:EF68 (weak, hits=1)
- owner backtracks:  (score=4);  (score=4);  (score=4)
- local clusters: C5:EF1C..C5:EF21; C5:EFD0..C5:EFD7
