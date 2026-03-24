# Toolkit Maintenance Refresh

This refresh is a tooling pass on top of the bundled pass-95 snapshot.

## What changed
- The completion score is now evidence-weighted instead of hard-coding bank separation and rebuild readiness.
- Workspace/state propagation now pulls the latest pass and live seam from the current note/report state instead of stale pass-93-era defaults.
- Added a dispatcher-family summary report for veneer / packet / opcode-family work.
- Added a focused sound/APU packet summary report for the C7 low-bank command side.
- Added an interactive dispatcher tracer helper for targeted inspection by label text or address.

## Why this matters
The recent passes have been closing real semantic work faster than the old score/report layer could admit.
This refresh does not pretend the rebuild layer is solved; it just stops the toolkit from underselling active progress and gives the next passes better navigation aids.

## Recommended first commands after unzipping
```bash
python3 scripts/ct_resume_workspace.py --workdir .
python3 scripts/ct_trace_dispatcher.py --label apu
python3 scripts/ct_trace_dispatcher.py --address C7:01A1
```
