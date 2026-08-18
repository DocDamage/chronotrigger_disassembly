# Seam block report — C5:8100 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 2, "candidate_code_lane": 5, "mixed_command_data": 3}`
- review postures: `{"bad_start_or_dead_lane_reject": 3, "local_control_only": 3, "manual_owner_boundary_review": 2, "mixed_lane_continue": 2}`

## Page breakdown

### `C5:8100..C5:81FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=2
- best targets: C5:8140 (invalid, hits=1)
- owner backtracks:  (score=0)
- local clusters: C5:8106..C5:8115; C5:81AE..C5:81B9

### `C5:8200..C5:82FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=4, xref_hits=5, strong_or_weak=0, hard_bad=2, soft_bad=0, clusters=1
- best targets: C5:8261 (suspect, hits=2); C5:82B9 (suspect, hits=1); C5:8204 (invalid, hits=1)
- owner backtracks:  (score=4);  (score=4);  (score=2)
- local clusters: C5:82E7..C5:82EE

### `C5:8300..C5:83FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C5:830F (suspect, hits=1)
- owner backtracks:  (score=2)
- local clusters: C5:8340..C5:8355

### `C5:8400..C5:84FF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=4
- best targets: C5:8498 (weak, hits=1); C5:84CF (weak, hits=1)
- owner backtracks:  (score=4);  (score=4)
- local clusters: C5:8493..C5:849F; C5:841C..C5:8420

### `C5:8500..C5:85FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=2, soft_bad=0, clusters=2
- best targets: C5:85FB (weak, hits=1); C5:8500 (invalid, hits=1); C5:85FF (invalid, hits=1) [boundary_bait]
- owner backtracks:  (score=2);  (score=2);  (score=-4)
- local clusters: C5:857D..C5:858A; C5:851E..C5:8524

### `C5:8600..C5:86FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=2
- best targets: C5:869C (weak, hits=1)
- owner backtracks:  (score=2)
- local clusters: C5:8639..C5:8648; C5:86E8..C5:86EE

### `C5:8700..C5:87FF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=2
- best targets: C5:8712 (weak, hits=1)
- owner backtracks:  (score=4)
- local clusters: C5:873B..C5:8756; C5:8788..C5:8792

### `C5:8800..C5:88FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=4, xref_hits=4, strong_or_weak=3, hard_bad=0, soft_bad=0, clusters=2
- best targets: C5:8800 (weak, hits=1); C5:8802 (weak, hits=1); C5:8877 (weak, hits=1)
- owner backtracks:  (score=2);  (score=2);  (score=1)
- local clusters: C5:88DA..C5:88E1; C5:88AB..C5:88B7

### `C5:8900..C5:89FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=4
- best targets: none
- owner backtracks: none
- local clusters: C5:8900..C5:890F; C5:8912..C5:8921

### `C5:8A00..C5:8AFF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C5:8A18..C5:8A26
