# Chrono Trigger Disassembly Toolkit

This folder is the repo-native home for the active reverse-engineering toolkit.

## Goals
- keep tooling versioned with the disassembly work
- eliminate stale zip/tool drift
- make every pass reproducible
- separate source scripts from generated pass artifacts
- support repo-first workflow on the live working branch

## Layout
- `scripts/` - executable helpers and report generators
- `config/` - schemas, rules, scoring weights, and tracked indexes
- `docs/` - workflow notes, confidence rules, repo layout, and conventions
- `requirements.txt` - lightweight Python dependency note

## Stable entrypoints
The toolkit keeps compatibility entrypoints for the common workflow:
- `find_next_callable_lane.py`
- `build_call_anchor_report.py`
- `classify_c3_ranges.py`
- `validate_labels.py`
- `publish_pass_bundle.py`
- `update_bank_progress.py`

Those scripts now forward to the newest maintained implementations so older handoffs and workflow notes remain usable without landing on placeholder stubs.

The toolkit also tolerates both repo-era canonical manifests and older legacy target-list manifests in its audit lanes.
Active analysis scripts now prefer the shared SNES helper layer instead of carrying local HiROM and range-parsing copies.
`snes_utils_hirom_v2.py` is now a compatibility shim over `snes_utils.py` so older imports stay stable without maintaining a second mapper implementation.

## Self-audit
- `scripts/audit_toolkit_entrypoints.py` - statically validates toolkit-local imported symbols and smoke-tests every argparse CLI guarded by a main entrypoint
- `scripts/audit_pre_disassembly_readiness.py` - reports pending active ranges, missing structured evidence/provenance, and unresolved candidate dispositions before source reconstruction
- `scripts/toolkit_doctor.py` - compiles all repository Python, runs Pyflakes and tests, invokes the toolkit entrypoint audit, validates canonical manifests and ownership, audits branch/policy state, and enforces the binary/cache policy

Run the focused entrypoint audit directly with:

```powershell
python tools/scripts/audit_toolkit_entrypoints.py
```

The primary seam scanner also has a synthetic-ROM integration test so import-compatible but non-runnable pipelines fail acceptance.

For large scans, `run_seam_block_v1.py --compact --minimum-score 6 --output-json <path>` retains only score-qualified candidates, clusters, and material targets. This is the preferred evidence format for whole-bank review.

Run the separate disassembly-boundary gate with:

```powershell
python tools/scripts/audit_pre_disassembly_readiness.py --strict
```

Ordinary repository acceptance can remain green while this stricter gate reports unresolved historical mapping evidence.

## Evidence and correction ledgers

- `config/candidate_dispositions.json` records accepted, rejected, reclassified, already-covered, and explicitly deferred candidate decisions.
- `config/manifest_corrections.json` records factual post-migration corrections without changing immutable legacy manifests.
- `migrate_manifests.py` reapplies adjudications and corrections deterministically. Schema-validated bulk corrections may be used when one reviewed data classification covers a large homogeneous pool; each original pass/range/label identity is still expanded and conserved individually.

## Core workflow
1. derive the next callable/data target
2. inspect bytes / xrefs / boundaries
3. close the pass honestly
4. publish one pass bundle
5. update bank progress and pass manifest
6. record candidate dispositions and any reviewed legacy correction
7. validate labels, ownership, migration reproducibility, and readiness impact
8. commit the result to the working branch

## Current missing-capability backlog
See `../reports/toolkit_missing_capabilities.md`.
