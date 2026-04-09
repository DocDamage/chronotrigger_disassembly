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
- `scripts/toolkit_doctor.py` - compiles the toolkit, checks low-bank mapping correctness, verifies core entrypoints are no longer stubbed, smoke-tests the main CLI surfaces, validates both legacy and canonical manifest schemas, and catches duplicate helper drift in active scripts

## Core workflow
1. derive the next callable/data target
2. inspect bytes / xrefs / boundaries
3. close the pass honestly
4. publish one pass bundle
5. update bank progress and pass manifest
6. validate labels and overlapping owners/helpers
7. commit the result to the working branch

## Current missing-capability backlog
See `../reports/toolkit_missing_capabilities.md`.
