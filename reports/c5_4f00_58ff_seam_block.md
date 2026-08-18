# Seam block report — C5:4F00 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 1, "candidate_code_lane": 6, "mixed_command_data": 3}`
- review postures: `{"bad_start_or_dead_lane_reject": 5, "local_control_only": 2, "manual_owner_boundary_review": 2, "mixed_lane_continue": 1}`

## Page breakdown

### `C5:4F00..C5:4FFF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=1
- best targets: C5:4F76 (weak, hits=1)
- owner backtracks:  (score=4)
- local clusters: C5:4FBD..C5:4FC4

### `C5:5000..C5:50FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=6, xref_hits=6, strong_or_weak=3, hard_bad=1, soft_bad=0, clusters=4
- best targets: C5:5004 (weak, hits=1); C5:5005 (weak, hits=1); C5:50AF (weak, hits=1)
- owner backtracks:  (score=4);  (score=2);  (score=2)
- local clusters: C5:508A..C5:5093; C5:501D..C5:5025

### `C5:5100..C5:51FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=0
- best targets: C5:51B0 (weak, hits=1)
- owner backtracks:  (score=2)
- local clusters: none

### `C5:5200..C5:52FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=2, soft_bad=0, clusters=2
- best targets: C5:5200 (invalid, hits=1); C5:5204 (invalid, hits=1)
- owner backtracks:  (score=-6);  (score=-6)
- local clusters: C5:529B..C5:52A1; C5:5244..C5:5248

### `C5:5300..C5:53FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=2, hard_bad=1, soft_bad=0, clusters=0
- best targets: C5:5360 (weak, hits=1); C5:53DF (weak, hits=1); C5:5308 (invalid, hits=1)
- owner backtracks:  (score=2);  (score=1);  (score=-2)
- local clusters: none

### `C5:5400..C5:54FF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=4, xref_hits=5, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=0
- best targets: C5:54FF (weak, hits=2) [boundary_bait]; C5:54C0 (weak, hits=1); C5:543F (suspect, hits=1)
- owner backtracks:  (score=4);  (score=4);  (score=4)
- local clusters: none

### `C5:5500..C5:55FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=1, soft_bad=0, clusters=1
- best targets: C5:554D (weak, hits=1); C5:550D (invalid, hits=1)
- owner backtracks:  (score=6);  (score=2)
- local clusters: C5:5500..C5:550D

### `C5:5600..C5:56FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C5:566A..C5:5670

### `C5:5700..C5:57FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: C5:5727 (suspect, hits=1)
- owner backtracks:  (score=4)
- local clusters: C5:579D..C5:57AD; C5:57D7..C5:57DB

### `C5:5800..C5:58FF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=3, xref_hits=4, strong_or_weak=1, hard_bad=1, soft_bad=0, clusters=4
- best targets: C5:5839 (weak, hits=1); C5:5800 (suspect, hits=2); C5:58E7 (invalid, hits=1)
- owner backtracks:  (score=6);  (score=4);  (score=-1)
- local clusters: C5:58BC..C5:58C4; C5:583B..C5:5840
