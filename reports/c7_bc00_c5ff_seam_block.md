# Seam block report — C7:BC00 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 1, "candidate_code_lane": 7, "mixed_command_data": 2}`
- review postures: `{"local_control_only": 6, "manual_owner_boundary_review": 3, "mixed_lane_continue": 1}`

## Page breakdown

### `C7:BC00..C7:BCFF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C7:BD00..C7:BDFF`
- page family: `branch_fed_control_pocket`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: none
- owner backtracks: none
- local clusters: C7:BD36..C7:BD4E; C7:BD05..C7:BD18

### `C7:BE00..C7:BEFF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: C7:BE00 (suspect, hits=1)
- owner backtracks: C7:BE00->C7:BE00 (score=1)
- local clusters: C7:BE66..C7:BE74; C7:BE79..C7:BE81

### `C7:BF00..C7:BFFF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=1, clusters=2
- best targets: C7:BFCB (suspect, hits=1)
- owner backtracks: C7:BFC8->C7:BFCB (score=4)
- local clusters: C7:BF26..C7:BF65; C7:BF79..C7:BF7F

### `C7:C000..C7:C0FF`
- page family: `mixed_command_data`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=5, xref_hits=5, strong_or_weak=3, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:C021 (weak, hits=1); C7:C0B1 (weak, hits=1); C7:C0F0 (weak, hits=1)
- owner backtracks: C7:C0A4->C7:C0B1 (score=4); C7:C011->C7:C021 (score=2); C7:C0E9->C7:C0F0 (score=2)
- local clusters: none

### `C7:C100..C7:C1FF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=4, xref_hits=4, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=2
- best targets: C7:C1FF (weak, hits=1) [boundary_bait]; C7:C120 (suspect, hits=1); C7:C155 (suspect, hits=1)
- owner backtracks: C7:C1EF->C7:C1FF (score=4); C7:C112->C7:C120 (score=2); C7:C150->C7:C155 (score=2)
- local clusters: C7:C193..C7:C1B2; C7:C1B6..C7:C1CE

### `C7:C200..C7:C2FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=3
- best targets: none
- owner backtracks: none
- local clusters: C7:C20F..C7:C21A; C7:C200..C7:C206

### `C7:C300..C7:C3FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=3
- best targets: C7:C302 (suspect, hits=1); C7:C3FA (suspect, hits=1)
- owner backtracks: C7:C300->C7:C302 (score=2); C7:C3F7->C7:C3FA (score=2)
- local clusters: C7:C3AE..C7:C3C6; C7:C388..C7:C392

### `C7:C400..C7:C4FF`
- page family: `candidate_code_lane`
- review posture: `local_control_only`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:C400 (suspect, hits=1); C7:C4EB (suspect, hits=1); C7:C4F3 (suspect, hits=1)
- owner backtracks: C7:C4EA->C7:C4EB (score=2); C7:C4EA->C7:C4F3 (score=2); C7:C400->C7:C400 (score=1)
- local clusters: C7:C4AA..C7:C4B3

### `C7:C500..C7:C5FF`
- page family: `candidate_code_lane`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0, clusters=2
- best targets: C7:C5B0 (weak, hits=1)
- owner backtracks: C7:C5AC->C7:C5B0 (score=6)
- local clusters: C7:C59D..C7:C5B5; C7:C547..C7:C55F
