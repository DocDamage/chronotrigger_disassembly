# Pass 430: C0:F07F..C0:F097 (6 CALLERS - MAJOR)

**Label:** `ct_c0_f07f_6callers`

**Address:** $C0:F07F

**Verification:**
- Score: 5 (owner backtrack)
- Start byte: 20 (JSR - clean start)
- Target: C0:F07F
- Range: C0:F07F..C0:F097 (25 bytes)
- **Callers: 6** (C0:3D20, C0:5969, C0:3D0B, C0:4898, C0:5902, C0:5992)

**Evidence:**
- **HIGH CALLER TARGET** - 6 different callers across the codebase
- Clean instruction start (JSR - subroutine call)
- ASCII ratio: 0.44 (moderate)
- This is a widely-used utility function

**Confidence:** High (due to high caller count)

**Notes:**
This function is called from multiple locations throughout Bank C0, indicating it's a core utility function. The 6 callers make this one of the most significant discoveries in the C0:F000 region.
