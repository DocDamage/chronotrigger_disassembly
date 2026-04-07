# `reports/` Status

This directory is the active generated-artifact lane for seam work.

Typical current outputs:
- `*_seam_block.json` and `*_seam_block.md`
- `*_backtrack.json`
- `*_flow.json`
- `*_anchor.json`
- toolkit release manifests

Working rule:
- current reports here mix historical seam evidence with newer repo-native generated artifacts
- older files in this directory are still useful evidence, but the current frontier should be taken from `README.md` and the latest manifest-backed work

Current frontier:
- current manifest-backed frontier: `C0:7800..`
- latest toolkit release manifest: `reports/toolkit_release_manifest_pass306_note100.md`

Use this directory together with:
- `README.md`
- `docs/session_23_progress_report.md`
- `passes/manifests/`
- older C7 handoffs / continuation notes only when that historical seam is relevant
