# Seam block report — C7:0800 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 1, "dead_zero_field": 4, "mixed_command_data": 5}`
- review postures: `{"bad_start_or_dead_lane_reject": 1, "dead_lane_reject": 4, "manual_owner_boundary_review": 4, "mixed_lane_continue": 1}`

## Page breakdown

### `C7:0800..C7:08FF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=4
- best targets: C7:08DC (weak, hits=1); C7:08E3 (suspect, hits=1)
- owner backtracks: C7:08DF->C7:08E3 (score=6); C7:08CC->C7:08DC (score=4)
- local clusters: C7:0835..C7:0844; C7:0868..C7:0874

### `C7:0900..C7:09FF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=5, xref_hits=44, strong_or_weak=8, hard_bad=0, soft_bad=0, clusters=2
- best targets: C7:09DA (weak, hits=32); C7:09EA (weak, hits=7); C7:09FD (weak, hits=2) [boundary_bait]
- owner backtracks: C7:09CA->C7:09DA (score=6); C7:09DA->C7:09EA (score=6); C7:09EA->C7:09F2 (score=6)
- local clusters: C7:09C1..C7:09FC; C7:097F..C7:0997

### `C7:0A00..C7:0AFF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=4, xref_hits=6, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=2
- best targets: C7:0A12 (weak, hits=3); C7:0A39 (suspect, hits=1); C7:0A64 (suspect, hits=1)
- owner backtracks: C7:0A0D->C7:0A12 (score=6); C7:0A36->C7:0A39 (score=4); C7:0A64->C7:0A64 (score=3)
- local clusters: C7:0A70..C7:0A97; C7:0A07..C7:0A11

### `C7:0B00..C7:0BFF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=2
- best targets: C7:0B91 (weak, hits=1); C7:0BA0 (weak, hits=1)
- owner backtracks: C7:0B90->C7:0B91 (score=4); C7:0B90->C7:0BA0 (score=0)
- local clusters: C7:0B3F..C7:0B57; C7:0B00..C7:0B0B

### `C7:0C00..C7:0CFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=4, xref_hits=4, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:0C10 (weak, hits=1); C7:0C11 (weak, hits=1); C7:0CA5 (suspect, hits=1)
- owner backtracks: C7:0C10->C7:0C10 (score=-1); C7:0C11->C7:0C11 (score=-1); C7:0CA5->C7:0CA5 (score=-3)
- local clusters: none

### `C7:0D00..C7:0DFF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=4, xref_hits=4, strong_or_weak=2, hard_bad=1, soft_bad=0, clusters=2
- best targets: C7:0D12 (weak, hits=1); C7:0DA8 (weak, hits=1); C7:0DD1 (suspect, hits=1)
- owner backtracks: C7:0DD0->C7:0DD1 (score=6); C7:0DA5->C7:0DA8 (score=2); C7:0D12->C7:0D12 (score=1)
- local clusters: C7:0DC6..C7:0DDE; C7:0DA4..C7:0DB5

### `C7:0E00..C7:0EFF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=5, xref_hits=6, strong_or_weak=1, hard_bad=5, soft_bad=0, clusters=1
- best targets: C7:0E0F (weak, hits=1); C7:0EF0 (invalid, hits=2); C7:0E3F (invalid, hits=1)
- owner backtracks: C7:0E00->C7:0E0F (score=0); C7:0E3F->C7:0E3F (score=-8); C7:0EEE->C7:0EEE (score=-8)
- local clusters: C7:0E00..C7:0E05

### `C7:0F00..C7:0FFF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=8, xref_hits=10, strong_or_weak=1, hard_bad=8, soft_bad=0, clusters=0
- best targets: C7:0FDF (weak, hits=1); C7:0F31 (suspect, hits=1); C7:0F00 (invalid, hits=2)
- owner backtracks: C7:0F31->C7:0F31 (score=-1); C7:0FDF->C7:0FDF (score=-3); C7:0F0F->C7:0F0F (score=-6)
- local clusters: none

### `C7:1000..C7:10FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=9, xref_hits=12, strong_or_weak=1, hard_bad=11, soft_bad=0, clusters=0
- best targets: C7:10DF (weak, hits=1); C7:10C2 (invalid, hits=3); C7:1000 (invalid, hits=2)
- owner backtracks: C7:10DF->C7:10DF (score=-3); C7:10EF->C7:10EF (score=-6); C7:10F0->C7:10F0 (score=-6)
- local clusters: none

### `C7:1100..C7:11FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=12, xref_hits=12, strong_or_weak=1, hard_bad=10, soft_bad=0, clusters=0
- best targets: C7:11FF (weak, hits=1) [boundary_bait]; C7:11D1 (suspect, hits=1); C7:1101 (invalid, hits=1)
- owner backtracks: C7:11D1->C7:11D1 (score=-3); C7:11FF->C7:11FF (score=-3); C7:110C->C7:110C (score=-6)
- local clusters: none
