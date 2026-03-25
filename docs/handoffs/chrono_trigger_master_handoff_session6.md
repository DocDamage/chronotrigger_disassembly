# Chrono Trigger (USA) ROM Disassembly — Detailed Session 6 Handoff

## Purpose
This is the full handoff for the work completed after **session 5**, covering:
- disassembly progress from **pass 107** through **pass 119**
- the bank/header/xref toolkit correction pass
- the deeper maintenance upgrade that followed
- the exact current project state
- the honest remaining work before this can be called a **complete Chrono Trigger SNES ROM disassembly**

Use this handoff to answer three things fast:
1. **What got done in this session?**
2. **Where is the disassembly right now?**
3. **What is still required before the project is actually finished?**

This handoff is the direct follow-up to:
- `chrono_trigger_master_handoff_session5.md`
- `ct_disasm_toolkit_v6_deep_upgrade.zip`
- `ct_disasm_toolkit_v6_pass119_toolkit_patch_bank_header_guardrails.zip`
- `ct_disasm_toolkit_v6_pass119_deep_maintenance_upgrade.zip`
- `chrono_trigger_toolkit_update_after_pass119.md`
- `chrono_trigger_toolkit_deep_upgrade_after_pass119.md`

---

## Mandatory context before anyone continues
Same rule as session 5:
refresh on public Chrono Trigger research/modding context before pushing new claims.

Priority external context to refresh:
- Chrono Compendium
- Data Crystal
- Temporal Flux / Kajar Labs / old forum material
- bsnes / bsnes-plus / Geiger-style debugger workflows

Reason:
- prevents fake novelty
- prevents inventing subsystem names that already exist in community research
- keeps community shorthand separate from ROM-proof ownership

Community context is still **vocabulary support, not proof**.
Final labels, subsystem ownership, and rebuild claims still have to come from ROM evidence.

---

# 1) Session scope

## Start state
This session started from the end of session 5:
- latest pass: **106**
- best toolkit snapshot at start: **`ct_disasm_toolkit_v6_deep_upgrade.zip`**
- completion estimate at session start: **~68.9%**
- toolkit doctor health at start: **100.0%**
- active seam at start: **`FD:C1EE..C2C0`**, specifically the unresolved FD-side body behind the HDMA-shadow/materialization path

## End state
This session ended at:
- latest pass: **119**
- current best toolkit snapshot: **`ct_disasm_toolkit_v6_pass119_deep_maintenance_upgrade.zip`**
- current live subsystem anchor: **`C2:8820..C2:991F`**
- current toolkit doctor health score: **100.0%**
- current rebuild mode: **starter**
- current runtime evidence rows linked: **0**
- current canonical next seam: broader same-bank caller family around:
  - `C2:9DB9..9ED0`
  - `C2:A046..A0BA`
  - `C2:A886..`
  - `C2:B002`
  - `C2:BA32`
  - `C2:BEEF`

## Two score tracks that must not be conflated
This session ended with **two honest score readings**:

### A. Pass-119 narrative score
From `ct_completion_score_after_pass119.json`:
- Label semantics: **83.7%**
- Opcode coverage: **92.5%**
- Bank separation: **35.0%**
- Rebuild readiness: **35.4%**
- Overall completion: **70.8%**
- Banks represented in generated source: **15 / 66**
- Represented bank percent: **22.7%**
- Frozen/stable ranges: **562**
- Runtime-linked labels: **0**

### B. Rebuilt toolkit workspace score after bank/header/xref correction
From `chrono_trigger_toolkit_update_after_pass119.md`:
- latest pass synced: **119**
- overall completion in rebuilt workspace: **67.7%**
- xref cache resolution version: **bank_local_v2**
- ROM payload size: **0x400000**
- xref cache header size: **0x0**

### What the score discrepancy means
The project did **not** lose disassembly work.
The lower rebuilt-workspace score came from correcting tooling/state assumptions:
- header-aware mapping was enforced
- bank-local absolute `JSR/JMP` resolution was corrected
- stale state/report layers were rebuilt from the actual pass corpus

So the honest reading is:
- **structural progress improved** this session
- **tooling truthfulness also improved**
- the lower rebuilt score is a **measurement correction**, not a rollback of real closures

## The blunt truth
This session was productive and important, but it still did **not** finish the project.

It did five real things:
1. it closed the FD HDMA installer/builder seam instead of leaving it fuzzy
2. it pushed through the low-bank VRAM/HDMA commit and dispatch families
3. it mapped a large C0/C2 VM-driven settlement/search/materialization family far beyond where session 5 left it
4. it found and corrected a **real banking methodology bug** before it could poison more passes
5. it materially upgraded the toolkit so mapper/header/xref/state drift is much harder to miss

It did **not** solve the endgame.
The expensive remaining work is still:
- broad bank-by-bank code/data separation across the untouched ROM banks
- decompressor / data grammar ownership
- runtime-backed WRAM proof
- source-tree expansion into a truly rebuildable disassembly
- assembler integration and zero-diff ROM verification

---

# 2) What was accomplished in this session

This session did seven major things.

## A. It closed the FD-side HDMA finalizer/body seam instead of leaving it as a vague shadow helper
Passes **107–108** resolved the hardware-facing FD side of the display/HDMA cluster.

Main outcomes:
- `FD:C1EE..C2C0` froze as the exact eight-channel indirect-HDMA installer/finalizer body
- `0153.bit0` froze as the bundle-side selector in this family
- `0126` froze as a real three-way grammar selector
- `0127` tightened into the variable-template parameter byte
- the `CC58/CC5E/CCB2/CCB8` path froze as a chunked HDMA-entry emitter/helper
- the six `FD:C2C1` targets froze as a **double-buffered three-family HDMA table builder system**
- important negative closure: those builder bodies do **not** directly own `7E:0128`

Why it mattered:
- it stopped the FD HDMA path from staying a bluff-heavy seam
- it isolated the remaining `0128 / $420C` ownership hunt away from the wrong body

## B. It froze the low-bank commit tail and split the real VRAM update paths
Passes **109–111** corrected the low-bank side and then moved upstream honestly.

Main outcomes:
- `C0:AE2B..AE33` was corrected into a forced-blank shutdown/zero-HDFA-off loop, not the general owner path
- `C0:EC00..EC5D` froze as the exact PPU-shadow flush + `0128 -> $420C` commit tail
- `C0:EC74..ECA3` froze as the VRAM DMA helper
- `C0:ECA4..ECCB` froze as the OAM DMA helper
- `C0:ECCC..ED13` froze as the IRQ-side HBlank wait / force-blank / HDMA-off wrapper
- `C0:ED15..F058` froze as the CPU-side immediate VRAM patch dispatcher
- `FD:E022..E272` froze as the channel-7 VRAM DMA streamer over alternating descriptor halves
- `FD:DE98..E01D` froze as the script-driven builder that materializes `7E:05B0..05EB` and `7F:0400/0410`
- `C0:F05E..F16F` froze as the `63`-driven immediate-VRAM prelude with a real four-way band selector

Why it mattered:
- it separated shutdown/commit work from actual content-update work
- it turned the `63` family into a real control surface instead of anonymous prelude fog

## C. It froze the selector writer chain and the packed seed/slot persistence family
Passes **112–114** converted the `63/64/65/66` neighborhood into a clean VM-driven family.

Main outcomes:
- `C0:1AFB..1B18` froze as the path that saves the current selector into `66` and forces `63 = 4`
- `C0:1B1A..1B37` froze as the increment/decrement-with-wrap owner for `63`
- `64` and `65` froze as exact wrap bounds
- `66` froze as the saved pre-force selector byte
- VM opcodes `0xC0 / 0xC3 / 0xC4` froze as the exact two-byte shared initializer family through `C0:3674..36A8`
- the packed byte split was corrected and frozen exactly:
  - `65 = bits 0..1`
  - `64 = bits 2..3`
- overwrite/retire paths were frozen through `7F:0A00,X` and `7F:0A80,X`
- `0xBB / 0xC1 / 0xC2` froze as the one-byte mode `0 / 1 / 2` sibling family
- `C0:20F0..2126` froze as the first exact packet builder consuming `2A / 2B / 2D`

Why it mattered:
- it transformed an awkward local-byte cluster into an exact VM opcode family with real slot-state persistence and packet-building consequences

## D. It closed the fallback and converted the local working pair into a real signed candidate-offset system
Passes **115–117** pushed through the major local solver family.

Main outcomes:
- `C0:2E1E..2E65` froze as the forced-blank fixed-color hard-stop fallback used by invalid `2D == 0`
- `C0:88E5..88EC` froze as the handoff `2A -> 2E`, `2B -> 30`
- `C0:88ED..8A69` froze as a signed-step template-dispatch lane writing `2C/2D` and shifting `2E/30`
- `C0:8A6C..8A9D` froze as the first exact downstream reader of `30`
- the eight-way family collapsed into a mirrored search system:
  - X-only roots
  - Y-only roots
  - four full quadrant bodies
- `2E/30` upgraded from generic working bytes into the exact **signed candidate-offset pair** applied onto the current slot coordinate words
- `8820..991F` froze structurally as the exact DP=`$1D00` current-slot candidate-offset settlement/search pipeline
- stages inside that owner band were frozen for:
  - seed/refine
  - gate
  - nibble quantize / zero
  - six-lane signed accumulator build
  - phase / coarse-cell propagation and wrap-flag fanout

Why it mattered:
- this was one of the biggest subsystem-structure wins of the session
- it turned a foggy local search/materialization family into a concrete pipeline

## E. It mapped the bank-`C2` caller side instead of leaving the solver orphaned
Pass **118** carried the solved internal family out into real caller ownership.

Main outcomes:
- iterative current-slot settlement sweep with export/clamp behavior froze in bank `C2`
- selective accepted-slot list builder froze around:
  - `0F53`
  - `0F57..`
  - `0F5D`
- template-block commit/mirror helper froze around `C2:9137..916D`
- one-shot settlement-driven materialization wrapper froze in `C2:A22F..A26F`
- selector-driven staircase-and-block materializer froze in `C2:A273..A2C5`

Why it mattered:
- it proved the settlement/search pipeline had real owner-side use in bank `C2`
- it moved the project from “internal algorithm solved” toward “gameplay/system ownership solved”

## F. It caught and fixed a real bank-local xref bug before it could poison later work
Pass **119** was a methodology correction and a disassembly pass at the same time.

Main outcomes:
- the settlement/search owner band was corrected from:
  - wrong: `C0:8820..C0:991F`
  - right: `C2:8820..C2:991F`
- bank-local absolute `JSR $8820` callsites were reinterpreted correctly as same-bank hits
- the sibling `C2` caller cluster around `A1B2..A418` was then frozen honestly on top of the corrected banking model
- a dedicated caveat note was shipped so the wrong prefix would not silently persist

Why it mattered:
- this prevented a bank-resolution bug from poisoning later ownership claims
- it preserved most of the structural work from passes 115–118 while correcting the bank prefix and xref logic

## G. It materially upgraded the toolkit again instead of just carrying caveats by hand
This session did two toolkit upgrade waves after pass 119.

### Focused toolkit correction wave
Main outcomes:
- header-aware HiROM mapper support
- payload-vs-raw offset reporting
- bank-local absolute `JSR/JMP` resolution
- versioned xref cache rebuild logic
- cache freshness checks at resume time
- mapper/header/xref freshness doctor checks
- `ct_dump_range.py` support for `--end` and `--bank-relative`
- workspace state rebuilt from the shipped pass corpus

### Deep maintenance upgrade wave
Main outcomes:
- canonical next-session parser
- pass-artifact ingest lane
- stronger state sync
- doctor checks for generated-report freshness
- one-shot target inspector
- resume/bootstrap now starts with artifact ingestion
- README/tool manifest refresh

Why it mattered:
- the toolkit is now much harder to drift with
- it is much better at absorbing newly uploaded pass artifacts
- it can catch stale seam/report state before the next pass is built on top of it

---

# 3) Detailed pass-by-pass summary for this session

## Pass 107
Main upgrades:
- `FD:C1EE..C2C0` froze as the exact eight-channel indirect-HDMA installer/finalizer body
- `0153.bit0` froze as the local selector for channel-7 B-bus target byte `0x28` vs `0x29`
- negative closure: this body is not the direct `7E:0128` writer

Why it mattered:
- it closed the exact seam session 5 ended on and moved the hunt upstream honestly

## Pass 108
Main upgrades:
- the six `FD:C2C1` targets froze as a double-buffered three-family HDMA table builder system
- `0126` froze as a three-way grammar selector
- `0127` tightened into the variable-template parameter byte

Why it mattered:
- it converted the builder fog into real structure and proved `0128` ownership was elsewhere

## Pass 109
Main upgrades:
- low-bank seam around `AE2B/AE33` corrected into a shutdown loop
- `EC00..EC5D`, `EC74..ECA3`, `ECA4..ECCB`, and `ECCC..ED13` froze as exact commit/helper/wrapper bodies
- address-rendering caveat surfaced and documented

Why it mattered:
- it corrected a wrong lead before it could harden into fake ownership

## Pass 110
Main upgrades:
- `FD:FFFD` corrected into a bank-local veneer
- `C0:ED15..F058` froze as CPU-side immediate VRAM patch dispatcher
- `FD:E022..E272` froze as channel-7 VRAM DMA streamer

Why it mattered:
- it split two real VRAM update methods cleanly

## Pass 111
Main upgrades:
- `FD:FFFA -> FD:DE98` froze as the real script-driven descriptor builder path
- `C0:F05E..F16F` froze as the exact `63`-driven immediate-VRAM prelude
- `63` upgraded into an exact four-way band selector plus forced/reset behavior

Why it mattered:
- it moved the seam from update machinery into the real selector-control chain

## Pass 112
Main upgrades:
- writer-side control of `63` tightened through `1AFB..1B37`
- `64`, `65`, and `66` gained exact local roles
- wrap/increment/decrement behavior froze

Why it mattered:
- it stopped the selector family from remaining partially descriptive and made it operationally exact

## Pass 113
Main upgrades:
- VM opcodes `0xC0 / 0xC3 / 0xC4` froze as the two-byte packed-seed family
- packed split into `64/65` corrected exactly
- `66` persistence path froze through `7F:0A80,X`

Why it mattered:
- it tied the local selector family to exact opcode ownership instead of loose adjacency

## Pass 114
Main upgrades:
- `0xB8` froze as the exact loader for `2B / 2C / 2D`
- `0xBB / 0xC1 / 0xC2` froze as the one-byte sibling family
- `20F0..2126` froze as the first exact downstream packet builder consuming these locals

Why it mattered:
- it mapped the family split cleanly and exposed the first hard consumer edge

## Pass 115
Main upgrades:
- `2E1E..2E65` froze as the hard invalid-parameter fallback
- `88E5..8A9D` froze enough to upgrade `30` into a real downstream discriminator

Why it mattered:
- it clarified that the fallback was a real hard-stop and not a soft alternate mode

## Pass 116
Main upgrades:
- `8A9E..8AB4` froze as the shared candidate-validator entry
- `9923..99D9` froze as the shared nearby-slot rejection scan
- the eight-way branch family collapsed into a mirrored candidate-search system

Why it mattered:
- it converted a large branch forest into one coherent search family

## Pass 117
Main upgrades:
- `8820..991F` froze structurally as the current-slot candidate-offset settlement/search pipeline
- gating, quantization, signed-lane build, and propagation stages all gained exact structural roles

Why it mattered:
- it turned the solver from a collection of local closures into a real pipeline

## Pass 118
Main upgrades:
- bank-`C2` caller grammars froze for iterative sweep, accepted-slot list building, and one-shot materialization
- more owner-side variables and buffers gained exact local structural meaning

Why it mattered:
- it put the solver into caller context instead of leaving it isolated

## Pass 119
Main upgrades:
- banking/xref methodology bug was corrected
- settlement/search owner band moved correctly to `C2:8820..C2:991F`
- `C2:A1B2..A418` sibling caller cluster froze on top of the corrected bank model

Why it mattered:
- it saved the project from building later ownership claims on a wrong-bank assumption

---

# 4) Exact current state of the disassembly

## Current best toolkit snapshot
Use this as the primary workspace going forward:
- **`ct_disasm_toolkit_v6_pass119_deep_maintenance_upgrade.zip`**

This supersedes:
- `ct_disasm_toolkit_v6_deep_upgrade.zip`
- `ct_disasm_toolkit_v6_pass119_toolkit_patch_bank_header_guardrails.zip`

## Current canonical owner band to carry forward
Carry this wording forward exactly:

- `C2:8820..C2:991F` = exact DP=`$1D00` current-slot candidate-offset settlement/search pipeline
- `C2:A1B2..A1E8` = exact full-span linear settlement sweep with post-result twin tail dispatch
- `C2:A1EF..A215` = exact selector/threshold gate for the post-settlement tail family
- `C2:A2CE..A2EC` = exact one-shot settlement tail fanning into `A6F0` and `ED31`
- `C2:A321..A38A` = exact settlement-driven quad-block materializer with three-service fanout
- `C2:A38B..A418` = exact selector-indexed helper cluster behind `A321`

## Current hot banks / families that are genuinely advanced
These areas are now materially ahead of the rest of the ROM:
- `C0` low-bank VRAM/PPU/selector-control neighborhoods
- `C1` master opcode/selector coverage machinery
- `CC / CD / CF / D1 / FD` display/palette/interrupt/HDMA-linked neighborhoods
- `C2` current-slot settlement/search/materialization owner family
- `7E / 7F` shadow/state work tied to the above families

## What is explicitly not solved yet
Do **not** misread current progress as endgame readiness.
These remain unsolved or only partially solved:
- broad code/data separation outside the represented banks
- accurate ownership of many decompressor/data grammar families
- runtime-backed proof for the major WRAM state families
- assembler-ready source for the majority of banks
- linker/assembler pipeline producing a zero-diff rebuilt ROM
- comprehensive bank-local xref validation across the whole project, not just the fixed hot seam

---

# 5) Toolkit upgrades shipped in this session

This section is here so the next session does **not** lose track of the tool improvements.

## New tools added in this session

### `scripts/ct_handoff_parse.py`
Canonical next-session/handoff parser.
Parses latest pass and seam headings from varied note formats instead of relying on one brittle regex.

### `scripts/ct_ingest_pass_artifacts.py`
Pass-artifact ingestion tool.
Scans a directory of loose pass files, copies in missing/changed artifacts, refreshes canonical notes, and writes sync reports.

### `scripts/ct_inspect_target.py`
One-shot target inspector.
For a target like `C2:8820`, it shows:
- nearby ROM bytes
- overlapping labels
- nearby labels
- bank-correct xrefs
- pass/note mentions

## Existing tools that were materially upgraded in this session

### `scripts/ct_common.py`
Now enforces header-aware HiROM mapping and normalized SNES↔PC conversion.

### `scripts/ct_addr.py`
Now reports payload-vs-raw offsets correctly under the corrected mapper model.

### `scripts/ct_dump_range.py`
Now supports:
- `--end`
- `--bank-relative`
- corrected payload/raw address handling

### `scripts/ct_xrefs.py`
Now resolves absolute `JSR/JMP` targets bank-locally under 65816 rules instead of encouraging wrong cross-bank ownership.

### `scripts/ct_build_xref_cache.py`
Now versions and tags xref caches with mapper/header/xref metadata so stale cache logic is harder to carry forward silently.

### `scripts/ct_resume_workspace.py`
Now:
- checks xref freshness
- can ingest new pass artifacts before rebuild
- surfaces the new target inspector in the startup lane

### `scripts/ct_toolkit_doctor.py`
Now checks:
- mapper/header/xref freshness
- canonical next-session note freshness
- unresolved-dashboard freshness
- seam-priority-report freshness
- artifact-sync freshness

### `scripts/ct_sync_handoff_state.py`
Now uses canonical note parsing and records the exact note source used to derive live seam/state.

## High-value existing tools that remain central
These were not the new additions, but they remain core to continuation and should stay in the handoff:
- `scripts/ct_make_pass.py`
- `scripts/ct_make_report.py`
- `scripts/ct_build_label_db.py`
- `scripts/ct_generate_bank_sources.py`
- `scripts/ct_generate_bank_dossiers.py`
- `scripts/ct_generate_bank_workbooks.py`
- `scripts/ct_generate_unresolved_dashboard.py`
- `scripts/ct_generate_build_manifest.py`
- `scripts/ct_prioritize_seams.py`
- `scripts/ct_completion_score.py`
- `scripts/ct_score_history.py`
- `scripts/ct_runtime_capture_plan.py`
- `scripts/ct_runtime_link_report.py`
- `scripts/ct_import_runtime_evidence.py`
- `scripts/ct_rebuild_diff.py`
- `scripts/ct_label_diff.py`

## Reports and state outputs added or made newly important
- `reports/completion/ct_pass_artifact_sync.json`
- `reports/completion/ct_pass_artifact_sync.md`
- refreshed `state/current_state.json`
- refreshed `state/workspace_config.json`
- corrected `data/ct_hot_xref_cache.json`

## Recommended command lane going forward
```bash
python3 scripts/ct_ingest_pass_artifacts.py --root . --source-dir /path/to/new/pass/files
python3 scripts/ct_resume_workspace.py --workdir . --rom "Chrono Trigger (USA).sfc" --artifact-dir /path/to/new/pass/files
python3 scripts/ct_toolkit_doctor.py --root .
python3 scripts/ct_inspect_target.py C2:8820 --root . --rom "Chrono Trigger (USA).sfc"
python3 scripts/ct_xrefs.py C2:8820 --mode calls --bank C2 --rom "Chrono Trigger (USA).sfc"
python3 scripts/ct_dump_range.py C2:8820 --end C2:8830 --rom "Chrono Trigger (USA).sfc" --bank-relative
```

---

# 6) What still has to be done to finish the disassembly

This is the part that matters most.

## Immediate next technical seams
These are the best next pass targets because they continue directly from the corrected bank-`C2` owner band:

1. broader same-bank caller family:
   - `C2:9DB9..9ED0`
   - `C2:A046..A0BA`
   - `C2:A886..`
   - `C2:B002`
   - `C2:BA32`
   - `C2:BEEF`

2. caller-side noun hunt:
   identify the larger gameplay/system-facing family that owns:
   - `0D4D`
   - `0D5D`
   - `0077`
   - `5CC2..5CD8`
   - `5D42..5D58`

3. wording cleanup and bank correction propagation:
   - scrub any remaining `C0:8820..991F` wording and replace with `C2:8820..991F`
   - re-audit old xref-based notes for bank-local absolute call ambiguity

## Mid-stage static work still required
These are the next big static milestones after the hot seam continues:

### A. Broaden represented bank coverage
Current source representation is still only **15 / 66 banks**.
That is nowhere near enough for a finished disassembly.

Need:
- systematic bank-by-bank source expansion
- better code/data separation in untouched banks
- more exact label density outside the current hot neighborhoods

### B. Freeze more hardware/data grammar ownership
Still needed:
- decompressor families
- pointer-table grammars
- map/script/content materialization families outside the current C0/C2/CD/D1/FD pocket
- stronger ownership of data-only zones versus executable code

### C. Improve bank separation confidence
Bank separation is still only mid-30s.
That means there are still too many places where code/data boundaries and owner paths are not hard enough.

Need:
- more exact xref-backed caller ownership
- more verified pointer-table/data demotions
- fewer broad provisional labels left standing

### D. Finish service-wrapper and engine-family mapping
Current service-7 wrapper coverage is still **5 / 8**.
This is another sign the project is not yet system-complete.

Need:
- freeze the remaining wrapper/service families
- propagate those closures into the rebuild skeleton and manifests

## Runtime-backed proof still required
Right now runtime-linked labels are still **0**.
That is a major unfinished category.

Need:
- bsnes-plus or equivalent trace captures for:
  - the corrected `C2:8820..C2:991F` owner band
  - `7E:0128` HDMA shadow commit behavior
  - `63/64/65/66` selector family transitions
  - key CD/D1/FD display/palette/interrupt neighborhoods
- import traces through:
  - `ct_trace_normalize.py`
  - `ct_import_runtime_evidence.py`
  - `ct_runtime_link_report.py`
- then relabel or promote rows based on runtime-backed ownership instead of static-only inference where needed

## Rebuildability work still required
Current rebuild mode is still **starter**.
This project is not finished until the source tree crosses into real rebuild territory.

Need:
- broaden assembler skeleton beyond the currently represented banks
- keep bank source output in sync with corrected labels
- improve manifest completeness
- close more unresolved ranges before trying serious assembly validation
- run real rebuild-diff loops instead of only carrying a starter scaffold

## Final endgame required for a true “finished disassembly” claim
This project cannot honestly be called complete until all of the following exist:

1. a broad, bank-complete or near-bank-complete source tree
2. stable code/data separation across the ROM
3. high-confidence labels for the major engine/script/display/data families
4. runtime-backed proof on important WRAM/shadow/dispatch families
5. assembler integration that can emit a ROM image
6. zero-diff or explainably bounded-diff rebuild verification against the original ROM

Until those six are true, this is an advanced disassembly project in progress, not a completed full disassembly.

---

# 7) Carry-forward warnings

## Warning 1: Do not reopen the bank bug
Do **not** treat raw absolute `JSR $8820` hits in other banks as proof of cross-bank calls.
For this subsystem, the corrected owner band is:
- `C2:8820..C2:991F`

## Warning 2: Do not mix the two score tracks casually
If someone cites **70.8%**, that is the pass-119 narrative score.
If someone cites **67.7%**, that is the rebuilt toolkit workspace score after tooling/state correction.
Both are honest, but they describe different layers.

## Warning 3: Do not treat toolkit doctor health as disassembly completion
A **100.0% toolkit doctor health score** means the toolkit/workspace is internally healthy.
It does **not** mean the ROM disassembly is 100% done.

## Warning 4: Do not skip runtime evidence forever
Static work carried this session, but runtime-backed proof is still missing.
That gap becomes more important, not less, as subsystem nouns get stronger.

---

# 8) Recommended next-session start order

1. open the current toolkit:
   - `ct_disasm_toolkit_v6_pass119_deep_maintenance_upgrade.zip`

2. read these in order:
   - `chrono_trigger_master_handoff_session6.md`
   - `chrono_trigger_next_session_start_here_pass119.md`
   - `chrono_trigger_toolkit_update_after_pass119.md`
   - `chrono_trigger_toolkit_deep_upgrade_after_pass119.md`

3. resume the workspace with doctor checks enabled

4. inspect the corrected owner band first:
   - `C2:8820`
   - `C2:A1B2`
   - `C2:A321`

5. continue into the broader same-bank caller family:
   - `C2:9DB9..9ED0`
   - `C2:A046..A0BA`
   - `C2:A886..`
   - `C2:B002`
   - `C2:BA32`
   - `C2:BEEF`

6. only after that, decide whether the next best move is:
   - more caller-family closure
   - runtime trace capture on the corrected owner band
   - broader bank-expansion work elsewhere

---

# 9) Final blunt status

This session was a **real advance**.
It did not just add labels.
It:
- materially improved the static disassembly
- materially improved subsystem ownership
- materially improved the toolkit
- corrected a real methodology bug before it contaminated more work

But the project is still **far from finished**.

The honest state now is:
- one more major subsystem family is much better understood than before
- the toolkit is much safer and cleaner than before
- the next seam is clear
- the endgame is still big, expensive, and unfinished

