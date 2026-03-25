# bsnes-plus capture checklist

1. Pick one profile from `reports/runtime/runtime_capture_plan.md`.
2. Add CPU breakpoints for the listed addresses.
3. Add WRAM/low-bank watches for the listed ranges.
4. For sound-path captures, also log writes to `$2140-$2143`.
5. Export as CSV/JSON when possible; otherwise save plain-text logs.
6. Drop the export into `traces/imported/` under a profile-specific subfolder.
7. Rerun `python3 scripts/ct_resume_workspace.py --workdir .`.
