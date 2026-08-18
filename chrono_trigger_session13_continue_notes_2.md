# Chrono Trigger Disassembly — Session 13 Continuation Notes (Second Continuation)

## Starting point
- Prior live seam: `C3:3300..`
- Prior latest completed pass: **201**
- Prior estimate: **~80.4%**

## Work completed now
This continuation closed **passes 202 through 211**.

### Pass 202 — `C3:3300..33FF`
Treated as mixed single-hit page with double-supported `33D6` landing into obvious control/table blob.

Key outcome:
- visible raw targets included `3301`, `3333`, `333F`, `3343`, `33A0`, `33A4`, `33A8`, `33D6`
- almost every landing was backed by a single caller from ASCII-heavy or otherwise suspicious neighborhoods
- `33D6` was the best-looking target on caller count with two same-bank hits
- it still failed local review because the target sits inside a wider mixed control/data blob rather than a defendable owner start

### Pass 203 — `C3:3400..34FF`
Treated as pointer-table page with false `3461` entry and no caller-backed owner.

Key outcome:
- `3461` had the cleanest caller-side evidence in the page
- the target bytes themselves resolve as obvious little-endian pointer/table material rather than callable structure
- remaining hits such as `3443`, `3448`, `347A`, `34D3`, and `34FB` were weaker or caller-contaminated

### Pass 204 — `C3:3500..35FF`
Treated as mixed init-like store-stream page with single cleaner `350E` hit and false `357B` jump cluster.

Key outcome:
- `350E` had one comparatively cleaner caller from `C3:2FB0`
- the target neighborhood still behaved like mixed immediate/store stream with padding contamination rather than stable code
- `357B` collected multiple visible jumps, but those callers were not trustworthy enough to rescue the page

### Pass 205 — `C3:3600..36FF`
Treated as mixed control page with tempting `3691` single-caller entry but table-bound followthrough.

Key outcome:
- `3691` was one of the more tempting single-caller landings of the run
- local bytes near `3691` do look more code-like than many recent pages
- even so, the entry still sits after a noisy mixed lead-in and quickly resolves into jumps/references into the still-untrusted `395E` / `39A7` lane
- `36E9` also looked like late tail bait rather than a defendable owner start

### Pass 206 — `C3:3700..37FF`
Treated as xref-heavy page with ASCII-spam early hits and triple-supported false `377E` landing.

Key outcome:
- the page was crowded with raw targets, especially in early `370C..3716`
- most of those early hits were backed by blatantly ASCII-heavy caller neighborhoods
- `377E` was the strongest target on paper because it received three same-bank callers, including two comparatively cleaner ones
- local byte review still killed it: the landing does not defend a true start and continues to read like mixed command/data material

### Pass 207 — `C3:3800..38FF`
Treated as mixed jump-bait page with quad-hit false `3800` and unsupported `3870` stub.

Key outcome:
- `3800` drew four same-bank jumps, which initially looked strong
- every visible `3800` caller came from dirty neighborhoods and the target did not stabilize into a real owner
- `3870` had the cleanest single visible hit in the page, but only as a tiny unsupported return-anchored pocket

### Pass 208 — `C3:3900..39FF`
Treated as xref-rich command-table page with false clean hits into `395E`, `39A7`, and `39DE`.

Key outcome:
- this page had the best caller-side density of the whole continuation
- visible targets such as `395E`, `39A7`, `39B1`, `39DE`, and `39F5` all received comparatively cleaner same-bank callers
- despite that, the target neighborhoods themselves resolve as repeated command/pointer-table style material, not defendable code starts

### Pass 209 — `C3:3A00..3AFF`
Treated as mixed table page with blatant text-side `3A20` call cluster and false `3AA9` jump target.

Key outcome:
- `3A20` received three visible hits, but all three came from an almost comically ASCII-heavy text-side neighborhood
- `3A01`, `3A3A`, and `3AA9` had cleaner-looking callers than `3A20`
- even then, the page itself remained dominated by table/command-stream behavior and did not produce a defendable owner boundary

### Pass 210 — `C3:3B00..3BFF`
Treated as sparse mixed page with double ASCII-side `3B46` hits and no defendable start.

Key outcome:
- `3B24` had only a weak dirty jump caller
- `3B46` received two hits, but both came from heavily ASCII-contaminated low addresses
- no part of the page held up as an owner/helper promotion

### Pass 211 — `C3:3C00..3CFF`
Treated as mixed long-call page with tempting `3C5E` and `3C80` interior landings but no true owner.

Key outcome:
- `3C5E` was the most interesting external hit of the continuation because it received a long call from bank `E9`
- `3C80` also had a cleaner same-bank jump from `C3:2917`
- both targets still failed the ownership test because they land inside a wider mixed blob made of setup/store-looking structure, tail jumps, and surrounding command/data contamination
- this page felt closer to a real routine lane than several previous pages, but still did not resolve into a defendable top-level owner

## Current state now
- Latest completed pass: **211**
- Current live seam: **`C3:3D00..`**
- Current completion estimate: **~81.2%**

## Honest read of the seam
This continuation kept the same rule that saved the last two runs: caller evidence matters, but caller evidence alone cannot promote garbage into code.

The run showed three especially deceptive shapes:
1. **Pass 202 (`3300`)** had a double-supported `33D6` landing that still collapsed under local byte review.
2. **Pass 206 (`3700`)** had a triple-supported `377E` landing that still behaved like mixed command/data material rather than a true start.
3. **Pass 208 (`3900`)** was packed with comparatively clean xrefs, but the targets themselves resolved as command/pointer-table style material instead of callable code.

## Biggest takeaways
1. **`3461` in pass 203** is the clearest example of a target with non-terrible caller support whose own bytes immediately expose it as a pointer table.
2. **`3691` in pass 205** is one of the more tempting code-like single-caller landings in this stretch, but it still does not defend its page.
3. **`377E` in pass 206** is the strongest multi-caller false landing of the continuation.
4. **`395E` / `39A7` / `39DE` in pass 208** prove that even cleanish same-bank xrefs can still be landing in table/command material.
5. **`3C5E` / `3C80` in pass 211** are the closest thing in this continuation to a structured reentry lane, but they still fail true ownership.

## Real next target
- **`C3:3D00..`**
