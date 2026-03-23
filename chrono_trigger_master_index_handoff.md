# Chrono Trigger (USA) ROM Disassembly — Master Index Handoff

## Purpose
This document is a **topic-based master index** for the work completed in this session, intended to sit beside the chronological handoff and the per-pass markdown files.

Use this file when you need to answer:
- "Where did we solve that?"
- "Which passes matter for this subsystem?"
- "What is strong vs provisional?"
- "What should be read first before continuing?"

This is **not** a replacement for the canonical handoffs. It is the navigation layer over them.

Primary companion documents:
- `chrono_trigger_master_handoff_session1.md` — original baseline handoff before this session
- `chrono_trigger_master_handoff_session2.md` — full detailed handoff for this session (passes 32–61)

---

## Mandatory starting context for the next worker
Before continuing ROM work, the next worker should refresh context from the **Chrono Trigger modding/research community** so they know where public knowledge ends and direct ROM proof still begins.

Priority external context to review first:
1. **Chrono Compendium**
   - Utilities / Chrono Compressor / Temporal Flux ecosystem
   - Event Encyclopedia and event-documentation context
   - battle / technical writeups where bank `C1` or related runtime systems are discussed
2. **Data Crystal**
   - ROM identity
   - RAM map
   - Enemy AI docs
3. **Temporal Flux / Kajar Labs / Chrono Trigger modification forum material**
   - established community vocabulary
   - where event-layer terminology already exists
4. **Debugger context**
   - bsnes / bsnes-plus / Geiger-style workflows for runtime confirmation

Reason this is mandatory:
- it prevents fake novelty
- it prevents misnaming known event/battle systems
- it helps distinguish what the community already edits from what still requires first-principles disassembly

But: community docs are **context only**. Final naming and ownership should still come from ROM proof.

---

## Current top-of-stack state
Current top-of-stack after this session:
- **Pass 61** is the latest pass.
- The strongest newly unified result from late-session work is that **`C1:B80D` is the master bank-C1 opcode dispatch table**, and earlier "group 1 / group 2 / group 3" tables are interior slices or views of that global opcode space.
- The `C1` selector / query / replay / late-pack layers are substantially less opaque than they were at session start.
- The panel/tilemap/UI-facing runtime side is much stronger and now includes tilemap staging, companion strips, record buffers, numeric formatting, HP/MP interpretation, and readiness-gauge export structure.
- The readiness system now reads as a **unified 11-slot family** with visible head partition and runtime tail partition, plus canonical/live occupant maps and deferred tail materialization.

Still not done:
- full opcode semantics across the entire `C1:B80D` master table
- full ownership/subsystem naming for every late selector-control path
- decompressor grammar formalization
- full VM completion for other unresolved engines
- full bank-by-bank code/data separation
- rebuildable source tree / assembly recreation

---

## Approximate completion
Working estimate after this session: **~38% complete overall**.

Interpretation:
- Much more than "early exploratory reverse engineering"
- Still far short of a complete disassembly
- Main semantic spine is strong in multiple subsystems
- Endgame tasks remain expensive: exhaustive opcode coverage, bank splitting, format specs, rebuild validation

This percentage is intentionally conservative.

---

# Topic Index

---

## 1) ROM identity, baseline, and canonical context
Use these first if you need the foundational state before looking at subsystem-level notes.

Core files:
- `chrono_trigger_master_handoff_session1.md`
- `chrono_trigger_master_handoff_session2.md`

Why they matter:
- ROM fingerprint / baseline assumptions
- pass-31 top-of-stack from prior session
- what was already solved before pass 32 began
- global open-item list

---

## 2) Bank C1 command-dispatch unification
This is one of the biggest structural outcomes of the session.

### Key result
`C1:B80D` is the **master bank-C1 opcode dispatch table**.
Earlier tables once treated as separate command roots are better understood as slices or regions inside one larger opcode space.

### Read in this order
1. `chrono_trigger_disasm_pass32.md`
2. `chrono_trigger_disasm_pass33.md`
3. `chrono_trigger_disasm_pass34.md`
4. `chrono_trigger_disasm_pass35.md`
5. `chrono_trigger_disasm_pass59.md`
6. `chrono_trigger_disasm_pass60.md`
7. `chrono_trigger_disasm_pass61.md`

Matching labels:
- `chrono_trigger_labels_pass32.md`
- `chrono_trigger_labels_pass33.md`
- `chrono_trigger_labels_pass34.md`
- `chrono_trigger_labels_pass35.md`
- `chrono_trigger_labels_pass59.md`
- `chrono_trigger_labels_pass60.md`
- `chrono_trigger_labels_pass61.md`

### Main solved pieces
- early group-1/group-2 opcode maps
- `FD:BA4A` command-advance/skip table role
- many stub/alias handlers identified and de-noised
- real semantics for selected opcodes in early tables
- late correction that `B8F3` was not an independent selector-wrapper table
- late correction that `B80D` is the master dispatcher, not a special pack-only subtable

### Important caution
Do **not** keep using the old mental model that `B85F`, `B88D`, and `B8BB` are separate root dispatch tables. After pass 61, that framing is weaker than the unified master-table model.

---

## 3) Early C1 command semantics: group-1 / group-2 phase
This is the phase where the initial live target from the session handoff was attacked directly.

### Read in this order
1. `chrono_trigger_disasm_pass32.md`
2. `chrono_trigger_disasm_pass33.md`
3. `chrono_trigger_disasm_pass34.md`
4. `chrono_trigger_disasm_pass35.md`

Labels:
- `chrono_trigger_labels_pass32.md`
- `chrono_trigger_labels_pass33.md`
- `chrono_trigger_labels_pass34.md`
- `chrono_trigger_labels_pass35.md`

### Main solved items
- group-1 opcode `0x04` as a random 4-way stream-advance / branch-style command
- `AF24` as a short-circuit/abort-style status flag in dispatcher flow
- `B3B8` as a post-handler path selector
- `0x0D` bitmask-driven state control structure
- `0x13/0x14/0x15` saturating signed-delta family structure
- early-pair resolution for `99BE` vs `9A39/9A3D`
- helper seam around `AC89`, `ACCE`, `ACF2`, `AD09`, `AD35`, `C1DD`, `FD:AB01`

### Best reference when revisiting command-shell ambiguity
- `chrono_trigger_disasm_pass34.md`
- `chrono_trigger_disasm_pass35.md`

---

## 4) Descriptor / candidate expansion pipeline (`C1:C55F` side)
This is where the session pivoted from early command-shell work into the deeper candidate-expansion/query machinery.

### Read in this order
1. `chrono_trigger_disasm_pass36.md`
2. `chrono_trigger_disasm_pass37.md`

Labels:
- `chrono_trigger_labels_pass36.md`
- `chrono_trigger_labels_pass37.md`

### Main solved items
- `C1:C55F` as a descriptor-driven candidate expansion/finalization path
- `$3A` as common-tail mode selector
- `$0C` as descriptor index into `CC:2AB0`
- packet-writer dispatch into `$9604..$9608`
- `C736` / `C741` as descriptor-selected trigger wrappers
- `C6D9` as final compaction/count phase
- bank-local `JSR $0003` dispatcher model cracked
- service 5 vs service 7 separated structurally

### Important output
This is the handoff point where service/query abstractions stop being vague and start becoming a real layered controller model.

---

## 5) Service-7 geometric query family and wrappers
This is one of the strongest mid-session gains.

### Read in this order
1. `chrono_trigger_disasm_pass37.md`
2. `chrono_trigger_disasm_pass38.md`
3. `chrono_trigger_disasm_pass39.md`
4. `chrono_trigger_disasm_pass40.md`

Labels:
- `chrono_trigger_labels_pass37.md`
- `chrono_trigger_labels_pass38.md`
- `chrono_trigger_labels_pass39.md`
- `chrono_trigger_labels_pass40.md`

### Main solved items
- service 7 outer dispatcher/subdispatcher structure
- `2332` as seeded same-axis band scan
- `23A4` as triangle / three-vertex inclusion scan
- `2701` as cell-radius scan using square table `CC:FB6F`
- `25A3` as dual-anchor oriented inclusion family
- `$9604` as service-7 partition selector
- service-7 wrapper table around `1FF8`
- result cursor helpers `27FA / 2814 / 282D`
- outer controller layer feeding service 7
- `$9609` replay/follow-up counter
- `$960F` preferred/current source slot
- table-driven/dynamic/fixed launch families above service 7

### Best place to understand the service-7 stack
- structural base: `pass37`
- geometry semantics: `pass38`
- wrapper/controller semantics: `pass39` + `pass40`

---

## 6) Pending FIFO, record metadata, and lane reconciliation
This is where the upstream controller/query system started attaching to concrete record structures.

### Read in this order
1. `chrono_trigger_disasm_pass41.md`
2. `chrono_trigger_disasm_pass42.md`
3. `chrono_trigger_disasm_pass43.md`

Labels:
- `chrono_trigger_labels_pass41.md`
- `chrono_trigger_labels_pass42.md`
- `chrono_trigger_labels_pass43.md`

### Main solved items
- `99D4..99D8` as 3-entry pending-slot FIFO/count/index
- `93EE..93F4` record metadata structure
- `CC:FAF0` slot->record-offset map
- `93EE.bit6/bit7` meaning split
- `93EF.bit6` reservation latch
- `93F3` packed nibble-pair dispatch byte
- `93F4` launch-table token copy
- lane-ID interpretation of `93F3`
- canonical-record lane reconciler at `B575..B6C9`
- enabled-lane dispatcher helpers in bank `FD`
- service 2 interpreted as 3-lane roster removal/reseat controller
- active-lane roster and pending-admission queue interpretation

### Why this matters
This is the bridge from selector/query math into a real runtime model with lanes, pending queues, record tables, and active roster management.

---

## 7) Panel/tilemap/UI staging pipeline (`0B40`, `0CC0`, `0E80` families)
This is the strongest UI-facing/runtime-presentation branch solved in the session.

### Read in this order
1. `chrono_trigger_disasm_pass44.md`
2. `chrono_trigger_disasm_pass45.md`
3. `chrono_trigger_disasm_pass46.md`
4. `chrono_trigger_disasm_pass47.md`
5. `chrono_trigger_disasm_pass48.md`
6. `chrono_trigger_disasm_pass49.md`

Labels:
- `chrono_trigger_labels_pass44.md`
- `chrono_trigger_labels_pass45.md`
- `chrono_trigger_labels_pass46.md`
- `chrono_trigger_labels_pass47.md`
- `chrono_trigger_labels_pass48.md`
- `chrono_trigger_labels_pass49.md`

### Main solved items
- `0B40` as VRAM-uploaded tilemap staging buffer
- `99E2` as pending upload/dirty counter
- DMA upload proof via bank `CF` to VRAM `7A00`
- default/alternate/reset strip templates from `D1:5800 / 5A50 / 5BD0`
- `0B40` geometry tightened to 32 words x 6 rows
- dynamic three-slot panel-strip composition tied to active-lane roster
- companion-strip blitters into `0CC0..0E08`
- companion-record buffer rebuild in `0E80..0FFF`
- `CC:FA23..FA3F` lane-anchor offset tables
- `CC:FADD` lane-block base table
- `CC:FAE9` lane-marker anchor table
- `C1:1918` old-marker clear/current-marker stamp path
- decimal digit formatters and leading-zero blanker
- numeric fields from lane-selected record data
- HP/MP interpretation strengthened
- `5E30/5E32` as current/max HP
- `5E2F.bit0` as low-HP/critical threshold flag
- `A10F` as lane-local HP-threshold presentation selector

### Best entry point for the panel branch
- start at `pass44` for raw staging buffer proof
- then `pass45/46` for composition model
- then `pass47/48/49` for numeric fields and field semantics

---

## 8) Readiness / ATB-style timer / gauge branch
This is the other strongest runtime-facing branch solved in the session.

### Read in this order
1. `chrono_trigger_disasm_pass50.md`
2. `chrono_trigger_disasm_pass51.md`
3. `chrono_trigger_disasm_pass52.md`
4. `chrono_trigger_disasm_pass53.md`
5. `chrono_trigger_disasm_pass54.md`
6. `chrono_trigger_disasm_pass55.md`
7. `chrono_trigger_disasm_pass56.md`
8. `chrono_trigger_disasm_pass57.md`

Labels:
- `chrono_trigger_labels_pass50.md`
- `chrono_trigger_labels_pass51.md`
- `chrono_trigger_labels_pass52.md`
- `chrono_trigger_labels_pass53.md`
- `chrono_trigger_labels_pass54.md`
- `chrono_trigger_labels_pass55.md`
- `chrono_trigger_labels_pass56.md`
- `chrono_trigger_labels_pass57.md`

### Main solved items
- visible bar path as active-time/readiness gauge
- base rate -> status-modified rate chain
- `BD6F` as halve/double time-increment helper under status bits
- `99DD` = current/fill export
- `9F22` = goal/cap export
- `B390` bridge from readiness seed into export-facing buffers
- seed formula centered on `0x69 - speed*6 + table bonus`
- `CC:2E31` as 8x16 config-page table family
- major correction that `B158..B162`, `AFAB..AFB5`, `B03A..B044` are one contiguous 11-slot family
- 3-slot visible head + 8-slot runtime tail model
- minimum-positive subtractive normalization across the 11-slot readiness array
- zero entries preserved, `AEFF==FF` skipped because slots are empty
- `AEFF..AF09` as live occupant map
- `AF0A..AF14` as remembered/canonical occupant map
- inverse map `B1BE`
- tail canonical/live builder paths
- deferred tail materialization state (`AF15.bit7`)

### Best reading order if you only care about readiness system
- `pass50` for gauge interpretation
- `pass52` for seed formula
- `pass53` for 11-slot family correction
- `pass54/55/56/57` for occupancy and materialization

---

## 9) Occupant maps, head/tail partitions, and deferred tail materialization
This is tightly connected to the readiness system, but important enough to isolate.

### Read in this order
1. `chrono_trigger_disasm_pass55.md`
2. `chrono_trigger_disasm_pass56.md`
3. `chrono_trigger_disasm_pass57.md`
4. `chrono_trigger_disasm_pass58.md`
5. `chrono_trigger_disasm_pass59.md`

Labels:
- `chrono_trigger_labels_pass55.md`
- `chrono_trigger_labels_pass56.md`
- `chrono_trigger_labels_pass57.md`
- `chrono_trigger_labels_pass58.md`
- `chrono_trigger_labels_pass59.md`

### Main solved items
- head live/canonical occupant maps
- tail live/canonical occupant maps
- visible-head occupied count vs tail canonical count
- `AF15.bit7` as canonical-but-withheld / deferred materialization state
- withheld-tail candidate list builder and random reducer
- deferred reinsertion helper at `AED3` narrowed
- late selector-control range ownership around `AC14 / AC2E`
- fixed selector bytes, visible min selector, withheld-tail reducer, live-tail reducer

### Important caution
Pass 58 produced useful negative proof: lack of direct whole-ROM `JSR/JMP/JSL` callers to `AB03` and `AED3` means they should not be mislabeled as top-level roots.

---

## 10) Late selector-control and micro-pack executor
This is the late-session branch that reframed several earlier assumptions.

### Read in this order
1. `chrono_trigger_disasm_pass58.md`
2. `chrono_trigger_disasm_pass59.md`
3. `chrono_trigger_disasm_pass60.md`
4. `chrono_trigger_disasm_pass61.md`

Labels:
- `chrono_trigger_labels_pass58.md`
- `chrono_trigger_labels_pass59.md`
- `chrono_trigger_labels_pass60.md`
- `chrono_trigger_labels_pass61.md`

### Main solved items
- selector-wrapper families are tied into the existing selector-control dispatch system
- `0x27..0x38` selector-control range now mapped much more concretely
- `0x49 -> AFD7` as seed into late selector-pack executor
- `CC:8B08` as 4-byte late selector pointer-record table
- FE/FF-delimited micro-pack execution model
- `B239`, `B1CF`, `B24A`, `B242`, `B263` structural roles in pack/replay system
- correction that late-pack execution feeds global C1 opcode bytes back into shared dispatcher
- `8C0A..8CF7` as tail replay/controller layer around that shared dispatcher

### Why this matters
This is the place where the session moved from local helper naming into a stronger global architectural statement: late-tail replay is not its own little world; it sits on top of the same master opcode space.

---

## 11) Helper routines and math/utility interpretations
Use this section when you need the support routines without rereading every subsystem pass.

Relevant passes:
- `chrono_trigger_disasm_pass35.md`
- `chrono_trigger_disasm_pass36.md`
- `chrono_trigger_disasm_pass51.md`
- `chrono_trigger_disasm_pass52.md`
- `chrono_trigger_disasm_pass54.md`

Relevant labels:
- `chrono_trigger_labels_pass35.md`
- `chrono_trigger_labels_pass36.md`
- `chrono_trigger_labels_pass51.md`
- `chrono_trigger_labels_pass52.md`
- `chrono_trigger_labels_pass54.md`

Key helper outcomes:
- `AC89`, `ACCE`, `ACF2`, `AD09`, `AD35`, `C1DD`
- `C90B` multiply helper in readiness seed path
- `A3D1` saturating signed-byte adjust helper
- minimum-positive subtractive normalization body at `FD:B8F7`

---

## 12) Community-context references that affected naming discipline
These are not proof sources for labels, but they matter for avoiding bad assumptions.

Use the community-research section in `chrono_trigger_master_handoff_session2.md` for the fuller narrative.

Main lessons imported from community context:
- event-engine documentation exists and should not be collapsed into all command interpreters
- bank `C1` contains battle-facing material in public research, so subsystem ownership must be proven, not assumed
- Chrono Trigger’s compression/tool ecosystem is real and specialized, but external tool behavior is validation, not primary proof
- RAM maps help sanity-check live structures but do not solve opcode semantics for us

---

# Reading paths by goal

## If you need to continue C1 opcode work
Read:
1. `chrono_trigger_master_handoff_session2.md`
2. `pass59`
3. `pass60`
4. `pass61`
5. then go backward to `pass32..35` as needed

## If you need to continue UI/panel/tilemap work
Read:
1. `pass44`
2. `pass45`
3. `pass46`
4. `pass47`
5. `pass48`
6. `pass49`

## If you need to continue readiness / active-time work
Read:
1. `pass50`
2. `pass52`
3. `pass53`
4. `pass54`
5. `pass55`
6. `pass56`
7. `pass57`

## If you need to continue selector / tail materialization work
Read:
1. `pass57`
2. `pass58`
3. `pass59`
4. `pass60`
5. `pass61`

---

# Strongest solved structures from this session
These are the findings I would trust most as foundations for future work.

1. **`C1:B80D` = master bank-C1 opcode dispatch table**
2. **service 7 = real geometric candidate-query family with multiple distinct query shapes**
3. **`0B40` = VRAM-uploaded tilemap staging buffer**
4. **`0CC0..0E08` = companion strip; `0E80..0FFF` = companion record buffer**
5. **panel branch renders HP/MP-adjacent numeric fields with critical-threshold presentation logic**
6. **readiness system = contiguous 11-slot family, not two unrelated pairs**
7. **occupant maps = unified live/canonical head+tail system with deferred tail materialization**
8. **late-tail pack/replay layer feeds back into the same master C1 opcode space**

---

# Highest-risk provisional areas still needing caution
These are the places where labels are still structurally useful but not fully frozen.

1. Exact high-level gameplay-facing name of the service-7 controller layer
2. Exact gameplay-facing name of the lane/record/panel subsystem as a whole
3. Final semantics of all late selector-control bytes beyond the best-solved range
4. Exact `$0E -> AED3` reinsertion bridge and ownership
5. Exact identities of all pack-emitted opcodes in live execution
6. Positive writer side for `9F38[x]`
7. Full tail runtime identity beyond occupancy/materialization model

---

# What still needs to be done to completely disassemble the ROM
This is the condensed master checklist.

## A. Finish semantic coverage of the known major engines
- complete the remaining unresolved opcode semantics in the master `C1:B80D` space
- fully finish selector-control ranges not yet structurally frozen
- finish the remaining helper seams around pack execution and replay
- keep validating service/controller ownership boundaries

## B. Finish the `7F:2000` VM and any other partially solved command systems
- reconcile with prior-session VM work
- close any remaining opcode gaps
- ensure scheduling / movement / palette / effect / camera paths are fully tied to callers

## C. Formalize decompressor / compression grammar
- convert current understanding from operational knowledge into a real format specification
- cross-check with Chrono Compressor-style external behavior
- identify encoded block types, escapes, copy modes, and termination rules rigorously

## D. Bank-by-bank code/data separation
This is one of the biggest remaining jobs.

Needed tasks:
- every bank needs conservative code/data separation
- jump tables and inline data must be explicitly isolated
- known service tables must be annotated and partitioned cleanly
- fake code from accidental linear sweep must be eliminated

## E. Build a real source tree
- split banks into source files
- establish label naming conventions globally
- keep strong/provisional labels separate
- create include structure for common tables and WRAM symbols
- assemble documentation for bank ownership and cross-bank contracts

## F. Rebuild validation
- prove a source recreation can rebuild matching bytes
- do incremental rebuild validation, not one giant all-at-once leap
- track bank-local checksum / byte-for-byte equivalence
- log unresolved ambiguities explicitly

## G. Runtime validation with emulator tooling
This is where bsnes/bsnes-plus matters.

Use runtime tooling to validate:
- which late selector-control bytes are emitted in real gameplay
- pack/replay execution flow
- UI tilemap mutation timing
- readiness / head-tail occupancy behavior under battle state changes
- deferred tail materialization triggers

## H. Produce final end-state artifacts
For a true completed disassembly, the final artifact set should include:
- rebuildable source tree
- per-bank code/data maps
- global symbol list
- subsystem architecture docs
- opcode reference docs
- decompression/compression format docs
- WRAM structure docs
- validation notes and remaining uncertainties

---

# Immediate next recommended work
If continuing right now, do this:

1. Refresh community context quickly (Chrono Compendium / Data Crystal / tooling ecosystem)
2. Re-read `chrono_trigger_master_handoff_session2.md`
3. Re-read `pass59`, `pass60`, and `pass61`
4. Continue on the **early global opcode band inside the master `C1:B80D` table**, especially the pack-fed observed opcodes:
   - `00`
   - `01`
   - `02`
   - `04`
   - `05`
   - `06`
   - `07`
   - `09`
   - `0A`
   - `0B`
   - `0F`
   - `12`
   - `15`
   - `1B`
   - `20`
5. Use runtime confirmation in bsnes/bsnes-plus if needed when static control flow stops being enough

---

# File inventory for this session

## Pass files
- `chrono_trigger_disasm_pass32.md`
- `chrono_trigger_disasm_pass33.md`
- `chrono_trigger_disasm_pass34.md`
- `chrono_trigger_disasm_pass35.md`
- `chrono_trigger_disasm_pass36.md`
- `chrono_trigger_disasm_pass37.md`
- `chrono_trigger_disasm_pass38.md`
- `chrono_trigger_disasm_pass39.md`
- `chrono_trigger_disasm_pass40.md`
- `chrono_trigger_disasm_pass41.md`
- `chrono_trigger_disasm_pass42.md`
- `chrono_trigger_disasm_pass43.md`
- `chrono_trigger_disasm_pass44.md`
- `chrono_trigger_disasm_pass45.md`
- `chrono_trigger_disasm_pass46.md`
- `chrono_trigger_disasm_pass47.md`
- `chrono_trigger_disasm_pass48.md`
- `chrono_trigger_disasm_pass49.md`
- `chrono_trigger_disasm_pass50.md`
- `chrono_trigger_disasm_pass51.md`
- `chrono_trigger_disasm_pass52.md`
- `chrono_trigger_disasm_pass53.md`
- `chrono_trigger_disasm_pass54.md`
- `chrono_trigger_disasm_pass55.md`
- `chrono_trigger_disasm_pass56.md`
- `chrono_trigger_disasm_pass57.md`
- `chrono_trigger_disasm_pass58.md`
- `chrono_trigger_disasm_pass59.md`
- `chrono_trigger_disasm_pass60.md`
- `chrono_trigger_disasm_pass61.md`

## Label files
- `chrono_trigger_labels_pass32.md`
- `chrono_trigger_labels_pass33.md`
- `chrono_trigger_labels_pass34.md`
- `chrono_trigger_labels_pass35.md`
- `chrono_trigger_labels_pass36.md`
- `chrono_trigger_labels_pass37.md`
- `chrono_trigger_labels_pass38.md`
- `chrono_trigger_labels_pass39.md`
- `chrono_trigger_labels_pass40.md`
- `chrono_trigger_labels_pass41.md`
- `chrono_trigger_labels_pass42.md`
- `chrono_trigger_labels_pass43.md`
- `chrono_trigger_labels_pass44.md`
- `chrono_trigger_labels_pass45.md`
- `chrono_trigger_labels_pass46.md`
- `chrono_trigger_labels_pass47.md`
- `chrono_trigger_labels_pass48.md`
- `chrono_trigger_labels_pass49.md`
- `chrono_trigger_labels_pass50.md`
- `chrono_trigger_labels_pass51.md`
- `chrono_trigger_labels_pass52.md`
- `chrono_trigger_labels_pass53.md`
- `chrono_trigger_labels_pass54.md`
- `chrono_trigger_labels_pass55.md`
- `chrono_trigger_labels_pass56.md`
- `chrono_trigger_labels_pass57.md`
- `chrono_trigger_labels_pass58.md`
- `chrono_trigger_labels_pass59.md`
- `chrono_trigger_labels_pass60.md`
- `chrono_trigger_labels_pass61.md`

---

# Final instruction
Treat this file as the **map**, not the proof.
When in doubt:
- use this file to find the right pass
- use the pass file for the actual evidence trail
- use the label file to see the naming state
- use the session handoff for overall narrative and next priorities
