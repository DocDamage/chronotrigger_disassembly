# Runbook: Coordinated Git History Cleanup (Phase 7B)

## Purpose
This runbook details the procedure for completely purging historical blobs (including prohibited commercial ROM binaries and redundant large archive blobs) from repository history using `git-filter-repo`.

> [!CAUTION]
> History rewriting alters all commit SHAs and disrupts active branches. It MUST NOT be performed casually and requires maintainer approval, team coordination, and a frozen maintenance window.

---

## 1. Pre-requisites & Approval Gate

Before executing history rewriting:
- [ ] Confirm maintainer sign-off on history cleanup window.
- [ ] Ensure all active work branches are merged or rebased onto canonical `live-work-from-pass166`.
- [ ] Create a full backup bundle of the repository:
  ```powershell
  git bundle create "../chrono_trigger_pre_rewrite_backup_$(Get-Date -Format 'yyyyMMdd').bundle" --all
  ```
- [ ] Verify the backup bundle integrity:
  ```powershell
  git bundle verify "../chrono_trigger_pre_rewrite_backup_$(Get-Date -Format 'yyyyMMdd').bundle"
  ```
- [ ] Install `git-filter-repo` (Python 3 tool):
  ```powershell
  pip install git-filter-repo
  ```

---

## 2. Dry Run on Mirror Clone

1. Clone a fresh mirror into an isolated temporary directory:
   ```powershell
   git clone --mirror "c:\dev\Chrono Trigger Disassembly" "$env:TEMP\ct_rewrite_mirror"
   cd "$env:TEMP\ct_rewrite_mirror"
   ```

2. Run `git-filter-repo` specifying paths and blob patterns to remove:
   ```powershell
   git-filter-repo --invert-paths `
     --path "rom/Chrono Trigger (USA).sfc" `
     --path-glob "*.sfc" `
     --path-glob "*.smc" `
     --path-glob "toolkits/**/*.zip" `
     --path-glob "emulators/*.zip" `
     --path-glob "tools/scripts/tools/cache/*" `
     --path-glob "**/raw_xref_index*.json"
   ```

3. Verify repository integrity and verify that prohibited blobs are unreachable:
   ```powershell
   git fsck --full --strict
   git rev-list --objects --all | Select-String -Pattern "\.sfc|\.smc|\.zip|raw_xref_index.*\.json"
   ```

4. Compare canonical source tree hashes between original and rewritten tips:
   ```powershell
   git log -n 5 --oneline
   ```

---

## 3. Production Execution & Collaborator Migration

1. Freeze upstream pushes and announce maintenance window.
2. Run filter on authoritative mirror or clean clone.
3. Force push updated canonical refs:
   ```powershell
   git push origin --force --all
   git push origin --force --tags
   ```
4. Collaborators MUST perform a clean clone rather than merging old history:
   ```powershell
   git clone <repo_url> "Chrono Trigger Disassembly Clean"
   ```

## Current authorization status

History rewriting has not been authorized or performed. The current tree is clean of ROMs, ZIP archives, and generated raw-xref caches, while the historical blobs remain reachable for recovery and audit until maintainers schedule the coordinated procedure above.
