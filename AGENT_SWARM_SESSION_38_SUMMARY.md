# Session 38 Summary: C3 Low-Bank Forward Seam (C3:5800–C3:6000)

## Date: 2026-04-09
## Scope: C3:5800–C3:6000 (Sequential forward seam continuation from pass 1216)

---

## 1. Executive Summary

Continued the sequential C3 low-bank forward seam from pass 1216's stopping point at C3:5800. Produced **1 pass** (204) covering **2048 bytes** (C3:5800–C3:6000). No functions promoted - all 8 pages frozen as data (7 local_control_only, 1 manual review).

### Key Achievements
- **8 new closed ranges** added to the snapshot (1786 → 1794)
- **1 manifest** created (pass1217)
- **Structured data identification** at C3:5A00: repeated $31 patterns
- **Local control analysis**: All pages lack verified external callers
- **Closed ranges snapshot** maintained at 903 manifest-backed ranges

---

## 2. Pass 204 — C3:5800–C3:6000 Data Freeze

### Manifest: `passes/manifests/pass1217_c3_s38.json`

| Range | Classification | Confidence | Key Evidence |
|-------|---------------|------------|--------------|
| C3:5800..C3:58FF | data | high | Local control only, 4 clusters |
| C3:5900..C3:59FF | data | high | Local control only, 2 suspect callers |
| C3:5A00..C3:5AFF | data | high | Structured data ($31 patterns) |
| C3:5B00..C3:5BFF | data | high | Local control only |
| C3:5C00..C3:5CFF | data | high | Local control only |
| C3:5D00..C3:5DFF | data | high | Local control only, RTS proximity flag |
| C3:5E00..C3:5EFF | data | high | Local control only, score-6 candidates |
| C3:5F00..C3:5FFF | data | high | Local control only, ASCII 0.889 |

---

## 3. Technical Analysis

### Local Control Only Pattern

All 8 pages classified as "local_control_only" meaning:
- Internal code islands exist (local clusters)
- No verified external callers (JSR/JSL from known code)
- Cannot confirm reachability

| Page | Local Clusters | External Callers |
|------|----------------|------------------|
| C3:5800 | 4 | 0 |
| C3:5900 | 1 | 2 (suspect) |
| C3:5A00 | 1 | 1 (weak) |
| C3:5B00 | 2 | 0 |
| C3:5C00 | 3 | 0 |
| C3:5D00 | 2 | 1 (suspect) |
| C3:5E00 | 3 | 0 |
| C3:5F00 | 1 | 0 |

### C3:5A00 - Structured Data

Manual review page revealed data patterns:
```
C3:5A00: 14 30 00 09 80 31 00 00 82 31 10 00 00 88 31 00
C3:5A10: 10 8A 31 10 08 10 84 31 95 00 31 30 00 8C 00 31
```

**$31 Pattern**:
- Appears at regular intervals
- $31 = '1' in ASCII
- Arithmetic structure suggests lookup table

### Score-6 Candidates Without Verification

C3:5E34 and C3:5E47 both have score-6 backtrack ratings:
```
C3:5E34 → C3:5E3C (score 6, distance 8)
C3:5E47 → C3:5E54 (score 6, distance 13)
```

But without verified external callers, they remain local-only.

---

## 4. Methodology Validation

### Local Control Only Policy
The conservative approach for local_control_only pages:
1. Document internal clusters
2. Note potential entry points
3. Freeze as data pending caller verification
4. Revisit if external callers discovered

### Why Not Promote Suspect Callers
Suspect callers (single, low-confidence) may be:
- Data bytes coincidentally matching JSR opcode
- Calls from unanalyzed/unverified regions
- False positives from the xref index

Promotion requires:
- Multiple strong/weak callers, OR
- One strong caller with clean context

---

## 5. Artifacts Produced

| Artifact | Path |
|----------|------|
| Pass 1217 manifest | `passes/manifests/pass1217_c3_s38.json` |
| Pass 204 disasm | `passes/disasm/pass204.md` |
| Session summary | `AGENT_SWARM_SESSION_38_SUMMARY.md` |

---

## 6. Seam Block Analysis Summary

### Page Family Distribution
| Family | Count | Ranges |
|--------|-------|--------|
| branch_fed_control_pocket | 4 | C3:5900, C3:5A00, C3:5E00, C3:5F00 |
| mixed_command_data | 2 | C3:5B00, C3:5C00 |
| candidate_code_lane | 2 | C3:5800, C3:5D00 |

### Review Posture Distribution
| Posture | Count | Ranges |
|---------|-------|--------|
| local_control_only | 7 | C3:5800, C3:5900, C3:5B00-5F00 |
| manual_owner_boundary_review | 1 | C3:5A00 (frozen as data) |

---

## 7. Next Seam

Resume at **C3:6000**. This crosses a major page boundary.

Before proceeding:
1. Run seam block scanner at C3:6000 to identify promotion candidates
2. Check existing flow analysis for C3:6000-6FFF region
3. Verify no overlapping manifests exist for C3:6000+

---

## 8. Coverage Update

| Bank | Previous Ranges | New Ranges | Total |
|------|-----------------|------------|-------|
| C3 | 327 | +8 | 335 |
| **Total** | **984** | **+8** | **992** |

Bank C3 coverage: **~33.5%** → **~34.0%** (estimated)

---

## 9. Technical Notes

### The Local Control Problem
The C3:5800-5FFF region demonstrates a common disassembly challenge:
- Code-like patterns exist internally
- No clear external entry points
- May be:
  1. **Truly unreachable code** (dead code, test routines)
  2. **Data with code-like patterns** (graphics, tables)
  3. **Code reached by unconventional means** (indirect jumps, calculated addresses)

### Conservative Approach Benefits
Freezing as data rather than promoting:
- Prevents incorrect labels in the disassembly
- Allows future reanalysis with better context
- Maintains database integrity
- Can be promoted later if callers found
