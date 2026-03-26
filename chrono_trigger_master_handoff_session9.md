# Chrono Trigger (USA) ROM Disassembly — Detailed Session 9 Handoff

## Purpose
This is the full handoff for the work completed after **session 8**, covering:
- disassembly progress from **pass 151** through **pass 161**
- the toolkit audit and upgrade work that produced **v6.8**
- the exact current project state at the end of pass 161
- the honest remaining work before this can be called a complete Chrono Trigger SNES ROM disassembly

Use this handoff to answer three things fast:
1. **What got done in this session?**
2. **Where is the disassembly right now?**
3. **What still has to happen before the Chrono Trigger ROM is actually finished and rebuild-ready?**

This handoff follows:
- `chrono_trigger_master_handoff_session8.md`
- `ct_disasm_toolkit_v6_7_pass150_upgraded.zip`

---

## Mandatory context before anyone continues
Same rule as before:
refresh on public Chrono Trigger research/modding context before pushing new claims.

Priority external context to refresh:
- Chrono Compendium
- Data Crystal
- Temporal Flux / Kajar Labs / older forum material
- bsnes / bsnes-plus / Geiger-style debugger workflows

Community context is still vocabulary support, not proof.
Final labels, subsystem ownership, rebuild claims, and handoff claims still need to come from ROM evidence and the project’s own artifacts.

---

# 1) Session scope

## Start state
This session started from the end of session 8:
- latest pass: **150**
- current best toolkit snapshot at start: **`ct_disasm_toolkit_v6_7_pass150_upgraded.zip`**
- current live seam at start: **`C2:F2F3..C2:F360`**
- completion estimate at start: **70.6%**
- label rows at start: **1237**
- strong labels at start: **947**
- caution labels at start: **52**
- toolkit doctor health at start: **100.0%**

## End state
This session ends at:
- latest pass: **161**
- current best toolkit snapshot: **`ct_disasm_toolkit_v6_8_pass161_upgraded.zip`**
- current toolkit version: **v6.8**
- current completion estimate: **69.8%**
- label rows: **1310**
- strong labels: **992**
- provisional labels: **150**
- alias labels: **42**
- caution labels: **57**
- toolkit doctor health score: **100.0%**
- smoke test health score: **100.0%**
- release audit health score: **100.0%**
- current canonical next seam: **`C3:0077..C3:01E3`**

## The blunt truth
This session absolutely mattered, but it still did **not** finish the project.

It did six important things:
1. pushed the live C2-side callable/helper families from **`C2:F2F3`** all the way through the honest end of bank **`C2:FFFF`**
2. corrected more fake seam boundaries, including one-byte-off routine heads and one bank-end tail that looked code-shaped but was really just truncated overlap
3. broke open low-bank `C3` honestly instead of trusting the toolkit’s false “unmapped” warning there
4. proved the bank-head `C3` veneer/launcher/trampoline cluster is real mapped ROM and not just weird edge noise
5. audited the toolkit more broadly than the one visible bug and upgraded it to **v6.8**
6. left the downloadable toolkit aligned with the real workspace again at **pass 161**

It did **not** solve the endgame.
The expensive remaining work is still:
- broader bank-by-bank code/data separation
- runtime-backed WRAM/system proof
- decompressor/data-grammar ownership
- source-tree expansion into something genuinely assembler-ready
- assembler integration, bounded-diff reporting, and eventually zero-diff rebuild verification

---

# 2) Toolkit work completed this session

The toolkit did not just get one spot fix. It got a real audit and a broader refresh.

## v6.8 — low-bank HiROM, regression coverage, score hardening, release refresh
Delivered at pass 161.

### What changed
- fixed the **shared HiROM mapper** so low-bank ROM CPU addresses like `C3:0000` and `C3:0557` map correctly
- fixed canonical `pc_to_hirom()` output so low-bank project addresses round-trip cleanly
- added a **toolkit-doctor low-bank mapping check**
- added a **dedicated low-bank smoke-test lane**
- bumped xref cache metadata to **`bank_local_v3_lowbank_hirom`**
- added high-value low-bank `C3` xref targets: `0008`, `000E`, `0011`, `0014`, `0557`
- hardened the **completion-score lane** so the packaged workspace stops faking a wildly inflated percentage when its label DB is thinner than the live work tree
- refreshed README / release-manifest notes for the low-bank upgrade
- refreshed the packaged release forward from pass 150 to pass 161

### Why this mattered
The visible symptom was the inspector rejecting `C3:0000`, but the actual problem was larger:
- shared address mapping was wrong for low-bank `C0-FF:0000-7FFF`
- xref-facing outputs were stale there
- smoke coverage didn’t touch that case
- doctor coverage didn’t catch it
- the packaged-score lane could drift into fake optimism

### Current released toolkit state
- latest pass: **161**
- toolkit version: **v6.8**
- live seam: **`C3:0077..C3:01E3`**
- completion estimate: **69.8%**
- toolkit doctor: **100.0%**
- smoke test: **100.0%**
- release audit: **100.0%**

---

# 3) What was accomplished in this session

## Session-wide net result
Across passes **151–161**, the work first kept pushing downstream through the same broad bank-`C2` callable/helper/materialization family that session 8 had already tightened. That chain was closed honestly all the way to the end of bank `C2`.

Then the session crossed the bank boundary and did the more important structural correction:
- the toolkit’s old low-bank `C3` blind spot was wrong
- `C3:0000` is real mapped ROM
- the bank head is a live veneer/data/launcher cluster
- the next real seam is the worker body at **`C3:0077..C3:01E3`**

Net result:
- bank `C2` is materially tighter through the cliff at `FFFF`
- low-bank `C3` is no longer being treated like a fake hole
- the next session starts from a sharp real target in startup code rather than from a tooling myth

---

# 4) Exact pass ledger for this session

## Pass 151
Closed the family that session 8 left open at **`C2:F2F3..C2:F360`**, and proved the old seam end was too short.

What froze:
- `C2:F2F3..C2:F331` exact change-handler / refresh owner
- `C2:F332..C2:F336` exact short base-copy helper
- `C2:F337..C2:F360` exact zero-bank record builder
- `C2:F361..C2:F363` exact width-forcing wrapper into the next helper
- `C2:F364..C2:F377` exact FF-bank length-prefixed importer
- `C2:F378..C2:F3CA` exact coordinate-to-coordinate multi-row word-swap owner

Important correction:
- the honest closure ran through **`C2:F3CA`**, not `F360`

## Pass 152
Closed the next owner family at **`C2:F3CB..C2:F421`** and the follow-on callable owner at **`C2:F422..C2:F547`**.

What froze:
- exact eight-row direct-page strip/import owner
- exact bank-`E4` header-decode / strip-import / optional unpack-submit owner

Important correction:
- the old seam edge was too conservative; `F422` was already a real owner

## Pass 153
Continued after `F547`, but the important result was negative proof on the seam front.

What froze:
- `C2:F588..C2:F5A6` exact eight-row row-clear helper
- `C2:F5A7..C2:F5EC` exact two-phase strip staging/import owner
- `C2:F5ED..C2:F625` exact bank-`D1` source-derivation helper
- `C2:F626..C2:F642` exact `A * 0x40` row-offset helper
- `C2:F643..C2:F656` exact fixed scheduler wrapper for `F657`

Important correction:
- **`C2:F56A..C2:F587` was not safe to freeze** as a real callable owner yet

## Pass 154
Closed the row-worker family rooted at **`C2:F657`** and cleaned up the local dispatch material around `F6D0`.

What froze:
- persistent row-band service loop
- increment-and-fallthrough alias entry
- row-change pointer/front-end owner
- local scale-return stubs
- exact four-entry dispatch table
- stream-scan / WRAM-submit tail
- exact factor table

Important correction:
- the old “mystery local table” was real code-plus-dispatch structure, not seam garbage

## Pass 155
Closed the callable family starting at **`C2:F75C`**, which turned out to be more than one owner.

What froze:
- exact `9890`-driven row materializer/helper
- direct-page-derived descriptor builder
- alias entry forcing `0214 = 81`
- shared dual-packet submit owner

## Pass 156
Closed the callback/bootstrap family rooted at **`C2:F943`**.

What froze:
- change-gated scheduler owner
- dual-phase bootstrap owner
- overlapping late entry into the second-phase tail
- active-block opener/scheduler owner
- local wrapper into `FAA4`
- iterative packet/service driver
- `0217`-change-gated rebuild/submit helper
- paired-table stamping helpers

Important correction:
- the seam did not stop near `F9AF`; it was a whole family through **`C2:FBD0`**

## Pass 157
Closed the selector/descriptor packet family after `FBD0` and the next arithmetic/helper cluster through `FE09`.

What froze:
- local selector/descriptor packet family
- outside-called quotient-prep owners
- shared 24-step divider
- multiply wrapper
- shared hardware-multiply accumulator
- staged add/subtract updaters
- clamp/normalize helper

## Pass 158
Closed the ugly repeated clamp/update family after `FE09` and froze the overlap/tail islands so they stop blocking forward motion.

What froze:
- repeated clamp helper clones
- subtract/update helper clone and overlapping late entry
- several overlap/tail islands that were **not** standalone owners

Important result:
- the whole `FE0A..FEF9` band stopped pretending to be one giant half-open mess

## Pass 159
Closed the bank-end callable family and fixed one more seam-head mistake.

What froze:
- exact `C2:FEFB..C2:FF25` owner
- exact `C2:FF26..C2:FF86` owner
- exact local helper `C2:FF87..C2:FFA3`
- several bank-end overlap/duplicate tails through `C2:FFED`

Important correction:
- the real routine heads were **`FEFB`** and **`FF26`**, not `FEFA` / `FF27`

## Pass 160
Closed the very end of bank `C2` honestly instead of inventing one more fake function at the cliff.

What froze:
- `C2:FFEE..C2:FFFF` as an exact **bank-end truncated duplicate / overlap tail** of the earlier import/mirror helper family

Important correction:
- `FFEE` is **not** a clean balanced owner head
- the correct next task moved across the bank boundary into low-bank `C3`

## Pass 161
Broke open low-bank `C3` by raw-byte proof and closed the fake “non-ROM-mapped” gap.

What froze:
- `C3:0000..0001` exact branch-over wrapper (`BRA $0014`)
- `C3:0005..0007` exact embedded raw long constant `C2:DECE`
- `C3:0008..000A` exact live entry veneer `JMP $0077`
- `C3:000B..000D` exact second embedded raw long constant `C2:DECE`
- `C3:000E..0010` exact live entry veneer `JMP $01E4`
- `C3:0011..0013` exact live entry veneer `JMP $0EFA`
- `C3:0014..0076` exact launcher that installs RAM trampolines, stages `FE:0003` unpack to `7E:3000`, and jumps there
- `C3:0529..0547` exact temporary RAM-trampoline body that blanks display and returns via `RTI`
- `C3:0548..0556` exact temporary RAM-trampoline body that acknowledges NMI / restores display and returns via `RTI`

Important correction:
- the toolkit’s old low-bank warning was the bug, not the ROM
- the next real seam is now **`C3:0077..C3:01E3`**

---

# 5) Where we are now

## Current canonical restart target
The next live seam is:
- **`C3:0077..C3:01E3`**

Immediate structural anchors already visible there:
- exact entry comes from the exact live veneer at **`C3:0008`**
- exact `C3:0008` has **11** proven long-call sites
- exact `C3:01E4` is already anchored by the second exact live veneer at **`C3:000E`**

## Current measurable project state
From the refreshed toolkit state and score:
- latest pass: **161**
- overall completion estimate: **69.8%**
- label semantics score: **80.3%**
- opcode coverage score: **92.5%**
- bank separation score: **39.3%**
- rebuild readiness score: **36.6%**
- master C1 opcodes covered: **170 / 170**
- selector-control bytes covered: **83 / 83**
- service-7 wrappers covered: **5 / 8**
- banks represented in generated source: **15 / 66**
- frozen/stable ranges: **919** (**70.2%** of label rows)
- runtime validation rows: **0 / 0**
- runtime linked labels: **0**
- rebuild mode: **starter**

## Honesty note on progress vs finish line
The percentage went **down** from the loose pass-161 artifact’s `70.2%` to the refreshed toolkit’s **69.8%** because the v6.8 audit also fixed an over-optimistic scoring path in packaged workspaces.

That is the right direction.
A toolkit that lies less is better than one that flatters progress.

---

# 6) What still needs to happen before the Chrono Trigger ROM is actually finished

## A. Finish the current live seam and its immediate follow-on owner
Immediate next task:
- close **`C3:0077..C3:01E3`** honestly
- then split the already-anchored follow-on owner at **`C3:01E4`**

## B. Keep widening exact code/data separation beyond the recent `C2` strip and `C3` bank head
What remains:
- more untouched or weakly-classified ROM territory still needs bank-by-bank separation
- more mixed code/data spans still need exact table vs helper vs owner identification
- more local packet/data spans still need proof as data, not fake code

## C. Tighten broader subsystem nouns, not just local helpers
Recent passes pinned many exact local behaviors, but broader gameplay/system nouns still need tightening around recurring scratch, selector, packet, and state bytes.

## D. Runtime proof is still basically missing
Current state still says it plainly:
- runtime evidence rows: **0**
- runtime linked labels: **0**

That means the static side is still outrunning the runtime-proof side.
To finish honestly, the project still needs:
- emulator-backed captures for hot live seams
- WRAM ownership validation for recurring selector/state bytes
- proof for packet emitters, strip materializers, HDMA-shadow lanes, startup-control bytes, and tile-write families

## E. Source-tree expansion is still too thin
Current generated-source coverage is only:
- **15 / 66 banks represented in generated source**

That is useful, but nowhere near enough for a “complete disassembly” claim.

## F. Rebuild readiness is still starter-only
Current rebuild mode:
- **starter**

Meaning:
- there is a scaffold
- there is a build manifest
- there is a place for rebuild/diff work
- there is **not yet** a finished assembler-ready, bounded-diff, zero-diff Chrono Trigger source tree

## G. Data/decompressor grammar ownership still needs deeper coverage
The static callable families tightened here are not the whole ROM.
Still needed:
- more explicit decompressor ownership
- more explicit startup/data grammar ownership
- more exact understanding of asset/materialization paths outside the currently-active seam family

---

# 7) Recommended next-session order of operations

1. refresh external Chrono Trigger community context for vocabulary only
2. resume from **`C3:0077..C3:01E3`**
3. keep the entry-veneer facts in mind:
   - exact `C3:0008` is live and already proven
   - exact `C3:01E4` is already anchored by exact `C3:000E`
4. do not flatten the whole startup band into one “boot blob”
5. keep separating:
   - callable owners
   - helper tails
   - overlapping late entries
   - local pointer/selector tables
   - literal packet/data spans
6. spend real time on runtime-proof lanes once the first `C3` worker family is split
7. keep the toolkit release in sync with the workspace so the downloadable package does not drift again

---

# 8) Current artifact map

## Primary current files
- `chrono_trigger_disasm_pass161.md`
- `chrono_trigger_labels_pass161.md`
- `chrono_trigger_next_session_start_here_pass161.md`
- `ct_completion_score_after_pass161.json`
- `ct_consistency_report_after_pass161.md`
- `ct_current_session_packet_after_pass161.md`
- `ct_toolkit_doctor_after_pass161.md`
- `ct_workspace_report_after_pass161.md`

## Current packaged toolkit
- `ct_disasm_toolkit_v6_8_pass161_upgraded.zip`

## Previous handoff this one continues from
- `chrono_trigger_master_handoff_session8.md`

---

# 9) Final blunt assessment

This session absolutely mattered.
It finished a real downstream bank-`C2` family chain, killed another fake bank-end owner, broke open low-bank `C3` honestly, and materially improved the toolkit instead of just pretending the handoff was enough.

But the project is **not** “basically done.”
At **69.8%**, the remaining work is still the expensive kind:
- broader bank coverage
- runtime proof
- decompressor / grammar ownership
- source-tree expansion
- assembler integration
- rebuild validation

That is the real state.

---

## Generated
- handoff generated: **2026-03-26T14:00:00Z**
- workspace root used for toolkit refresh: **`/mnt/data/ctpass161_toolkit_v6_8_work/ct_pass150_toolkit_v6_7_release_work`**
- toolkit version at handoff time: **v6.8**
