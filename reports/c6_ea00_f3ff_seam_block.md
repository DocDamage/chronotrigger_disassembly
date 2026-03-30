# Seam block report — C6:EA00 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 1, "dead_zero_field": 3, "mixed_command_data": 6}`
- review postures: `{"bad_start_or_dead_lane_reject": 2, "dead_lane_reject": 3, "mixed_lane_continue": 5}`

## Page breakdown

### `C6:EA00..C6:EAFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C6:EB00..C6:EBFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C6:EC00..C6:ECFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:EC10 (suspect, hits=1)
- owner backtracks: C6:EC09->C6:EC10 (score=4)
- local clusters: none

### `C6:ED00..C6:EDFF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=3, xref_hits=12, strong_or_weak=11, hard_bad=1, soft_bad=0, clusters=0
- best targets: C6:EDE1 (weak, hits=8); C6:ED04 (weak, hits=3); C6:ED07 (invalid, hits=1)
- owner backtracks: C6:EDDF->C6:EDE1 (score=4); C6:ED02->C6:ED07 (score=2); C6:ED02->C6:ED04 (score=0)
- local clusters: none

### `C6:EE00..C6:EEFF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C6:EE21 (suspect, hits=1)
- owner backtracks: C6:EE21->C6:EE21 (score=3)
- local clusters: C6:EE36..C6:EE42

### `C6:EF00..C6:EFFF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=3, soft_bad=0, clusters=0
- best targets: C6:EFBD (invalid, hits=1); C6:EFC7 (invalid, hits=1); C6:EFCC (invalid, hits=1)
- owner backtracks: C6:EFBD->C6:EFBD (score=-8); C6:EFC7->C6:EFC7 (score=-8); C6:EFCC->C6:EFCC (score=-8)
- local clusters: none

### `C6:F000..C6:F0FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=6, xref_hits=7, strong_or_weak=1, hard_bad=1, soft_bad=0, clusters=0
- best targets: C6:F020 (weak, hits=1); C6:F0BF (suspect, hits=2); C6:F00D (suspect, hits=1)
- owner backtracks: C6:F00C->C6:F00D (score=4); C6:F0B7->C6:F0BF (score=4); C6:F078->C6:F078 (score=3)
- local clusters: none

### `C6:F100..C6:F1FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:F100 (suspect, hits=1); C6:F14E (suspect, hits=1); C6:F1AE (suspect, hits=1)
- owner backtracks: C6:F14B->C6:F14E (score=2); C6:F1AD->C6:F1AE (score=2); C6:F100->C6:F100 (score=1)
- local clusters: none

### `C6:F200..C6:F2FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=3, strong_or_weak=0, hard_bad=0, soft_bad=1, clusters=0
- best targets: C6:F2BF (suspect, hits=2); C6:F25C (suspect, hits=1)
- owner backtracks: C6:F2BE->C6:F2BF (score=4); C6:F254->C6:F25C (score=2)
- local clusters: none

### `C6:F300..C6:F3FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=2, soft_bad=0, clusters=0
- best targets: C6:F300 (invalid, hits=1); C6:F30C (invalid, hits=1)
- owner backtracks: C6:F300->C6:F300 (score=-8); C6:F30C->C6:F30C (score=-8)
- local clusters: none
