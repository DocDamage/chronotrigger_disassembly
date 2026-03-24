# V5 Runtime Evidence Refresh

This maintenance refresh upgrades the runtime side of the toolkit.

## What changed
- recursive runtime trace import under `traces/imported/`
- richer CSV / JSON / text parsing for debugger exports
- weighted runtime validation instead of row-count-only validation
- generated runtime capture plan tied to the live seam
- new WRAM / APU templates and watch-checklist files
- updated bsnes trace targets and watch presets

## Why it matters
The project was strong on static label work but weak on debugger-backed proof. This refresh makes it much easier to import real runtime evidence and promote provisional RAM / packet labels with actual trace support.
