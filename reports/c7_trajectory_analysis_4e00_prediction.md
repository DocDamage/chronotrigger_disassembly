# C7 Bank Trajectory Analysis — C7:4E00..57FF Prediction

## Executive Summary

Based on analysis of the last 3 continuation notes (64, 65, 66) covering C7:3000..4DFF, C7 bank shows a **clear and accelerating progression from code → mixed → data**. The next block (C7:4E00..57FF) is expected to be predominantly data-heavy with minimal viable code candidates.

---

## Historical Trajectory (Last 3 Blocks)

### Block 64: C7:3000..39FF (notes_64)
- **Manual review rate**: 20% (2 of 10 pages)
- **Page families**: 50% mixed_command_data, 30% candidate_code_lane, 20% branch_fed_control_pocket
- **Character**: Still showing code-candidate activity with 2 pages in `manual_owner_boundary_review`
- **Key signal**: Mixed content with some candidate lanes, but all rejected on byte review

### Block 65: C7:3A00..43FF (notes_65)
- **Manual review rate**: 70% (7 of 10 pages) — **peak activity**
- **Page families**: 50% mixed_command_data, 40% branch_fed_control_pocket, **10% dead_zero_field**
- **Character**: High manual review rate, but zero promotions
- **Key signal**: First `dead_zero_field` appears (C7:4300) — the canary in the coal mine
- **Strongest near-miss**: C7:4100 with 6 callers to 418D, but all suspect from data regions

### Block 66: C7:4400..4DFF (notes_66)
- **Manual review rate**: 10% (1 of 10 pages) — **dramatic drop**
- **Page families**: 70% mixed_command_data, **30% text_ascii_heavy** (NEW)
- **Character**: Data-heavy, first text/ASCII region
- **Key signal**: Three consecutive `text_ascii_heavy` pages (4400, 4500, 4600)
- **Strongest reject**: C7:4600 with hard_bad_start at 46C8 (zero-filled padding)

---

## Trajectory Analysis Questions

### 1. Is C7 bank showing a clear progression from code → mixed → data?

**YES — unmistakably.**

| Block | Code-Heavy | Mixed | Data-Heavy | Signal |
|-------|-----------|-------|------------|--------|
| C7:3000..39FF | 50% candidate_code_lane | 50% mixed | 0% | Code-dominant |
| C7:3A00..43FF | 40% branch_fed | 50% mixed | 10% dead_zero | Transitioning |
| C7:4400..4DFF | 0% | 70% mixed | 30% text_ascii | Data-dominant |

The progression is clear:
- **candidate_code_lane** → **branch_fed_control_pocket** → **mixed_command_data** → **text_ascii_heavy**
- Manual review rate: 20% → 70% → 10% (collapsed when data took over)
- Target density: declining steadily (multiple targets per page → 0-1 targets per page)

### 2. What would we expect at C7:4E00+ if the data-heavy trend continues?

**Expect primarily data regions with these characteristics:**

| Expected Page Family | Probability | Description |
|---------------------|-------------|-------------|
| `text_ascii_heavy` | 40% | ASCII text, pointer tables, dialogue data |
| `mixed_command_data` | 35% | Data with occasional control structures |
| `dead_zero_field` | 20% | Zero-filled padding between data regions |
| `branch_fed_control_pocket` | 5% | Small control structures (diminishing) |

**Expected review postures:**
- `local_control_only`: 50-60% (data regions with local clusters)
- `mixed_lane_continue`: 30% (straight data lanes)
- `manual_owner_boundary_review`: 5-10% (occasional data masquerading as code)
- `dead_lane_reject`: 10-20% (dead_zero_field pages)

### 3. Could we see more dead_zero_field pages?

**YES — highly likely.**

Evidence:
- First `dead_zero_field` appeared at C7:4300 (block 65)
- C7:0E00..1BFF was an **extended dead-zero corridor** (8 of 10 pages in C7:1200..1BFF)
- Pattern: `dead_zero_field` appears in **patches**, not isolated pages
- C7 bank has shown dead zones at: 0E00-11FF, 1200-1BFF (partial), 4300

**Prediction**: Expect 1-3 `dead_zero_field` pages in C7:4E00..57FF, potentially clustered.

### 4. Are we approaching the end of viable code in C7?

**YES — we are likely past the end of viable code.**

Key indicators:
1. **Zero promotions** for 53 consecutive blocks (C5:3B00 through C7:4DFF)
2. **text_ascii_heavy** emergence — this is a terminal state for code discovery
3. **Manual review rate collapse** from 70% to 10% — not enough signal to review
4. **Caller quality degradation**: suspect callers from data regions, unresolved regions only
5. **C7:0800..1BFF** was already identified as "extended dead-zero / low-ingress corridor"

**Assessment**: Viable code in C7 likely ended around C7:3000-3FFF. The 4400+ region is firmly in data territory.

### 5. Remaining bytes analysis (3800 bytes left to C7:FFFF)

| Region | Size | Expected Content |
|--------|------|------------------|
| C7:4E00..57FF | 2,560 bytes | Data-heavy, text_ascii, dead_zero patches |
| C7:5800..FFFF | 14,336 bytes | Likely all data, padding, or garbage bytes |

At current trajectory:
- **C7:4E00..5FFF**: Mixed data with occasional control structures
- **C7:6000..7FFF**: Likely dead_zero_field patches or text data
- **C7:8000..FFFF**: Probably all padding/garbage (no xrefs, no ingress)

---

## Specific Predictions for C7:4E00..57FF

### Prediction Table

| Page | Predicted Family | Predicted Posture | Confidence |
|------|-----------------|-------------------|------------|
| C7:4E00 | text_ascii_heavy OR mixed_command_data | local_control_only | 70% |
| C7:4F00 | mixed_command_data | mixed_lane_continue | 60% |
| C7:5000 | mixed_command_data | local_control_only | 60% |
| C7:5100 | dead_zero_field OR mixed | dead_lane_reject | 50% |
| C7:5200 | mixed_command_data | mixed_lane_continue | 55% |
| C7:5300 | text_ascii_heavy | local_control_only | 50% |
| C7:5400 | mixed_command_data | local_control_only | 60% |
| C7:5500 | mixed_command_data | mixed_lane_continue | 55% |
| C7:5600 | dead_zero_field | dead_lane_reject | 45% |
| C7:5700 | mixed_command_data | local_control_only | 55% |

### Expected Summary Stats

```
Predicted page families:
- mixed_command_data: 6 pages (60%)
- text_ascii_heavy: 2 pages (20%)
- dead_zero_field: 2 pages (20%)

Predicted review postures:
- local_control_only: 5 pages (50%)
- mixed_lane_continue: 3 pages (30%)
- dead_lane_reject: 2 pages (20%)
- manual_owner_boundary_review: 0-1 pages (5-10%)
```

### Promotion Expectation

**Expected promotions: 0**

Rationale:
- Previous 53 blocks: 0 promotions
- Data-heavy trajectory accelerating
- text_ascii_heavy regions do not contain executable code
- Any targets detected will likely be:
  - False positives from data byte patterns
  - Suspect callers from unresolved regions
  - Hard_bad starts from zero-filled padding

---

## Risk Factors

### What could prove this prediction wrong?

1. **Late-blooming code region**: Unlikely but possible — a compact utility routine buried in data
2. **Jump table region**: C7 could have a jump table dispatch area (would show as branch_fed_control_pocket)
3. **Data-to-code transition**: The bank might transition back to code after a data section

### Mitigation

- Still run full `manual_owner_boundary_review` for any pages that qualify
- Check anchor reports for any weak targets (don't skip due diligence)
- Watch for coherent jump table patterns (regular spacing, aligned addresses)

---

## Conclusion

C7:4E00..57FF is expected to continue the **data-heavy trajectory** established in C7:4400..4DFF. The bank has transitioned from mixed code/data to predominantly data regions with ASCII text and zero-filled padding. 

**Bottom line**: Expect 0 promotions, minimal manual review (0-1 pages), and confirmation that C7's viable code regions are behind us. The remaining 3800 bytes to C7:FFFF are likely data, padding, and unused space.

---

*Analysis based on continuation notes 64, 65, 66 and seam block reports through C7:4DFF.*
