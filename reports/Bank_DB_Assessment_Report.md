# Bank DB Assessment Report

## Bank Information
- **Bank**: DB (0xDB)
- **ROM Offset**: 0x1B0000 - 0x1BFFFF
- **Status**: CODE BANK (verified)
- **Exploration Date**: 2026-04-08

---

## Regional Analysis

### DB:0000-4000 (Lower Half)
- **Classification**: CODE REGION
- **Size**: 16,384 bytes
- **RTS Count**: 51
- **RTL Count**: 13
- **JSL Count**: 109
- **JSR Count**: 251
- **PHP Count**: 633
- **Candidate Functions**: 287 (score 1-6+)
- **Score-6+ Candidates**: 16

### DB:4000-8000 (Mid Half)
- **Classification**: CODE REGION
- **Size**: 16,384 bytes
- **RTS Count**: 50
- **RTL Count**: 14
- **Candidate Functions**: 57
- **Score-6+ Candidates**: 4

### DB:8000-C000 (Upper Half)
- **Classification**: DEAD ZONE (Zero-filled)
- **Size**: 16,384 bytes
- **Status**: Exclude from mapping

### DB:C000-FFFF (Bank End)
- **Classification**: DEAD ZONE (Zero-filled)
- **Size**: 16,383 bytes
- **Status**: Exclude from mapping

---

## Cross-Bank Verification

Bank DB has **18 verified cross-bank calls** from other banks:

| Caller | Target | Type |
|--------|--------|------|
| C4:D185 | DB:5E2B | JML |
| C7:7D5E | DB:0111 | JSL |
| C7:B671 | DB:0ECF | JSL |
| C8:4DC2 | DB:8A21 | JSL |
| C9:E16A | DB:8A20 | JSL |
| CA:7768 | DB:01FE | JSL |
| CA:7F7B | DB:5831 | JSL |
| CF:A599 | DB:22D9 | JSL |
| CF:D859 | DB:22D9 | JSL |
| CF:D889 | DB:22F5 | JSL |
| D2:B351 | DB:E2CD | JSL |
| DA:CBD0 | DB:00F2 | JSL |
| E8:DCE0 | DB:8E80 | JML |
| E9:433C | DB:1378 | JSL |
| F1:1AE2 | DB:020F | JML |
| F1:5947 | DB:0AFC | JSL |
| F2:A57F | DB:60FB | JML |
| FE:D966 | DB:6A11 | JML |

---

## Score-6+ Function Candidates

### High-Confidence Candidates (Score 6)

| Address | Start Byte | Distance | Type | Region |
|---------|------------|----------|------|--------|
| DB:00AC | PHP (08) | 1 | Prologue | 0000-4000 |
| DB:024E | PHP (08) | 1 | Prologue | 0000-4000 |
| DB:027D | PHP (08) | 3 | Prologue | 0000-4000 |
| DB:0290 | JSR (20) | 1 | Call | 0000-4000 |
| DB:03A7 | JSR (20) | 3 | Call | 0000-4000 |
| DB:05E2 | LDY# (A0) | 6 | Load | 0000-4000 |
| DB:0813 | JSR (20) | 6 | Call | 0000-4000 |
| DB:084F | PHP (08) | 2 | Prologue | 0000-4000 |
| DB:0AFE | LDY# (A0) | 8 | Load | 0000-4000 |
| DB:0C38 | PHP (08) | 3 | Prologue | 0000-4000 |
| DB:0D80 | PHB (8B) | 2 | Prologue | 0000-4000 |
| DB:1B7E | PHB (8B) | 13 | Prologue | 0000-4000 |
| DB:210B | PHB (8B) | 14 | Prologue | 0000-4000 |
| DB:2190 | PHB (8B) | 6 | Prologue | 0000-4000 |
| DB:2382 | PHP (08) | 9 | Prologue | 0000-4000 |
| DB:320C | PHP (08) | 2 | Prologue | 0000-4000 |
| DB:3303 | PHP (08) | 2 | Prologue | 0000-4000 |
| DB:39B3 | LDX# (A2) | 8 | Load | 0000-4000 |
| DB:58C1 | JSR (20) | 1 | Call | 4000-8000 |
| DB:6015 | PHA (48) | 3 | Prologue | 4000-8000 |
| DB:60F2 | PHB (8B) | 9 | Prologue | 4000-8000 |
| DB:7511 | JSR (20) | 6 | Call | 4000-8000 |

### Verified via Cross-Bank Calls

| Address | Verified By | Type | Status |
|---------|-------------|------|--------|
| DB:5E2B | C4:D185 (JML) | Entry Point | VERIFIED |
| DB:6A11 | FE:D966 (JML) | Entry Point | HIGH_CONFIDENCE |
| DB:60FB | F2:A57F (JML) | Entry Point | VERIFIED |

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total Candidate Functions | 344 |
| Score-6+ Candidates | 20 |
| Verified via Cross-Bank | 3 |
| Total Functions Identified | 23 |
| Cross-Bank Callers | 18 |
| Dead Zone (8000-FFFF) | 32,767 bytes |

---

## Recommendation

**Bank DB is a CODE BANK** with significant function density in the lower half (0000-8000). The upper half (8000-FFFF) is zero-filled and should be excluded from disassembly.

### Next Steps:
1. Create manifests for top 10 score-6+ candidates
2. Disassemble verified cross-bank targets first (DB:5E2B, DB:6A11, DB:60FB)
3. Cluster analysis around DB:00AC, DB:0813, DB:2190 for function groups
4. Investigate DB:8A20-8A21 region (has multiple cross-bank callers)

---

## Files Created
- `labels/DB_candidates/` - 22 candidate YAML files
- `reports/Bank_DB_Assessment_Report.md` - This report
