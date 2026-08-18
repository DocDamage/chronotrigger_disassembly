# Chrono Trigger Session 15 — Continuation Notes 62

## Block closed: C7:1C00..C7:25FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:1C00 | dead_zero_field | dead_lane_reject | freeze | all candidate starts stay invalid in dead-field bytes |
| C7:1D00 | dead_zero_field | dead_lane_reject | freeze | all candidate starts stay invalid in dead-field bytes |
| C7:1E00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | suspect-only `1EA9` plus invalid `1E11/1E00` under hard-bad page pressure |
| C7:1F00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | suspect-only `1FA9` plus invalid companion starts |
| C7:2000 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | suspect-only `2022` and 13 hard-bad starts in mixed page |
| C7:2100 | dead_zero_field | dead_lane_reject | freeze | suspect-only `2111` plus invalid zero-start landings |
| C7:2200 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | suspect-only `2201/2212/22C1` never rise above mixed hard-bad page pressure |
| C7:2300 | dead_zero_field | dead_lane_reject | freeze | all candidate starts stay invalid in dead-field bytes |
| C7:2400 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | three weak hits (`24AA/24AD/24CC`) still collapse under mixed patterned bytes and a hard-bad companion |
| C7:2500 | mixed_command_data | manual_owner_boundary_review | freeze | lone weak `25C1` plus suspect `2540/25A0`, but all candidate windows stay data-like on byte review |

---

## Manual-owner review summary

One page survived into `manual_owner_boundary_review`:
- `C7:2500..C7:25FF`

### C7:2500..25FF
Summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C7:25C1 (1 weak caller from `C7:C088`)
- C7:2540 (1 suspect caller from `C7:1FA7`)
- C7:25A0 (1 suspect caller from `C7:8C40`)

Backtrack scan:
- C7:253E->2540 score=6
- C7:2599->25A0 score=4
- C7:25C1->25C1 score=1

Anchor reports:
- no target survived byte review strongly enough to justify anchor follow-up

ROM-byte check:
- C7:253E = `A0 1F E8 E0 C5 A1 1F E8 E1 C5 20 1F E8 00 C5 21`
- C7:2540 = `E8 E0 C5 A1 1F E8 E1 C5 20 1F E8 00 C5 21 1F E8`
- C7:2599 = `DA F6 EC 66 F1 E8 00 DA F4 2F 03 3F 38 14 83 87`
- C7:25A0 = `DA F4 2F 03 3F 38 14 83 87 B4 8B BD D0 06 8F 07`
- C7:25C1 = `91 E4 86 48 FF 24 53 24 24 C4 A3 E5 61 F1 C4 A8`

Verdict:
- `2540` and `25A0` get good backtrack scores, but both windows read like dense table/data material rather than coherent helper bodies.
- `25C1` is the only weak-supported target, yet its body bytes read worse than the two suspect-only candidates and do not justify an owner claim.
- The page reached manual review because it avoided the hard-bad gates, not because it held up as executable structure.

**Frozen.**

---

## Reject-heavy page note

### C7:2400..24FF
Summary: raw_targets=6, xref_hits=6, strong_or_weak=3, hard_bad=1, soft_bad=0

Targets:
- C7:24AA (1 weak caller from `C7:8F30`)
- C7:24AD (1 weak caller from `C7:C580`)
- C7:24CC (1 weak caller from `C7:77DB`)
- C7:2478 (1 suspect caller from `C7:2226`)

Backtrack scan from block report:
- C7:2477->2478 score=4
- C7:24CA->24CC score=4
- C7:24AD->24AD score=3

ROM-byte check:
- C7:2477 = `08 F0 07 FF 07 98 06 C0 05 A8 04 A0 04 E0 05 FF`
- C7:2478 = `F0 07 FF 07 98 06 C0 05 A8 04 A0 04 E0 05 FF 05`
- C7:24AA = `8F 0A FF 08 A8 04 DC 0A FF 07 FF 05 FF 0A D8 07`
- C7:24AD = `08 A8 04 DC 0A FF 07 FF 05 FF 0A D8 07 AC 06 FF`
- C7:24CA = `E8 00 5D AF C8 F0 D0 FB 8B 80 1A BB 8D 2C 3F A3`
- C7:24CC = `5D AF C8 F0 D0 FB 8B 80 1A BB 8D 2C 3F A3 07 8D`

Verdict:
- `24AA` and `24AD` are patterned, nibble-heavy data-like starts despite their isolated weak callers.
- `24CC` is the only locally plausible control pocket in the page and explains the local cluster at `24CC..24FB`.
- That still is not enough. All three defended targets are single weak unresolved hits, and the page carries a hard-bad companion landing, so the honest posture remains reject, not owner review.

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **`C7:2500..C7:25FF`** — it reached manual review, but every candidate window still collapsed into data-like bytes before anchor follow-up.
- **Strongest reject signal**: **`C7:2400..C7:24FF`** — three isolated weak hits and one locally plausible cluster still were not enough to overcome mixed patterned bytes plus a hard-bad companion.
- One page reached `manual_owner_boundary_review`, and it still failed on structural byte quality rather than caller count alone.
- The earlier half of the block (`C7:1C00..23FF`) stays consistent with the dead-field corridor seen in the prior two blocks.

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
- C7:1C00..25FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_1c00_25ff_seam_block.json`
- `reports/c7_1c00_25ff_seam_block.md`
- `reports/c7_2500_25ff_backtrack.json`

---

## New live seam: C7:2600..

Next unprocessed block starts at **C7:2600**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:2600 --pages 10 --json > reports/c7_2600_2fff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c7_2600_2fff_seam_block.json --output reports/c7_2600_2fff_seam_block.md`
3. Run owner-backtrack scans only for pages that still land in `manual_owner_boundary_review`, then write notes_63.
