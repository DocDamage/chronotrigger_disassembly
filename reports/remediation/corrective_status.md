# Remediation Corrective Action Status

| Field | Value |
|---|---|
| Repository | Chrono Trigger Disassembly |
| Branch | `live-work-from-pass166` |
| Baseline Commit | `253f2f6c75cd9b572bdc1fc25d6dcc0e8d148a59` |
| Last Reviewed Commit | `c5e6f287ddd5f1afdbb9ff50f67886c34e6769c0` |
| Plan | `docs/plans/REMEDIATION_CORRECTIVE_ACTION_IMPLEMENTATION_PLAN.md` |
| Last Updated | 2026-08-18 |
| Current State | **Implementation and clean report provenance complete; independent acceptance pending** |

## Phase status

| Phase | Status | Current evidence |
|---|---|---|
| 0 — Freeze and preserve | Complete | Baseline inventories and SHA-256 recovery evidence remain under `reports/remediation/`. |
| 1 — Regression and policy harness | Complete | 39 tests; strict schemas and semantic policy validation are active. |
| 2 — Migration and trust repair | Complete | Path-plus-hash source identity, transactional replacement, pending-by-default verification, and rejection of unknown kinds. |
| 3 — Source recovery and rebuild | Complete | 1,000/1,000 source files represented; 961 canonical manifests; a second 962-file generation is byte-identical. |
| 4 — Trust and gap reconciliation | Complete | 1,105 baseline claims checked with 0 trust changes; 106 pass numbers factually accounted as baseline-absent. |
| 5 — Range ownership | Complete | 326 explicit interval decisions; original claims retained; 184 active non-overlapping residual records; 0 active conflicts; 0 waivers. |
| 6 — Seam and coverage authority | Complete | Pass 1229 explicitly records `C3:D000.. / C4:A000..`; 59,050 unique covered bytes. |
| 7 — Doctor, CLI, tests, and CI parity | Complete | Local 12-step acceptance passes; doctor passes 8/8; CI calls the same strict policy gates. |
| 8 — Reports and provenance | Complete | Drift checks are read-only and pass. Canonical reports were regenerated from clean implementation commit `c5e6f287ddd5f1afdbb9ff50f67886c34e6769c0`; clean-provenance enforcement passes across newline conventions. |
| 9 — Binary and cache hygiene | Current tree complete; history cleanup deferred | 82 tracked ZIPs (284,204,840 bytes) removed from the index and inventoried by hash; no ROM/ZIP/raw-xref cache is tracked. Reachable-history rewrite remains separately gated. |
| 10 — Documentation reconciliation | Complete | Current seam, coverage, archive policy, progress metrics, and status claims are reconciled. |
| 11 — Independent clean acceptance | Pending release workflow | Local acceptance passes. A fresh-clone/clean-detached-worktree acceptance run requires committed inputs. |

## Verified metrics

- Source conservation: 1,000 / 1,000; 0 missing.
- Historical range conservation: 1,105 / 1,105; 0 missing.
- Canonical manifests: 961, plus `manifest_migration_map.json`.
- Canonical range records: 1,289 total; 1,061 active and 228 superseded provenance records.
- Unique active coverage: 59,050 bytes (1.4079% of the 4 MiB ROM).
- Range conflicts: 0 active; waiver registry: 0.
- Pass gaps: 106 baseline-absence records with reachable commit and existing evidence paths.
- Tests: 39 passing; Pyflakes: 0 findings; doctor: 8/8; canonical JSON/YAML artifact report: 4,401 valid, 0 errors.

## Remaining release actions

1. Commit the clean-source report refresh separately.
2. Run `python -m tools.ctrepo acceptance --strict` from a fresh clone or clean detached worktree.
3. Keep Git-history cleanup deferred unless maintainers separately approve the coordinated rewrite runbook.
