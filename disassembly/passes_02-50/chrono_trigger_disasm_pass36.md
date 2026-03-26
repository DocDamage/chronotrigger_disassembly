# Chrono Trigger (USA) — Disassembly Pass 36

## Scope
This pass continues directly from pass 35 and covers the exact continuation seam it left open:

1. the unresolved later type cases inside `C1:C1DD`
2. the common downstream path rooted at `C1:C55F`

The goal of this pass was to stop treating `C55F` as a vague “shared success tail” and turn it into a concrete, descriptor-driven post-materialization pipeline, while also tightening the remaining `C1:C1DD` type families that feed it.

---

## Baseline carried forward from pass 35
Pass 35 had already established:

- `C1:C1DD` is a **validation + type-dispatched candidate-list materializer**
- type `0/5/6`, `1`, `3`, `4`, and `7` were structurally pinned
- the unresolved work was the later type families and the common downstream path at `C55F`

What was still unclear was:

- how the later `C1:C1DD` type families map onto the common tail
- what `$3A` actually controls
- whether `C55F` is just cleanup or a real expansion/query phase
- what the local helper cluster `C732/C736/C741/C74C/C78D..C813/C95C` actually does

---

## What was done in this pass
1. Decoded the remaining later `C1:C1DD` type dispatch families as far as the bytes safely allow
2. Linearly decoded the full common downstream path at `C1:C55F`
3. Decoded the helper/dispatch layer around:
   - `C1:C732`
   - `C1:C736`
   - `C1:C741`
   - `C1:C74C`
   - `C1:C78D..C813`
   - `C1:C95C`
4. Traced the candidate-list cleanup/count tail at `C1:C6D9`
5. Tightened the working meaning of `$3A`, `$0C`, `AD8E/AD8D`, `AECC`, and the `CC:2AB0` descriptor table usage

---

## Core results

### 1. The later `C1:C1DD` type families are now much tighter
The routine does not explode into dozens of unrelated unique tails. A lot of the later type space collapses into a handful of shared families.

#### Type `8`
This is a distinct list-building case and is **not** the same as type `1`.

Observed structure:

- seeds `$0A = 1`
- if `$B18B >= 3`, clears `$0A` and jumps into the earlier shared list-builder path
- otherwise scans later `AEFF` slots and writes qualifying indices into `AD8E[]`
- requires at least one result
- sets `AD8D = count`
- sets `$3A = 1`
- jumps into `C55F`

Safest reading:

> **tail-`AEFF` index materializer feeding common tail mode 1**

Do not overclaim the exact `AEFF` semantic yet, but this is clearly an index-list case, not a direct copy-of-values case.

#### Type `9`
This case is still partially opaque, but the byte structure is now clear enough to state its role.

Observed structure:

- seeds `$3A = 1`
- calls the RNG helper at `AF:22` with `#$64`
- then splits on the result in four threshold buckets
- each bucket loads one byte from either `$00:00FA` or `$00:00FB`
- each bucket also seeds fixed immediates into scratch (`$06`, `$08`)
- then jumps into either:
  - `C82D`, or
  - the earlier shared type-`1` / type-`8` family entry points

Safest reading:

> **random four-bucket splitter into delegated selector/materializer subpaths**

It is real control logic, not junk, but it still needs downstream semantic proof before receiving a gameplay-facing name.

#### Types `0B`, `0C`, `0D`, `0E`, `0F`, `12`, and `1A`
These all collapse into one shared family:

- `JSR $C82D`
- if `$AF23 != 0`, fail through `C72B`
- otherwise set `$3A = 2`
- jump into `C55F`

Safest reading:

> **`C82D`-delegated materializer family feeding common tail mode 2**

#### Types `10`, `11`, `13`, `14`, `15`, and `1B`
These all collapse into a direct common-tail family:

- set `$3A = 3`
- jump into `C55F`

No pre-materialization work is done locally in this case block.

Safest reading:

> **direct common-tail family using mode 3**

#### Type `0A`
This is the analogous direct common-tail family for mode 1:

- set `$3A = 1`
- jump into `C55F`

#### Type `32`
This is a special single-entry seed case:

- map `$B2AE` through `JSR $C8F7`
- store one entry into `AD8E`
- set `AD8D = 1`
- set `$3A = 4`
- set `$0A = 1`
- continue into `C55F`

Safest reading:

> **single mapped-entry special feeding common tail mode 4**

So the later type space is no longer “unresolved noise.” It is mostly:

- a special index-list family (`8`)
- a random delegated splitter (`9`)
- a delegated helper family (`0B/0C/0D/0E/0F/12/1A`)
- a direct-tail family (`10/11/13/14/15/1B`)
- one special single-entry mode (`32`)

---

### 2. `C1:C55F` is a real descriptor-driven candidate expansion/finalization pipeline
This was the largest result of the pass.

`C55F` is not just a cleanup tail. It is a structured post-materialization phase driven by a table at `CC:2AB0`.

#### Proven front-end behavior
At entry it reads `$3A` and branches by mode.

Observed front-end:

- if `$3A == 0` or `$3A == 2`:
  - map `$B2AE` through `JSR $C8F7`
  - store the result into `AD8E[0]`
- otherwise skip that preseeding step

This immediately proves that `$3A` is a **real mode selector** for the common tail.

The routine then:

- clears `$12`
- clears `$AF23`
- checks `$0C`
- if `$0C == 0`, jumps straight to the local return at `C730`

So `$0C` is not random scratch here. It is the selector for whether the descriptor-driven expansion phase runs at all.

---

### 3. `$0C` indexes a descriptor-pointer table at `CC:2AB0`
If `$0C != 0`, `C55F` does:

```text
REP #$20
ASL A
TAX
LDA $CC:2AB0,x
STA $3B
```

This is a 16-bit pointer lookup.

For the currently proven range, the table entries are pointer-like and lead to small descriptor blocks such as:

- `0x01 -> CC:2B14`
- `0x02 -> CC:2B18`
- `0x03 -> CC:2B1C`
- `...`
- `0x0B -> CC:2B3C`

Those descriptor blocks begin with a count byte followed by fixed-size records.

Safest reading:

> `$0C` = **descriptor index into the `CC:2AB0` common-tail expansion table**

---

### 4. The `CC:2AB0`-selected descriptor blocks use a simple count + 3-byte-record format
Once the pointer has been loaded into `$3B`, `C55F` reads:

- byte 0 = record count -> `$14`
- then iterates record-by-record, advancing by `+3` each time

Per-record extraction:

- byte 0 -> `$3D`
- byte 1 -> `$04`
- byte 2 low 7 bits -> `$08`
- byte 2 high bit -> `$0E` as `0/1`
- byte 1 high bit -> copied into local flag `$3C`

So each record is structurally:

```text
record = [byte0, byte1, byte2]
byte1 bit7  -> local mode flag (`$3C`)
byte1 low7  -> selects a writer routine
byte2 bit7  -> boolean flag copied into `$0E`
byte2 low7  -> small parameter copied into `$08`
byte0       -> separate small parameter copied into `$3D`
```

The exact gameplay meaning of those three bytes is still unresolved, but their structural role in the pipeline is now firm.

---

### 5. `C1:C95C` is a packet-writer jump table for `$9604..9608`
From each descriptor record, `C55F` masks `byte1 & 0x7F`, doubles it, and uses it to dispatch through `C95C`.

`C95C` is a word table of subroutine targets:

- `C78D`
- `C7A7`
- `C7BD`
- `C7D1`
- `C7E7`
- `C7FD`
- `C813`

Each of those routines writes a specific permutation/subset of working scratch bytes into `$9604..$9608`.

This is a strong structural result.

#### Proven helper role of `C74C`
Before those writers are used, `C55F` calls `C74C`, which loads the working scratch context:

- `$00` / `$02` / `$04` from selector-related state (`B2EA/B2EB/B2EC` via `B1BE[...]` when applicable)
- `$06 = B2AE`
- `$0C = B18B`
- also mirrors current selector bytes into `AE97/AE98`

So `C74C` is the **seed/selector-context loader** for the whole descriptor pipeline.

#### Proven writer family role
The `C78D..C813` family are not random helper blobs. They are small, mode-specific packet emitters into `$9604..$9608`.

For example:

- `C78D` writes a full 5-byte packet from `$0A/$00/$06/$08/$0E`
- `C7A7` writes a reduced packet from `$0A/$06/$08`
- `C7BD` writes an even smaller packet from `$0A/$08`
- `C7D1`, `C7E7`, `C7FD`, and `C813` provide the other fixed packet permutations

Safest reading:

> `C95C` = **packet-writer dispatch table**  
> `C78D..C813` = **mode-specific emitters for the `$9604..$9608` service/query packet**

Do not over-name `$9604..$9608` beyond “packet/service bytes” yet, but the packet-emitter role is now solid.

---

### 6. `C736` and `C741` are descriptor-selected service triggers, not generic helpers
After the packet writer runs, `C55F` checks the high bit of descriptor byte 1 and chooses between:

- `JSR $C736`, or
- `JSR $C741`

Resolved structure:

#### `C736`
```text
LDA $3D
STA $986E
LDA #$05
JSR $0003
RTS
```

#### `C741`
```text
LDA $3D
STA $99CC
LDA #$07
JSR $0003
RTS
```

So these routines:

- consume descriptor byte 0 (`$3D`)
- store it into one of two service latches (`986E` or `99CC`)
- invoke local service `JSR $0003` with fixed mode `5` or `7`

Safest reading:

> **descriptor-selected service/query triggers for mode 5 vs mode 7**

The exact engine behind `JSR $0003` still needs proof, but these are no longer just anonymous helpers.

---

### 7. The middle of `C55F` collects query results from `$99C0` into `AD8E` and `AECC`
After each descriptor-triggered service call, `C55F` runs a bounded collection loop over 11 slots.

Observed structure:

- initializes local indexing via `C90B`
- iterates `X = $2C .. 0x0A`
- reads `LDA $99C0,x`
- for values `< 3`, accepts directly
- for values `>= 3`, consults `AF12[value]` and only accepts entries with bit 7 set
- accepted entries are written to:
  - `AD8E[x]`
  - `AECC[x]`
- non-`FF` accepted entries increase the running count in `Y`
- at the end:
  - `AECB = count`
  - `AD8D = count`

This proves several important things at once:

1. `AD8E` is not only built by `C1:C1DD`; it is also **expanded/rewritten by the common tail**
2. `AECC` is a **parallel mirror of the current accepted query-pass entries**
3. `$99C0` is a bounded result vector consumed by the common-tail expansion path
4. `AF12` bit 7 is a real per-entry acceptance gate for entries `>= 3`

Safest reading:

> **common-tail query/expansion results are merged from `$99C0` into `AD8E/AECC` under an `AF12` eligibility gate**

---

### 8. `$3A` is now a real mode selector for the common tail
This pass finally makes `$3A` meaningful.

Current proven mode behavior:

- `$3A = 0`
  - preseed `AD8E[0]` from mapped `B2AE`
  - run descriptor expansion
  - run final compaction/count phase

- `$3A = 1`
  - no initial `B2AE` preseeding
  - run descriptor expansion
  - run final compaction/count phase

- `$3A = 2`
  - same initial preseeding behavior as mode 0
  - descriptor expansion still runs
  - later behavior diverges only by how the mode was reached upstream

- `$3A = 3`
  - direct common-tail family with no initial `B2AE` preseeding

- `$3A = 4`
  - after descriptor expansion, explicitly append mapped `B2AE` if absent
  - then continue into final compaction/count

- `$3A = 5`
  - skips the later `AEFF`-based pruning phase

That is enough to relabel `$3A` from vague scratch into:

> **common-tail post-materialization mode selector**

---

### 9. `C659` handles the “empty query result” case before failure
After the descriptor loop, `C55F` checks the first query result slot and branches to a special path if the result vector looks empty.

Observed condition:

- if `3A != 4`
- and `$99C0[0] == $FFFF`

then it takes a special path.

For the proven `$B18B < 3` side, that path:

- snapshots context into `AE91..AE96`
- chooses `AE93` from the fixed set `{7B, 7C, 7D}` based on `B2EB/B2EC`
- calls `JSR $AC57`
- then fails through `C72B`

This is strong enough to say:

> `C659` is an **empty-result special handler that prepares failure-side follow-up context before reporting local failure**

Do not over-name the `AE91..AE96` fields yet, but this path is no longer just “weird extra code.”

---

### 10. `C6D9` is the final compaction/count phase for `AD8E`
After the descriptor/query phase, `C55F` enters a final cleanup pass unless `$3A == 5`.

Observed behavior at `C6D9`:

- scan `AD8E[]`
- for each non-`FF` entry:
  - use that value as an index into `AEFF[...]`
  - if `AEFF[value] == FF`, remove the entry by shifting the tail of `AD8E` left
  - otherwise keep it
- after compaction, rescan `AD8E[]`
- first `FF` position becomes `AD8D`
- if no terminator is found in the bounded 11-slot scan, set `AF23 = 1`

So this tail is not vague bookkeeping. It is:

> **bounded `AD8E` compaction against `AEFF` validity plus final count/termination derivation into `AD8D`**

This is a strong new label opportunity.

---

## What changed in the understanding of the `C1DD -> C55F` seam
Before this pass, the seam looked roughly like this:

- `C1:C1DD` builds some list into `AD8E`
- `C55F` does some shared follow-up work
- `$3A` is some mode byte
- `C732/C736/C741/C74C/C95C` are helper clutter

After this pass, it looks more like this:

- `C1:C1DD` chooses a type family and often selects a **common-tail mode**
- `$3A` is the **mode selector for the common descriptor/query expansion path**
- `$0C` indexes a **descriptor pointer table** at `CC:2AB0`
- each descriptor block contains a **count + 3-byte records**
- each record:
  - emits a mode-specific packet into `$9604..$9608`
  - chooses one of two service/query trigger routines
  - contributes accepted results from `$99C0` into `AD8E/AECC`
- then `C6D9` compacts/prunes `AD8E` and derives final `AD8D`

That is a substantial jump in semantic clarity.

---

## Strongest new working interpretations

### `C1:C55F`
Best current reading:

> **descriptor-driven candidate expansion/finalization pipeline for `AD8E/AD8D`, using `CC:2AB0` blocks, service-packet emitters, and bounded result merging from `$99C0`**

### `C1:C74C`
Best current reading:

> **load current seed/selector context into working scratch for the descriptor pipeline**

### `C1:C95C`
Best current reading:

> **mode-indexed packet-writer jump table for `$9604..$9608`**

### `C1:C78D..C813`
Best current reading:

> **fixed packet emitters writing specific scratch permutations into `$9604..$9608`**

### `C1:C736` / `C1:C741`
Best current reading:

> **descriptor-selected service/query triggers using mode 5 vs mode 7**

### `C1:C6D9`
Best current reading:

> **compact/prune `AD8E` against `AEFF` validity and derive final `AD8D`**

---

## New cautions after this pass
- Do **not** assign gameplay-facing names to `$9604..$9608` yet. Their role as a service/query packet is now strong, but the outward subsystem still needs proof.
- Do **not** over-name `JSR $0003`; only its two local trigger wrappers and fixed mode IDs `5` / `7` are proven here.
- Do **not** claim the exact meaning of descriptor bytes 0/1/2 yet. Their structural roles are pinned, but their gameplay semantics are not.
- Do **not** pretend type `9` is fully solved; its random four-bucket structure is clear, but the exact meaning of the `$00:00FA/$00:00FB` reads still needs proof.
- Do **not** collapse `AD8E` and `AECC`; this pass proves they are related, but not identical in role.

---

## Recommended next target after this pass
The cleanest next continuation point is now:

1. trace the engine behind the descriptor-trigger wrappers (`C736/C741 -> JSR $0003`)
2. trace producers/consumers of `$9604..$9608`, `$99C0`, and `AE91..AE96`
3. then return to any still-open type-`9` semantics only after that downstream service context is pinned

That is the path most likely to convert the current “descriptor/service/query” wording into hard subsystem names.
