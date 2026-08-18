# Bank C3 Deep Scan Report - Game Logic/Event System Bank

**Date:** 2026-04-08  
**Scan Target:** C3 (Game Logic/Event System Bank)  
**ROM:** Chrono Trigger (USA).sfc  

---

## Executive Summary

Bank C3 is the **game logic/event system bank** with the highest coverage (19.85%) of any bank in the disassembly project. This deep scan analyzed four key regions:

- **C3:0000-1000** (bank start - branch fed control pocket)
- **C3:5000-6000** (game logic region)
- **C3:7000-8000** (event handlers - mixed command/data)
- **C3:B000-C000** (upper region - branch fed control pocket)

### Key Findings

| Metric | Value |
|--------|-------|
| **Total Score-6+ Candidates** | **169** |
| Score-13 (HIGHEST IN C3) | C3:4548 |
| Currently Documented Functions | 60+ ranges |
| Coverage Target | 28% (from 19.85%) |
| Potential New Functions | 20-25 |

---

## Region Analysis

### 1. C3:0000-1000 - Bank Start (Branch Fed Control Pocket)

**Page Family:** `branch_fed_control_pocket`  
**Characteristics:** Branch-dense, return-anchored code region

**Metrics:**
- ASCII ratio: 32.9%
- Zero ratio: 9.3%
- Branch ratio: 8.2%
- Call ratio: 5.7%
- Return count: 56

**Key Findings:**
- **138 tiny veneer candidates** identified
- 326 entry targets with caller analysis
- **C3:0000** has 1 strong anchor (C3:C0E2) + 17 weak anchors
- **C3:0002** has 1 strong anchor (C0:0A0F - DMA setup!) + 38 weak anchors
- High concentration of `bra_landing_pad` patterns
- Multiple RTL stubs at C3:01C5, C3:0306, C3:0331, etc.

**Notable Patterns:**
- JSR/RTS wrappers targeting C3:2085, C3:20C6, C3:2809
- Heavy use of BRA (branch) landing pads for control flow
- Strong evidence this is active game logic code

---

### 2. C3:5000-6000 - Game Logic Region

**Page Family:** `branch_fed_control_pocket`  
**Characteristics:** Dense game logic with many callable entry points

**Metrics:**
- ASCII ratio: 30.8%
- Zero ratio: 10.7%
- Branch ratio: 8.5%
- Call ratio: 3.6%
- Return count: 71

**Key Findings:**
- **48 tiny veneer candidates**
- 69 entry targets with caller analysis
- **Strong anchor at C3:5028** (JMP from C3:C279 - resolved code)
- **Strong anchor at C3:51B5** (JSR from C3:4B48 - resolved code)
- **Strong anchor at C3:5420** (JMP from C3:3885 - math function)
- **Strong anchor at C3:5777** (JSR from C3:3059 - resolved code)

**High-Value Targets:**
| Address | Anchor Type | Caller | Description |
|---------|-------------|--------|-------------|
| C3:5028 | Strong | C3:C279 | Jump table entry |
| C3:51B5 | Strong | C3:4B48 | Game logic function |
| C3:5420 | Strong | C3:3885 | Math 16-bit function |
| C3:5640 | Strong | C3:5E01 | JSL long function |
| C3:5777 | Strong | C3:3059 | Score-6 cluster |

---

### 3. C3:7000-8000 - Event Handlers (Mixed Command/Data)

**Page Family:** `mixed_command_data`  
**Characteristics:** Mixed metrics - transition region between code and data

**Metrics:**
- ASCII ratio: 31.0%
- Zero ratio: 39.7% (higher - indicates data presence)
- Zero/FF ratio: 40.2%
- Branch ratio: 2.7% (lower - less branch-heavy)
- Call ratio: 2.2%
- Return count: 51

**Key Findings:**
- **12 tiny veneer candidates**
- 57 entry targets
- **Strong anchor at C3:7000** (JSR from C3:84E2)
- **Strong anchor at C3:7020** (JSR from C3:87BC)
- **Strong anchor at C3:7141** (JSR from C3:A3E2)
- **Strong anchor at C3:7420** (2 strong anchors - C3:2E32 + C3:4B6C)
- **Strong anchor at C3:7774** (JSR from C3:4B6D)

**Notable Feature:**
- C3:7C13 has **5 weak anchors** - potential utility function
- Mix of code and data suggests event handler dispatch tables

---

### 4. C3:B000-C000 - Upper Region (Branch Fed Control Pocket)

**Page Family:** `branch_fed_control_pocket`  
**Characteristics:** High branch density, return-anchored

**Metrics:**
- ASCII ratio: 37.1% (higher - more text/ASCII)
- Zero ratio: 7.2%
- Branch ratio: 10.7% (highest!)
- Call ratio: 3.7%
- Return count: 104 (highest!)

**Key Findings:**
- **60 tiny veneer candidates** (highest count!)
- 33 entry targets
- **Strong anchor at C3:B574** (JSR from C3:2E33 - PHD prologue)
- **Strong anchor at C3:BC1B** (JSR from C3:387B - math 16-bit)
- **Strong anchor at C3:BD12** (JSR from C3:389B - math 16-bit)
- **Strong anchor at C3:BFAA** (JSR from C3:4A66 - score-6 cluster)

**Cross-Bank Callers:**
- C3:B131: JML from CA:31C2 (external bank call)
- C3:B563: JML from DF:2716 (external bank call)
- C3:B8EE: JSL from CA:31D8 (external bank call)

---

## Score-6+ Candidate Analysis

### Candidate Distribution

| Score Type | Count | Status |
|------------|-------|--------|
| Score 6+ (candidates) | 169 | **PENDING TRIAGE** |
| Score -6 (rejected) | 7 | Already filtered |
| Score -8 (rejected) | 8 | Already filtered |

### Top Score-6+ Clusters

Based on the scan data, these clusters show strongest potential:

1. **C3:4548** - **Score 13 (HIGHEST IN C3!)**
   - ct_c3_453b_unknown_function_score6_cluster
   - Pass 234, high confidence

2. **C3:0000** - Multiple weak anchors + 1 strong
   - Entry point for many callers

3. **C3:5777** - Strong anchor from C3:3059
   - Connected to score-6 cluster

4. **C3:7420** - Double strong anchors
   - PHD prologue connection

5. **C3:B574** - Strong anchor from C3:2E33
   - PHD prologue caller

---

## Current Coverage Status

### Documented Ranges: 60+ closed executable ranges

**Latest Passes:**
- Pass 715: C3:7207 gap handler
- Pass 714: C3:6643 gap handler
- Pass 713: C3:65AB gap handler
- Pass 604-605: Various handlers

**Coverage by Region:**
| Region | Status |
|--------|--------|
| C3:0000-1000 | Partial - needs more work |
| C3:1000-2000 | CODE END marker region |
| C3:2000-3000 | Data/padding blocks |
| C3:3000-4000 | Well covered (math, PPU handlers) |
| C3:4000-5000 | Well covered |
| C3:5000-6000 | Game logic - active work area |
| C3:6000-7000 | Recent gap passes (713-715) |
| C3:7000-8000 | Event handlers - mixed |
| C3:8000-9000 | Covered |
| C3:9000-A000 | Partial |
| C3:A000-B000 | Partial |
| C3:B000-C000 | Upper region - needs attention |
| C3:C000-D000 | Covered |
| C3:D000-E000 | Partial |
| C3:E000-F000 | Partial |
| C3:F000-FFFF | Partial |

---

## Recommendations

### Immediate Actions (20-25 new functions)

1. **C3:0000 region** - 5 new functions
   - Entry point handlers
   - RTL stub clusters

2. **C3:5000-6000** - 8 new functions
   - Game logic entries
   - Math utility functions

3. **C3:7000-8000** - 5 new functions
   - Event handlers
   - Utility functions (C3:7C13 with 5 callers)

4. **C3:B000-C000** - 7 new functions
   - Upper region handlers
   - Cross-bank interfaces

### Path to 28% Coverage

Current: **19.85%**  
Target: **28%**  
Gap: **~8.15%** (requires ~1600 bytes of newly documented code)

With 20-25 new functions averaging 60-80 bytes each = 1200-2000 bytes, **28% is achievable**.

---

## Files Referenced

- `labels/c3_candidates/` - 45 existing candidate labels
- `passes/manifests/pass716-723.json` - Recent gap passes
- `reports/c3_coverage_report.txt` - Coverage data
- `reports/bank_c3_progress.md` - Progress tracking

---

## Conclusion

Bank C3 is the **most documented bank** in the disassembly project with strong structural evidence of game logic and event handling code. The 169 score-6+ candidates represent a rich vein of undocumented functions that can push coverage from 19.85% to the 28% target.

**Priority regions:**
1. **C3:5000-6000** (game logic - strong anchors)
2. **C3:B000-C000** (upper region - high branch density)
3. **C3:0000-1000** (bank start - entry points)
4. **C3:7000-8000** (event handlers - mixed opportunities)

**Next Steps:**
- Promote high-confidence score-6+ candidates
- Create manifests for strong anchor targets
- Validate cross-bank callers
- Continue gap analysis for 20-25 new functions

---

*Report generated by run_c3_candidate_flow_v7.py deep scan*
