# Seam block report — C6:FE00 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 2, "candidate_code_lane": 1, "mixed_command_data": 7}`
- review postures: `{"bad_start_or_dead_lane_reject": 5, "manual_owner_boundary_review": 2, "mixed_lane_continue": 3}`

## Page breakdown

### `C6:FE00..C6:FEFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:FE10 (suspect, hits=1); C6:FE3B (suspect, hits=1); C6:FECB (suspect, hits=1)
- owner backtracks: C6:FE2C->C6:FE3B (score=4); C6:FE00->C6:FE10 (score=2); C6:FEC2->C6:FECB (score=2)
- local clusters: none

### `C6:FF00..C6:FFFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=7, xref_hits=13, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=0
- best targets: C6:FF80 (weak, hits=1); C6:FF22 (suspect, hits=6); C6:FF29 (suspect, hits=2)
- owner backtracks: C6:FF01->C6:FF11 (score=2); C6:FF21->C6:FF22 (score=2); C6:FF21->C6:FF29 (score=2)
- local clusters: none

### `C7:0000..C7:00FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=29, xref_hits=113, strong_or_weak=78, hard_bad=7, soft_bad=0, clusters=3
- best targets: C7:0004 (weak, hits=60); C7:0000 (weak, hits=4); C7:00F0 (weak, hits=3)
- owner backtracks: C7:0030->C7:0040 (score=6); C7:004B->C7:004F (score=6); C7:0070->C7:0078 (score=6)
- local clusters: C7:0003..C7:0015; C7:009F..C7:00A9

### `C7:0100..C7:01FF`
- page family: `candidate_code_lane`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=18, xref_hits=31, strong_or_weak=22, hard_bad=1, soft_bad=0, clusters=3
- best targets: C7:0192 (weak, hits=8); C7:01A5 (weak, hits=4); C7:0102 (weak, hits=3)
- owner backtracks: C7:018A->C7:0192 (score=6); C7:0197->C7:01A5 (score=6); C7:0139->C7:0140 (score=4)
- local clusters: C7:0104..C7:010C; C7:016F..C7:017E

### `C7:0200..C7:02FF`
- page family: `branch_fed_control_pocket`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=12, xref_hits=15, strong_or_weak=9, hard_bad=2, soft_bad=0, clusters=2
- best targets: C7:02D6 (weak, hits=3); C7:02FE (weak, hits=2) [boundary_bait]; C7:0201 (weak, hits=1)
- owner backtracks: C7:0266->C7:0268 (score=6); C7:0269->C7:0278 (score=6); C7:02BC->C7:02C7 (score=6)
- local clusters: C7:02AD..C7:02C9; C7:028F..C7:02A7

### `C7:0300..C7:03FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=8, xref_hits=11, strong_or_weak=7, hard_bad=1, soft_bad=0, clusters=4
- best targets: C7:0326 (weak, hits=2); C7:037B (weak, hits=2); C7:03D6 (weak, hits=2)
- owner backtracks: C7:030E->C7:030F (score=6); C7:034A->C7:0358 (score=6); C7:039E->C7:03A5 (score=6)
- local clusters: C7:038D..C7:0395; C7:035D..C7:0364

### `C7:0400..C7:04FF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:04C0 (weak, hits=1); C7:04F9 (weak, hits=1)
- owner backtracks: C7:04EE->C7:04F9 (score=4); C7:04B5->C7:04C0 (score=2)
- local clusters: C7:0400..C7:0415

### `C7:0500..C7:05FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:05A5 (weak, hits=3)
- owner backtracks: C7:05A2->C7:05A5 (score=2)
- local clusters: none

### `C7:0600..C7:06FF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=6, xref_hits=6, strong_or_weak=5, hard_bad=0, soft_bad=1, clusters=2
- best targets: C7:061C (weak, hits=1); C7:062C (weak, hits=1); C7:0655 (weak, hits=1)
- owner backtracks: C7:0616->C7:061C (score=6); C7:0628->C7:062C (score=4); C7:0646->C7:0654 (score=4)
- local clusters: C7:068F..C7:06AA; C7:0669..C7:0681

### `C7:0700..C7:07FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=5, xref_hits=5, strong_or_weak=3, hard_bad=1, soft_bad=0, clusters=3
- best targets: C7:071D (weak, hits=1); C7:0734 (weak, hits=1); C7:07A9 (weak, hits=1)
- owner backtracks: C7:070D->C7:071D (score=6); C7:079D->C7:07A9 (score=6); C7:0734->C7:0734 (score=3)
- local clusters: C7:079B..C7:07BA; C7:0704..C7:071C
