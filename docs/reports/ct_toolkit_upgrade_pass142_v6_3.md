# Chrono Trigger Toolkit Upgrade — pass 142 / v6.3

## What changed
- fixed the smoke-test target-selection fallback so seam text no longer degrades into junk targets when the session packet is missing or stale
- added `scripts/ct_release_audit.py` to validate workspace freshness, packaged zip contents, top-level root naming, and report drift after packaging
- upgraded `scripts/ct_package_toolkit_release.py` so packaging now runs the release audit after the zip is created
- added `scripts/ct_generate_seam_candidates.py` to score likely callable starts inside the live seam from incoming calls, packet seeds, and simple boundary hints
- extended Windows wrapper coverage for the release-audit and seam-candidate lanes
- bumped the toolkit version marker to **v6.3**

## Why this matters
The old toolkit could still *look* healthy while shipping a stale smoke report from an older pass. That is exactly the kind of quiet drift that can waste time or mislead the next seam split. The new audit lane catches that before release, and the seam-candidate report makes the next structural pass more surgical.

## New high-value commands
```bash
python3 scripts/ct_generate_seam_candidates.py --root . --rom "Chrono Trigger (USA).sfc"
python3 scripts/ct_release_audit.py --root . --zip ../ct_disasm_toolkit_v6_3_pass142_toolkit_release_refresh.zip
python3 scripts/ct_package_toolkit_release.py --root . --rom "Chrono Trigger (USA).sfc"
```
