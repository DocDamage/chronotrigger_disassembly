# Chrono Trigger (USA) ROM Disassembly — Detailed Session 4 Handoff

## Purpose
This is the **full narrative handoff for the work completed in this session**, covering the jump from **pass 82** to **pass 96**, plus the toolkit maintenance and runtime-evidence refreshes that happened on top of those passes.

Use this file to answer three things fast:
1. **What got done in this session?**
2. **Where is the disassembly right now?**
3. **What is still left before this can honestly be called a complete Chrono Trigger SNES ROM disassembly?**

This handoff is the direct follow-up to:
- `chrono_trigger_master_handoff_session3.md` — prior detailed session handoff ending at pass 81
- `ct_disasm_toolkit_v5_updated_pass96_runtime_evidence_refresh.zip` — current best toolkit snapshot from this session
- `ct_disasm_toolkit_v5_updated_pass96.zip` — plain pass-96 snapshot before the runtime-evidence refresh
- `work_pass96/ct_disasm_toolkit_v5_pass96/reports/ct_completion_score.md` — current weighted completion score
- `work_pass96/ct_disasm_toolkit_v5_pass96/notes/next_session_start_here.md` — current live seam note

---

## Mandatory context before anyone continues
Before doing more ROM work, refresh on the public Chrono Trigger modding / research context first.
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

Same rule as before:
**community context is vocabulary support, not proof.**
Final ownership, labels, and semantics should still come from direct ROM evidence.

---

# 1) Session scope

## Start state
This session started from the end of session 3:
- latest pass was **81**
- canonical toolkit snapshot was **`ct_disasm_toolkit_v5_updated_pass81 (1).zip`**
- completion estimate was about **~60.9%** under the old scoring model
- late unresolved work was centered on the downstream graphics / auxiliary-VM / D1 materialization side
- the late `CD` auxiliary VM, `D1` helper chain, and downstream workspace ownership were materially tighter than before, but the final output-side noun structure was still foggy

## End state
This session ended at:
- latest pass: **96**
- best current toolkit: **`ct_disasm_toolkit_v5_updated_pass96_runtime_evidence_refresh.zip`**
- latest plain pass snapshot: **`ct_disasm_toolkit_v5_updated_pass96.zip`**
- completion estimate: **~68.2%**

Current weighted breakdown:
- Label semantics: **76.9%**
- Opcode coverage: **92.5%**
- Bank separation: **38.1%**
- Rebuild readiness: **34.3%**

Current coverage counts:
- Master C1 opcodes: **170 / 170**
- Selector-control bytes: **83 / 83**
- Service-7 wrappers: **5 / 8**
- Banks represented in generated source: **15 / 66**
- Frozen/stable ranges: **447**
- Total label rows: **670**
- Strong labels: **459**
- Provisional labels: **141**
- Current non-strong rows: **192**
- Runtime evidence rows imported: **0**

## The blunt truth
This session was **not** a decorative note-taking session.
It did three important things:
1. It materially advanced the late graphics / raster / packet / sound-side semantics.
2. It corrected the toolkit so the completion score stopped underselling real progress.
3. It added a runtime-evidence layer so future passes can promote WRAM and packet labels with debugger-backed proof instead of pure static reasoning.

It also did **not** solve the hard endgame.
The project is still far from done in the byte-perfect rebuild sense.
The expensive final work is still:
- broad bank-by-bank code/data separation
- decompressor/data grammar ownership
- rebuildable source lift
- assembler integration and byte-accurate ROM proof
- debugger-backed RAM ownership validation

---

# 2) What was accomplished in this session

This session did six major things.

## A. It closed the pass-81 auxiliary-VM / D1 seam instead of letting it drift
Passes **82–85** finished the immediate seam behind the `CD` auxiliary token tail and the `D1:E8xx/E9xx` helper cluster.

Main outcomes:
- `D1:E91A / E899 / E8C1 / E984` were no longer vague downstream helpers
- the `0x80` sub-op tail stopped being “one more mystery wrapper area” and turned into exact reset / promote / seed / snapshot helpers
- `CFFF`, `CDC8`, and `CE0F` moved from anonymous gate bytes toward a real local control family
- the late `0xE0..0xE8` auxiliary token pocket became an actual mapped family instead of a junk drawer

This mattered because it stopped the late downstream control path from splintering into dozens of small fake nouns.

## B. It turned the D1 output side into a real column/lane/raster pipeline
Passes **86–90** materially upgraded the graphics / raster side.

Main outcomes:
- `CDC8` got its first exact external reader
- the `5DA0..5DA5` family stopped being vague “six bytes somewhere” and tightened into a current three-pair point bundle
- `CAEA..CAF5` became an indexed snapshot family for that bundle
- `D1:F8EB..FB67` resolved into a column-oriented sort / slope / rasterizer chain
- the `C161 / C163 / C4E1 / C4E3` neighborhood stopped looking like random WRAM and became a dual-bundle raster-target workspace with exact mirror helpers
- `D1:F331..F410` finally gave the local write-side cluster a caller-side orchestrator instead of leaving it as isolated math/emit bodies

This was the point where the downstream D1 side stopped being “graphics-adjacent helper soup” and started reading as a genuine staged lane/raster pipeline.

## C. It froze the CE/CD/C0/C2 follow-up chain into a real downstream packet/stream pipeline
Passes **91–93** cracked the downstream tail that sits after the D1 writer/orchestrator side.

Main outcomes:
- `CE:EE6E` was frozen as a nine-record template seeder into `7E:C867..C9EC`
- `CD:0235 / 0239` stopped being vague bridge addresses and became a real contiguous eight-strip workspace clear path for `B400..B7FF`
- `C0:0008` and `C0:000B` stopped being mystery low-bank jumps and became exact one-packet / multi-packet C7-submit veneers
- `CD:025E..0295` became a shared selector/workspace setup helper for the `020C..0214` family
- `C2:0003 / 0009` became exact veneers into a real stream-state initializer and four-family token/stream dispatcher
- `C7:0004` became an exact veneer into the low-bank packet dispatcher

This was the point where the downstream bridge stopped being a list of addresses and became a coherent staged engine path.

## D. It promoted the C7 low-bank side from “generic packet machinery” to a real sound/APU command pipeline
Passes **94–96** were the biggest subsystem noun upgrade of the session.

Main outcomes:
- the `C7:0140` dispatcher is now clearly on the **sound/APU command** side
- `C7:0755` and `C7:08E3` were proven as exact APU-port handlers through `$2140..$2143`
- `1E00..` is now best read as a low-bank sound/APU command packet workspace
- `1E20..1E63` is now a live sound-slot selector/base/end strip family
- the negative-`1E05` special path (`01A1`) was cracked into real stages: candidate rebuild, reconcile/migration, staged command-`0x02` emit, post-emit tail, per-slot command-`0x03` helper, handshake gate, and immediate-family bridge pieces
- `C7:04B1..061B`, `0655`, `0734`, and `0A39` stopped being honest unknowns

This is the biggest semantic change of the whole session.
The C7 side is no longer honestly describable as “low-bank packet stuff.”
It is now a real staged **sound/APU command pipeline**.

## E. It fixed the toolkit so the completion metric stopped lying
A tooling refresh was done after pass 95 because the percentage had been stuck in a misleading way.

Main outcomes:
- the score script stopped hard-coding `bank_separation` and `rebuild_readiness`
- workspace/state propagation stopped advertising stale pass-93-era defaults
- a dispatcher-family report was added for veneer / packet / opcode-family work
- a focused sound/APU packet summary report was added for the C7 command side
- a dispatcher tracer helper was added

This matters because the old ~61% number was under-reporting real progress.
After the metric correction, the project read much closer to the true semantic state.

## F. It added a real runtime-evidence layer instead of just talking about one
A second tooling refresh was done on top of pass 96.

Main outcomes:
- recursive runtime trace import under `traces/imported/`
- richer CSV / JSON / text debugger import
- weighted runtime validation
- generated runtime capture plan tied to the live seam
- new WRAM/APU trace templates and bsnes-plus capture checklist
- updated resume/bootstrap so runtime work is now part of the normal workflow

This matters because the project had gotten strong on static labels but weak on debugger-backed proof.
That is no longer a tooling excuse.
The templates and import layer now exist.

---

# 3) Detailed pass-by-pass summary for this session

## Pass 82
Main upgrades:
- tightened the `D1:E8xx/E9xx` helpers behind auxiliary token `0x80`
- `D1:E899` and `D1:E8C1` froze as exact `0x7FFF` sentinel-fill helpers
- `D1:E91A` and `D1:E984` froze as a complementary promote/copy vs seed/snapshot pair
- `D0:FD00..FD5F` tightened as a fixed 48-color ROM seed block consumed by `D1:E984`

Why it mattered:
- stopped the `0x80` sub-op seam from remaining fuzzy after pass 81

## Pass 83
Main upgrades:
- `D1:F411` froze as the eight-header snapshot of `0520 + n*0C`
- `D1:F431` froze as the suspend half of the gate
- `D1:F457` froze as the restore half
- `CFFF` tightened as the suspend/restore selector byte
- corrected the header mirror width from `CD2F..CD34` to `CD2F..CD36`

Why it mattered:
- turned the late D1 gate from vague stateful behavior into an exact arm/suspend/restore contract

## Pass 84
Main upgrades:
- `CFFF` got exact writers in both script VMs
- auxiliary token `0xE6` froze as a direct streamed-immediate writer to `CFFF`
- `C1:58DB` and `C1:58E4` froze as hard set / hard clear helpers
- `CDC8` tightened as the local seed-vs-promote phase byte
- `CE0F` tightened as a seed-side arm/epoch byte

Why it mattered:
- promoted `CFFF / CDC8 / CE0F` from anonymous control bytes into a real local control neighborhood

## Pass 85
Main upgrades:
- mapped the late aux token tail `0xE0..0xE8`
- exact wrappers for `E8`, `E7`, `E0`
- exact immediate/state helpers for `E5`, `E4`, `E3`, `E2`, `E1`

Why it mattered:
- removed the last “junk drawer” feeling from that auxiliary token pocket

## Pass 86
Main upgrades:
- first exact external reader of `CDC8` at `CE:E18E..E1A4`
- `5DA0..5DA5` tightened into a current three-pair point bundle
- `CAEA..CAF5` tightened into indexed snapshot records for that bundle
- `D1:F5CD..F5F2` froze as an exact D1 snapshot helper for the family

Why it mattered:
- gave the D1 downstream seam a real data model instead of abstract scratch-space labels

## Pass 87
Main upgrades:
- `D1:F8EB..F91B` froze as an in-place sort of four point pairs by the second byte
- `D1:F972..F9AE` froze as a row-per-column hardware-divide slope helper
- `D1:F9E7..FB67` froze as a three-case column rasterizer
- corrected the bundle interpretation toward `row/Y-like` vs `column/X-like`

Why it mattered:
- proved the seam is column-oriented raster work, not some generic scanline-ish math blob

## Pass 88
Main upgrades:
- `C161 / C163 / C4E1 / C4E3` resolved into a dual-bundle eight-table raster-target workspace
- `CE:E000..E08D`, `D1:F5F6..F676`, and `D1:FD80..FE46` froze as exact mirror helpers
- `7C.bit0` froze as the direction selector for those mirror helpers

Why it mattered:
- gave the downstream raster workspace real ownership and exact mirror behavior

## Pass 89
Main upgrades:
- `D1:EDCD..EE2F` froze as a clamped lower-edge byte stamp
- `D1:EE33..EE95` froze as a clamped companion word-span fill
- `D1:EEC5..F107` froze as the first four primary lanes’ curve/profile writer

Why it mattered:
- closed the writer side of the newly owned raster-target workspace

## Pass 90
Main upgrades:
- `D1:F331..F410` froze as the missing local orchestrator
- `D1:F83D..F8EA` froze as a `C030..C14F` quartet-table seed helper
- `D1:F47C..F4BF` froze as the `CA5A / CA5C` masked-pair staging path

Why it mattered:
- finally gave the lane/raster writer cluster a caller-side contract instead of leaving it as isolated local writers

## Pass 91
Main upgrades:
- `CE:EE6E..EF0D` froze as a 9-record template seeder into `C867..C9EC`
- `CD:0239..025D` froze as the exact `B400..B7FF` eight-strip clear
- `C0:1BAB` froze as a conditional one-packet `C7:0004` submit helper

Why it mattered:
- mapped the first downstream bridge after D1 into real CE/CD/C0/C7 actions

## Pass 92
Main upgrades:
- `CD:025E..0295` froze as a shared selector/workspace setup helper
- `C0:1BE6..1CFB` froze as a gated multi-packet `C7:0004` submit helper
- the default `bit6 == 0` path was shown to submit an exact 5-packet sequence

Why it mattered:
- the downstream tail stopped bottlenecking on unnamed local helpers

## Pass 93
Main upgrades:
- `C2:0003` froze as a veneer to `C2:57DF`
- `C2:0009` froze as a veneer to `C2:5823`
- `C2:57DF..5822` froze as a stream-state initializer
- `C2:5823..5841` froze as a four-family token/stream dispatcher
- `C7:0004` froze as a veneer to `C7:0140`
- new source bank files were opened for `00`, `C2`, and `C7`

Why it mattered:
- turned raw dispatcher slots into named stages and pushed source-tree coverage forward

## Pass 94
Main upgrades:
- `C7:0755` froze as exact opcode-`0x71` table-driven APU burst sender
- `C7:08E3` froze as exact opcode-`0x70` APU handshake / packet sender
- `C7:0AD9` froze as the exact `0x10..0x17` gate table
- `C2:58B2..5902` froze as the primary stream-token consumer / dispatcher

Why it mattered:
- promoted the C7 side to a real sound/APU command subsystem

## Pass 95
Main upgrades:
- `C2:5BF5 / 5C3E / 5C77` froze as a chained three-family long-stream stage
- `C2:5D1D..5D55` froze as the bounded sentinel-scan helper cluster
- `C7:01A1..0216` froze as the candidate rebuild / staging gate of the negative-`1E05` path
- `C7:0217..0325` froze as the live-slot reconcile / migration phase using APU command `0x07`
- `C7:037B..04B0` froze as the staged command-`0x02` emit phase over `1F80..`

Why it mattered:
- crossed the structural threshold where the `01A1` branch was no longer just “the active half of an early gate”

## Toolkit maintenance refresh (post pass 95)
Main upgrades:
- evidence-weighted completion scoring
- dispatcher-family report
- APU packet summary
- interactive dispatcher tracer
- fixed stale workspace propagation

Why it mattered:
- the percentage stopped lying as badly, and dispatcher-heavy work got better tooling

## Pass 96
Main upgrades:
- `C7:04B1..061B` froze as the exact post-emit tail of the negative-`1E05` special path
- `C7:0655..071C` froze as the per-slot command-`0x03` table-stream helper
- `C7:0734` tightened to an exact `1E00 |= 0x04` effect in the current ROM image
- `C7:0A39..0A97` froze as the selector-table-backed APU handshake gate
- the `0x18..0x3F` bridge tightened materially through exact labels at `061C..064F` and `071D..0733`

Why it mattered:
- it removed the last honest helper fog around the negative-`1E05` C7 seam and left a very clear next step

## Runtime-evidence refresh (post pass 96)
Main upgrades:
- recursive trace import
- weighted runtime validation
- generated runtime capture plan
- new WRAM/APU trace templates and watch presets

Why it mattered:
- the toolkit now supports live debugger evidence properly instead of just static reasoning

---

# 4) Where the disassembly stands now

## The strongest current subsystem nouns
These are the biggest keepable project-level truths coming out of this session.

### A. The D1 late downstream side is a real staged raster/lane pipeline
This is no longer honest helper fog.
The project now has exact ownership for:
- point-bundle capture/snapshot work
- sort / slope / rasterizer math
- dual-bundle raster-target workspace mirrors
- primary-lane builder / stamp / span / curve/profile writer
- local orchestrator / seed path / downstream bridge

### B. The CE/CD/C0/C2 tail is a real downstream stream/packet follow-up chain
This is now materially tighter than it was at pass 81.
There is now exact ownership for:
- CE template record seeding
- CD workspace clear/setup helpers
- C0 one-packet and multi-packet submission helpers
- C2 stream-state initialization and downstream family dispatch

### C. The C7 low-bank side is now clearly a sound/APU command subsystem
This is the biggest noun upgrade of the session.
Current strongest safe reading:
- `1E00..` = low-bank sound/APU command packet header/workspace
- `1E20..1E63` = live sound-slot selector/base/end strip family
- `1F00..1FC0` = candidate/unmatched/emit staging strips for the negative-`1E05` path
- `C7:0140` = low-bank sound/APU opcode-family dispatcher
- `0x70` and `0x71` = exact APU-port handlers
- negative-`1E05` = exact staged special path with rebuild, reconcile, emit, tail, and handshake helpers

### D. The toolkit is materially healthier than it was at the start of the session
The project now has:
- corrected scoring
- dispatcher-family report
- sound/APU packet summary report
- runtime capture plan
- runtime trace templates
- improved import/validation path for debugger evidence

---

# 5) No-BS status against the actual “complete disassembly” checklist

## 1. Symbol mapping and labeling
**Status: strong, but incomplete.**

What is true now:
- symbol work is one of the project’s strongest areas
- there are **670 total label rows**
- **459** are strong
- **141** are provisional
- all **170/170** master C1 opcodes are covered
- all **83/83** selector-control bytes are covered

What is still left:
- **192 non-strong rows** remain
- several late WRAM and low-bank packet families still need final gameplay-facing nouns
- top unresolved bank pressure is still concentrated in:
  - `7E` (**134** unresolved/provisional rows)
  - `C1` (**29**)
  - `FD` (**10**)
  - `D1` (**8**)

## 2. RAM map construction
**Status: underway, but under-validated.**

What is true now:
- large chunks of WRAM are meaningfully labeled
- `7E` has **226 source-represented rows** in the scaffold tree
- key runtime/state families on `7E` and low bank `00` are now structurally mapped

What is still left:
- runtime evidence rows are still **0**
- a lot of WRAM ownership is still static-inference-first, not trace-backed
- the toolkit now supports debugger capture, but the actual imports still need to be done

This is one of the biggest remaining quality gaps.

## 3. Data extraction (graphics, audio, maps, formats)
**Status: partial.**

What is true now:
- graphics/output-oriented downstream work advanced materially this session
- the sound/APU command side made a real leap
- several table/pointer families are now exact enough to stop calling them “mystery data”

What is still left:
- decompressor grammar / format work is still not broadly finished
- map/level data ownership is not broadly solved
- graphics/tile/materialization data is improved but not globally decoded
- sound sequence/sample ownership is far from fully solved even though the low-bank APU command side is much tighter now

## 4. Re-assemblability
**Status: not there yet.**

What is true now:
- there is a scaffold-first source tree
- banks represented in source: **15 / 66**
- rebuild mode is still **scaffold**
- rebuild readiness is only **34.3%**
- rebuild/diff reports exist and are part of the workflow

What is still left:
- broad source lift across untouched banks
- code/data boundary proof across the ROM
- assembler integration work
- byte-for-byte rebuild validation against the original ROM

This is still the single hardest “acid test” gap.

## 5. Documentation and tools
**Status: strong and improving.**

What is true now:
- pass writeups exist through pass 96
- merged labels report exists
- unresolved dashboard exists
- dispatcher-family report exists
- sound/APU packet summary exists
- source state, rebuild diff, graph summary, workspace report, and runtime plan exist
- runtime templates and import path now exist

What is still left:
- keep the reports honest as the project broadens beyond the current seam
- continue turning repeated manual analysis patterns into helper scripts only when they actually buy time

---

# 6) Current live seam and what to do next

## The exact live seam right now
From `notes/next_session_start_here.md`:

1. **Tighten `0155` and the immediate bridge around the `0x18..0x3F` family**
2. **Then go back to `CE0F`**
3. **Do not go broad while the C7 seam is still warm**

That is still the right call.

## Why this is the right next move
Because the C7 send path now has the supporting helper fog removed.
The next step is no longer blocked by anonymous local helpers.
That means the highest-value next work is:
- finish the immediate-family bridge and `0155`
- freeze the remaining exact control behavior in the C7 send path
- then return to `CE0F` with much less ambiguity than before

## Suggested next-session order
1. Stay on the **C7 low-bank immediate bridge** first.
2. Use the dispatcher-family report while doing that.
3. If static naming stalls, take a runtime capture using the new C7/APU trace template.
4. Once the C7 bridge is tighter, return to the **`CDC8 / CE0F / CFFF`** control family with runtime support if needed.
5. Only then widen back out into broader unresolved bank pressure.

---

# 7) Top unresolved work right now

## Immediate unresolved items near the live seam
- `00:1E20..00:1E63` — live sound-slot selector/base/end strip family is still provisional even though its structure is much tighter now
- `00:1F00..00:1FC0` — candidate/unmatched/emit staging strips are still provisional at the final gameplay-facing noun level
- `00:1E00..00:1E10` — low-bank sound/APU command packet workspace still wants final user-facing field nouns
- `7E:0237..7E:023A` — C2 active long-stream cursor/counter family still wants a more final engine-facing noun
- `7E:020C..7E:0214` — shared C2 packet workspace still wants tighter final field ownership
- `CE0F` — still lacks the first fully frozen clean-code external reader path needed to settle its final noun

## Structural unresolved pressure by bank
Current unresolved/provisional pressure:
- `00`: **4**
- `7E`: **134**
- `7F`: **1**
- `C0`: **2**
- `C1`: **29**
- `CC`: **3**
- `CD`: **1**
- `D1`: **8**
- `FD`: **10**

## Bigger project-scale unresolved work
These are the real endgame items, not just the next seam.

### A. Broad bank separation
Still required:
- continue code/data ownership across untouched banks
- lift more banks into source form
- keep proving boundaries instead of hand-waving them

### B. Rebuildable source tree
Still required:
- expand source representation beyond the current 15 banks
- grow from scaffold to assembler-credible source
- run byte-accurate diff/rebuild proof

### C. Decompressor / format work
Still required:
- global graphics/data grammar ownership
- compressed asset format ownership
- broader map/data extraction work

### D. Runtime proof
Still required:
- import actual debugger traces
- validate WRAM ownership with live evidence
- validate C7/APU packet behavior with real `$2140..$2143` traffic captures

---

# 8) Toolkit state and how to use it now

## Best current bundle
Use:
- **`ct_disasm_toolkit_v5_updated_pass96_runtime_evidence_refresh.zip`**

That is the best current “resume from here” toolkit bundle.

## Important reports/files to read first after unzipping
1. `notes/next_session_start_here.md`
2. `reports/ct_completion_score.md`
3. `reports/ct_workspace_report.md`
4. `reports/ct_unresolved_dashboard.md`
5. `reports/ct_dispatch_family_report.md`
6. `reports/ct_apu_packet_summary.md`
7. `reports/runtime/runtime_capture_plan.md`
8. `notes/runtime_evidence_workflow.md`

## Recommended first commands after unzipping
```bash
python3 scripts/ct_resume_workspace.py --workdir .
python3 scripts/ct_trace_dispatcher.py --label apu
python3 scripts/ct_trace_dispatcher.py --address C7:01A1
```

If runtime evidence is needed next:
```bash
# import debugger exports into traces/imported/
python3 scripts/ct_resume_workspace.py --workdir .
```

## Toolkit refresh policy going forward
Toolkit updates should continue to happen **when they buy real gains**, not just for noise.
Good reasons to update the toolkit:
- a metric/report is misleading
- a repeated manual dispatcher pattern deserves automation
- a subsystem is mature enough to justify a dedicated report/helper
- stale state risks sending the next pass down the wrong seam

That rule was followed in this session and should continue.

---

# 9) Honest project status in one paragraph
The project is now in a much better state than it was at pass 81.
The late downstream graphics/raster side is materially tighter, the CE/CD/C0/C2 bridge is much less mysterious, and the C7 low-bank side has crossed into a real sound/APU command subsystem with staged packet semantics instead of vague helper fog. The toolkit is better too: the completion score is less misleading, dispatcher-heavy work has dedicated reports, and runtime capture/import support now exists. But the project is **not done**. The hard endgame is still broad bank separation, decompressor/data grammar work, runtime-backed WRAM ownership, and especially rebuildable source proof. Right now the project is best described as a **strong, deeply structured, semantically advanced disassembly-in-progress**, not a finished byte-perfect disassembly.

---

# 10) Resume instruction for the next chat
Use the refreshed toolkit, resume at pass 96 state, stay on the C7 low-bank immediate bridge first, then return to `CE0F`, and do **not** go broad until that seam is colder.
