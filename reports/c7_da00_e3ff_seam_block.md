# Seam block report — C7:DA00 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 1, "candidate_code_lane": 1, "mixed_command_data": 7, "text_ascii_heavy": 1}`
- review postures: `{"bad_start_or_dead_lane_reject": 3, "local_control_only": 1, "manual_owner_boundary_review": 3, "mixed_lane_continue": 3}`

## Page breakdown

### `C7:DA00..C7:DAFF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=4, xref_hits=4, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=0
- best targets: C7:DAF0 (suspect, hits=1); C7:DAF4 (suspect, hits=1); C7:DAF5 (suspect, hits=1)
- owner backtracks: C7:DA22->C7:DA31 (score=4); C7:DAEE->C7:DAF0 (score=2); C7:DAEE->C7:DAF4 (score=2)
- local clusters: none

### `C7:DB00..C7:DBFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=1, clusters=0
- best targets: C7:DB58 (suspect, hits=1); C7:DBEB (suspect, hits=1)
- owner backtracks: C7:DB53->C7:DB58 (score=4); C7:DBE8->C7:DBEB (score=2)
- local clusters: none

### `C7:DC00..C7:DCFF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=10, xref_hits=11, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:DC1D (weak, hits=1); C7:DCFC (weak, hits=1); C7:DCD4 (suspect, hits=2)
- owner backtracks: C7:DC07->C7:DC13 (score=4); C7:DC34->C7:DC40 (score=4); C7:DCC4->C7:DCD4 (score=4)
- local clusters: none

### `C7:DD00..C7:DDFF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=7, xref_hits=7, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:DD0D (suspect, hits=1); C7:DD0F (suspect, hits=1); C7:DD20 (suspect, hits=1)
- owner backtracks: C7:DDEE->C7:DDF4 (score=6); C7:DD03->C7:DD0D (score=4); C7:DD03->C7:DD0F (score=4)
- local clusters: C7:DD99..C7:DDA6

### `C7:DE00..C7:DEFF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=2, hard_bad=1, soft_bad=0, clusters=1
- best targets: C7:DED0 (weak, hits=1); C7:DEF2 (weak, hits=1); C7:DEED (invalid, hits=1)
- owner backtracks: C7:DEE0->C7:DEED (score=4); C7:DEF2->C7:DEF2 (score=3); C7:DECF->C7:DED0 (score=2)
- local clusters: C7:DEB7..C7:DEC4

### `C7:DF00..C7:DFFF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=5, xref_hits=5, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=0
- best targets: C7:DF48 (suspect, hits=1); C7:DFB0 (suspect, hits=1); C7:DFC9 (suspect, hits=1)
- owner backtracks: C7:DFAE->C7:DFB0 (score=4); C7:DFB9->C7:DFC9 (score=4); C7:DFDE->C7:DFED (score=2)
- local clusters: none

### `C7:E000..C7:E0FF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=10, xref_hits=14, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:E00D (weak, hits=1); C7:E0A9 (suspect, hits=3); C7:E0E3 (suspect, hits=3)
- owner backtracks: C7:E005->C7:E008 (score=4); C7:E005->C7:E00D (score=4); C7:E0CC->C7:E0CC (score=3)
- local clusters: none

### `C7:E100..C7:E1FF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:E198 (weak, hits=1); C7:E113 (suspect, hits=1); C7:E1FF (suspect, hits=1) [boundary_bait]
- owner backtracks: C7:E188->C7:E198 (score=4); C7:E110->C7:E113 (score=2); C7:E1F9->C7:E1FF (score=2)
- local clusters: none

### `C7:E200..C7:E2FF`
- page family: `text_ascii_heavy`
- review posture: `mixed_lane_continue`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:E2B4 (suspect, hits=1); C7:E2EC (suspect, hits=1); C7:E2F4 (suspect, hits=1)
- owner backtracks: C7:E2B0->C7:E2B4 (score=2); C7:E2EF->C7:E2F4 (score=2); C7:E2EC->C7:E2EC (score=1)
- local clusters: none

### `C7:E300..C7:E3FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:E3DA (suspect, hits=1); C7:E3DD (suspect, hits=1)
- owner backtracks: C7:E3D7->C7:E3DA (score=2); C7:E3DC->C7:E3DD (score=2)
- local clusters: none
