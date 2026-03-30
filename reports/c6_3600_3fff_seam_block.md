# Seam block report — C6:3600 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 2, "candidate_code_lane": 1, "mixed_command_data": 7}`
- review postures: `{"bad_start_or_dead_lane_reject": 5, "local_control_only": 1, "manual_owner_boundary_review": 2, "mixed_lane_continue": 2}`

## Page breakdown

### `C6:3600..C6:36FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=4, xref_hits=4, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=1
- best targets: C6:3630 (suspect, hits=1); C6:3631 (suspect, hits=1); C6:3688 (suspect, hits=1)
- owner backtracks:  (score=3);  (score=1);  (score=-1)
- local clusters: C6:3613..C6:3624

### `C6:3700..C6:37FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=4, strong_or_weak=3, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:37C4 (weak, hits=3); C6:37FC (weak, hits=1)
- owner backtracks:  (score=2);  (score=1)
- local clusters: none

### `C6:3800..C6:38FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=1, soft_bad=0, clusters=0
- best targets: C6:3806 (weak, hits=1); C6:3808 (suspect, hits=1); C6:3801 (invalid, hits=1)
- owner backtracks:  (score=4);  (score=4);  (score=2)
- local clusters: none

### `C6:3900..C6:39FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:391C (suspect, hits=1)
- owner backtracks:  (score=6)
- local clusters: none

### `C6:3A00..C6:3AFF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=4, xref_hits=4, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=1
- best targets: C6:3ACE (weak, hits=1); C6:3A08 (suspect, hits=1); C6:3A13 (suspect, hits=1)
- owner backtracks:  (score=4);  (score=2);  (score=2)
- local clusters: C6:3A65..C6:3A74

### `C6:3B00..C6:3BFF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=2, soft_bad=0, clusters=0
- best targets: C6:3B00 (invalid, hits=1); C6:3B80 (invalid, hits=1)
- owner backtracks:  (score=-4);  (score=-5)
- local clusters: none

### `C6:3C00..C6:3CFF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=3, xref_hits=23, strong_or_weak=0, hard_bad=22, soft_bad=0, clusters=2
- best targets: C6:3CF9 (suspect, hits=1); C6:3CC4 (invalid, hits=21); C6:3C90 (invalid, hits=1)
- owner backtracks:  (score=1);  (score=0);  (score=-4)
- local clusters: C6:3C00..C6:3C04; C6:3C58..C6:3C6A

### `C6:3D00..C6:3DFF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=4
- best targets: C6:3D0B (weak, hits=1); C6:3D1A (suspect, hits=1); C6:3D61 (suspect, hits=1)
- owner backtracks:  (score=6);  (score=3);  (score=2)
- local clusters: C6:3D07..C6:3D12; C6:3D60..C6:3D6A

### `C6:3E00..C6:3EFF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=1, soft_bad=0, clusters=3
- best targets: C6:3E04 (weak, hits=1); C6:3E12 (invalid, hits=1)
- owner backtracks:  (score=2);  (score=2)
- local clusters: C6:3E68..C6:3E71; C6:3E49..C6:3E51

### `C6:3F00..C6:3FFF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=3
- best targets: none
- owner backtracks: none
- local clusters: C6:3FE0..C6:3FEC; C6:3F08..C6:3F16
