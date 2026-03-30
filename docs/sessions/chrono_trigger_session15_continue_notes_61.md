# Chrono Trigger Session 15 — Continuation Notes 61

## Block closed: C7:1200..C7:1BFF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:1200 | dead_zero_field | dead_lane_reject | freeze | suspect-only `1211` plus invalid `12DE/120F` inside dead-field bytes |
| C7:1300 | dead_zero_field | dead_lane_reject | freeze | all candidate starts stay invalid in zero-heavy field |
| C7:1400 | dead_zero_field | dead_lane_reject | freeze | five invalid starts, no viable ingress |
| C7:1500 | dead_zero_field | dead_lane_reject | freeze | lone `15EE` target is invalid dead-field landing |
| C7:1600 | dead_zero_field | dead_lane_reject | freeze | lone `16F0` target is invalid dead-field landing |
| C7:1700 | dead_zero_field | dead_lane_reject | freeze | only `17B0/17B2` invalid starts survive xref scan |
| C7:1800 | dead_zero_field | dead_lane_reject | freeze | invalid `1898/1824/18BF` targets with no executable body support |
| C7:1900 | mixed_command_data | local_control_only | freeze | local control cluster at `194F..1957`, but no ingress targets (`raw=0`, `xref=0`) |
| C7:1A00 | dead_zero_field | dead_lane_reject | freeze | empty dead-field page with no ingress targets |
| C7:1B00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | lone target `1B4B` is invalid with negative backtrack |

---

## Manual-owner review summary

No page in this block survived into `manual_owner_boundary_review`.

Closest page to that threshold:
- **`C7:1900..C7:19FF`**
- posture stayed **`local_control_only`**
- page carried **0 ingress targets** and **1 local control cluster** at `C7:194F..C7:1957`

ROM-byte check for the near-miss page:
- C7:194F = `25 3E 2C 27 4B 11 28 4C 40 00 00 00 00 00 00 24`
- C7:1957 = `40 00 00 00 00 00 00 24 37 40 26 44 6E 00 00 00`

Verdict:
- `1900` is the strongest honest near-miss only because it contains a real local-control pocket instead of flat dead-zero terrain.
- That still is not close to promotable. There are no ingress targets at all, so there is no owner candidate to defend.
- The honest outcome is freeze, not speculative splitting around the local cluster.

**Frozen.**

---

## Reject-heavy page note

### C7:1200..12FF
Summary: raw_targets=7, xref_hits=9, strong_or_weak=0, hard_bad=7, soft_bad=0

Targets:
- C7:1211 (2 suspect callers)
- C7:12DE (2 invalid callers)
- C7:120F (1 invalid caller)

Backtrack scan from block report:
- C7:1211->1211 score=-3
- C7:12ED->12ED score=-6
- C7:12EF->12EF score=-6

ROM-byte check:
- C7:1200 = `00 1A 00 00 00 00 00 00 00 00 00 00 00 00 00 00`
- C7:1211 = `2E 00 08 00 3B 00 00 00 00 00 00 00 00 00 00 00`
- C7:12DE = `00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00`

Verdict:
- `C7:1200..12FF` is the strongest reject signal in the block.
- It draws the most xref traffic in the range, but that traffic terminates in low-entropy data and dead-zero starts rather than executable body bytes.
- There is nothing here that should be promoted or split.

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **`C7:1900..C7:19FF`** — it contains a real local-control pocket, but there are no ingress targets to defend as an owner.
- **Strongest reject signal**: **`C7:1200..C7:12FF`** — dead-zero page with nine xref hits and seven hard-bad starts.
- This block produced **no manual-owner pages**.
- `C7:1200..C7:18FF` and `C7:1A00` materially strengthen the read that this stretch is dead-field corridor, not hidden mixed-code seam.

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
- C7:1200..1BFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_1200_1bff_seam_block.json`
- `reports/c7_1200_1bff_seam_block.md`

---

## New live seam: C7:1C00..

Next unprocessed block starts at **C7:1C00**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:1C00 --pages 10 --json > reports/c7_1c00_25ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c7_1c00_25ff_seam_block.json --output reports/c7_1c00_25ff_seam_block.md`
3. Run owner-backtrack scans only for pages that still land in `manual_owner_boundary_review`, then write notes_62.
