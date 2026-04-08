# Bank DB Mapping Session Report

## Session Summary
Continued mapping of Bank DB - the newly discovered code bank in Chrono Trigger.

## Bank DB Overview
- **Region 1**: DB:0000-4000 (Dense code region)
- **Region 2**: DB:4000-8000 (Secondary code region)
- **Dead Zone**: DB:8000-FFFF (Zero-filled, confirmed dead)

## Analysis Results

### 1. Score-6+ Candidates Found

#### DB:0000-4000 (Primary Region)
| Address | Score | Start Byte | Type | Verified |
|---------|-------|------------|------|----------|
| DB:00AC | 6 | 08 (PHP) | Prolog | ✓ |
| DB:024E | 6 | 08 (PHP) | Prolog | ✓ |
| DB:027D | 6 | 08 (PHP) | Prolog | ✓ |
| DB:0290 | 6 | 20 (JSR) | Prolog | ✓ |
| DB:03A7 | 6 | 20 (JSR) | Prolog | ✓ |
| DB:05E2 | 6 | A0 (LDY#) | Prolog | ✓ |
| DB:0813 | 6 | 20 (JSR) | Prolog | ✓ |
| DB:084F | 6 | 08 (PHP) | Prolog | ✓ |
| DB:0AFE | 6 | A0 (LDY#) | Prolog | ✓ |
| DB:0C38 | 6 | 08 (PHP) | Prolog | ✓ |
| DB:0D80 | 6 | 8B (PHB) | Prolog | ✓ |
| DB:1B7E | 6 | 8B (PHB) | Prolog | ✓ |
| DB:210B | 6 | 8B (PHB) | Prolog | ✓ |
| DB:2190 | 6 | 8B (PHB) | Prolog | ✓ |
| DB:2382 | 6 | 08 (PHP) | Prolog | ✓ |
| DB:320C | 6 | 08 (PHP) | Prolog | ✓ |
| DB:3303 | 6 | 08 (PHP) | Prolog | ✓ |

#### DB:4000-8000 (Secondary Region)
| Address | Score | Start Byte | Type | Verified |
|---------|-------|------------|------|----------|
| DB:58C1 | 6 | 20 (JSR) | Prolog | ✓ |
| DB:6015 | 6 | 48 (PHA) | Prolog | ✓ |
| DB:60F2 | 6 | 8B (PHB) | Prolog | ✓ |
| DB:7511 | 6 | 20 (JSR) | Prolog | ✓ |

### 2. Local Code Islands (Cluster Analysis)

#### High-Score Clusters DB:0000-4000
| Range | Score | Width | Returns |
|-------|-------|-------|---------|
| DB:1D81..DB:1D95 | 7 | 21 | 1 |
| DB:1358..DB:1366 | 7 | 15 | 1 |
| DB:1A53..DB:1A5A | 7 | 8 | 1 |
| DB:0C32..DB:0C4C | 6 | 27 | 2 |

#### High-Score Clusters DB:4000-8000
| Range | Score | Width | Returns |
|-------|-------|-------|---------|
| DB:5090..DB:50AC | 8 | 29 | 9 |
| DB:7551..DB:7568 | 8 | 24 | 4 |
| DB:7966..DB:7973 | 6 | 14 | 1 |
| DB:62B8..DB:62C3 | 6 | 12 | 1 |
| DB:41C2..DB:41CC | 6 | 11 | 1 |

### 3. Cross-Bank Callers

**18 total cross-bank calls** targeting **17 unique addresses** in Bank DB:

| Target | Caller Count | Source Banks |
|--------|--------------|--------------|
| DB:22D9 | 2 | CF:A599, CF:D859 |
| DB:5E2B | 1 | C4:D185 |
| DB:0111 | 1 | C7:7D5E |
| DB:0ECF | 1 | C7:B671 |
| DB:8A21 | 1 | C8:4DC2 |
| DB:8A20 | 1 | C9:E16A |
| DB:01FE | 1 | CA:7768 |
| DB:5831 | 1 | CA:7F7B |
| DB:22F5 | 1 | CF:D889 |
| DB:E2CD | 1 | D2:B351 |
| DB:00F2 | 1 | DA:CBD0 |
| DB:8E80 | 1 | E8:DCE0 |
| DB:1378 | 1 | E9:433C |
| DB:020F | 1 | F1:1AE2 |
| DB:0AFC | 1 | F1:5947 |
| DB:60FB | 1 | F2:A57F |
| DB:6A11 | 1 | FE:D966 |

**Note**: Cross-bank targets (DB:8A21, DB:8E80, DB:E2CD, DB:6A11) are in the DB:8000-FFFF range which is zero-filled/dead. These may be:
1. False positives from data misinterpretation
2. Invalid/outdated references
3. Dynamic code that gets loaded

### 4. Verified Functions (Recommended for Manifest)

Top 15 verified candidates with prologue + return instructions:

```
CT_DB_00AC_SCORE6    DB:00AC..DB:00B8    [PHP prologue]
CT_DB_024E_SCORE6    DB:024E..DB:0259    [PHP prologue]
CT_DB_027D_SCORE6    DB:027D..DB:0284    [PHP prologue]
CT_DB_0290_SCORE6    DB:0290..DB:0298    [JSR prologue]
CT_DB_03A7_SCORE6    DB:03A7..DB:03AD    [JSR prologue]
CT_DB_05E2_SCORE6    DB:05E2..DB:05EF    [LDY# prologue]
CT_DB_0813_SCORE6    DB:0813..DB:081E    [JSR prologue]
CT_DB_084F_SCORE6    DB:084F..DB:0857    [PHP prologue]
CT_DB_0AFE_SCORE6    DB:0AFE..DB:0B09    [LDY# prologue]
CT_DB_0C38_SCORE6    DB:0C38..DB:0C43    [PHP prologue]
CT_DB_0D80_SCORE6    DB:0D80..DB:0D87    [PHB prologue]
CT_DB_1B7E_SCORE6    DB:1B7E..DB:1B8B    [PHB prologue]
CT_DB_210B_SCORE6    DB:210B..DB:2119    [PHB prologue]
CT_DB_2190_SCORE6    DB:2190..DB:2197    [PHB prologue]
CT_DB_2382_SCORE6    DB:2382..DB:2385    [PHP prologue]
```

## Statistics

| Metric | Count |
|--------|-------|
| Total candidates analyzed | 344 |
| Score 6+ candidates | 34 |
| Unique verified functions | 17 |
| Cross-bank call targets | 17 |
| Local code islands (score 6+) | 9 |
| **Recommended manifests** | **15** |

## Next Steps

1. **Create manifest files** for the 15 verified functions
2. **Investigate cross-bank targets** that fall in zero-filled regions
3. **Continue mapping** remaining score-4/5 candidates
4. **Analyze function relationships** in the cluster regions (DB:1D81, DB:5090, etc.)

## Files Generated

- `reports/db_0000_4000_backtrack.json` - Backtrack analysis for region 1
- `reports/db_4000_8000_backtrack.json` - Backtrack analysis for region 2
- `reports/db_0000_4000_islands.json` - Local code islands for region 1
- `reports/db_4000_8000_islands.json` - Local code islands for region 2
- `reports/db_cross_bank_callers.json` - Cross-bank caller analysis
- `reports/db_verified_candidates.json` - Verified function candidates
- `reports/db_manifest_recommendations.json` - Recommended manifest entries
