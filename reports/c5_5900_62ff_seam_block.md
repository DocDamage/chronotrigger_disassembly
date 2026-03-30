# Seam block report — C5:5900 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 2, "candidate_code_lane": 7, "mixed_command_data": 1}`
- review postures: `{"bad_start_or_dead_lane_reject": 4, "local_control_only": 2, "manual_owner_boundary_review": 2, "mixed_lane_continue": 2}`

## Page breakdown

### `C5:5900..C5:59FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C5:596A..C5:5971

### `C5:5A00..C5:5AFF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=2
- best targets: C5:5A4D (suspect, hits=1); C5:5A7E (invalid, hits=1)
- owner backtracks:  (score=4);  (score=4)
- local clusters: C5:5A81..C5:5A86; C5:5AA0..C5:5AA5

### `C5:5B00..C5:5BFF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=1
- best targets: C5:5B22 (invalid, hits=1)
- owner backtracks:  (score=2)
- local clusters: C5:5B90..C5:5B9B

### `C5:5C00..C5:5CFF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=2
- best targets: C5:5C50 (invalid, hits=1)
- owner backtracks:  (score=6)
- local clusters: C5:5C48..C5:5C4C; C5:5C00..C5:5C06

### `C5:5D00..C5:5DFF`
- page family: `candidate_code_lane`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C5:5E00..C5:5EFF`
- page family: `candidate_code_lane`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C5:5F00..C5:5FFF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=2
- best targets: C5:5FBA (weak, hits=1); C5:5FBF (weak, hits=1); C5:5F60 (suspect, hits=1)
- owner backtracks:  (score=4);  (score=2);  (score=1)
- local clusters: C5:5F13..C5:5F17; C5:5F00..C5:5F10

### `C5:6000..C5:60FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=12, xref_hits=14, strong_or_weak=6, hard_bad=4, soft_bad=1, clusters=0
- best targets: C5:60E0 (weak, hits=3); C5:6005 (weak, hits=1); C5:6006 (weak, hits=1)
- owner backtracks:  (score=4);  (score=4);  (score=4)
- local clusters: none

### `C5:6100..C5:61FF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=0
- best targets: C5:6161 (weak, hits=1); C5:61E0 (weak, hits=1); C5:6107 (suspect, hits=1)
- owner backtracks:  (score=4);  (score=3);  (score=1)
- local clusters: none

### `C5:6200..C5:62FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=1, clusters=4
- best targets: C5:62FB (suspect, hits=1)
- owner backtracks:  (score=2)
- local clusters: C5:6272..C5:6284; C5:62DD..C5:62E7
