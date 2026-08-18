# Session 37 Summary: C3 Low-Bank Forward Seam (C3:5000–C3:5800)

## Date: 2026-04-09
## Scope: C3:5000–C3:5800 (Sequential forward seam continuation from pass 1215)

---

## 1. Executive Summary

Continued the sequential C3 low-bank forward seam from pass 1215's stopping point at C3:5000. Produced **2 passes** (202-203) covering **2048 bytes** (C3:5000–C3:5800). No functions promoted - all 8 pages frozen as data with jump table and data table analysis.

### Key Achievements
- **8 new closed ranges** added to the snapshot (1778 → 1786)
- **2 manifests** created (pass1216, disasm notes)
- **Jump table identification** at C3:5700: C3:5777 is JMP $A22A (not a real function)
- **Data table analysis** at C3:5600: arithmetic progression pattern (+$21)
- **Closed ranges snapshot** maintained at 903 manifest-backed ranges

---

## 2. Pass 202–203 — C3:5000–C3:5800 Data Freeze

### Manifest: `passes/manifests/pass1216_c3_s37.json`

| Range | Classification | Confidence | Key Evidence |
|-------|---------------|------------|--------------|
| C3:5000..C3:50FF | data | high | 2 hard bad starts |
| C3:5100..C3:51FF | data | high | 2 hard bad starts |
| C3:5200..C3:52FF | data | high | 1 hard bad start |
| C3:5300..C3:53FF | data | high | Local control only |
| C3:5400..C3:54FF | data | high | 1 hard bad start |
| C3:5500..C3:55FF | data | high | 1 hard bad start |
| C3:5600..C3:56FF | data | high | Structured data patterns |
| C3:5700..C3:57FF | data | high | Jump table entries |

---

## 3. Technical Analysis

### C3:5700: Jump Table Discovery

The manual review flagged C3:5777 with 2 callers (C3:3059, C3:5BEE). Disassembly revealed:

```
C3:5777: JMP $A22A        ; Jump to bank $A2
C3:577C: JMP $802A        ; Jump to $802A
```

**Key Insight**: This is a **jump table**, not actual functions!

| Feature | Function | Jump Table Entry |
|---------|----------|------------------|
| First instruction | Prologue (PHA, PHP) | JMP $xxxx |
| Size | 10-100 bytes | 3 bytes |
| Returns | 1-3 RTS/RTL | None |
| Purpose | Execute code | Dispatch to code |

The callers aren't calling C3:5777 as a function - they're using it as a trampoline to reach $A22A.

### C3:5600: Data Table Pattern

Highly structured data with arithmetic progression:
```
$21, $42, $63, $84 (+$21 each)
$00, $10, $20, $30 (+$10 each)
```

| Pattern | Interpretation |
|---------|----------------|
| Arithmetic progression | Lookup table |
| Regular spacing | Graphics/tile data |
| High byte structure | Menu/dialog data |

---

## 4. Methodology Validation

### Jump Table Detection
The scanner correctly flagged C3:5777 for manual review, but the JMP opcode at entry should have been a hint:

- **$4C (JMP) at entry** = Dispatch, not function
- **Immediate JMP** = Trampoline pattern
- **Cross-bank targets** ($A22A, $802A) = Far call dispatch

### Data Pattern Recognition
C3:5600 demonstrates the importance of recognizing structured data:

- **Arithmetic sequences** = Tables, not code
- **Regular spacing** = Raster/palette data
- **No returns** = Data region

---

## 5. Artifacts Produced

| Artifact | Path |
|----------|------|
| Pass 1216 manifest | `passes/manifests/pass1216_c3_s37.json` |
| Pass 202 disasm | `passes/disasm/pass202.md` (C3:5700 jump table) |
| Pass 203 disasm | `passes/disasm/pass203.md` (C3:5600 data table) |
| Pass 202 labels | `passes/labels/pass202.md` |
| Session summary | `AGENT_SWARM_SESSION_37_SUMMARY.md` |

---

## 6. Seam Block Analysis Summary

### Page Family Distribution
| Family | Count | Ranges |
|--------|-------|--------|
| branch_fed_control_pocket | 4 | C3:5300, C3:5400, C3:5500, C3:5700 |
| mixed_command_data | 2 | C3:5000, C3:5600 |
| candidate_code_lane | 2 | C3:5100, C3:5200 |

### Review Posture Distribution
| Posture | Count | Ranges |
|---------|-------|--------|
| bad_start_or_dead_lane_reject | 5 | C3:5000-5200, C3:5400-5500 |
| local_control_only | 1 | C3:5300 (frozen) |
| mixed_lane_continue | 1 | C3:5600 (frozen) |
| manual_owner_boundary_review | 1 | C3:5700 (frozen - jump table) |

---

## 7. Next Seam

Resume at **C3:5800**. This continues the low-bank forward seam.

Before proceeding:
1. Run seam block scanner at C3:5800 to identify promotion candidates
2. Check existing flow analysis for C3:5800-5FFF region
3. Verify no overlapping manifests exist for C3:5800+

---

## 8. Coverage Update

| Bank | Previous Ranges | New Ranges | Total |
|------|-----------------|------------|-------|
| C3 | 319 | +8 | 327 |
| **Total** | **976** | **+8** | **984** |

Bank C3 coverage: **~33.0%** → **~33.5%** (estimated)

---

## 9. Technical Notes

### Jump Table Patterns
SNES games commonly use jump tables for:
- **Bank switching**: JMP to routines in other banks
- **Dispatch tables**: Menu or event handlers
- **Trampolines**: 24-bit address formation

Characteristics:
- 3-byte entries (JMP $xxxx)
- Sequentially arranged
- Cross-bank targets
- No prologues or returns

### Data Table Patterns
Structured data recognition:
- Arithmetic progressions → Lookup tables
- Regular null spacing → Graphics data
- Repeating patterns → Tile/palette data
