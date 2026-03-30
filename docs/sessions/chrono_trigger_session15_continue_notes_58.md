# Chrono Trigger Session 15 — Continuation Notes 58

## Block closed: C6:F400..C6:FDFF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:F400 | branch_fed_control_pocket | local_control_only | freeze | no ingress targets; only local control clusters |
| C6:F500 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | lone target `C6:F5EE` is an invalid `FF`-start field |
| C6:F600 | mixed_command_data | mixed_lane_continue | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:F700 | mixed_command_data | mixed_lane_continue | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:F800 | mixed_command_data | mixed_lane_continue | freeze | busiest page in block, but all 8 hits stay suspect-only and the body bytes stay patterned/data-like |
| C6:F900 | text_ascii_heavy | mixed_lane_continue | freeze | no ingress targets in text-heavy page |
| C6:FA00 | text_ascii_heavy | mixed_lane_continue | freeze | suspect-only `FA10/FA47` inside text-heavy page |
| C6:FB00 | candidate_code_lane | local_control_only | freeze | local-control page with only a lone suspect `FB40` landing |
| C6:FC00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | lone target `C6:FC9D` lands on all-zero dead field |
| C6:FD00 | mixed_command_data | mixed_lane_continue | freeze | no ingress targets (`raw=0`, `xref=0`) |

---

## Manual-owner review summary

No page in this block survived into `manual_owner_boundary_review`.

Closest page to that threshold:
- **`C6:F800..C6:F8FF`**
- posture stayed **`mixed_lane_continue`**
- page carried **8 suspect-only ingress targets** and **0 strong/weak hits**
- best-supported targets stayed spread across `C6:F801`, `C6:F802`, `C6:F830`, `C6:F840`, and `C6:F8B9`, each with only **1 suspect caller**
- top owner-backtracks were `C6:F8B4->F8B9`, `C6:F8B4->F8BE`, and `C6:F8B4->F8C0`, all score `4`

ROM-byte check for the near-miss page:
- C6:F8B4 = `A9 88 89 AC 86 66 67 89 55 44 56 77`
- C6:F8B9 = `66 67 89 55 44 56 77 BC CC CC CC CC`
- C6:F8BE = `56 77 BC CC CC CC CC DD EE EE CD DE`
- C6:F8C0 = `BC CC CC CC CC DD EE EE CD DE EE EE`

Verdict:
- `F800` was the strongest honest near-miss page in the block because it drew the most raw traffic.
- That still was not close to enough. Every hit stayed suspect-only, and the candidate windows collapse into patterned nibble-heavy data rather than coherent executable body bytes.
- The honest outcome is still freeze, not manual review or promotion.

**Frozen.**

---

## Reject-heavy page note

### C6:FC00..FCFF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0

Targets:
- C6:FC9D (1 invalid caller from `C6:1B26`)

Backtrack scan from block report:
- C6:FC9D->FC9D score=-8

ROM-byte check:
- C6:FC15 = `70 18 63 10 80 46 4A 2D C6 1C 21 08`
- C6:FC9D = `00 00 00 00 00 00 00 00 00 00 00 00`

Verdict:
- `FC00` is the strongest reject signal in the block.
- The page does contain a local control pocket earlier on, but the only ingress target that matters lands at `FC9D`.
- That target is an all-zero dead field with a hard-bad start, so there is nothing to rescue.

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **`C6:F800..C6:F8FF`** — the busiest page in the block, but still entirely suspect-backed and structurally data-like.
- **Strongest reject signal**: **`C6:FC00..C6:FCFF`** — the only ingress target lands on an all-zero dead field at `FC9D`.
- No page in this block survived into `manual_owner_boundary_review`.

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
- C6:F400..FDFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_f400_fdff_seam_block.json`
- `reports/c6_f400_fdff_seam_block.md`

---

## New live seam: C6:FE00..

Next unprocessed block starts at **C6:FE00** and crosses into bank `C7`.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:FE00 --pages 10 --json > reports/c6_fe00_c7_07ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_fe00_c7_07ff_seam_block.json --output reports/c6_fe00_c7_07ff_seam_block.md`
3. Run owner-backtrack scans only for pages that still land in `manual_owner_boundary_review`, then write notes_59.
