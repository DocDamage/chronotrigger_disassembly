# Seam block report — C7:E400 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 1, "candidate_code_lane": 3, "mixed_command_data": 5, "text_ascii_heavy": 1}`
- review postures: `{"local_control_only": 2, "mixed_lane_continue": 8}`

## Page breakdown

### `C7:E400..C7:E4FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=2, xref_hits=3, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:E4F5 (suspect, hits=2); C7:E4F4 (suspect, hits=1)
- owner backtracks: C7:E4EF->C7:E4F4 (score=2); C7:E4EF->C7:E4F5 (score=2)
- local clusters: C7:E4AC..C7:E4C4

### `C7:E500..C7:E5FF`
- page family: `candidate_code_lane`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:E5CA (suspect, hits=1); C7:E5DF (suspect, hits=1)
- owner backtracks: C7:E5DF->C7:E5DF (score=3); C7:E5C5->C7:E5CA (score=2)
- local clusters: none

### `C7:E600..C7:E6FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C7:E700..C7:E7FF`
- page family: `candidate_code_lane`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:E708 (weak, hits=1)
- owner backtracks: C7:E706->C7:E708 (score=2)
- local clusters: none

### `C7:E800..C7:E8FF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:E81F (suspect, hits=1); C7:E8B9 (suspect, hits=1); C7:E8E8 (suspect, hits=1)
- owner backtracks: C7:E81D->C7:E81F (score=2); C7:E8DC->C7:E8E8 (score=2); C7:E8A9->C7:E8B9 (score=0)
- local clusters: C7:E852..C7:E85C

### `C7:E900..C7:E9FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:E91F (suspect, hits=1); C7:E954 (suspect, hits=1)
- owner backtracks: C7:E91D->C7:E91F (score=4); C7:E950->C7:E954 (score=2)
- local clusters: none

### `C7:EA00..C7:EAFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=3, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:EABF (suspect, hits=2); C7:EA84 (suspect, hits=1)
- owner backtracks: C7:EAB3->C7:EABF (score=4); C7:EA74->C7:EA84 (score=2)
- local clusters: none

### `C7:EB00..C7:EBFF`
- page family: `text_ascii_heavy`
- review posture: `mixed_lane_continue`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=0, soft_bad=1, clusters=0
- best targets: C7:EB06 (suspect, hits=1); C7:EB25 (suspect, hits=1); C7:EB58 (suspect, hits=1)
- owner backtracks: C7:EB00->C7:EB06 (score=2); C7:EB1D->C7:EB25 (score=2); C7:EB54->C7:EB58 (score=2)
- local clusters: none

### `C7:EC00..C7:ECFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:EC01 (suspect, hits=1); C7:EC1E (suspect, hits=1)
- owner backtracks: C7:EC0E->C7:EC1E (score=2); C7:EC01->C7:EC01 (score=1)
- local clusters: none

### `C7:ED00..C7:EDFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:ED00 (suspect, hits=1); C7:ED23 (suspect, hits=1); C7:EDFF (suspect, hits=1) [boundary_bait]
- owner backtracks: C7:ED1E->C7:ED23 (score=4); C7:EDEF->C7:EDFF (score=2); C7:ED00->C7:ED00 (score=-1)
- local clusters: none
