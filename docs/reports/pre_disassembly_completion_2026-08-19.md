# Pre-disassembly completion report — 2026-08-19

The repository is ready to cross the disassembly boundary, subject to project-owner approval. This work stops before broad source reconstruction or final assembly authoring.

## Completed scope

- Re-reviewed the requested C3:8800–8FFF, C4:6800–6FFF and 772E, C2 score-14, and C1 mega-cluster priorities.
- Deep-scanned D4 and D6; reconciled D1–D9, C5, C7, CF, and DA–DF; confirmed that E0–FF held no active claims.
- Reviewed every remaining active canonical record and finalized every candidate disposition.
- Preserved all legacy sources and historical reports; corrections are additive and reproducibly reapplied after migration.
- Hardened toolkit entrypoints, xref semantics, bulk correction handling, conservation checks, readiness auditing, CLI output, and regression coverage.

## Mapping outcome

- New executable owners promoted: **0**
- Historical `code_owner` records corrected: **771**
  - reclassified as data: **282**
  - reclassified as executable boundary fragments: **489**
- Final active records: **1,061**
  - code owners: 137
  - helpers/wrappers/veneers: 20
  - executable fragments: 489
  - data: 413
  - text markers: 2
- Candidate ledger: 29 final dispositions, with no deferred entries

Score was treated only as a discovery lead. Asset banks C4–C7 and much of CF contained systematic false positives caused by graphics masks, compressed fields, and little-endian tables. Genuine code windows without independently proven entry/end boundaries were retained as fragments rather than promoted as owners.

## Coverage

| Metric | Baseline | Final |
|---|---:|---:|
| Unique covered bytes | 59,050 | 59,050 |
| Whole-ROM coverage | 1.4079% | 1.4079% |
| Executable bytes | 38,079 | 28,189 |
| Classified-data bytes | 20,971 | 30,861 |
| Canonical manifests | 961 | 961 |
| Canonical records | 1,289 | 1,289 |

The unchanged unique total is intentional: this project phase corrected classifications and ownership claims rather than inflating coverage.

## Validation results

- Pre-disassembly readiness: **READY**, 1,061/1,061 active ranges reviewed
- Evidence/provenance gaps: **0 / 0**
- Deferred candidates: **0**
- Historical conservation: **1,000/1,000 sources; 1,105/1,105 ranges**
- Ownership conflicts: **0** across 1,289 canonical records
- Python compilation: pass
- Pyflakes/static checks: pass
- Unit and regression tests: **48 passed**
- Toolkit doctor: **9/9 passed**
- Strict repository acceptance: **12/12 passed**
- Artifact validation: **4,412 valid, 0 errors**
- Binary/cache policy: pass; no tracked ZIP archives or ROM artifacts introduced

## Remaining risks and boundary

- `tail_fragment` records deliberately do not promise complete function boundaries. Establishing their owning routines is source-reconstruction work and belongs after approval.
- Historical completion reports that promoted opcode-density results remain preserved for provenance; the correction and candidate ledgers are authoritative where they disagree.
- The backup bundle was not modified or removed.

The exact next step is explicit project-owner approval to begin source reconstruction from the authoritative frontier `C3:D000.. / C4:A000..`. Until that approval, no broad disassembly implementation should begin.
