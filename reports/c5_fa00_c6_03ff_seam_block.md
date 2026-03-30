# Seam block report — C5:FA00 (10 pages)

## Summary
- page families: `{"candidate_code_lane": 2, "dead_zero_field": 6, "mixed_command_data": 2}`
- review postures: `{"bad_start_or_dead_lane_reject": 3, "dead_lane_reject": 6, "manual_owner_boundary_review": 1}`

## Page breakdown

### `C5:FA00..C5:FAFF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C5:FB00..C5:FBFF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=3, soft_bad=0, clusters=0
- best targets: C5:FB00 (invalid, hits=1); C5:FB04 (invalid, hits=1); C5:FBE2 (invalid, hits=1)
- owner backtracks:  (score=-8);  (score=-8);  (score=-8)
- local clusters: none

### `C5:FC00..C5:FCFF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=4, xref_hits=4, strong_or_weak=0, hard_bad=4, soft_bad=0, clusters=0
- best targets: C5:FC20 (invalid, hits=1); C5:FC58 (invalid, hits=1); C5:FCC3 (invalid, hits=1)
- owner backtracks:  (score=-8);  (score=-8);  (score=-8)
- local clusters: none

### `C5:FD00..C5:FDFF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=6, xref_hits=6, strong_or_weak=0, hard_bad=6, soft_bad=0, clusters=0
- best targets: C5:FD5D (invalid, hits=1); C5:FD7F (invalid, hits=1); C5:FD8C (invalid, hits=1)
- owner backtracks:  (score=-8);  (score=-8);  (score=-8)
- local clusters: none

### `C5:FE00..C5:FEFF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=10, xref_hits=10, strong_or_weak=0, hard_bad=10, soft_bad=0, clusters=0
- best targets: C5:FE00 (invalid, hits=1); C5:FE01 (invalid, hits=1); C5:FE04 (invalid, hits=1)
- owner backtracks:  (score=-8);  (score=-8);  (score=-8)
- local clusters: none

### `C5:FF00..C5:FFFF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=18, xref_hits=44, strong_or_weak=0, hard_bad=44, soft_bad=0, clusters=0
- best targets: C5:FFF0 (invalid, hits=22); C5:FF00 (invalid, hits=5); C5:FF7E (invalid, hits=2)
- owner backtracks:  (score=-8);  (score=-8);  (score=-8)
- local clusters: none

### `C6:0000..C6:00FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=55, xref_hits=82, strong_or_weak=9, hard_bad=3, soft_bad=33, clusters=0
- best targets: C6:0080 (weak, hits=3); C6:00E2 (weak, hits=2); C6:0011 (weak, hits=1)
- owner backtracks:  (score=4);  (score=4);  (score=4)
- local clusters: none

### `C6:0100..C6:01FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=17, xref_hits=19, strong_or_weak=4, hard_bad=7, soft_bad=2, clusters=1
- best targets: C6:0106 (weak, hits=1); C6:017A (weak, hits=1); C6:01D1 (weak, hits=1)
- owner backtracks:  (score=6);  (score=5);  (score=3)
- local clusters: C6:013F..C6:0144

### `C6:0200..C6:02FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=12, xref_hits=13, strong_or_weak=10, hard_bad=1, soft_bad=0, clusters=2
- best targets: C6:0202 (weak, hits=2); C6:0200 (weak, hits=1); C6:0201 (weak, hits=1)
- owner backtracks:  (score=6);  (score=5);  (score=5)
- local clusters: C6:0280..C6:0288; C6:0215..C6:021C

### `C6:0300..C6:03FF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=4, xref_hits=4, strong_or_weak=3, hard_bad=0, soft_bad=0, clusters=2
- best targets: C6:0301 (weak, hits=1); C6:0310 (weak, hits=1); C6:03EE (weak, hits=1)
- owner backtracks:  (score=6);  (score=4);  (score=4)
- local clusters: C6:0380..C6:0392; C6:03CC..C6:03D3
