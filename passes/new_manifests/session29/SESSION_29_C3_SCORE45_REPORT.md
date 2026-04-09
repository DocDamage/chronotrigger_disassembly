# Session 29: Bank C3 Score-4/5 Processing Report

## Session Information
- **Session**: 29
- **Date**: 2026-04-08
- **Focus**: Process score-4/5 candidates to push C3 coverage toward 30%
- **Starting Coverage**: ~28.2%
- **Target Coverage**: 30%
- **Gap**: ~1.8% (~1,180 bytes)

---

## Manifests Created

### Score-4 Candidates from C3:5000-5FFF (Priority Queue)

| Pass | Address | Type | Estimated Bytes | Region |
|------|---------|------|-----------------|--------|
| 1200 | C3:5110 | CPY# prologue | 30 | 5000-5FFF |
| 1201 | C3:515E | PHD prologue | 30 | 5000-5FFF |
| 1202 | C3:5436 | SED pattern | 46 | 5000-5FFF |
| 1203 | C3:549F | SED handler | 30 | 5000-5FFF |
| 1204 | C3:578D | LDX# prologue | 42 | 5000-5FFF |
| 1205 | C3:57BC | Branch-heavy | 27 | 5000-5FFF |
| 1206 | C3:5CA8 | LDA# prologue | 30 | 5000-5FFF |
| 1207 | C3:5DF9 | Call-heavy | 30 | 5000-5FFF |

### Score-4 Candidates from C3:6000-6FFF (Discovery Region)

| Pass | Address | Type | Estimated Bytes | Region |
|------|---------|------|-----------------|--------|
| 1208 | C3:600C | JSR entry | 28 | 6000-6FFF |
| 1209 | C3:6041 | BCC handler | 10 | 6000-6FFF |
| 1210 | C3:62CE | ADC handler | 9 | 6000-6FFF |
| 1211 | C3:6410 | DEC handler | 7 | 6000-6FFF |
| 1212 | C3:64DA | JSR helper | 4 | 6000-6FFF |
| 1213 | C3:6504 | PHP init | 10 | 6000-6FFF |
| 1214 | C3:6807 | JSR target | 2 | 6000-6FFF |
| 1215 | C3:68CE | JMP handler | 7 | 6000-6FFF |
| 1216 | C3:6CA0 | Cluster start | 21 | 6000-6FFF |
| 1217 | C3:6BDA | Return-anchored | 18 | 6000-6FFF |
| 1218 | C3:6730 | Multi-return | 17 | 6000-6FFF |
| 1219 | C3:6C61 | Call-dense | 16 | 6000-6FFF |

---

## Coverage Impact

### Estimated New Coverage
- **Total manifests created**: 20
- **Estimated new bytes**: 397 bytes
- **Coverage increase**: ~0.6%

### Updated Bank C3 Status (Estimated)
- Previous coverage: ~28.2%
- New coverage: **~28.8%**
- Remaining to 30%: **~1.2%** (~780 bytes)

---

## Regions Covered

### C3:5000-5FFF (Game Logic Region)
- **8 new manifests** created
- **Estimated coverage**: 267 bytes
- Focus: SED patterns, prologues, branch-heavy functions

### C3:6000-6FFF (Discovery Region)
- **12 new manifests** created
- **Estimated coverage**: 130 bytes
- Focus: Entry points, handlers, clusters

---

## Validation Checklist

### Manifest Structure
- [x] All 20 manifests have valid JSON structure
- [x] All manifests include pass_index, bank, session fields
- [x] All manifests include target start/end addresses
- [x] All manifests include metadata with prologue/epilogue info
- [x] All manifests tagged with "Session 29 - Score-4/5 Processing"

### Coverage Targets
- [x] 15-20 manifests created (✓ 20 created)
- [x] Focus on score-4/5 candidates
- [x] Gap fillers prioritized
- [x] Compact functions included

---

## Next Steps

### Immediate
1. Validate manifests with disassembler
2. Move validated manifests to passes/manifests/
3. Generate label files for confirmed functions

### Future (To Reach 30%)
1. Continue processing remaining score-4 candidates
2. Analyze C3:7000-7FFF and C3:8000-8FFF regions
3. Look for compact functions in remaining gaps
4. Process C3:0000-2000 and C3:2000-3000 regions

---

## Summary

Session 29 successfully created **20 manifests** for score-4/5 candidates in Bank C3:
- 8 manifests from C3:5000-5FFF priority queue
- 12 manifests from C3:6000-6FFF discovery region

**Estimated coverage improvement**: 28.2% → 28.8% (+0.6%)

Remaining work to reach 30%:
- Need additional ~780 bytes documented
- Consider score-3 candidates with strong evidence
- Explore remaining regions (7000-7FFF, 8000-8FFF)

---

*Generated: 2026-04-08*  
*Session 29 - Score-4/5 Processing Complete*
