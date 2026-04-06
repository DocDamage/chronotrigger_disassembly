# Seam block report — C7:5800 (10 pages)

## Summary
- page families: `{"mixed_command_data": 7, "text_ascii_heavy": 3}`
- review postures: `{"bad_start_or_dead_lane_reject": 2, "local_control_only": 1, "manual_owner_boundary_review": 1, "mixed_lane_continue": 6}`

## Page breakdown

### `C7:5800..C7:58FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:5813 (weak, hits=1); C7:58DD (weak, hits=1); C7:5800 (suspect, hits=1)
- owner backtracks: C7:5805->C7:5813 (score=2); C7:58D1->C7:58DD (score=2); C7:5800->C7:5800 (score=1)
- local clusters: none

### `C7:5900..C7:59FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C7:5A00..C7:5AFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=1, clusters=0
- best targets: C7:5AD3 (suspect, hits=1)
- owner backtracks: C7:5AD1->C7:5AD3 (score=2)
- local clusters: none

### `C7:5B00..C7:5BFF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=1
- best targets: C7:5B1F (invalid, hits=1)
- owner backtracks: C7:5B17->C7:5B1F (score=4)
- local clusters: C7:5B11..C7:5B1F

### `C7:5C00..C7:5CFF`
- page family: `text_ascii_heavy`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C7:5D00..C7:5DFF`
- page family: `text_ascii_heavy`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:5DC2 (weak, hits=1); C7:5D98 (suspect, hits=2)
- owner backtracks: C7:5D8D->C7:5D98 (score=2); C7:5DB2->C7:5DC2 (score=2)
- local clusters: C7:5DF3..C7:5DFE

### `C7:5E00..C7:5EFF`
- page family: `text_ascii_heavy`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:5ED1 (weak, hits=1)
- owner backtracks: C7:5EC5->C7:5ED1 (score=2)
- local clusters: C7:5E00..C7:5E1E

### `C7:5F00..C7:5FFF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:5F10 (suspect, hits=1); C7:5FD1 (suspect, hits=1)
- owner backtracks: C7:5FCE->C7:5FD1 (score=4); C7:5F0E->C7:5F10 (score=2)
- local clusters: C7:5FCD..C7:5FD2

### `C7:6000..C7:60FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=4, xref_hits=6, strong_or_weak=1, hard_bad=1, soft_bad=0, clusters=0
- best targets: C7:60D3 (weak, hits=1); C7:60B5 (suspect, hits=3); C7:60F5 (suspect, hits=1)
- owner backtracks: C7:60E9->C7:60F5 (score=4); C7:60AB->C7:60B5 (score=2); C7:60AB->C7:60B9 (score=2)
- local clusters: none

### `C7:6100..C7:61FF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=2
- best targets: C7:61D1 (weak, hits=1); C7:61D0 (suspect, hits=1)
- owner backtracks: C7:61C6->C7:61D0 (score=6); C7:61C6->C7:61D1 (score=6)
- local clusters: C7:618A..C7:61A2; C7:61DF..C7:61E4
