# Seam block report — C6:CC00 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 1, "mixed_command_data": 6, "text_ascii_heavy": 3}`
- review postures: `{"bad_start_or_dead_lane_reject": 1, "local_control_only": 5, "mixed_lane_continue": 4}`

## Page breakdown

### `C6:CC00..C6:CCFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=5, xref_hits=5, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:CC1C (suspect, hits=1); C6:CC2C (suspect, hits=1); C6:CCA9 (suspect, hits=1)
- owner backtracks: C6:CC17->C6:CC1C (score=4); C6:CCA8->C6:CCA9 (score=2); C6:CCFD->C6:CCFF (score=2)
- local clusters: none

### `C6:CD00..C6:CDFF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C6:CD2E..C6:CD39; C6:CD66..C6:CD72

### `C6:CE00..C6:CEFF`
- page family: `text_ascii_heavy`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:CE2B (suspect, hits=1); C6:CE30 (suspect, hits=1)
- owner backtracks: C6:CE2E->C6:CE30 (score=2); C6:CE23->C6:CE2B (score=0)
- local clusters: none

### `C6:CF00..C6:CFFF`
- page family: `text_ascii_heavy`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:CF90 (suspect, hits=1)
- owner backtracks: C6:CF8C->C6:CF90 (score=4)
- local clusters: none

### `C6:D000..C6:D0FF`
- page family: `text_ascii_heavy`
- review posture: `local_control_only`
- summary: raw_targets=4, xref_hits=4, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=3
- best targets: C6:D001 (suspect, hits=1); C6:D007 (suspect, hits=1); C6:D008 (suspect, hits=1)
- owner backtracks: C6:D05E->C6:D06B (score=4); C6:D000->C6:D007 (score=2); C6:D000->C6:D008 (score=2)
- local clusters: C6:D064..C6:D07C; C6:D0BE..C6:D0C8

### `C6:D100..C6:D1FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:D1E3 (suspect, hits=1)
- owner backtracks: C6:D1D5->C6:D1E3 (score=4)
- local clusters: none

### `C6:D200..C6:D2FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=3
- best targets: none
- owner backtracks: none
- local clusters: C6:D2B7..C6:D2BF; C6:D2DD..C6:D2E4

### `C6:D300..C6:D3FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=8
- best targets: none
- owner backtracks: none
- local clusters: C6:D3C2..C6:D3DB; C6:D329..C6:D337

### `C6:D400..C6:D4FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=4, strong_or_weak=0, hard_bad=3, soft_bad=0, clusters=3
- best targets: C6:D42C (suspect, hits=1); C6:D409 (invalid, hits=3)
- owner backtracks: C6:D42C->C6:D42C (score=1); C6:D409->C6:D409 (score=-2)
- local clusters: C6:D4CC..C6:D4DC; C6:D43A..C6:D445

### `C6:D500..C6:D5FF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=4
- best targets: C6:D500 (suspect, hits=1)
- owner backtracks: C6:D500->C6:D500 (score=3)
- local clusters: C6:D500..C6:D510; C6:D567..C6:D572
