# Chrono Trigger Session 15 — Continuation Notes 65

## Block closed: C7:3A00..C7:43FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:3A00 | mixed_command_data | manual_owner_boundary_review | freeze | weak `3AF5` with single unresolved caller; mixed data patterns dominate |
| C7:3B00 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | `3BA1` is strong RTS return (score 6) but single weak caller unresolved |
| C7:3C00 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | `3C12` score 6 but single weak caller from `E7:11FD` never upgrades |
| C7:3D00 | mixed_command_data | manual_owner_boundary_review | freeze | `3DE1` score 6, 2-byte distance from prologue, but unresolved caller quality fails |
| C7:3E00 | mixed_command_data | manual_owner_boundary_review | freeze | `3ED1/3ED2` candidates 1 byte apart — internal labels, not defensible owners |
| C7:3F00 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | `3FC2` score 4 but weak caller + mixed page signals reject |
| C7:4000 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | suspect targets with invalid companion starts; reject-heavy page |
| C7:4100 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | `4133` PHB prologue weak; `418D` score 4 but all 6 callers SUSPECT from data regions |
| C7:4200 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | mixed control/data with no ingress strong enough to matter |
| C7:4300 | dead_zero_field | dead_lane_reject | freeze | dead_zero_field — no viable targets, zero ingress |

---

## Manual-owner review summary

Seven pages survived into `manual_owner_boundary_review`:
- `C7:3A00..C7:3AFF`
- `C7:3B00..C7:3BFF`
- `C7:3C00..C7:3CFF`
- `C7:3D00..C7:3DFF`
- `C7:3E00..C7:3EFF`
- `C7:3F00..C7:3FFF`
- `C7:4100..C7:41FF`

### C7:3A00..3AFF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C7:3AF5 (1 weak caller from unresolved)

Backtrack scan:
- C7:3AED->3AF5 score=4

ROM-byte check:
- C7:3AED = `A5 11 29 FF 00 C9 80 00 90 02 A9 80 00 85 11 A5`
- C7:3AF5 = `90 02 A9 80 00 85 11 A5 0F C9 00 10 30 03 4C 6D`

Verdict:
- `3AF5` is the only target in the page. Single weak caller from unresolved region cannot support promotion.
- Page shows mixed command/data patterns throughout.

**Frozen.**

### C7:3B00..3BFF
Summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C7:3BA1 (1 weak caller from unresolved) — RTS return, score 6

Backtrack scan:
- C7:3B93->3BA1 score=6

ROM-byte check:
- C7:3B93 = `8B 0B A5 11 29 FF 00 C9 80 00 90 02 A9 80 00 85`
- C7:3BA1 = `90 02 A9 80 00 85 11 A5 0F C9 00 10 30 03 4C 8D`

Verdict:
- `3BA1` is a complete function with PHP prologue and RTS return, score 6.
- However, single weak caller from unresolved region keeps it frozen.
- Do not promote without stronger caller evidence.

**Frozen.**

### C7:3C00..3CFF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C7:3C12 (1 weak caller from `E7:11FD`)

Backtrack scan:
- C7:3C04->3C12 score=6

ROM-byte check:
- C7:3C04 = `A9 08 00 20 F7 03 C7 29 FF 7F C9 00 00 F0 13 A5`
- C7:3C12 = `C9 00 00 F0 13 A5 11 C9 00 10 10 0D A5 0F C9 00`

Verdict:
- `3C12` backtracks cleanly with score 6.
- Single weak caller from `E7:11FD` (unresolved region) prevents promotion.
- Do not promote without stronger caller evidence.

**Frozen.**

### C7:3D00..3DFF
Summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C7:3DE1 (1 weak caller from unresolved) — 2-byte distance, score 6

Backtrack scan:
- C7:3DDF->3DE1 score=6

ROM-byte check:
- C7:3DDF = `08 C2 20 A5 11 38 E9 00 10 85 11 B0 02 C6 13 28`
- C7:3DE1 = `C2 20 A5 11 38 E9 00 10 85 11 B0 02 C6 13 28 60`

Verdict:
- `3DE1` shows PHP/PLP + SBC arithmetic pattern, score 6.
- Only 2 bytes from prologue start (`3DDF`).
- Weak/unresolved caller quality keeps it frozen.

**Frozen (WEAK/UNRESOLVED).**

### C7:3E00..3EFF
Summary: raw_targets=3, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C7:3ED1 (1 weak caller)
- C7:3ED2 (1 weak caller) — shares candidate with 3ED1, 1 byte apart

Backtrack scan:
- C7:3EC9->3ED1 score=4
- C7:3ECA->3ED2 score=4

ROM-byte check:
- C7:3EC9 = `A9 01 00 85 0B A9 0A 00 85 0D 80 2D A9 03 00 80`
- C7:3ED1 = `80 2D A9 03 00 80 28 A9 0F 00 80 23 A9 1E 00 80`
- C7:3ECA = `01 00 85 0B A9 0A 00 85 0D 80 2D A9 03 00 80 28`
- C7:3ED2 = `00 85 0B A9 0A 00 85 0D 80 2D A9 03 00 80 28 A9`

Verdict:
- `3ED1` and `3ED2` are only 1 byte apart — internal labels, not independent function starts.
- Both share the same candidate location; neither rises to defensible boundary status.
- Not promoted — treat as internal structure.

**Frozen.**

### C7:3F00..3FFF
Summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C7:3FC2 (1 weak caller)

Backtrack scan:
- C7:3FB8->3FC2 score=4

ROM-byte check:
- C7:3FB8 = `A0 0F 00 B9 B3 3E C5 11 90 10 B9 B3 3E C5 0F 90`
- C7:3FC2 = `B9 B3 3E C5 0F 90 08 88 10 EE 38 60 18 60 00 00`

Verdict:
- `3FC2` shows LDY + RTS + BCC coherent pattern, score 4.
- Weak caller plus mixed page signals result in rejection.

**Frozen (REJECT).**

### C7:4100..41FF
Summary: raw_targets=4, xref_hits=7, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C7:4133 (1 weak caller from unresolved) — PHB prologue
- C7:418D (score 4, 6 callers) — BUT all 6 callers are SUSPECT from data regions

Backtrack scan:
- C7:412B->4133 score=4
- C7:418C->418D score=4

ROM-byte check:
- C7:412B = `8B 4B AB C2 20 A9 00 00 A8 A2 00 00 86 16 A2 00`
- C7:4133 = `A2 00 00 86 16 A2 00 00 86 18 A9 00 00 85 1A A9`
- C7:418C = `22 5F 09 C5 22 B9 3D C5 22 65 0F C5 AB 28 6B 00`
- C7:418D = `5F 09 C5 22 B9 3D C5 22 65 0F C5 AB 28 6B 00 00`

Verdict:
- `4133` has PHB prologue pattern but single weak unresolved caller.
- `418D` has impressive 6-call ingress BUT all callers are flagged SUSPECT from data regions.
- JSL instructions at `418C` look coherent, but suspect caller quality poisons the promotion case.
- This is the strongest near-miss of the block, but still fails the caller-quality threshold.

**Frozen (REJECT for 418D, WEAK for 4133).**

---

## Strongest honest near-miss page

### C7:4100..41FF

This page represents the strongest honest near-miss in the entire block:
- `4133` presents a PHB prologue sequence (classic function start pattern)
- `418D` has 6 incoming callers — the highest caller count in the block

However:
- `4133` has only 1 weak caller from unresolved region
- `418D`'s 6 callers are ALL flagged SUSPECT from data regions

The coherent JSL long-jump instructions at `418C` (`22 5F 09 C5`) show genuine 65816 code structure, but the suspect caller quality makes this a false positive. This is exactly the kind of page that looks promotable at first glance but fails under boundary discipline.

**Frozen.**

---

## Strongest reject signal

### C7:4300..43FF (dead_zero_field)

This page is classified as `dead_zero_field` — the strongest automatic reject category.

Characteristics:
- No viable targets identified
- Zero ingress references
- Dead lane with no code ownership candidates

Unlike the near-miss pages, this requires no manual boundary review. The dead_zero_field classification triggers immediate freeze without promotion consideration.

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **`C7:4100..C7:41FF`** — `418D` had 6 callers (highest in block) and `4133` showed PHB prologue pattern, but suspect caller quality from data regions poisoned the promotion case.
- **Strongest reject signal**: **`C7:4300..C7:43FF`** — dead_zero_field with zero viable targets and zero ingress.
- Seven pages reached `manual_owner_boundary_review` (70% of block), significantly higher than previous blocks, but all failed on caller quality or unresolved status.
- Two pages (`C7:4000` and `C7:4200`) were rejected via `bad_start_or_dead_lane_reject`.
- Notable pattern: Multiple pages had high backtrack scores (4-6) but were undone by weak/unresolved callers from suspect regions.

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
- C7:3A00..43FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_3a00_43ff_seam_block.json`
- `reports/c7_3a00_43ff_seam_block.md`
- `reports/c7_3a00_3aff_backtrack.json`
- `reports/c7_3b00_3bff_backtrack.json`
- `reports/c7_3c00_3cff_backtrack.json`
- `reports/c7_3d00_3dff_backtrack.json`
- `reports/c7_3e00_3eff_backtrack.json`
- `reports/c7_3f00_3fff_backtrack.json`
- `reports/c7_4100_41ff_backtrack.json`

---

## New live seam: C7:4400..

Next unprocessed block starts at **C7:4400**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:4400 --pages 10 --json > reports/c7_4400_4dff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c7_4400_4dff_seam_block.json --output reports/c7_4400_4dff_seam_block.md`
3. Run owner-backtrack scans only for pages that still land in `manual_owner_boundary_review`, then write notes_66.
