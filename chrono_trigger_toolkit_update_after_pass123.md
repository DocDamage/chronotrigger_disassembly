# Chrono Trigger Toolkit Update After Pass 123

## What changed
This was a **toolkit-only upgrade pass**. It did **not** advance the disassembly pass counter beyond **123**.

The main goal was to fix the release friction that still existed even though the internal workspace itself was healthy.

## Problems addressed
- The shipped toolkit zip still used an internal root folder name locked to the old `pass119` upgrade scaffold.
- Core scripts were easiest to use only after manually `cd`-ing into the exact workspace root.
- Running tools from the parent extraction directory could misfire on pathing, especially around ROM lookup and report generation.
- There was no repeatable one-command way to package a fresh toolkit release with the **current pass number** embedded in the internal root name.

## Implemented upgrades

### 1. Workspace-root autodetect
Added shared workspace-root detection in `scripts/ct_common.py`.

This now lets key scripts recover the real toolkit root even when launched from the parent extraction directory.

Upgraded scripts:
- `scripts/ct_resume_workspace.py`
- `scripts/ct_toolkit_doctor.py`
- `scripts/ct_generate_build_manifest.py`
- `scripts/ct_inspect_target.py`

### 2. Better ROM path resolution
Improved `default_rom_path()` so relative ROM paths can still resolve correctly when commands are launched from the parent directory instead of only from the workspace root.

### 3. Repeatable release packaging lane
Added a new script:
- `scripts/ct_package_toolkit_release.py`

What it does:
- auto-detects the real workspace root
- refreshes the build manifest
- runs toolkit doctor
- stages a clean release copy
- repackages the toolkit with a **current-pass internal workspace root name**
- emits release metadata under `build/releases/`

### 4. Release manifest lane
New packaged-release metadata now lands in:
- `build/releases/toolkit_release_manifest.json`
- `build/releases/toolkit_release_manifest.md`

### 5. README refresh
Updated the main `README.md` so the release/packaging flow is documented and the new packaging command is obvious.

## Validation
The upgraded scripts were validated from the **parent extraction directory**, not just from inside the workspace root.

Validated successfully:
- toolkit doctor
- build manifest generation
- target inspection
- release packaging

Toolkit doctor result after the upgrade:
- **100.0% health**

## New release artifact produced
- `ct_disasm_toolkit_v6_pass123_toolkit_release_refresh.zip`

## Internal root name in the new packaged zip
- `ct_pass123_toolkit_v6_release_work/`

This fixes the old misleading pass119-root-name problem in the shipped artifact.

## What did not change
- Latest disassembly pass remains **123**
- No new ROM ownership claims were added in this toolkit-only update
- No completion estimate change was claimed from this upgrade alone

## Recommended command going forward
From either the workspace root **or its parent extraction directory**:

```bash
python3 scripts/ct_package_toolkit_release.py --root . --rom "Chrono Trigger (USA).sfc"
```

That is now the cleanest way to ship a refreshed toolkit snapshot after future pass work.
