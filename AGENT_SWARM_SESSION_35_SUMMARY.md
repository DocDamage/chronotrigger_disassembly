# Session 35 Summary: C3 Low-Bank Forward Seam (C3:4000–C3:4800)

## Date: 2026-04-09
## Scope: C3:4000–C3:4800 (Sequential forward seam continuation from pass 1213)

---

## 1. Executive Summary

Continued the sequential C3 low-bank forward seam from pass 1213's stopping point at C3:4000. Produced **1 pass** (198) covering **2048 bytes** (C3:4000–C3:4800). No functions promoted - all 8 pages frozen as data with documented false positive analysis.

### Key Achievements
- **8 new closed ranges** added to the snapshot (1762 → 1770)
- **1 manifest** created (pass1214)
- **False positive analysis** at C3:4548: identified 88-byte data table with inflated cluster score (13)
- **Code fragment documentation** at C3:4200 demonstrating byte-coincidence detection
- **Closed ranges snapshot** maintained at 903 manifest-backed ranges

---

## 2. Pass 198 — C3:4000–C3:4800 Data Freeze

### Manifest: `passes/manifests/pass1214_c3_s35.json`

| Range | Classification | Confidence | Key Evidence |
|-------|---------------|------------|--------------|
| C3:4000..C3:40FF | data | high | 12 hard bad starts |
| C3:4100..C3:41FF | data | high | 2 hard bad starts |
| C3:4200..C3:42FF | data | high | Manual review rejected - fragmented |
| C3:4300..C3:43FF | data | high | 1 hard bad start |
| C3:4400..C3:44FF | data | high | Text/ASCII heavy, 1 hard bad start |
| C3:4500..C3:45FF | data | high | Cluster score 13 = data table (25 RTS coincidences) |
| C3:4600..C3:46FF | data | high | Mixed lane continue, no coherent functions |
| C3:4700..C3:47FF | data | high | 1 hard bad start |

---

## 3. Technical Analysis: False Positive Detection

### C3:4548 Data Table (Score 13 Analysis)

The scanner flagged C3:4548 with cluster score 13 - one of the highest in the region. However, analysis revealed this is **data, not code**:

| Metric | Value | Expected for Code |
|--------|-------|-------------------|
| Width | 88 bytes | 10-40 bytes typical |
| Returns | 25 | 1-3 typical |
| Calls | 0 | 2-10 typical |
| Branches | 5 | 8-20 typical |
| ASCII ratio | 0.398 | 0.2-0.3 typical |

**Conclusion**: The 25 "returns" are data bytes ($40 RTI, $60 RTS) that happen to match return opcodes. This is a data table, likely:
- Text/menu string table
- Jump pointer table  
- Game data/configuration values

### C3:4200 Fragment Analysis

The manual review page revealed classic byte-coincidence patterns:

```
C3:42C2: REP #$18       ; Valid 65816 instruction
C3:42C4: .db $00        ; BRK - data byte breaks flow
C3:42C5: STA $A801      ; Valid store
C3:42C8: PHP            ; Valid push
C3:42C9: .db $01        ; ORA operand - data breaks flow
```

**Pattern**: Valid opcode, data byte, valid opcode, data byte...

This fragmentation prevents promotion because:
1. No coherent execution flow
2. No clean function boundaries
3. Data bytes would cause crashes if executed

---

## 4. Methodology Validation

### Byte-Coincidence Detection Success
The seam scanner correctly identified suspicious patterns:
- `"rti_rts_proximity_at_20"` - Multiple return opcodes too close together
- `"repeated_pair_score"` - Detects structured data patterns

### Conservative Promotion Policy
No pages promoted because:
- All candidates have data bytes breaking flow
- Caller contexts are suspect or invalid
- Cluster scores inflated by byte coincidences
- ASCII ratios too high for executable code

---

## 5. Artifacts Produced

| Artifact | Path |
|----------|------|
| Pass 1214 manifest | `passes/manifests/pass1214_c3_s35.json` |
| Pass 198 disasm | `passes/disasm/pass198.md` (C3:4200 fragments) |
| Pass 199 disasm | `passes/disasm/pass199.md` (C3:4500 data table) |
| Pass 198 labels | `passes/labels/pass198.md` |
| Session summary | `AGENT_SWARM_SESSION_35_SUMMARY.md` |

---

## 6. Seam Block Analysis Summary

### Page Family Distribution
| Family | Count | Ranges |
|--------|-------|--------|
| candidate_code_lane | 3 | C3:4000, C3:4500, C3:4700 |
| mixed_command_data | 3 | C3:4200, C3:4300, C3:4600 |
| branch_fed_control_pocket | 1 | C3:4100 |
| text_ascii_heavy | 1 | C3:4400 |

### Review Posture Distribution
| Posture | Count | Ranges |
|---------|-------|--------|
| bad_start_or_dead_lane_reject | 6 | C3:4000-4100, C3:4300-4500, C3:4700 |
| manual_owner_boundary_review | 1 | C3:4200 (rejected after disassembly) |
| mixed_lane_continue | 1 | C3:4600 (frozen) |

---

## 7. Next Seam

Resume at **C3:4800**. This continues the low-bank forward seam.

Before proceeding:
1. Run seam block scanner at C3:4800 to identify promotion candidates
2. Check existing flow analysis for C3:4800-4FFF region
3. Verify no overlapping manifests exist for C3:4800+

---

## 8. Coverage Update

| Bank | Previous Ranges | New Ranges | Total |
|------|-----------------|------------|-------|
| C3 | 303 | +8 | 311 |
| **Total** | **960** | **+8** | **968** |

Bank C3 coverage: **~32.0%** → **~32.5%** (estimated)

---

## 9. Technical Notes

### Score Inflation Patterns
This session demonstrates common score inflation sources:

1. **Return opcodes in data**: $40 (RTI) and $60 (RTS) are common data values
2. **ASCII text**: Printable characters happen to match valid opcodes
3. **Structured tables**: Regular patterns resemble valid instruction sequences

### Corrective Measures Applied
- Manual disassembly confirmed data nature of high-score clusters
- Byte-coincidence analysis validated scanner rejections
- Conservative promotion policy maintained - no borderline promotions
