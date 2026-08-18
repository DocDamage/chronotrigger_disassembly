# Chrono Trigger Session 15 — Continuation Notes 59

## Block closed: C6:FE00..C7:07FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:FE00 | mixed_command_data | mixed_lane_continue | freeze | suspect-only `FE10/FE3B/FECB` targets, no strong/weak support |
| C6:FF00 | mixed_command_data | mixed_lane_continue | freeze | lone weak `FF80` plus suspect-heavy interior traffic, not enough to survive review |
| C7:0000 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | very high traffic into `0004`, but page mixes dispatcher jumps, data contamination, and 7 hard-bad starts |
| C7:0100 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | multiple weak landings (`0192/01A5/0102`) but still reject-heavy overall |
| C7:0200 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | weak traffic plus boundary-bait `02FE` and two hard-bad starts |
| C7:0300 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | weak multi-target page with a hard-bad companion landing |
| C7:0400 | mixed_command_data | manual_owner_boundary_review | freeze | `04C0/04F9` both stay weak-only from unresolved callers |
| C7:0500 | mixed_command_data | mixed_lane_continue | freeze | only `05A5` with 3 weak hits, not enough to justify manual-owner split |
| C7:0600 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | strongest manual-review page in block, but every defended target stays weak-only from unresolved callers |
| C7:0700 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | mixed weak targets plus invalid `07F0` companion landing |

---

## Manual-owner review summary

Two pages survived into `manual_owner_boundary_review`:
- `C7:0400..C7:04FF`
- `C7:0600..C7:06FF`

### C7:0400..04FF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C7:04C0 (1 weak caller from `C7:04AE`)
- C7:04F9 (1 weak caller from `C7:B789`)

Backtrack scan:
- C7:04EE->04F9 score=4
- C7:04B5->04C0 score=2

Anchor reports:
- `C7:04C0` = **weak / unresolved**
- `C7:04F9` = **weak / unresolved**

ROM-byte check:
- C7:04AE = `4C C0 04 A2 20 00 D5 1E F0 04 CA CA`
- C7:04B5 = `1E F0 04 CA CA D0 F8 CA CA 86 FC E2`
- C7:04C0 = `E2 20 A5 10 18 69 FF A9 00 2A C5 11`
- C7:04EE = `20 DA 09 85 84 A9 03 CD 41 21 F0 05`
- C7:04F9 = `05 20 EA 09 80 DC C2 20 A5 05 29 FF`

Verdict:
- `04C0` is locally plausible.
- `04F9` is much weaker structurally and looks like an interior landing.
- Neither target has caller support beyond single weak unresolved anchors.

**Frozen.**

### C7:0600..06FF
Summary: raw_targets=6, xref_hits=6, strong_or_weak=5, hard_bad=0, soft_bad=1

Targets:
- C7:061C (1 weak caller from `C7:017A`)
- C7:062C (1 weak caller from `C7:6EBD`)
- C7:0655 (1 weak caller from `C7:034F`)
- C7:06D6 (1 weak caller from `C7:5A66`)
- C7:06F0 (1 weak caller from `C7:0756`)

Backtrack scan:
- C7:0616->061C score=6
- C7:0628->062C score=4
- C7:0646->0654 score=4
- C7:0646->0655 score=4
- C7:06ED->06F0 score=4

Anchor reports:
- `C7:061C` = **weak / unresolved**
- `C7:062C` = **weak / unresolved**
- `C7:0655` = **weak / unresolved**
- `C7:06D6` = **weak / unresolved**
- `C7:06F0` = **weak / unresolved**

ROM-byte check:
- C7:0616 = `20 12 0A 4C 92 01 E2 20 A5 03 8D 43`
- C7:061C = `E2 20 A5 03 8D 43 21 A5 02 8D 42 21`
- C7:0628 = `A5 01 8D 41 21 A5 00 A2 00 04 8D 40`
- C7:062C = `21 A5 00 A2 00 04 8D 40 21 CD 40 21`
- C7:0646 = `0B A5 01 29 0F C5 F0 F0 03 20 FD 09`
- C7:0655 = `08 C2 20 A6 1C B5 20 3A 85 82 0A 18`
- C7:06D6 = `14 B7 12 8D 42 21 C8 D0 02 E6 14 B7`
- C7:06ED = `20 DA 09 85 84 CA CA CA D0 D6 80 1E`
- C7:06F0 = `85 84 CA CA CA D0 D6 80 1E B7 12 8D`

Verdict:
- `061C` is the clearest structural candidate in the page and the block.
- `0655` is locally plausible but still only single-caller weak.
- `062C`, `06D6`, and `06F0` all look worse structurally.
- The entire page still collapses because every target depends on unresolved weak callers only.

**Frozen.**

---

## Reject-heavy page note

### C7:0000..00FF
Summary: raw_targets=29, xref_hits=113, strong_or_weak=78, hard_bad=7, soft_bad=0

Targets:
- C7:0004 (60 weak callers)
- C7:0000 (4 weak callers)
- C7:00F0 (3 weak callers)
- C7:00A2 (2 weak callers)
- C7:00B9 (2 weak callers)

Backtrack scan from block report:
- C7:0030->0040 score=6
- C7:004B->004F score=6
- C7:0070->0078 score=6

ROM-byte check:
- C7:0000 = `4C 38 00 EA 4C 40 01 EA 4C 26 03 EA`
- C7:0004 = `4C 40 01 EA 4C 26 03 EA 4C 7B 03 EA`
- C7:000B = `EA 4C 7B 03 EA C3 24 09 43 B4 40 B7`
- C7:0030 = `20 0C 11 0E E9 0A 0B 5B 8B 0B 08 C2`
- C7:0040 = `DA 5A E2 20 A9 00 48 AB A2 00 1E DA`
- C7:0070 = `A9 CC 8D 41 21 8D 40 21 CD 40 21 D0`
- C7:00F0 = `41 21 EB 8D 40 21 CD 40 21 D0 FB EB`

Verdict:
- `C7:0000..00FF` is the strongest reject signal in the block by far.
- `0004` draws massive traffic, but the page is not a clean owner lane. It mixes chained dispatcher jumps, embedded data-like contamination, later executable islands, and seven hard-bad starts.
- The honest result is to freeze the page, not to promote a page-wide owner around the hottest landing.

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **`C7:0600..C7:06FF`** — it reached manual review and contains the clearest local candidate at `C7:061C`, but every defended target stayed weak-only from unresolved callers.
- **Strongest reject signal**: **`C7:0000..C7:00FF`** — extremely hot ingress into `C7:0004`, but the page still fails under mixed dispatcher/data structure and seven hard-bad starts.
- Two pages reached `manual_owner_boundary_review`, and both collapsed under weak-only caller quality.

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
- C6:FE00..C7:07FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_fe00_c7_07ff_seam_block.json`
- `reports/c6_fe00_c7_07ff_seam_block.md`
- `reports/c7_0400_04ff_backtrack.json`
- `reports/c7_0600_06ff_backtrack.json`
- `reports/C7_04C0_anchor.json`
- `reports/C7_04F9_anchor.json`
- `reports/C7_061C_anchor.json`
- `reports/C7_062C_anchor.json`
- `reports/C7_0655_anchor.json`
- `reports/C7_06D6_anchor.json`
- `reports/C7_06F0_anchor.json`

---

## New live seam: C7:0800..

Next unprocessed block starts at **C7:0800**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:0800 --pages 10 --json > reports/c7_0800_11ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c7_0800_11ff_seam_block.json --output reports/c7_0800_11ff_seam_block.md`
3. Run owner-backtrack scans only for pages that still land in `manual_owner_boundary_review`, then write notes_60.
