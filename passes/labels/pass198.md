# Pass 198 Labels: C3:4000-47FF Region

## Tentative Labels (Future Reference)

### C3:4200 Page
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:427B | ct_c3_427b_fragment | code | JSR $2440 fragment |
| C3:42C2 | ct_c3_42c2_rep_cluster | code | REP #$18 cluster start |
| C3:42D3 | ct_c3_42d3_rtl_return | code | RTL return point |
| C3:42CA | ct_c3_42ca_jsr_8e8e | code | JSR $8E8E call |

### C3:4500 Page
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:4548 | ct_c3_4548_data_table | data | 88-byte data table (score 13 false positive) |
| C3:45A9 | ct_c3_45a9_fragment | code | Score-4 function fragment |

### C3:4600 Page
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:4601 | ct_c3_4601_sep_fragment | code | SEP #$20 fragment |
| C3:4631 | ct_c3_4631_entry_point | code | Suspect entry point |
| C3:4690 | ct_c3_4690_entry_point | code | Suspect entry point |

## Notes
All regions frozen as data due to fragmented execution flow and insufficient caller evidence. Labels documented for future reference if additional context emerges.
