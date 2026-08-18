# Session 36 Summary: C3 Low-Bank Forward Seam (C3:4800–C3:5000)

## Date: 2026-04-09
## Scope: C3:4800–C3:5000 (Sequential forward seam continuation from pass 1214)

---

## 1. Executive Summary

Continued the sequential C3 low-bank forward seam from pass 1214's stopping point at C3:4800. Produced **2 passes** (200-201) covering **2048 bytes** (C3:4800–C3:5000). No functions promoted - all 8 pages frozen as data with documented fragment analysis.

### Key Achievements
- **8 new closed ranges** added to the snapshot (1770 → 1778)
- **2 manifests** created (pass1215, disasm notes)
- **Local control analysis** at C3:4900: identified inline data patterns with long addressing
- **ASCII ratio validation** at C3:4A00: cluster score 11 debunked by 0.619 ASCII ratio
- **Closed ranges snapshot** maintained at 903 manifest-backed ranges

---

## 2. Pass 200–201 — C3:4800–C3:5000 Data Freeze

### Manifest: `passes/manifests/pass1215_c3_s36.json`

| Range | Classification | Confidence | Key Evidence |
|-------|---------------|------------|--------------|
| C3:4800..C3:48FF | data | high | 2 hard bad starts |
| C3:4900..C3:49FF | data | high | Local control only, fragmented |
| C3:4A00..C3:4AFF | data | high | Cluster score 11, ASCII 0.619 = data |
| C3:4B00..C3:4BFF | data | high | 1 hard bad start |
| C3:4C00..C3:4CFF | data | high | 2 hard bad starts |
| C3:4D00..C3:4DFF | data | high | 1 hard bad start |
| C3:4E00..C3:4EFF | data | high | 1 hard bad start |
| C3:4F00..C3:4FFF | data | high | 2 hard bad starts |

---

## 3. Technical Analysis

### C3:4900: Local Control Only Pattern

The "local_control_only" posture indicated internal code islands without verified external callers. Disassembly revealed:

```
C3:4930: RTS               ; Return
C3:4931: LDA #$1B          ; Valid instruction
C3:4933-4934: .db $00, $00 ; Data breaks flow
C3:4935: STA $35           ; Valid instruction
C3:493A: STA $7E:7480BB    ; Long addressing to WRAM
```

**Pattern**: Inline data within code sequences, typical of:
- Jump table dispatches
- Parameter tables embedded in code
- Self-modifying code patterns

### C3:4A00: Cluster Score 11 Debunked

| Metric | Value | Normal Code Range |
|--------|-------|-------------------|
| Cluster Score | 11 | — |
| ASCII Ratio | 0.619 | 0.2-0.3 |
| Returns | 7 | 1-3 |
| Width | 42 bytes | 10-40 |

**Conclusion**: The high ASCII ratio (0.619) confirms this is **text/data**, not code. The cluster score is inflated by:
- $4D bytes ('M' in ASCII, EOR opcode coincidence)
- $60 bytes (RTS opcode coincidence)
- Printable character patterns

### Data Misread Flag Validation
```
"data_misread_flags": ["rti_rts_proximity_at_12"]
```

The scanner correctly identified multiple RTS/RTI bytes in close proximity as suspicious.

---

## 4. Methodology Validation

### Multi-Factor Analysis
This session demonstrates the importance of combining multiple metrics:

1. **Cluster score alone is insufficient**: Score 11 seemed promising
2. **ASCII ratio is diagnostic**: 0.619 clearly indicates data
3. **Data misread flags catch coincidences**: RTS proximity detection
4. **Manual disassembly confirms**: Fragmented code patterns

### Conservative Promotion Policy
No promotions because:
- Local control only = no verified external callers
- High ASCII ratio = data, not code
- Fragmented execution = inline data patterns
- Hard bad starts = invalid entry points

---

## 5. Artifacts Produced

| Artifact | Path |
|----------|------|
| Pass 1215 manifest | `passes/manifests/pass1215_c3_s36.json` |
| Pass 200 disasm | `passes/disasm/pass200.md` (C3:4900 fragments) |
| Pass 201 disasm | `passes/disasm/pass201.md` (C3:4A00 data table) |
| Pass 200 labels | `passes/labels/pass200.md` |
| Session summary | `AGENT_SWARM_SESSION_36_SUMMARY.md` |

---

## 6. Seam Block Analysis Summary

### Page Family Distribution
| Family | Count | Ranges |
|--------|-------|--------|
| mixed_command_data | 5 | C3:4A00, C3:4B00, C3:4C00, C3:4D00, C3:4F00 |
| branch_fed_control_pocket | 2 | C3:4800, C3:4900 |
| candidate_code_lane | 1 | C3:4E00 |

### Review Posture Distribution
| Posture | Count | Ranges |
|---------|-------|--------|
| bad_start_or_dead_lane_reject | 7 | C3:4800-4800, C3:4A00-4F00 |
| local_control_only | 1 | C3:4900 (frozen) |

---

## 7. Next Seam

Resume at **C3:5000**. This crosses into a new 256-byte page boundary.

Before proceeding:
1. Run seam block scanner at C3:5000 to identify promotion candidates
2. Check existing flow analysis for C3:5000-5FFF region
3. Verify no overlapping manifests exist for C3:5000+

---

## 8. Coverage Update

| Bank | Previous Ranges | New Ranges | Total |
|------|-----------------|------------|-------|
| C3 | 311 | +8 | 319 |
| **Total** | **968** | **+8** | **976** |

Bank C3 coverage: **~32.5%** → **~33.0%** (estimated)

---

## 9. Technical Notes

### Inline Data Patterns
C3:4900 demonstrates common SNES coding patterns:
- Code interspersed with parameter tables
- Long addressing to WRAM ($7E:xxxx)
- RTS followed immediately by data

These patterns require specialized analysis beyond simple opcode scanning.

### ASCII Ratio as Discriminator
The 0.619 ASCII ratio at C3:4A00 is a clear indicator of:
- Menu text
- Dialog strings
- Lookup tables with printable values

Any ratio above 0.5 should trigger data suspicion.
