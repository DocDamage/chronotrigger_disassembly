# Seam block report — C5:F000 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 2, "candidate_code_lane": 1, "dead_zero_field": 6, "mixed_command_data": 1}`
- review postures: `{"bad_start_or_dead_lane_reject": 3, "dead_lane_reject": 6, "manual_owner_boundary_review": 1}`

## Page breakdown

### `C5:F000..C5:F0FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=14, xref_hits=18, strong_or_weak=10, hard_bad=5, soft_bad=0, clusters=2
- best targets: C5:F000 (weak, hits=2); C5:F018 (weak, hits=1); C5:F01A (weak, hits=1)
- owner backtracks:  (score=4);  (score=4);  (score=4)
- local clusters: C5:F0DE..C5:F0EE; C5:F093..C5:F0A2

### `C5:F100..C5:F1FF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=2
- best targets: C5:F1A0 (weak, hits=1); C5:F140 (suspect, hits=1)
- owner backtracks:  (score=4);  (score=1)
- local clusters: C5:F107..C5:F11C; C5:F15C..C5:F164

### `C5:F200..C5:F2FF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=1
- best targets: C5:F2FA (invalid, hits=1)
- owner backtracks:  (score=0)
- local clusters: C5:F2A6..C5:F2BE

### `C5:F300..C5:F3FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=5, xref_hits=5, strong_or_weak=2, hard_bad=3, soft_bad=0, clusters=0
- best targets: C5:F300 (weak, hits=1); C5:F304 (weak, hits=1); C5:F380 (invalid, hits=1)
- owner backtracks:  (score=0);  (score=-1);  (score=-8)
- local clusters: none

### `C5:F400..C5:F4FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=2, soft_bad=0, clusters=0
- best targets: C5:F400 (invalid, hits=1); C5:F409 (invalid, hits=1)
- owner backtracks:  (score=-8);  (score=-8)
- local clusters: none

### `C5:F500..C5:F5FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C5:F600..C5:F6FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=2, soft_bad=0, clusters=0
- best targets: C5:F609 (invalid, hits=1); C5:F6E3 (invalid, hits=1)
- owner backtracks:  (score=-8);  (score=-8)
- local clusters: none

### `C5:F700..C5:F7FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=2, soft_bad=0, clusters=0
- best targets: C5:F700 (invalid, hits=1); C5:F748 (invalid, hits=1)
- owner backtracks:  (score=-8);  (score=-8)
- local clusters: none

### `C5:F800..C5:F8FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=5, xref_hits=6, strong_or_weak=0, hard_bad=6, soft_bad=0, clusters=0
- best targets: C5:F810 (invalid, hits=2); C5:F803 (invalid, hits=1); C5:F818 (invalid, hits=1)
- owner backtracks:  (score=-8);  (score=-8);  (score=-8)
- local clusters: none

### `C5:F900..C5:F9FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=3, soft_bad=0, clusters=0
- best targets: C5:F920 (invalid, hits=1); C5:F986 (invalid, hits=1); C5:F9CE (invalid, hits=1)
- owner backtracks:  (score=-8);  (score=-8);  (score=-8)
- local clusters: none
