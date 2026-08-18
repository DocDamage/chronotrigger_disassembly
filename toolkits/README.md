# Toolkit Archives and Release Policy

This directory documents historical toolkit releases. Generated ZIP snapshots were removed from the current Git tree under the repository binary policy.

## Retention Policy

- **Active Tooling**: Active tools live in `tools/` and `tools/ctrepo/`.
- **Releases**: Distribution bundles should be generated reproducibly from Git tags via release automation (`tools/scripts/package_repo_toolkit_release_v1.py`) and attached to GitHub Releases rather than tracked in the main Git tree.
- **Historical Snapshots**: The removed archives are inventoried by SHA-256 in `reports/remediation/binary_archive_disposition.json` and remain recoverable from commit `cfd7d54a7a3dbfd7e7089fa976dee998fdf62d75` until separately authorized history cleanup occurs.
