# Chrono Trigger Session 15 — Continuation Notes 35

## Block closed: C6:0E00..C6:17FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:0E00 | branch_fed_control_pocket | local_control_only | freeze | lone suspect target `C6:0EBC` only |
| C6:0F00 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=1 despite two weak targets |
| C6:1000 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=3 on high-noise page (`raw=16`, `xref=22`) |
| C6:1100 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | hard_bad=1 with mixed suspect traffic |
| C6:1200 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=1 (`C6:12A5` invalid) despite five weak hits |
| C6:1300 | mixed_command_data | manual_owner_boundary_review | freeze | weak/suspect-only targets with unresolved callers |
| C6:1400 | candidate_code_lane | manual_owner_boundary_review | freeze | weak/suspect mesh; no strong anchors |
| C6:1500 | mixed_command_data | local_control_only | freeze | suspect-only targets (`C6:1509`, `C6:1578`) |
| C6:1600 | mixed_command_data | manual_owner_boundary_review | freeze | three weak + two suspect targets, all unresolved |
| C6:1700 | candidate_code_lane | local_control_only | freeze | lone suspect target `C6:1723` only |

---

## Manual-owner pages (anchor detail)

### C6:1300..13FF
Summary: raw_targets=3, xref_hits=4, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C6:1303 (suspect, caller C6:A518)
- C6:1304 (weak, caller C6:1B0C)
- C6:1395 (weak/suspect, callers C6:2548 and C6:2733)

Backtrack scan (`reports/c6_1300_13ff_backtrack.json`):
- C6:1304->1304 score=5, start=0x20
- C6:1300->1303 score=4, start=0x50
- C6:1395->1395 score=3, start=0xC2

Anchor reports:
- C6:1303: strong=0, weak=1, invalid=7
- C6:1304: strong=0, weak=1, invalid=5
- C6:1395: strong=0, weak=2, invalid=2

ROM-byte check:
- C6:1303 = `10 20 02 30 C4 00 62 40 F8 38 C1 7E`
- C6:1304 = `20 02 30 C4 00 62 40 F8 38 C1 7E 00`
- C6:1395 = `C2 FD CA 00 FF E7 FD EB 78 77 1D 06`

Verdict: no strong anchors and high invalid companion-caller counts; freeze.

### C6:1400..14FF
Summary: raw_targets=6, xref_hits=7, strong_or_weak=3, hard_bad=0, soft_bad=0

Targets:
- C6:1400 (suspect, caller C6:D4C2)
- C6:1410 (suspect, caller C6:3919)
- C6:1411 (suspect, caller C6:5938)
- C6:1444 (suspect, caller C6:D508)
- C6:14BD (weak, caller C6:E3B9)
- C6:14C4 (weak, callers CA:B335 and CB:1129)

Backtrack scan (`reports/c6_1400_14ff_backtrack.json`):
- C6:1410->1411 score=4, start=0xE3
- C6:1441->1444 score=4, start=0x20
- C6:14BC->14BD score=4, start=0xF2
- C6:14BC->14C4 score=4, start=0xF2
- C6:1400->1400 score=3, start=0x08
- C6:1410->1410 score=3, start=0xE3

Anchor reports:
- C6:1400: strong=0, weak=1, invalid=16
- C6:1410: strong=0, weak=1, invalid=9
- C6:1411: strong=0, weak=1, invalid=2
- C6:1444: strong=0, weak=1, invalid=2
- C6:14BD: strong=0, weak=1, invalid=17
- C6:14C4: strong=0, weak=2, invalid=1

ROM-byte check:
- C6:1400 = `08 01 0E 03 1C 00 00 FF 79 BF 50 BF`
- C6:1410 = `E3 7E E1 1A 85 1A 25 00 58 A7 17 61`
- C6:14C4 = `3F 40 5E E1 FD 02 BE 41 00 9C 63 88`

Verdict: weak/suspect-only ownership with very high invalid caller overlap; freeze.

### C6:1600..16FF
Summary: raw_targets=5, xref_hits=5, strong_or_weak=3, hard_bad=0, soft_bad=0

Targets:
- C6:1600 (suspect, caller C6:D371)
- C6:1611 (suspect, caller C6:593E)
- C6:1648 (weak, caller C6:5EFB)
- C6:16AD (weak, caller C6:EA3F)
- C6:16B8 (weak, caller C6:2C73)

Backtrack scan (`reports/c6_1600_16ff_backtrack.json`):
- C6:1647->1648 score=6, start=0x20
- C6:160C->1611 score=2, start=0xF6
- C6:16AA->16AD score=2, start=0x84
- C6:16B3->16B8 score=2, start=0x52
- C6:1600->1600 score=1, start=0xC8

Anchor reports:
- C6:1600: strong=0, weak=1, invalid=19
- C6:1611: strong=0, weak=1, invalid=1
- C6:1648: strong=0, weak=1, invalid=0
- C6:16AD: strong=0, weak=1, invalid=27
- C6:16B8: strong=0, weak=1, invalid=2

ROM-byte check:
- C6:1600 = `C8 00 D8 08 58 6C 38 6C B8 FC 00 C2`
- C6:1611 = `FE 18 00 F8 58 B8 3C FC 7C FC 3C F0`
- C6:1648 = `24 0B 74 2E 10 40 40 98 04 A0 70 A0`
- C6:16AD = `52 5C A2 B7 00 C9 52 EF 93 EC BF C8`
- C6:16B8 = `C8 74 00 0B C1 3E 57 AC 3E DD BC 00`

Verdict: all starts remain weak/suspect with heavy invalid contamination; freeze.

---

## Reject/mixed lane notes

- C6:0400: rejected on hard_bad=3 (invalid starts at `C6:041E`, `C6:042F`, `C6:044C`).
- C6:0500: rejected on hard_bad=2 (`C6:0560`, `C6:05E4` invalid).
- C6:0700: mixed-command reject (`hard_bad=4`, effective weak/strong=0).
- C6:0800: most contaminated page in block (`hard_bad=12`, `soft_bad=2`, 25 xref hits).
  - Invalid examples: `C6:0802`, `C6:0810`, `C6:0814`, `C6:0820`, `C6:0849`
- C6:0A00/0B00/0C00: rejected on explicit invalids:
  - `C6:0A1D`, `C6:0B10`, `C6:0B18`, `C6:0C05`, `C6:0C0B`, `C6:0CE2`
- C6:0600 stays mixed-lane carry (weak hits + soft_bad=1); C6:0900/C6:1500/C6:1700 remain suspect-only local-control pages.

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
- C6:0E00..17FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_0e00_17ff_seam_block.json`
- `reports/c6_0e00_17ff_seam_block.md`
- `reports/c6_1300_13ff_backtrack.json`
- `reports/c6_1400_14ff_backtrack.json`
- `reports/c6_1600_16ff_backtrack.json`
- `reports/C6_1303_anchor.json`
- `reports/C6_1304_anchor.json`
- `reports/C6_1395_anchor.json`
- `reports/C6_1400_anchor.json`
- `reports/C6_1410_anchor.json`
- `reports/C6_1411_anchor.json`
- `reports/C6_1444_anchor.json`
- `reports/C6_14BD_anchor.json`
- `reports/C6_14C4_anchor.json`
- `reports/C6_1600_anchor.json`
- `reports/C6_1611_anchor.json`
- `reports/C6_1648_anchor.json`
- `reports/C6_16AD_anchor.json`
- `reports/C6_16B8_anchor.json`
- `reports/c6_1300_13ff_flow.json` (manual-page extraction)
- `reports/c6_1400_14ff_flow.json` (manual-page extraction)
- `reports/c6_1600_16ff_flow.json` (manual-page extraction)
- `reports/c6_0f00_0fff_flow.json` (reject-page support)
- `reports/c6_1000_10ff_flow.json` (reject-page support)
- `reports/c6_1100_11ff_flow.json` (reject-page support)
- `reports/c6_1200_12ff_flow.json` (reject-page support)

---

## New live seam: C6:1800..

Next unprocessed block starts at **C6:1800**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:1800 --pages 10 --json > reports/c6_1800_21ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_1800_21ff_seam_block.json --output reports/c6_1800_21ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_36.
