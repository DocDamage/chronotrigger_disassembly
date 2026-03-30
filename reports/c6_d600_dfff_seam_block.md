# Seam block report — C6:D600 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 5, "dead_zero_field": 3, "mixed_command_data": 2}`
- review postures: `{"bad_start_or_dead_lane_reject": 1, "dead_lane_reject": 3, "local_control_only": 5, "mixed_lane_continue": 1}`

## Page breakdown

### `C6:D600..C6:D6FF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=4
- best targets: C6:D6CC (suspect, hits=1)
- owner backtracks: C6:D6C0->C6:D6CC (score=4)
- local clusters: C6:D62C..C6:D63A; C6:D6A6..C6:D6AE

### `C6:D700..C6:D7FF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=3
- best targets: none
- owner backtracks: none
- local clusters: C6:D769..C6:D781; C6:D7C1..C6:D7D1

### `C6:D800..C6:D8FF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=5
- best targets: C6:D800 (suspect, hits=1)
- owner backtracks: C6:D800->C6:D800 (score=3)
- local clusters: C6:D8B7..C6:D8BD; C6:D864..C6:D86D

### `C6:D900..C6:D9FF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=3
- best targets: none
- owner backtracks: none
- local clusters: C6:D920..C6:D928; C6:D976..C6:D97B

### `C6:DA00..C6:DAFF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=3
- best targets: C6:DAA5 (invalid, hits=1)
- owner backtracks: C6:DA96->C6:DAA5 (score=4)
- local clusters: C6:DA5D..C6:DA64; C6:DAD2..C6:DAD8

### `C6:DB00..C6:DBFF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=1, clusters=1
- best targets: C6:DB29 (suspect, hits=1); C6:DBAC (suspect, hits=1)
- owner backtracks: C6:DB28->C6:DB29 (score=4); C6:DBA9->C6:DBAC (score=0)
- local clusters: C6:DB38..C6:DB4E

### `C6:DC00..C6:DCFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=1, clusters=0
- best targets: C6:DC90 (suspect, hits=1)
- owner backtracks: C6:DC83->C6:DC90 (score=0)
- local clusters: none

### `C6:DD00..C6:DDFF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C6:DE00..C6:DEFF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=2, soft_bad=0, clusters=0
- best targets: C6:DE00 (invalid, hits=1); C6:DE20 (invalid, hits=1)
- owner backtracks: C6:DE00->C6:DE00 (score=-8); C6:DE20->C6:DE20 (score=-8)
- local clusters: none

### `C6:DF00..C6:DFFF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=1, xref_hits=5, strong_or_weak=0, hard_bad=5, soft_bad=0, clusters=0
- best targets: C6:DF21 (invalid, hits=5)
- owner backtracks: C6:DF21->C6:DF21 (score=-8)
- local clusters: none
