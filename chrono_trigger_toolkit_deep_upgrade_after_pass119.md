# Chrono Trigger Toolkit Deep Upgrade After Pass 119

This upgrade was not another cosmetic report pass. It hardens the toolkit around the real failure modes that showed up after the bank-correction work.

## What was added

### 1. Canonical next-session parser
New helper:
- `scripts/ct_handoff_parse.py`

It now parses:
- `Latest completed pass: **N**`
- title-style notes like `Pass 119`
- seam headings such as:
  - `## Best next seam`
  - `## The real next seam now`
  - `## Best next move`

This removes the brittle single-regex dependence that let stale seam text survive even after newer pass files were present.

### 2. Pass-artifact ingest lane
New script:
- `scripts/ct_ingest_pass_artifacts.py`

What it does:
- scans a source directory for loose pass artifacts
- copies missing/changed files into the workspace
- refreshes canonical notes from the latest pass-specific artifacts:
  - `notes/next_session_start_here.md`
  - `notes/chrono_trigger_disasm_passNNN.md`
  - `notes/chrono_trigger_labels_passNNN.md`
- writes a machine-readable sync report:
  - `reports/completion/ct_pass_artifact_sync.json`
  - `reports/completion/ct_pass_artifact_sync.md`

This is the big practical upgrade for future sessions: if new pass files get uploaded outside the workspace, the toolkit now has a built-in lane to ingest them instead of silently lagging behind.

### 3. Stronger state sync
Updated script:
- `scripts/ct_sync_handoff_state.py`

What changed:
- it now uses the canonical parser instead of one brittle regex
- it records the exact next-session note source used to derive the live seam
- it refreshes `state/current_state.json` and `state/workspace_config.json` from parsed note/report truth, not stale hand-carry text

### 4. Doctor now checks generated-report freshness, not just script health
Updated script:
- `scripts/ct_toolkit_doctor.py`

New checks:
- canonical next-session note exists, matches the latest pass-specific note, and is parseable
- unresolved dashboard seam/pass match current state
- seam priority report seam/pass match current state
- pass-artifact sync report exists and is not older than the current pass

Result after rebuild in this upgraded workspace:
- toolkit doctor health score: **100.0%**

### 5. Target inspector CLI
New script:
- `scripts/ct_inspect_target.py`

What it gives you in one shot for an address like `C2:8820`:
- raw ROM bytes around the target
- latest overlapping labels
- nearby labels
- bank-correct xrefs
- note/pass-file mentions

That is a real speed upgrade for future static passes because it cuts out a bunch of manual cross-checking.

### 6. Resume/bootstrap now starts with artifact ingestion
Updated script:
- `scripts/ct_resume_workspace.py`

New behavior:
- accepts `--artifact-dir`
- runs pass-artifact ingest before rebuilding reports
- includes the new sync report in the startup reading lane
- surfaces the new target inspector in its suggested commands

### 7. Documentation refreshed
Updated:
- `README.md`
- `tool_manifest.md`

They now document the new V6.1-style maintenance upgrades and the new high-value commands.

## What this fixes in practice

The toolkit can now catch and prevent all of these:
- stale canonical next-session note despite newer pass files existing
- stale unresolved dashboard or seam-priority report even when state already moved on
- fragile seam parsing tied to one markdown wording pattern
- wasted time manually grepping labels/xrefs/notes for one hot target
- uploaded pass artifacts sitting outside the workspace without being folded in

## High-value commands now

```bash
python3 scripts/ct_ingest_pass_artifacts.py --root . --source-dir /path/to/new/pass/files
python3 scripts/ct_resume_workspace.py --workdir . --rom "Chrono Trigger (USA).sfc" --artifact-dir /path/to/new/pass/files
python3 scripts/ct_inspect_target.py C2:8820 --root . --rom "Chrono Trigger (USA).sfc"
```

## Honest note

This deep upgrade did **not** invent new disassembly claims. It improved the toolkit’s ability to:
- stay synchronized with the real latest pass
- catch report drift early
- inspect hot targets faster
- absorb future uploaded pass artifacts cleanly
