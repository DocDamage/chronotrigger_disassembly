# Chrono Trigger Session 15 — Continuation Notes 66

## Block closed: C7:4400..C7:4DFF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:4400 | text_ascii_heavy | mixed_lane_continue | freeze | ASCII text/data patterns; pointer tables masquerading as code; zero ingress |
| C7:4500 | text_ascii_heavy | local_control_only | freeze | text-heavy page with local clusters; no promotion candidates |
| C7:4600 | text_ascii_heavy | bad_start_or_dead_lane_reject | freeze | hard_bad_start at 46C8; zero-filled padding misidentified as code target |
| C7:4700 | mixed_command_data | local_control_only | freeze | local clusters only (478B, 471A); no owner-quality targets |
| C7:4800 | mixed_command_data | local_control_only | freeze | suspect targets only (4851, 48EF); callers lack sufficient strength |
| C7:4900 | mixed_command_data | mixed_lane_continue | freeze | no targets identified; mixed lane with no ingress |
| C7:4A00 | mixed_command_data | mixed_lane_continue | freeze | no targets identified; data-heavy page |
| C7:4B00 | mixed_command_data | local_control_only | freeze | single local cluster (4B7C); no owner candidates |
| C7:4C00 | mixed_command_data | local_control_only | freeze | local clusters only (4CB5, 4C16); no promotable targets |
| C7:4D00 | mixed_command_data | manual_owner_boundary_review | freeze | weak 4DD4 and suspect 4D11 both fail caller quality and byte-structure review |

---

## Manual-owner review summary

Only one page survived into `manual_owner_boundary_review`:

### C7:4D00..C7:4DFF
Summary: raw_targets=2, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C7:4DD4 (1 weak caller from `C7:91CB`)
- C7:4D11 (2 suspect callers from `C7:B1B9`, `C7:B426`)

Backtrack scan:
- C7:4DCA->4DD4 score=4
- C7:4D06->4D11 score=2

Anchor report for C7:4DD4:
- **Classification: valid / weak / unresolved**
- Caller `C7:91CB` lives in **unresolved bytes**, providing insufficient anchor evidence

ROM-byte check:
- C7:4DCA = `A9 EB C4 38 D0 CF 12 09 E2 02 0D CF 31 E3 EB C4 38 D2 DC 06 D6 03 CB 00 01 7F C9 0B 01 7F 09 DC 01 C8 0C 18 0A EB C4 00 D0 CF 11 DF 01 01 EB D2`
- While the sequence decodes to valid 65816 instructions, patterns suggest data rather than code:
  - `C4 38` appears twice in 16 bytes (repetitive)
  - `CF` and `EB` bytes appear with suspicious frequency
  - Large backward branch (`D0 CF` = -49 bytes) unusual for function entry
  - C7:4DD4 falls at offset 10, making it an **interior instruction**, not a callable boundary

C7:4D06 bytes:
- `CF 1C 06 EB C4 70 D2 DC 04 D6 02 DD 0A E0 17 C8 38 10 E4 06 EB C4 00 DC 06 D6 02 0A D8 DD 08 55`
- Starts with `CF` (CMP absolute long) - not a typical function prologue
- No coherent entry point pattern

Verdict:
- 4DD4's score-4 backtrack cannot overcome weak caller and data-like byte structure
- 4D11's score-2 backtrack is below threshold and suspect callers provide no support
- Neither target represents a defensible code boundary

**Frozen.**

---

## Reject-heavy page note

### C7:4600..C7:46FF (text_ascii_heavy with hard_bad_start)
Summary: raw_targets=1, xref_hits=1, strong_or_weak=0, hard_bad=1, soft_bad=0

Target:
- C7:46C8 (1 invalid caller from `C7:6E5E`) [hard_bad_start]

Backtrack scan:
- C7:46C8->46C8 score=-8 (self-loop indicates data misinterpretation)

ROM-byte check:
- C7:46C8 region: `00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 DF 46 EA 46 00 00 00 00 00 00 00 00 00`
- Zero-filled padding with occasional pointer bytes (`DF 46`, `EA 46`)
- Target starts with byte `0x00` (BRK) - classic hard_bad_start indicator

Caller analysis:
- C7:6E5E contains bytes `20 C8 46` which appears as `JSR $46C8`
- However, C7:6E00 region contains non-code patterns (high frequency of `EB`, `DC`, `D6`, `D4`, `D2`)
- The "JSR" is a **false positive from data table scanning** - this is not executable code

Verdict:
- Clear case of zero-filled padding being targeted by a misaligned data byte pattern
- The `text_ascii_heavy` family combined with `hard_bad_start` rejection makes this unambiguous
- Toolkit heuristics worked correctly

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **C7:4D00..C7:4DFF** — the only manual-review page in this block. 4DD4 had score-4 backtrack but weak caller and data-like bytes prevented promotion. 4D11 had suspect callers and below-threshold backtrack.
- **Strongest reject signal**: **C7:4600..C7:46FF** — text_ascii_heavy with hard_bad_start at 46C8; zero-filled padding misidentified as code; false-positive caller from data region.
- **New pattern emergence**: Three consecutive text_ascii_heavy pages (4400, 4500, 4600) mark first major data/text region in C7 bank. These contain pointer tables with ASCII-range high bytes, not actual text.
- **Dramatic shift in manual review rate**: Dropped to **10%** (1 of 10 pages) from **70%** in previous block — clear signal that C7 bank is transitioning from code-heavy to data-heavy regions.
- **Zero promotions** continues the conservative streak: 530 pages processed without a single promotion, validating the toolkit's discipline.

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
- C7:4400..4DFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_4400_4dff_seam_block.json`
- `reports/c7_4400_4dff_seam_block.md`
- `reports/c7_4d00_4dff_backtrack.json`
- `reports/C7_4DD4_anchor.json`

---

## New live seam: C7:4E00..

Next unprocessed block starts at **C7:4E00**.

Recommended next move:
1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:4E00 --pages 10 --json > reports/c7_4e00_57ff_seam_block.json`
2. `python tools/scripts/render_seam_block_report_v1.py --input reports/c7_4e00_57ff_seam_block.json --output reports/c7_4e00_57ff_seam_block.md`
3. Run owner-backtrack scans only for pages that land in `manual_owner_boundary_review`
4. Write `docs/sessions/chrono_trigger_session15_continue_notes_67.md`
