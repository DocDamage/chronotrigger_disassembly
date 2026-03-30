# Seam block report — C5:4500 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 1, "candidate_code_lane": 8, "mixed_command_data": 1}`
- review postures: `{"bad_start_or_dead_lane_reject": 2, "local_control_only": 4, "manual_owner_boundary_review": 2, "mixed_lane_continue": 2}`

## Page breakdown

### `C5:4500..C5:45FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=2
- best targets: C5:45BA (invalid, hits=1)
- owner backtracks:  (score=2)
- local clusters: C5:459A..C5:45B2; C5:450C..C5:451D

### `C5:4600..C5:46FF`
- page family: `candidate_code_lane`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=1
- best targets: C5:4603 (weak, hits=1); C5:46C0 (weak, hits=1)
- owner backtracks:  (score=2);  (score=2)
- local clusters: C5:4647..C5:464F

### `C5:4700..C5:47FF`
- page family: `candidate_code_lane`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=2
- best targets: C5:4728 (weak, hits=1)
- owner backtracks:  (score=2)
- local clusters: C5:4767..C5:476F; C5:4787..C5:4795

### `C5:4800..C5:48FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=4, xref_hits=4, strong_or_weak=2, hard_bad=1, soft_bad=0, clusters=1
- best targets: C5:4805 (weak, hits=1); C5:481E (weak, hits=1); C5:48C0 (suspect, hits=1)
- owner backtracks:  (score=5);  (score=4);  (score=2)
- local clusters: C5:4821..C5:482A

### `C5:4900..C5:49FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C5:498F..C5:49A4

### `C5:4A00..C5:4AFF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C5:4A00..C5:4A17

### `C5:4B00..C5:4BFF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C5:4BEF..C5:4BFF

### `C5:4C00..C5:4CFF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=0
- best targets: C5:4C00 (weak, hits=1); C5:4CDF (weak, hits=1); C5:4CFF (suspect, hits=1) [boundary_bait]
- owner backtracks:  (score=3);  (score=2);  (score=2)
- local clusters: none

### `C5:4D00..C5:4DFF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: C5:4D3F (suspect, hits=1); C5:4DC1 (suspect, hits=1)
- owner backtracks:  (score=4);  (score=4)
- local clusters: C5:4D8C..C5:4D90; C5:4DC5..C5:4DC9

### `C5:4E00..C5:4EFF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=1, clusters=3
- best targets: C5:4E20 (weak, hits=1); C5:4E00 (suspect, hits=1); C5:4E30 (suspect, hits=1)
- owner backtracks:  (score=4);  (score=3);  (score=0)
- local clusters: C5:4E04..C5:4E0A; C5:4E85..C5:4E8C
