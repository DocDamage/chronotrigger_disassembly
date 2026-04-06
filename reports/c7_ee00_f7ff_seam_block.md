# Seam block report — C7:EE00 (10 pages)

## Summary
- page families: `{"branch_fed_control_pocket": 1, "mixed_command_data": 5, "text_ascii_heavy": 4}`
- review postures: `{"bad_start_or_dead_lane_reject": 3, "local_control_only": 2, "manual_owner_boundary_review": 1, "mixed_lane_continue": 4}`

## Page breakdown

### `C7:EE00..C7:EEFF`
- page family: `text_ascii_heavy`
- review posture: `local_control_only`
- summary: raw_targets=3, xref_hits=3, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=2
- best targets: C7:EE24 (suspect, hits=1); C7:EEFE (suspect, hits=1) [boundary_bait]; C7:EEFF (suspect, hits=1) [boundary_bait]
- owner backtracks: C7:EE1E->C7:EE24 (score=4); C7:EEFC->C7:EEFE (score=4); C7:EEFC->C7:EEFF (score=4)
- local clusters: C7:EE4F..C7:EE67; C7:EE2F..C7:EE34

### `C7:EF00..C7:EFFF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=8, xref_hits=8, strong_or_weak=2, hard_bad=1, soft_bad=0, clusters=0
- best targets: C7:EFCB (weak, hits=1); C7:EFEB (weak, hits=1); C7:EF1F (suspect, hits=1)
- owner backtracks: C7:EF05->C7:EF11 (score=2); C7:EF1D->C7:EF1F (score=2); C7:EF74->C7:EF80 (score=2)
- local clusters: none

### `C7:F000..C7:F0FF`
- page family: `text_ascii_heavy`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=14, xref_hits=15, strong_or_weak=3, hard_bad=1, soft_bad=0, clusters=0
- best targets: C7:F0FE (weak, hits=2) [boundary_bait]; C7:F0EF (weak, hits=1); C7:F01E (suspect, hits=1)
- owner backtracks: C7:F0A9->C7:F0AF (score=4); C7:F0A9->C7:F0B0 (score=4); C7:F00E->C7:F01E (score=2)
- local clusters: none

### `C7:F100..C7:F1FF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=12, xref_hits=12, strong_or_weak=1, hard_bad=2, soft_bad=0, clusters=0
- best targets: C7:F1EC (weak, hits=1); C7:F101 (suspect, hits=1); C7:F102 (suspect, hits=1)
- owner backtracks: C7:F18E->C7:F194 (score=4); C7:F1E7->C7:F1EB (score=4); C7:F1E7->C7:F1EC (score=4)
- local clusters: none

### `C7:F200..C7:F2FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:F2DC (suspect, hits=1)
- owner backtracks: C7:F2D8->C7:F2DC (score=2)
- local clusters: none

### `C7:F300..C7:F3FF`
- page family: `branch_fed_control_pocket`
- review posture: `manual_owner_boundary_review`
- summary: raw_targets=5, xref_hits=5, strong_or_weak=2, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:F3CC (weak, hits=1); C7:F3EA (weak, hits=1); C7:F3BC (suspect, hits=1)
- owner backtracks: C7:F3BE->C7:F3C4 (score=4); C7:F3E5->C7:F3EA (score=4); C7:F3E5->C7:F3EF (score=4)
- local clusters: none

### `C7:F400..C7:F4FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: C7:F410 (suspect, hits=1); C7:F4C4 (suspect, hits=1)
- owner backtracks: C7:F403->C7:F410 (score=4); C7:F4B4->C7:F4C4 (score=2)
- local clusters: C7:F4D9..C7:F4E5

### `C7:F500..C7:F5FF`
- page family: `mixed_command_data`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C7:F600..C7:F6FF`
- page family: `text_ascii_heavy`
- review posture: `mixed_lane_continue`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: C7:F60F (suspect, hits=1)
- owner backtracks: C7:F603->C7:F60F (score=0)
- local clusters: none

### `C7:F700..C7:F7FF`
- page family: `text_ascii_heavy`
- review posture: `mixed_lane_continue`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none
