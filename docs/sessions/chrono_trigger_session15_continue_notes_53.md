# Chrono Trigger Session 15 — Continuation Notes 53

## Block closed: C6:C200..C6:CBFF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:C200 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:C239` with no strong/weak support |
| C6:C300 | mixed_command_data | mixed_lane_continue | freeze | no ingress targets and no surviving local cluster pressure |
| C6:C400 | mixed_command_data | mixed_lane_continue | freeze | only one weak target `C6:C408`, but page stays noisy and non-manual |
| C6:C500 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:C50A` plus soft-bad page pressure |
| C6:C600 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:C700 | mixed_command_data | manual_owner_boundary_review | freeze | `C720` is the best near-miss, but both callers are weak and unresolved |
| C6:C800 | text_ascii_heavy | local_control_only | freeze | text-heavy page with suspect-only `C820/C880` targets |
| C6:C900 | branch_fed_control_pocket | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:CA00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard-bad zero-start targets dominate the page |
| C6:CB00 | branch_fed_control_pocket | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |

---

## Manual-owner page detail

### C6:C700..C7FF
Summary: raw_targets=2, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C6:C720 (2 weak callers from unresolved `C6:E82E` and `C6:E843`)
- C6:C792 (1 suspect caller from frozen `C6:6C00` data page)

Backtrack scan (`reports/c6_c700_c7ff_backtrack.json`):
- C6:C719->C720 score=4, start=0x08
- C6:C78C->C792 score=2, start=0xF8

Anchor reports:
- C6:C720: strong=0, weak=2, invalid=0
- C6:C792: strong=0, weak=0, suspect=1, invalid=0

ROM-byte check:
- C6:C719 = `08 C0 30 35 70 71 72 73 3C F8 01 F8`
- C6:C720 = `73 3C F8 01 F8 23 89 42 60 00 00 2F`
- C6:C78C = `F8 60 F8 01 F8 01 F8 60 F8 01 F8 01`
- C6:C792 = `F8 60 F8 01 F8 01 F8 60 F8 FF 01 F8`

Verdict:
- `C720` is the only target that survives as weak effective strength, and it is the strongest honest near-miss in the block.
- That still is not enough. Both callers remain unresolved.
- `C792` is worse: its only caller sits inside a closed data page, and the target body is visibly contaminated by repeated `F8` patterning.

**Frozen.**

---

## Reject-heavy page note

### C6:CA00..CAFF
Summary: raw_targets=3, xref_hits=4, strong_or_weak=0, hard_bad=3, soft_bad=0

Targets:
- C6:CA6A (1 suspect caller from `C6:2577`)
- C6:CACA (2 invalid callers from `CF:E65F` and `CF:E68E`)
- C6:CACC (1 invalid caller from `C6:BC55`)

Backtrack scan from block report:
- C6:CA66->CA6A score=4
- C6:CACA->CACA score=-6
- C6:CACC->CACC score=-6

ROM-byte check:
- C6:CA66 = `B3 30 B4 30 B5 30 00 B6 30 B7 30 B8`
- C6:CA6A = `B5 30 00 B6 30 B7 30 B8 30 B9 30 80`
- C6:CACA = `00 FA 00 FA 00 FA 00 FA 00 FA 00 FA`
- C6:CACC = `00 FA 00 FA 00 FA 00 FA 00 FA 00 FA`

Verdict:
- `CA00` is the clearest reject page in the block.
- The two busiest targets land directly on `00` hard-bad starts and die immediately.
- The only non-invalid lane, `CA6A`, still never rises above suspect.

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **`C6:C700..C7FF`** — `C720` kept two weak callers, but both are still unresolved and the page does not survive promotion review.
- **Strongest reject signal**: **`C6:CA00..CAFF`** — hard-bad zero-start targets dominate the page and keep the whole branch-fed pocket frozen.
- `C6:C400..C4FF` had some weak/suspect traffic, but it never escalated beyond `mixed_lane_continue` and did not justify manual-owner review.

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
- C6:4000..49FF: 0 promotions (notes_40)
- C6:4A00..53FF: 0 promotions (notes_41)
- C6:5400..5DFF: 0 promotions (notes_42)
- C6:5E00..67FF: 0 promotions (notes_43)
- C6:6800..71FF: 0 promotions (notes_44)
- C6:7200..7BFF: 0 promotions (notes_45)
- C6:7C00..85FF: 0 promotions (notes_46)
- C6:8600..8FFF: 0 promotions (notes_47)
- C6:9000..99FF: 0 promotions (notes_48)
- C6:9A00..A3FF: 0 promotions (notes_49)
- C6:A400..ADFF: 0 promotions (notes_50)
- C6:AE00..B7FF: 0 promotions (notes_51)
- C6:B800..C1FF: 0 promotions (notes_52)
- C6:C200..CBFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_c200_cbff_seam_block.json`
- `reports/c6_c200_cbff_seam_block.md`
- `reports/c6_c700_c7ff_flow.json`
- `reports/c6_c700_c7ff_backtrack.json`
- `reports/C6_C720_anchor.json`
- `reports/C6_C792_anchor.json`

---

## New live seam: C6:CC00..

Next unprocessed block starts at **C6:CC00**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:CC00 --pages 10 --json > reports/c6_cc00_d5ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_cc00_d5ff_seam_block.json --output reports/c6_cc00_d5ff_seam_block.md`
3. Run owner-backtrack scans only for pages that still land in `manual_owner_boundary_review`, then write notes_54.
