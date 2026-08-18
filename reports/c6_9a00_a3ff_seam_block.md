# Seam block report — C6:9A00 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 1, "mixed_command_data": 8, "text_ascii_heavy": 1}`
- review postures: `{"bad_start_or_dead_lane_reject": 2, "local_control_only": 6, "manual_owner_boundary_review": 1, "mixed_lane_continue": 1}`

## Page breakdown

### `C6:9A00..C6:9AFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C6:9B00..C6:9BFF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=3
- best targets: C6:9B30 (suspect, hits=1)
- owner backtracks: C6:9B2B->C6:9B30 (score=6)
- local clusters: C6:9B93..C6:9BA1; C6:9B3A..C6:9B3F

### `C6:9C00..C6:9CFF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=4
- best targets: C6:9C2E (suspect, hits=1)
- owner backtracks: C6:9C20->C6:9C2E (score=2)
- local clusters: C6:9C67..C6:9C7B; C6:9C09..C6:9C1D

### `C6:9D00..C6:9DFF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=2
- best targets: C6:9D0B (invalid, hits=1)
- owner backtracks: C6:9D04->C6:9D0B (score=2)
- local clusters: C6:9DE4..C6:9DFC; C6:9D03..C6:9D23

### `C6:9E00..C6:9EFF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C6:9EE9..C6:9EF4; C6:9E56..C6:9E72

### `C6:9F00..C6:9FFF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C6:9F02..C6:9F1D; C6:9F37..C6:9F49

### `C6:A000..C6:A0FF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=5, xref_hits=9, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=4
- best targets: C6:A0BF (weak, hits=2); C6:A043 (suspect, hits=4); C6:A004 (suspect, hits=1)
- owner backtracks: C6:A051->C6:A05F (score=6); C6:A038->C6:A043 (score=4); C6:A000->C6:A004 (score=2)
- local clusters: C6:A0DB..C6:A0F2; C6:A07F..C6:A091

### `C6:A100..C6:A1FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=1, clusters=7
- best targets: C6:A1E0 (suspect, hits=1)
- owner backtracks: C6:A1DF->C6:A1E0 (score=6)
- local clusters: C6:A1CC..C6:A1DC; C6:A142..C6:A150

### `C6:A200..C6:A2FF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=4, xref_hits=5, strong_or_weak=3, hard_bad=1, soft_bad=0, clusters=5
- best targets: C6:A2BF (weak, hits=2); C6:A28B (weak, hits=1); C6:A200 (suspect, hits=1)
- owner backtracks: C6:A200->C6:A201 (score=4); C6:A28A->C6:A28B (score=4); C6:A2B0->C6:A2BF (score=4)
- local clusters: C6:A2D9..C6:A2EE; C6:A23D..C6:A257

### `C6:A300..C6:A3FF`
- page family: `text_ascii_heavy`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=4
- best targets: C6:A321 (suspect, hits=1)
- owner backtracks: C6:A318->C6:A321 (score=2)
- local clusters: C6:A32D..C6:A355; C6:A317..C6:A31F
