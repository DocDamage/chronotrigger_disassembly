# Bank C0:B000-FFFF Mapping Report

## Executive Summary

Analysis of the remaining 20KB region (B000-FFFF) in Bank C0 completed. Found **46 score-6+ function candidates** across 5 sampled regions, with **E000-EFFF** showing highest code density (15 high-score candidates).

**Key Findings:**
- Total candidates analyzed: 214 across all regions
- Score-6+ candidates: 46 (21% of total)
- Score-7+ clusters: 6
- Highest cluster score: 9 at C0:CA4D-CA7B
- Data region confirmed: F360-F6E0 (avoid for code mapping)

---

## Score-6+ Candidates by Region

### B000-BFFF (4KB) - 12 candidates
| Address | Score | Start Byte | Target | Distance | Range |
|---------|-------|------------|--------|----------|-------|
| C0:B0E4 | 6 | 20 (JSR) | C0:B0E6 | 2 | C0:B0E4..C0:B0FE |
| C0:B188 | 6 | 20 (JSR) | C0:B192 | 10 | C0:B188..C0:B1AA |
| C0:B202 | 6 | A0 (LDY#) | C0:B204 | 2 | C0:B202..C0:B21C |
| C0:B262 | 6 | A9 (LDA#) | C0:B271 | 15 | C0:B262..C0:B289 |
| C0:B780 | 6 | 20 (JSR) | C0:B788 | 8 | C0:B780..C0:B7A0 |
| C0:B8C5 | 6 | 4B (PHK) | C0:B8CA | 5 | C0:B8C5..C0:B8E2 |
| C0:B996 | 6 | 4B (PHK) | C0:B9A6 | 16 | C0:B996..C0:B9BE |
| C0:BA57 | 6 | 48 (PHA) | C0:BA65 | 14 | C0:BA57..C0:BA7D |
| C0:BCD7 | 6 | 4B (PHK) | C0:BCDC | 5 | C0:BCD7..C0:BCF4 |
| C0:BFDE | 6 | 48 (PHA) | C0:BFE0 | 2 | C0:BFDE..C0:BFF8 |
| C0:BFD8 | 6 | 48 (PHA) | C0:BFE8 | 16 | C0:BFD8..C0:BFFF |
| C0:BFE4 | 6 | 48 (PHA) | C0:BFF2 | 14 | C0:BFE4..C0:BFFF |

### C000-CFFF (4KB) - 8 candidates
| Address | Score | Start Byte | Target | Distance | Range |
|---------|-------|------------|--------|----------|-------|
| C0:C0B5 | 6 | DA (PHX) | C0:C0C0 | 11 | C0:C0B5..C0:C0D8 |
| C0:C475 | 6 | 48 (PHA) | C0:C482 | 13 | C0:C475..C0:C49A |
| C0:C6D9 | 6 | 48 (PHA) | C0:C6E7 | 14 | C0:C6D9..C0:C6FF |
| C0:C71B | 6 | C2 (REP) | C0:C727 | 12 | C0:C71B..C0:C73F |
| C0:C819 | 6 | 20 (JSR) | C0:C820 | 7 | C0:C819..C0:C838 |
| C0:CAAE | 6 | 20 (JSR) | C0:CABD | 15 | C0:CAAE..C0:CAD5 |
| C0:CACA | 6 | A9 (LDA#) | C0:CAD9 | 15 | C0:CACA..C0:CAF1 |
| C0:CBA6 | 6 | 0B (PHD) | C0:CBAD | 7 | C0:CBA6..C0:CBC5 |

### D000-DFFF (4KB) - 5 candidates
| Address | Score | Start Byte | Target | Distance | Range |
|---------|-------|------------|--------|----------|-------|
| C0:D3A5 | 6 | A0 (LDY#) | C0:D3A9 | 4 | C0:D3A5..C0:D3C1 |
| C0:D3A5 | 6 | A0 (LDY#) | C0:D3AD | 8 | C0:D3A5..C0:D3C5 |
| C0:DA52 | 6 | 48 (PHA) | C0:DA60 | 14 | C0:DA52..C0:DA78 |
| C0:DAA4 | 6 | A0 (LDY#) | C0:DAA5 | 1 | C0:DAA4..C0:DABD |
| C0:DD11 | 6 | 48 (PHA) | C0:DD20 | 15 | C0:DD11..C0:DD38 |

### E000-EFFF (4KB) - 15 candidates
| Address | Score | Start Byte | Target | Distance | Range |
|---------|-------|------------|--------|----------|-------|
| C0:E682 | 6 | C2 (REP) | C0:E687 | 5 | C0:E682..C0:E69F |
| C0:E8BA | 6 | 20 (JSR) | C0:E8BB | 1 | C0:E8BA..C0:E8D3 |
| C0:E945 | 6 | C2 (REP) | C0:E952 | 13 | C0:E945..C0:E96A |
| C0:E970 | 6 | 20 (JSR) | C0:E97A | 10 | C0:E970..C0:E992 |
| C0:E9A0 | 6 | 20 (JSR) | C0:E9A5 | 5 | C0:E9A0..C0:E9BD |
| C0:E9A0 | 6 | 20 (JSR) | C0:E9A6 | 6 | C0:E9A0..C0:E9BE |
| C0:E9A0 | 6 | 20 (JSR) | C0:E9A9 | 9 | C0:E9A0..C0:E9C1 |
| C0:E9A0 | 6 | 20 (JSR) | C0:E9AA | 10 | C0:E9A0..C0:E9C2 |
| C0:E9F4 | 6 | C2 (REP) | C0:E9FF | 11 | C0:E9F4..C0:EA17 |
| C0:EA11 | 6 | C2 (REP) | C0:EA1F | 14 | C0:EA11..C0:EA37 |
| C0:EA34 | 6 | A9 (LDA#) | C0:EA42 | 14 | C0:EA34..C0:EA5A |
| C0:EC58 | 6 | C2 (REP) | C0:EC60 | 8 | C0:EC58..C0:EC78 |
| C0:EC6D | 6 | 20 (JSR) | C0:EC77 | 10 | C0:EC6D..C0:EC8F |
| C0:ED0C | 6 | C2 (REP) | C0:ED15 | 9 | C0:ED0C..C0:ED2D |
| C0:EFCB | 6 | 20 (JSR) | C0:EFCC | 1 | C0:EFCB..C0:EFE4 |

### F000-FFFF (4KB) - 6 candidates
| Address | Score | Start Byte | Target | Distance | Range |
|---------|-------|------------|--------|----------|-------|
| C0:F0B9 | 6 | A2 (LDX#) | C0:F0C9 | 16 | C0:F0B9..C0:F0E1 |
| C0:F11D | 6 | A2 (LDX#) | C0:F12B | 14 | C0:F11D..C0:F143 |
| C0:F198 | 6 | A2 (LDX#) | C0:F1A5 | 13 | C0:F198..C0:F1BD |
| C0:F3A5 | 6 | 20 (JSR) | C0:F3A9 | 4 | C0:F3A5..C0:F3C1 |
| C0:F41D | 6 | 0B (PHD) | C0:F42D | 16 | C0:F41D..C0:F445 |

---

## Code Island Clusters (Score-6+)

### B000-BFFF
| Cluster Range | Score | Width | Calls | Branches | Returns |
|---------------|-------|-------|-------|----------|---------|
| C0:B257..C0:B270 | 7 | 26 | 1 | 3 | 2 |
| C0:B2FB..C0:B30E | 7 | 20 | 1 | 4 | 2 |
| C0:B649..C0:B663 | 6 | 27 | 1 | 2 | 2 |
| C0:B777..C0:B784 | 6 | 14 | 1 | 1 | 2 |
| C0:B0DF..C0:B0E5 | 6 | 7 | 1 | 1 | 1 |

### C000-CFFF
| Cluster Range | Score | Width | Calls | Branches | Returns |
|---------------|-------|-------|-------|----------|---------|
| C0:CA4D..C0:CA7B | **9** | 47 | 0 | 6 | 5 |
| C0:CABD..C0:CAD8 | 7 | 28 | 2 | 7 | 2 |
| C0:C983..C0:C996 | 7 | 20 | 1 | 2 | 2 |
| C0:CBEB..C0:CC03 | 6 | 25 | 2 | 4 | 1 |
| C0:C7F2..C0:C7FA | 6 | 9 | 1 | 1 | 1 |
| C0:C817..C0:C81F | 6 | 9 | 1 | 1 | 1 |
| C0:CFDE..C0:CFE4 | 6 | 7 | 1 | 1 | 1 |

### D000-DFFF
| Cluster Range | Score | Width | Calls | Branches | Returns |
|---------------|-------|-------|-------|----------|---------|
| C0:D53B..C0:D54B | 7 | 17 | 1 | 4 | 1 |
| C0:D4FC..C0:D514 | 6 | 25 | 2 | 3 | 1 |
| C0:D88D..C0:D894 | 6 | 8 | 1 | 1 | 1 |
| C0:DB4C..C0:DB53 | 6 | 8 | 1 | 1 | 1 |
| C0:DD51..C0:DD58 | 6 | 8 | 1 | 1 | 1 |
| C0:DF4C..C0:DF53 | 6 | 8 | 1 | 1 | 1 |
| C0:D145..C0:D14B | 6 | 7 | 1 | 1 | 1 |
| C0:D3B4..C0:D3BA | 6 | 7 | 1 | 1 | 1 |

### E000-EFFF
| Cluster Range | Score | Width | Calls | Branches | Returns |
|---------------|-------|-------|-------|----------|---------|
| C0:EA05..C0:EA1E | 6 | 26 | 0 | 5 | 2 |
| C0:E152..C0:E16A | 6 | 25 | 1 | 4 | 1 |
| C0:E93A..C0:E951 | 6 | 24 | 1 | 1 | 1 |
| C0:E9E8..C0:E9FE | 6 | 23 | 0 | 5 | 2 |
| C0:EA44..C0:EA62 | 5 | 31 | 0 | 5 | 2 |
| C0:EA2F..C0:EA41 | 5 | 19 | 0 | 4 | 2 |
| C0:E969..C0:E979 | 5 | 17 | 1 | 2 | 2 |
| C0:E999..C0:E9A9 | 5 | 17 | 1 | 2 | 2 |

### F000-FFFF
| Cluster Range | Score | Width | Calls | Branches | Returns |
|---------------|-------|-------|-------|----------|---------|
| C0:F488..C0:F4A0 | 7 | 25 | 1 | 3 | 1 |
| C0:F408..C0:F420 | 6 | 25 | 1 | 2 | 1 |
| C0:F428..C0:F440 | 6 | 25 | 2 | 2 | 1 |
| C0:F448..C0:F460 | 6 | 25 | 2 | 2 | 1 |
| C0:F468..C0:F480 | 6 | 25 | 1 | 3 | 1 |
| C0:F4A8..C0:F4C0 | 6 | 25 | 1 | 2 | 1 |

---

## Data vs Code Assessment

### Confirmed Data Regions (Avoid)
| Range | Size | Evidence |
|-------|------|----------|
| C0:F360-F6E0 | ~896 bytes | ASCII ratio 80-96%, High repeated pairs, Known data tables |
| C0:F7A9-F7C1 | ~24 bytes | 100% zero/FF bytes |
| C0:FF49-FF61 | ~24 bytes | 60% zero/FF bytes |
| C0:FF8D-FFA5 | ~24 bytes | 60% zero/FF bytes |
| C0:FFA9-FFC1 | ~24 bytes | 60% zero/FF bytes |
| C0:FFEF-FFFF | ~16 bytes | 72% zero/FF bytes |

### High-Probability Code Regions
| Range | Confidence | Evidence |
|-------|------------|----------|
| C0:B000-BFFF | High | 12 score-6+ candidates, 2 score-7 clusters |
| C0:C000-C8FF | High | 6 score-6+ candidates, score-9 cluster at CA4D |
| C0:C900-CFFF | Medium | Mix of code and data patterns |
| C0:D000-DFFF | Medium | 5 score-6+ candidates, score-7 cluster |
| C0:E000-EFFF | Very High | 15 score-6+ candidates, dense function groups |
| C0:F000-F35F | High | Code islands with good scores |
| C0:F6E1-F8FF | Medium | Some code, some data |
| C0:F900-FFFF | Mixed | High ASCII in F900-FBFF, code at FE00+ |

---

## Recommended New Manifests (12 Functions)

Based on score-6+ candidates and cluster analysis:

### Priority 1: High Confidence (Score 7+)
```
C0:B257..C0:B270    ; score-7 cluster, 26 bytes, 1 call, 3 branches
C0:B2FB..C0:B30E    ; score-7 cluster, 20 bytes, 1 call, 4 branches
C0:CA4D..C0:CA7B    ; score-9 cluster, 47 bytes, 6 branches, 5 returns
C0:D53B..C0:D54B    ; score-7 cluster, 17 bytes, 1 call, 4 branches
C0:F488..C0:F4A0    ; score-7 cluster, 25 bytes, 1 call, 3 branches
```

### Priority 2: Good Confidence (Score 6)
```
C0:B0E4..C0:B0FE    ; score-6, JSR prologue
C0:B780..C0:B7A0    ; score-6, JSR prologue
C0:C475..C0:C49A    ; score-6, PHA prologue
C0:C819..C0:C838    ; score-6, JSR prologue
C0:E970..C0:E992    ; score-6, JSR prologue
C0:E9A0..C0:E9C2    ; score-6, JSR prologue, multiple targets
C0:EC58..C0:EC78    ; score-6, REP prologue
```

---

## Code Density by Region

| Region | Total Candidates | Score-6+ | Score-7+ | Code Density |
|--------|------------------|----------|----------|--------------|
| B000-BFFF | 37 | 12 (32%) | 2 (5%) | High |
| C000-CFFF | 47 | 8 (17%) | 3 (6%) | High |
| D000-DFFF | 35 | 5 (14%) | 1 (3%) | Medium |
| E000-EFFF | 52 | 15 (29%) | 0 (0%) | Very High |
| F000-FFFF | 43 | 6 (14%) | 1 (2%) | Medium |

---

## Next Steps

1. **Immediate**: Create manifests for the 12 recommended functions
2. **Verification**: Run disassembly verification on C0:CA4D-CA7B (highest score cluster)
3. **Gap Analysis**: Fill gaps between identified functions
4. **Cross-reference**: Verify call targets match known function signatures
5. **F-Region**: Skip F360-F6E0 data region; focus on F000-F35F and F6E1-FFFF

---

## Summary Statistics

- **Total candidates found**: 214
- **Score-6+ candidates**: 46 (21.5%)
- **Score-7+ clusters**: 6
- **Recommended new manifests**: 12
- **Data regions identified**: 1 major (F360-F6E0)
- **Regions with high code density**: B000, C000, E000

Report generated: 2026-04-08
