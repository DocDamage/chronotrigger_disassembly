# Chrono Trigger Session 15 — Continuation Notes 60

## Block closed: C7:0800..C7:11FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:0800 | mixed_command_data | manual_owner_boundary_review | freeze | `08DC` stays lone weak unresolved helper; `08E3` never rises above suspect |
| C7:0900 | mixed_command_data | manual_owner_boundary_review | freeze | hot `09DA/09EA` lane is byte-plausible, but support downgrades to weak unresolved plus suspect hits from already frozen pages |
| C7:0A00 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | `0A12` is locally coherent, but caller support stays weak/suspect only; `0A39/0A64` do not survive beyond suspect |
| C7:0B00 | mixed_command_data | manual_owner_boundary_review | freeze | `0B91` is weak-only and `0BA0` runs straight into zero-heavy bytes |
| C7:0C00 | mixed_command_data | mixed_lane_continue | freeze | adjacent weak `0C10/0C11` starts have negative backtracks and no cluster support |
| C7:0D00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | weak `0D12/0DA8` cannot overcome hard-bad page pressure |
| C7:0E00 | dead_zero_field | dead_lane_reject | freeze | dead-field page with lone weak `0E0F` and five hard-bad starts |
| C7:0F00 | dead_zero_field | dead_lane_reject | freeze | dead-field page with only weak tail `0FDF` and eight hard-bad starts |
| C7:1000 | dead_zero_field | dead_lane_reject | freeze | all-zero / low-entropy field with lone weak `10DF` and eleven hard-bad starts |
| C7:1100 | dead_zero_field | dead_lane_reject | freeze | boundary-bait `11FF` sits inside another dead field with ten hard-bad starts |

---

## Manual-owner review summary

Four pages survived into `manual_owner_boundary_review`:
- `C7:0800..C7:08FF`
- `C7:0900..C7:09FF`
- `C7:0A00..C7:0AFF`
- `C7:0B00..C7:0BFF`

### C7:0800..08FF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C7:08DC (1 weak caller from `C7:4995`)
- C7:08E3 (1 suspect caller)

Backtrack scan:
- C7:08DF->08E3 score=6
- C7:08CC->08DC score=4

Anchor reports:
- `C7:08DC` = **weak / unresolved**
- `C7:08E3` stayed suspect-only and did not justify anchor follow-up

ROM-byte check:
- C7:08CC = `21 CD 40 21 F0 03 CA D0 F8 CD 40 21`
- C7:08DC = `A5 01 95 20 4C 92 01 E2 20 A5 01 18`
- C7:08DF = `20 4C 92 01 E2 20 A5 01 18 69 FF A9`
- C7:08E3 = `E2 20 A5 01 18 69 FF A9 00 2A C5 11`

Verdict:
- `08DC` is a plausible tiny helper ending in a jump back into the hotter lane at `0192`.
- `08E3` is cleaner byte-wise, but it never gained support beyond a lone suspect hit.
- The page still collapses because no resolved caller supports either entry.

**Frozen.**

### C7:0900..09FF
Summary: raw_targets=5, xref_hits=44, strong_or_weak=8, hard_bad=0, soft_bad=0

Targets:
- C7:09DA (32 total hits; 11 weak unresolved, 21 suspect from closed pages)
- C7:09EA (7 total hits; 1 weak unresolved, 6 suspect from closed pages)
- C7:09FD (2 total hits; 1 weak unresolved, 1 suspect from a closed page) [boundary_bait]

Backtrack scan:
- C7:09CA->09DA score=6
- C7:09DA->09EA score=6
- C7:09EA->09F2 score=6
- C7:09F7->09FD score=6

Anchor reports:
- `C7:09DA` = **11 weak / unresolved + 21 suspect / resolved_data**
- `C7:09EA` = **1 weak / unresolved + 6 suspect / resolved_data**
- `C7:09FD` = **1 weak / unresolved + 1 suspect / resolved_data**

ROM-byte check:
- C7:09CA = `DA 09 85 84 CA CA CA D0 E2 64 F3 A9`
- C7:09DA = `08 E2 20 8D 40 21 CD 40 21 D0 FB 1A`
- C7:09EA = `08 E2 20 A5 84 8D 40 21 CD 40 21 D0`
- C7:09F2 = `CD 40 21 D0 FB A9 E0 85 84 28 60 08`
- C7:09F7 = `A9 E0 85 84 28 60 08 E2 20 85 F0 0A`
- C7:09FD = `08 E2 20 85 F0 0A 0A 0A 49 FF 1A 18`

Verdict:
- `09DA` and `09EA` are locally coherent and explain why the page looks hot.
- The repaired closed-range snapshot is doing the important work here: most of that traffic now downgrades to suspect because it comes from already frozen pages behind the seam.
- The remaining live callers are still only weak unresolved hits from unresolved territory, and `09FD` is boundary bait rather than a defensible owner start.

**Frozen.**

### C7:0A00..0AFF
Summary: raw_targets=4, xref_hits=6, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C7:0A12 (3 hits: 2 weak unresolved, 1 suspect from a closed page)
- C7:0A39 (1 suspect caller)
- C7:0A64 (1 suspect caller)

Backtrack scan:
- C7:0A0D->0A12 score=6
- C7:0A36->0A39 score=4
- C7:0A64->0A64 score=3

Anchor reports:
- `C7:0A12` = **2 weak / unresolved + 1 suspect / resolved_data**
- `C7:0A39` and `C7:0A64` stayed suspect-only and did not justify anchor follow-up

ROM-byte check:
- C7:0A0D = `20 12 0A 28 60 08 E2 20 A2 00 00 B5`
- C7:0A12 = `08 E2 20 A2 00 00 B5 63 F0 1B C5 F2`
- C7:0A36 = `F4 28 60 08 C2 20 A5 01 29 7F 00 0A`
- C7:0A39 = `08 C2 20 A5 01 29 7F 00 0A AA E2 20`
- C7:0A64 = `A5 01 8D 41 21 A5 00 8D 40 21 A2 00`

Verdict:
- `0A12` is the clearest helper candidate in the page.
- `0A39` also parses locally, but neither it nor `0A64` gained support beyond suspect traffic.
- The only defended target with caller evidence, `0A12`, still depends entirely on unresolved or already frozen caller ranges.

**Frozen.**

### C7:0B00..0BFF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C7:0B91 (1 weak caller from `C7:3250`)
- C7:0BA0 (1 weak caller)

Backtrack scan:
- C7:0B90->0B91 score=4
- C7:0B90->0BA0 score=0

Anchor reports:
- `C7:0B91` = **weak / unresolved**
- `C7:0BA0` did not survive byte review strongly enough to justify anchor follow-up

ROM-byte check:
- C7:0B90 = `48 CA BF 52 CA 22 61 CA 99 7C CA D7`
- C7:0B91 = `CA BF 52 CA 22 61 CA 99 7C CA D7 7F`
- C7:0BA0 = `CA 65 86 CA 00 00 00 00 00 00 00 00`

Verdict:
- `0B91` is only barely arguable structurally and still lands inside a dense mixed sequence.
- `0BA0` runs directly into zero-heavy bytes and reads worse than the headline weak hit count suggests.
- The page does not hold up as a defensible owner split.

**Frozen.**

---

## Reject-heavy page note

### C7:1000..10FF
Summary: raw_targets=9, xref_hits=12, strong_or_weak=1, hard_bad=11, soft_bad=0

Targets:
- C7:10DF (1 weak caller)
- C7:10C2 (3 invalid callers)
- C7:1000 (2 invalid callers)

Backtrack scan from block report:
- C7:10DF->10DF score=-3
- C7:10EF->10EF score=-6
- C7:10F0->10F0 score=-6

ROM-byte check:
- C7:1000 = `00 00 00 00 00 00 00 00 00 00 00 00`
- C7:10C2 = `00 0A 00 00 00 00 00 00 00 00 00 00`
- C7:10DF = `27 00 02 00 03 00 00 00 00 00 00 00`

Verdict:
- `C7:1000..10FF` is the strongest reject signal in the block.
- The page is overwhelmingly a dead field: the nominal weak tail at `10DF` is just low-entropy data-like bytes, while the rest of the page is dominated by zero-start invalid landings.
- There is nothing here that should be promoted or split.

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **`C7:0900..C7:09FF`** — the page has a real hot lane at `09DA/09EA`, but the repaired snapshot shows most of its traffic comes from already frozen pages and the remaining live callers are still only weak unresolved hits.
- **Strongest reject signal**: **`C7:1000..C7:10FF`** — an all-zero / low-entropy dead field with eleven hard-bad starts and no defensible landing.
- Four pages reached `manual_owner_boundary_review`, and all four still collapsed under unresolved-only caller support or local byte contamination.
- `C7:0E00..C7:11FF` now reads as a contiguous dead-zero corridor rather than a hidden owner lane.

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
- C7:0800..11FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_0800_11ff_seam_block.json`
- `reports/c7_0800_11ff_seam_block.md`
- `reports/c7_0800_08ff_backtrack.json`
- `reports/c7_0900_09ff_backtrack.json`
- `reports/c7_0a00_0aff_backtrack.json`
- `reports/c7_0b00_0bff_backtrack.json`
- `reports/C7_08DC_anchor.json`
- `reports/C7_09DA_anchor.json`
- `reports/C7_09EA_anchor.json`
- `reports/C7_09FD_anchor.json`
- `reports/C7_0A12_anchor.json`
- `reports/C7_0B91_anchor.json`

---

## New live seam: C7:1200..

Next unprocessed block starts at **C7:1200**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:1200 --pages 10 --json > reports/c7_1200_1bff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c7_1200_1bff_seam_block.json --output reports/c7_1200_1bff_seam_block.md`
3. Run owner-backtrack scans only for pages that still land in `manual_owner_boundary_review`, then write notes_61.
