# Seam block report — C5:B400 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 3, "candidate_code_lane": 6, "mixed_command_data": 1}`
- review postures: `{"bad_start_or_dead_lane_reject": 2, "local_control_only": 4, "manual_owner_boundary_review": 2, "mixed_lane_continue": 2}`

## Page breakdown

### `C5:B400..C5:B4FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=5, xref_hits=5, strong_or_weak=2, hard_bad=1, soft_bad=0, clusters=5
- best targets: C5:B400 (weak, hits=1); C5:B4D8 (weak, hits=1); C5:B416 (suspect, hits=1)
- owner backtracks:  (score=6);  (score=6);  (score=2)
- local clusters: C5:B46B..C5:B48A; C5:B4C3..C5:B4CE

### `C5:B500..C5:B5FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C5:B58F..C5:B5E6; C5:B51B..C5:B536

### `C5:B600..C5:B6FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C5:B64E..C5:B667; C5:B6B5..C5:B6BE

### `C5:B700..C5:B7FF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=2
- best targets: C5:B707 (weak, hits=1); C5:B740 (weak, hits=1)
- owner backtracks:  (score=6);  (score=2)
- local clusters: C5:B723..C5:B72B; C5:B7D7..C5:B7DE

### `C5:B800..C5:B8FF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=5, xref_hits=6, strong_or_weak=1, hard_bad=4, soft_bad=0, clusters=2
- best targets: C5:B849 (weak, hits=1); C5:B860 (suspect, hits=1); C5:B800 (invalid, hits=2)
- owner backtracks:  (score=6);  (score=4);  (score=3)
- local clusters: C5:B854..C5:B85F; C5:B800..C5:B809

### `C5:B900..C5:B9FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=4
- best targets: C5:B900 (weak, hits=2)
- owner backtracks:  (score=1)
- local clusters: C5:B9B4..C5:B9B9; C5:B915..C5:B91C

### `C5:BA00..C5:BAFF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C5:BA25..C5:BA2B; C5:BA52..C5:BA66

### `C5:BB00..C5:BBFF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C5:BB7F..C5:BB97; C5:BBA7..C5:BBAB

### `C5:BC00..C5:BCFF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=8
- best targets: C5:BC04 (weak, hits=1); C5:BC08 (weak, hits=1)
- owner backtracks:  (score=4);  (score=3)
- local clusters: C5:BC1E..C5:BC36; C5:BC8A..C5:BC9E

### `C5:BD00..C5:BDFF`
- page family: `candidate_code_lane`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=3
- best targets: C5:BD49 (weak, hits=1)
- owner backtracks:  (score=1)
- local clusters: C5:BDE7..C5:BDFE; C5:BD61..C5:BD65
