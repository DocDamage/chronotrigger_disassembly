# Toolkit Missing Capabilities Log

This file exists so friction turns into concrete upgrades instead of being forgotten.

## Implemented in this repo upgrade pass
- repo-native `tools/` folder
- pass manifest schema
- bank-local progress index for C3
- label validation rules
- next-target scoring config
- repo-first workflow docs
- script stubs for publishing, next-lane finding, code/data classification, xref reporting, validation, and progress refresh
- shared low-bank-aware SNES mapping in `tools/scripts/snes_utils.py`
- compatibility entrypoints that forward old workflow commands to maintained implementations
- repo-native `tools/scripts/toolkit_doctor.py` health audit
- mixed manifest-schema compatibility across audit, packaging, and checker scripts
- shared-helper consolidation across active analysis scripts plus duplicate-helper drift detection

## Still incomplete / future work
- real byte parser integration instead of config-first stubs
- automated cross-reference extraction from the ROM/disasm database
- seam confidence report with numeric scoring output
- one-command publish that writes every pass artifact and updates indexes
- branch-state verifier aware of GitHub working branch history
- code/data classifier tuned on actual Chrono Trigger patterns
- rebuild-readiness validation tied to assembler output

## Pain points observed so far
- manual next-lane derivation after code-end markers still exists outside the C3-focused scorer
- multi-file repo publish friction still exists because the publish lane does not yet update every tracked index
- too much manual code-vs-data judgment remains in mixed banks even with the current classifier family
