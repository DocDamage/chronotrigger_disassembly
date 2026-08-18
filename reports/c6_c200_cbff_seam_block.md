# Seam block report — C6:C200 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 3, "mixed_command_data": 6, "text_ascii_heavy": 1}`
- review postures: `{"bad_start_or_dead_lane_reject": 1, "local_control_only": 6, "manual_owner_boundary_review": 1, "mixed_lane_continue": 2}`

## Page breakdown

### `C6:C200..C6:C2FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C6:C239 (suspect, hits=1)
- owner backtracks: C6:C22E->C6:C239 (score=2)
- local clusters: C6:C200..C6:C229

### `C6:C300..C6:C3FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C6:C400..C6:C4FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=4, xref_hits=4, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:C408 (weak, hits=1); C6:C400 (suspect, hits=1); C6:C42C (suspect, hits=1)
- owner backtracks: C6:C400->C6:C408 (score=2); C6:C41C->C6:C42C (score=2); C6:C400->C6:C400 (score=1)
- local clusters: none

### `C6:C500..C6:C5FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=1, clusters=1
- best targets: C6:C50A (suspect, hits=1)
- owner backtracks: C6:C507->C6:C50A (score=0)
- local clusters: C6:C5BC..C6:C5DF

### `C6:C600..C6:C6FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C6:C690..C6:C69F

### `C6:C700..C6:C7FF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:C720 (weak, hits=2); C6:C792 (suspect, hits=1)
- owner backtracks: C6:C719->C6:C720 (score=4); C6:C78C->C6:C792 (score=2)
- local clusters: none

### `C6:C800..C6:C8FF`
- page family: `text_ascii_heavy`
- review posture: `local_control_only`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=1, clusters=4
- best targets: C6:C820 (suspect, hits=1); C6:C880 (suspect, hits=1)
- owner backtracks: C6:C81B->C6:C820 (score=4); C6:C87D->C6:C880 (score=4)
- local clusters: C6:C819..C6:C827; C6:C89F..C6:C8AD

### `C6:C900..C6:C9FF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C6:C9B2..C6:C9BD; C6:C9CE..C6:C9D5

### `C6:CA00..C6:CAFF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=3, xref_hits=4, strong_or_weak=0, hard_bad=3, soft_bad=0, clusters=2
- best targets: C6:CA6A (suspect, hits=1); C6:CACA (invalid, hits=2); C6:CACC (invalid, hits=1)
- owner backtracks: C6:CA66->C6:CA6A (score=4); C6:CACA->C6:CACA (score=-6); C6:CACC->C6:CACC (score=-6)
- local clusters: C6:CA6D..C6:CA7E; C6:CA94..C6:CAA0

### `C6:CB00..C6:CBFF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C6:CBAE..C6:CBCB
