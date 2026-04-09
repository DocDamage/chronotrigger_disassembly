# C3:8000 High Bank Scan Report

## Executive Summary

The C3:8000 high bank region (first 8 pages: C3:8000-C3:87FF) was scanned using the seam_block_v1 scanner. Results indicate **significantly higher code density** compared to the C3 low bank, with 62.5% of pages classified as `candidate_code_lane` and multiple strong promotion candidates identified.

## Scan Parameters

| Parameter | Value |
|-----------|-------|
| ROM | Chrono Trigger (USA).sfc |
| Start Address | C3:8000 |
| Pages Scanned | 8 (C3:8000-C3:87FF) |
| Scanner | seam_block_v1 |
| Session | 32 |
| Branch | live-work-from-pass166 |

## Page Family Distribution

The high bank exhibits different patterns than the low bank:

| Page Family | Count | Percentage | Description |
|-------------|-------|------------|-------------|
| candidate_code_lane | 5 | 62.5% | Pages with code-like characteristics |
| mixed_command_data | 1 | 12.5% | Mixed code and data |
| text_ascii_heavy | 1 | 12.5% | ASCII text with possible code |
| branch_fed_control_pocket | 1 | 12.5% | Complex branch table structures |

## Review Posture Analysis

| Posture | Count | Description |
|---------|-------|-------------|
| bad_start_or_dead_lane_reject | 4 | Pages with problematic entry points |
| local_control_only | 2 | Pages with only local flow evidence |
| manual_owner_boundary_review | 2 | Pages requiring manual review |

## Strong Promotion Candidates

### Score 6 Backtrack Candidates (5 identified)

| Address | Target | Start Byte | Distance | Classification |
|---------|--------|------------|----------|----------------|
| C3:8074 | C3:807C | 20 (JSR) | 8 bytes | clean_start |
| C3:80C4 | C3:80C9 | 08 (PHP) | 5 bytes | clean_start |
| C3:8274 | C3:8278 | 20 (JSR) | 4 bytes | clean_start |
| C3:8400 | C3:8402 | 20 (JSR) | 2 bytes | clean_start |
| C3:8440 | C3:8440 | 20 (JSR) | 0 bytes | clean_start |

### Weak Caller Evidence Targets

| Address | Strength | Caller Count | Notable Callers |
|---------|----------|--------------|-----------------|
| C3:800C | weak | 8 | C3:91C3, C3:C8FB, C3:9337, C3:9584, C3:ADE3, C3:AE06, C3:C09E, C3:C122 |
| C3:8207 | weak | 2 | E5:8EA7, EC:3F40 (cross-bank) |
| C3:8500 | weak | 3 | C3:0520, C3:38D9, C3:4368 |
| C3:862B | weak | 1 | C3:832D |
| C3:8692 | weak | 1 | C3:2A9C |
| C3:8752 | weak | 1 | C3:579F |
| C3:8772 | weak | 1 | C3:584A |

## Special Findings

### C3:8700 - Branch-Fed Control Pocket

This page is particularly significant:

- **8 local islands** detected (highest in scan)
- **3 local clusters** with complex interconnections
- **Score 8 cluster** at C3:87BA..C3:87E1:
  - 6 child ranges
  - 40 bytes width
  - 6 calls, 6 branches, 6 returns
  - Consecutive RTS pattern suggests jump table

This represents a dense code region likely containing a branch table or dispatch mechanism.

## High Bank vs Low Bank Comparison

| Metric | Low Bank (C3:0000-4000) | High Bank (C3:8000-8700) |
|--------|-------------------------|--------------------------|
| Code Lane Pages | Lower percentage | 62.5% |
| Score 6 Candidates | Fewer per page | 5 in 8 pages |
| Cross-Bank Callers | Limited | E5, EC banks |
| Branch Tables | Less common | C3:8700 pocket |
| Caller Evidence Density | Moderate | High (C3:800C has 8 callers) |

## Conclusions

1. **Higher Code Density**: The C3:8000 high bank contains substantially more code than the low bank, with 5 out of 8 pages showing candidate_code_lane characteristics.

2. **Strong Promotion Opportunities**: 5 score-6 backtrack candidates are ready for immediate promotion to the disassembly.

3. **Cross-Bank Integration**: Evidence of calls from banks E5 and EC into C3:8000 region indicates this is an important integration point.

4. **Complex Control Structures**: The branch_fed_control_pocket at C3:8700 suggests sophisticated control flow patterns (likely jump tables) not commonly seen in the low bank.

5. **Recommendation**: The high bank warrants more aggressive scanning and promotion compared to the low bank. Continuing the scan from C3:8800-C3:9FFF is highly recommended.

## Action Items

1. **Immediate**: Promote 5 score-6 candidates to pass manifests
2. **Short-term**: Manual disassembly review of C3:800C (8 callers) and C3:87BA cluster
3. **Medium-term**: Expand seam scan to C3:8800-9FFF
4. **Follow-up**: Investigate cross-bank callers from E5 and EC banks

## Files Generated

- `passes/pass1221.json` - Pass manifest for C3:8000 region
- `disassembly/pass208.md` - Disassembly notes and findings
- `C3_8000_HIGH_BANK_REPORT.md` - This report

---
*Report generated from seam_block_v1 scan results*
*Session 32, Branch: live-work-from-pass166*
