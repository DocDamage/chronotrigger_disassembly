# Remediation Corrective Action Status

| Field | Value |
|---|---|
| Repository | Chrono Trigger Disassembly |
| Branch | `live-work-from-pass166` |
| Baseline Commit | `c00ebe6f8e2d81f9c724c79215ac7643a5c1b353` |
| Last Reviewed Commit | `8779214587ea05fc52a1ecbd448a8387f5628c19` |
| Plan | `docs/plans/REMEDIATION_CORRECTIVE_ACTION_IMPLEMENTATION_PLAN.md` |
| Last Updated | 2026-08-18 |
| Current State | **Non-destructive remediation complete; all release acceptance gates pass** |

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
| 8 — Reports and provenance | Complete | Drift checks are read-only and pass. Canonical reports were regenerated from clean implementation commit `8779214587ea05fc52a1ecbd448a8387f5628c19`; clean-provenance enforcement passes across newline conventions. |
| 9 — Binary and cache hygiene | Current tree complete; history cleanup deferred | 82 tracked ZIPs (284,204,840 bytes) removed from the index and inventoried by hash; no ROM/ZIP/raw-xref cache is tracked. Reachable-history rewrite remains separately gated. |
| 10 — Documentation reconciliation | Complete | Current seam, coverage, archive policy, progress metrics, and status claims are reconciled. |
| 11 — Independent clean acceptance | Complete | The 12-step strict acceptance suite passes from a fresh detached worktree at commit `ffbb234`; 39 tests pass and report drift remains current across checkout newline conventions. |

## Verified metrics

- Source conservation: 1,000 / 1,000; 0 missing.
- Historical range conservation: 1,105 / 1,105; 0 missing.
- Canonical manifests: 961, plus `manifest_migration_map.json`.
- Canonical range records: 1,289 total; 1,061 active and 228 superseded provenance records.
- Unique active coverage: 59,050 bytes (1.4079% of the 4 MiB ROM).
- Range conflicts: 0 active; waiver registry: 0.
- Pass gaps: 106 baseline-absence records with reachable commit and existing evidence paths.
- Tests: 39 passing; Pyflakes: 0 findings; doctor: 8/8; canonical JSON/YAML artifact report: 4,401 valid, 0 errors.

## Separately gated history maintenance

The current tree is release-ready. Historical ROM/archive blobs remain reachable from older commits; keep Git-history cleanup deferred unless maintainers separately approve the coordinated rewrite runbook.
