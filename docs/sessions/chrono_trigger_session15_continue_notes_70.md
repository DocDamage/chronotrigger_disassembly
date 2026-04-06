# Chrono Trigger Session 15 — Continuation Notes 70

## Block closed: C7:6C00..C7:75FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:6C00 | mixed_command_data | mixed_lane_continue | freeze | 1 suspect target, event script patterns |
| C7:6D00 | mixed_command_data | local_control_only | freeze | local clusters only |
| C7:6E00 | mixed_command_data | local_control_only | freeze | local clusters only |
| C7:6F00 | mixed_command_data | manual_owner_boundary_review | freeze | weak targets, event script data, weak callers |
| C7:7000 | mixed_command_data | mixed_lane_continue | freeze | 1 weak target |
| C7:7100 | mixed_command_data | local_control_only | freeze | local clusters only |
| C7:7200 | mixed_command_data | manual_owner_boundary_review | freeze | weak target, transition region, weak caller |
| C7:7300 | candidate_code_lane | local_control_only | freeze | prologues present but no coherent functions |
| C7:7400 | candidate_code_lane | mixed_lane_continue | freeze | score-6 backtrack is false positive (TRB, not entry) |
| C7:7500 | candidate_code_lane | mixed_lane_continue | freeze | prologues but minimal returns, suspect structure |

---

## Manual-owner review summary

### C7:6F00..C7:6FFF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C7:6FCD (1 weak caller from `C7:C0D0`)
- C7:6FE4 (1 weak caller from `C7:7C6B`)

Backtrack scan:
- C7:6FBD->6FCD score=2
- C7:6FD6->6FE4 score=4

Anchor reports:
- **Classification: valid / weak / unresolved** for both targets
- Both callers from **unresolved regions**

ROM-byte check:
- **Event script data dominance**: ~25% EF bytes (event end/return opcodes)
- Pattern: `EF C6 BA BD 5D 06 20 E9 EF 27 CB EF B6 29 CC EF` - classic event script
- No function prologues detected
- Backtrack candidates start with data bytes (D4 event command, 4C JMP data-driven)

Verdict:
- Both targets are data addresses, not function entries
- Event script patterns throughout entire page
- Weak callers from unresolved regions provide no anchor support

**Frozen.**

---

### C7:7200..C7:72FF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Target:
- C7:7253 (1 weak caller from `D9:784F`)

Backtrack scan:
- C7:7250->7253 score=4

Anchor report:
- **Classification: valid / weak / unresolved**
- Caller from **unresolved region**

ROM-byte check:
- **Mixed transition page**: Event data (7200-724F) → code-like region (7250+)
- Prologue found at 7250: `C2 BE` (REP #$BE) - clears status bits
- Local clusters show code-like structure with branches
- Boundary between event data and code around middle of page

Verdict:
- Target 7253 has weak caller from unresolved region
- Page shows transition but insufficient anchor quality for promotion
- Recommend split consideration at 0x7250 but freeze for now

**Frozen.**

---

## Candidate_code_lane pages analysis

### C7:7300, 7400, 7500 — New family appearance

These three pages were classified as `candidate_code_lane` (cleaner code regions), differing from the `mixed_command_data` that dominated previous blocks.

**Analysis results:**

| Metric | C7:7300 | C7:7400 | C7:7500 |
|--------|---------|---------|---------|
| Prologues | 4 | 6 | 2 |
| RTS | 0 | 1 | 0 |
| RTL | 1 | 0 | 1 |
| RTI | 1 | 1 | 1 |
| Code density | 12% | 15% | 10% |
| Unique bytes | 97 | 111 | 102 |

**Key findings:**

1. **Prologues present but inconsistent**: REP/SEP variants appear mid-stream, not at function boundaries. Example: C7:7400 has consecutive REP #C2 / REP #33 at offsets +3C/+3D (atypical for real code).

2. **Minimal returns**: Only ONE RTS across all three pages (C7:7400 at +10). Real code pages typically have multiple scattered RTS/RTL at function exits.

3. **C7:7400 score-6 backtrack — FALSE POSITIVE:**
   ```
   740C: C2 01    REP #$01      
   740E: 1C E1 60 TRB $60E1     <- Target (NOT a function entry!)
   7410: 60       RTS           
   ```
   - Target 740E starts with TRB (read-modify-write), not a prologue
   - Consecutive REP instructions impossible in real code flow
   - Score-6 results from misaligned disassembly, not valid code structure

4. **Other targets on 7400:**
   - C7:741E: `44 F0 FF` = MVP (block move) — **data**, not code entry
   - C7:7422: `33 DF` = DEC ($DF,S),Y — valid opcode but NOT a function boundary

**Conclusion:** The `candidate_code_lane` designation is misleading. These pages contain:
- Fragmented executable snippets interleaved with data
- Control flow data (branch tables, jump vectors)
- Game state/command structures with embedded function pointers

**NOT coherent function structures suitable for promotion.**

---

## Block read

- **Strongest honest near-miss page**: **C7:7400..C7:74FF** — classified as `candidate_code_lane` with score-6 backtrack initially suggesting viable code. Detailed analysis revealed the score-6 was a **false positive** from misaligned disassembly (TRB instruction at 740E, not a function entry). Prologues present but inconsistent, only one RTS in entire page.

- **Manual review rate increase**: **20%** (2/10 pages) vs 10% in previous blocks. Both manual-review pages (6F00, 7200) had weak callers from unresolved regions and were correctly frozen.

- **New family appearance**: `candidate_code_lane` appeared for first time in C7:7300-7500, but analysis shows this designation was triggered by presence of call instructions (JSR/JSL) rather than coherent function structure.

- **No bad starts**: All 10 pages showed zero hard/soft bad start hits — cleaner block than some previous ones, but still insufficient for promotion.

- **Caller quality critical finding**: All anchor reports confirmed **weak callers from unresolved regions**. The circular dependency continues: potential targets exist but callers are unresolved, preventing promotion chain from forming.

- **Score-6 false positive lesson**: C7:740E demonstrated that even maximum backtrack scores can result from misaligned instruction boundaries. Byte-level review (revealing TRB opcode) was essential to prevent false promotion.

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
- C7:5800..61FF: 0 promotions (notes_68)
- C7:6200..6BFF: 0 promotions (notes_69)
- C7:6C00..75FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_6c00_75ff_seam_block.json`
- `reports/c7_6c00_75ff_seam_block.md`
- `reports/c7_6f00_6fff_backtrack.json`
- `reports/c7_7200_72ff_backtrack.json`
- `reports/C7_740E_anchor.json`
- `reports/C7_6FCD_anchor.json`
- `reports/C7_6FE4_anchor.json`

---

## New live seam: C7:7600..

Next unprocessed block starts at **C7:7600**.

### Block analysis summary

This block showed increased manual review rate (20%) and new `candidate_code_lane` family, but all analysis confirmed data/event script patterns. Key lessons:

1. **Score-6 backtracks can be false positives** — C7:740E TRB instruction demonstrated need for byte-level verification
2. **Candidate_code_lane ≠ promotable** — presence of prologues without coherent function structure
3. **Caller quality remains critical blocker** — all callers from unresolved regions

### Remaining C7 bank

~138 pages (C7:7600..FFFF). Estimated 14 more ten-page blocks.

### Next steps

1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:7600 --pages 10 --json > reports/c7_7600_7fff_seam_block.json`
2. `python tools/scripts/render_seam_block_report_v1.py --input reports/c7_7600_7fff_seam_block.json --output reports/c7_7600_7fff_seam_block.md`
3. Run owner-backtrack and anchor reports for manual-review pages
4. Write `docs/sessions/chrono_trigger_session15_continue_notes_71.md`
