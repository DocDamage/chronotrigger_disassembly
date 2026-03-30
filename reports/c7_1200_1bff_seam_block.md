# Seam block report — C7:1200 (10 pages)

## Summary
- page families: `{"dead_zero_field": 8, "mixed_command_data": 2}`
- review postures: `{"bad_start_or_dead_lane_reject": 1, "dead_lane_reject": 8, "local_control_only": 1}`

## Page breakdown

### `C7:1200..C7:12FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=7, xref_hits=9, strong_or_weak=0, hard_bad=7, soft_bad=0, clusters=0
- best targets: C7:1211 (suspect, hits=2); C7:12DE (invalid, hits=2); C7:120F (invalid, hits=1)
- owner backtracks: C7:1211->C7:1211 (score=-3); C7:12ED->C7:12ED (score=-6); C7:12EF->C7:12EF (score=-6)
- local clusters: none

### `C7:1300..C7:13FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=5, xref_hits=6, strong_or_weak=0, hard_bad=6, soft_bad=0, clusters=0
- best targets: C7:13EC (invalid, hits=2); C7:130F (invalid, hits=1); C7:13DE (invalid, hits=1)
- owner backtracks: C7:130F->C7:130F (score=-6); C7:13DE->C7:13DE (score=-8); C7:13DF->C7:13DF (score=-8)
- local clusters: none

### `C7:1400..C7:14FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=5, xref_hits=5, strong_or_weak=0, hard_bad=5, soft_bad=0, clusters=0
- best targets: C7:140D (invalid, hits=1); C7:1410 (invalid, hits=1); C7:14B3 (invalid, hits=1)
- owner backtracks: C7:140D->C7:140D (score=-8); C7:1410->C7:1410 (score=-8); C7:14B3->C7:14B3 (score=-8)
- local clusters: none

### `C7:1500..C7:15FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=0
- best targets: C7:15EE (invalid, hits=1)
- owner backtracks: C7:15EE->C7:15EE (score=-6)
- local clusters: none

### `C7:1600..C7:16FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=0
- best targets: C7:16F0 (invalid, hits=1)
- owner backtracks: C7:16F0->C7:16F0 (score=-8)
- local clusters: none

### `C7:1700..C7:17FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=2, soft_bad=0, clusters=0
- best targets: C7:17B0 (invalid, hits=1); C7:17B2 (invalid, hits=1)
- owner backtracks: C7:17B0->C7:17B0 (score=-8); C7:17B2->C7:17B2 (score=-8)
- local clusters: none

### `C7:1800..C7:18FF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=4, xref_hits=5, strong_or_weak=0, hard_bad=5, soft_bad=0, clusters=0
- best targets: C7:1898 (invalid, hits=2); C7:1824 (invalid, hits=1); C7:18BF (invalid, hits=1)
- owner backtracks: C7:18ED->C7:18F0 (score=0); C7:1824->C7:1824 (score=-8); C7:1898->C7:1898 (score=-8)
- local clusters: none

### `C7:1900..C7:19FF`
- page family: `mixed_command_data`
- review posture: `local_control_only`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=1
- best targets: none
- owner backtracks: none
- local clusters: C7:194F..C7:1957

### `C7:1A00..C7:1AFF`
- page family: `dead_zero_field`
- review posture: `dead_lane_reject`
- summary: raw_targets=0, xref_hits=0, strong_or_weak=0, hard_bad=0, soft_bad=0, clusters=0
- best targets: none
- owner backtracks: none
- local clusters: none

### `C7:1B00..C7:1BFF`
- page family: `mixed_command_data`
- review posture: `bad_start_or_dead_lane_reject`
- summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0, clusters=1
- best targets: C7:1B4B (invalid, hits=1)
- owner backtracks: C7:1B4B->C7:1B4B (score=-4)
- local clusters: C7:1B71..C7:1B7B
