# Chrono Trigger Disassembly Pass 49

## Scope of this pass
This pass continued directly from pass 48’s seam:

- determine the real meaning of the three numeric fields rendered by `C1:0299`
- resolve what `A10F` actually means in that path
- re-check the `5E30 / 5E32 / 5E34` family against non-UI logic so the labels stop floating at “numeric field” level

The important correction in this pass is that pass 48 treated the `JSR $011B` helper as an 8-bit right shift. That was too loose. The entry at `C1:011B` is a **mid-routine entry** into the `LSR` helper and performs a **3-bit right shift**, not an 8-bit one.

That changes the interpretation materially.

---

## Method
1. Re-read the `C1:0299` numeric writer path with exact entry points for:
   - `C1:010D`
   - `C1:011B`
   - `C1:011F`
   - `C1:0174`
   - `C1:104E`
2. Re-traced every strong non-UI reference to:
   - `5E30`
   - `5E32`
   - `5E34`
3. Focused on three proving bands:
   - `C1:B094..B0B3`
   - `C1:EC90..ECD7`
   - `C1:CC74..CCC5`
4. Only promoted labels that are supported by both the presentation path and the mutator/threshold logic.

---

## Starting point from pass 48
Pass 48 had already established:

- the three dynamic fields in `C1:0299` are numeric, not text
- field A uses `5E30[offset]`
- field B uses `5E32[offset]`
- field C uses `5E34[offset]`
- `A10F` is touched by a compare between field A and a reduced form of field B

But pass 48 still left two big gaps:

1. the exact interpretation of the `5E30/32/34` trio
2. whether `A10F` was a warning/counter, palette selector, or something else

---

## 1. Pass 48’s `>> 8` read was wrong; `C1:011B` is a **3-bit right shift entry**, not an 8-bit shift helper
This is the first thing that needed correction.

### Exact local layout
The helper band is:

```text
C1:010D  0A 0A 0A 0A 0A 0A 0A 0A 60
C1:0116  4A 4A 4A 4A 4A 4A 4A 4A 60
```

But `C1:0299` does **not** call `0116`.
It calls `011B`.

So the actual entered sequence is:

```text
C1:011B  4A
C1:011C  4A
C1:011D  4A
C1:011E  60
```

That means:

> `JSR $011B` = **logical right shift by 3**

not by 8.

This correction makes the threshold logic in the panel path coherent.

---

## 2. `C1:B094..B0B3` directly proves `5E30` and `5E32` are a **current-vs-max HP pair** with a one-eighth critical threshold
This is the strongest proof in the pass.

### Proven code shape
The routine beginning at `C1:B094` does:

```text
BD 2F 5E 29 FE 9D 2F 5E      ; clear bit 0 in 5E2F[x]
C2 20                        ; 16-bit A
BD 32 5E                     ; load 5E32[x]
4A 4A 4A                     ; divide by 8
DD 30 5E                     ; compare against 5E30[x]
90 0A                        ; if (5E32 >> 3) < 5E30, branch
E2 20                        ; otherwise set bit 0 in 5E2F[x]
BD 2F 5E 09 01 9D 2F 5E
```

### Structural meaning
This is exactly the classic:

> **if current HP is at or below one-eighth of max HP, set the critical/low-HP flag**

reading.

Why this is strong:
- the comparison is explicitly `max_like_value / 8` versus `current_like_value`
- the result is stored as a flag bit in a per-record status byte (`5E2F`)
- this is not UI-only behavior; it is core per-record state maintenance

So the safest promoted interpretation is now:

- `5E30[x]` = **current HP**
- `5E32[x]` = **max HP**
- `5E2F.bit0` = **critical / low-HP threshold flag**

That is materially harder than pass 48’s generic “numeric field” wording.

---

## 3. `C1:EC90..ECD7` independently confirms `5E30` is a mutable current value clamped to `5E32`
The second strong proof is the mutator path in the `EC90` band.

### Proven behavior
This band subtracts several possible damage/heal-like quantities from `5E30[x]` and then immediately normalizes the result:

```text
BD 30 5E ... subtract one of several B3xx values ... 9D 30 5E
...
BD 30 5E
30 0F                        ; negative -> special handling
C9 0000 F0 0A                ; zero stays zero
DD 32 5E 90 41               ; if current < max, keep it
BD 32 5E                     ; else clamp to max
```

### Why this matters
This is exactly what you expect from a **current HP** field:
- it is directly mutated by delta logic
- it is not allowed to remain above the paired cap field
- the cap it is clamped to is `5E32[x]`

So pass 49 promotes the pair harder:

> `5E30[x]` is the mutable current HP scalar, and `5E32[x]` is its maximum/cap scalar.

This is no longer just a UI inference.

---

## 4. `A10F` is not a generic warning counter; it is a **lane-local HP-threshold palette selector/count** used by the numeric panel writer
With the `011B` correction and the `B094` proof above, the `0299` compare now reads cleanly.

### Proven `C1:0299` logic
Inside the per-lane writer:

```text
STZ $A10F
...
LDA 5E30[x] -> 9499         ; field A source
BEQ skip_compare
LDA 5E32[x]
JSR $011B                   ; divide by 8
CMP 9499                    ; compare maxHP/8 to currentHP
BEQ skip
BCC set_flag                ; currentHP > maxHP/8
LDA $A110
BEQ skip
INC $A10F
```

Then later, when writing the companion bytes for the generated decimal fields, the routine does:

```text
LDX #$0029
LDA $A10F
BEQ keep_29
LDX #$002D
```

and uses that selected value as the repeated paired byte beside the generated digits.

### What changed from pass 48
Pass 48 treated this as a vague warning counter tied to a bad `>> 8` read.
The correct reading is much tighter:

- `A10F` is reset per lane before the field group is built
- it is only influenced by the current-vs-max-HP threshold check
- it is then used immediately to choose **which numeric attribute/paired-byte value** the lane’s rendered digits receive

Safest keepable reading:

> `A10F` = **lane-local HP-threshold presentation flag/count for the numeric field attribute selection**

I am still keeping the exact human-facing palette/color name conservative, because this pass proves the threshold role harder than the visible color name.

---

## 5. The three numeric fields in `C1:0299` now read best as **current HP, max HP, current MP**
With the HP pair solved harder, the `0299` field family becomes much less ambiguous.

### Field A — `5E30[offset]`
Rendered with:
- `011F` (3-digit formatter)
- `104E` (leading-zero blanker)

And now independently proven elsewhere as the mutable current member of a current-vs-max pair.

Safest promoted reading:

> field A = **current HP**

### Field B — `5E32[offset]`
Also rendered through the 3-digit formatter, and now independently proven as:
- the paired cap for `5E30`
- the source of the `maxHP / 8` critical threshold check

Safest promoted reading:

> field B = **max HP**

### Field C — `5E34[offset]`
This field remains less over-proven than the HP pair, but it tightened materially in this pass.

#### Supporting ROM proof
- it is rendered through the 2-digit formatter (`0174`)
- it is grouped alongside the HP pair in the same per-lane panel record
- `C1:CC74..CCC5` subtracts a computed quantity from exactly one of:
  - `5E34`
  - `5EB4`
  - `5F34`

That pattern is exactly what you expect from a **lane-selected spendable resource**.

Given the display width, the grouping with HP, and the subtraction/use pattern, the safest promoted reading is now:

> field C = **current MP**

I am keeping this one just slightly more conservative than the HP pair, but it is no longer best described as an unnamed auxiliary numeric.

---

## 6. `5E2F.bit0` is now the strongest internal name for the old unresolved “danger/threshold” state
The `B094` path above makes this explicit enough to label.

### Proven behavior
- bit 0 is cleared first
- if the current-vs-max threshold condition is met, bit 0 is set
- the bit lives in the same `0x80`-stride per-lane record family as `5E30/32/34`

Safest reading:

> `5E2F.bit0` = **critical / low-HP state flag**

This also explains why the presentation branch in `0299` cares about the same threshold family.

The UI writer and the record-state flagger are two consumers of the same HP-threshold logic.

---

## 7. This pass makes the three-lane strip/panel much more legible as a party-status presentation branch
I am still being conservative about slapping a final subsystem name on every downstream bank-`C0` consumer.
But the status-panel branch itself is a lot less anonymous now.

The currently proven lane record presentation bundle is:

- fixed 5-glyph lane run
- current HP (3 digits)
- max HP (3 digits)
- current MP (2 digits)
- a scaled bar/meter field
- per-lane marker data in `0E80`
- threshold-sensitive attribute selection tied to low HP

That is no longer “a panel that happens to show some numbers.”
It is plainly a **party-member status presentation lane**.

I am still leaving the final higher-level destination name for the bank-`C0` consumer open.
But the producer side is now substantially harder.

---

## Net result of pass 49
This pass materially advances the pass-48 seam in four ways.

### 1. It corrected the bad shift-width assumption
`JSR $011B` is a **3-bit right shift**, not an 8-bit one.
That correction is central.

### 2. It upgraded `5E30/5E32` from generic numeric fields to a real HP pair
The ROM now supports a strong reading of:
- `5E30` = current HP
- `5E32` = max HP
- `5E2F.bit0` = low-HP/critical threshold flag

### 3. It resolved `A10F` as a local presentation selector tied to the HP threshold
`A10F` is no longer a vague warning counter.
It is a **lane-local numeric-attribute selector/count** driven by the current-versus-one-eighth-max-HP test.

### 4. It tightened `5E34` from “aux numeric” to a likely current-MP field
The subtraction/use path in `CC74..CCC5` plus the 2-digit render path make that reading materially stronger.

---

## Remaining uncertainty after pass 49
The next open seams are narrower now.

1. determine the exact human-facing meaning of the scaled bar path driven by `99DD / 9F22`
   - whether it is a second HP-style bar, an ATB-style bar, or another party-status gauge
2. determine whether the bank-`C0` consumer should now be promoted from generic “parallel source-plane consumer” to a final HUD/status-panel destination name
3. tighten `5E34` from strong-provisional “current MP” to completely locked if a cleaner direct cost-check/spend path is found

