# Bank C3:6000-6FFF Analysis Summary

## Overview
Analysis of the newly discovered high-density region C3:6000-6FFF in the Chrono Trigger SNES ROM disassembly project.

- **Region Size**: 4096 bytes (16 pages)
- **Previous Coverage**: ~1.1% (46 bytes documented)
- **Analysis Date**: 2026-04-08

---

## Key Findings

### Score-6+ Candidates (Strong Function Evidence)
| Address | Target | Score | Prologue | Status |
|---------|--------|-------|----------|--------|
| C3:65AB | C3:65AE | 6 | PHD | ✓ Documented (pass 713) |
| C3:6643 | C3:6648 | 6 | LDA# | ✓ Documented (pass 714) |
| **C3:66A6** | C3:66B0 | **6** | **LDA#** | **→ NEW (pass 716)** |
| **C3:6A29** | C3:6A2F | **6** | **JSR** | **→ NEW (pass 717)** |
| **C3:6ACB** | C3:6ACD | **6** | **PHP** | **→ NEW (pass 718)** |
| **C3:6C11** | C3:6C20 | **6** | **JSL** | **→ NEW (pass 719)** |

### Score-4 Candidates (Moderate Function Evidence)
Top 10 candidates requiring further analysis:

| Address | Target | Score | Prologue | Notes |
|---------|--------|-------|----------|-------|
| C3:600C | C3:6010 | 4 | JSR | C3:6000 page entry |
| C3:6041 | C3:604A | 4 | BCC | Shared start candidate |
| C3:62CE | C3:62D1 | 4 | ADC | C3:6200 page |
| C3:6410 | C3:6416 | 4 | DEC | C3:6400 page |
| C3:6454 | C3:645A | 4 | JSR | → NEW (pass 721) |
| C3:64DA | C3:64DD | 4 | JSR | C3:6400 page |
| C3:6504 | C3:6505 | 4 | PHP | C3:6500 page |
| C3:6807 | C3:6808 | 4 | JSR | C3:6800 page |
| C3:68CE | C3:68D4 | 4 | JMP | C3:6800 page |
| C3:690B | C3:6918 | 4 | PHD | → NEW (pass 722) |
| C3:6A4F | C3:6A53 | 4 | JSL | → NEW (pass 723) |

---

## New Manifests Created

### Score-6 Priority Manifests
1. **pass716_c3_66a6_gap.json** - C3:66A6..C3:66C8 (LDA# prologue)
2. **pass717_c3_6a29_gap.json** - C3:6A29..C3:6A47 (JSR prologue)
3. **pass718_c3_6acb_gap.json** - C3:6ACB..C3:6AE5 (PHP prologue)
4. **pass719_c3_6c11_gap.json** - C3:6C11..C3:6C38 (JSL prologue)

### Score-4 Secondary Manifests
5. **pass720_c3_600c_gap.json** - C3:600C..C3:6028 (JSR prologue)
6. **pass721_c3_6454_gap.json** - C3:6454..C3:6472 (JSR prologue)
7. **pass722_c3_690b_gap.json** - C3:690B..C3:6930 (PHD prologue)
8. **pass723_c3_6a4f_gap.json** - C3:6A4F..C3:6A6B (JSL prologue)

---

## Page Family Analysis

### Distribution by Type
| Page Family | Count | Description |
|-------------|-------|-------------|
| candidate_code_lane | 10 | Pages with executable code patterns |
| branch_fed_control_pocket | 3 | Branch-controlled code pockets |
| mixed_command_data | 2 | Mixed code and data |
| text_ascii_heavy | 1 | ASCII text data |

### Review Posture
| Posture | Count | Pages |
|---------|-------|-------|
| bad_start_or_dead_lane_reject | 9 | C3:6000,6100,6200,6300,6400,6500,6800,6900,6A00 |
| local_control_only | 2 | C3:6700, 6C00 |
| manual_owner_boundary_review | 2 | C3:6600, 6B00 |
| mixed_lane_continue | 3 | C3:6D00, 6E00, 6F00 |

---

## Local Code Clusters (High-Score Islands)

### Score-6 Clusters
| Range | Width | Calls | Returns |
|-------|-------|-------|---------|
| C3:6334..C3:6345 | 18 bytes | 1 | 1 |
| C3:6641..C3:6649 | 9 bytes | 1 | 1 |

### Score-5 Clusters
| Range | Width | Calls | Returns |
|-------|-------|-------|---------|
| C3:6CAF..C3:6CB5 | 7 bytes | 1 | 1 |

### Score-4 Clusters
| Range | Width | Calls | Returns |
|-------|-------|-------|---------|
| C3:6C00..C3:6C14 | 21 bytes | 2 | 1 |
| C3:6730..C3:6740 | 17 bytes | 1 | 1 |
| C3:6BDA..C3:6BEB | 18 bytes | 0 | 1 |
| C3:6C61..C3:6C70 | 16 bytes | 0 | 3 |

---

## Coverage Improvement

### Before Analysis
- Documented ranges in C3:6000-6FFF: **2**
- Documented bytes: **~46 bytes**
- Coverage: **~1.1%**

### After New Manifests
- New manifests created: **8**
- Estimated new coverage: **~200-250 bytes**
- New coverage: **~5-6%**

### Potential Coverage
With all score-4+ candidates documented:
- Estimated potential coverage: **~800-1200 bytes**
- Potential coverage: **~20-30%**

---

## Files Generated

1. `reports/c3_6000_6fff_backtrack.json` - Backtrack analysis results
2. `reports/c3_6000_6fff_seam_block.json` - Seam block scan results
3. `reports/c3_6000_6fff_analysis_report.txt` - Detailed analysis report
4. `reports/C3_6000_6FFF_DISCOVERY_SUMMARY.md` - This summary document

### New Manifests
- `passes/manifests/pass716_c3_66a6_gap.json`
- `passes/manifests/pass717_c3_6a29_gap.json`
- `passes/manifests/pass718_c3_6acb_gap.json`
- `passes/manifests/pass719_c3_6c11_gap.json`
- `passes/manifests/pass720_c3_600c_gap.json`
- `passes/manifests/pass721_c3_6454_gap.json`
- `passes/manifests/pass722_c3_690b_gap.json`
- `passes/manifests/pass723_c3_6a4f_gap.json`

---

## Next Steps

1. **Verify new manifests** - Run validation on created manifests
2. **Continue scanning** - Additional score-4 candidates may be promoted
3. **Analyze gaps** - Check gaps between documented functions
4. **Extend region** - Consider C3:7000+ if density continues

---

## Methodology

### Tools Used
- `run_seam_block_v1.py` - 16-page contiguous block scanner
- `score_target_owner_backtrack_v1.py` - Owner boundary backtracking
- `run_c3_candidate_flow_v7.py` - C3-specific triage analysis

### Scoring Criteria
- Score += 2 for prologue byte (PHD, PHP, JSR, JSL, LDA#, etc.)
- Score += 2 for return instructions (RTS, RTL, RTI)
- Score -= 4 for hard bad starts (BRK, COP, 0x00, 0xFF)
- Score -= 2 for high ASCII ratio (>45%)
- Score -= 2 for high zero/FF ratio (>25%)

---

*Report generated by Bank C3 Analysis Subagent*
