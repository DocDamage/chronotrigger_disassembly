# Seam block report — C7:3A00 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 4, "dead_zero_field": 1, "mixed_command_data": 5}`
- review postures: `{"bad_start_or_dead_lane_reject": 2, "dead_lane_reject": 1, "manual_owner_boundary_review": 7}`

## Page breakdown

### `C7:3A00..C7:3AFF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=3
- best targets: C7:3AF5 (weak, hits=1)
- owner backtracks: C7:3AE5->C7:3AF5 (score=4)
- local clusters: C7:3A37..C7:3A4F; C7:3A00..C7:3A06

### `C7:3B00..C7:3BFF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:3BA1 (weak, hits=1)
- owner backtracks: C7:3B93->C7:3BA1 (score=6)
- local clusters: C7:3BC2..C7:3BD6

### `C7:3C00..C7:3CFF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=4
- best targets: C7:3C12 (weak, hits=1)
- owner backtracks: C7:3C04->C7:3C12 (score=6)
- local clusters: C7:3C33..C7:3C5D; C7:3C1F..C7:3C30

### `C7:3D00..C7:3DFF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=3
- best targets: C7:3DE1 (weak, hits=1); C7:3D2D (suspect, hits=1)
- owner backtracks: C7:3DDF->C7:3DE1 (score=6); C7:3D27->C7:3D2D (score=2)
- local clusters: C7:3DAE..C7:3DFE; C7:3D3B..C7:3D54

### `C7:3E00..C7:3EFF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=3, hard_bad=0, soft_bad=0, clusters=3
- best targets: C7:3EC2 (weak, hits=1); C7:3ED1 (weak, hits=1); C7:3ED2 (weak, hits=1)
- owner backtracks: C7:3ECC->C7:3ED1 (score=4); C7:3ECC->C7:3ED2 (score=4); C7:3EC0->C7:3EC2 (score=2)
- local clusters: C7:3E15..C7:3E2D; C7:3ECB..C7:3EF0

### `C7:3F00..C7:3FFF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=4, xref_hits=4, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=4
- best targets: C7:3FC2 (weak, hits=1); C7:3FE1 (weak, hits=1); C7:3FE0 (suspect, hits=1)
- owner backtracks: C7:3FB8->C7:3FC2 (score=4); C7:3FD9->C7:3FE0 (score=2); C7:3FD9->C7:3FE1 (score=2)
- local clusters: C7:3F50..C7:3F76; C7:3F31..C7:3F49

### `C7:4000..C7:40FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=6, xref_hits=7, strong_or_weak=1, hard_bad=4, soft_bad=0, clusters=1
- best targets: C7:4000 (weak, hits=1); C7:404C (suspect, hits=1); C7:4095 (suspect, hits=1)
- owner backtracks: C7:4038->C7:4048 (score=2); C7:4000->C7:4000 (score=1); C7:404A->C7:404C (score=0)
- local clusters: C7:4073..C7:4079

### `C7:4100..C7:41FF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=3, xref_hits=8, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:4133 (weak, hits=1); C7:417E (weak, hits=1); C7:418D (suspect, hits=6)
- owner backtracks: C7:412B->C7:4133 (score=4); C7:418C->C7:418D (score=4); C7:4172->C7:417E (score=2)
- local clusters: C7:41E8..C7:41F3

### `C7:4200..C7:42FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=6, xref_hits=10, strong_or_weak=0, hard_bad=4, soft_bad=0, clusters=0
- best targets: C7:428D (suspect, hits=4); C7:42D1 (suspect, hits=1); C7:42EE (suspect, hits=1)
- owner backtracks: C7:42CC->C7:42D1 (score=4); C7:4289->C7:428D (score=2); C7:4292->C7:42A2 (score=2)
- local clusters: none

### `C7:4300..C7:43FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=5, xref_hits=5, strong_or_weak=0, hard_bad=3, soft_bad=0, clusters=0
- best targets: C7:4322 (suspect, hits=1); C7:4333 (suspect, hits=1); C7:4348 (invalid, hits=1)
- owner backtracks: C7:431F->C7:4322 (score=2); C7:4323->C7:4333 (score=-2); C7:4348->C7:4348 (score=-8)
- local clusters: none
