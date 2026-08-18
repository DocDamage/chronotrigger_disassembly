# Contributor Guide

Welcome to the Chrono Trigger Disassembly project!

## 1. Setup

Clone the repository and install development dependencies in a virtual environment:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

Place your verified SNES USA release ROM in `rom/Chrono Trigger (USA).sfc` and verify it:
```powershell
python -m tools.ctrepo verify-rom
```

## 2. Canonical Commands

Use the unified `tools.ctrepo` CLI for all standard workflow tasks:

| Command | Purpose |
|---|---|
| `python -m tools.ctrepo test` | Run pytest unit and integration tests |
| `python -m tools.ctrepo check` | Run strict manifest schema and semantic checks |
| `python -m tools.ctrepo doctor` | Run comprehensive repository health checks |
| `python -m tools.ctrepo coverage` | Rebuild coverage reports from canonical manifests |
| `python -m tools.ctrepo verify-rom` | Verify local ROM checksum without copying bytes |

## 3. Pass Lifecycle & Manifest Contract

Every new pass:
1. Must be numbered sequentially (e.g. `pass1230.json`).
2. Must follow Canonical Manifest Schema v2 (`schema_version: 2`).
3. Must define `closed_ranges` with uppercase hex `BB:AAAA..BB:EEEE` format.
4. Closed ranges must not introduce unreviewed collisions or overlaps with existing active code owners.
5. All tests and strict doctor checks must pass before opening a Pull Request.
