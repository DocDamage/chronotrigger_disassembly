# Pass 202 Labels: C3:5000-57FF Region

## Tentative Labels (Future Reference)

### C3:5100 Page
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:5131 | ct_c3_5131_score6_candidate | code | Score-6 candidate |
| C3:51EF | ct_c3_51ef_score6_candidate | code | Score-6 candidate |

### C3:5200 Page
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:5247 | ct_c3_5247_entry | code | Suspect entry point |

### C3:5300 Page (Local Control)
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:5364 | ct_c3_5364_cluster | code | Cluster score 6 |

### C3:5400 Page
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:54A5 | ct_c3_54a5_weak_target | code | 2 callers |
| C3:5437 | ct_c3_5437_weak_target | code | 1 caller |

### C3:5500 Page
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:55A5 | ct_c3_55a5_score6 | code | Score-6 candidate |
| C3:5550 | ct_c3_5550_jsr_target | code | JSR target |

### C3:5600 Page (Data Table)
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:5600 | ct_c3_5600_data_table | data | Structured data region |
| C3:5640 | ct_c3_5640_lookup | data | Lookup table entry |

### C3:5700 Page (Jump Table)
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:5777 | ct_c3_5777_jump_a22a | data | Jump to $A22A |
| C3:577C | ct_c3_577c_jump_802a | data | Jump to $802A |
| C3:579F | ct_c3_579f_fragment | code | JSR $8752 fragment |
| C3:57C2 | ct_c3_57c2_jump_5550 | data | Jump to $5550 |

## Notes
C3:5777 appears to be part of a jump table for cross-bank calls, not an actual function. The JMP $A22A indicates a far call to bank $A2.
