# Pre-disassembly baseline — 2026-08-18

This is the read-only starting snapshot for the pre-disassembly completion program. It records canonical repository state before mapping or manifest edits in this work batch. Historical session percentages and candidate totals are preserved in their original reports but are not substituted for canonical metrics here.

## Repository state

- Branch: `live-work-from-pass166`
- Commit: `d01e39a467f0e46661d9459006396b2b8b42aea0`
- Remote branch: `origin/live-work-from-pass166` at the same commit after `git fetch --prune origin`
- Ahead/behind: `0/0`
- `origin/main`: `487a698bc1fd25cd564853cffe03c26902b7bbeb`
- Working tree before baseline generation: clean
- Authoritative frontier: `C3:D000.. / C4:A000..`

## Canonical inventory and coverage

- Canonical manifests: 961
- Historical closed-range claims conserved: 1,105
- Canonical records: 1,289
- Active records: 1,061
- Superseded provenance records: 228
- Active ownership conflicts: 0
- Unique covered bytes: 59,050
- Executable closed bytes: 38,079
- Classified-data closed bytes: 20,971
- Whole-ROM coverage: 1.4079% of 4 MiB
- Active banks: 23

Priority-bank canonical coverage at baseline:

| Bank | Bytes | Coverage | Disjoint intervals |
|---|---:|---:|---:|
| C1 | 1,661 | 2.53% | 45 |
| C2 | 883 | 1.35% | 10 |
| C3 | 29,665 | 45.27% | 56 |
| C4 | 1,393 | 2.13% | 48 |
| C5 | 1,505 | 2.30% | 20 |
| CF | 1,623 | 2.48% | 45 |
| D1 | 933 | 1.42% | 18 |
| D4 | 499 | 0.76% | 15 |
| D6 | 798 | 1.22% | 24 |

## Verification and unresolved-candidate baseline

The repository did not contain a canonical candidate-disposition registry at this starting commit. Consequently, a single defensible global count of unpromoted candidates could not be derived from the many historical JSON, YAML, ASM, and Markdown pools without first reconciling duplicates and already-promoted ranges.

The canonical manifest set itself contains a larger readiness gap:

- all 1,289 records have `verification_status: pending`;
- all 1,061 active records are therefore pending final verification;
- 963 active records have no structured `evidence` object;
- 47 active records carry a structured score of at least 6.

These values are the authoritative starting unresolved counts. Historical candidate pools remain leads until each entry is assigned an accepted, rejected, duplicate/already-covered, or deferred disposition with source provenance.

## Validation results

The following commands ran without changing tracked files:

```text
python -m tools.ctrepo acceptance --strict
python tools/scripts/toolkit_doctor.py --strict --output-json <temp>/doctor.json --output-md <temp>/doctor.md
python tools/scripts/generate_coverage.py --strict --output-json <temp>/coverage.json --output-md <temp>/coverage.md
git fetch --prune origin
git rev-list --left-right --count HEAD...origin/live-work-from-pass166
```

Results:

- strict acceptance: passed 12/12 steps;
- Python compilation: 241 files passed;
- Pyflakes: passed;
- tests: 39 passed;
- toolkit doctor: passed 8/8 checks at the unmodified baseline;
- manifest/schema integrity: 961 manifests valid;
- conservation: 1,000/1,000 source manifests represented and 1,105/1,105 historical ranges conserved;
- ownership: zero unresolved conflicts;
- repository artifacts: 4,402 scanned, 4,402 valid, zero errors;
- binary/cache policy: passed, with the local ROM remaining ignored and untracked;
- report drift: deterministic payloads and provenance current.

## Baseline defect discovered after recording

The baseline doctor did not exercise every active analysis entrypoint. Direct invocation of `score_target_owner_backtrack_v1.py` and the primary `run_seam_block_v1.py` workflow exposed stale shared-helper imports. This is a toolkit-health gap, not a change to the baseline figures above. The current work batch expands the doctor with a toolkit-wide local-import audit, CLI help smoke tests, and an end-to-end seam-pipeline regression test before mapping resumes.

No ROM, archive, generated seam-cache, or backup-bundle artifact was added or removed while establishing this baseline.
