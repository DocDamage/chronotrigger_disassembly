# Chrono Trigger Session 15 — Continuation Notes 80

## Block closed: C7:BC00..C7:C5FF (10 pages)

**MAJOR MILESTONE: Reached promoted C7:C300 region!**

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**, but **strongest candidate yet identified** (C7:C5AC, score 6).

---

## Connection to promoted C7:C300 ✅ CONFIRMED

This block successfully reached and includes the promoted C7:C300 region:

| Property | C7:C300 Page |
|----------|--------------|
| **Status** | Promoted (pass 192) |
| **Targets** | C7:C302 (called from C7:AEDE), C7:C3FA (called from C7:9258) |
| **Posture** | local_control_only |
| **Family** | candidate_code_lane |

**No direct calls** found between C000-C500 region and C300-C400, but both are in the same continuous analysis block.

---

## Strongest candidate yet: C7:C5AC (Score 6!)

### Analysis
| Property | Value |
|----------|-------|
| **Candidate** | C7:C5AC |
| **Target** | C7:C5B0 |
| **Score** | **6** (highest in C7 bank!) |
| **Distance** | 4 bytes |
| **Start byte** | **0xC2 (REP #$20)** - classic function prologue |

### ROM bytes at C7:C5AC:
```
C7:C5AC: C2 20       ; REP #$20     (Set 16-bit accumulator)
C7:C5AE: DE 13 EE    ; DEC $EE13,X  
C7:C5B1: EB          ; XBA
...
```

**Why this is exceptional:**
- **Score 6** - highest backtrack score in entire C7 bank analysis
- **Clean 65816 prologue**: `REP #$20` sets 16-bit mode (classic subroutine start)
- **Perfect alignment**: 4 bytes before target
- **Connected cluster**: C7:C59D-C7:C5B5 (score 4, 2 calls, 4 branches, 1 return)

**Status:** Frozen due to weak caller (C7:C275), but **strongest promotion candidate yet**.

---

## Other candidates in C000-C500

### C7:C000-C0FF (5 xref hits, 3 targets)
- Best candidate: C7:C0A4→C0B1 (score 4, start 0xA2 = LDX #)
- Mixed family - shows both code and data patterns
- Requires more analysis

### C7:C100-C1FF (4 xref hits)
- **BEST FINDING: Local clusters!**
  - C7:C193-C7:C1B2: score 7, 1 call, 5 branches, 2 returns
  - C7:C1B6-C7:C1CE: score 6, 3 calls, 2 branches, 1 return
- These clusters indicate **existing undiscovered code**

### C7:C200-C2FF - ORPHAN REGION
- **NO external anchors found**
- Code-like patterns but no strong validation
- Gap between C100 and C300

### C7:C400-C4FF
- Part of promoted C300-C4FF region ✓
- Cluster at C7:C4AA-C7:C4B3 (score 4)

---

## Can we promote C000-C500 as contiguous code?

**VERDICT: NOT YET**

**Blockers:**
| Region | Issue |
|--------|-------|
| C7:C000-C0FF | Mixed patterns, needs validation |
| C7:C100-C1FF | Clusters strong but anchors weak |
| **C7:C200-C2FF** | **ORPHAN** - no external anchors |
| C7:C300-C4FF | ✅ PROMOTED |
| C7:C500-C5FF | C5B0 strong but caller weak |

**The C200-C2FF orphan block** prevents contiguous promotion. It needs:
1. Adjacent region promotion (C5B0 or C100) to provide anchors
2. Or discovery of callers from other banks

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:BC00 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:BD00 | candidate_code_lane | local_control_only | freeze | local clusters |
| C7:BE00 | mixed_command_data | local_control_only | freeze | local clusters |
| C7:BF00 | branch_fed_control_pocket | local_control_only | freeze | local clusters |
| C7:C000 | mixed_command_data | manual_owner_boundary_review | freeze | 5 targets, mixed patterns |
| C7:C100 | candidate_code_lane | manual_owner_boundary_review | freeze | strong clusters, weak anchors |
| C7:C200 | candidate_code_lane | local_control_only | freeze | **orphan - no external anchors** |
| C7:C300 | candidate_code_lane | local_control_only | freeze | **PROMOTED region** ✓ |
| C7:C400 | candidate_code_lane | local_control_only | freeze | **PROMOTED region** ✓ |
| C7:C500 | candidate_code_lane | manual_owner_boundary_review | freeze | **C5B0 score-6 candidate** |

---

## Strategic analysis

### Current C7 code regions:
```
B000-B1FF  [PROMOTED pass 193]
  ↓ GAP: B200-C2FF (orphan block!)
C300-C4FF  [PROMOTED pass 192]
  ↓
C500-C5FF  [C5B0 candidate - strongest yet]
```

### Promotion pathway:
1. **C7:C5B0** (score 6) - promote to bridge to C500
2. Re-analyze C200-C2FF once C100/C500 connected
3. **C7:C100 clusters** (score 6-7) - strong internal evidence
4. Eventually: contiguous C000-C500 code region

### The C200-C2FF orphan problem
This region has:
- Code-like patterns (high entropy)
- No external xrefs (orphan)
- No direct connection to promoted regions

**Solution:** Promote adjacent regions (C100 or C500) first, then C200-C2FF gains anchor context.

---

## Running promotion count

- ... (passes 192-193) ...
- C7:B200..C7:B9FF: 0 promotions (notes_79) - bridge region
- **C7:BC00..C7:C5FF: 0 promotions (this note)** - but **strongest candidate yet** (C5AC score 6)

Total promotions: **2** (C7:B100, C7:C300)

**Next likely promotion:** C7:C5AC (score 6) - pending strong caller validation.

---

## Files generated

- `reports/c7_bc00_c5ff_seam_block.json`
- `reports/c7_bc00_c5ff_seam_block.md`
- `reports/c7_c000_c0ff_backtrack.json`
- `reports/c7_c100_c1ff_backtrack.json`
- `reports/c7_c500_c5ff_backtrack.json`
- `reports/C7_C0B1_anchor.json`
- `reports/C7_C5B0_anchor.json`

---

## New live seam: C7:C600..

Next block starts at **C7:C600**.

### Status
- ✅ Reached promoted C300 region
- ✅ Strongest candidate identified (C5AC, score 6)
- ⚠️ C200-C2FF orphan block needs resolution
- 🎯 Contiguous code potential: C000-C500

### Options:
1. **Continue linear** (C7:C600..) - extend coverage
2. **Promote C5AC now** - score 6 is compelling
3. **Analyze C200-C2FF** - solve orphan block

### Recommendation
**Continue linear** to C7:C600+ to:
- Extend code region beyond C500
- Find more anchors for C5B0
- Potentially validate C200-C2FF from other side

### Next steps
1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:C600 --pages 10 --json > reports/c7_c600_cfff_seam_block.json`
2. Continue extending C7 code region
3. Write `docs/sessions/chrono_trigger_session15_continue_notes_81.md`

**The C7 code region is expanding with the strongest candidate yet at C5AC!** 🚀
