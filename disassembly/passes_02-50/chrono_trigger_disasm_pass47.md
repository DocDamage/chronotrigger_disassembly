# Chrono Trigger Disassembly Pass 47

## Scope of this pass
This pass continued directly from pass 46’s live seam:

- tighten the exact semantics of the small `CC:FA23 / FA29 / FADD`-style selector tables
- determine whether the `0CC0` paired-byte strip has a full rebuild entry beyond the slice-local helpers already pinned
- determine whether `0E80+` has any hard read-side consumer proof, rather than only writer-side proof
- keep labels conservative unless byte-level control flow proved the role directly

This pass stayed in the same presentation/strip band opened by passes 44–46.
It did **not** force the final gameplay-facing subsystem name.

---

## Method
1. Re-read the earlier `C1:0299..0784` strip-building band against pass 46.
2. Treated every direct `0CC0 / 0E80` write site as potential rebuild logic, not just the late `07xx..09xx` helpers.
3. Recovered the exact word values of the `CC:FA23..FA3F`, `CC:FADD`, and `CC:FAE9` tables.
4. Traced the strongest read-side consumers of `7F:0E80`.
5. Only promoted labels where table layout and caller behavior agreed.

---

## Starting point from pass 46
Pass 46 had already proved:

- `0CC0..0E08` is a narrow paired-byte companion strip with row stride `0x40`
- `07BD / 07EE` are template blitters into that strip
- `086D / 08E8` are slice-local mutators
- `0958 / 09B0` rebuild a separate `0x180`-byte companion-record buffer at `0E80+`

The main open questions were:

- what the small selector tables actually encoded
- whether there was a larger full-strip refresh path for `0CC0`
- whether `0E80+` was actually consumed downstream or only built

---

## 1. `CC:FA23..FA3F` are not vague selector bytes; they are a family of **3-entry 16-bit lane-anchor offset tables**
The values are direct and strongly patterned.

### `CC:FA23`
```text
0029, 00A9, 0129
```

### `CC:FA29`
```text
001B, 009B, 011B
```

### `CC:FA2F`
```text
0068, 00E8, 0168
```

### `CC:FA35`
```text
005A, 00DA, 015A
```

### `CC:FA3B`
```text
0066, 00E6, 0166
```

### Structural consequence
All five tables are:

- exactly 3 entries wide
- 16-bit offsets
- separated by a constant lane stride of `0x80`

That is **not** the shape of an arbitrary selector or opcode table.
It is the shape of:

> **per-lane anchor offsets inside three `0x80`-byte strip blocks**

This directly tightens pass 46’s broad “selector tables” wording.

### Immediate caller proof
- `C1:08E8` chooses between `FA23` and `FA29` based on `9F20` and then fills five positions in `0CC0 / 0D00` with `0x29`.
- `C1:05DD` chooses between `FA2F`, `FA35`, and `FA3B` based on `9F20` and then uses the result as the base anchor for dynamic glyph writes into `0CC0`.

So the safe reading is now:

> `FA23 / FA29 / FA2F / FA35 / FA3B` = **lane-anchor offset tables for distinct `0CC0` strip subfields/layouts**

The exact human-facing names of the subfields are still open.
But the table role is no longer vague.

---

## 2. `CC:FADD` is not a broad selector family; the proven live part is just the **3-entry lane-block base table**
The live entries used by `C1:08BF` are:

```text
0000, 0080, 0100
```

That is exactly the lane-block stride expected from the `0CC0` companion strip:

- lane 0 block base = `0x0000`
- lane 1 block base = `0x0080`
- lane 2 block base = `0x0100`

### Why this matters
Pass 46 correctly identified `FADD` as part of the slice-local update path, but this pass tightens the role:

- the proven portion is not a fuzzy mixed selector
- it is the exact **three-lane block-base table**

At `C1:08B4..08C7`, the code:

1. chooses a lane from the active-lane roster
2. reads that lane’s local mode from `95DC`
3. converts that mode to an offset using `FADD`
4. adds the local slice base
5. writes a small 4-glyph marker block (`60/61/62/63`) into `0CC0/0D00`

Safest tightened reading:

> `CC:FADD` = **base offsets for the three `0x80`-byte `0CC0` lane blocks**

Anything beyond those first 3 words should remain unresolved unless a later caller proves it.

---

## 3. `C1:0299` is the real **full companion-strip rebuild entry** for `0CC0`
This was the biggest new structural result in the pass.

The routine beginning at `C1:0299` does all of the following in one entry path:

### Phase A — clear the full strip
It starts with:

```text
TDC
TAX
TAY
TDC
STA $0CC0,Y
LDA #$29
STA $0CC1,Y
INY
INY
INX
CPX #$00C0
BNE ...
```

This clears/fills the entire paired-byte strip region with:

- data byte = `00`
- companion byte = `29`

for exactly `0x00C0` paired positions.

That is a true strip-wide initialization pass, not a slice-local patch.

### Phase B — stamp layout-dependent fixed glyphs
Immediately after the clear, it checks `9F20` and stamps fixed glyphs:

- `64`
- `65`
- `66`

at different hardcoded offsets in the `0CC0` region.

This is direct evidence that `9F20` is a **3-state strip-layout selector**, even if the final gameplay meaning of those three states is still open.

### Phase C — iterate the three lane blocks
The routine then loops lane-by-lane, using `96F5[x]` as the active/enabled gate and per-lane `0x80` block spacing.

For enabled lanes it writes:

- a 5-byte ROM glyph run from `CC:F837 + lane` via `9412`
- one or more dynamic glyph groups generated through the `9499..949F` helper path
- optional additional fixed glyphs (`5D / 5E`) in nonzero `9F20` layouts
- and, in the nonzero-layout path, a call to `C1:06F0`

So this is not just another helper that happens to touch `0CC0`.
It is the real **full-strip rebuild/controller** for the paired-byte companion strip.

Safest keepable reading:

> `C1:0299` = **rebuild the full three-lane `0CC0` companion strip**

That is a materially harder result than pass 46’s local helper framing.

---

## 4. `C1:06F0` is a real **scaled bar/meter renderer** inside the `0CC0` strip
This routine is now concrete enough to call much harder.

### Proven setup
It begins by choosing the bar anchor with:

```text
LDA lane
ASL
TAX
LDA CC:FA35,X
ADC #$001A
TAY
```

So the bar starts from a fixed anchor inside the lane block.

### Proven input state
It then loads two per-lane bytes:

```text
LDA $99DD,X -> $AD
LDA $9F22,X -> $B3
```

and runs them through:

- `C1:010D` (left-shift by 8)
- `C1:00D7` (hardware division path via `$4204/$4205/$4206`)
- `C1:011B` (right-shift reduction)

That is a scale/ratio pipeline, not a plain lookup.

### Proven emitted pattern
It writes into `0CC0`:

- repeated base tile `67`
- repeated fill tile `6F`
- a final partial-tail tile `67 + remainder`
- companion byte `29` or `2D` based on `99DD[lane]`

The emitted field is exactly the kind of output produced by a segmented fill-bar or meter.

### Safest reading
Even without forcing the final gameplay stat name, the structural role is now strong:

> `C1:06F0` = **render a scaled segmented bar/meter into the lane’s `0CC0` strip block**

And this is the first pass where `99DD` and `9F22` can be read as more than anonymous carried-state bytes:

- `99DD[lane]` behaves like a current/display value
- `9F22[lane]` behaves like a scale/divisor/capacity input

Those names should still remain provisional, but the bar-rendering role is strong.

---

## 5. `CC:FAE9` is the **3-entry `0E80` lane-marker anchor table**
The live word values are:

```text
0002, 0082, 0102
```

Again this is the same three-lane `0x80` block spacing.

### Caller proof: `C1:1918..1969`
That path:

1. clears the old lane marker using `991F`
2. loads `FAE9[old_lane]`
3. writes `FF` to:
   - `0E80`
   - `0E82`
   - `0EC0`
   - `0EC2`
4. loads the new lane from `95E5`
5. loads `FAE9[new_lane]`
6. writes:
   - `60`
   - `61`
   - `62`
   - `63`
   plus companion `29` bytes to the matching odd positions

This is not a generic record mutation.
It is a very small, highly patterned **lane-marker glyph refresh** inside `0E80`.

So the safe reading is now:

> `FAE9` = **lane-marker anchors for the three `0E80` companion-record blocks**

and

> `C1:1918..1969` = **clear the old `0E80` lane marker and stamp the current one**

That materially tightens the `0E80` side of the seam.

---

## 6. There is now hard **read-side consumer proof** for `0E80`
This pass did not fully solve the downstream consumer routine, but it did find direct read-side proof in bank `C0`.

At both:

- `C0:A2BD / A2C4`
- `C0:A32A / A331`

the code does this exact read pair:

```text
LDA $7F0E00,X
STA $0C00,Y

LDA $7F0E80,X
STA $0C01,Y
```

### What that proves
This is enough to promote one important fact:

> `0E80` is not a dead-side build artifact or a private scratch block.
> It is directly consumed downstream as one byte lane of a paired merge/composition path.

The exact high-level meaning of the downstream `0C00/Y` target remains unresolved, so the final gameplay-facing label should still stay open.
But the “is `0E80` really consumed?” question is now settled.

---

## 7. Net result of pass 47
This pass materially advanced the presentation-strip seam in five ways.

### 1. It hardened the small `CC:FAxx` tables into exact anchor roles
The `FA23 / FA29 / FA2F / FA35 / FA3B` family is now best read as:

> **three-lane anchor offset tables for distinct `0CC0` strip subfields/layouts**

### 2. It collapsed `FADD` to its proven role
The live part of `FADD` is simply the three lane-block bases:

```text
0000, 0080, 0100
```

### 3. It found the actual full-strip rebuild entry
`C1:0299` is now pinned as the real:

> **full rebuild/controller entry for the three-lane `0CC0` companion strip**

### 4. It turned `06F0` into a real semantic renderer
`06F0` is no longer a mystery helper.
It is a:

> **scaled segmented bar/meter renderer**

inside the lane strip.

### 5. It finally gave `0E80` hard read-side proof
The `FAE9` anchors plus the `1918..1969` marker refresh and the bank-`C0` read pair together make `0E80` much less abstract.

---

## Next clean seam after pass 47
The best continuation target is now:

1. the exact downstream consumer routine around:
   - `C0:A2B0..A335`
2. the exact semantics of the helper-generated dynamic glyph groups routed through:
   - `9499..949F`
   - `104E`
   - `011F / 0174`
3. whether the `0CC0` strip and `0E80` marker/record blocks belong to a single three-lane status panel, command panel, or another presentation layer

That is the cleanest remaining abstraction gap on this strip/record presentation branch.
