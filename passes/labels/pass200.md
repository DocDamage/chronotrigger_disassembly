# Pass 200 Labels: C3:4800-4FFF Region

## Tentative Labels (Future Reference)

### C3:4900 Page
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:4930 | ct_c3_4930_rts_fragment | code | RTS return point |
| C3:493A | ct_c3_493a_sta_7e7480bb | code | Long store to $7E:7480BB |
| C3:4953 | ct_c3_4953_jmp_3810 | code | JMP $3810 |
| C3:4994 | ct_c3_4994_jsr_0080 | code | JSR $0080 fragment |

### C3:4A00 Page
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:4A00 | ct_c3_4a00_data_table | data | 42-byte data table |
| C3:4A2A | ct_c3_4a2a_cluster_start | data | Cluster score 11 start |

### C3:4D00 Page
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:4D4A | ct_c3_4d4a_score6_candidate | code | Score-6 candidate start |
| C3:4D49 | ct_c3_4d49_cluster | code | Cluster score 4 |

### C3:4E00 Page
| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:4E0E | ct_c3_4e0e_score6_candidate | code | Score-6 candidate |
| C3:4EE7 | ct_c3_4ee7_score6_candidate | code | Score-6 candidate |
| C3:4E2C | ct_c3_4e2c_cluster | code | Cluster score 5 |

## Notes
All regions frozen as data due to fragmented execution or data-like characteristics. Labels documented for future reference.
