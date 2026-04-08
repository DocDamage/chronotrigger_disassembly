# Bank C0:8400-8FFF Region Mapping Report

## Executive Summary
- **Region:** C0:8400-8FFF (3KB, 12 pages)
- **Current coverage:** 15 small ranges (~347 bytes, ~11%)
- **Score-6+ candidates found:** 22
- **New function ranges identified:** 8 recommended for promotion

## Seam Block Analysis Results
```
C0:8400..C0:84FF: mixed_command_data / manual_owner_boundary_review
C0:8500..C0:85FF: mixed_command_data / manual_owner_boundary_review  
C0:8600..C0:86FF: mixed_command_data / manual_owner_boundary_review
C0:8700..C0:87FF: branch_fed_control_pocket / manual_owner_boundary_review
C0:8800..C0:88FF: branch_fed_control_pocket / manual_owner_boundary_review
C0:8900..C0:89FF: branch_fed_control_pocket / local_control_only
C0:8A00..C0:8AFF: branch_fed_control_pocket / manual_owner_boundary_review
C0:8B00..C0:8BFF: text_ascii_heavy / local_control_only
C0:8C00..C0:8CFF: text_ascii_heavy / local_control_only
C0:8D00..C0:8DFF: text_ascii_heavy / bad_start_or_dead_lane_reject
C0:8E00..C0:8EFF: text_ascii_heavy / local_control_only
C0:8F00..C0:8FFF: text_ascii_heavy / manual_owner_boundary_review
```

## Score-6+ Candidates (22 total)

### High Confidence Tier
| Address | End | Score | Start Byte | Type | Notes |
|---------|-----|-------|------------|------|-------|
| C0:8434 | C0:845D | 6 | A9 (LDA) | Clean start | RTS at 8444 |
| C0:84A2 | C0:84BF | 6 | 20 (JSR) | Clean start | Short helper |
| C0:851E | C0:853B | 6 | 20 (JSR) | Clean start | DMA-related |
| C0:8580 | C0:859D | 6 | 20 (JSR) | Clean start | - |
| C0:8644 | C0:8661 | 6 | 20 (JSR) | Clean start | - |
| C0:86A6 | C0:86C3 | 6 | 20 (JSR) | Clean start | - |
| C0:8703 | C0:8741 | 6 | A2 (LDX) | Clean start | Complex function |
| C0:8A43 | C0:8A85 | 6 | A9 (LDA) | Clean start | Coordinate math |
| C0:8A92 | C0:8AB6 | 6 | 08 (PHP) | Clean start | **Stack frame setup** |

### Medium Confidence Tier
| Address | End | Score | Start Byte | Type |
|---------|-----|-------|------------|------|
| C0:8724 | C0:8773 | 6 | 20 (JSR) | Clean start |
| C0:874A | C0:8797 | 6 | C2 (REP) | Clean start |
| C0:8756 | C0:87A5 | 6 | 20 (JSR) | Clean start |
| C0:877C | C0:87C5 | 6 | C2 (REP) | Clean start |
| C0:8788 | C0:87D7 | 6 | 20 (JSR) | Clean start |
| C0:8789 | C0:8809 | 6 | 20 (JSR) | Clean start |
| C0:8805 | C0:8836 | 6 | 0B (PHD) | Clean start |
| C0:882B | C0:8872 | 6 | 20 (JSR) | Clean start |
| C0:888D | C0:88BA | 6 | A9 (LDA) | Clean start |
| C0:88D1 | C0:8906 | 6 | 0B (PHD) | Clean start |
| C0:8A43 | C0:8A85 | 6 | A9 (LDA) | Clean start |
| C0:8D02 | C0:8D21 | 6 | 20 (JSR) | Clean start |

## PHP Prologue Functions (5 found)
Five functions with proper PHP/PLP stack frame management:
- **C0:8837** - Dispatcher with multiple branches
- **C0:886C** - Utility with clear frame
- **C0:8A76** - Return-anchored helper
- **C0:8A85** - Return-anchored helper  
- **C0:8A92** - Highest confidence, clear PHP/RTS pattern

## RTS Returns Found
76 RTS instructions in the 8400-8FFF region - indicates dense executable code

## Code Density Assessment
| Region | Type | Density | Notes |
|--------|------|---------|-------|
| 8400-8700 | Utility/DMA helpers | Medium | Multiple small functions |
| 8700-8A00 | Core library | High | Branch-fed control pockets |
| 8A00-8B00 | Graphics/coordinate | High | Math operations |
| 8B00-8F00 | Mixed code/data | Variable | Text-heavy but executable |

## Recommended New Manifests

### Tier 1: Immediate Promotion (High Confidence)
```json
{
  "range": "C0:8434..C0:845D",
  "label": "ct_c0_8434_unknown_init",
  "score": 6,
  "prologue": "LDA #$0F",
  "returns": ["C0:8444"],
  "kind": "code_owner"
}
```

```json
{
  "range": "C0:8A92..C0:8AB6",
  "label": "ct_c0_8a92_stack_frame_helper",
  "score": 6,
  "prologue": "PHP",
  "returns": ["C0:8AAB"],
  "kind": "code_helper"
}
```

### Tier 2: After Boundary Verification
```json
{
  "range": "C0:8703..C0:8741",
  "label": "ct_c0_8703_complex_utility",
  "score": 6,
  "notes": "Multiple internal branches, needs boundary verification"
}
```

```json
{
  "range": "C0:8A43..C0:8A85",
  "label": "ct_c0_8a43_coordinate_math",
  "score": 6,
  "notes": "Graphics-related coordinate calculations"
}
```

### Tier 3: Extension Candidates
- Extend C0:8500..C0:8518 to capture full function body
- Extend C0:86DD..C0:86F6 based on entry point analysis
- Extend C0:8719..C0:8770 (currently documented but partial)

## Next Steps
1. Promote 5-8 Tier 1 candidates to manifests
2. Run `render_seam_block_report_v1.py` for detailed analysis
3. Verify boundaries for Tier 2 candidates
4. Continue mapping to 9000-9FFF region
