# Toolkit Upgrade — Pass 161 / v6.8

## What changed

This refresh did more than patch one inspector bug.

### 1) Core low-bank HiROM mapping fix
- fixed the shared HiROM mapper so low-bank CPU ROM addresses like `C3:0000` and `C3:0557` map to the real payload offsets instead of being falsely rejected as unmapped
- fixed canonical `pc_to_hirom()` round-tripping so low-bank project addresses stay low-bank instead of being forced up into `$8000+`

### 2) Low-bank regression coverage
- added a new toolkit-doctor check that explicitly verifies:
  - `C3:0000 -> 0x030000`
  - `C3:0557 -> 0x030557`
  - reverse mapping back to `C3:0000` / `C3:0557`
- added a dedicated low-bank smoke-test lane so release smoke now inspects both:
  - the current live seam `C3:0077..C3:01E3`
  - a low-bank target `C3:0008..C3:0008`

### 3) Xref-facing refresh
- bumped xref cache resolution metadata to `bank_local_v3_lowbank_hirom`
- added low-bank `C3` hot targets that matter for the startup band:
  - `C3:0008`
  - `C3:000E`
  - `C3:0011`
  - `C3:0014`
  - `C3:0557`
- seeded cache entries for the proven live long-call veneers so the toolkit is not half-blind exactly where session 9 moved next

### 4) Completion-score hardening
- found and fixed another real toolkit problem: the packaged workspace could overstate completion badly because the score lane trusted a reduced label DB too much
- updated the score lane to use current synced state as a floor for label/pass totals, which keeps the packaged toolkit from hallucinating a fake ~93% completion number
- current honest packaged score after the fix: **69.8%**

### 5) Documentation / release surface refresh
- bumped the toolkit to **v6.8**
- updated README for the low-bank HiROM fix
- updated release-manifest notes so the release itself records the low-bank mapping and coverage upgrades
- refreshed the packaged release forward from pass 150 to pass 161

## Audit result
- toolkit doctor: **100.0%**
- smoke test: **100.0%**
- release audit: **100.0%**
- packaged zip: `ct_disasm_toolkit_v6_8_pass161_upgraded.zip`

## Current packaged state
- latest pass: **161**
- toolkit version: **v6.8**
- current live seam: **`C3:0077..C3:01E3`**
- honest completion estimate: **69.8%**

## What I checked beyond the original bug
I specifically audited more than the one low-bank inspect failure.

The additional surfaces that needed work were:
- the shared address-mapper layer, not just `ct_inspect_target.py`
- xref cache versioning and low-bank target coverage
- release smoke coverage
- doctor coverage
- the completion-score lane, which could otherwise lie about overall progress inside the refreshed package

## What still remains a future upgrade candidate
- deeper xref coverage for the whole low-bank `C3` startup/worker band beyond the newly seeded high-value targets
- more runtime-proof automation now that the project is entering the bank-head startup area
- broader generated-source expansion; the toolkit is healthier now, but the project is still far from rebuild-complete
