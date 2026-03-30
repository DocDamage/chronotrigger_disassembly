# Chrono Trigger Session 15 — Continuation Notes 57

## Block closed: C6:EA00..C6:F3FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:EA00 | mixed_command_data | mixed_lane_continue | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:EB00 | mixed_command_data | mixed_lane_continue | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:EC00 | mixed_command_data | mixed_lane_continue | freeze | lone suspect target `C6:EC10` plus only suspect ingress into the page |
| C6:ED00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | heavy weak traffic into `EDE1/ED04`, but invalid `ED07` keeps the page reject-heavy |
| C6:EE00 | dead_zero_field | dead_lane_reject | freeze | dead-field page with only suspect `EE21` traffic |
| C6:EF00 | dead_zero_field | dead_lane_reject | freeze | hard-bad zero-start targets `EFBD/EFC7/EFCC` |
| C6:F000 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | weak `F020` cannot overcome hard-bad page pressure |
| C6:F100 | mixed_command_data | mixed_lane_continue | freeze | suspect-only `F100/F14E/F1AE` targets, no strong/weak support |
| C6:F200 | mixed_command_data | mixed_lane_continue | freeze | suspect-only `F2BF/F25C` targets plus soft-bad page pressure |
| C6:F300 | dead_zero_field | dead_lane_reject | freeze | hard-bad zero-start targets `F300` and `F30C` |

---

## Manual-owner review summary

No page in this block survived into `manual_owner_boundary_review`.

Closest page to that threshold:
- **`C6:EC00..C6:ECFF`**
- posture stayed **`mixed_lane_continue`**
- best-supported target was **`C6:EC10`** with only **1 suspect caller** (`C6:8EF5`)
- page also carries a direct `JSR C6:EDE1` at `C6:EC09`, which is why this block forced a harder look at `ED00`

ROM-byte check for the near-miss page:
- C6:EC09 = `20 E1 ED A6 13 A5 00 9F 76 91 7E 9F`
- C6:EC10 = `9F 76 91 7E 9F 78 91 7E A5 02 49 FF`

Verdict:
- `EC00` was the strongest honest near-miss page in the block.
- It still never justified manual-owner review because its only target support remained suspect-only.
- The direct `JSR EDE1` explains why `ED00` gets real traffic, but it does not rescue `EC10` itself.

**Frozen.**

---

## Reject-heavy page note

### C6:ED00..EDFF
Summary: raw_targets=3, xref_hits=12, strong_or_weak=11, hard_bad=1, soft_bad=0

Targets:
- C6:EDE1 (8 weak callers from `C6:EB3B`, `C6:EB8E`, `C6:EB96`, `C6:EBF1`, `C6:EC09`, `C6:EC64`, `C6:EC7C`, `C6:ECDF`)
- C6:ED04 (3 weak callers from `C6:EB93`, `C6:EC06`, `C6:EC79`)
- C6:ED07 (1 invalid caller from `C6:B32D`)

Backtrack scan from block report:
- C6:EDDF->EDE1 score=4
- C6:ED02->ED07 score=2
- C6:ED02->ED04 score=0

ROM-byte check:
- C6:ED02 = `85 06 64 10 A5 00 10 0B 49 FF FF 1A`
- C6:ED04 = `64 10 A5 00 10 0B 49 FF FF 1A 85 00`
- C6:ED07 = `00 10 0B 49 FF FF 1A 85 00 A9 01 00`
- C6:EDDF = `26 6B A6 08 A5 0D 8E 04 42 8D 06 42`
- C6:EDE1 = `A6 08 A5 0D 8E 04 42 8D 06 42 A6 0A`

Verdict:
- `ED00` is the strongest reject signal in the block by far.
- `EDE1` and `ED04` both draw real weak traffic and have plausible local structure.
- That still is not enough. The page carries an invalid companion landing at `ED07`, and the overall posture stays `bad_start_or_dead_lane_reject`.
- The honest outcome is still freeze, not promotion.

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **`C6:EC00..ECFF`** — the clearest mixed-lane page in the block, but still only suspect-backed.
- **Strongest reject signal**: **`C6:ED00..EDFF`** — the busiest page in the block, with 11 weak effective hits, but still reject-heavy because of the invalid `ED07` companion target.
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
- C6:EA00..F3FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_ea00_f3ff_seam_block.json`
- `reports/c6_ea00_f3ff_seam_block.md`

---

## New live seam: C6:F400..

Next unprocessed block starts at **C6:F400**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:F400 --pages 10 --json > reports/c6_f400_fdff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_f400_fdff_seam_block.json --output reports/c6_f400_fdff_seam_block.md`
3. Run owner-backtrack scans only for pages that still land in `manual_owner_boundary_review`, then write notes_58.
