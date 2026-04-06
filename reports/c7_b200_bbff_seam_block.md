# Seam block report — C7:B200 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 1, "candidate_code_lane": 6, "mixed_command_data": 3}`
- review postures: `{"bad_start_or_dead_lane_reject": 1, "local_control_only": 7, "mixed_lane_continue": 2}`

## Page breakdown

### `C7:B200..C7:B2FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:B21B (suspect, hits=1)
- owner backtracks: C7:B219->C7:B21B (score=2)
- local clusters: C7:B200..C7:B213

### `C7:B300..C7:B3FF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C7:B3C4..C7:B3D6; C7:B363..C7:B36C

### `C7:B400..C7:B4FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=5, xref_hits=5, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=3
- best targets: C7:B440 (suspect, hits=1); C7:B4EE (suspect, hits=1); C7:B4FC (suspect, hits=1)
- owner backtracks: C7:B435->C7:B440 (score=2); C7:B4E0->C7:B4EE (score=2); C7:B4F3->C7:B4FC (score=2)
- local clusters: C7:B4B9..C7:B4C5; C7:B44E..C7:B45A

### `C7:B500..C7:B5FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:B500 (suspect, hits=1)
- owner backtracks: C7:B500->C7:B500 (score=1)
- local clusters: C7:B5D5..C7:B5ED

### `C7:B600..C7:B6FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C7:B68F..C7:B6A7

### `C7:B700..C7:B7FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C7:B777..C7:B78F; C7:B7B8..C7:B7BC

### `C7:B800..C7:B8FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C7:B82C..C7:B844

### `C7:B900..C7:B9FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:B900 (suspect, hits=1); C7:B963 (suspect, hits=1)
- owner backtracks: C7:B961->C7:B963 (score=4); C7:B900->C7:B900 (score=3)
- local clusters: C7:B903..C7:B917

### `C7:BA00..C7:BAFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C7:BB00..C7:BBFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none
