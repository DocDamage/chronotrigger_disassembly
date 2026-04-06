# Chrono Trigger Session 15 — Continuation Notes 68

## Block closed: C7:5800..C7:61FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:5800 | mixed_command_data | mixed_lane_continue | freeze | 3 targets but event script data patterns, no viable entry points |
| C7:5900 | mixed_command_data | mixed_lane_continue | freeze | mixed lane with local clusters only |
| C7:5A00 | mixed_command_data | mixed_lane_continue | freeze | no strong targets, data patterns dominate |
| C7:5B00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | hard_bad_start signal, invalid targets |
| C7:5C00 | text_ascii_heavy | mixed_lane_continue | freeze | pointer tables with ASCII-range high bytes (false positive classification) |
| C7:5D00 | text_ascii_heavy | mixed_lane_continue | freeze | pointer tables (128 x 16-bit pointers), not dialogue text |
| C7:5E00 | text_ascii_heavy | mixed_lane_continue | freeze | pointer tables targeting C7:3300-46C3 range |
| C7:5F00 | mixed_command_data | local_control_only | freeze | 2 suspect targets, local clusters only, no strong ingress |
| C7:6000 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | 4 targets/6 hits but all event script data, hard_bad_start on 60B9 |
| C7:6100 | mixed_command_data | manual_owner_boundary_review | freeze | score-6 backtracks but event script command patterns, weak callers |

---

## Manual-owner review summary

### C7:6100..C7:61FF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C7:61D1 (1 weak caller from `C7:7C34`)
- C7:61D0 (1 suspect caller from `C7:9ACF`)

Backtrack scan:
- C7:61C6->61D0 score=6
- C7:61C6->61D1 score=6

Both targets achieve maximum score-6 backtracks from shared candidate C7:61C6 with `JSR` (0x20) start byte.

ROM-byte check:
- C7:61C6 = `20 F2 61 C4 05 C4 06 C4 07 C4 08 C4 09 3F BB 04 3F 5E 0E 6F D4 DC 06 D6 02 CB 00 01 7F 09 D4 DC 02`

Byte analysis:
- **Event script data pattern**: High frequency of C4, DC, D6, D4, CB command bytes
- 61D0/61D1 fall within event command sequences, not subroutine boundaries
- `JSR` at 61C6 is within event script context, not 65816 machine code
- Both callers (C7:7C34, C7:9ACF) from unresolved regions

Verdict:
- Despite exceptional score-6 backtracks, byte patterns confirm **event script data**, not executable code
- Shared candidate start for adjacent targets (61D0/61D1) is typical of data structure interpretation, not dual entry points
- Weak/suspect caller quality provides no anchor support

**Frozen.**

---

## Reject-heavy page notes

### C7:6000..C7:60FF (highest activity page)
Summary: raw_targets=4, xref_hits=6, strong_or_weak=1, hard_bad=1, soft_bad=0

Targets:
- C7:60B5 (3 suspect callers from `C7:0362`, `C7:0842`, `C7:0856`)
- C7:60B9 (1 invalid caller from `C7:02A5`) [hard_bad_start]
- C7:60D3 (1 weak caller from `C7:B170`)
- C7:60F5 (1 suspect caller from `C7:2D3E`)

ROM-byte check:
- C7:60A0 = `04 54 E0 1D 0A EB C4 7F D6 03 C9 00 03 BF E0 12 0A EB C4 7F DC 08 E0 14 0A EB C4 7F DC 06 E0 16`

Critical findings:
- **Event script command density**: 47% of bytes in C0-EF range (command opcodes)
- High-frequency bytes: E0 (17x), EB (15x), C4 (14x), DC (14x), 7F (16x), D6 (10x)
- Target 60B5 points to byte 0xD6 — third byte of event command `C4 7F D6 03`
- Target 60B9 points to byte 0x03 — operand, not opcode
- All 4 targets fall within event script command structures

Why rejected despite 6 xref hits:
- **hard_bad_start** on 60B9 (invalid classification)
- Targets are **data addresses misinterpreted as code entry points**
- Callers jump into **middle of event command sequences**, not subroutines
- No local code islands found (`local_island_count: 0`)

This page demonstrates that **high xref count ≠ viable code**. The toolkit correctly rejected despite apparent "high activity."

**Frozen.**

---

### C7:5B00..C7:5BFF
Summary: bad_start_or_dead_lane_reject posture

- Hard_bad_start signal detected
- Invalid target classifications
- No viable entry points

**Frozen.**

---

## Pointer table discovery (C7:5C00-5E00)

The three `text_ascii_heavy` pages contain **16-bit pointer tables**, not dialogue text:

| Page | Content | Pointer Count | Target Range |
|------|---------|---------------|--------------|
| C7:5C00 | 128 × 16-bit LE pointers | 128 (6 null) | C7:3300-46C3 |
| C7:5D00 | 128 × 16-bit LE pointers | 128 (0 null) | C7:3300-46C3 |
| C7:5E00 | 128 × 16-bit LE pointers | 128 (5 null) | C7:3300-46C3 |

**Why classified as text_ascii_heavy:**
- Pointer high bytes (0x33-0x46) fall in ASCII range ('3'-'F')
- Little-endian storage: pointer 0x3446 stored as bytes `[46 34]` = 'F' '4'
- ~35-40% of bytes appear as printable ASCII by coincidence
- This is a **false positive** from the classification heuristic

**Actual content:** Data tables containing addresses, not readable text.

---

## Block read

- **Strongest honest near-miss page**: **C7:6100..C7:61FF** — exceptional score-6 backtracks on both targets (61D0, 61D1) with shared candidate C7:61C6. However, byte-level review revealed event script command patterns (C4, DC, D6, CB frequencies), confirming data rather than executable code. Weak/suspect callers from unresolved regions provided no supporting anchor evidence.

- **Strongest reject signal**: **C7:6000..C7:60FF** — despite being the most active page in the block (4 targets, 6 xref hits), all targets fall within event script command structures. Target 60B9 received hard_bad_start classification (points to operand byte 0x03, not opcode). Demonstrates that high xref counts can occur when callers reference data — the toolkit correctly filtered this before promotion consideration.

- **Pointer table discovery**: Pages C7:5C00, 5D00, 5E00 contain 128-entry pointer tables (16-bit LE) targeting C7:3300-46C3 range. Classified as text_ascii_heavy due to ASCII-range pointer high bytes, but contain no dialogue text.

- **Event script data dominance**: ROM byte analysis across multiple pages confirms event script command patterns (EB, C4, DC, D6, D0, CF frequencies). C7:5800+ continues the data-heavy character established in C7:3A00+.

- **Consistent low manual review rate**: Only 10% (1 of 10 pages) reached manual_owner_boundary_review, matching previous two blocks and confirming C7 bank's transition to data territory.

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
- C7:4E00..57FF: 0 promotions (notes_67)
- C7:5800..61FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_5800_61ff_seam_block.json`
- `reports/c7_5800_61ff_seam_block.md`
- `reports/c7_6100_61ff_backtrack.json`

---

## New live seam: C7:6200..

Next unprocessed block starts at **C7:6200**.

Recommended next move:
1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:6200 --pages 10 --json > reports/c7_6200_6bff_seam_block.json`
2. `python tools/scripts/render_seam_block_report_v1.py --input reports/c7_6200_6bff_seam_block.json --output reports/c7_6200_6bff_seam_block.md`
3. Run owner-backtrack scans only for pages that land in `manual_owner_boundary_review`
4. Write `docs/sessions/chrono_trigger_session15_continue_notes_69.md`

**Note:** C7 bank has approximately 158 pages remaining (C7:6200..FFFF). Based on trajectory analysis, this region is expected to contain primarily event script data, pointer tables, and padding. Consider whether project priorities warrant continued detailed analysis of C7 or a transition to other banks (C8, C9, etc.) with higher code probability.
