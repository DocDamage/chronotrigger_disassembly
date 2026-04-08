======================================================================
BANK C1:8E00-9800 DISPATCH TABLE ANALYSIS REPORT
======================================================================

## 1. CALLER VALIDATION FOR C1:8C3E HUB
----------------------------------------------------------------------
Target: C1:8C3E
Total Callers Found: 42
Strong Anchors: 0
Weak Anchors: 42
Suspect Anchors: 0
Invalid: 0

All 42 callers are VALID JSR instructions
All 42 are WEAK anchors (callers in unresolved regions)

## 2. DISPATCH TABLE PATTERN ANALYSIS
----------------------------------------------------------------------
Spacing Pattern:
  - 65.9% of gaps are table-like (0x30-0x80 bytes)
  - Average gap: 58.4 bytes
  - Range: 10-121 bytes

Dispatch Type: CODE-BASED JUMP TABLE
  - 42 handler functions in C1:8E00-9800 range
  - Each handler calls C1:8C3E as a shared subroutine
  - Pattern: Handler -> JSR C1:8C3E -> RTS

## 3. SCORE-6+ CANDIDATES (BACKTRACK ANALYSIS)
----------------------------------------------------------------------

Found 3 score-6+ candidates:

  C1:8E9B -> C1:8EA6
    Score: 6, Distance: 11
    Start: 08 (clean_start)
    Range: C1:8E9B..C1:8EBE

  C1:8F02 -> C1:8F10
    Score: 6, Distance: 14
    Start: 20 (clean_start)
    Range: C1:8F02..C1:8F28

  C1:8FF4 -> C1:9003
    Score: 6, Distance: 15
    Start: 08 (clean_start)
    Range: C1:8FF4..C1:901B

## 4. HIGH-SCORE CLUSTERS (SEAM BLOCK ANALYSIS)
----------------------------------------------------------------------
Top clusters (score 6+):

  C1:8E95..C1:8EAA: score=8, width=22, calls=1, rts=2
  C1:9792..C1:97D4: score=8, width=67, calls=3, rts=3
  C1:906E..C1:9081: score=7, width=20, calls=1, rts=1
  C1:9032..C1:9044: score=7, width=19, calls=1, rts=1
  C1:96C2..C1:96D3: score=7, width=18, calls=1, rts=1
  C1:9745..C1:9764: score=7, width=32, calls=2, rts=2
  C1:9000..C1:9012: score=6, width=19, calls=1, rts=1
  C1:928A..C1:92A2: score=6, width=25, calls=1, rts=1
  C1:9301..C1:9313: score=6, width=19, calls=1, rts=1
  C1:937A..C1:938C: score=6, width=19, calls=1, rts=1
  C1:9639..C1:9655: score=6, width=29, calls=4, rts=2
  C1:968C..C1:96A4: score=6, width=25, calls=1, rts=1
  C1:8F6E..C1:8F86: score=5, width=25, calls=3, rts=1
  C1:8FC1..C1:8FD9: score=5, width=25, calls=3, rts=1
  C1:9117..C1:912F: score=5, width=25, calls=3, rts=1

## 5. RECOMMENDED NEW MANIFESTS (Pass 621+)
----------------------------------------------------------------------

### Priority 1: Score-6+ Functions (3 manifests)

  Pass 62X: C1:8E9B (score 6)
    Type: Function, Note: Handler dispatching to C1:8C3E

  Pass 62X: C1:8F02 (score 6)
    Type: Function, Note: Handler dispatching to C1:8C3E

  Pass 62X: C1:8FF4 (score 6)
    Type: Function, Note: Handler dispatching to C1:8C3E

### Priority 2: Score-4 Candidates (6 manifests)

  Pass 624: C1:8E41 (score 4)
  Pass 625: C1:8E6C (score 4)
  Pass 626: C1:8E77 (score 4)
  Pass 627: C1:9151 (score 4)
  Pass 628: C1:93A4 (score 4)

### Priority 3: High-Score Clusters (10+ manifests)

  Pass 630: C1:8E95..C1:8EAA (score 8) - Handler cluster
  Pass 631: C1:9792..C1:97D4 (score 8) - Large handler cluster
  Pass 632: C1:9032..C1:9044 (score 7) - Handler cluster
  Pass 633: C1:906E..C1:9081 (score 7) - Handler cluster
  Pass 634: C1:9745..C1:9764 (score 7) - Handler cluster
  Pass 635: C1:96C2..C1:96D3 (score 7) - Handler cluster

## 6. COVERAGE IMPACT
----------------------------------------------------------------------
Current Bank C1: 14 documented ranges (1.47%)
Estimated new ranges from this analysis: 15-20
Projected Bank C1 coverage: ~2.5-3%

## 7. STATE MACHINE IDENTIFICATION
----------------------------------------------------------------------
The C1:8C3E hub with 42 callers implements:
  - A STATE MACHINE DISPATCH PATTERN
  - 42 handler functions (C1:8E00-9800)
  - Central dispatch/handler at C1:8C3E
  - Likely handles game state, menu, or event processing

======================================================================
END OF REPORT
======================================================================