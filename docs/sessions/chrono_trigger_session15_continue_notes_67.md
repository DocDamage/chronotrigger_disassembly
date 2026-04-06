# Chrono Trigger Session 15 — Continuation Notes 67

## Block closed: C7:4E00..C7:57FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:4E00 | mixed_command_data | mixed_lane_continue | freeze | weak target 4EBF, score-2 backtrack, unresolved caller C7:C0CC |
| C7:4F00 | mixed_command_data | manual_owner_boundary_review | freeze | score-4 backtrack on 4F14 but event script data pattern, weak caller |
| C7:5000 | mixed_command_data | mixed_lane_continue | freeze | zero targets, zero ingress, data lane |
| C7:5100 | mixed_command_data | mixed_lane_continue | freeze | suspect target 5155, score-4 but suspect caller C7:E9FA |
| C7:5200 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid 5222 + suspect 5228 share same backtrack origin (impossible for valid code) |
| C7:5300 | mixed_command_data | local_control_only | freeze | local clusters only, zero xref targets |
| C7:5400 | mixed_command_data | mixed_lane_continue | freeze | suspect target 54CC, score-4 but suspect caller C7:9A07 |
| C7:5500 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | hard_bad_start at 55D0, invalid companion |
| C7:5600 | mixed_command_data | local_control_only | freeze | suspect target 5635, score-2 backtrack, caller from data region C7:4447 |
| C7:5700 | mixed_command_data | local_control_only | freeze | zero targets, tiny local clusters, dead lane |

---

## Manual-owner review summary

### C7:4F00..C7:4FFF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C7:4F14 (1 weak caller from `C7:CE26`)
- C7:4F33 (1 suspect caller from `C7:5B21`)

Backtrack scan:
- C7:4F11->4F14 score=4
- C7:4F2B->4F33 score=2

ROM-byte check:
- C7:4F00 = `EB C4 14 D0 CF 1E DD 09 CB 00 0B BF 06 EB CB 00 01 BF DC 06 D8 DD 0A E2 01 A6 60 7B E3 EB C4 04 D4 DC 07 DD 00 9A E9 FE DC 02 D7 D2 D4 DD 03 C8 11 13 38 E9 FE C4 3C D4 DC 01 D7 CB 00 01 BF C8`

Byte analysis:
- **Event script data pattern detected**: High frequency of command bytes (EB, C4, CB, D4, DC, DD, D7, D0, CF)
- 37/64 unique bytes (high entropy typical of data, not code structure)
- No function prologue at entry points
- PHD (0B) appears mid-stream at offset 0x0A, not at function start
- Isolated RTS at 0x1A without proper function boundary

Verdict:
- Despite score-4 backtrack, the byte pattern clearly indicates **event script data**, not 65816 executable code
- 4F14 falls at an interior instruction offset within event script commands
- 4F33's score-2 backtrack is below promotion threshold
- Weak/suspect callers from unresolved regions provide no anchor support

**Frozen.**

---

## Reject-heavy page note

### C7:5200..C7:52FF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=0, hard_bad=1, soft_bad=0

Targets:
- C7:5222 (1 invalid caller from `C7:E8EB`) [hard_bad classification]
- C7:5228 (1 suspect caller from `C7:A229`)

Backtrack scan:
- C7:521C->5222 score=4
- C7:521C->5228 score=4

ROM-byte check:
- C7:521C = `0B 03 BF 09 A4 DC 03 D6 08 C8 0D CC 0A EB C4 00 D0 CF 18 DD 07 09 C5 10 1C AD EB D7 D4 D2 CB 00`

Critical finding:
- **Both targets backtrack from the SAME origin address (C7:521C)**
- This is mathematically impossible for valid code - two different entry points cannot share the exact same start address
- The pattern indicates data misinterpretation, not genuine code boundaries
- 28/32 unique bytes with event script command patterns (EB, C4, D0, CF, DD, D7, D4, D2, CB)
- No function prologue, no RTS/RTL returns

Verdict:
- Shared backtrack origin proves these are **false positive targets** in event script data
- Invalid classification on 5222 is correct
- Toolkit's bad_start_or_dead_lane_reject posture properly filtered this page

**Frozen.**

---

### C7:5500..C7:55FF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0

Target:
- C7:55D0 (1 invalid caller) [hard_bad_start]

Backtrack:
- Score=2 (below threshold), distance=15 bytes

Verdict:
- hard_bad_start classification correctly identifies invalid target
- Low backtrack score confirms data misread

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **C7:4F00..C7:4FFF** — the only manual-review page in this block. 4F14 achieved score-4 backtrack with clean_start classification, but byte-level review revealed event script data patterns rather than executable 65816 code. The weak caller from unresolved region C7:CE26 provided no supporting anchor evidence.

- **Strongest reject signal**: **C7:5200..C7:52FF** — two targets (5222 invalid, 5228 suspect) both backtracked from the **same origin address (C7:521C)**, which is mathematically impossible for valid code entry points. This definitively proves false-positive data misinterpretation. The toolkit's bad_start_or_dead_lane_reject posture correctly filtered this before manual review.

- **Event script data dominance**: ROM byte analysis revealed characteristic event script command patterns (high frequency of EB, C4, CB, DC, DD, D7 bytes) across multiple pages. This is not 65816 executable code but game engine script data.

- **Continued low manual review rate**: Only 10% (1 of 10 pages) reached manual_owner_boundary_review, matching the previous block's trend and confirming C7 bank's data-heavy character.

- **Zero viable code boundaries**: Despite multiple score-4 backtracks across the block (4F14, 5155, 54CC), all targets failed byte-structure review (event script data) or caller quality review (weak/suspect from unresolved regions).

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
- C7:3000..39FF: 0 promotions (notes_64)
- C7:3A00..43FF: 0 promotions (notes_65)
- C7:4400..4DFF: 0 promotions (notes_66)
- C7:4E00..57FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_4e00_57ff_seam_block.json`
- `reports/c7_4e00_57ff_seam_block.md`
- `reports/c7_4f00_4fff_backtrack.json`
- `reports/c7_5200_52ff_backtrack.json`

---

## New live seam: C7:5800..

Next unprocessed block starts at **C7:5800**.

Recommended next move:
1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:5800 --pages 10 --json > reports/c7_5800_61ff_seam_block.json`
2. `python tools/scripts/render_seam_block_report_v1.py --input reports/c7_5800_61ff_seam_block.json --output reports/c7_5800_61ff_seam_block.md`
3. Run owner-backtrack scans only for pages that land in `manual_owner_boundary_review`
4. Write `docs/sessions/chrono_trigger_session15_continue_notes_68.md`
