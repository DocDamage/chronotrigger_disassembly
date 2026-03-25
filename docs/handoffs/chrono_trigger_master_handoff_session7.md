# Chrono Trigger (USA) ROM Disassembly — Detailed Session 7 Handoff

## Purpose
This is the full handoff for the work completed after **session 6**, covering:
- disassembly progress from **pass 120** through **pass 139**
- the toolkit hardening and maintenance work that happened after pass 119
- the exact current project state
- the honest remaining work before this can be called a **complete Chrono Trigger SNES ROM disassembly**

Use this handoff to answer three things fast:
1. **What got done in this session?**
2. **Where is the disassembly right now?**
3. **What is still required before the project is actually finished?**

This handoff is the direct follow-up to:
- `chrono_trigger_master_handoff_session6.md`
- `ct_disasm_toolkit_v6_pass119_deep_maintenance_upgrade.zip`
- `chrono_trigger_toolkit_deep_upgrade_after_pass119.md`

---

## Mandatory context before anyone continues
Same rule as session 6:
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
This session started from the end of session 6:
- latest pass: **119**
- current best toolkit snapshot at start: **`ct_disasm_toolkit_v6_pass119_deep_maintenance_upgrade.zip`**
- current live subsystem anchor at start: **`C2:8820..C2:991F`**
- completion estimate at start: roughly **high-60s / low-70s depending on report layer**
- toolkit doctor health at start: **100.0%**

## End state
This session ends at:
- latest pass: **139**
- current best toolkit snapshot: **`ct_disasm_toolkit_v6_pass139_continued.zip`**
- current completion estimate: **69.7%**
- label rows: **1111**
- strong labels: **822**
- caution labels: **51**
- toolkit doctor health score: **100.0%**
- current canonical next seam: **`C2:DE98..C2:DF76`**

## The blunt truth
This session was productive and real, but it still did **not** finish the project.

It did five important things:
1. it pushed the C2-side caller / refresh / export / materializer family from the session-6 anchor well downstream through pass 139
2. it corrected several false seam boundaries where the old seam stopped in the middle of live code or data
3. it kept converting fuzzy local byte clusters into exact owners, helpers, local packet descriptors, and local tables
4. it hardened the toolkit so stale session notes / stale seam packets are much harder to miss
5. it left the project in a healthier, more honest state than it started

It did **not** solve the endgame.
The expensive remaining work is still:
- broad bank-by-bank code/data separation across untouched ROM regions
- decompressor / data grammar ownership
- runtime-backed WRAM proof
- source-tree expansion into a truly rebuildable disassembly
- assembler integration and bounded-diff / zero-diff ROM verification

---

# 2) Toolkit work completed this session

The toolkit was not left static after pass 119. The maintenance upgrade and this session’s usage proved out a stronger workflow.

## Major toolkit hardening now in place

### A. Canonical next-session parser
Added:
- `scripts/ct_handoff_parse.py`

What it fixed:
- stale seam extraction caused by brittle markdown parsing
- dependence on one exact heading format

### B. Pass-artifact ingest lane
Added:
- `scripts/ct_ingest_pass_artifacts.py`

What it fixed:
- loose pass artifacts living outside the workspace
- canonical note files drifting behind the newest pass files

### C. Stronger handoff/state sync
Updated:
- `scripts/ct_sync_handoff_state.py`

What it fixed:
- workspace state drifting away from actual pass artifacts
- unclear origin of the live seam note

### D. Stronger doctor checks
Updated:
- `scripts/ct_toolkit_doctor.py`

What it fixed:
- stale canonical next-session note
- stale unresolved dashboard / seam-priority reports
- missing pass-artifact freshness checks

### E. Target inspector CLI
Added:
- `scripts/ct_inspect_target.py`

What it added:
- one-shot inspection of raw bytes, overlapping labels, nearby labels, xrefs, and note mentions for a target seam

### F. Resume/bootstrap ingest-first behavior
Updated:
- `scripts/ct_resume_workspace.py`

What it fixed:
- resuming from a workspace that had newer pass artifacts available but not yet absorbed

## Practical effect
The toolkit is now materially better at:
- staying synchronized with the latest pass
- catching report drift early
- inspecting hot targets faster
- absorbing future pass artifacts without manual cleanup

---

# 3) What was accomplished in this session

## Important honesty note about detail level
This session advanced the project from **pass 119** to **pass 139**.

The exact per-pass artifacts still preserved in the current downloadable set begin at the later portion of this run, especially **passes 131–139**. Earlier session work between **passes 120–130** is reflected in the improved end-state, but this handoff does **not** invent exact pass-by-pass claims that are not preserved in the current artifact chain.

So the summary below is split into:
- the **session-wide net result**
- the **exact later-pass closures we can state precisely**

## Session-wide net result
Across this session, the disassembly pushed much deeper into the C2-side refresh / build / export / materialization families downstream of the already-frozen `C2:8820..C2:991F` anchor.

The core pattern of progress was:
- identify a seam
- discover the seam boundary was too short or too fuzzy
- widen it to the real owner/helper/data family
- freeze exact local tables / descriptor packets / wrappers
- move the next seam further downstream

That happened repeatedly through passes 131–139.

## Exact later-pass closures completed this session

### Pass 131
Closed:
- `C2:CED2..C2:CFFB`
- callback entry stub
- local 4-word dispatch table
- bit-6 OR gate owner
- `0D1D`-gated dispatcher
- local selector descriptor packet
- immediate packet emitter / overflow jump tail
- sibling `0D1D`-gated owner
- `0D9B` decrementing wrapper
- state-refresh / strip-expansion owner
- callable block/template initializer

Net effect:
- moved the real next seam to `C2:D065..C2:D0C5` and clarified that the preceding family was fully real code, not spillover.

### Pass 132
Closed:
- `C2:D065..C2:D0DD`
- `C2:D0DE..C2:D0E4`
- `C2:D0E5..C2:D10C`
- `C2:D10D..C2:D130`
- `C2:D131..C2:D155`
- `C2:D156..C2:D197`
- `C2:D198..C2:D19E`

Net effect:
- corrected the false seam end at `D0C5`
- exposed the real 3-pass source-page / window driver chain
- froze an externally-callable 3-slot poll/service owner

### Pass 133
Closed:
- `C2:D19F..C2:D265`
- `C2:D266..C2:D28C`
- `C2:D28D..C2:D295`
- `C2:D296..C2:D305`
- `C2:D306..C2:D328`
- `C2:D329..C2:D32B`
- `C2:D32C..C2:D36B`

Net effect:
- resolved the next seam into a 3-row template/export owner
- froze the per-slot threshold/setup helper family
- froze a real externally-callable `0D8C` refresh owner

### Pass 134
Closed:
- `C2:D36C..C2:D45E`
- `C2:D45F..C2:D465`
- `C2:D466..C2:D4B3`
- `C2:D4B4..C2:D4BB`
- `C2:D4BC..C2:D4D4`
- `C2:D4D5..C2:D4EF`
- `C2:D4F0..C2:D4F7`
- `C2:D4F8..C2:D505`
- `C2:D506..C2:D519`

Net effect:
- froze the real externally-called three-slot refresh/build owner
- identified one local selector packet, one shared row/descriptor writer, two short wrappers, one local dispatch table, and an `E984`-status dispatcher

### Pass 135
Closed:
- `C2:D519..C2:D52A`
- `C2:D52B..C2:D545`
- `C2:D546..C2:D58A`
- `C2:D58B..C2:D5D8`
- `C2:D5D9..C2:D604`
- `C2:D605..C2:D617`
- `C2:D618..C2:D644`
- `C2:D645..C2:D68F`
- `C2:D690..C2:D6C2`
- `C2:D6C3..C2:D714`
- `C2:D715..C2:D777`

Net effect:
- corrected the seam so it actually began at the exact 9-word local dispatch table
- froze multiple status-gated owners plus a shared overflow/service body

### Pass 136
Closed:
- `C2:D778..C2:D7CE`
- `C2:D7CF..C2:D8B1`
- `C2:D8B2..C2:D994`
- `C2:D995..C2:D9FF`

Net effect:
- split the seam into one status-gated sibling owner, two larger refresh/build owners, and a shared sign-split block/template helper

### Pass 137
Closed:
- `C2:DA01..C2:DA34`
- `C2:DA35..C2:DA3C`
- `C2:DA3D..C2:DA4F`
- `C2:DA50..C2:DA63`
- `C2:DA64..C2:DA82`
- `C2:DA83..C2:DA9E`
- `C2:DA9F..C2:DAB0`
- `C2:DAB1..C2:DACA`

Important correction:
- `C2:DA00` was not the entry at all; it was only the terminal `RTS` byte of the previous helper.

Net effect:
- froze the exact selector-step dispatcher family and its four bounded step/clamp handlers plus shared accumulator tail.

### Pass 138
Closed:
- `C2:DACB..C2:DB97`
- `C2:DB98..C2:DB9E`
- `C2:DB9F..C2:DBE6`
- `C2:DBE8..C2:DC1C`
- `C2:DC1E..C2:DC73`
- `C2:DC74..C2:DC7A`

Net effect:
- froze the exact setup/import/export owner following the selector-step family
- froze the `0D5F -> 104D/93CC/93CD` compactor/export helper
- froze the `104D`-driven row/materializer owner

### Pass 139
Closed:
- `C2:DC7B..C2:DCBF`
- `C2:DCC0..C2:DCD7`
- `C2:DCD8..C2:DD01`
- `C2:DD02..C2:DD1D`
- `C2:DD20..C2:DD3F`
- `C2:DD40..C2:DD55`
- `C2:DD56..C2:DD97`
- `C2:DD98..C2:DE1C`
- `C2:DE1D..C2:DE20`
- `C2:DE21..C2:DE55`
- `C2:DE56..C2:DE97`

Important correction:
- the old seam `C2:DC7B..C2:DD80` was too short; it stopped in the middle of live helper code.

Net effect:
- froze the refresh/materializer owner, two local strip helpers, the shared export/materializer helpers, the `104D`-driven refresh owner, the local table, and the dual-lane helper family.

---

# 4) Where the project is right now

## Current exact state
- latest pass: **139**
- completion estimate: **69.7%**
- label rows: **1111**
- strong labels: **822**
- caution labels: **51**
- toolkit doctor health: **100.0%**
- current next seam: **`C2:DE98..C2:DF76`**

## What that means in plain English
The project is no longer just sitting on the session-6 anchor.
It now has a much larger exact C2-side ownership map downstream of that anchor, especially in the refresh/build/export/materializer lane.

The project is healthier than it was at session start because:
- more code/data boundaries are exact
- more wrappers/helpers/local tables are frozen
- the toolkit is better at resisting stale handoff state

But it is still **not done**.

---

# 5) What still has to be done to be completely done

There are two layers here:
1. the **immediate next disassembly target**
2. the **actual endgame requirements** for calling the Chrono Trigger ROM disassembly complete

## Immediate next move
The next clean seam to continue from is:
- **`C2:DE98..C2:DF76`**

That is the direct continuation target from the current pass-139 state.

## Still-open project-level semantic gaps
The current state still explicitly leaves these broader semantic problems open:
- broader noun for **`7E:0F0F`**
- broader noun for **`7E:0D1F`**
- broader gameplay/system role of **`7E:0D8B`**
- broader gameplay/system role of **`7E:0D8C`**
- broader gameplay/system role of **`7E:0D90`**
- broader top-level family noun for **`C2:A886..C2:AA30`**

## Still-open endgame requirements
The project still is not complete until all of this is done:

### A. Broad bank coverage / source-tree expansion
Still required:
- much broader bank-by-bank representation across the ROM
- not just hot-zone excellence in C0/C2/FD-style families
- a genuinely broad source tree rather than a mostly advanced partial tree

### B. Stable code/data separation across the untouched ROM
Still required:
- continue converting fuzzy ranges into exact owners/helpers/tables/descriptors
- continue demoting fake code and fake entry points
- continue separating true executable ranges from packet/data bands

### C. High-confidence subsystem ownership
Still required:
- keep naming and proving the major engine/script/display/data families
- keep tightening WRAM ownership and local packet grammar
- keep community shorthand separate from ROM-proof ownership

### D. Runtime-backed proof
Still required:
- bring in trace-backed proof for major WRAM/shadow/dispatch families
- validate static claims with debugger/runtime evidence
- especially for the important slot/materializer/state families

### E. Rebuildability
Still required:
- move beyond “starter” rebuild mode
- expand into a truly assembler-ready source tree
- integrate with an assembler pipeline that can emit a ROM image

### F. ROM verification
Still required:
- zero-diff rebuild if achievable
- or at minimum an explainably bounded-diff rebuild against the original ROM

## The real definition of “complete” still stands
The project is only truly complete when it reaches all of these:
1. broad, bank-complete or near-bank-complete source coverage
2. stable code/data separation across the ROM
3. high-confidence labels for the major engine/script/display/data families
4. runtime-backed proof on important WRAM/shadow/dispatch families
5. assembler integration that can emit a ROM image
6. zero-diff or explainably bounded-diff rebuild verification against the original ROM

---

# 6) Recommended continuation plan

## Immediate continuation
1. continue at **`C2:DE98..C2:DF76`**
2. keep freezing the C2-side caller / refresh / export / materializer family downstream
3. keep correcting false seam ends aggressively whenever a seam lands in mid-helper or mid-data

## Medium-term continuation
1. finish the surrounding C2-side family around the current seam
2. revisit still-broad WRAM nouns (`0F0F`, `0D1F`, `0D8B/8C/90`)
3. tighten the broader `C2:A886..C2:AA30` family noun

## Endgame continuation
1. widen bank coverage substantially
2. start bringing in runtime-backed proof
3. push toward assembler-ready rebuildability
4. finish with bounded-diff / zero-diff rebuild verification

---

# 7) Current key files to continue from

## Current main continuation files
- `ct_disasm_toolkit_v6_pass139_continued.zip`
- `chrono_trigger_disasm_pass139.md`
- `chrono_trigger_labels_pass139.md`
- `chrono_trigger_next_session_start_here_pass139.md`
- `ct_completion_score_after_pass139.json`
- `ct_consistency_report_after_pass139.md`
- `ct_toolkit_doctor_after_pass139.md`
- `ct_current_session_packet_after_pass139.md`

## Important baseline context files
- `chrono_trigger_master_handoff_session6.md`
- `chrono_trigger_toolkit_deep_upgrade_after_pass119.md`

---

# Final blunt summary

This session was real progress.
It moved the project from the session-6 endpoint at **pass 119** to **pass 139**, pushed the completion estimate to **69.7%**, kept the toolkit healthy, and materially expanded the exact C2-side ownership map through the refresh/build/export/materializer families.

But the project is still in the **advanced disassembly in progress** phase, not the **complete disassembly** phase.

The strongest continuation point right now is simple:
- continue at **`C2:DE98..C2:DF76`**
- keep widening exact subsystem ownership
- then finish the broader bank, runtime-proof, and rebuild-verification endgame work until the project actually meets the full completion bar.
