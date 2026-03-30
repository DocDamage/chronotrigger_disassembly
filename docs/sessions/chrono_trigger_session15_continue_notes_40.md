# Chrono Trigger Session 15 — Continuation Notes 40

## Block closed: C6:4000..C6:49FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:4000 | text_ascii_heavy | bad_start_or_dead_lane_reject | freeze | text-heavy page with explicit contamination (`hard_bad=2`) |
| C6:4100 | candidate_code_lane | manual_owner_boundary_review | freeze | weak/suspect-only targets with unresolved ownership |
| C6:4200 | mixed_command_data | mixed_lane_continue | freeze | lone suspect target `C6:4254` with `soft_bad=1` |
| C6:4300 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid-only ingress (`C6:4318`, `hard_bad=1`) |
| C6:4400 | mixed_command_data | manual_owner_boundary_review | freeze | weak/suspect set with invalid overlap and no strong anchors |
| C6:4500 | mixed_command_data | local_control_only | freeze | suspect-only target `C6:4520` |
| C6:4600 | candidate_code_lane | mixed_lane_continue | freeze | strong weak-hit volume at `C6:46C4` but no strong anchors |
| C6:4700 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid companion target `C6:470F` (`hard_bad=1`) |
| C6:4800 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | multiple weak hits but still `hard_bad=1` |
| C6:4900 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | invalid-only target `C6:4998` |

---

## Manual-owner pages (anchor detail)

### C6:4100..41FF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:41E6 (weak, caller C6:9DE0)
- C6:4122 (suspect, caller C6:69B3)

Backtrack scan (`reports/c6_4100_41ff_backtrack.json`):
- C6:4120->4122 score=4, start=0x89
- C6:41E5->41E6 score=2, start=0x15

Anchor reports:
- C6:41E6: strong=0, weak=1, invalid=0
- C6:4122: strong=0, weak=1, invalid=2

ROM-byte check:
- C6:41E6 = `1E 00 BF 58 10 C0 1E 00 B1 16 B9 0B`
- C6:4122 = `8A 36 82 36 83 00 36 8B 36 C1 36 84`

Verdict: weak/suspect-only ownership with no strong caller anchors; freeze.

### C6:4400..44FF
Summary: raw_targets=3, xref_hits=4, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:4401 (weak, caller F8:DC41)
- C6:4422 (suspect, callers C6:D866 and C6:D922)
- C6:4420 (suspect, caller C6:D507)

Backtrack scan (`reports/c6_4400_44ff_backtrack.json`):
- C6:4418->4420 score=4, start=0x48
- C6:4418->4422 score=4, start=0x48
- C6:4401->4401 score=3, start=0x08

Anchor reports:
- C6:4401: strong=0, weak=1, invalid=7
- C6:4422: strong=0, weak=2, invalid=3
- C6:4420: strong=0, weak=1, invalid=5

ROM-byte check:
- C6:4401 = `08 84 0C CB 3A CC 3A CD 0C 1A CE 84`
- C6:4422 = `0A 1A 0B 1A 1A 1A 1B 1A 00 1E 1A 1F`
- C6:4420 = `0C 00 0A 1A 0B 1A 1A 1A 1B 1A 00 1E`

Verdict: all candidates remain weak/suspect-only with unresolved ownership and invalid overlap; freeze.

---

## Reject/mixed lane notes

- C6:4000 rejected as `text_ascii_heavy` with `hard_bad=2` despite weak hits (`C6:4008`, `C6:40A7`).
- C6:4200 remains mixed-lane carry with only suspect `C6:4254` and `soft_bad=1`.
- C6:4300 rejected on explicit invalid `C6:4318`.
- C6:4600 remains mixed-lane carry: `C6:46C4` has 8 weak hits, but all caller ownership is unresolved.
- C6:4700 rejected on invalid `C6:470F`.
- C6:4800 rejected on `hard_bad=1` despite weak traffic (`C6:4805`, `C6:48BB`, `C6:483F`).
- C6:4900 is invalid-only (`C6:4998`) and hard rejected.

---

## Running promotion count

- C5:3B00..44FF: 0 promotions (notes_14)
- C5:4500..4EFF: 0 promotions (notes_15)
- C5:4F00..58FF: 0 promotions (notes_16)
- C5:5900..62FF: 0 promotions (notes_17)
- C5:6300..6CFF: 0 promotions (notes_18)
- C5:6D00..76FF: 0 promotions (notes_19)
- C5:7700..80FF: 0 promotions (notes_20)
- C5:8100..8AFF: 0 promotions (notes_21)
- C5:8B00..94FF: 0 promotions (notes_22)
- C5:9500..9EFF: 0 promotions (notes_23)
- C5:A000..A9FF: 0 promotions (notes_24)
- C5:AA00..B3FF: 0 promotions (notes_25)
- C5:B400..BDFF: 0 promotions (notes_26)
- C5:BE00..C7FF: 0 promotions (notes_27)
- C5:C800..D1FF: 0 promotions (notes_28)
- C5:D200..DBFF: 0 promotions (notes_29)
- C5:DC00..E5FF: 0 promotions (notes_30)
- C5:E600..EFFF: 0 promotions (notes_31)
- C5:F000..F9FF: 0 promotions (notes_32)
- C5:FA00..C6:03FF: 0 promotions (notes_33)
- C6:0400..0DFF: 0 promotions (notes_34)
- C6:0E00..17FF: 0 promotions (notes_35)
- C6:1800..21FF: 0 promotions (notes_36)
- C6:2200..2BFF: 0 promotions (notes_37)
- C6:2C00..35FF: 0 promotions (notes_38)
- C6:3600..3FFF: 0 promotions (notes_39)
- C6:4000..49FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_4000_49ff_seam_block.json`
- `reports/c6_4000_49ff_seam_block.md`
- `reports/c6_4100_41ff_backtrack.json`
- `reports/c6_4400_44ff_backtrack.json`
- `reports/c6_4100_41ff_flow.json` (manual-page extraction)
- `reports/c6_4400_44ff_flow.json` (manual-page extraction)
- `reports/C6_41E6_anchor.json`
- `reports/C6_4122_anchor.json`
- `reports/C6_4401_anchor.json`
- `reports/C6_4422_anchor.json`
- `reports/C6_4420_anchor.json`

---

## New live seam: C6:4A00..

Next unprocessed block starts at **C6:4A00**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:4A00 --pages 10 --json > reports/c6_4a00_53ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_4a00_53ff_seam_block.json --output reports/c6_4a00_53ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_41.
