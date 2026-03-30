# Seam block report — C5:D200 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 5, "candidate_code_lane": 3, "mixed_command_data": 2}`
- review postures: `{"bad_start_or_dead_lane_reject": 2, "local_control_only": 5, "manual_owner_boundary_review": 1, "mixed_lane_continue": 2}`

## Page breakdown

### `C5:D200..C5:D2FF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=2
- best targets: C5:D2E0 (weak, hits=1); C5:D21F (suspect, hits=2)
- owner backtracks:  (score=4);  (score=4)
- local clusters: C5:D237..C5:D24F; C5:D2C0..C5:D2C4

### `C5:D300..C5:D3FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=4
- best targets: none
- owner backtracks: none
- local clusters: C5:D3C2..C5:D3DA; C5:D350..C5:D367

### `C5:D400..C5:D4FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=3
- best targets: C5:D456 (suspect, hits=1)
- owner backtracks:  (score=1)
- local clusters: C5:D480..C5:D491; C5:D478..C5:D47D

### `C5:D500..C5:D5FF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=5
- best targets: none
- owner backtracks: none
- local clusters: C5:D5A9..C5:D5B8; C5:D500..C5:D50E

### `C5:D600..C5:D6FF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C5:D61B..C5:D62B

### `C5:D700..C5:D7FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C5:D716 (suspect, hits=1)
- owner backtracks:  (score=0)
- local clusters: none

### `C5:D800..C5:D8FF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=0
- best targets: C5:D8D0 (suspect, hits=1); C5:D8FF (suspect, hits=1) [boundary_bait]; C5:D870 (invalid, hits=1)
- owner backtracks:  (score=0);  (score=0);  (score=0)
- local clusters: none

### `C5:D900..C5:D9FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C5:D905 (suspect, hits=1); C5:D982 (suspect, hits=1)
- owner backtracks:  (score=0);  (score=-1)
- local clusters: none

### `C5:DA00..C5:DAFF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=2
- best targets: C5:DA12 (suspect, hits=1); C5:DA3F (invalid, hits=1)
- owner backtracks:  (score=4);  (score=0)
- local clusters: C5:DAB2..C5:DABC; C5:DA9F..C5:DAA8

### `C5:DB00..C5:DBFF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=8
- best targets: C5:DB20 (suspect, hits=1)
- owner backtracks:  (score=1)
- local clusters: C5:DB2B..C5:DB3D; C5:DB6D..C5:DB73
