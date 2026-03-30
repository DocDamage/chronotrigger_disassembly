# Seam block report — C6:E000 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 1, "mixed_command_data": 9}`
- review postures: `{"bad_start_or_dead_lane_reject": 4, "local_control_only": 5, "manual_owner_boundary_review": 1}`

## Page breakdown

### `C6:E000..C6:E0FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C6:E000 (suspect, hits=1); C6:E030 (suspect, hits=1); C6:E0E0 (suspect, hits=1)
- owner backtracks: C6:E02E->C6:E030 (score=4); C6:E0DF->C6:E0E0 (score=4); C6:E000->C6:E000 (score=3)
- local clusters: C6:E070..C6:E084

### `C6:E100..C6:E1FF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: C6:E19E (suspect, hits=1)
- owner backtracks: C6:E193->C6:E19E (score=4)
- local clusters: C6:E1EE..C6:E1FE; C6:E174..C6:E180

### `C6:E200..C6:E2FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=2
- best targets: C6:E200 (suspect, hits=1); C6:E201 (suspect, hits=1); C6:E236 (invalid, hits=1)
- owner backtracks: C6:E200->C6:E201 (score=4); C6:E228->C6:E236 (score=4); C6:E200->C6:E200 (score=3)
- local clusters: C6:E226..C6:E236; C6:E245..C6:E251

### `C6:E300..C6:E3FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C6:E357..C6:E367

### `C6:E400..C6:E4FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: C6:E412 (suspect, hits=1); C6:E498 (suspect, hits=1)
- owner backtracks: C6:E489->C6:E498 (score=6); C6:E40B->C6:E412 (score=2)
- local clusters: C6:E487..C6:E497; C6:E441..C6:E447

### `C6:E500..C6:E5FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=1, soft_bad=0, clusters=3
- best targets: C6:E5A5 (weak, hits=1); C6:E5E5 (suspect, hits=1); C6:E521 (invalid, hits=1)
- owner backtracks: C6:E5D9->C6:E5E5 (score=4); C6:E595->C6:E5A5 (score=2); C6:E520->C6:E521 (score=-1)
- local clusters: C6:E588..C6:E594; C6:E522..C6:E52D

### `C6:E600..C6:E6FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=2, xref_hits=3, strong_or_weak=1, hard_bad=2, soft_bad=0, clusters=2
- best targets: C6:E6A2 (weak, hits=1); C6:E621 (invalid, hits=2)
- owner backtracks: C6:E61B->C6:E621 (score=4); C6:E6A0->C6:E6A2 (score=4)
- local clusters: C6:E6A9..C6:E6C1; C6:E63C..C6:E649

### `C6:E700..C6:E7FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=4, xref_hits=5, strong_or_weak=3, hard_bad=1, soft_bad=0, clusters=3
- best targets: C6:E74E (weak, hits=2); C6:E797 (weak, hits=1); C6:E700 (suspect, hits=1)
- owner backtracks: C6:E7F8->C6:E7F9 (score=4); C6:E797->C6:E797 (score=3); C6:E700->C6:E700 (score=1)
- local clusters: C6:E7BE..C6:E7DB; C6:E76A..C6:E77E

### `C6:E800..C6:E8FF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=2
- best targets: C6:E8C7 (weak, hits=2); C6:E830 (suspect, hits=1)
- owner backtracks: C6:E82E->C6:E830 (score=4); C6:E8C7->C6:E8C7 (score=3)
- local clusters: C6:E88C..C6:E891; C6:E85C..C6:E871

### `C6:E900..C6:E9FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C6:E904..C6:E90E; C6:E949..C6:E94E
