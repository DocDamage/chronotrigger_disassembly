# Repository Remediation — Baseline Summary

| Attribute | Baseline Value |
|---|---|
| Generation Timestamp | `2026-08-18T20:22:47.948727+00:00` |
| Git Branch | `live-work-from-pass166` |
| Git Commit Baseline | `253f2f6c75cd9b572bdc1fc25d6dcc0e8d148a59` |
| Python Version | `3.10.11` |
| ROM SHA-256 | `06d1c2b06b716052c5596aaa0c2e5632a027fee1a9a28439e509f813c30829a9` |
| Total Manifest Candidates | `1138` |
| Exact `passNNN.json` Names | `919` |
| Non-exact Manifest Names | `81` |
| Duplicate Pass Identities | `38` |
| Exact Duplicate Ranges | `23` |
| Non-tail Overlaps | `131` |
| Strict JSON Parser Failures | `194` |
| Tracked Toolkit Archives | `6` |

## Key Findings

1. **Manifest Visibility**: 81 manifests use suffixed names (`pass1000_c3_session28.json` through `pass1229_c3_cb47.json`) and are ignored by legacy `passNNN.json` iterators, masking recent sessions 28–46.
2. **Duplicate Passes**: 38 pass numbers are shared by multiple manifest files in `passes/manifests/`.
3. **Range Collisions**: 154 strict warnings (23 exact duplicate ranges and 131 overlaps) require deterministic deconfliction.
4. **Artifact Encoding**: 194 JSON files fail strict UTF-8 decoding without BOM, including UTF-16, UTF-8 BOM, and mislabeled text/logs.
5. **Prohibited Binaries**: Commercial ROM `rom/Chrono Trigger (USA).sfc` is tracked in git index and must be untracked with clear local verification.
