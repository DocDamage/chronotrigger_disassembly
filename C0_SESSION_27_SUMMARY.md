# Bank C0 Session 27 Summary

## Coverage Progress
- **Previous**: 223 ranges, 11784 bytes (17.98%)
- **Current**: 225 ranges, 11992 bytes (18.30%)
- **Added**: +2 ranges, +208 bytes (+0.32%)

## Manifests Created (14 total)

### Pass 1062-1071: Score-6 Cluster in C0:6000-7000 Gap
| Pass | Address | Range | Target | Score |
|------|---------|-------|--------|-------|
| 1062 | C0:1212 | C0:1212..C0:1227 | C0:1217 | 6 |
| 1063 | C0:6896 | C0:6896..C0:68B5 | C0:68A5 | 6 |
| 1064 | C0:6986 | C0:6986..C0:699A | C0:698A | 6 |
| 1065 | C0:6D61 | C0:6D61..C0:6D74 | C0:6D64 | 6 |
| 1066 | C0:6E1E | C0:6E1E..C0:6E37 | C0:6E27 | 6 |
| 1067 | C0:6E58 | C0:6E58..C0:6E6C | C0:6E5C | 6 |
| 1068 | C0:6EC7 | C0:6EC7..C0:6EDB | C0:6ECB | 6 |
| 1069 | C0:6EE5 | C0:6EE5..C0:6F01 | C0:6EF1 | 6 |
| 1070 | C0:6EF9 | C0:6EF9..C0:6F0C | C0:6EFC | 6 |
| 1071 | C0:6F08 | C0:6F08..C0:6F1C | C0:6F0C | 6 |

### Pass 1072-1073: C0:0000-2000 Gap
| Pass | Address | Range | Target | Score |
|------|---------|-------|--------|-------|
| 1072 | C0:0CFC | C0:0CFC..C0:0D11 | C0:0D01 | 4 |
| 1073 | C0:0FA5 | C0:0FA5..C0:0FBF | C0:0FAF | 4 |

### Pass 1074-1075: C0:2000-3000 Gap
| Pass | Address | Range | Target | Score |
|------|---------|-------|--------|-------|
| 1074 | C0:269F | C0:269F..C0:26BF | C0:26AF | 6 |
| 1075 | C0:26A2 | C0:26A2..C0:26C0 | C0:26B0 | 6 |

## Regions Scanned
1. **C0:6814..C0:6F50** (C0:6000-7000 gap) - 23 backtrack candidates, 21 islands found
2. **C0:10A0..C0:16AC** (C0:1000-2000 gap) - 14 backtrack candidates found
3. **C0:414D..C0:4611** (C0:4000-5000 gap) - 7 backtrack candidates found
4. **C0:0CA2..C0:107E** (C0:0000-2000 gap) - 10 backtrack candidates found
5. **C0:9E47..C0:A204** (C0:9000-A000 gap) - 6 backtrack candidates found
6. **C0:56DC..C0:5975** (C0:5000-6000 gap) - Scanned
7. **C0:251C..C0:275F** (C0:2000-3000 gap) - 2 score-6 candidates found
8. **C0:D166..C0:D3A4** (C0:D000-E000 gap) - Scanned

## Largest Remaining Gaps in C0
1. C0:6814..C0:6F50 (1852 bytes) - Partially filled
2. C0:10A0..C0:16AC (1548 bytes) - Partially filled
3. C0:414D..C0:4611 (1220 bytes)
4. C0:0CA2..C0:107E (988 bytes) - Partially filled
5. C0:9E47..C0:A204 (957 bytes)
6. C0:FB4D..C0:FF21 (980 bytes)

## Methodology
- Used `score_target_owner_backtrack_v1.py` for backtrack analysis
- Used `find_local_code_islands_v2.py` for island detection
- Targeted score-6+ candidates in major gap regions
- Created 10 manifests for score-6 candidates
- Created 4 manifests for score-4 candidates in high-value gaps

## Files Modified/Created
- `passes/manifests/pass_1062_c0_1212.json` through `pass_1075_c0_26a2.json`

## Notes
The C0:6000-7000 region continues to show high code density with multiple score-6 candidates clustered together. The 23% target remains unmet but progress continues steadily. Future sessions should focus on:
1. C0:414D..C0:4611 (4000-5000 gap)
2. C0:9E47..C0:A204 (9000-A000 gap)  
3. C0:FB4D..C0:FF21 (F000-FFFF gap)
