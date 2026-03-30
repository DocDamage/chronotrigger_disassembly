# Seam block report — C6:B800 (10 pages)

## Summary
- page families: `{"mixed_command_data": 10}`
- review postures: `{"bad_start_or_dead_lane_reject": 2, "local_control_only": 6, "manual_owner_boundary_review": 2}`

## Page breakdown

### `C6:B800..C6:B8FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C6:B85D..C6:B86D; C6:B82F..C6:B847

### `C6:B900..C6:B9FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C6:B93C..C6:B954; C6:B9D4..C6:B9E1

### `C6:BA00..C6:BAFF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=2
- best targets: C6:BA7C (weak, hits=1); C6:BA60 (suspect, hits=1); C6:BA76 (suspect, hits=1)
- owner backtracks: C6:BA72->C6:BA76 (score=4); C6:BA72->C6:BA7C (score=4); C6:BA50->C6:BA60 (score=2)
- local clusters: C6:BA71..C6:BA7E; C6:BADE..C6:BAF6

### `C6:BB00..C6:BBFF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=1, clusters=1
- best targets: C6:BB06 (suspect, hits=1)
- owner backtracks: C6:BB00->C6:BB06 (score=2)
- local clusters: C6:BB2D..C6:BB45

### `C6:BC00..C6:BCFF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: C6:BC4D (suspect, hits=1)
- owner backtracks: C6:BC4C->C6:BC4D (score=6)
- local clusters: C6:BC64..C6:BC77; C6:BC46..C6:BC5E

### `C6:BD00..C6:BDFF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=3
- best targets: C6:BD7D (weak, hits=2); C6:BD44 (suspect, hits=1)
- owner backtracks: C6:BD6F->C6:BD7D (score=6); C6:BD3E->C6:BD44 (score=2)
- local clusters: C6:BD8F..C6:BDA5; C6:BDB1..C6:BDC6

### `C6:BE00..C6:BEFF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: C6:BE15 (suspect, hits=1); C6:BE43 (suspect, hits=1)
- owner backtracks: C6:BE35->C6:BE43 (score=6); C6:BE08->C6:BE15 (score=4)
- local clusters: C6:BE31..C6:BE49; C6:BE75..C6:BE86

### `C6:BF00..C6:BFFF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=1, soft_bad=0, clusters=3
- best targets: C6:BF02 (weak, hits=1); C6:BFFF (suspect, hits=1) [boundary_bait]; C6:BF01 (invalid, hits=1)
- owner backtracks: C6:BFFF->C6:BFFF (score=3); C6:BF00->C6:BF01 (score=2); C6:BF00->C6:BF02 (score=2)
- local clusters: C6:BFAB..C6:BFC3; C6:BFC8..C6:BFDD

### `C6:C000..C6:C0FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=5, xref_hits=8, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=1
- best targets: C6:C0C0 (suspect, hits=3); C6:C020 (suspect, hits=2); C6:C00E (suspect, hits=1)
- owner backtracks: C6:C010->C6:C020 (score=4); C6:C011->C6:C021 (score=4); C6:C00E->C6:C00E (score=3)
- local clusters: C6:C07F..C6:C097

### `C6:C100..C6:C1FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: C6:C109 (suspect, hits=1); C6:C115 (suspect, hits=1)
- owner backtracks: C6:C100->C6:C109 (score=2); C6:C111->C6:C115 (score=2)
- local clusters: C6:C1D7..C6:C1EF; C6:C16E..C6:C186
