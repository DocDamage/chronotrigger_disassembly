# Session 33 Summary: C3 Low-Bank Forward Seam (C3:3000–C3:3800)

## Date: 2026-04-09
## Scope: C3:3000–C3:3800 (Sequential forward seam continuation from pass 1210)

---

## 1. Executive Summary

Continued the sequential C3 low-bank forward seam from pass 1210's stopping point at C3:3000. Produced **3 passes** (194–196) covering **2048 bytes** (C3:3000–C3:3800). Three functions promoted from the C3:3500 page; 7 pages frozen as mixed data.

### Key Achievements
- **10 new closed ranges** added to the snapshot (1744 → 1754)
- **3 manifests** created (pass1211, pass1212, disasm notes pass194-196)
- **3 functions promoted** at C3:3500, C3:353B, C3:357A
- **7 data pages frozen** with detailed justification (hard bad starts, suspect callers)
- **Closed ranges snapshot** updated to 903 manifest-backed ranges

---

## 2. Pass 194–196 — C3:3500 Owner Promotions

### Manifest: `passes/manifests/pass1211_c3_s33.json`

| Range | Classification | Confidence | Score | Key Evidence |
|-------|---------------|------------|-------|--------------|
| C3:3500..C3:3526 | owner | medium | 6 | 3 callers (C3:5584, C3:6786, C3:21A8), JSR $350E, $20 clean start |
| C3:353B..C3:3554 | owner | medium | 6 | $A9 LDA clean start, JSR target at $353C |
| C3:357A..C3:3593 | owner | medium | 4 | 3 callers to $357B, caller anchor validation |

### C3:3500 Function Analysis
- **Entry**: JSR $A90B - cross-bank utility call
- **65816 instructions**: TCD ($5B), PER ($62) - native mode code
- **Pattern**: LDA immediate + STA DP for $50, $52, $54, $56, $58
- **Purpose**: Data structure initialization or DMA parameter setup

### C3:353B Function Analysis
- **Entry**: LDA #$00D8 (16-bit immediate)
- **Stores**: $62, $64, $66 - DP variable initialization
- **Note**: Contains RTI at $3546 - possible boundary marker or data coincidence

### C3:357A Function Analysis
- **Entry**: LDA #$55, STA $0B
- **Calls**: JSR $02A2 (low-bank utility)
- **Operations**: AND ($21),Y (indirect indexed), STX $30

---

## 3. Pass 197 — C3:3000–C3:37FF Data Freeze

### Manifest: `passes/manifests/pass1212_c3_s33.json`

| Range | Classification | Confidence | Key Evidence |
|-------|---------------|------------|--------------|
| C3:3000..C3:30FF | data | high | 4 hard bad starts, suspect caller contexts |
| C3:3100..C3:31FF | data | high | 1 hard bad start, mixed command/data patterns |
| C3:3200..C3:32FF | data | high | 2 hard bad starts, branch-fed pocket reject |
| C3:3300..C3:33FF | data | high | 3 hard bad starts, candidate lane reject |
| C3:3400..C3:34FF | data | high | 2 hard bad starts, candidate lane reject |
| C3:3600..C3:36FF | data | high | 1 hard bad start, mixed command/data |
| C3:3700..C3:37FF | data | high | 2 hard bad starts, mixed command/data |

### Key Analysis Insights
- All 7 pages rejected via `bad_start_or_dead_lane_reject` posture
- Local code islands identified but insufficient for standalone promotion
- Strongest candidates (C3:3500+) successfully extracted and promoted
- Remaining regions show data-like characteristics under byte-coincidence analysis

---

## 4. Artifacts Produced

| Artifact | Path |
|----------|------|
| Pass 1211 manifest | `passes/manifests/pass1211_c3_s33.json` |
| Pass 1212 manifest | `passes/manifests/pass1212_c3_s33.json` |
| Pass 194 disasm | `passes/disasm/pass194.md` (C3:3500) |
| Pass 195 disasm | `passes/disasm/pass195.md` (C3:353B) |
| Pass 196 disasm | `passes/disasm/pass196.md` (C3:357A) |
| Pass 194 labels | `passes/labels/pass194.md` |
| Pass 195 labels | `passes/labels/pass195.md` |
| Pass 196 labels | `passes/labels/pass196.md` |
| Closed ranges update | `tools/cache/closed_ranges_snapshot_v1.json` (903 ranges) |
| Session summary | `AGENT_SWARM_SESSION_33_SUMMARY.md` |

---

## 5. Seam Block Analysis Summary

### Page Family Distribution
| Family | Count | Ranges |
|--------|-------|--------|
| branch_fed_control_pocket | 2 | C3:3000, C3:3200 |
| mixed_command_data | 3 | C3:3100, C3:3600, C3:3700 |
| candidate_code_lane | 3 | C3:3300, C3:3400, C3:3500 |

### Review Posture Distribution
| Posture | Count | Ranges |
|---------|-------|--------|
| bad_start_or_dead_lane_reject | 7 | All except C3:3500 |
| manual_owner_boundary_review | 1 | C3:3500 (promoted) |

---

## 6. Next Seam

Resume at **C3:3800**. The seam scanner indicates C3:3800+ continues the pattern of mixed code/data regions.

Before proceeding:
1. Run seam block scanner at C3:3800 to identify next promotion candidates
2. Check existing flow analysis for C3:3800-3FFF region
3. Verify no overlapping manifests exist for C3:3800+

---

## 7. Coverage Update

| Bank | Previous Ranges | New Ranges | Total |
|------|-----------------|------------|-------|
| C3 | 285 | +10 | 295 |
| **Total** | **942** | **+10** | **952** |

Bank C3 coverage: **~30.5%** → **~31.5%** (estimated)

---

## 8. Technical Notes

### 65816 Native Mode Detection
The C3:3500 function uses 65816-specific instructions:
- TCD ($5B) - Transfer 16-bit A to Direct Page Register
- PER ($62) - Push Effective Relative Address

This confirms the code runs in native mode (not 6502 emulation mode).

### Direct Page Variable Cluster
Functions at C3:3500 and C3:353B both initialize consecutive DP variables:
- C3:3500: $50, $52, $54, $56, $58 (even addresses)
- C3:353B: $62, $64, $66 (even addresses)

Pattern suggests structure/array initialization for DMA or register setup.
