# Chrono Trigger Session 15 — Continuation Notes 36

## Block closed: C6:1800..C6:21FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:1800 | candidate_code_lane | manual_owner_boundary_review | freeze | weak-only targets, unresolved callers, no strong anchors |
| C6:1900 | candidate_code_lane | mixed_lane_continue | freeze | weak-only carry lane (`sw=3`) with unresolved ownership |
| C6:1A00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | explicit invalid target `C6:1ADE` (`hard_bad=1`) |
| C6:1B00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | weak/suspect mix includes invalid `C6:1B7F` (`hard_bad=1`) |
| C6:1C00 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | four weak hits but still `hard_bad=1` (no credible owner anchors) |
| C6:1D00 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | weak/suspect page with invalid ingress (`hard_bad=1`) |
| C6:1E00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid-only traffic, `hard_bad=9` |
| C6:1F00 | dead_zero_field | dead_lane_reject | freeze | dead zero field with five invalid starts (`hard_bad=5`) |
| C6:2000 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | highest contamination in block (`raw=40`, `xref=45`, `hard_bad=20`) |
| C6:2100 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | mixed weak/suspect traffic plus `hard_bad=3`, `soft_bad=4` |

---

## Manual-owner page (anchor detail)

### C6:1800..18FF
Summary: raw_targets=11, xref_hits=13, strong_or_weak=5, hard_bad=0, soft_bad=1

Targets:
- C6:183F (weak, callers C6:D84E and C6:D906)
- C6:1802 (weak, caller C6:CD23)
- C6:1827 (weak, caller C6:D49A)
- C6:186F (weak, caller C6:BE3D)
- C6:18DB (weak, caller C6:607A)

Backtrack scan (`reports/c6_1800_18ff_backtrack.json`):
- C6:1801->1802 score=6, start=0x0B
- C6:1821->1827 score=6, start=0x20
- C6:186E->186F score=4, start=0x5A
- C6:183D->183F score=2, start=0x7B
- C6:18D9->18DB score=2, start=0xD8

Anchor reports:
- C6:1802: strong=0, weak=1, invalid=11
- C6:1827: strong=0, weak=1, invalid=3
- C6:183F: strong=0, weak=2, invalid=12
- C6:186F: strong=0, weak=1, invalid=0
- C6:18DB: strong=0, weak=1, invalid=1

ROM-byte check:
- C6:1802 = `3F 09 33 04 0F 04 10 20 E8 F8 C0 F8`
- C6:1827 = `34 8F 9B 64 B0 C7 27 7B 1F 60 3D 0B`
- C6:183F = `3F 3F 1B 1F 0F 03 9E 06 8E 10 77 0B`
- C6:186F = `BB F4 AC 72 00 E8 69 27 E9 59 F1 D0`
- C6:18DB = `90 FF F6 C7 6F 00 07 7D 8D 5E F9 1E`

Verdict: all candidates remain weak-only and caller-side ownership is unresolved, with significant invalid overlap on key targets (`1802`, `183F`); freeze.

---

## Reject/mixed lane notes

- C6:1900 remains mixed-lane carry (three weak hits, no strong anchors, unresolved caller ownership).
- C6:1A00 and C6:1B00 are rejected on explicit invalid entries (`C6:1ADE`, `C6:1B7F`).
- C6:1E00 is full invalid-lane contamination (`hard_bad=9`, effective weak/strong=0).
- C6:1F00 remains dead-lane (`dead_zero_field`, five invalid starts).
- C6:2000 is the most contaminated page in this block (`hard_bad=20`, `soft_bad=1`) despite five weak hits.
- C6:2100 stays mixed-command reject (`hard_bad=3`, `soft_bad=4`) with no promotable ownership evidence.

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
- C6:1800..21FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_1800_21ff_seam_block.json`
- `reports/c6_1800_21ff_seam_block.md`
- `reports/c6_1800_18ff_backtrack.json`
- `reports/c6_1800_18ff_flow.json` (manual-page extraction)
- `reports/C6_1802_anchor.json`
- `reports/C6_1827_anchor.json`
- `reports/C6_183F_anchor.json`
- `reports/C6_186F_anchor.json`
- `reports/C6_18DB_anchor.json`

---

## New live seam: C6:2200..

Next unprocessed block starts at **C6:2200**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:2200 --pages 10 --json > reports/c6_2200_2bff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_2200_2bff_seam_block.json --output reports/c6_2200_2bff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_37.
