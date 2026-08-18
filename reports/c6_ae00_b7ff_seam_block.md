# Seam block report — C6:AE00 (10 pages)

## Summary
- page families: `{"mixed_command_data": 10}`
- review postures: `{"bad_start_or_dead_lane_reject": 4, "local_control_only": 3, "manual_owner_boundary_review": 2, "mixed_lane_continue": 1}`

## Page breakdown

### `C6:AE00..C6:AEFF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=3
- best targets: none
- owner backtracks: none
- local clusters: C6:AE32..C6:AE5C; C6:AE9C..C6:AEA9

### `C6:AF00..C6:AFFF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=2
- best targets: C6:AFAE (weak, hits=1); C6:AF40 (suspect, hits=1)
- owner backtracks: C6:AF30->C6:AF40 (score=4); C6:AFAA->C6:AFAE (score=2)
- local clusters: C6:AF83..C6:AF8C; C6:AF4C..C6:AF55

### `C6:B000..C6:B0FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=3
- best targets: C6:B068 (invalid, hits=1)
- owner backtracks: C6:B068->C6:B068 (score=-4)
- local clusters: C6:B098..C6:B0A0; C6:B011..C6:B01B

### `C6:B100..C6:B1FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=1
- best targets: C6:B140 (invalid, hits=1)
- owner backtracks: C6:B138->C6:B140 (score=6)
- local clusters: C6:B131..C6:B13F

### `C6:B200..C6:B2FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=4, xref_hits=4, strong_or_weak=1, hard_bad=1, soft_bad=0, clusters=1
- best targets: C6:B20C (weak, hits=1); C6:B23F (suspect, hits=1); C6:B2C1 (suspect, hits=1)
- owner backtracks: C6:B20A->C6:B20C (score=4); C6:B22B->C6:B239 (score=4); C6:B23B->C6:B23F (score=4)
- local clusters: C6:B298..C6:B2A5

### `C6:B300..C6:B3FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=1
- best targets: C6:B3B2 (suspect, hits=1); C6:B3FD (invalid, hits=1) [boundary_bait]
- owner backtracks: C6:B3A2->C6:B3B2 (score=2); C6:B3ED->C6:B3FD (score=2)
- local clusters: C6:B3BD..C6:B3D5

### `C6:B400..C6:B4FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C6:B4FF (suspect, hits=1) [boundary_bait]
- owner backtracks: C6:B4FD->C6:B4FF (score=2)
- local clusters: C6:B4C4..C6:B4D2

### `C6:B500..C6:B5FF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=2
- best targets: C6:B569 (weak, hits=1)
- owner backtracks: C6:B55D->C6:B569 (score=4)
- local clusters: C6:B514..C6:B536; C6:B5E3..C6:B5FA

### `C6:B600..C6:B6FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: C6:B604 (suspect, hits=1); C6:B62E (suspect, hits=1)
- owner backtracks: C6:B62D->C6:B62E (score=6); C6:B603->C6:B604 (score=4)
- local clusters: C6:B617..C6:B62F; C6:B680..C6:B69F

### `C6:B700..C6:B7FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:B74A (suspect, hits=1)
- owner backtracks: C6:B73A->C6:B74A (score=4)
- local clusters: none
