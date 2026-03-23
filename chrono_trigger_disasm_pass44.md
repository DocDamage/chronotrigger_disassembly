# Chrono Trigger Disassembly Pass 44

## Scope of this pass
This pass continued directly from pass 43’s live seam:

- resolve the practical meaning of the `0B40` workspace restored by `C1:1C3A`
- trace the producer/consumer chain for the template copies into `0B40`
- determine whether the `0B40` block is logic scratch, a structured data buffer, or a render/upload staging area
- re-check `9F38[x]` only if the same trace exposed a trustworthy positive writer

This pass stayed on the exact controller/render seam opened by passes 40–43.
It did **not** rename the whole gameplay subsystem.

---

## Method
1. Re-traced every proven `0B40` writer in bank `C1`:
   - `0EA1..0EB1`
   - `1301..1315`
   - `1594..15A9`
   - `15B5..15C5`
   - `1C3A..1C49`
2. Inspected the ROM-resident source blocks at:
   - `D1:5800`
   - `D1:5A50`
   - `D1:5BD0`
3. Traced the only cross-bank consumer of the dirty/upload byte at `99E2`.
4. Re-checked direct accesses to `9F38[x]` so this pass would not silently smuggle in a fake positive-writer label.

---

## Starting point from pass 43
Pass 43 had already proved:

- `C1:1C3A` restores `0x180` bytes from `D1:5800` into WRAM at `0B40`
- service 2 (`1BAA`) falls through that restore tail after lane removal/reseat
- outer follow-up families already copy `0x180` bytes from `D1:5BD0` into `0B40` in the `95DB = 2` family
- the exact human-facing meaning of `0B40` was still open

The ambiguity was therefore no longer “is `0B40` structured?”
It was specifically:

> **what kind of structured buffer is it, and what consumes it?**

---

## 1. `7E:0B40` is **not** generic logic scratch; it is a VRAM-uploaded `0x180`-byte staging buffer
The strongest result of this pass comes from the cross-bank sink for `99E2`.

At `CF:E380` the code does:

```text
LDA $99E2
BEQ skip

LDA #$01 -> $4370
LDA #$18 -> $4371
LDA #$40 -> $4372
LDA #$0B -> $4373
LDA #$00 -> $4374
LDA #$80 -> $4375
LDA #$01 -> $4376

LDA #$00 -> $2116
LDA #$7A -> $2117
LDA #$80 -> $420B

STZ $99E2
```

This is a standard SNES DMA setup:

- DMA source = `00:0B40`
  - which is the low-bank WRAM mirror of the same workspace rooted at `7E:0B40`
- transfer size = `0x0180`
- destination register = `$2118` / VRAM data port
- destination VRAM address = `0x7A00`
- after the transfer, `99E2` is cleared

So the safest strong reading is now:

> `0B40` = **VRAM tilemap/data staging buffer uploaded in `0x180`-byte chunks to VRAM `7A00`**

This is the missing hard proof that pass 43 did not have.

---

## 2. `99E2` is the **pending-upload latch/counter** for that `0B40 -> VRAM 7A00` transfer
Before this pass, `99E2` was only known structurally:

- `INC $99E2` appears after multiple `0B40` write paths in bank `C1`
- no clear reader had been tied down in the same controller band

The bank-`CF` sink now resolves that.

### Proven writer sites
`INC $99E2` occurs at:

- `C1:0C7D`
- `C1:0EB1`
- `C1:1315`
- `C1:15A9`
- `C1:15C5`

### Proven consumer/clear site
- `CF:E380` checks `99E2`
- if nonzero, uploads `0B40` to VRAM `7A00`
- then `STZ $99E2`

So `99E2` is no longer just “some state byte touched after template copies.”
It is the exact **request/dirty latch (or small counter)** that schedules the `0B40` upload.

Safest strong reading:

> `99E2` = **pending tilemap/upload dirty counter for the `0B40` staging block**

I am keeping “counter” rather than forcing “boolean” because the writers use `INC`, not immediate `01`, even though the sink only cares about zero/nonzero.

---

## 3. `D1:5800`, `D1:5A50`, and `D1:5BD0` are three ROM-resident `0x180`-byte template blocks for that upload buffer
The copy sites are now materially unified.

### Proven copy sources
- `C1:1C3A..1C49` copies `D1:5800 -> 0B40`
- `C1:0EA1..0EB1` copies `D1:5A50 -> 0B40`
- `C1:1301..1315` copies `D1:5BD0 -> 0B40`
- `C1:1594..15A9` copies `D1:5BD0 -> 0B40`
- `C1:15B5..15C5` copies `D1:5BD0 -> 0B40`

And, critically, the mode-specific copies that are followed by `INC $99E2` are now linked to the bank-`CF` upload sink.

So these three `D1` blocks are not anonymous tables sitting near code.
They are **exact template sources** for the render/upload buffer at `0B40`.

---

## 4. Those `D1` source blocks are structured as **192 little-endian words**, and their contents strongly match a tilemap/panel template family
The data shape matters here.

Each source block is exactly `0x180` bytes.
Interpreted as little-endian words, that is:

- `0x180 / 2 = 0xC0 = 192` words

The contents are highly regular and not logic-like.
Representative values from `D1:5800` are:

```text
00F0 00F1 00F2 ... 00F3
00F4 00FC 00FD 03FC 03FD ... 00F5
00F6 00FE 00FF 03FE 03FF ... 00F7
...
00F8 00F9 00FA ... 00FB
```

The three sources differ only in a small number of entries:

- `5800` vs `5A50` differ at 19 byte positions
- `5800` vs `5BD0` differ at 10 byte positions

So the sources are clearly the **same base layout family with small mode-specific edits**, not unrelated data structures.

### Why the tilemap reading is now strong
This is not just pattern-matching wishful thinking.
It rests on three independent facts:

1. the source blocks are copied into a fixed-size WRAM buffer
2. that WRAM buffer is then DMA-uploaded to a fixed VRAM address (`7A00`) in the same exact size (`0x180`)
3. the source blocks themselves look like dense 16-bit tile-entry matrices rather than sparse logic tables

That is enough to upgrade the old “workspace template” wording into:

> `0B40` is a **tilemap-style staging buffer**, and `D1:5800 / 5A50 / 5BD0` are **tilemap template variants** for it

The exact UI/gameplay-facing name of that panel/screen is still open.
But the render/upload role is no longer open.

---

## 5. `C1:1C3A` is specifically the **default/reset template restore**, not a generic workspace wipe
Pass 43 already proved the raw copy loop.
This pass gives it the missing context.

Because:

- the destination is now known to be a VRAM-uploaded staging block
- the source is one of the tilemap-template variants in `D1`
- service 2 falls through this copy after lane removal/reseat

`1C3A` is no longer best described as “restore workspace template `0B40`.”
It is more accurately:

> `1C3A` = **restore the default/reset `0B40` tilemap template**

That is a meaningful strengthening of the pass-43 label.

---

## 6. The alternate copies at `0EA1`, `1301`, `1594`, and `15B5` are **mode/template swaps** into the same render buffer
The outer-controller work from pass 40 already showed:

- `12ED` / the `95DB = 2` family copies `D1:5BD0` to `0B40`
- the same family then marks `99E2` dirty

This pass adds the missing sink proof and the additional alternate source.

### `0EA1..0EB1`
This path copies `D1:5A50 -> 0B40`, then increments `99E2`, then clears `A86A`.
So `5A50` is not some unused cousin block.
It is a second mode/template variant uploaded through the same path.

### `1301..1315`, `1594..15A9`, `15B5..15C5`
All three copy the `5BD0` variant into `0B40` and then increment `99E2`.
So the controller has multiple entry paths that converge on the same alternate template.

The safest structural reading is:

- `5800` = default/reset template
- `5A50` = alternate template family A
- `5BD0` = alternate template family B

I am intentionally **not** forcing final screen/menu names yet.
The ROM proof is “template family A/B/default,” not “this is definitely screen X.”

---

## 7. The source data strongly suggests a **16x12 word matrix**, which fits the render reading much better than a logic-buffer reading
The size alone gives 192 words, but the data pattern goes further.

When the words are laid out row-wise, the blocks naturally read as a regular grid with repeated edge/fill families:

- outer rows built from `F0..F3` and `F8..FB`
- interior rows built from `F4..F7`, `FC/FD`, and `FE/FF`
- paired `00FC / 03FC`, `00FD / 03FD`, `00FE / 03FE`, `00FF / 03FF` variants used in repeating horizontal bands

That is exactly the kind of dense, repeated, row-structured data you expect from a tilemap/panel template, and **not** what you expect from candidate lists, lane rosters, or controller logic.

A 16-column by 12-row interpretation accounts cleanly for all 192 words.
I am still keeping the final “panel/menu/screen” wording provisional, but the matrix shape itself is now strong enough to mention directly.

---

## 8. `9F38[x]` did **not** get a promotion this pass
I re-checked the same trace for a direct positive writer to `9F38[x]`.
Nothing in the newly resolved `0B40` upload path promoted it.

What remains true:

- `1B69` clears `9F38[lane]` on pending->active promotion
- `16F7` ORs `9F38[current_lane]` into emitted record aux state at `93EF + record_offset`
- a trustworthy positive producer is still not directly pinned

So `9F38[x]` stays provisional.
This pass does **not** pretend otherwise.

---

## Net result of pass 44
The `0B40` side of the seam is no longer abstract.

What was previously “a 0x180-byte workspace template restored by service 2” is now materially solved as:

- a **tilemap-style WRAM staging buffer** at `0B40`
- fed by three ROM-resident template variants at `D1:5800 / 5A50 / 5BD0`
- marked dirty through `99E2`
- uploaded by DMA from `00:0B40` to VRAM `7A00`

That is a real subsystem-level clarification, not just another local helper rename.

The abstraction gap moved again.
The next clean seam is now:

1. the exact high-level screen/panel semantics of the three `0B40` template variants
2. the in-place mutators that rewrite `0B40` before upload
3. the still-unresolved positive writer side of `9F38[x]`
