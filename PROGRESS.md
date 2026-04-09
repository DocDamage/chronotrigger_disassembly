# Chrono Trigger Disassembly Progress Report

**Last Updated**: 2026-04-09 (Session 41 Complete)  
**Working Branch**: `live-work-from-pass166`  
**Latest Manifest Pass**: 1224 (Session 42: C4:714E promotion)

---

## Executive Summary

The Chrono Trigger SNES ROM disassembly project has reached significant milestones:

- **1,836 closed ranges** documented (917 manifest-backed + 919 continuation)
- **42 Agent Swarm Sessions** completed
- **Bank C0**: 31.90% coverage (30% target exceeded)
- **Bank C3**: ~35.8% coverage (30% target exceeded)
- **Bank C4**: ~12.8% coverage (approaching 15% target)
- **12 functions promoted** in latest Session 40 (C3:7000 breakthrough)

---

## Coverage by Bank

| Bank | Ranges | Coverage | Status | Notes |
|------|--------|----------|--------|-------|
| C0 | 308 | 31.90% | ✅ Target Exceeded | Audio/HDMA systems complete |
| C1 | 89 | 7.60% | In Progress | 434A mega-cluster mapped |
| C2 | 75 | 8.00% | ✅ Target Achieved | Score-14 functions discovered |
| C3 | 356 | ~35.9% | ✅ Target Exceeded | +1 function in Session 41 |
| C4 | 155 | ~12.9% | In Progress | C4:714E promoted, path to 15% |
| C5 | 28 | 4.10% | In Progress | Score-9 cluster at 9BC1 |
| C6 | 15 | 0.50% | Initial | D400-D800 mapped |
| C7 | 23 | 2.16% | In Progress | 95% mapped |
| CF | 43 | 2.14% | In Progress | D000-FFFF complete |
| D1 | 24 | 2.05% | Discovered | 505 islands found |
| D2-D9 | 8 | 0.04% each | Discovered | All code banks identified |
| **Total** | **1,835** | **~14.5%** | **Active** | **971+ manifests** |

---

## Recent Major Achievements

### Session 42: High Bank + C4 Deep Scan (2026-04-09)
Continued high bank exploration and C4 bank deep scan:
- **24 pages scanned** (C3:9800-A7FF, C4:7000-77FF)
- **1 function promoted**: C4:714E (score-6, 32-bit arithmetic helper)
- **C4 bank progress**: 11 candidate pages found, path to 15% clearer
- **High bank continues**: 6 branch_fed_control_pocket pages at C3:A000+
- **Current seam**: C3:A800.. / C4:7800..

### Session 41: Sequential Seam + High Bank Pivot (2026-04-09)
Continued disassembly with focus on C3:7800+ and high bank exploration:
- **32 pages scanned** across C3:7800-97FF and C4:6800-6FFF
- **1 function promoted**: C3:8912 (score-6, ASCII 0.175)
- **High bank validation**: C3:8000+ confirms 62.5% code density
- **Cluster score 8**: C3:87BA-87E1 (branch_fed_control_pocket)
- **4 RTL stubs** detected at C3:8900
- **Current seam**: C3:9800..

### Session 40: Agent Swarm Multi-Region Scan (2026-04-09)
**4 parallel agents** scanned **4 regions simultaneously**:

#### Agent 1: C3:6800-6FFF
- No promotions (all data)
- 3 score-6 candidates examined and rejected

#### Agent 2: C3:7000-77FF ⭐ BREAKTHROUGH
- **12 functions promoted**
- Score-6 star candidate at **C3:7207**
- **Cross-bank call**: FC:BA5A → C3:76C3
- ~416 bytes verified code (+1.3% C3 coverage)

#### Agent 3: C3:8000-87FF
- **High bank shows 62.5% candidate_code_lane** (vs low bank)
- 5+ score-6 candidates identified
- Complex branch tables discovered
- **Recommendation**: Prioritize C3:8800-9FFF

#### Agent 4: C4 Bank Scan
- **8 score-6+ candidates** found
- Strong verified callers in C4:6000 region
- Path to 15% coverage: 3-4 more sessions

### Session 39: C3:6000-6800 Analysis
- Fragmented code patterns at C3:6600
- Cross-bank JSL $C30D5E identified
- 16-bit mode detection (LDA #$003C)
- Milestone: **1,000 total closed ranges reached**

### Sessions 33-38: C3 Low-Bank Forward Seam
- Sequential scanning C3:3000-6000
- Jump table identification (C3:5777 = JMP $A22A)
- Data table analysis (arithmetic progression +$21)
- ASCII ratio validation debunking false positives

---

## Key Technical Discoveries

### 1. High Bank vs Low Bank Code Density
| Region | Candidate Code Lane % | Finding |
|--------|----------------------|---------|
| C3:0000-7FFF (Low) | ~30% | Mixed code/data |
| C3:8000+ (High) | **62.5%** | **Much higher density** |

**Implication**: High banks (8000-FFFF) contain significantly more executable code.

### 2. Cross-Bank Call Patterns
- FC:BA5A → C3:76C3 (Session 40)
- E5:8EA7 → C3:8207 (Session 40)
- EC:3F40 → C3:8207 (Session 40)
- C4:807E → C4:6005 (Session 40)

### 3. 65816 Native Mode Usage
- 16-bit immediate values: `LDA #$003C` (LDA #$3C + .db $00)
- REP #$20 / SEP #$20 mode switching
- Cross-bank JSL/JML instructions

### 4. Jump Table Patterns
- C3:5777: `JMP $A22A` (dispatch entry, not function)
- C3:800C: 8 weak callers (high importance entry)
- Trampoline pattern for bank switching

---

## File Inventory

### Manifests (passes/manifests/)
- **970+ total manifests**
- Latest: `pass1222_c4_scan.json`
- Session 40: pass1219, pass1220, pass1221, pass1222

### Disassembly Notes (passes/disasm/)
- pass205.md - C3:6600 fragments
- pass206.md - C3:6800 analysis
- pass207.md - C3:7000 breakthrough
- pass208.md - C3:8000 high bank

### Session Reports
- `AGENT_SWARM_SESSION_40_MASTER_SUMMARY.md`
- `C3_7000_REGION_REPORT.md`
- `C3_8000_HIGH_BANK_REPORT.md`
- `C4_BANK_PROGRESS_REPORT.md`

---

## Path to Targets

### Bank C3: 35% Target
- **Current**: ~35.8% ✅
- **Status**: Target achieved!
- **Next**: Continue high bank scanning (C3:8800+)

### Bank C4: 15% Target
- **Current**: ~12.8%
- **Gap**: ~2.2%
- **Path**: 
  1. Promote 8 Session 40 candidates (+0.6%)
  2. Scan C4:6800-6FFF (continuation)
  3. Scan C4:4000-4FFF (dense region)
- **ETA**: 3-4 sessions

### Bank C1: 10% Target
- **Current**: 7.6%
- **Gap**: 2.4%
- **Focus**: 434A mega-cluster (score-17)

---

## Recommended Next Steps

### Immediate Priority (Next Session)
1. **Scan C3:8800-8FFF** - High bank code density
2. **Promote C3:7000 functions** - 12 verified candidates
3. **Scan C4:6800-6FFF** - Continue 6000-region

### Short Term (Next 3-4 Sessions)
1. Complete C4:15% target
2. Continue C3 high bank exploration
3. Process C1 434A mega-cluster

### Medium Term
1. Deep scan C2 score-14 region
2. Expand D1, D4, D6 banks
3. Map CF:C000-D000 region

---

## Toolkit Status

All tools operational:
- `run_seam_block_v1.py` - Primary seam scanner
- `ensure_seam_cache_v1.py` - Cache management
- `score_target_owner_backtrack_v1.py` - Candidate scoring
- `toolkit_doctor.py` - Health checks (8/8 passing)

**Scripts**: 102 Python scripts compile successfully

---

## Statistics

| Metric | Value |
|--------|-------|
| Total Closed Ranges | 1,834 |
| Manifest-Backed | 915 |
| Continuation | 919 |
| Total Manifests | 970+ |
| Sessions Completed | 40 |
| Parallel Agents | 4 (Session 40) |
| Functions Promoted (Latest) | 12 |
| Cross-Bank Calls Identified | 20+ |

---

## Documentation Links

- Main: `README.md`
- Session 40: `AGENT_SWARM_SESSION_40_MASTER_SUMMARY.md`
- C3:7000: `C3_7000_REGION_REPORT.md`
- C3:8000: `C3_8000_HIGH_BANK_REPORT.md`
- C4 Bank: `C4_BANK_PROGRESS_REPORT.md`
- This File: `PROGRESS.md`
