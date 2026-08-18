# Chrono Trigger Session 15 — Continuation Notes 63

## Block closed: C7:2600..C7:2FFF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:2600 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | suspect `264F` plus invalid `26C6` companion in patterned bytes |
| C7:2700 | branch_fed_control_pocket | local_control_only | freeze | local clusters only, no ingress targets (`raw=0`, `xref=0`) |
| C7:2800 | branch_fed_control_pocket | local_control_only | freeze | lone suspect `2840` with no strong/weak caller support |
| C7:2900 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | suspect `293A` collapses next to invalid `2940` companion target |
| C7:2A00 | mixed_command_data | local_control_only | freeze | local clusters only, no ingress targets (`raw=0`, `xref=0`) |
| C7:2B00 | candidate_code_lane | manual_owner_boundary_review | freeze | lone weak `2B46` still collapses under table-like body bytes |
| C7:2C00 | mixed_command_data | manual_owner_boundary_review | freeze | weak `2C05/2C0F/2C12` and suspect `2C90/2C35` all stay data-like on byte review |
| C7:2D00 | mixed_command_data | manual_owner_boundary_review | freeze | `2DE6` gets score-6 backtrack but remains patterned/data-like; `2D21` weak-only |
| C7:2E00 | candidate_code_lane | manual_owner_boundary_review | freeze | weak `2E03/2EE4` and boundary-bait `2EFE` never read as coherent code |
| C7:2F00 | candidate_code_lane | manual_owner_boundary_review | freeze | busiest manual page in block, but `2F07/2FE0/2FE1/2F33` all remain patterned/data windows |

---

## Manual-owner review summary

Five pages survived into `manual_owner_boundary_review`:
- `C7:2B00..C7:2BFF`
- `C7:2C00..C7:2CFF`
- `C7:2D00..C7:2DFF`
- `C7:2E00..C7:2EFF`
- `C7:2F00..C7:2FFF`

### C7:2B00..2BFF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C7:2B46 (1 weak caller from `C7:CB4A`)

Backtrack scan:
- C7:2B44->2B46 score=4

Anchor reports:
- no target survived byte review strongly enough to justify anchor follow-up

ROM-byte check:
- C7:2B44 = `3A 9B E4 9B D5 E0 F3 E4 9C D5 E1 F3 F5 40 F3 D5`
- C7:2B46 = `E4 9B D5 E0 F3 E4 9C D5 E1 F3 F5 40 F3 D5 41 F3`

Verdict:
- `2B46` is weak-supported, but the byte stream is a dense repeating pattern rather than a believable helper body.
- With only one unresolved weak caller and no cleaner neighboring lane, the page does not justify an owner split.

**Frozen.**

### C7:2C00..2CFF
Summary: raw_targets=5, xref_hits=7, strong_or_weak=3, hard_bad=0, soft_bad=0

Targets:
- C7:2C05 (1 weak caller from `C7:D095`)
- C7:2C0F (1 weak caller from `C7:AA08`)
- C7:2C12 (1 weak caller from `C7:A5A9`)
- C7:2C90 (3 suspect callers from closed pages `C7:0549`, `C7:06CA`, `C7:07DC`)
- C7:2C35 (1 suspect caller from `C7:4443`)

Backtrack scan:
- C7:2C06->2C0F score=4
- C7:2C06->2C12 score=4
- C7:2C33->2C35 score=4
- C7:2C80->2C90 score=4

Anchor reports:
- no target survived byte review strongly enough to justify anchor follow-up

ROM-byte check:
- C7:2C05 = `F3 DA 9B E4 B8 CF DA 9D EB 9B E4 B8 CF DD 8D 00`
- C7:2C06 = `DA 9B E4 B8 CF DA 9D EB 9B E4 B8 CF DD 8D 00 7A`
- C7:2C0F = `E4 B8 CF DD 8D 00 7A 9D F3 B8 02 9A 9B D5 00 F5`
- C7:2C12 = `DD 8D 00 7A 9D F3 B8 02 9A 9B D5 00 F5 DD D5 01`
- C7:2C33 = `DA 9B E4 B6 C4 B7 F5 21 F2 C4 9E 38 70 9E 28 07`
- C7:2C35 = `E4 B6 C4 B7 F5 21 F2 C4 9E 38 70 9E 28 07 3F DE`
- C7:2C90 = `41 F4 FD F5 40 F4 DA 9B F5 21 F2 C4 9E 38 07 9E`

Verdict:
- `2C90` is the busiest target in the page, but all of its traffic is already downgraded to suspect from frozen pages behind the seam.
- The weak-supported targets near the page head are even worse structurally; they read like the same patterned table material.
- This page reached manual review only because it avoided hard-bad starts, not because any entry survived byte scrutiny.

**Frozen.**

### C7:2D00..2DFF
Summary: raw_targets=2, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C7:2D21 (2 weak callers from `C7:D81C`, `C7:7539`)
- C7:2DE6 (1 weak caller from `C7:CED2`)

Backtrack scan:
- C7:2DDF->2DE6 score=6
- C7:2D20->2D21 score=2

Anchor reports:
- no target survived byte review strongly enough to justify anchor follow-up

ROM-byte check:
- C7:2D20 = `9C CB F2 C4 F3 EA 9B 00 AB 9C 23 9C 08 E4 9D 48`
- C7:2D21 = `CB F2 C4 F3 EA 9B 00 AB 9C 23 9C 08 E4 9D 48 FF`
- C7:2DDF = `4B 9C 6B 9B 4B 9C 6B 9B 58 FF 9B 58 FF 9C 3A 9B`
- C7:2DE6 = `9B 58 FF 9B 58 FF 9C 3A 9B BA 9B 7A B5 6F FD F0`

Verdict:
- `2DE6` gets the best backtrack score in the page and one of the best in the block.
- That still does not rescue it. The surrounding bytes are strongly repetitive and table-like rather than a coherent executable body.
- `2D21` has more caller support, but its local bytes read even worse.

**Frozen.**

### C7:2E00..2EFF
Summary: raw_targets=4, xref_hits=4, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C7:2E03 (1 weak caller from `C7:8F80`)
- C7:2EE4 (1 weak caller from `C7:C61A`)
- C7:2EFE (1 suspect caller from `C7:AC35`) [boundary_bait]
- C7:2EFF (1 suspect caller from `C7:AD31`) [boundary_bait]

Backtrack scan:
- C7:2ED4->2EE4 score=4
- C7:2E03->2E03 score=3
- C7:2EFD->2EFE score=2
- C7:2EFD->2EFF score=2

Anchor reports:
- no target survived byte review strongly enough to justify anchor follow-up

ROM-byte check:
- C7:2E03 = `3A B5 4B 9C 6B 9B 4B 9C 6B 9B BA 9B 7A B5 DA B5`
- C7:2ED4 = `DA D2 C4 D1 69 BC BB D0 46 3F E5 13 E4 53 F0 3F`
- C7:2EE4 = `38 E0 8C 09 62 8C CD 00 8F 01 91 BB 26 D8 A6 3F`
- C7:2EFD = `A3 07 FC 3F A3 07 FC CB 9C 3F 78 0A 3D 3D 0B 91`
- C7:2EFE = `07 FC 3F A3 07 FC CB 9C 3F 78 0A 3D 3D 0B 91 D0`

Verdict:
- `2EE4` is the least-bad candidate in the page, but it still reads as mixed data/control material rather than executable code.
- `2EFE` and `2EFF` are boundary bait at page tail and do not deserve owner defense.

**Frozen.**

### C7:2F00..2FFF
Summary: raw_targets=6, xref_hits=6, strong_or_weak=3, hard_bad=0, soft_bad=0

Targets:
- C7:2F07 (1 weak caller from `C7:2808`)
- C7:2FE0 (1 weak caller from `C7:802D`)
- C7:2FE1 (1 weak caller from `C7:93D1`)
- C7:2F00 (1 suspect caller from `C7:13B9`)
- C7:2F33 (1 suspect caller from `C7:5B17`)

Backtrack scan:
- C7:2F28->2F33 score=6
- C7:2FDD->2FE0 score=4
- C7:2FDD->2FE1 score=4
- C7:2F00->2F07 score=2

Anchor reports:
- no target survived byte review strongly enough to justify anchor follow-up

ROM-byte check:
- C7:2F00 = `3F A3 07 FC CB 9C 3F 78 0A 3D 3D 0B 91 D0 E0 E8`
- C7:2F07 = `78 0A 3D 3D 0B 91 D0 E0 E8 00 C4 55 C4 57 C4 59`
- C7:2F28 = `DA 54 DA 56 DA 58 C4 22 C4 23 DA 24 C4 5A C4 5C`
- C7:2F33 = `24 C4 5A C4 5C C4 60 C4 7C C4 7B 8F 01 47 8F FF`
- C7:2FDD = `A0 F3 D5 61 F3 D5 00 F3 BC D4 26 E8 10 D5 01 F3`
- C7:2FE0 = `61 F3 D5 00 F3 BC D4 26 E8 10 D5 01 F3 6F E4 8E`
- C7:2FE1 = `F3 D5 00 F3 BC D4 26 E8 10 D5 01 F3 6F E4 8E 64`

Verdict:
- `2F00` is the busiest manual-review page in the block and the strongest honest near-miss overall.
- The backtrack into `2F33` is real, but the entire page still reads like patterned table/control material rather than an owner lane.
- None of the weak-supported starts hold up once the local bytes are examined.

**Frozen.**

---

## Reject-heavy page note

### C7:2900..29FF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=1, soft_bad=0

Targets:
- C7:293A (1 suspect caller from `C7:0763`)
- C7:2940 (1 invalid caller from `C7:1DF7`)

Backtrack scan from block report:
- C7:2938->293A score=4
- C7:2938->2940 score=4

ROM-byte check:
- C7:2938 = `3A 9B F5 60 F3 D0 05 8F 00 9D 2F 12 5D E4 9C 8D`
- C7:293A = `F5 60 F3 D0 05 8F 00 9D 2F 12 5D E4 9C 8D 00 9E`
- C7:2940 = `00 9D 2F 12 5D E4 9C 8D 00 9E C4 9D E4 9B 9E C4`

Verdict:
- `2900` is the strongest reject signal in the block.
- It looks like candidate-code bait because both targets backtrack cleanly out of `2938`.
- That still fails immediately: `293A` remains suspect-only and `2940` is an invalid companion landing inside the same patterned byte field.

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **`C7:2F00..C7:2FFF`** — it was the busiest manual-review page in the block, but every candidate window still collapsed into patterned table/data bytes before anchor follow-up.
- **Strongest reject signal**: **`C7:2900..C7:29FF`** — candidate-code bait page with clean backtracks, but the defended pair is only suspect-plus-invalid inside the same patterned field.
- Five pages reached `manual_owner_boundary_review`, and all five still failed on structural byte quality rather than caller count alone.
- `C7:2700`, `C7:2800`, and `C7:2A00` show real local control pockets, but none of them carry the ingress needed to defend ownership.

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
- C7:2600..2FFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_2600_2fff_seam_block.json`
- `reports/c7_2600_2fff_seam_block.md`
- `reports/c7_2b00_2bff_backtrack.json`
- `reports/c7_2c00_2cff_backtrack.json`
- `reports/c7_2d00_2dff_backtrack.json`
- `reports/c7_2e00_2eff_backtrack.json`
- `reports/c7_2f00_2fff_backtrack.json`

---

## New live seam: C7:3000..

Next unprocessed block starts at **C7:3000**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:3000 --pages 10 --json > reports/c7_3000_39ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c7_3000_39ff_seam_block.json --output reports/c7_3000_39ff_seam_block.md`
3. Run owner-backtrack scans only for pages that still land in `manual_owner_boundary_review`, then write notes_64.
