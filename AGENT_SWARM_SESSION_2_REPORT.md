# Agent Swarm Session 2 Report

**Date:** 2026-04-08  
**Session:** Agent Swarm Parallel Analysis - Wave 2  
**New Passes:** 579-603 (25 manifests)  
**Agents Deployed:** 5 parallel workers

---

## Executive Summary

Second agent swarm session completed, adding **25 new confirmed code ranges** across **5 banks**. Key breakthroughs:
- **C5:4000-4FFF** deep scan validated as high-priority code region
- **C1 hub functions** confirmed with 25-29 callers each
- **C2 vector table** discovered at bank start
- **C3:5000-5FFF** identified as major unexplored code region

### Coverage Update

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total Passes | 578 | 603 | +25 |
| Total Ranges | 406 | 431 | +25 |
| Total Bytes | 27,611 | 29,003 | +1,392 |
| Project % | 7.02% | 7.38% | +0.36% |

---

## Agent 1: C5:4000-4FFF Deep Scan

### Mission
Comprehensive analysis of highest-priority bank C5 region.

### Results
- **51 total candidates** identified
- **2 score-6** and **2 score-5** confirmed
- **14 candidate_code_lane** pages
- Region confirmed as **active code territory**

### New Manifests (4)

| Pass | Range | Evidence |
|------|-------|----------|
| 579 | C5:4206..C5:4280 | Score-6, PHP prologue |
| 580 | C5:4FBD..C5:4FC4 | Score-6, return-anchored |
| 581 | C5:4805..C5:481D | Score-5, PHD prologue |
| 582 | C5:44D6..C5:44E1 | Score-5 island |

---

## Agent 2: C1 Hub Functions Deep Dive

### Mission
Validate and map around three major hub functions.

### Results
- **All three hubs validated**: 25, 29, and 27 callers respectively
- **Score-9 clusters** discovered near hubs
- **Satellite functions** mapped around each hub

### Key Discoveries

| Hub | Callers | Type |
|-----|---------|------|
| C1:179C | 25 | JMP-based dispatch |
| C1:1B55 | 29 | JSR-based subroutine |
| C1:4AEB | 27 | Core utility |

### New Manifests (6)

| Pass | Range | Score | Context |
|------|-------|-------|---------|
| 583 | C1:178E..C1:1800 | 6 | C1:179C entry |
| 584 | C1:1B55..C1:1B80 | 3* | Subroutine hub |
| 585 | C1:4A6B..C1:4B00 | 6 | C1:4AEB satellite |
| 586 | C1:1569..C1:159D | **9** | Highest in C1 |
| 587 | C1:1C3E..C1:1C66 | 8 | Post-hub region |
| 588 | C1:4CBD..C1:4CF7 | **9** | C1:4AEB neighborhood |

---

## Agent 3: C0:8400-8FFF Continuation

### Mission
Continue mapping Bank C0 utility code.

### Results
- **22 score-6+ candidates** identified
- **76 RTS returns** in region (high code density)
- **5 PHP prologues** found (proper stack frames)

### New Manifests (5)

| Pass | Range | Evidence |
|------|-------|----------|
| 589 | C0:8434..C0:845D | LDA# prologue |
| 590 | C0:8A92..C0:8AB6 | **PHP stack frame** |
| 591 | C0:84A2..C0:84BF | JSR helper |
| 592 | C0:851E..C0:853B | DMA function |
| 593 | C0:8703..C0:8741 | Complex utility |

---

## Agent 4: C2 Vector Table & B716 Cluster

### Mission
Analyze C2 initialization code and high-scoring cluster.

### Key Discovery: Vector Table
```
C2:0000 → C2:000F  (Reset/Init)
C2:0003 → C2:57DF  (Vector 1)
C2:0009 → C2:5823  (Vector 3)
```

### Results
- **Initialization code** at C2:000F with SNES standard prologue
- **11 new functions** identified
- **Cross-bank callers** from 15 banks to B700 region

### New Manifests (5)

| Pass | Range | Score | Note |
|------|-------|-------|------|
| 594 | C2:032C..C2:0350 | **8** | Vector region |
| 595 | C2:000F..C2:0050 | - | **Init entry point** |
| 596 | C2:B7B3..C2:B7CB | 6 | Adjacent to B716 |
| 597 | C2:0465..C2:0477 | 6 | Vector region |
| 598 | C2:8249..C2:82D5 | 6 | 8000 region |

---

## Agent 5: C3 Gap Fill

### Mission
Continue filling C3 gaps, especially 0000-01E3 and 5000-5FFF.

### Major Discovery
**C3:5000-5FFF is a substantial code region** with:
- 551+ RTS returns
- Multiple function clusters
- Previously completely unexplored

### New Manifests (5)

| Pass | Range | Evidence |
|------|-------|----------|
| 599 | C3:01A8..C3:01C9 | JSR prologue (gap 0000-01E3) |
| 600 | C3:01B4..C3:01E3 | PHP prologue (gap 0000-01E3) |
| 601 | C3:052A..C3:054B | JSR entry (gap 0529-08A0) |
| 602 | C3:5131..C3:5158 | PHD prologue (gap 5000-5FFF) |
| 603 | C3:5E01..C3:5E74 | JSL long function (gap 5000-5FFF) |

---

## New Manifest Summary (Passes 579-603)

### By Confidence
- **High (16)**: Passes 579-580, 583, 586-588, 594-596, 599-603
- **Medium (9)**: Passes 581-582, 584-585, 591-593, 597-598

### By Bank

| Bank | Passes | Functions | Coverage Gain |
|------|--------|-----------|---------------|
| C5 | 579-582 | 4 | 0.55% → 0.80% |
| C1 | 583-588 | 6 | 0.59% → 1.29% |
| C0 | 589-593 | 5 | 17.70% → 18.01% |
| C2 | 594-598 | 5 | 0.42% → 0.85% |
| C3 | 599-603 | 5 | 20.70% → 21.11% |

---

## Technical Notes

### Highest Scores Found
- **C1:1569**: Score-9, width 52 (C1:179C caller region)
- **C1:4CBD**: Score-9, width 58 (C1:4AEB neighborhood)
- **C2:032C**: Score-8 (vector region)
- **C1:1C3E**: Score-8, width 40 (post-C1:1B55)

### Prologue Distribution
- **PHP (08)**: 8 candidates (stack frame setup)
- **JSR (20)**: 6 candidates (subroutine entry)
- **LDA# (A9)**: 4 candidates (register init)
- **PHD (0B)**: 3 candidates (direct page push)
- **JSL (22)**: 2 candidates (long calls)

---

## Next Steps

### Immediate Priority
1. **Deep scan C5:4400-4F00** - Continue high-density region
2. **Explore C1:8000-9000** - Rich code region with 6+ candidates
3. **Map C3:5000-5FFF** - Major newly-discovered code region

### Short-term
1. Continue C0:9000-9FFF mapping
2. Explore C2:B700-B800 cross-bank hub
3. Fill remaining C3 gaps

### Medium-term
1. Complete C1 systematic mapping
2. Complete C5 systematic mapping
3. Begin C4 exploration

---

## Files Changed

- `passes/manifests/pass579.json` through `pass603.json` (25 new manifests)
- `AGENT_SWARM_SESSION_2_REPORT.md` (this file)
- `README.md` (updated coverage stats)

---

*End of Agent Swarm Session 2 Report*
