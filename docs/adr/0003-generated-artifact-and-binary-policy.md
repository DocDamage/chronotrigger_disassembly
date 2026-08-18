# ADR 0003: Generated Artifacts, Binary Hygiene, and Cache Policy

## Status
Accepted

## Context
The repository contained tracked copyrighted ROM binaries (`rom/Chrono Trigger (USA).sfc`), multiple redundant copies of large generated xref indices (~18 MB each), legacy zip files under `toolkits/`, and JSON files with inconsistent encodings (BOM, UTF-16, tracebacks).

## Decision

### 1. Binary & Commercial ROM Policy
- Commercial ROM binaries MUST NOT be tracked in Git.
- `rom/*.sfc`, `rom/*.smc`, `*.sfc`, and `*.smc` are added to `.gitignore`.
- The user provides their own legally obtained ROM locally in `rom/Chrono Trigger (USA).sfc`.
- Tooling provides a standalone verification tool (`tools/scripts/verify_rom.py`) checking SHA-256 (`06d1c2b06b716052c5596aaa0c2e5632a027fee1a9a28439e509f813c30829a9`) without embedding game bytes into the repository.
- Unit tests MUST use synthetic mock bytes rather than copyright ROM content.

### 2. Generated Artifacts & Cache Directory
- All generated caches (xref indices, raw search caches) MUST be stored in `tools/cache/` (or `.cache/`) and ignored by Git.
- Redundant tracked copies of xref indexes are removed.
- Generated reports (`reports/coverage.json`, `reports/branch_state.json`) MUST include full provenance (git commit, manifest digest, generator version, UTC timestamp).

### 3. File Encodings & JSON Hygiene
- All tracked `.json`, `.yaml`, `.md`, and `.py` files MUST be encoded in UTF-8 without BOM.
- Files named `.json` MUST contain valid JSON syntax. Plaintext reports or error logs MUST use `.txt`, `.md`, or `.log`.

### 4. Emulators and Toolkit Archives
- Toolkit archive releases should be distributed via Git releases / external artifacts rather than bloating working tree history.
- Local emulator dependencies must provide explicit provenance and licensing documentation in `emulators/README.md`.

## Consequences
- Repository size and clone overhead are reduced.
- Copyright risk is eliminated from tracked working tree.
- Caches are consolidated into a single reproducible path.
