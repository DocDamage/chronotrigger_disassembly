# Runtime Evidence Workflow

Use runtime evidence to confirm ownership and control flow, not to invent names from scratch.

## First-pass routine
1. Read `notes/next_session_start_here.md`.
2. Read `reports/runtime/runtime_capture_plan.md`.
3. Pick the smallest profile that answers the current seam question.
4. Capture CPU hits, WRAM writes/reads, and APU port traffic if relevant.
5. Save the trace into `traces/imported/`.
6. Run `python3 scripts/ct_resume_workspace.py --workdir .`.
7. Read:
   - `reports/runtime/runtime_evidence_summary.md`
   - `reports/ct_runtime_validation.md`
   - `reports/runtime/runtime_capture_plan.md`

## What good evidence looks like
- same address hit repeatedly across multiple frames or scene transitions
- live writes to the exact WRAM strip you think a helper owns
- APU port writes with matching command bytes near the C7 handlers
- negative evidence too: no write/read hits where the static guess said there should be some

## What to avoid
- naming from one-off trace noise
- assuming every mention means execution
- mixing multiple subsystem captures into one unlabeled file
