# Chrono Trigger (USA) ROM Disassembly — Detailed Session 5 Handoff

## Purpose
This is the full handoff for the work completed after **session 4**, covering:
- disassembly progress from **pass 97** through **pass 106**
- the focused toolkit-upgrade pass
- the deeper **v6** toolkit upgrade
- the exact current project state
- the honest remaining work before this can be called a **complete Chrono Trigger SNES ROM disassembly**

Use this handoff to answer three things fast:
1. **What got done in this session?**
2. **Where is the disassembly right now?**
3. **What is still required before the project is actually finished?**

This handoff is the direct follow-up to:
- `3-23-26-1126pm-chrono_trigger_master_handoff_session4.md`
- `ct_disasm_toolkit_v5_updated_pass96_runtime_evidence_refresh.zip`
- `ct_disasm_toolkit_v6_deep_upgrade.zip`
- `chrono_trigger_toolkit_v6_deep_upgrade_summary.md`

---

## Mandatory context before anyone continues
Same rule as session 4:
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
This session started from the end of session 4:
- latest pass: **96**
- best toolkit snapshot at start: **`ct_disasm_toolkit_v5_updated_pass96_runtime_evidence_refresh.zip`**
- completion estimate at session start: **~68.2%**
- the freshly closed hot seam was the low-bank `C7` sound/APU packet path
- the next unresolved seam was back on the `CE0F / CDC8 / CFFF` side and its downstream D1/CD/FD control families

## End state
This session ended at:
- latest pass: **106**
- current best toolkit snapshot: **`ct_disasm_toolkit_v6_deep_upgrade.zip`**
- current canonical completion estimate: **~68.9%**
- current toolkit health score: **100.0%**
- current rebuild mode: **starter**
- current runtime evidence rows linked: **0**
- current live seam: **`FD:C1EE..C2C0`**, specifically the remaining FD-side body behind the HDMA-shadow/materialization path

## Current canonical score breakdown
From the canonical score source `reports/completion/ct_completion_score.json` in the v6 toolkit:
- Label semantics: **78.4%**
- Opcode coverage: **92.5%**
- Bank separation: **38.1%**
- Rebuild readiness: **35.6%**
- Overall completion: **68.9%**

## Current coverage/state counts
- Master C1 opcodes: **170 / 170**
- Selector-control bytes: **83 / 83**
- Service-7 wrappers: **5 / 8**
- Banks represented in generated source: **15 / 66**
- Represented bank percent: **22.7%**
- Frozen/stable ranges: **504**
- Total label rows: **754**
- Strong labels: **532**
- Provisional labels: **148**
- Alias labels: **1**
- Caution labels: **5**
- Current non-strong rows: **200**
- Runtime evidence rows: **0**
- Runtime-linked labels: **0**

## The blunt truth
This session was productive, but it did **not** finish the project.

It did four real things:
1. it closed the post-pass-96 control/palette/trampoline seam much further than before
2. it turned the D1/CD/C0/FD neighborhood into a much cleaner palette + interrupt + HDMA control cluster
3. it upgraded the toolkit from “good enough to continue” to “actually self-auditing and much harder to drift with”
4. it improved the project’s ability to continue cleanly

It did **not** solve the endgame.
The expensive remaining work is still:
- broad bank-by-bank code/data separation across the untouched ROM banks
- decompressor / data grammar ownership
- runtime-backed WRAM proof
- source-tree expansion into a truly rebuildable disassembly
- assembler integration and zero-diff ROM verification

---

# 2) What was accomplished in this session

This session did six major things.

## A. It finished the warm C7 bridge seam instead of leaving it half-exact
Pass **97** closed the low-bank bridge around `C7:0155`, `C7:071D`, and `C7:0A98`.

Main outcomes:
- `C7:0155..0191` froze as a real shared **post-prologue redispatch entry**
- `C7:071D..0733` froze as an exact **rewrite + redispatch** path for `0x30..0x3F`
- `C7:0A98..0AD7` froze as the exact synthetic `{0x10, selector, 0xFF, 0xFF}` rewrite table
- `C7:061C..064F` was corrected into the broader negative-header + direct-immediate sender path

Why it mattered:
- it stopped the late C7 sound/APU bridge from staying fuzzy at exactly the point where the immediate-family split mattered most

## B. It killed a bad `CE0F` lead instead of building on a false reader
Pass **98** did something small but important: it killed the fake `CD:BEF8` direct-reader lead.

Main outcomes:
- `CD:BEF8` was demoted as dense pointer-table-backed data, not clean CPU code
- the only honest mapped direct `$CE0F` uses left standing were the D1 write-side hits
- the adjacent D1 controller at `D1:EB70..EBCF` was promoted instead of forcing a bad noun from fake code

Why it mattered:
- it made the `CE0F` seam more honest
- it prevented a bad reader claim from poisoning later labels

## C. It turned the D1 post-controller tail into a real palette/phase/materialization path
Passes **99–100** materially upgraded the D1 control pocket.

Main outcomes:
- `CDC9` froze as a real local **phase/match index**
- `D1:EA21..EA4A` froze as three exact 14-entry circular phase tables
- `D1:EB00..EB1C` froze as duplication of `CDCC..CDE7` into `CDE8..CE03`
- `D1:EB1D..EB4B` froze as a three-window phase materializer
- `D1:EBDF..EBFF` froze as a 14-word window copier into the paired palette bands
- `D1:EA5F..EAF4` froze as a per-channel **SNES BGR555 palette convergence/tween loop**
- `D0:FBE2..` tightened into the base + selectable palette-profile family

Why it mattered:
- this was the point where the old “profile math / selector fog” finally became a real **palette transition / palette window** system

## D. It anchored that D1 palette-maintenance path back to clean CD-side owners
Passes **101–104** pulled the D1 work back into its real caller chain.

Main outcomes:
- `D1:EB4C..EB6F` was demoted to dead-output timing / cycle-burn work instead of hidden selector logic
- the first clean external caller anchor for `D1:EA4B` froze in `CD:8978..89CB`
- `CE13` froze as the local mask that suppresses `D1:EA4B` when `7C & CE13 != 0`
- `CD2D`, `CD2E`, and `CD29` got exact clean-code consumer roles
- `CD:3B82..3BA5` froze as a raster/beam wait helper
- `CD:0DB1..0DFF` froze as the owner-side transition/drain/quiescence helper family
- `CE13 = 0x03` and `CE0E = 0x80` were proven as owner-side transition inputs
- `CD:83EE..840C` froze as the chooser above `0D93` vs `0DB1`
- `CD:840D..8449` froze as the wrapper around the installed RAM-trampoline/NMI path
- `CD:044A..0452` froze as a one-cycle RAM-trampoline/NMI wait helper through `$47`

Why it mattered:
- it turned “caller neighborhood” into a real owner-side launch chain feeding the D1 palette maintenance path

## E. It froze the installed D1 RAM NMI trampoline and the HDMA-shadow producer edge
Passes **105–106** were the biggest hardware-facing upgrade of the session.

Main outcomes:
- `D1:F4C0..F55A` froze as the installed **RAM NMI trampoline body**
- `$45 -> $2100` froze as the `INIDISP` flush path
- `7E:2C70..2C7B` froze as the BG scroll-shadow byte band flushed to `$210D..$2112`
- `C0:0005 -> C0:0AFF` froze as the helper edge returning the current **HDMA enable shadow**
- `7E:0128` froze as the low-bank / FD-side **HDMA enable shadow byte**
- `FD:C2C1..C2DF` froze as an exact two-table local dispatcher keyed by `0153.bit0` and indexed by `0126`
- `C0:0B2B..0B50` froze as a startup sibling proving the same FD helper family lives in a real display / interrupt / HDMA control neighborhood

Why it mattered:
- the installed NMI trampoline is no longer a hazy interrupt blob
- the `$420C` write inside it now has a real producer edge
- the active seam is now properly isolated down to the remaining FD-side body instead of a huge multi-bank fog bank

## F. It materially upgraded the toolkit instead of just adding more notes
This session did two toolkit passes:
- **focused toolkit upgrade pass 1**
- **deep toolkit v6 upgrade**

Main outcomes:
- canonical score / handoff / state sync
- runtime trace normalization and live-seam-aware runtime capture planning
- runtime evidence linking reports
- seam prioritization report
- toolkit doctor/self-audit
- score history
- stronger rebuild manifest/stub path
- broken script repair (`ct_label_diff.py`)
- cleaner workspace root naming tied to pass 106

Why it mattered:
- the toolkit is now much less likely to drift, lie, or silently rot between passes
- it is still not a fully assembler-driven rebuild system, but it is a materially better continuation environment than the pass-96 toolset

---

# 3) Detailed pass-by-pass summary for this session

## Pass 97
Main upgrades:
- `C7:0155` froze as the shared redispatch entry under the negative-`1E05` gate
- `C7:071D` froze as the exact `0x30..0x3F -> 0x10 selector FF FF` bridge
- `C7:0A98` froze as the 16-entry rewrite table
- `C7:061C` was corrected into the broader shared immediate sender

Why it mattered:
- it closed the warm C7 immediate-family bridge cleanly before moving away from the sound/APU seam

## Pass 98
Main upgrades:
- killed the fake `CD:BEF8` `CE0F` reader lead
- kept only the honest direct `$CE0F` write-side hits
- froze `D1:EB70..EBCF` as the neighboring selector/profile controller
- froze `D1:EBD0..EBDE` as the `CE10`-gated direct-vs-mirrored helper

Why it mattered:
- this was a cleanup pass that removed bad confidence from the `CE0F` seam

## Pass 99
Main upgrades:
- `CDC9` froze as a real local phase/match index byte
- `D1:EA21..EA4A` froze as three exact circular phase-offset tables
- `D1:EB00..EB1C` froze as duplication of the active 14-word profile into a doubled ring
- `D1:EB1D..EB4B` froze as the three-window phase materializer
- `D1:EBDF..EBFF` froze as the 14-word window copier from the doubled ring into `20A2/22A2`

Why it mattered:
- this turned the post-controller D1 tail into a real materialization path instead of helper soup

## Pass 100
Main upgrades:
- `D1:EA4B..EA5E` froze as the top-level guard wrapper
- `D1:EA5F..EAF4` froze as the BGR555 palette convergence loop
- `D0:FBE2..` tightened as the palette-profile source family
- `CE0A / CE0B / CE0C / CE0D` sharpened as the palette-transition control bytes

Why it mattered:
- it proved the D1 cluster was palette logic, not generic profile math

## Pass 101
Main upgrades:
- `D1:EB4C..EB6F` was demoted to dead-output timing work
- first clean external caller anchor for `D1:EA4B` froze at `CD:8978..89CB`

Why it mattered:
- it ended pointless babysitting of the dead-output seam and shifted the work into the real caller chain

## Pass 102
Main upgrades:
- `CD:8978..89CB` froze as an exact staged tail driver
- `CE13` froze as the suppressor mask on the palette-maintenance call
- `CD2D`, `CD2E`, `CD29`, and `CD:3B82..3BA5` all tightened materially

Why it mattered:
- it gave the palette-maintenance path a real clean CD-side tail driver

## Pass 103
Main upgrades:
- `CD:0D62..0D92` froze as a fixed `C7:0004` prelude + reinit helper
- `CD:0D93..0DB0` froze as a blocking selector-`0x87` launcher
- `CD:0DB1..0DD7` froze as the owner-side transition helper that seeds `CE13 = 0x03` and `CE0E = 0x80`
- `CD:0DD8..0DFF` froze as the shared drain/quiescence loop
- `CD:0E05..0E22` froze as the blocking selector-driven sibling of `CD:0D28`

Why it mattered:
- it made the owner-side launch/drain path exact instead of semi-descriptive

## Pass 104
Main upgrades:
- `CD:83EE..840C` froze as the chooser above `0D93` vs `0DB1`
- `CD:840D..8449` froze as the wrapper around `0501/0503 = D1:F4C0` and `C0:000B`
- `CD:044A..0452` froze as the one-cycle wait helper through `$47`

Why it mattered:
- it made the RAM-trampoline launch path exact enough to follow into D1 cleanly

## Pass 105
Main upgrades:
- `D1:F4C0..F55A` froze as the installed RAM NMI trampoline body
- `$45 -> $2100` froze as the `INIDISP` flush
- `7E:2C70..2C7B` froze as the scroll-shadow band flushed to the BG scroll registers
- `C0:0005..0007` froze as a veneer into `C0:0AFF`

Why it mattered:
- it turned the installed interrupt body into a real named hardware-facing subsystem edge

## Pass 106
Main upgrades:
- `C0:0AFF..0B27` froze exactly enough to prove the returned byte is `7E:0128`
- `7E:0128` froze as the HDMA enable shadow byte
- `FD:C2C1..C2DF` froze as the exact two-table dispatcher keyed by `0153.bit0` and indexed by `0126`
- `C0:0B2B..0B50` froze as the startup sibling that reuses the same family before enabling NMI

Why it mattered:
- it isolated the remaining live seam to `FD:C1EE..C2C0`
- it proved the `$420C` write in the installed trampoline has a real local producer edge

## Toolkit upgrade — focused pass 1
Main upgrades:
- consistency lock between pass/seam/score state
- runtime evidence linking
- code-vs-data scoring improvement
- starter rebuild-lane improvements

Why it mattered:
- it stopped score drift and made runtime evidence usable as a normal continuation tool

## Toolkit upgrade — v6 deep upgrade
Main upgrades:
- stronger workspace/state sync
- runtime trace normalization and seam-aware capture plans
- score history
- toolkit doctor
- seam priority report
- stronger rebuild manifest/stub
- workspace hygiene and broken-script repair

Why it mattered:
- it materially improved the toolkit’s trustworthiness and continuation quality

---

# 4) Where the disassembly stands right now

## Current best high-level state
The project is meaningfully stronger than it was at the end of session 4.

The strongest subsystem-level truths now are:
- `C7` low-bank packet machinery is a real staged **sound/APU command pipeline**
- the `D1` post-controller cluster is a real **palette transition / palette window materialization** system
- the `CD` caller/owner side above that D1 path is a real **launch / suppress / drain / quiesce** chain
- `D1:F4C0` is the installed **RAM NMI trampoline**
- `C0:0005 -> C0:0AFF -> FD:C2C1 / FD:C1EE` is now the active **HDMA-shadow/materialization** edge behind the trampoline’s `$420C` write

That is real progress.

## Current live seam
The cleanest next disassembly seam is still:
- **`FD:C1EE..C2C0`**

Exact open questions on that seam:
- what pointer/table family it seeds
- how it finalizes or materializes `7E:0128`
- whether `7E:0153` and `7E:0126` are true wider mode/state bytes or only local helper-family selectors

## Current important unresolved labels/bytes
These are the most relevant unresolved or caution-level items near the current seam:
- `7E:0153` — exact local bit contracts are known, but broader subsystem noun is still cautious
- `7E:0126` — exact local table-index role is known, broader noun still open
- `7E:CE0F` — still no frozen clean direct static reader; still caution-level globally
- some late WRAM hotspots remain provisional or caution-level and need runtime proof, not more blind renaming

## Current toolkit state
The v6 toolkit is materially better than the pass-96 toolset.

Current truths:
- toolkit doctor health: **100.0%**
- rebuild mode: **starter**
- runtime evidence rows: **0**
- runtime-linked labels: **0**
- canonical score source now exists and is synchronized
- seam-priority and runtime-capture reports now exist

Current limitation:
- the toolkit does **not** magically create runtime proof or a rebuilt ROM by itself
- it is better prepared for those jobs, but those jobs still need to be done

---

# 5) Everything still needed to be completely done

This section is the honest completion definition.
The project is **not complete** when the labels feel nice.
It is complete only when the ROM can be explained, lifted, and rebuilt with credible proof.

## A. Finish the active FD helper family
Before going broad again, the current seam still needs closure:
- freeze `FD:C1EE..C2C0`
- pin the exact role of `0126`
- pin the exact broader role of `0153`
- confirm how `0128` is finalized or committed on the FD side

This is the first next job.

## B. Close the remaining hot subsystem-level seams
After the active seam, the remaining late-stage subsystem closures still include:
- a real clean global reader/owner path for `CE0F`
- final ownership boundaries around the D1 palette family and its wider caller neighborhoods
- any remaining weak owner boundaries on the C7/APU side
- unresolved battle/tail/occupant-map families that still sit high in seam-priority reports

## C. Do broad bank-by-bank code/data separation across the untouched ROM
This is still one of the biggest unfinished categories.

Right now only **15 / 66** banks are represented in generated source.
That means the majority of the ROM still needs:
- honest code vs data classification
- pointer-table ownership
- bank dossiers / workbooks
- stable labels instead of raw address islands
- cross-bank call / table boundaries frozen cleanly

Until this happens, the project is still a partially lifted disassembly, not a complete one.

## D. Finish data grammar / decompressor / format ownership
This is another huge unfinished category.

Still required:
- decompressor family identification and proof
- compressed blob grammar ownership
- graphics/tilemap/script/battle/data stream format boundaries
- exact ownership of table-driven data families vs executable code
- proof around any banked resource loaders and materializers

Without this, large parts of the ROM may be named but not truly understood.

## E. Add runtime-backed proof where static naming is no longer enough
Runtime rows are still **0**.
That means the toolkit is ready for runtime evidence, but the project itself does not yet have that proof imported.

Still required runtime campaigns include:
- active seam capture for `FD:C1EE..C2C0`
- D1 installed NMI trampoline capture
- C7 low-bank sound/APU seam capture
- `CDC8 / CE0F / CFFF` runtime capture
- WRAM hotspot validation passes

Why this matters:
- some WRAM nouns are now strong enough statically
- some are not
- the late-stage WRAM/control bytes will need debugger-backed proof to promote safely

## F. Expand the source tree from scaffold-first to real disassembly coverage
Current source state is still scaffold-first.
It needs to grow into a real source tree with:
- substantially more banks represented
- cleaner macro/include structure
- stable ownership of tables and data blobs
- safer separation of frozen vs provisional regions
- enough source coverage to support actual assembly attempts

## G. Build a real assembler loop
Current rebuild mode is only **starter**.
That means:
- no rebuilt ROM has been emitted yet
- no compare mode is active yet
- no byte-diff against a real assembled ROM exists yet

Still required:
- wire a real assembler into the build manifest/stub path
- emit a rebuilt ROM
- compare rebuilt ROM vs original ROM
- iterate until diffs are explainable or gone

## H. Reach compare mode, then match mode
A complete disassembly is not just “lots of labels.”
It needs:
- **compare mode**: original and rebuilt ROMs both exist and diff cleanly enough to inspect
- **match mode**: zero diffs across equal-size ROMs or fully explained, deliberately transformed diffs if the project defines another standard

For a strict preservation-grade disassembly, the real target is still:
- **byte-accurate rebuild parity**

## I. Final documentation and project packaging
Before calling the project complete, it still needs:
- final subsystem summaries by bank/family
- final build instructions
- final runtime-proof documentation where used
- final unresolved list reduced to zero or explicitly waived
- a clean release-grade toolkit/workspace snapshot

---

# 6) What “done” should mean for this project

To avoid fake finish lines, use this standard:

The disassembly is only honestly complete when all of these are true:
1. all meaningful executable banks and major data families are classified and owned
2. major WRAM control families have either static proof or runtime-backed proof
3. decompressor/data grammars are understood well enough to rebuild resources safely
4. source coverage is broad enough to assemble the ROM
5. assembler integration exists and produces a rebuilt ROM
6. rebuilt ROM matches the original ROM byte-for-byte, or every deviation is explicitly intentional and documented
7. remaining caution/provisional labels are reduced to near-zero or zero

Anything less than that is progress, not completion.

---

# 7) Best next move

Do **not** jump randomly.
The right next move is still:
- stay on **`FD:C1EE..C2C0`**
- freeze the FD-side materialization/finalization body behind the HDMA-shadow path
- use runtime capture immediately if the static seam stops yielding honest nouns

Recommended immediate order:
1. static pass on `FD:C1EE..C2C0`
2. if the wider noun of `0153` or `0126` still stalls, run the active runtime-capture plan for that seam
3. only then widen back out to the next unresolved control-byte or bank-separation seam

---

# 8) Files that matter most right now

## Best toolkit snapshot
- `ct_disasm_toolkit_v6_deep_upgrade.zip`

## This session’s disassembly passes
- `chrono_trigger_disasm_pass97.md`
- `chrono_trigger_disasm_pass98.md`
- `chrono_trigger_disasm_pass99.md`
- `chrono_trigger_disasm_pass100.md`
- `chrono_trigger_disasm_pass101.md`
- `chrono_trigger_disasm_pass102.md`
- `chrono_trigger_disasm_pass103.md`
- `chrono_trigger_disasm_pass104.md`
- `chrono_trigger_disasm_pass105.md`
- `chrono_trigger_disasm_pass106.md`

## Toolkit summaries
- `chrono_trigger_toolkit_upgrade_pass1_summary.md`
- `chrono_trigger_toolkit_v6_deep_upgrade_summary.md`

## Best internal toolkit reports in v6
- `reports/completion/ct_completion_score.json`
- `reports/completion/ct_consistency_report.md`
- `reports/ct_workspace_report.md`
- `reports/ct_seam_priority.md`
- `reports/runtime/runtime_capture_plan.md`
- `reports/ct_toolkit_doctor.md`
- `reports/ct_rebuild_diff_report.md`
- `notes/next_session_start_here.md`

---

# 9) Bottom line

Compared to the end of session 4, the project is now in a better place.

The good news:
- the late D1/CD/C0/FD seam is much tighter
- the installed RAM NMI trampoline is no longer vague
- the HDMA-shadow producer edge is now isolated
- the toolkit is materially stronger and more trustworthy

The bad news:
- the project is still only around **68.9%** complete by the current weighted model
- runtime proof is still **not imported yet**
- rebuild is still only in **starter** mode
- most banks are still not represented in source
- full completion still requires a lot more than another handful of local-label passes

That is the honest state.
