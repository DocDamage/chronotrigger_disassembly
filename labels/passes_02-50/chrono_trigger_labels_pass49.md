# Chrono Trigger Disassembly Labels — Pass 49

This file contains labels newly added, corrected, or materially strengthened in pass 49.

As in prior passes:
- **strong** = directly supported by control flow and data role in the ROM work of this pass
- **strengthened** = previously useful label materially tightened by new proof
- **provisional** = structurally useful but still not safe as a final gameplay-facing name

---

## Strong labels

### C1:011B  ct_c1_lsr3_entry                                          [strong]
- Mid-routine entry into the `LSR` helper band.
- Executes exactly three `LSR A` operations before `RTS`.
- Corrects pass 48’s earlier loose `>> 8` interpretation.

### 7E:5E30  ct_c1_lane_current_hp                                     [strong]
- Rendered as the first 3-digit numeric lane field in `C1:0299`.
- Compared against `5E32 >> 3` in both UI and non-UI logic.
- Mutated directly and clamped against `5E32` in `C1:EC90..ECD7`.
- Strongest safe reading now: current HP.

### 7E:5E32  ct_c1_lane_max_hp                                         [strong]
- Rendered as the second 3-digit numeric lane field in `C1:0299`.
- Divided by 8 for the low-HP threshold test.
- Used as the clamp/cap for `5E30` in `C1:EC90..ECD7`.
- Strongest safe reading now: max HP.

### 7E:5E2F.bit0  ct_c1_lane_low_hp_critical_flag                      [strong]
- Cleared, then conditionally set in `C1:B094..B0B3`.
- Condition is driven by `5E30` versus `5E32 >> 3`.
- Strongest safe reading: low-HP / critical threshold flag.

### 7E:A10F  ct_c1_lane_hp_threshold_numeric_attr_selector             [strong]
- Reset per lane before numeric field generation in `C1:0299`.
- Incremented only through the `currentHP` versus `maxHP/8` compare path.
- Immediately consumed to choose between paired-byte values `0x29` and `0x2D` for the lane’s rendered digits.
- Strongest safe reading: lane-local HP-threshold presentation selector/count.

---

## Strengthened labels

### C1:0299  ct_c1_rebuild_full_companion_strip_0cc0                   [strengthened]
- Pass 47 proved this was the full strip rebuild entry.
- Pass 48 proved it contained rendered numeric fields.
- Pass 49 tightens the three dynamic fields inside it to:
  - current HP
  - max HP
  - current MP (still slightly more conservative than the HP pair)
- The routine is now best understood as a per-lane status-field strip rebuild path, not a generic glyph mixer.

### 7E:0CC0..7E:0E08  ct_c1_companion_paired_byte_strip_buffer         [strengthened]
- Previously known as a paired-byte companion strip.
- Pass 49 materially tightens its live content model:
  - fixed lane glyphs
  - HP/max HP decimal fields
  - current-MP-like decimal field
  - threshold-sensitive paired-byte selection
  - meter/bar content
- This is now much harder as a status-lane presentation buffer.

### 7E:9F20  ct_c1_companion_strip_layout_mode_3state                  [strengthened]
- Earlier passes proved it selects layout variants.
- With the HP/maxHP/MP field family now resolved harder, the layout mode is better understood as repositioning a stable status-field bundle rather than arbitrary numeric fragments.

### C1:B094..C1:B0B3  ct_c1_update_lane_low_hp_threshold_flag          [strengthened]
- Previously part of a vague flag-maintenance band.
- Pass 49 proves this exact routine clears and re-establishes `5E2F.bit0` from the `maxHP/8` versus current HP test.

---

## Provisional labels

### 7E:5E34  ct_c1_lane_current_mp                                    [provisional]
- Rendered as the third lane numeric field through the 2-digit formatter.
- Participates in a lane-selected subtract/update path at `C1:CC74..CCC5`.
- Grouped tightly with the now-strong HP pair in the same per-lane panel record.
- Strongest safe reading now: current MP.
- Kept provisional only because pass 49 did not yet pin the cleanest possible direct “tech cost / MP spend” caller chain.

### C1:CC74..C1:CCC5  ct_c1_lane_selected_resource_spend_on_5e34_family [provisional]
- Subtracts a computed quantity from exactly one of:
  - `5E34`
  - `5EB4`
  - `5F34`
- Strongly looks like a lane-selected spend/update path for the field now best read as current MP.
- Still kept provisional until the caller-side action family is nailed harder.

---

## Corrected labels / interpretations

### Previous pass-48 wording “`5E32 >> 8`”                               [corrected]
- This should be read as `5E32 >> 3` in the `C1:0299` compare path.
- The earlier wording came from reading the helper family too broadly instead of the actual `011B` entry point.

### 7E:A10F  old wording “numeric threshold or warning counter”         [replaced]
- Too vague after pass 49.
- The ROM now supports a harder reading: a lane-local HP-threshold presentation selector/count.

---

## Still intentionally unresolved

### Exact visible palette/color meaning of paired bytes `0x29` vs `0x2D` [unresolved]
- Pass 49 proves the selector role and the HP-threshold dependency.
- It does not prove the human-facing color/palette names with enough directness to freeze them.

### Exact final caller identity for the `5E34` spend path               [unresolved]
- Strongly MP-like.
- Not yet locked to the cleanest exact caller chain.

### Final destination-side subsystem name for the bank-`C0` consumer    [unresolved]
- The producer side is now status-panel-like enough to tighten further later.
- The exact destination-side label is still being kept conservative.
