# Bank C0 Upper Regions Mapping Report

**Generated:** 2026-04-08  
**Target Regions:** C0:8000-BFFF, C0:C000-FFFF

## Summary

| Region | Islands Found | Score-6+ Islands | Backtracks | Score-6+ Backtracks |
|--------|--------------|------------------|------------|---------------------|
| C0:8000-BFFF | 259 | 15 | 247 | 97 |
| C0:C000-FFFF | 109 | 23 | 177 | 33 |
| **Total** | **368** | **38** | **424** | **130** |

## Manifests Generated

20 new manifests created (pass882.json through pass901.json):

| Manifest | Range | Score | Method | Description |
|----------|-------|-------|--------|-------------|
| pass882.json | C0:970D..C0:9725 | 7 | island | 25-byte function, 2 returns |
| pass883.json | C0:D53B..C0:D54B | 7 | island | 17-byte function, DMA-related |
| pass884.json | C0:F488..C0:F4A0 | 7 | island | 25-byte function, HDMA area |
| pass885.json | C0:812C..C0:813C | 6 | island | 17-byte function, 2 calls |
| pass886.json | C0:813B..C0:814D | 6 | backtrack | JSR target near existing code |
| pass887.json | C0:8204..C0:8216 | 6 | backtrack | LDA# start, clean entry |
| pass888.json | C0:8253..C0:8270 | 6 | backtrack | LDA# start, extended range |
| pass889.json | C0:8253..C0:8273 | 6 | backtrack | LDA# start, alternate target |
| pass890.json | C0:82B5..C0:82D5 | 6 | backtrack | LDA# start, utility function |
| pass891.json | C0:82D5..C0:82F5 | 6 | backtrack | LDA# start, utility function |
| pass892.json | C0:82F5..C0:830F | 6 | backtrack | LDA# start, utility function |
| pass893.json | C0:8335..C0:8355 | 6 | backtrack | LDA# start, utility function |
| pass894.json | C0:835C..C0:8375 | 6 | backtrack | PHY start (5A), stack operation |
| pass895.json | C0:83BC..C0:83D5 | 6 | backtrack | PHY start, stack operation |
| pass896.json | C0:83DC..C0:83F5 | 6 | backtrack | PHY start, stack operation |
| pass897.json | C0:843C..C0:8455 | 6 | backtrack | PHY start, stack operation |
| pass898.json | C0:8644..C0:8659 | 6 | backtrack | JSR start, subroutine |
| pass899.json | C0:86A6..C0:86BB | 6 | backtrack | JSR start, subroutine |
| pass900.json | C0:874B..C0:876B | 6 | backtrack | JSR start, extended subroutine |
| pass901.json | C0:877C..C0:878F | 6 | backtrack | REP start (C2), mode setting |

## Top Score-6+ Candidates by Region

### C0:8000-BFFF Islands

| Range | Score | Width | Calls | Returns | Notes |
|-------|-------|-------|-------|---------|-------|
| C0:970D..C0:9725 | 7 | 25 | 1 | 2 | Index/pointer operation |
| C0:88AB..C0:88C3 | 6 | 25 | 2 | 1 | Near C0:88A7 (existing) |
| C0:97B3..C0:97CB | 6 | 25 | 1 | 1 | String/data operation |
| C0:97E4..C0:97FC | 6 | 25 | 1 | 1 | String/data operation |
| C0:9877..C0:988F | 6 | 25 | 1 | 1 | Data processing |
| C0:98A8..C0:98C0 | 6 | 25 | 1 | 1 | Data processing |
| C0:AAE4..C0:AAFC | 6 | 25 | 2 | 1 | Engine utility |
| C0:B2FB..C0:B30E | 6 | 20 | 1 | 2 | Near C0:B188 (existing) |
| C0:812C..C0:813C | 6 | 17 | 2 | 1 | Extends C0:80BD area |
| C0:B777..C0:B784 | 6 | 14 | 1 | 2 | Near scroll handler |
| C0:B08D..C0:B095 | 6 | 9 | 1 | 1 | Near C0:B08E (existing) |
| C0:99C4..C0:99CB | 6 | 8 | 1 | 1 | Quick utility |
| C0:99D6..C0:99DD | 6 | 8 | 1 | 1 | Quick utility |
| C0:AB9B..C0:ABA1 | 6 | 7 | 1 | 1 | Branch helper |
| C0:B0DF..C0:B0E5 | 6 | 7 | 1 | 1 | Near B000 handler |

### C0:C000-FFFF Islands

| Range | Score | Width | Calls | Returns | Notes |
|-------|-------|-------|-------|---------|-------|
| C0:F488..C0:F4A0 | 7 | 25 | 1 | 1 | HDMA config cluster |
| C0:D53B..C0:D54B | 7 | 17 | 1 | 1 | DMA helper |
| C0:CABD..C0:CAD5 | 6 | 25 | 1 | 1 | Script handler area |
| C0:CAC0..C0:CAD8 | 6 | 25 | 2 | 2 | Script handler area |
| C0:CBEB..C0:CC03 | 6 | 25 | 2 | 1 | Near C0:C6E7 (existing) |
| C0:D4FC..C0:D514 | 6 | 25 | 2 | 1 | DMA processing |
| C0:E152..C0:E16A | 6 | 25 | 1 | 1 | Array operation |
| C0:F408..C0:F420 | 6 | 25 | 1 | 1 | HDMA config cluster |
| C0:F428..C0:F440 | 6 | 25 | 2 | 1 | HDMA config cluster |
| C0:F448..C0:F460 | 6 | 25 | 2 | 1 | HDMA config cluster |
| C0:F468..C0:F480 | 6 | 25 | 1 | 1 | HDMA config cluster |
| C0:F4A8..C0:F4C0 | 6 | 25 | 1 | 1 | HDMA config cluster |
| C0:E93A..C0:E951 | 6 | 24 | 1 | 1 | Near existing E93A handler |
| C0:C983..C0:C996 | 6 | 20 | 1 | 2 | Script processing |
| C0:C7F2..C0:C7FA | 6 | 9 | 1 | 1 | Near C0:C7A6 (existing) |
| C0:C817..C0:C81F | 6 | 9 | 1 | 1 | Graphics helper |

## Connections to Existing C0 Documentation

The scan reveals several candidates that connect to existing documented regions:

1. **C0:813B area** - Extends the C0:80BD DMA handler cluster
2. **C0:8200-8500 area** - Dense cluster of utility functions near C0:84A7
3. **C0:88AB** - Adjacent to existing C0:88A7 handler
4. **C0:9700-9900** - String/data processing region
5. **C0:AAE4** - Engine utility near A600 area
6. **C0:B08D/B0DF** - Extensions to B000 handler area
7. **C0:C7F2/C817** - Graphics handler extensions
8. **C0:C983/CABD** - Script handler area extensions
9. **C0:CBEB** - Near C0:C6E7 script handler
10. **C0:F400-F500** - HDMA configuration cluster (multiple functions)

## Recommendations

### Priority 1 (High Confidence)
- **C0:970D..C0:9725** (score 7) - Well-defined function with multiple returns
- **C0:F488..C0:F4A0** (score 7) - HDMA configuration function
- **C0:D53B..C0:D54B** (score 7) - DMA utility

### Priority 2 (Good Coverage)
- **C0:8200-8500 range** - 10+ backtrack candidates suggest dense code region
- **C0:F400-F500 cluster** - Multiple related HDMA functions
- **C0:C900-CB00 range** - Script processing extensions

### Priority 3 (Gap Filling)
- **C0:9700-9900** - String/data utilities
- **C0:AA00-AB00** - Engine utilities
- **C0:C7F2/C817** - Graphics helpers

## Next Steps

1. Process manifests pass882.json through pass901.json through the disassembly pipeline
2. Run seam block analysis on C0:8200-8500 for extended coverage
3. Investigate the F400-F500 HDMA cluster more deeply
4. Connect C0:C900-CB00 script handlers to existing C0:C6E7 documentation

## Files Generated

- `reports/c0_8000_bfff_islands.json` - Island scan results
- `reports/c0_c000_ffff_islands.json` - Island scan results
- `reports/c0_8000_bfff_backtrack.json` - Backtrack analysis
- `reports/c0_c000_ffff_backtrack.json` - Backtrack analysis
- `passes/manifests/pass882.json` through `pass901.json` - 20 new manifests
