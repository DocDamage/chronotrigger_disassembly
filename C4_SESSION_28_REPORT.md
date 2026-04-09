
================================================================================
BANK C4 - SESSION 28 DISASSEMBLY REPORT
================================================================================

EXECUTIVE SUMMARY
--------------------------------------------------------------------------------
Session: 28
Bank: C4
Target Coverage: 10%

MANIFESTS CREATED
--------------------------------------------------------------------------------
Total Manifests: 40
Total Bytes Documented: 995
Coverage Increase: +1.52%

Previous Coverage: ~8.05%
New Coverage: ~9.57%

COVERAGE BY REGION
--------------------------------------------------------------------------------
  C4:4000-8000         |  14 manifests |  260 bytes
  C4:9000-FFFF         |  26 manifests |  735 bytes

COVERAGE BY SCORE
--------------------------------------------------------------------------------
  Score 7  |   3 manifests |   71 bytes
  Score 6  |  29 manifests |  780 bytes
  Score 5  |   8 manifests |  144 bytes

TOP 15 MANIFESTS (BY SIZE)
--------------------------------------------------------------------------------
   1. pass0712 | C4:FF0F..C4:FF36 |  39 bytes | Score 6 | PHP prologue, extended
   2. pass0713 | C4:E0EC..C4:E110 |  36 bytes | Score 6 | LDY# prologue, extended
   3. pass0714 | C4:B3B1..C4:B3D4 |  35 bytes | Score 6 | JSR prologue, caller from C4:0
   4. pass0715 | C4:F9FA..C4:FA1D |  35 bytes | Score 6 | LDX# prologue, extended
   5. pass0716 | C4:FA07..C4:FA28 |  33 bytes | Score 6 | JSL prologue, long subroutine
   6. pass0717 | C4:FDB9..C4:FDD8 |  31 bytes | Score 6 | LDX# prologue
   7. pass0718 | C4:F9FA..C4:FA18 |  30 bytes | Score 6 | LDX# prologue, register init
   8. pass0719 | C4:FE2F..C4:FE4D |  30 bytes | Score 6 | JSR prologue, extended
   9. pass0720 | C4:FF0F..C4:FF2D |  30 bytes | Score 6 | PHP prologue
  10. pass0721 | C4:E0EC..C4:E108 |  28 bytes | Score 6 | LDY# prologue, multiple caller
  11. pass0722 | C4:E35E..C4:E37A |  28 bytes | Score 6 | PHP prologue, clear pattern
  12. pass0723 | C4:C0DF..C4:C0FA |  27 bytes | Score 6 | PHP prologue, extended
  13. pass0724 | C4:FDFE..C4:FE19 |  27 bytes | Score 6 | PHP prologue
  14. pass0725 | C4:9D10..C4:9D2A |  26 bytes | Score 6 | LDY# prologue, cluster at C4:9
  15. pass0726 | C4:B8B1..C4:B8CB |  26 bytes | Score 6 | PHP prologue, stack operation

HIGH-VALUE TARGETS IDENTIFIED
--------------------------------------------------------------------------------

Score 7+ (Highest Confidence):
  - C4:7730..C4:7748 (25 bytes) - score-7 cluster
  - C4:7732..C4:774A (25 bytes) - score-7 cluster
  - C4:5025..C4:5039 (21 bytes) - score-7 cluster

Call-Heavy Functions (2+ calls):
  - C4:5025..C4:5039 (21 bytes) - 2 calls
  - C4:752A..C4:753C (19 bytes) - 3 calls
  - C4:7980..C4:7992 (19 bytes) - 3 calls

Branch-Heavy Handlers (3+ branches):
  - C4:7730..C4:7748 (25 bytes) - 6 branches
  - C4:7732..C4:774A (25 bytes) - 5 branches
  - C4:46B7..C4:46CF (25 bytes) - 3 branches
  - C4:7F8F..C4:7FA7 (25 bytes) - 6 branches
  - C4:772E..C4:7742 (21 bytes) - 4 branches
  - C4:7980..C4:7992 (19 bytes) - 4 branches
  - C4:772E..C4:7740 (19 bytes) - 3 branches

FILES CREATED
--------------------------------------------------------------------------------
  - passes/pass0709.json through pass0748.json (40 manifests)
  - c4_session28_manifests.json (combined manifest list)
  - analyze_c4_session28_full.py (analysis script)
  - validate_session28.py (validation script)

NEXT STEPS
--------------------------------------------------------------------------------
1. Apply manifests to disassembly database
2. Verify no conflicts with existing labels
3. Continue analysis of remaining gaps:
   - C4:0000-1000 (remaining gaps)
   - C4:1000-4000
   - C4:8000-9000
   - C4:D000-E000 (mixed region)

================================================================================
END OF REPORT
================================================================================
