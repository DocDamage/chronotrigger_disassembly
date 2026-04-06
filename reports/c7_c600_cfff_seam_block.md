# Seam block report — C7:C600 (10 pages)

## Summary
- page families: `{"candidate_code_lane": 8, "mixed_command_data": 2}`
- review postures: `{"bad_start_or_dead_lane_reject": 1, "local_control_only": 4, "manual_owner_boundary_review": 2, "mixed_lane_continue": 3}`

## Page breakdown

### `C7:C600..C7:C6FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C7:C700..C7:C7FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=3, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:C70C (suspect, hits=2); C7:C748 (suspect, hits=1)
- owner backtracks: C7:C748->C7:C748 (score=3); C7:C702->C7:C70C (score=2)
- local clusters: none

### `C7:C800..C7:C8FF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:C8B6 (weak, hits=1)
- owner backtracks: C7:C8AF->C7:C8B6 (score=4)
- local clusters: C7:C860..C7:C86D

### `C7:C900..C7:C9FF`
- page family: `candidate_code_lane`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C7:CA00..C7:CAFF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: C7:CA03 (suspect, hits=1)
- owner backtracks: C7:CA01->C7:CA03 (score=4)
- local clusters: C7:CA7E..C7:CA96; C7:CAC1..C7:CAD9

### `C7:CB00..C7:CBFF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:CB6E (suspect, hits=1); C7:CBCD (suspect, hits=1); C7:CBED (suspect, hits=1)
- owner backtracks: C7:CBC4->C7:CBCD (score=4); C7:CB6A->C7:CB6E (score=2); C7:CBEC->C7:CBED (score=2)
- local clusters: C7:CBAF..C7:CBC7

### `C7:CC00..C7:CCFF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:CC14 (suspect, hits=1)
- owner backtracks: C7:CC0F->C7:CC14 (score=4)
- local clusters: C7:CCA3..C7:CCAD

### `C7:CD00..C7:CDFF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=7, xref_hits=7, strong_or_weak=2, hard_bad=1, soft_bad=0, clusters=2
- best targets: C7:CD20 (weak, hits=1); C7:CDEB (weak, hits=1); C7:CD17 (suspect, hits=1)
- owner backtracks: C7:CD09->C7:CD17 (score=4); C7:CD1B->C7:CD20 (score=4); C7:CD1B->C7:CD21 (score=4)
- local clusters: C7:CD91..C7:CDA9; C7:CD53..C7:CD5D

### `C7:CE00..C7:CEFF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=4, xref_hits=4, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=3
- best targets: C7:CE0E (weak, hits=1); C7:CEA0 (suspect, hits=1); C7:CEB0 (suspect, hits=1)
- owner backtracks: C7:CE95->C7:CEA0 (score=4); C7:CEA5->C7:CEB0 (score=4); C7:CEE9->C7:CEEB (score=4)
- local clusters: C7:CE1B..C7:CE33; C7:CEB1..C7:CEBA

### `C7:CF00..C7:CFFF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:CF3E (suspect, hits=1); C7:CFF2 (suspect, hits=1)
- owner backtracks: C7:CF2E->C7:CF3E (score=2); C7:CFEE->C7:CFF2 (score=2)
- local clusters: C7:CF61..C7:CF6F
