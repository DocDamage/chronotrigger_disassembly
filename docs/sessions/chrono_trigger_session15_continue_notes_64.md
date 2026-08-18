# Chrono Trigger Session 15 — Continuation Notes 64

## Block closed: C7:3000..C7:39FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:3000 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | weak `3023/30B0/30EC` still collapse under patterned bytes and a hard-bad companion |
| C7:3100 | candidate_code_lane | manual_owner_boundary_review | freeze | `3120` is locally arguable but stays weak-only; `31FE` is boundary bait and `3133` stays suspect |
| C7:3200 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | `3222/32CE` backtrack cleanly, but caller quality and body bytes still do not support ownership |
| C7:3300 | mixed_command_data | mixed_lane_continue | freeze | weak `3312/330E/33CF` never converge into a defensible owner lane |
| C7:3400 | mixed_command_data | manual_owner_boundary_review | freeze | lone weak `34EE` plus suspect `3402/34DE`, but all three windows stay mixed on byte review |
| C7:3500 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | suspect `350E/35CA` plus invalid `3524` companion start |
| C7:3600 | mixed_command_data | local_control_only | freeze | local control cluster only, no ingress targets (`raw=0`, `xref=0`) |
| C7:3700 | branch_fed_control_pocket | local_control_only | freeze | local control clusters only, no ingress targets (`raw=0`, `xref=0`) |
| C7:3800 | mixed_command_data | mixed_lane_continue | freeze | weak `3816` plus suspect `38A3` with soft-bad page pressure |
| C7:3900 | mixed_command_data | local_control_only | freeze | local control cluster only, no ingress targets (`raw=0`, `xref=0`) |

---

## Manual-owner review summary

Two pages survived into `manual_owner_boundary_review`:
- `C7:3100..C7:31FF`
- `C7:3400..C7:34FF`

### C7:3100..31FF
Summary: raw_targets=3, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C7:3120 (1 weak caller from `C7:A297`)
- C7:31FE (1 weak caller from `C7:AC9A`) [boundary_bait]
- C7:3133 (1 suspect caller from `C7:F343`)

Backtrack scan:
- C7:3110->3120 score=4
- C7:312F->3133 score=2
- C7:31F2->31FE score=2

Anchor reports:
- `C7:3120` = **weak / unresolved**
- `C7:31FE` stayed boundary bait and `C7:3133` stayed suspect-only, so neither justified anchor follow-up

ROM-byte check:
- C7:3110 = `F0 E6 4D 3F 5F 0E CE D5 6C F1 DD D5 6D F1 E8 00`
- C7:3120 = `D5 60 F1 6F 0D B0 03 48 FF BC F8 8E 8D 00 9E C4`
- C7:312F = `C4 B6 E8 00 9E C4 B5 8E B0 08 58 FF B5 58 FF B6`
- C7:3133 = `9E C4 B5 8E B0 08 58 FF B5 58 FF B6 3A B5 BA B5`
- C7:31F2 = `53 C4 54 C4 58 C4 56 9C C4 80 C4 BB C4 BC 6F 03`
- C7:31FE = `C4 BC 6F 03 8E 32 E4 86 28 C0 0E 23 00 4E 22 00`

Verdict:
- `3120` is the only locally arguable start in the page.
- That still is not enough. Its only anchor remains weak and unresolved, `31FE` is boundary bait, and `3133` never rises above suspect.
- The page freezes because caller quality and local structure never converge.

**Frozen.**

### C7:3400..34FF
Summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C7:34EE (1 weak caller from `C7:7B53`)
- C7:3402 (1 suspect caller from `C7:9E05`)
- C7:34DE (1 suspect caller from `C7:80D4`)

Backtrack scan:
- C7:34D8->34DE score=4
- C7:3401->3402 score=2
- C7:34DE->34EE score=2

Anchor reports:
- no target survived byte review strongly enough to justify anchor follow-up

ROM-byte check:
- C7:3401 = `E1 E8 F0 2E F5 DC C4 8E 5F BD 12 DD 28 7F FD E5`
- C7:3402 = `E8 F0 2E F5 DC C4 8E 5F BD 12 DD 28 7F FD E5 0B`
- C7:34D8 = `DA 9B D8 F4 DD F0 28 BA 97 C5 2D 12 CC 2E 12 BA`
- C7:34DE = `28 BA 97 C5 2D 12 CC 2E 12 BA 99 C5 30 12 CC 31`
- C7:34EE = `12 8D 00 F6 97 00 D6 97 00 FC D0 F7 AB 98 AB 9A`

Verdict:
- `3402` and `34DE` backtrack cleanly enough to demand a look, but both windows remain mixed control/data rather than executable entry bodies.
- `34EE` is the lone weak-supported target, yet it reads more like an interior continuation than a defensible owner start.
- The page does not survive beyond byte review.

**Frozen.**

---

## Reject-heavy page note

### C7:3200..32FF
Summary: raw_targets=6, xref_hits=7, strong_or_weak=2, hard_bad=1, soft_bad=0

Targets:
- C7:3222 (1 weak caller from `C7:7740`)
- C7:32CE (1 weak caller from `C7:8F41`)
- C7:3258 (2 suspect callers from `C7:F20C`, `C7:F3E0`)

Backtrack scan from block report:
- C7:32C2->32CE score=6
- C7:321E->3222 score=4
- C7:3250->3258 score=4

ROM-byte check:
- C7:321E = `0B A4 90 0C E8 C1 D4 02 E8 1D D4 03 E8 02 D4 26`
- C7:3222 = `E8 C1 D4 02 E8 1D D4 03 E8 02 D4 26 1D 1D 4B 91`
- C7:3250 = `20 91 0B A4 90 0C E8 C1 D4 02 E8 1D D4 03 E8 02`
- C7:3258 = `D4 02 E8 1D D4 03 E8 02 D4 26 1D 1D 4B 91 73 91`
- C7:32C2 = `08 80 C4 F3 DD 60 88 10 FD 10 F1 92 87 8F FF D0`
- C7:32CE = `87 8F FF D0 6F 7D BC 28 7F C4 9B E4 F4 F0 FC 64`

Verdict:
- `3200` is the strongest reject signal in the block because it looks more promising than it is: branch-fed pocket, decent backtracks, and real ingress.
- That still does not hold up. The weak-supported starts stay unresolved-only, the suspect pair never upgrades, and the page still carries hard-bad reject pressure.
- This is reject-heavy mixed content, not a promotable owner lane.

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **`C7:3100..C7:31FF`** — `3120` survived long enough to justify anchor follow-up, but it still ended as a lone weak unresolved start next to boundary-bait and suspect-only alternatives.
- **Strongest reject signal**: **`C7:3200..C7:32FF`** — branch-fed pocket with real backtracks and ingress, but still reject-heavy once caller quality and byte structure are both weighed.
- Two pages reached `manual_owner_boundary_review`, and both still failed on byte-level structure before any promotion case could form.
- `C7:3600`, `C7:3700`, and `C7:3900` continue to show local-control pockets without any ingress strong enough to matter.

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
- C6:C200..CBFF: 0 promotions (notes_53)
- C6:CC00..D5FF: 0 promotions (notes_54)
- C6:D600..DFFF: 0 promotions (notes_55)
- C6:E000..E9FF: 0 promotions (notes_56)
- C6:EA00..F3FF: 0 promotions (notes_57)
- C6:F400..FDFF: 0 promotions (notes_58)
- C6:FE00..C7:07FF: 0 promotions (notes_59)
- C7:0800..11FF: 0 promotions (notes_60)
- C7:1200..1BFF: 0 promotions (notes_61)
- C7:1C00..25FF: 0 promotions (notes_62)
- C7:2600..2FFF: 0 promotions (notes_63)
- C7:3000..39FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_3000_39ff_seam_block.json`
- `reports/c7_3000_39ff_seam_block.md`
- `reports/c7_3100_31ff_backtrack.json`
- `reports/c7_3400_34ff_backtrack.json`
- `reports/C7_3120_anchor.json`

---

## New live seam: C7:3A00..

Next unprocessed block starts at **C7:3A00**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:3A00 --pages 10 --json > reports/c7_3a00_43ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c7_3a00_43ff_seam_block.json --output reports/c7_3a00_43ff_seam_block.md`
3. Run owner-backtrack scans only for pages that still land in `manual_owner_boundary_review`, then write notes_65.
