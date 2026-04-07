# Bank C0 Coverage Analysis Report

**Generated:** 2026-04-06  
**Bank Range:** C0:0000-FFFF (64KB)  
**Analysis Scope:** All pass manifests (272 files)

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total C0 Functions Identified | **183** |
| Total Bytes Covered | **7,836 / 65,536** |
| Overall Coverage | **11.96%** |
| Pages with 0% Coverage | **121 / 256 (47.3%)** |
| Pages with <10% Coverage | **164 / 256 (64.1%)** |

---

## Coverage Heatmap

```
       0 1 2 3 4 5 6 7 8 9 A B C D E F
C0:0000 + + + . . + - + + . - - - . . .
C0:1000 + # - . . . - . - - - - . . . +
C0:2000 - . . - . + . - * . . . + - * -
C0:3000 + . . . - * . - - . - . + . . .
C0:4000 - . . . . . + . . . . - - . - .
C0:5000 . . * . * . + . . + - - - . . .
C0:6000 + - - + . + . - - - . . . . - -
C0:7000 + - . . - - + - . - - + - . . -
C0:8000 + + - . - - - + + . - . . - . .
C0:9000 . - . . + . . - . + - - . . - -
C0:A000 . . - + . . * + - - . - . . . .
C0:B000 + + - - . . . - - - . - - - . -
C0:C000 # - * - . . - * * - - - . . . .
C0:D000 . . . . . . . . . * + + * - . -
C0:E000 . - - . - - - . - + - . - - . -
C0:F000 + * . . . . - . . . . . . . . -

Legend: .=0%  -<25%  +<50%  *<75%  #=<100%
```

---

## Coverage by 1KB Regions

### Best Covered Regions

| Rank | Region | Coverage |
|------|--------|----------|
| 1 | C0:C000-C3FF | **42.4%** |
| 2 | C0:1000-13FF | **38.4%** |
| 3 | C0:D800-DBFF | **34.6%** |
| 4 | C0:0000-03FF | **26.6%** |
| 5 | C0:5400-57FF | **26.4%** |

### Least Covered Regions

| Rank | Region | Coverage |
|------|--------|----------|
| 1 | C0:AC00-AFFF | **0.0%** |
| 2 | C0:CC00-CFFF | **0.0%** |
| 3 | C0:D000-D3FF | **0.0%** |
| 4 | C0:D400-D7FF | **0.0%** |
| 5 | C0:F800-FBFF | **0.0%** |

---

## Coverage by 4KB Sectors

| Sector | Range | Coverage | Visual |
|--------|-------|----------|--------|
| 0 | C0:0000-0FFF | 16.7% | `###-----------------` |
| 1 | C0:1000-1FFF | 16.4% | `###-----------------` |
| 2 | C0:2000-2FFF | 14.2% | `##------------------` |
| 3 | C0:3000-3FFF | 11.9% | `##------------------` |
| 4 | C0:4000-4FFF | 7.7% | `#-------------------` |
| 5 | C0:5000-5FFF | 15.9% | `###-----------------` |
| 6 | C0:6000-6FFF | 9.3% | `#-------------------` |
| 7 | C0:7000-7FFF | 11.0% | `##------------------` |
| 8 | C0:8000-8FFF | 11.7% | `##------------------` |
| 9 | C0:9000-9FFF | 7.6% | `#-------------------` |
| 10 | C0:A000-AFFF | 10.1% | `##------------------` |
| 11 | C0:B000-BFFF | 9.1% | `#-------------------` |
| 12 | C0:C000-CFFF | 19.9% | `###-----------------` |
| 13 | C0:D000-DFFF | 13.0% | `##------------------` |
| 14 | C0:E000-EFFF | 8.9% | `#-------------------` |
| 15 | C0:F000-FFFF | 7.9% | `#-------------------` |

---

## Top 5 Most Under-Covered 256-Byte Pages

| Rank | Address Range | Coverage | Function Count |
|------|---------------|----------|----------------|
| 1 | C0:0300-03FF | 0.0% | 0 |
| 2 | C0:0400-04FF | 0.0% | 0 |
| 3 | C0:0900-09FF | 0.0% | 0 |
| 4 | C0:0D00-0DFF | 0.0% | 0 |
| 5 | C0:0E00-0EFF | 0.0% | 0 |

**Note:** The first 10 most under-covered pages all have **0% coverage** with no functions identified.

---

## Largest Coverage Gaps

| Rank | Gap Range | Size (Pages) | Size (Bytes) | Est. Functions |
|------|-----------|--------------|--------------|----------------|
| 1 | **C0:CB00-D8FF** | 14 | 3,584 | ~4 |
| 2 | C0:8B00-93FF | 9 | 2,304 | ~3 |
| 3 | C0:B200-BAFF | 9 | 2,304 | ~3 |
| 4 | C0:6600-6DFF | 8 | 2,048 | ~3 |
| 5 | C0:9A00-A1FF | 8 | 2,048 | ~3 |
| 6 | C0:F700-FEFF | 8 | 2,048 | ~3 |
| 7 | C0:1200-17FF | 6 | 1,536 | ~2 |
| 8 | C0:AA00-AFFF | 6 | 1,536 | ~2 |
| 9 | C0:4100-45FF | 5 | 1,280 | ~2 |
| 10 | C0:7100-75FF | 5 | 1,280 | ~2 |

---

## Function Type Breakdown

| Type | Count | Bytes | Percentage of Coverage |
|------|-------|-------|------------------------|
| owner | 183 | 7,836 | 100% |

---

## Pages with <10% Coverage

**Total: 164 pages (64.1% of Bank C0)**

### Complete List by 1KB Section

| Section | Uncovered Pages |
|---------|-----------------|
| C0:0000 | 0300 |
| C0:0400 | 0400, 0600 |
| C0:0800 | 0900 |
| C0:0C00 | 0D00, 0E00, 0F00 |
| C0:1000 | 1200, 1300 |
| C0:1400 | 1400, 1500, 1600, 1700 |
| C0:1C00 | 1C00, 1D00, 1E00 |
| C0:2000 | 2100, 2200, 2300 |
| C0:2400 | 2400, 2600 |
| C0:2800 | 2900, 2A00, 2B00 |
| C0:2C00 | 2F00 |
| C0:3000 | 3100, 3200, 3300 |
| C0:3400 | 3400, 3600 |
| C0:3800 | 3900, 3A00, 3B00 |
| C0:3C00 | 3D00, 3E00, 3F00 |
| C0:4000 | 4100, 4200, 4300 |
| C0:4400 | 4400, 4500, 4700 |
| C0:4800 | 4800, 4900, 4A00 |
| C0:4C00 | 4D00, 4F00 |
| C0:5000 | 5000, 5100, 5300 |
| C0:5400 | 5500, 5700 |
| C0:5800 | 5800 |
| C0:5C00 | 5D00, 5E00, 5F00 |
| C0:6000 | 6100 |
| C0:6400 | 6400, 6600, 6700 |
| C0:6800 | 6800, 6900, 6A00, 6B00 |
| C0:6C00 | 6C00, 6D00, 6F00 |
| C0:7000 | 7100, 7200, 7300 |
| C0:7400 | 7400, 7500, 7700 |
| C0:7800 | 7800 |
| C0:7C00 | 7C00, 7D00, 7E00, 7F00 |
| C0:8000 | 8300 |
| C0:8400 | 8500 |
| C0:8800 | 8900, 8B00 |
| C0:8C00 | 8C00, 8D00, 8E00, 8F00 |
| C0:9000 | 9000, 9100, 9200, 9300 |
| C0:9400 | 9500, 9600 |
| C0:9800 | 9800, 9A00, 9B00 |
| C0:9C00 | 9C00, 9D00, 9E00, 9F00 |
| C0:A000 | A000, A100 |
| C0:A400 | A400, A500 |
| C0:A800 | A800, AA00, AB00 |
| C0:AC00 | AC00, AD00, AE00, AF00 |
| C0:B000 | B200, B300 |
| C0:B400 | B400, B500, B600, B700 |
| C0:B800 | B800, B900, BA00 |
| C0:BC00 | BE00 |
| C0:C000 | C100, C300 |
| C0:C400 | C400, C500, C600 |
| C0:C800 | C900, CB00 |
| C0:CC00 | CC00, CD00, CE00, CF00 |
| C0:D000 | D000, D100, D200, D300 |
| C0:D400 | D400, D500, D600, D700 |
| C0:D800 | D800 |
| C0:DC00 | DE00, DF00 |
| C0:E000 | E000, E100, E300 |
| C0:E400 | E400, E700 |
| C0:E800 | E800, EB00 |
| C0:EC00 | ED00, EE00, EF00 |
| C0:F000 | F200, F300 |
| C0:F400 | F400, F500, F700 |
| C0:F800 | F800, F900, FA00, FB00 |
| C0:FC00 | FC00, FD00, FE00 |

---

## Recommendations for Next Scanning Priorities

### Priority 1: Largest Gap (Immediate Action)
```
Range:  C0:CB00..C0:D8FF
Size:   3,584 bytes (14 pages)
Note:   This is the largest contiguous uncovered region in Bank C0
```

### Priority 2: Secondary Large Gaps
```
Range:  C0:8B00..C0:93FF  (2,304 bytes)
Range:  C0:B200..C0:BAFF  (2,304 bytes)
Range:  C0:6600..C0:6DFF  (2,048 bytes)
Range:  C0:9A00..C0:A1FF  (2,048 bytes)
```

### Priority 3: Zero-Coverage 1KB Sectors
The following sectors have 0% coverage and should be prioritized:
- C0:AC00-AFFF
- C0:CC00-CFFF  
- C0:D000-D3FF
- C0:D400-D7FF
- C0:F800-FBFF

### Priority 4: Low-Coverage Hotspots
Focus on completing coverage in partially covered sectors:
- C0:4000-4FFF (7.7%)
- C0:9000-9FFF (7.6%)
- C0:6000-6FFF (9.3%)
- C0:B000-BFFF (9.1%)

---

## Summary

Bank C0 currently has **11.96% coverage** with **183 functions** identified across **7,836 bytes**. 

**Key Findings:**
- 47.3% of the bank is completely uncovered (121 pages)
- 64.1% of pages have <10% coverage
- The largest gap is 3.5KB at C0:CB00-D8FF
- Best coverage is in C0:C000-C3FF (42.4%) and C0:1000-13FF (38.4%)

**Estimated Work Remaining:**
Based on average function size of ~43 bytes, approximately **1,340 additional functions** may remain to be discovered in Bank C0.

---

*Report generated by analyze_c0_coverage.py and c0_detailed_coverage.py*
