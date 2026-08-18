# Chrono Trigger Disassembly Progress Report

**Last Updated**: 2026-04-09 (Session 46 Complete)
**Working Branch**: `live-work-from-pass166`
**Latest Manifest Pass**: 1229 (Session 46: C4:9D10 + C3:CB47 dual promotion)

---

## Executive Summary

The canonical repository state is reconstructed from the complete historical manifest archive:

- **1,105 historical closed-range claims** conserved across 961 canonical manifests
- **1,289 canonical records** after ownership normalization (1,061 active, 228 superseded provenance records)
- **0 unresolved active ownership conflicts**; superseded claims remain preserved as provenance
- **1,000/1,000 source manifests** represented in the migration ledger
- **106 absent pass numbers** factually accounted as having no baseline manifest
- **46 Agent Swarm Sessions** completed
- **59,050 unique bytes** covered after active-interval union (1.4079% of the 4 MiB ROM)
- **Current frontier**: `C3:D000.. / C4:A000..`

---

## Coverage by Bank

These are canonical active-interval metrics from `reports/coverage.json`; older session sections below retain their historical snapshots.

| Bank | Disjoint Intervals | Covered Bytes | Bank Coverage |
|------|-------------------:|--------------:|--------------:|
| C0 | 292 | 16,075 | 24.53% |
| C1 | 45 | 1,661 | 2.53% |
| C2 | 10 | 883 | 1.35% |
| C3 | 56 | 29,665 | 45.27% |
| C4 | 48 | 1,393 | 2.13% |
| C5 | 20 | 1,505 | 2.30% |
| C6 | 14 | 317 | 0.48% |
| C7 | 23 | 1,416 | 2.16% |
| CF | 45 | 1,623 | 2.48% |
| D1 | 18 | 933 | 1.42% |
| D2–DF | 112 | 3,579 | — |
| **ROM total** | **683** | **59,050** | **1.4079%** |

---

## Recent Major Achievements

### Session 46: Major Breakthrough - C4:9800 Exceptional Density (2026-04-09)
Scanned C3:C800-CFFF and C4:9800-9FFF with major C4 discovery:
- **16 pages scanned** (C3:C800-CFFF, C4:9800-9FFF)
- **2 functions promoted**: C4:9D10 (3-byte copy) + C3:CB47 (hardware init)
- **C4:9800-9FFF**: 7 of 8 pages are candidate_code_lane (exceptional!)
- **Score-6 clusters**: 3 discovered (C3:CB8E, C4:9DE6, C4:9E50)
- **Session-ending seam**: C3:D000.. / C4:A000..

### Session 45: Continuation Scan - Pending Candidates (2026-04-09)
Scanned C3:B800-C7FF and C4:8800-97FF, documented pending candidates:
- **24 pages scanned** (C3:B800-C7FF, C4:8800-97FF)
- **No promotions**: 4 score-4 candidates pending verification
- **Cross-bank caller**: CA:31D8 → C3:B8EE (external bank)
- **C4:8A00**: 5 entry callers, 2 local clusters
- **Session-ending seam**: C3:C800.. / C4:9800..

### Session 44: Dual Promotion Breakthrough - C3:B000 (2026-04-09)
Scanned C3:B000-B7FF and C4:8000-87FF with exceptional C3 results:
- **16 pages scanned** (C3:B000-B7FF, C4:8000-87FF)
- **2 functions promoted**: C3:B002 (hardware clear) + C3:B086 (range validation)
- **C3 bank**: ~36.0% coverage (target exceeded)
- **C4 bank**: ~13.0%, 6 candidate_code_lane pages found
- **Session-ending seam**: C3:B800.. / C4:8800..

### Session 43: C4 Bank Push to 15% (2026-04-09)
Focused on C4:7800-7FFF to push toward 15% coverage target:
- **16 pages scanned** (C3:A800-AFFF, C4:7800-7FFF)
- **1 function promoted**: C4:7FAC (score-6, clamped value update routine)
- **Major discovery**: C4:7F00 page has 7 verified entry callers
- **C4 bank**: ~13.0% coverage, 2.0% to 15% target
- **Session-ending seam**: C3:B000.. / C4:8000..

### Session 42: High Bank + C4 Deep Scan (2026-04-09)
Continued high bank exploration and C4 bank deep scan:
- **24 pages scanned** (C3:9800-A7FF, C4:7000-77FF)
- **1 function promoted**: C4:714E (score-6, 32-bit arithmetic helper)
- **C4 bank progress**: 11 candidate pages found, path to 15% clearer
- **High bank continues**: 6 branch_fed_control_pocket pages at C3:A000+
- **Session-ending seam**: C3:A800.. / C4:7800..

### Session 41: Sequential Seam + High Bank Pivot (2026-04-09)
Continued disassembly with focus on C3:7800+ and high bank exploration:
- **32 pages scanned** across C3:7800-97FF and C4:6800-6FFF
- **1 function promoted**: C3:8912 (score-6, ASCII 0.175)
- **High bank validation**: C3:8000+ confirms 62.5% code density
- **Cluster score 8**: C3:87BA-87E1 (branch_fed_control_pocket)
- **4 RTL stubs** detected at C3:8900
- **Session-ending seam**: C3:9800..

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
- **961 canonical manifests** generated reproducibly from 1,000 archived sources
- Latest canonical manifest: `pass1229.json`
- The range-less `pass1222_c4_scan.json` source is retained in `legacy/` and represented in the migration ledger

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
- **Path**: pending next-session selection
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
