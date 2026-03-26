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

## Still incomplete / future work
- real byte parser integration instead of config-first stubs
- automated cross-reference extraction from the ROM/disasm database
- seam confidence report with numeric scoring output
- one-command publish that writes every pass artifact and updates indexes
- branch-state verifier aware of GitHub working branch history
- code/data classifier tuned on actual Chrono Trigger patterns
- rebuild-readiness validation tied to assembler output

## Pain points observed so far
- manual next-lane derivation after code-end markers
- multi-file repo publish friction
- occasional connector block/timeouts on tiny snapshot files
- too much manual code-vs-data judgment in mixed banks
