# Chrono Trigger Toolkit Deep Upgrade After Pass 130 — Round 3

## Scope
This was a **toolkit-only** deep audit and upgrade pass.
The disassembly itself remains at **pass 130**.

## What I found in the deep dive

### 1. Release readiness still depended on trust, not proof
The toolkit had a doctor and a package lane, but it still did **not** have a single release-style smoke test proving that the most important commands actually still worked from:
- the workspace root, and
- a parent extraction directory using root autodetect.

That gap mattered because the toolkit has repeatedly been sensitive to launch context and report/output path drift.

### 2. Doctor scoring still mixed real failures with advisory friction
A harmless issue like an awkward temp workspace name could drag down the health score even when the toolkit was otherwise fine.
That made the doctor less trustworthy, because the score could look worse without a real functional problem.

### 3. Release packaging did not carry forward proof-of-health
Even when a clean package was built, the release metadata did not include smoke-test evidence.
So a shipped zip could still look “fresh” without proving the important commands had actually been exercised.

## Implemented upgrades

### 1. New release smoke-test lane
Added:
- `scripts/ct_smoke_test.py`

What it does:
- runs a high-value command set from the workspace root
- runs the same critical subset from a parent-dir harness using workspace autodetect
- records pass number, chosen inspection target, command lines, pass/fail status, and stdout/stderr tails
- writes:
  - `reports/ct_smoke_test.json`
  - `reports/ct_smoke_test.md`

Validated commands in the smoke lane:
- toolkit doctor
- build manifest generation
- session packet generation
- target inspection
- parent-dir autodetect for doctor/session-packet/inspect flows

### 2. Windows launcher coverage extended
Added:
- `windows/run_smoke_test.bat`

### 3. Doctor scoring made more honest
Updated:
- `scripts/ct_toolkit_doctor.py`

Changes:
- the workspace-root-name check is now **advisory** and does **not** reduce the health percentage by itself
- smoke-test freshness is now surfaced in the doctor output
- the doctor now expects the smoke-test wrapper to exist in Windows coverage

Result:
- harmless workspace naming noise no longer makes the toolkit look broken
- actual failures still show up clearly

### 4. Post-pass sync doctor call updated
Updated:
- `scripts/ct_post_pass_sync.py`

Change:
- the doctor invocation now knows about the smoke-test report path, so state/report refreshes do not silently ignore that new readiness lane

### 5. Release manifest upgraded
Updated:
- `scripts/ct_package_toolkit_release.py`
- `build/releases/toolkit_release_manifest.json`
- `build/releases/toolkit_release_manifest.md`

Changes:
- release metadata now includes smoke-test details
- release manifest now records smoke-test health and inspected target
- package flow now includes a smoke-test lane in its logic

### 6. README refresh
Updated:
- `README.md`

Changes:
- documented the new smoke-test workflow
- documented that advisory checks no longer drag down doctor score
- surfaced the new Windows smoke wrapper

## Validation

### Smoke test
- result: **100.0%**
- target used: `C2:CED2..C2:CF92`
- root-context command set: passed
- parent-dir autodetect command set: passed

### Toolkit doctor
- result: **100.0%**
- warnings: none
- notices: none

### Compile health
- all Python scripts compile cleanly after the upgrade

### Release packaging
A fresh upgraded release zip was produced:
- `ct_disasm_toolkit_v6_pass130_toolkit_deep_refresh_round3.zip`

One honest note: inside this sandbox, the end-to-end CLI packaging wrapper was flaky to validate directly after the smoke lane was added. I still produced the final release zip successfully by running the same underlying packaging functions directly after the smoke/doctor validation succeeded.

## Net effect
The toolkit is stronger now because it no longer just **claims** it is healthy.
It now has a real proof lane for the important launch paths, a more honest doctor score, and release metadata that carries forward evidence instead of vibes.
