# Chrono Trigger (USA) ROM Disassembly — Detailed Session 3 Handoff

## Purpose
This is the **full narrative handoff for the work completed in this session**, covering the jump from **pass 61** to **pass 81**.

Use this file to answer three things fast:
1. **What got done in this session?**
2. **Where is the disassembly now?**
3. **What is still left before this project can honestly be called a complete Chrono Trigger SNES ROM disassembly?**

This file is the detailed companion to:
- `chrono_trigger_master_index_handoff.md` — topic index / navigation layer
- `ct_disasm_toolkit_v5_updated_pass81.zip` — current canonical toolkit snapshot
- `ct_completion_score_pass81.md` — current conservative completion score

---

## Mandatory context before anyone continues
Before doing more ROM work, refresh on the public Chrono Trigger modding/research context first.
That is still mandatory.

Priority external context to refresh:
- Chrono Compendium
- Data Crystal
- Temporal Flux / Kajar Labs / older forum material
- bsnes / bsnes-plus / Geiger-style runtime debugger workflow

Reason:
- prevents fake novelty
- prevents inventing wrong names for already-known systems
- keeps the ROM-proof layer separate from community shorthand

But the same rule still applies:
**community context is vocabulary support, not proof.**
Final ownership, labels, and semantics should still come from direct ROM evidence.

---

# 1) Session scope

## Start state
This session started from the prior handoff state:
- latest pass was **61**
- `C1:B80D` had already been elevated to the **master bank-C1 opcode dispatch table**
- major selector/query/replay/control layers were partially understood
- project-wide completion estimate was still only about **38%**

## End state
This session ended at:
- latest pass: **81**
- canonical toolkit: **`ct_disasm_toolkit_v5_updated_pass81.zip`**
- completion estimate: **~60.9%**

Current weighted breakdown:
- Label semantics: **74.9%**
- Opcode coverage: **92.5%**
- Bank separation: **24.0%**
- Rebuild readiness: **8.2%**

Current coverage counts:
- Master C1 opcodes: **170 / 170**
- Selector-control bytes: **83 / 83**
- Service-7 wrappers: **5 / 8**

### The blunt truth
This session was a **huge semantic consolidation session**.
It did not just add more notes.
It pushed the project from “a strong exploratory reverse-engineering body” to “a mostly-covered control-plane disassembly with real late-pipeline structure.”

Still, the project is **not near done** in the assembler/rebuild sense.
The expensive endgame is still ahead.

---

# 2) What was accomplished in this session

This session did four major things:

## A. It cracked the early global `C1:B80D` opcode band much harder
Passes **62–66** tightened the low global opcodes into real families instead of leaving them as isolated mystery handlers.

Main outcomes:
- replay/control gates were separated from true work handlers
- `AF24` failure signaling was reinforced as a real dispatcher-side fail/abort output
- multiple low opcodes were proven to be **selector reducers**, **relation gates**, **record gates**, or **live-tail presence tests**, not vague “battle logic”
- `AE21` stopped being a fuzzy helper and became a real **marked-entry reducer**

That early band is now much less noisy and much more architectural.

## B. It promoted the old sliced opcode views into proper master-opcode ownership
Passes **67–72** were the “promotion and ownership cleanup” wave.

Main outcomes:
- old group-local bodies were promoted into their true global-master opcode slots
- alias clusters were separated from real bodies
- master coverage was extended cleanly across:
  - `23..28`
  - `29..2F`
  - `30..56`
  - `57..A9`
- visible-head selector families, nonhead selector families, and late mutator/controller bands were all placed in their correct global-master context
- **master C1 coverage eventually reached 170/170**

This matters because the project is no longer pretending local slices are separate top-level dispatch tables.
The global table model won.

## C. It tightened the late helper/continuation chain into a real system
Passes **73–76** upgraded the late continuation path from “helper soup” into a real control/data pipeline.

Main outcomes:
- `8CF9` became a real **current-tail selector-control interpreter / materialization controller**
- `EBF8` / `EC7F` became a real **pending signed stat-delta packet system**
- `FD:ACEE` was pinned as the exact workspace clear for the transient packet area
- `BFAA`, `895B`, `AC57`, and the service-04 entry chain stopped being vague and started reading like explicit mode-driven continuation paths
- service `04` was upgraded from “unknown hook” into a real **mode dispatcher** keyed by `AE92`

This was a major step because it gave the late `C1` control side a memory model, not just label fog.

## D. It pushed the late output/materialization side toward a graphics-oriented reading
Passes **77–81** opened the downstream output path much more aggressively.

Main outcomes:
- service-04 mode layout became cleaner
- the `2D00..` workspace was tightened as a **packed fragment/tile row stream workspace**
- `CD:13E6` resolved into concrete tile-orientation transforms:
  - direct
  - H-flip
  - V-flip
  - HV-flip
- `C0:FD00` was pinned as the bit-reverse lookup used by the H-flip path
- `1509` became a real **32-byte 4bpp tile-block materializer**
- the optional `CD:0018` auxiliary side stopped looking like generic trash and started reading like a small **command VM** with repeat/rewind behavior, state latches, and tile-block request logic
- token `0x80` inside that VM was cracked into a real 29-entry extended sub-op family instead of a fake 32-entry namespace

This is the strongest evidence so far that the late unresolved seam is not “generic battle fluff” but a **graphics/tile/sprite-oriented assembly path**.

---

# 3) Detailed pass-by-pass summary for this session

## Passes 62–64: early global opcode seam, replay gates, reducers, selector bodies

### Pass 62
Main upgrades:
- low opcodes `00`, `05`, `06`, `07`, `20`, `21` tightened hard
- proved a real replay-gate / control subset inside the master table
- success path vs `AF24 = 1` failure path became much clearer

Important outcomes:
- `00` = unconditional replay/controller step
- `05` = live unwithheld tail-count threshold gate
- `06` = current `96F1..96F3` triplet compare gate
- `07` = comparator gate over `B320[current]`
- `20` / `21` = per-slot state gates over `AEB3` and `AF15`

### Pass 63
Main upgrades:
- `01`, `02`, `03`, `04` stopped being foggy
- corrected stale toolkit carry-forward on opcode `04`

Important outcomes:
- `01` = arbitrary selector-result filter through `FD:A80B` records
- `02` = head-vs-nonhead partition filter via lane-block byte/mask data
- `03` = selector filter where `AEFF[selected] == immediate`
- `04` = invertible live-tail presence/absence gate over `AF02`

### Pass 64
Main upgrades:
- `AE21` was finally pinned properly
- `08`, `09`, `0A`, `0B` clarified through the new reducer proof

Important outcomes:
- `AE21` = reduce marked selected entries to one chosen entry or fail
- `08` = marked survivor builder by `FD` record word `+3`
- `09` / `0B` = scan-into-`AE21` wrappers
- `0A` = chosen-entry direct mask-clear gate bypassing `AE21`

---

## Passes 65–67: relation-query gates, current-slot record gates, alias cleanup, seed persistence

### Pass 65
Main upgrades:
- `0C/0D/0E/0F/10` tightened into a real relation-query wrapper/gate family
- `11/12` split away as direct per-slot record gates

Important outcomes:
- `0C` / `0F` / `10` = current-subject relation gates and band tests
- `11` = `B19E` upper-nibble class gate
- `12` = paired `B19E/B19F` gate

### Pass 66
Main upgrades:
- `13/14/15` tightened as current-slot record gates
- `16` and `19` proven as replay aliases
- `17`, `1B`, `1D`, `22` materially improved

Important outcomes:
- `17` = RNG threshold gate
- `1B` = visible-head live-count gate
- `1D` = selected tail-live presence/absence gate
- `22` = selected-entry `B158` threshold gate

### Pass 67
Main upgrades:
- `23..28` locked as exact aliases of opcode `18`
- `29..2F` promoted to true master-table ownership
- seed persistence bridge became much clearer

Important outcomes:
- `29` = selector-head persistence into `5E15/5E0D`
- `2A` = collapse by `B23A` priority, then persist into `5E15/5E0D`
- `2B` = collapse by `B23A` priority, then persist into `B16E`
- `2D` = random 4-way stream-advance command promoted into proper master identity

This is where the old local-group mental model really stopped being useful.

---

## Passes 68–72: master coverage promotion, visible/nonhead selector families, late lane/timer mutator band

### Pass 68
Main upgrades:
- master-table promotion of `30..56`
- group-2 slice promoted into real master ownership

Important outcomes:
- `32` = capture current inline param byte into `AEE4`
- `39` / `3F` = gate on whether a canonical tail slot can be materialized into the live tail map
- `30`, `34`, `3A..3E` = `STZ AF24 ; RTS` aliases
- `31`, `33`, `35..38`, `43`, `4E` = plain `RTS` aliases

### Pass 69
Main upgrades:
- promoted old selector-control slice into master `57..A9`
- decoded first promoted band `57..5F`
- fixed toolkit generator so master coverage no longer truncated at `0x3F`

Important outcomes:
- `58` = select occupied visible-head live slots `0..2`
- `59` = select all occupied live slots `0..10`
- `5A` = select current tail-local live slot (`B252 + 3`)
- `5B` = select current quad-record low nibble from `B19E + 4*B252`
- `5C` = random visible-head live-slot selector with unresolved pre-refresh gate through `B279`
- `5D` / `5E` = target-select relation modes `00` and `01`
- `5F` = select visible entry `0..2` by minimum current HP

### Pass 70
Main upgrades:
- closed full `60..6C` band
- proved this is one coherent visible-entry `FD`-record selector family

Important outcomes:
- `60..6B` = visible-entry selectors over exact `FD` record bytes/masks
- `6C` = select all occupied tail slots except the current one
- `AD68`, `AE70`, `ADA1` were tightened as the core helper trio for this family

### Pass 71
Main upgrades:
- closed full promoted band `70..7D`
- proved it is the nonhead counterpart to the pass-70 family

Important outcomes:
- `70` and `7D` = min-selector bodies over occupied nonhead live slots using the `FD` record word at `+3`
- `71..7C` = nonhead `FD`-byte selectors, often excluding `B18B`
- `76` flagged as provisional because the loop-update byte pattern is anomalous

### Pass 72
Main upgrades:
- cracked most of the promoted late band `90..A9`
- separated the real timed-state / lane-derived family from internal alias entries

Important outcomes:
- `90/92/93/94/95/9A` = lane-derived timed-state mutator family
- `91/98/99` = lane-derived helper/seed/controller paths
- `96/97/9B` = `RTS` aliases
- `9D..A9` = internal alias entries into the late-pack executor blob, not clean standalone top-level op bodies
- important correction: `A0` should not be treated as a clean top-level initializer

---

## Passes 73–76: continuation chain, packet system, descriptor loaders, service-04 mode dispatcher

### Pass 73
Main upgrades:
- `9C` materially upgraded
- `8CF9` and the packet chain got real nouns

Important outcomes:
- `8CF9` = current-tail selector-control interpreter / materialization controller
- `E89F` / `E8C0` = packet-slot offset calculators
- `EBF8` = queue one signed pending delta packet into the `B328` family
- `EC39` = clear non-persistent pending packet channels
- `EC7F` = apply pending channels into `5E30/32` and `5E34/36`
- `9C` = service-7 tail-lane admission/reseat and readiness-refresh controller

### Pass 74
Main upgrades:
- `91` and `99` upgraded from vague helpers into dual-path packet callers
- `98` upgraded into the stripped-down fast path
- `FD:ACEE` pinned as exact transient workspace clear

Important outcomes:
- `895B` = fixed follow-up-context seed helper into `AE91..AE96`
- `AC57` = common follow-up tail bridging into packet apply
- `AC85` = exact `EC7F` wrapper
- `FD:ACEE` = clears `AD9B` plus `AD9C..AE4B`
- `AE55` tightened as a materialization descriptor / option-flag byte
- `B2C0` tightened as armed alternate continuation-pointer flag

### Pass 75
Main upgrades:
- `BFA4` demystified completely
- `BF7F`, `BFAA`, `FD:ABA2`, `FD:AC6E` all tightened materially

Important outcomes:
- `BFA4` = exact `LDA #$04 ; JSR $0003 ; RTS`
- `AC57` = run service-04 hook, then apply pending stat-delta channels
- `BF7F` = 17-byte descriptor/profile loader from `CC:213F + 0x11*B18C`
- `BFAA` = current-tail follow-up-context initializer + descriptor-load + common-tail runner
- `FD:ABA2` = 7-byte descriptor accumulator + optional unique-token queue filler
- `FD:AC6E` = pending slot queue consumer / admission-materialization runner

### Pass 76
Main upgrades:
- service `04` stopped being a vague unknown hook and became a real mode dispatcher

Important outcomes:
- service `04` keyed by `AE92`
- `431D` = service-04 mode dispatcher through `7A63`
- `432C..459F` = mode-1 current-context profile loader/emitter front end
- `45A0..4758` = mode-2 fixed-follow-up profile loader/emitter front end
- `4833` = shared service-04 output materialization / emit-finalize runner
- `AE91` = service-04 source/current slot selector

---

## Passes 77–81: graphics/tile-oriented late pipeline and auxiliary command VM

### Pass 77
Main upgrades:
- service-04 mode `0` and mode `3` clarified
- `48EC` and `4943` were materially upgraded
- a structural correction was made to output-slot stride

Important outcomes:
- `475A` = service-04 mode `0` is just `RTS`
- `475B..4832` = service-04 mode `3`, high-range fixed-followup profile front end using `CD:5C26 + 7*(AE93 - BC)`
- `48EC` = segmented CE fragment-group stream parser into `A280` and `A2A0`
- `4943` = packed fragment/quad batch decoder into `A2D3` and `4500..` workspaces
- correction: the downstream output slots are **8-byte stride**, not 6-byte stride

### Pass 78
Main upgrades:
- `C3:0002` and `CD:0015/0018/002A` stopped being black boxes / stubs
- `2D00..` workspace got much tighter

Important outcomes:
- `C3:0002` = packed-stream-to-WRAM materializer veneer
- `C3:0557` = real worker, output through `$2180..$2183`, returns output size in `0306`
- `CD:0015` and `CD:002A` = fixed builders for six packed row-sections of the `2D00..` workspace
- `CD:0018` = optional selector-driven auxiliary fragment-stage initializer / expander
- `2D00..` = service-04 packed fragment-row stream workspace

### Pass 79
Main upgrades:
- transform table at `CD:13E6` resolved into exact tile-orientation modes
- tile-assembly interpretation strengthened sharply

Important outcomes:
- transform modes = direct / H-flip / V-flip / HV-flip
- `C0:FD00` = bit-reverse lookup used by H-flip path
- `1509` = 32-byte 4bpp tile-block materializer from one or two `D0` source blocks
- `CA32..` path = two-slot auxiliary descriptor stream interpreter

### Pass 80
Main upgrades:
- optional `CD:0018` side upgraded into a real command VM
- first clean token families were pinned

Important outcomes:
- `1654` = one-token interpreter
- token `< 0x7F` = derive `D0`-side tile-block source pointer into `CA18`
- token `0x7F` = pure advance token
- token `>= 0x80` = dispatch through 128-entry command table
- `0x80` = 32-way extended sub-dispatch entry point
- `0x81` = slot countdown seed
- `0x82` = 8-way paired-delta operator over `CA5E/CA60`
- `0x83..0x86` = repeat/rewind loop control
- `CA72/CA74` = repeat resume pointer + repeat countdown
- `CA5E/CA60` = paired 16-bit accumulators
- `CA17/CA18` = pending/current auxiliary `D0` tile-block request state

### Pass 81
Main upgrades:
- token `0x80` was cracked much further
- the fake clean “32 sub-op” assumption was killed

Important outcomes:
- token `0x80` opens a **29-entry live sub-op family (`0x00..0x1C`)**
- upper sub-ops were tightened into real wrappers/latches/state builders
- `0x18` = `JSL D1:E91A`
- `0x19` = increment `CE10`
- `0x1A` = `JSL D1:E899`
- `0x1B` = 8-byte increment strip rooted at `9FFA`
- `0x1C` = `JSL D1:E8C1`
- `0x15..0x17` = `E500/E850` strided table-control band
- `0x0F..0x14` = state/preset-builder band
- `0x00`, `0x0E`, `0x13` = shared parallel-table builder family over `BB06/BB07`, `BB86/BB87`, `BC06/BC07`

This is where the auxiliary side stopped looking like a random pile and started reading like a structured, stateful little VM.

---

# 4) Where the project stands now

## The strongest solved global result
The strongest global result after this session is:

> the **bank-C1 control plane is mostly covered at the opcode level**, with master opcode coverage at **170 / 170**, selector-control coverage at **83 / 83**, and the remaining uncertainty shifted away from dispatch ownership and toward **exact semantics, field nouns, format grammar, runtime proof, and rebuildability**.

That is a very different project state from where this session began.

## What is now strong
These areas are materially strong now:

### 1. Master C1 opcode ownership
- global master-table model is strong
- old local-slice confusion is much weaker
- alias entries vs real bodies are much cleaner

### 2. Selector-control and reducer logic
- visible-head vs nonhead families are separated
- `AE21`, `AE70`, `ADA1`, and surrounding families are much more concrete
- record-byte / record-word selector families are well mapped structurally

### 3. Late lane/timer/state mutator family
- `90..9C` region is much less vague
- late lane-derived controller behavior and timer expiration side effects are structurally real now

### 4. Packet/delta continuation chain
- `8CF9`
- `EBF8`
- `EC39`
- `EC7F`
- `AC57`
- `FD:ACEE`

These no longer read like disconnected helpers.
They read like a system.

### 5. Service-04 descriptor and output front-end
- service `04` is a mode dispatcher, not a mystery hook
- mode-1 / mode-2 / mode-3 front ends are structurally distinct
- descriptor/profile loading is materially tighter

### 6. Late graphics/tile-oriented materialization path
This is now one of the most important near-finished seams.
What is strong:
- packed-stream-to-WRAM materializer veneer
- tile orientation transforms
- tile-block materialization
- packed fragment/tile row workspace
- auxiliary VM request/control side

What is **not** strong yet is the final noun for every downstream record and emit structure.

---

# 5) What is still unresolved or only provisional

This section matters because the project is now at the stage where the unfinished work is more subtle and more expensive.

## A. Still-provisional master-opcode semantics
These areas still need caution or runtime confirmation:
- `0D`
- `0E`
- `14`
- `18`
- `1C`
- `1F`
- `44..4C`
- `54`
- `55`
- `76`

Reason:
- structural behavior is stronger than before
- but the final top-level contract or one anomalous byte path is still not clean enough to overstate

## B. Service-7 wrapper coverage is not complete
Current count is only:
- **5 / 8 service-7 wrappers**

That means service-7 is not “done” just because the main query families are strong.
There are still wrapper/controller edges left to settle.

## C. Final field nouns are still missing for key descriptor/work tables
These still need dedicated passes:
- exact field meanings inside the **17-byte `CC:213F` records**
- exact field meanings inside the **7-byte `CC:5E00` records**
- exact final nouns for `AE91..AE96`
- exact final nouns for `AE55` option bits beyond the already-strong parts
- final noun of the **fourth byte** in the per-packet 4-byte record family
- exact meaning of packet workspace modes **2** and **3**

## D. Late output-family noun is still not fully closed
The biggest unresolved late seam is still the final noun and ownership model around:
- `4943`
- `4500..`
- `5D00..`
- `A07B`
- downstream consumers of the packed/tile/auxiliary output path

There is now real evidence for a graphics/tile/sprite-oriented reading.
There is even good reason to keep checking whether the `4500..` 4-byte units are effectively OAM-like output records.
But the project is **not** at the point where that should be stated as final truth yet.

## E. Auxiliary VM is materially better, but not complete
The auxiliary command VM is no longer a mystery box.
But it is not fully complete.

Still left there:
- finish token `0x80` sub-dispatch middle-band semantics
- finish the `0x88..0x9F` command families
- settle the final noun for the `E500/E850` table family
- settle the final noun for the `9FFA` 8-byte strip
- settle the final noun for the `BB/BC` parallel-table families
- understand the `D1:E91A`, `D1:E899`, `D1:E8C1`, `D1:E984` JSL targets well enough to stop treating them as external opaque wrappers

## F. Bank separation is still very incomplete
This is one of the biggest reasons the completion score is still only ~60.9%.

Current bank-separation score is only **24.0%**.
That means:
- code vs data boundaries are still not fully formalized bank by bank
- local tables are not all split into clean assembler-ready units
- many blobs are still understood semantically but not fully reorganized for source lift

## G. Rebuild readiness is still low
This is the biggest remaining gap.

Current rebuild-readiness score is only **8.2%**.
That means the project is still far away from:
- full assembler-valid source lift
- clean file/folder source decomposition
- macro/include architecture
- reproducible binary rebuild
- validation against the original ROM

## H. Decompressor / format grammar work still remains
Even though parts of the late materialization side are much better, the project still needs:
- formal packed-stream grammar docs
- decompressor / unpacker format specification
- compressor-side confidence where relevant
- code/data boundary clarity around all packing pipelines

## I. Full bank-by-bank disassembly still remains
The project is not just “finish C1.”
A true complete disassembly still requires:
- all code banks split cleanly
- all major VMs and data formats mapped cleanly
- symbolized cross-bank ownership
- per-bank code/data maps
- validation passes over jumps, calls, and table roots

---

# 6) Immediate next recommended work

If continuing right now, this is the best next path.

## Priority 1: stay on the late graphics/output seam
This is the cleanest high-value seam left open from pass 81.

Read first:
1. `chrono_trigger_disasm_pass77.md`
2. `chrono_trigger_disasm_pass78.md`
3. `chrono_trigger_disasm_pass79.md`
4. `chrono_trigger_disasm_pass80.md`
5. `chrono_trigger_disasm_pass81.md`

Then attack:
- finish token `0x80` middle-band sub-ops
- finish `0x88..0x9F` command families
- tighten the `D1:E9xx` wrapper targets
- re-open `4943`
- re-open `4500.. / 5D00.. / A07B`
- prove or disprove the OAM-like reading of the 4-byte output records

## Priority 2: tighten unresolved descriptor/workspace nouns
After the above, tighten:
- `CC:213F` 17-byte records
- `CC:5E00` 7-byte records
- `AE91..AE96`
- packet byte-4 meaning
- packet modes 2 and 3

## Priority 3: close remaining service-7 wrappers
Do not forget this just because the late pipeline is interesting.
Service-7 wrapper coverage is still incomplete.

## Priority 4: start formal bank separation passes
The project is now at the point where more semantic gains should start being converted into actual bank-level structure.
If that does not begin soon, completion percentage will plateau even if labels keep improving.

---

# 7) Everything left before the project can honestly be called “complete”

This is the full remaining map.

## Phase 1 — finish unresolved semantics in the currently hot seam
- finish auxiliary VM command families
- finish late output-family nouns
- finish remaining service-7 wrappers
- runtime-confirm provisional opcodes and anomalous cases

## Phase 2 — formalize major data formats
- packed-stream grammar
- descriptor record specs
- packet record specs
- output-slot / emit-record specs
- any remaining selector/result list formats

## Phase 3 — bank-by-bank code/data separation
For each relevant bank:
- split executable code from tables
- identify pointer roots and table ranges
- label jump tables, local dispatchers, and external veneers
- produce clean bank maps

## Phase 4 — source lift and assembly structure
- assembler-targeted file layout
- macro/include layer
- constants / symbols / WRAM maps
- cross-bank call declarations
- local table extraction into assembler-valid sources

## Phase 5 — rebuild validation
- rebuild ROM
- compare against original
- fix any drift caused by mistaken code/data boundaries or mislabeled tables
- produce reproducibility notes

## Phase 6 — final artifact set
A truly complete Chrono Trigger disassembly should end with:
- rebuildable source tree
- per-bank code/data maps
- global symbol list
- subsystem architecture docs
- opcode reference docs
- decompression/materialization format docs
- WRAM structure docs
- validation notes
- explicit remaining uncertainty list, ideally very small

---

# 8) Session file inventory

## New pass research files created this session
- `chrono_trigger_disasm_pass62.md`
- `chrono_trigger_disasm_pass63.md`
- `chrono_trigger_disasm_pass64.md`
- `chrono_trigger_disasm_pass65.md`
- `chrono_trigger_disasm_pass66.md`
- `chrono_trigger_disasm_pass67.md`
- `chrono_trigger_disasm_pass68.md`
- `chrono_trigger_disasm_pass69.md`
- `chrono_trigger_disasm_pass70.md`
- `chrono_trigger_disasm_pass71.md`
- `chrono_trigger_disasm_pass72.md`
- `chrono_trigger_disasm_pass73.md`
- `chrono_trigger_disasm_pass74.md`
- `chrono_trigger_disasm_pass75.md`
- `chrono_trigger_disasm_pass76.md`
- `chrono_trigger_disasm_pass77.md`
- `chrono_trigger_disasm_pass78.md`
- `chrono_trigger_disasm_pass79.md`
- `chrono_trigger_disasm_pass80.md`
- `chrono_trigger_disasm_pass81.md`

## New label files created this session
- `chrono_trigger_labels_pass62.md`
- `chrono_trigger_labels_pass63.md`
- `chrono_trigger_labels_pass64.md`
- `chrono_trigger_labels_pass65.md`
- `chrono_trigger_labels_pass66.md`
- `chrono_trigger_labels_pass67.md`
- `chrono_trigger_labels_pass68.md`
- `chrono_trigger_labels_pass69.md`
- `chrono_trigger_labels_pass70.md`
- `chrono_trigger_labels_pass71.md`
- `chrono_trigger_labels_pass72.md`
- `chrono_trigger_labels_pass73.md`
- `chrono_trigger_labels_pass74.md`
- `chrono_trigger_labels_pass75.md`
- `chrono_trigger_labels_pass76.md`
- `chrono_trigger_labels_pass77.md`
- `chrono_trigger_labels_pass78.md`
- `chrono_trigger_labels_pass79.md`
- `chrono_trigger_labels_pass80.md`
- `chrono_trigger_labels_pass81.md`

## Canonical toolkit snapshots from this session
- `ct_disasm_toolkit_v5_updated_pass62.zip`
- `ct_disasm_toolkit_v5_updated_pass63.zip`
- `ct_disasm_toolkit_v5_updated_pass64.zip`
- `ct_disasm_toolkit_v5_updated_pass65.zip`
- `ct_disasm_toolkit_v5_updated_pass66.zip`
- `ct_disasm_toolkit_v5_updated_pass67.zip`
- `ct_disasm_toolkit_v5_updated_pass68.zip`
- `ct_disasm_toolkit_v5_updated_pass69.zip`
- `ct_disasm_toolkit_v5_updated_pass70.zip`
- `ct_disasm_toolkit_v5_updated_pass71.zip`
- `ct_disasm_toolkit_v5_updated_pass72.zip`
- `ct_disasm_toolkit_v5_updated_pass73.zip`
- `ct_disasm_toolkit_v5_updated_pass74.zip`
- `ct_disasm_toolkit_v5_updated_pass75.zip`
- `ct_disasm_toolkit_v5_updated_pass76.zip`
- `ct_disasm_toolkit_v5_updated_pass77.zip`
- `ct_disasm_toolkit_v5_updated_pass78.zip`
- `ct_disasm_toolkit_v5_updated_pass79.zip`
- `ct_disasm_toolkit_v5_updated_pass80.zip`
- `ct_disasm_toolkit_v5_updated_pass81.zip`

## Completion reports added this session
- `ct_completion_score_pass80.md`
- `ct_completion_score_pass81.md`

---

# 9) Bottom-line handoff summary

## What this session really achieved
This session:
- finished the **master opcode ownership story** for bank `C1`
- pushed global opcode coverage to **170 / 170**
- pushed selector-control coverage to **83 / 83**
- materially tightened late continuation, packet, and descriptor/output systems
- opened the strongest evidence yet that the late unresolved path is a **graphics/tile/sprite-oriented materialization pipeline**
- raised the conservative overall completion estimate from about **38%** to about **60.9%**

## What it did **not** achieve
This session did **not** complete:
- bank separation
- full format formalization
- final late output-family nouns
- full VM completion across all remaining engines
- source lift
- ROM rebuild

## What the next worker should believe
The next worker should assume:
- the project is now past the “what table even owns this opcode?” stage
- the project is now in the “finish late semantic seams, formalize formats, split banks, lift to source” stage
- progress will be slower and more expensive from here, because the remaining gaps are less about finding handlers and more about proving exact meaning and building rebuildable structure

---

# Final instruction
Treat this file as the **narrative state of the project after passes 62–81**.
When continuing:
- use this file for overall state and priorities
- use `chrono_trigger_master_index_handoff.md` as the topic map
- use the pass files for proof trails
- use the label files for naming state
- use `ct_disasm_toolkit_v5_updated_pass81.zip` as the canonical current toolkit snapshot
