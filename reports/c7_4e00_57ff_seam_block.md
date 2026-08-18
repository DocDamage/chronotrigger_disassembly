# Seam block report — C7:4E00 (10 pages)

## Summary
- page families: `{"mixed_command_data": 10}`
- review postures: `{"bad_start_or_dead_lane_reject": 2, "local_control_only": 3, "manual_owner_boundary_review": 1, "mixed_lane_continue": 4}`

## Page breakdown

### `C7:4E00..C7:4EFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:4EBF (weak, hits=1)
- owner backtracks: C7:4EB5->C7:4EBF (score=2)
- local clusters: none

### `C7:4F00..C7:4FFF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:4F14 (weak, hits=1); C7:4F33 (suspect, hits=1)
- owner backtracks: C7:4F11->C7:4F14 (score=4); C7:4F2B->C7:4F33 (score=2)
- local clusters: C7:4F10..C7:4F1A

### `C7:5000..C7:50FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C7:5100..C7:51FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:5155 (suspect, hits=1)
- owner backtracks: C7:5146->C7:5155 (score=4)
- local clusters: none

### `C7:5200..C7:52FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=0
- best targets: C7:5228 (suspect, hits=1); C7:5222 (invalid, hits=1)
- owner backtracks: C7:521C->C7:5222 (score=4); C7:521C->C7:5228 (score=4)
- local clusters: none

### `C7:5300..C7:53FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C7:5384..C7:5392

### `C7:5400..C7:54FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:54CC (suspect, hits=1)
- owner backtracks: C7:54C0->C7:54CC (score=4)
- local clusters: none

### `C7:5500..C7:55FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=1
- best targets: C7:55D0 (invalid, hits=1)
- owner backtracks: C7:55C1->C7:55D0 (score=2)
- local clusters: C7:5548..C7:554C

### `C7:5600..C7:56FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: C7:5635 (suspect, hits=1)
- owner backtracks: C7:5626->C7:5635 (score=2)
- local clusters: C7:561E..C7:5625; C7:5686..C7:5693

### `C7:5700..C7:57FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C7:5798..C7:57A0; C7:578A..C7:5793
