# Chrono Trigger Session 15 — Continuation Notes 17

## Block closed: C5:5900..C5:62FF (10 pages)

Processed with fully upgraded toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:5900 | mixed_command_data | local_control_only | freeze | no xref hits, no callers |
| C5:5A00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad target; branch-fed pocket |
| C5:5B00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad target (C5:5B22=invalid); branch-fed |
| C5:5C00 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | score-6 backtrack present but target C5:5C50=0x00 (BRK, hard_bad_start) |
| C5:5D00 | candidate_code_lane | mixed_lane_continue | freeze | zero xref hits, zero clusters |
| C5:5E00 | candidate_code_lane | mixed_lane_continue | freeze | zero xref hits, zero clusters |
| C5:5F00 | candidate_code_lane | manual_owner_boundary_review | freeze | see anchor detail below |
| C5:6000 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | 4 hard_bad among 12 raw targets; page poisoned |
| C5:6100 | candidate_code_lane | manual_owner_boundary_review | freeze | see anchor detail below |
| C5:6200 | candidate_code_lane | local_control_only | freeze | soft_bad target C5:62FB (suspect); no weak/strong xref |

---

## Anchor report details

### C5:5F00..5FFF
Targets: C5:5FBA (weak, hits=1), C5:5FBF (weak, hits=1), C5:5F60 (suspect, hits=1)

Best backtrack: C5:5FBD → target C5:5FBF, score=4, start_byte=0x7E (`ROR abs,X`)
- 0x7E is NOT in LIKELY_PROLOG — it's a bitshift operation, not a function preamble
- SED (0xF8) appears at C5:5FC3 — 4 bytes beyond C5:5FBF — `sed_decimal_mode` data-misread signal
- ASCII ratio 0.37 (backtrack region is borderline noisy)
- C5:5FBA: start_byte=0xFE (`INC abs,X`), score=1, no returns in lookahead
- Verdict: no promotable candidate; all three targets have non-prologue start bytes

### C5:6100..61FF
Targets: C5:6161 (weak, hits=1), C5:61E0 (weak, hits=1), C5:6107 (suspect, hits=1)

Best backtrack: C5:6105 → target C5:6107, score=4, start_byte=0xA2 (`LDX #`)
- 0xA2 IS in LIKELY_PROLOG ✓ — this is a legitimate function-entry opcode
- However: reading forward from C5:6105, `LDX #$FE` is 2 bytes → C5:6107 starts next instruction
- C5:6107 = A3 3F → `LDA $3F,S` (stack-relative), then C5:6109 = 0x00 = **BRK**
- BRK at C5:6109 (2 bytes into target) is a strong data-misread indicator
- Additional BRK at C5:6112 — multiple hard barriers in 13-byte range confirms data
- Score=4 achieved via: +1 clean_start + 2 LIKELY_PROLOG + 1 inside_offset (no returns in lookahead)
- Target C5:6107 is `suspect` (not even weak) — caller confidence already lower
- Verdict: near-miss (LIKELY_PROLOG opcode at start) but BRK-contaminated target; no promotion

Other candidates:
- C5:6161: score=3, start_byte=0x94 (`STY dp,X`) — not in LIKELY_PROLOG; blob has returns but start isn't a prologue
- C5:61E0: score=1, start_byte=0x06 (`ASL dp`) — data-pattern bytes (0x00 0x00 at +4/+5)

### C5:6000 notable near-miss
C5:60E0 (weak, hits=3 — highest hit count in block) but page is `bad_start_or_dead_lane_reject` (4 hard_bad entries out of 12 raw targets). Reading C5:60E0 = 0x1C (`TRB abs`) — not in LIKELY_PROLOG. Page is poisoned regardless.

---

## Quiet stretches

- **C5:5D00..5EFF**: two consecutive pages with zero xref hits, zero clusters — complete dead zone
- **C5:5900..5BFF**: all branch_fed or mixed_command, no direct call evidence anywhere

---

## Running promotion count

- C5:3B00..44FF: 0 promotions (notes_14)
- C5:4500..4EFF: 0 promotions (notes_15)
- C5:4F00..58FF: 0 promotions (notes_16)
- C5:5900..62FF: 0 promotions (this note)

Total promotions since seam work began: **0**
Pass estimate: ~729 (continuing from ~721 at start of session)

---

## Toolkit status

All 5 upgrades in production:
1. RTI (0x40) → hard_bad_start ✓
2. PLD (0x2B), PLB (0xAB) → soft_bad_start ✓
3. LIKELY_PROLOG expanded: PHD (0x0B), PHK (0x4B), PHB (0x8B), REP (0xC2) added ✓
4. boundary_bait flag in run_seam_block_v1.py + render ✓
5. check_data_misread_patterns() in seam_triage_utils_v1.py + find_local_code_islands_v2.py ✓

This block had no instances where the new toolkit auto-caught something that changed a decision — the detections in previous blocks (RTI at C5:550D, boundary_bait at C5:54FF) were already re-run in notes_16 re-report.

---

## New live seam: C5:6300..

Next unprocessed block starts at **C5:6300**.

Recommended next move:
1. Run: `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:6300 --pages 10 --json > reports/c5_6300_6cff_seam_block.json`
2. Render: `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_6300_6cff_seam_block.json --output reports/c5_6300_6cff_seam_block.md`
3. Run anchor reports for any `manual_owner_boundary_review` pages
4. Write notes_18
