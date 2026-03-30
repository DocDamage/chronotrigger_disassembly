# Seam block report — C5:C800 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 3, "candidate_code_lane": 6, "mixed_command_data": 1}`
- review postures: `{"bad_start_or_dead_lane_reject": 4, "local_control_only": 2, "manual_owner_boundary_review": 2, "mixed_lane_continue": 2}`

## Page breakdown

### `C5:C800..C5:C8FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C5:C855..C5:C85B

### `C5:C900..C5:C9FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: C5:C9FF (suspect, hits=1) [boundary_bait]
- owner backtracks:  (score=0)
- local clusters: C5:C947..C5:C95F; C5:C9C1..C5:C9C9

### `C5:CA00..C5:CAFF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=2, soft_bad=0, clusters=0
- best targets: C5:CA23 (invalid, hits=1); C5:CAF3 (invalid, hits=1)
- owner backtracks:  (score=-4);  (score=-6)
- local clusters: none

### `C5:CB00..C5:CBFF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=3
- best targets: C5:CB02 (weak, hits=1); C5:CB2F (weak, hits=1)
- owner backtracks:  (score=4);  (score=2)
- local clusters: C5:CB70..C5:CB7A; C5:CB4B..C5:CB57

### `C5:CC00..C5:CCFF`
- page family: `candidate_code_lane`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=1
- best targets: C5:CCC0 (weak, hits=1)
- owner backtracks:  (score=2)
- local clusters: C5:CCE0..C5:CCE9

### `C5:CD00..C5:CDFF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=3
- best targets: C5:CD33 (weak, hits=1)
- owner backtracks:  (score=5)
- local clusters: C5:CD3A..C5:CD49; C5:CDC1..C5:CDD2

### `C5:CE00..C5:CEFF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=1, soft_bad=0, clusters=5
- best targets: C5:CEBF (weak, hits=1); C5:CEDF (invalid, hits=1)
- owner backtracks:  (score=2);  (score=-2)
- local clusters: C5:CEE0..C5:CEF6; C5:CE5E..C5:CE71

### `C5:CF00..C5:CFFF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=1, soft_bad=0, clusters=2
- best targets: C5:CF2E (weak, hits=1); C5:CF00 (invalid, hits=1)
- owner backtracks:  (score=2);  (score=-2)
- local clusters: C5:CF00..C5:CF0D; C5:CFAF..C5:CFB3

### `C5:D000..C5:D0FF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=3, strong_or_weak=2, hard_bad=1, soft_bad=0, clusters=2
- best targets: C5:D000 (weak, hits=2); C5:D0DC (invalid, hits=1)
- owner backtracks:  (score=4);  (score=1)
- local clusters: C5:D08E..C5:D092; C5:D0C2..C5:D0C9

### `C5:D100..C5:D1FF`
- page family: `candidate_code_lane`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=4
- best targets: C5:D100 (weak, hits=1); C5:D1C0 (suspect, hits=1)
- owner backtracks:  (score=2);  (score=1)
- local clusters: C5:D1DC..C5:D1E5; C5:D1EA..C5:D1F5
