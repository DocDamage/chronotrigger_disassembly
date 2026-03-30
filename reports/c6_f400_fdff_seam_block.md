# Seam block report — C6:F400 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 2, "candidate_code_lane": 1, "mixed_command_data": 5, "text_ascii_heavy": 2}`
- review postures: `{"bad_start_or_dead_lane_reject": 2, "local_control_only": 2, "mixed_lane_continue": 6}`

## Page breakdown

### `C6:F400..C6:F4FF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C6:F401..C6:F418; C6:F42E..C6:F446

### `C6:F500..C6:F5FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=1
- best targets: C6:F5EE (invalid, hits=1)
- owner backtracks: C6:F5EE->C6:F5EE (score=-8)
- local clusters: C6:F542..C6:F547

### `C6:F600..C6:F6FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C6:F700..C6:F7FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C6:F800..C6:F8FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=8, xref_hits=8, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:F801 (suspect, hits=1); C6:F802 (suspect, hits=1); C6:F830 (suspect, hits=1)
- owner backtracks: C6:F8B4->C6:F8B9 (score=4); C6:F8B4->C6:F8BE (score=4); C6:F8B4->C6:F8C0 (score=4)
- local clusters: none

### `C6:F900..C6:F9FF`
- page family: `text_ascii_heavy`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C6:FA00..C6:FAFF`
- page family: `text_ascii_heavy`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:FA10 (suspect, hits=1); C6:FA47 (suspect, hits=1)
- owner backtracks: C6:FA37->C6:FA47 (score=2); C6:FA00->C6:FA10 (score=0)
- local clusters: none

### `C6:FB00..C6:FBFF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C6:FB40 (suspect, hits=1)
- owner backtracks: C6:FB40->C6:FB40 (score=3)
- local clusters: C6:FB5F..C6:FB6B

### `C6:FC00..C6:FCFF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=1
- best targets: C6:FC9D (invalid, hits=1)
- owner backtracks: C6:FC9D->C6:FC9D (score=-8)
- local clusters: C6:FC15..C6:FC46

### `C6:FD00..C6:FDFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none
