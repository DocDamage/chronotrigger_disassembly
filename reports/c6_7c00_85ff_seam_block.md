# Seam block report — C6:7C00 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 1, "mixed_command_data": 9}`
- review postures: `{"bad_start_or_dead_lane_reject": 5, "local_control_only": 1, "manual_owner_boundary_review": 2, "mixed_lane_continue": 2}`

## Page breakdown

### `C6:7C00..C6:7CFF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=1
- best targets: C6:7C2B (suspect, hits=1); C6:7C8B (invalid, hits=1)
- owner backtracks:  (score=4);  (score=2)
- local clusters: C6:7C86..C6:7C8B

### `C6:7D00..C6:7DFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:7D00 (suspect, hits=1)
- owner backtracks:  (score=3)
- local clusters: none

### `C6:7E00..C6:7EFF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=1, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=1
- best targets: C6:7EA9 (weak, hits=2)
- owner backtracks:  (score=6)
- local clusters: C6:7E3F..C6:7E44

### `C6:7F00..C6:7FFF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=3, xref_hits=10, strong_or_weak=1, hard_bad=8, soft_bad=1, clusters=3
- best targets: C6:7F80 (weak, hits=1); C6:7FCD (suspect, hits=1); C6:7FC4 (invalid, hits=8)
- owner backtracks:  (score=4);  (score=4);  (score=1)
- local clusters: C6:7F29..C6:7F3B; C6:7FD9..C6:7FE9

### `C6:8000..C6:80FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=8, xref_hits=10, strong_or_weak=7, hard_bad=2, soft_bad=0, clusters=1
- best targets: C6:8021 (weak, hits=3); C6:8031 (weak, hits=1); C6:808D (weak, hits=1)
- owner backtracks:  (score=4);  (score=4);  (score=3)
- local clusters: C6:80AD..C6:80B5

### `C6:8100..C6:81FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:81E2 (suspect, hits=1)
- owner backtracks:  (score=2)
- local clusters: none

### `C6:8200..C6:82FF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=1
- best targets: C6:826E (weak, hits=1); C6:8200 (suspect, hits=1)
- owner backtracks:  (score=4);  (score=-1)
- local clusters: C6:8265..C6:8272

### `C6:8300..C6:83FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=1, soft_bad=0, clusters=3
- best targets: C6:835B (weak, hits=1); C6:8326 (invalid, hits=1)
- owner backtracks:  (score=6);  (score=2)
- local clusters: C6:8300..C6:8309; C6:83B2..C6:83CA

### `C6:8400..C6:84FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: C6:8421 (suspect, hits=1); C6:846E (suspect, hits=1)
- owner backtracks:  (score=4);  (score=2)
- local clusters: C6:847C..C6:8494; C6:8420..C6:8438

### `C6:8500..C6:85FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=1, soft_bad=0, clusters=0
- best targets: C6:8500 (weak, hits=1); C6:85FF (invalid, hits=1) [boundary_bait]
- owner backtracks:  (score=4);  (score=-1)
- local clusters: none
