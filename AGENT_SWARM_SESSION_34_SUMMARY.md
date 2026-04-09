# Session 34 Summary: C3 Low-Bank Forward Seam (C3:3800–C3:4000)

## Date: 2026-04-09
## Scope: C3:3800–C3:4000 (Sequential forward seam continuation from pass 1212)

---

## 1. Executive Summary

Continued the sequential C3 low-bank forward seam from pass 1212's stopping point at C3:3800. Produced **1 pass** (197) covering **2048 bytes** (C3:3800–C3:4000). No functions promoted - all 8 pages frozen as mixed data with documented code fragments.

### Key Achievements
- **8 new closed ranges** added to the snapshot (1754 → 1762)
- **1 manifest** created (pass1213)
- **Code fragments documented** at C3:3F00: Mode 7 matrix manipulation, window mask settings, WRAM long addressing
- **Closed ranges snapshot** maintained at 903 manifest-backed ranges (pending cache rebuild)

---

## 2. Pass 197 — C3:3800–C3:4000 Data Freeze

### Manifest: `passes/manifests/pass1213_c3_s34.json`

| Range | Classification | Confidence | Key Evidence |
|-------|---------------|------------|--------------|
| C3:3800..C3:38FF | data | high | 5 hard bad starts, suspect callers |
| C3:3900..C3:39FF | data | high | 3 hard bad starts |
| C3:3A00..C3:3AFF | data | high | 3 hard bad starts, mixed command/data |
| C3:3B00..C3:3BFF | data | high | 1 hard bad start, 5 local clusters |
| C3:3C00..C3:3CFF | data | high | 2 hard bad starts, 4 local clusters |
| C3:3D00..C3:3DFF | data | high | 1 hard bad start, 4 local clusters |
| C3:3E00..C3:3EFF | data | high | 3 hard bad starts, 3 local clusters |
| C3:3F00..C3:3FFF | data | high | Fragmented code, no promotable functions |

### C3:3F00 Fragment Analysis

Despite being flagged for manual review, disassembly revealed fragmented code patterns insufficient for promotion:

#### Hardware Register Access Points
- **$211B** (C3:3F24) - Mode 7 Matrix A register
- **$2123** (C3:3F9E) - Window Mask Settings register
- **$038C** (C3:3FC3) - Likely WRAM mirror

#### WRAM Long Addressing (Bank $7E)
- **STA $7E6A5F** at C3:3FB0 - WRAM data structure access
- **$7E6A7E**, **$7E2006** - Additional WRAM references

#### Code Fragments Identified
```
C3:3F20: RTS
C3:3F21: LDA #$01
C3:3F23: CLC
C3:3F24: STZ $211B       ; Clear Mode 7 matrix register

C3:3F99: JSR $36CC        ; Call known utility
C3:3F9C: LDA #$33
C3:3F9E: STA $2123        ; Window mask settings

C3:3FB0: STA $7E6A5F      ; Long store to WRAM
C3:3FB4: LDA #$08
C3:3FB6: PHP
C3:3FB7: STA $7E2006      ; Long store to WRAM
```

#### Why Not Promoted
- No clean entry points with verified caller chains
- Fragmented execution flow with data interspersed
- Byte-coincidence patterns suggest data/table regions
- Local clusters lack sufficient return anchoring

---

## 3. Artifacts Produced

| Artifact | Path |
|----------|------|
| Pass 1213 manifest | `passes/manifests/pass1213_c3_s34.json` |
| Pass 197 disasm | `passes/disasm/pass197.md` (C3:3F00 fragments) |
| Pass 197 labels | `passes/labels/pass197.md` |
| Session summary | `AGENT_SWARM_SESSION_34_SUMMARY.md` |

---

## 4. Seam Block Analysis Summary

### Page Family Distribution
| Family | Count | Ranges |
|--------|-------|--------|
| branch_fed_control_pocket | 3 | C3:3800, C3:3900, C3:3B00 |
| mixed_command_data | 3 | C3:3A00, C3:3E00, C3:3F00 |
| candidate_code_lane | 2 | C3:3C00, C3:3D00 |

### Review Posture Distribution
| Posture | Count | Ranges |
|---------|-------|--------|
| bad_start_or_dead_lane_reject | 7 | C3:3800-3E00 |
| manual_owner_boundary_review | 1 | C3:3F00 (rejected after disassembly) |

---

## 5. Next Seam

Resume at **C3:4000**. This is the next page-aligned boundary continuing the low-bank forward seam.

Before proceeding:
1. Run seam block scanner at C3:4000 to identify promotion candidates
2. Check existing flow analysis for C3:4000-4FFF region
3. Verify no overlapping manifests exist for C3:4000+

---

## 6. Coverage Update

| Bank | Previous Ranges | New Ranges | Total |
|------|-----------------|------------|-------|
| C3 | 295 | +8 | 303 |
| **Total** | **952** | **+8** | **960** |

Bank C3 coverage: **~31.5%** → **~32.0%** (estimated)

---

## 7. Technical Notes

### Mode 7 Register Discovery
The fragment at C3:3F24 accesses **$211B** (Mode 7 Matrix A), indicating:
- SNES background mode 7 manipulation code
- Likely related to screen rotation/scaling effects
- Common in Chrono Trigger's world map and effect sequences

### WRAM Long Addressing Pattern
Multiple **STA $7Exxxx** instructions confirm:
- Active use of 65816 long addressing mode
- WRAM data structures in bank $7E
- Consistent with save data, character stats, or game state

### Conservative Promotion Policy
This session demonstrates the project's conservative promotion standard:
- Requires score >= 6 with verified callers
- Needs clean entry points and coherent execution flow
- Fragments with hardware register access but poor caller evidence are frozen, not promoted
