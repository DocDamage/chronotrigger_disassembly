# Chrono Trigger (USA) ROM Disassembly — Detailed Session 8 Handoff

## Purpose
This is the full handoff for the work completed after **session 7**, covering:
- disassembly progress from **pass 140** through **pass 150**
- the toolkit upgrades and release refreshes that happened during this run
- the exact current project state at the end of pass 150
- the honest remaining work before this can be called a **complete Chrono Trigger SNES ROM disassembly**

Use this handoff to answer three things fast:
1. **What got done in this session?**
2. **Where is the disassembly right now?**
3. **What still has to happen before the Chrono Trigger ROM is actually finished and rebuild-ready?**

This handoff is the direct follow-up to:
- `chrono_trigger_master_handoff_session7.md`
- `ct_disasm_toolkit_v6_pass139_continued.zip`

---

## Mandatory context before anyone continues
Same rule as the prior sessions:
refresh on public Chrono Trigger research/modding context before pushing new claims.

Priority external context to refresh:
- Chrono Compendium
- Data Crystal
- Temporal Flux / Kajar Labs / older forum material
- bsnes / bsnes-plus / Geiger-style debugger workflows

Reason:
- prevents fake novelty
- prevents inventing subsystem names that already exist in community research
- keeps community shorthand separate from ROM-proof ownership

Community context is still **vocabulary support, not proof**.
Final labels, subsystem ownership, rebuild claims, and handoff claims still need to come from ROM evidence and the project’s own artifacts.

---

# 1) Session scope

## Start state
This session started from the end of session 7:
- latest pass: **139**
- current best toolkit snapshot at start: **`ct_disasm_toolkit_v6_pass139_continued.zip`**
- current live seam at start: **`C2:DE98..C2:DF76`**
- completion estimate at start: **69.7%**
- label rows at start: **1111**
- strong labels at start: **822**
- caution labels at start: **51**
- toolkit doctor health at start: **100.0%**

## End state
This session ends at:
- latest pass: **150**
- current best toolkit snapshot: **`ct_disasm_toolkit_v6_7_pass150_upgraded.zip`**
- current toolkit version: **v6.7**
- current completion estimate: **70.6%**
- label rows: **1237**
- strong labels: **947**
- provisional labels: **150**
- alias labels: **19**
- caution labels: **52**
- toolkit doctor health score: **100.0%**
- release audit health score: **100.0%**
- current canonical next seam: **`C2:F2F3..C2:F360`**

## The blunt truth
This session was real progress, but it still did **not** finish the project.

It did five important things:
1. it pushed the live C2-side callable/helper/materializer families from **`C2:DE98`** all the way through **`C2:F2F2`**
2. it corrected a long chain of fake seam boundaries where the old seam ended one byte or one owner too early
3. it converted more local packet emitters, selector tables, interpreter lanes, tile/BCD formatters, and strip/materialization helpers into exact callable owners/helpers/tables
4. it hardened and then refreshed the toolkit so the current downloadable release finally matches the real workspace again at **pass 150**
5. it left the project in a cleaner, more honest state than the session started

It did **not** solve the endgame.
The expensive remaining work is still:
- broad bank-by-bank code/data separation outside the recently-closed C2 families
- runtime-backed WRAM proof for the still-open system nouns
- decompressor/data grammar ownership and asset-format understanding
- source-tree expansion into something truly assembler-ready instead of a starter scaffold
- assembler integration, bounded-diff reporting, and eventually zero-diff rebuild verification

---

# 2) Toolkit work completed this session

The toolkit did not stay static. It evolved during the session from the old session-7 baseline into the new **v6.7** release.

## v6.3 — release drift + seam acceleration
Delivered at pass 142.

What changed:
- release-drift checking tightened
- a seam-candidate lane was added so likely callable starts inside the live seam show up faster
- packaging and audit behavior were improved so stale release assumptions are easier to catch

Practical effect:
- less blind seam-triage work
- easier detection of wrong seam ends before the next pass ships

## v6.4 — pass finalization lane
Delivered at pass 143.

What changed:
- a one-command finalizer lane was added so post-pass sync, smoke, audit, and packaging can happen together
- state sync stopped collapsing the toolkit version back to a generic older value
- stale smoke metadata stopped being treated as “good enough” for release packaging

Practical effect:
- per-pass closeout became more reproducible
- release refreshes stopped depending on memory and luck

## v6.5 — seam parser/state-sync fixes
Delivered at pass 144.

What changed:
- seam parsing was tightened so `current_live_seam` keeps the real seam range instead of flattening prose
- toolkit-version persistence was tightened across state refreshes
- smoke refresh started honoring the real live seam instead of stale seam text

Practical effect:
- state and reports became materially less likely to lie about the current seam

## v6.6 — seam-edge lookahead
Delivered at pass 145.

What changed:
- seam candidate generation gained a short lookahead window past the declared seam end
- that specifically targeted the recurring project failure mode where the seam stopped one owner too early

Practical effect:
- better detection of “the next byte is actually still live code” cases
- cleaner handoff continuity from pass to pass

## Toolkit freeze period
From passes **146 through 150**, the toolkit was intentionally left frozen because that was the user instruction during those passes.

That means:
- the static disassembly kept moving
- the pass-specific artifacts kept updating
- but the downloadable packaged toolkit stayed behind at the last refreshed release until now

## v6.7 — session-close refresh + handoff generation
Delivered now, at the end of pass 150.

What changed:
- the toolkit release was refreshed forward to **pass 150** so the downloadable zip finally matches the current workspace again
- a new handoff-generation lane was added:
  - `scripts/ct_generate_master_handoff.py`
  - `windows/run_generate_master_handoff.bat`
- README / manifest / wrapper coverage were updated for the new lane
- the packaged toolkit now ships with:
  - current state at **pass 150**
  - current seam at **`C2:F2F3..C2:F360`**
  - fresh smoke results
  - fresh release audit
  - toolkit doctor at **100.0%**

Practical effect:
- future full-session restarts are easier to produce from inside the toolkit itself
- the shipped toolkit is no longer lagging five passes behind the real workspace

---

# 3) What was accomplished in this session

## Session-wide net result
Across passes **140–150**, the work kept moving downstream inside the same broad C2-side system family that session 7 had already been tightening.

The repeated pattern was:
- pick up the next live seam
- prove the old seam end was too short, too long, or split at the wrong byte
- widen or tighten the seam to the real callable/helper/data family
- freeze local tables, selector packets, interpreter lanes, wrapper entries, and helper tails exactly
- move the next seam further downstream

That happened over and over from **`C2:DE98`** through **`C2:F2F2`**.

Net result:
- one long downstream family chain in bank C2 is now materially better owned
- multiple fake seam edges were killed
- exact callable late entries and local data tables were separated from live code much more cleanly
- the next session starts from a smaller, sharper live target instead of a stale broad guess

---

# 4) Exact pass ledger for this session

## Pass 140
Closed the exact follow-on family left open by session 7 at **`C2:DE98..C2:DF76`**.

What froze:
- `C2:DE98..C2:DECB` exact `0D88`-checked sibling refresh owner
- `C2:DECC..C2:DF30` shared exact `5600/5700` build-refresh helper
- `C2:DF31..C2:DF50` shared exact eight-pass export driver
- `C2:DF51..C2:DF75` shared exact `5600` entry loader/materializer helper

Important correction:
- `C2:DF76` was **not** part of the old seam; it was the first byte of the next owner

Net effect:
- the session-7 seam was honestly closed
- the next live seam moved to **`C2:DF76..C2:E095`**

## Pass 141
Closed the follow-on family starting at **`C2:DF76`**, but also proved the old seam end at **`E095`** was too short.

What froze:
- threshold-recovery owner
- local 5-word selector table
- restore/clear/import helper
- selector-packet wrapper
- direct tail wrapper
- `104D`-window export owner
- row-pointer helper
- bounded `104D` export helper
- negative refresh/export owner
- short marker/finalizer wrapper
- cyclic selector-step owner
- short latched-selector marker-writer wrapper

Important correction:
- the honest closure ran through **`C2:E162`**, not `E095`

Net effect:
- the next live seam moved to **`C2:E163..C2:E34A`**

## Pass 142
Closed the next mini-family at **`C2:E163..C2:E349`** and corrected the seam in the opposite direction.

What froze:
- selected-entry loader owner
- partial slot-reseed / marker-refresh owner
- local selector table
- lane chooser / setup tail / poll owner cluster
- `0D1E`-dispatched owner
- local indirect dispatch table
- overlapping updater pairs for `0F09` and `0F08`
- `0D1D`-gated tail/refill dispatcher
- lookup-backed `0F00` fill helper

Important correction:
- `C2:E34A` was the first byte of the next owner, so the old seam was **one byte too long**

Net effect:
- the next live seam moved to **`C2:E34A..C2:E5F0`**
- toolkit **v6.3** shipped here

## Pass 143
Closed the front callable/helper family left open at **`C2:E34A..C2:E5F0`** and proved the back edge was too short.

What froze:
- count-capped offset writer
- normalize/compare/fallback-copy owner
- compact-list normalizer
- overlapping row-match helper pair
- large setup/import/selector-emission owner
- local selector packet
- `9890` table-materialization helper
- zero-lane import/staging owner
- `(54 + 1)` change-handler / refresh owner

Important correction:
- the honest closure ran through **`C2:E60A`**

Net effect:
- the next live seam moved to **`C2:E60B..C2:E760`**
- toolkit **v6.4** shipped here

## Pass 144
Closed the family around **`C2:E60B..C2:E840`** and corrected the seam on both ends.

What froze:
- local 4-word dispatch table
- short wrapper at `E613`
- `0420/0D1D`-gated dispatcher
- slot-scan / packet-emitter owner
- sibling `0D1D`-gated dispatcher with overflow handoff
- overflow clear/reset wrapper
- service owner with forced selector lane
- cyclic occupied-slot search / state-refresh / strip-expansion owner
- `30:7FE0`-indexed setup/export owner

Important corrections:
- the seam began with a table, not one weird owner
- the old seam end at `E760` was too short; the family ran through **`E840`**

Net effect:
- the next live seam moved to **`C2:E841..C2:E923`**
- toolkit **v6.5** shipped here

## Pass 145
Closed the family left open at **`C2:E841..C2:E923`**, then proved `E923` itself was not a stop.

What froze:
- setup owner
- local selector packet
- fast-lane owner
- selected-slot clear / pointer-build owner with overlapping late entries
- local 7-byte data span
- poll-loop wrapper
- short wrapper at `E923`
- workspace reset / indexed seed owner
- wait loop
- `0D1D` rebuild owner
- local 9-byte table
- `F5`-bit scan / 4-way dispatch owner
- local dispatch table
- low-byte-times-6 helper
- overlapping table-byte loader quartet
- sign/bounds helper
- delta / hardware-division helper
- short wrapper into `EB03`

Important correction:
- the honest closure ran through **`C2:EAC1`**

Net effect:
- the next live seam moved to **`C2:EAC2..C2:EB9A`**
- toolkit **v6.6** shipped here

## Pass 146
Closed the wrapper/packet family at **`C2:EAC2..C2:EB9A`**.

What froze:
- two sibling short wrappers
- one bit-gated packet wrapper
- one overlapping packet-wrapper late entry
- one gated packet-emitter helper
- one signed table-walk / 3-byte record builder owner

Net effect:
- the next live seam moved to **`C2:EB9B..C2:EC37`**
- toolkit stayed frozen by instruction

## Pass 147
Closed the family at **`C2:EB9B..C2:EC37`** and the spillover beyond it through **`C2:ED30`**.

What froze:
- WRAM strip / stepped-loop seed helper
- six-row ascending-word writer plus FF-bank importer
- counted row-stride wrapper
- paired odd-byte fill helper
- paired odd-byte nibble-merge helper
- bank-7E setup owner deriving `0D47/0D48`
- FF-bank 16-byte importer keyed by `0D8C/0D48`

Important correction:
- the old seam end at `EC37` was too short; `EC38` was already live code

Net effect:
- the next live seam moved to **`C2:ED31..C2:EE7F`**

## Pass 148
Closed the family at **`C2:ED31..C2:EE7F`** and the spillover through **`C2:EF64`**.

What froze:
- FF-bank command-stream dispatcher
- local 11-word command dispatch table
- short FF→7E record importer late entry
- repeated seed-word strip materializer
- packed row/column-to-pointer builder
- short wrapper pair
- derived-extent owner
- packet/fallback staging owner
- row-band builder owner
- spillover post-adjust copy helper
- local 16-byte template selector table
- coordinate-to-coordinate row-band copy owner
- multi-row 7E→7E block copier
- FF-table selected front-end into `EF65`

Important correction:
- the old seam end at `EE7F` was too short; the callable/helper closure really ran through **`EF64`**

Net effect:
- the next live seam moved to **`C2:EF65..C2:F00F`**

## Pass 149
Closed the script/template interpreter family at **`C2:EF65..C2:F113`**.

What froze:
- FF-bank script/template interpreter front-end
- byte-token interpreter loop
- paired-byte writer with optional sentinel shadow mirror
- local opcode-dispatch helper
- local 16-word opcode-handler table
- signed-mode write-pointer step helper
- inline offset-to-write-pointer helper
- two-word wrapper into `F114`
- pointed-script wrapper into `EF7E`
- local `7E`-bank five-step subscript expander
- single-byte latch helper
- pointed-word importer/writer
- repeated sentinel-pair emitter
- masked-flag import helper
- mode/flag latch helper
- two-word wrapper into `F227`
- indexed-threshold gate owner with fallback packet materializer

Important correction:
- the old seam end at `F00F` was too short; the family ran through **`F113`**

Net effect:
- the next live seam moved to **`C2:F114..C2:F24A`**

## Pass 150
Closed the numeric/formatter family at **`C2:F114..C2:F2F2`**.

What froze:
- packed-bitfield-to-BCD front-end owner
- packed-bitfield-to-BCD accumulator helper
- packed-BCD powers-of-two table
- bank-7E BCD nibble-decode/materialize helper
- nibble/blank-flag tile-pair writer
- sibling fixed-value writer owner
- fixed-width bank-7E nibble/tile materializer helper
- nibble-to-tile-pair writer helper
- local nibble/tile table
- two-field formatter owner
- two-decimal-byte-to-binary helper
- indexed wrapper into `EF65`
- `7D00`-table selector helper

Important correction:
- the old seam end at `F24A` was too short; the honest closure ran through **`F2F2`**

Net effect:
- the next live seam moved to **`C2:F2F3..C2:F360`**
- this is the exact current restart point

---

# 5) Where we are now

## Current canonical restart target
The next live seam is:
- **`C2:F2F3..C2:F360`**

Immediate structural anchors already visible there:
- exact owner entry at **`C2:F2F3`**
- exact short base-copy helper at **`C2:F333`**
- exact sibling owner at **`C2:F338`**
- immediate lookahead heat just beyond the seam at **`C2:F378`**

## Current measurable project state
From the refreshed toolkit state and score:
- latest pass: **150**
- overall completion estimate: **70.6%**
- label semantics score: **81.4%**
- opcode coverage score: **92.5%**
- bank separation score: **40.8%**
- rebuild readiness score: **37.8%**
- master C1 opcodes covered: **170 / 170**
- selector-control bytes covered: **83 / 83**
- service-7 wrappers covered: **5 / 8**
- banks represented in generated source: **15 / 66**
- frozen/stable ranges: **919** (**74.3%** of label rows)
- runtime validation rows: **0 / 0**
- runtime linked labels: **0**
- rebuild mode: **starter**

## Honesty note on progress vs finish line
The score moving from **69.7%** to **70.6%** is real, but it also shows the project’s actual shape:
- semantic/static ownership in the recent C2 family is improving well
- opcode coverage is already strong
- the hard part now is **not** “find another obvious helper in bank C2”
- the hard part is the expensive finish work: more banks, more runtime proof, more rebuildability, more exact code/data separation, and a real assembler path

---

# 6) What still needs to happen before the Chrono Trigger ROM is actually finished

## A. Finish the current live seam and its immediate spillover
Immediate next task:
- close **`C2:F2F3..C2:F360`** honestly
- do not stop early if the real owner/helper chain keeps running into **`F378`** or beyond

## B. Keep widening exact code/data separation outside the recent C2 strip
What remains:
- more untouched or weakly-classified ROM territory still needs bank-by-bank separation
- more mixed code/data spans need exact table vs helper vs owner identification
- more local packet/data spans need to be proven as data, not reopened as fake code

## C. Tighten broader subsystem nouns, not just local helper names
Recent passes pinned many exact local behaviors, but broader gameplay/system nouns still need tightening, including:
- the broader system role of **`7E:0D8B`**
- the broader system role of **`7E:0D8C`**
- the broader system role of **`7E:0D90`**
- the broader role of **`7E:0D1F`**
- the broader role of **`7E:0F0F`**
- top-level family naming around **`C2:A886..C2:AA30`**
- deeper interpretation of recent scratch/work bytes and selector bytes such as **`22/23`**, **`8F`**, and the local **`7D00`** pointer table

## D. Runtime proof is still basically missing
Current state says it plainly:
- runtime evidence rows: **0**
- runtime linked labels: **0**

That means the static side is outpacing the runtime-proof side.
To finish honestly, the project still needs:
- emulator-backed captures for hot live seams
- WRAM ownership validation for the recurring selector/state bytes
- proof for packet emitters, strip materializers, and HDMA-shadow / tile-write families
- better linkage between static labels and observed runtime behavior

## E. Source-tree expansion is still too thin
Current generated-source coverage is only:
- **15 / 66 banks represented in generated source**

That is useful, but nowhere near enough for a “complete disassembly” claim.
What still has to happen:
- generate and curate more bank source scaffolds
- keep freeze ranges aligned with real owner/helper/table boundaries
- push beyond evidence notes and into bank source coverage that can actually rebuild

## F. Rebuild readiness is still starter-only
Current rebuild mode:
- **starter**

Meaning:
- there is a scaffold
- there is a build manifest
- there is a place for rebuild/diff work
- there is **not yet** a finished assembler-ready, bounded-diff, zero-diff Chrono Trigger source tree

To finish this project honestly, it still needs:
- assembler/toolchain integration locked down
- build pipeline hardened past starter scaffolding
- bounded-diff reporting on rebuilt output
- eventually zero-diff or tightly-explained-diff rebuild verification

## G. Data/decompressor grammar ownership still needs deeper coverage
The static callable families tightened here are not the whole ROM.
Still needed:
- more explicit decompressor ownership
- more explicit script/data grammar ownership
- more exact understanding of asset/materialization paths outside the currently-active seam family

---

# 7) Recommended next-session order of operations

1. refresh external Chrono Trigger community context for vocabulary only
2. resume from **`C2:F2F3..C2:F360`**
3. treat **`F333`**, **`F338`**, and **`F378`** as likely structural anchors immediately
4. do not trust the old seam end blindly; keep using lookahead so the next stop does not cut an owner in half again
5. after closing the next seam, keep pushing downstream while continuously separating:
   - callable owners
   - helper tails
   - overlapping late entries
   - local pointer/selector tables
   - literal packet/data spans
6. after the next static cluster, spend real time on runtime-proof lanes and broader subsystem naming instead of only adding more local helper names
7. keep the toolkit release in sync with the workspace so the downloadable package does not lag behind the real pass count again

---

# 8) Current artifact map

## Primary current files
- `chrono_trigger_disasm_pass150.md`
- `chrono_trigger_labels_pass150.md`
- `chrono_trigger_next_session_start_here_pass150.md`
- `ct_completion_score_after_pass150.json`
- `ct_consistency_report_after_pass150.md`
- `ct_current_session_packet_after_pass150.md`
- `ct_current_seam_candidates_after_pass150.md`
- `ct_smoke_test_after_pass150.md`
- `ct_toolkit_doctor_after_pass150.md`
- `ct_workspace_report_after_pass150.md`

## Current packaged toolkit
- `ct_disasm_toolkit_v6_7_pass150_upgraded.zip`

## Previous handoff this one continues from
- `chrono_trigger_master_handoff_session7.md`

---

# 9) Final blunt assessment

This session absolutely mattered.
It pushed the static disassembly forward in a real way, cleaned up a long downstream C2 family, and corrected multiple fake seam stops that would have poisoned later passes.

But this project is **not** “basically done.”
At **70.6%**, the remaining work is the expensive kind:
- broader bank coverage
- runtime proof
- decompressor / grammar ownership
- source-tree expansion
- assembler integration
- rebuild validation

That is the real state.

---

## Generated
- handoff generated: **2026-03-25T21:56:08Z**
- workspace root used for toolkit refresh: **`/mnt/data/ctpass150_toolkit_v6_7_release_work`**
- toolkit version at handoff time: **v6.7**
