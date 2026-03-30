# Chrono Trigger Session 15 — Continuation Notes 49

## Block closed: C6:9A00..C6:A3FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:9A00 | mixed_command_data | mixed_lane_continue | freeze | no ingress targets, no local clusters |
| C6:9B00 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:9B30` with no strong/weak support |
| C6:9C00 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:9C2E` plus only score-2 backtrack |
| C6:9D00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid `C6:9D0B` with `hard_bad=1` |
| C6:9E00 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:9F00 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:A000 | mixed_command_data | manual_owner_boundary_review | freeze | weak/suspect mix collapsed under bad start bytes and unresolved callers |
| C6:A100 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:A1E0` with `soft_bad=1` |
| C6:A200 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | invalid `C6:A201` (`cop_barrier`) plus weak-only `A28B/A2BF` pressure |
| C6:A300 | text_ascii_heavy | local_control_only | freeze | text-heavy page with lone suspect target `C6:A321` |

---

## Manual-owner page detail

### C6:A000..A0FF
Summary: raw_targets=5, xref_hits=9, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C6:A043 (4 weak callers from unresolved `C6:E1xx..E4xx`)
- C6:A0BF (2 weak callers from unresolved `C6:E05C`, `C6:E67E`)
- C6:A004 (suspect, caller C6:1E6B from frozen data)
- C6:A05F (suspect, caller C6:06C2 from frozen data)
- C6:A0FF (suspect, caller C6:1238 from frozen data)

Backtrack scan (`reports/c6_a000_a0ff_backtrack.json`):
- C6:A051->A05F score=6, start=0x08
- C6:A038->A043 score=4, start=0x07
- C6:A000->A004 score=2, start=0x0C
- C6:A0AF->A0BF score=2, start=0x79

Anchor reports:
- C6:A043: strong=0, weak=4, invalid=0
- C6:A0BF: strong=0, weak=2, invalid=0

ROM-byte check:
- C6:A043 = `1E 1D D5 0F 60 F8 7E 2C 2D 3D 2E 49`
- C6:A05F = `2D 2E B1 B1 9F 02 A2 02 DD C3 1E 45`
- C6:A0BF = `11 69 06 56 08 50 1E EB 08 D4 AF FE`

Verdict:
- `A043` has the most caller traffic but still opens on `1E` (`ASL abs,X`), not a defensible function entry.
- `A05F` got the best backtrack score, but it opens on `2D` (`AND abs`), which still fails the entry-byte test.
- `A0BF` keeps two weak unresolved callers, but the target byte `11` (`ORA (dp),Y`) is not a credible owner start.
- The data-side callers into `A004`, `A05F`, and `A0FF` now downgrade to suspect-only evidence under the repaired snapshot layer.

**Frozen.**

---

## Reject-heavy page note

### C6:A200..A2FF
Summary: raw_targets=4, xref_hits=5, strong_or_weak=3, hard_bad=1, soft_bad=0

Targets:
- C6:A201 (weak anchor from C6:AAD9, but invalid effective strength due `cop_barrier`)
- C6:A28B (weak, caller C6:E7FB)
- C6:A2BF (weak, callers C6:E065 and C6:E687)
- C6:A200 (suspect, caller C6:05A0 from frozen data)

Backtrack scan from block report:
- C6:A200->A201 score=4
- C6:A28A->A28B score=4
- C6:A2B0->A2BF score=4

ROM-byte check:
- C6:A201 = `02 F4 58 80 B9 01 02 E2 60 2A 04 D6`
- C6:A28B = `28 82 83 76 77 82 83 01 60 F8 40 40`
- C6:A2BF = `23 60 F8 AA 01 49 00 14 15 05 07 16`

Verdict:
- `A201` is killed immediately by the `cop_barrier` start byte.
- `A28B` and `A2BF` keep only weak unresolved callers and still do not open on defensible owner bytes.
- The branch-fed-control-pocket classification is real, but it does not survive the bad-start gate.

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **`C6:A000..A0FF`** — only page that still reached `manual_owner_boundary_review`, but its best-supported targets collapsed on bad start bytes (`A043=ASL abs,X`, `A05F=AND abs`, `A0BF=ORA (dp),Y`).
- **Strongest reject signal**: **`C6:A200..A2FF`** — branch-fed control pocket with three strong/weak effective hits, but invalid `A201` plus weak-only `A28B/A2BF` kept the page reject-heavy.
- The rest of the block mostly relaxed into no-ingress or suspect-only freeze territory.

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
- C6:9A00..A3FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_9a00_a3ff_seam_block.json`
- `reports/c6_9a00_a3ff_seam_block.md`
- `reports/c6_a000_a0ff_flow.json`
- `reports/c6_a000_a0ff_backtrack.json`
- `reports/c6_a200_a2ff_flow.json`
- `reports/C6_A043_anchor.json`
- `reports/C6_A0BF_anchor.json`
- `reports/C6_A28B_anchor.json`
- `reports/C6_A2BF_anchor.json`

---

## New live seam: C6:A400..

Next unprocessed block starts at **C6:A400**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:A400 --pages 10 --json > reports/c6_a400_adff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_a400_adff_seam_block.json --output reports/c6_a400_adff_seam_block.md`
3. Run owner-backtrack scans only for pages that still land in `manual_owner_boundary_review`, then write notes_50.
