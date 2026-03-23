# Chrono Trigger Disassembly — Pass 73

## Scope of this pass
This pass continues directly from the pass-72 seam.

Pass 72 left two explicit targets:

- fully crack global `9C`
- re-open the helper chain around:
  - `C1:8CF9`
  - `C1:E89F`
  - `C1:EBF8`
  - `C1:EC7F`

This pass does exactly that.

The biggest improvement is not a cosmetic rename.
It is a real architectural cleanup:

> the `AD9C/AD9E/EBF8/EC7F` family is **not** vague “lane geometry glue.”
> It is a concrete **pending signed stat-delta packet system** rooted in 4-byte entries,
> with `EBF8` seeding packets and `EC7F` applying them into the lane-current scalar pairs.

That in turn sharpens both:

- the outer controller at global `9C`
- the helper-chain interpretation behind globals `91`, `98`, and `99`

And it gives `C1:8CF9` a much safer structural identity:

> a **current-tail selector-control interpreter / materialization controller**
> rather than an anonymous service-side blob.

---

## 1. `C1:E89F` and `C1:E8C0` are packet-slot offset calculators into a `0x2C`-byte record family
These two tiny helpers looked like generic arithmetic before this pass.
They are now much tighter.

### `C1:E89F..C1:E8BE`
Direct bytes:

```text
C1:E89F  7B AA 86 0E
C1:E8A3  AD FD B1
C1:E8A6  0A 0A
C1:E8A8  85 0E
C1:E8AA  AD 9B AD
C1:E8AD  AA
C1:E8AE  86 2A
C1:E8B0  A2 2C 00
C1:E8B3  86 28
C1:E8B5  20 0B C9
C1:E8B8  A5 2C
C1:E8BA  18 65 0E
C1:E8BC  85 0E
C1:E8BE  60
```

With `C1:C90B` already locked as:

> 16-bit multiply of `DP28 * DP2A -> DP2C`

this helper is now direct arithmetic, not guesswork.

What it computes:

- `DP0E = 4 * B1FD`
- `DP2C = 0x2C * AD9B`
- final result:
  - `DP0E = 0x2C * AD9B + 4 * B1FD`

That is a hard structural result.

### `C1:E8C0..C1:E8E0`
The sibling helper does the same thing, but uses `B18B` instead of `B1FD`:

- `DP10 = 4 * B18B`
- `DP2C = 0x2C * AD9B`
- final result:
  - `DP10 = 0x2C * AD9B + 4 * B18B`

### What that proves
A stride of `0x2C` is `44`, which is exactly:

- `11` slots
- `* 4` bytes per slot

So the safe reading is:

- `AD9B` selects one record inside a `0x2C`-byte record family
- `B1FD` or `B18B` selects one **4-byte per-slot packet** inside that record
- `E89F/E8C0` compute the exact byte offset for that packet

That is the first hard anchor for the `AD9C/AD9E` packet workspace.

---

## 2. `C1:EBF8` seeds one signed pending stat-delta packet into the `B328` family
This helper is now much stronger than “some downstream writer.”

Direct bytes:

```text
C1:EBF8  7B
C1:EBF9  AD 02 B2
C1:EBFC  8D 03 B2
C1:EBFF  89 80
C1:EC01  F0 0F
C1:EC03  C2 20
C1:EC05  AD 89 AD
C1:EC08  49 FF FF
C1:EC0B  1A
C1:EC0C  8D 89 AD
C1:EC0F  7B
C1:EC10  E2 20
C1:EC12  AD C7 B2
C1:EC15  AA
C1:EC16  86 28
C1:EC18  A2 2C 00
C1:EC1B  86 2A
C1:EC1D  20 0B C9
C1:EC20  0A 0A
C1:EC22  18 65 2C
C1:EC24  A8
C1:EC25  C2 20
C1:EC27  AD 89 AD
C1:EC2A  99 28 B3
C1:EC2D  7B
C1:EC2E  E2 20
C1:EC30  AD 03 B2
C1:EC33  99 2B B3
C1:EC36  60
```

### What it does
1. mirrors `B202 -> B203`
2. if `B202` bit `0x80` is set:
   - negate `AD89` as a signed 16-bit value
3. compute a packet offset from:
   - `B2C7`
   - `0x2C`
   - then `<< 2`
4. write:
   - `AD89 -> B328[offset]` as a 16-bit value
   - `B203 -> B32B[offset]` as the packet flag byte

### Strongest safe reading
This is not generic scratch export.
It is a **packet writer** for one 4-byte per-slot record:

- `B328/B329` = signed 16-bit amount
- `B32B` = packet flags copied from `B202`

The fourth byte in the 4-byte record remains unresolved here,
so the label should stay structural rather than over-flavored.

But the core meaning is now strong:

> `C1:EBF8` = **queue one signed pending stat-delta packet into the `B328` packet family**

### Flag meaning tightened in this pass
Two flag bits are now materially stronger:

- `B202` bit `0x80`
  - selects signed negation before write
  - safe reading: **sign / add-vs-subtract control**
- `B202` bit `0x40`
  - later routes the packet into the parallel `5E34/5E36` phase in `EC7F`
  - safe reading: **parallel secondary-stat path selector**
  - best-fit gameplay noun is MP-side, but keep that final noun slightly cautious
- `B202` bit `0x20`
  - later prevents automatic packet clearing in `EC39`
  - safe reading: **persistent / hold packet flag**

---

## 3. `C1:EC39` clears non-persistent packet channels and associated scratch
This helper was easy to underestimate because it sits between the packet writer and the packet applier.

But its loop is direct.

It walks the 4-byte packet channels in three parallel families:

- `B328`
- `B354`
- `B380`

For each channel group, it checks the packet flag byte:

- `B32B`
- `B357`
- `B383`

If **none** of those three flag bytes carries bit `0x20`, it zeroes the channel data.

It also clears nearby scratch/export bytes such as:

- `AEB2`
- `AEB0,X`
- `AE82,X`

under the later-loop part of the same scan.

Strongest safe reading:

> `C1:EC39` = **clear non-persistent pending stat-delta packet channels and associated scratch/export bytes**

That is a real packet-lifecycle helper, not generic cleanup.

---

## 4. `C1:EC7F` applies pending packet channels into the lane-current scalar pairs
This is the biggest concrete win in the pass.

Pass 49 had already hardened:

- `5E30[x]` = current HP
- `5E32[x]` = max/cap HP
- `5E34[x]` = parallel current scalar, best read as current MP
- `5E36[x]` = parallel cap scalar

Re-opening `EC7F` against that context turns the helper into a real packet applier.

### HP/current-primary phase
The first phase:

- calls `EC39`
- iterates lane blocks with `X += 0x80`
- iterates the 4-byte packet channels with `Y += 4`
- for each of the three channel families:
  - `B328`
  - `B354`
  - `B380`
- subtracts the 16-bit packet amount from `5E30[x]`
  **when the packet does not carry the secondary-stat route bit**
- then clamps the result against:
  - zero
  - `5E32[x]`

That is the exact same lane-current-vs-cap pattern pass 49 already proved for HP.

So the first phase is now strong:

> apply queued signed packet amounts into **current HP** and clamp to `0..max HP`

### Parallel secondary-stat phase
The second phase starts at `ED1D` and does the same structural thing against:

- `5E34[x]`
- `5E36[x]`

but only for packets that do carry the secondary-stat route bit.

Safest reading:

> apply queued signed packet amounts into the **parallel secondary current/cap scalar pair**

Best-fit gameplay noun is MP-side,
but because `5E36` still has not been independently frozen in an earlier pass,
this should remain written one notch below absolute certainty.

### Side effects after application
The helper also performs lane-refresh side effects, including:

- setting `5E4A.bit7` under a visibility/occupancy gate
- conditionally calling `JSL FD:ABA2`
- preserving / clearing packet channels through the flag logic already discussed

So `EC7F` is not just arithmetic.
It is the real **apply-and-refresh** stage for this packet system.

Strongest safe reading:

> `C1:EC7F` = **apply pending HP/secondary-stat packet channels into lane current values, clamp them, and trigger the needed lane refresh side effects**

---

## 5. The `AD9C/AD9E` helper chain behind globals `91`, `98`, and `99` is now materially stronger
Before this pass, the cleanest wording was still “geometry / helper chain / seed gate.”
That is now too vague.

What is now strong:

- `AD9C/AD9E` is part of a **4-byte per-slot packet workspace** indexed through `0x2C * record + 4 * slot`
- `EBF8` writes signed packet amounts plus packet flags
- `EC39` manages packet persistence / clearing
- `EC7F` applies those packets into the lane-current scalar pairs

So the helpers used by globals:

- `91`
- `98`
- `99`

should now be read as seeding and applying **pending signed lane-stat delta packets**,
not as generic opaque controller glue.

Important honesty:

- that does **not** magically solve the final gameplay noun of every caller
- especially `91`, where the front-end still uses `5E32/5E64/C92A` before packet seeding
- but the back-end packet system itself is no longer vague

That is a genuine upgrade in confidence.

---

## 6. `C1:8CF9` is a current-tail selector-control interpreter / materialization controller
This helper was the other half of the seam.

Direct re-open of `C1:8CF9..8EA6` now supports a much stronger structural label.

### What it undeniably does
At entry it:

- initializes current-tail context from `AEC8`
  - `B252 = AEC8`
  - `B18B = AEC8 + 3`
- clears selection/result scratch such as:
  - `AE93..AE9B`
  - `AE97/AE98 = FF`

Then it chooses a command-stream pointer from either:

- the saved per-tail pointer pair in `B1D4/B1E4`
- or the alternate continuation pointer in `B273`
  - gated by `B2C0`

It fetches the current `CC`-bank command byte into `AEE3` and dispatches through:

- `JSR ($B88D,X)`

which is the already-established selector-control / promoted late-band dispatch table.

So this helper is not a random side service.
It is a real **interpreter/driver** for the late selector-control stream.

### What the result side proves
After dispatch it:

- checks `AF24`
- branches on `B3B8`
- uses selection scratch such as:
  - `AD8E`
  - `AECC`
  - `AECB`
  - `AE91`
- scans for free visible-head slots when needed
- writes visible-slot and saved-state fields such as:
  - `5E0D`
  - `B242`
  - `B1D4`
- manages continuation / replay state through:
  - `B2C0`
  - `AE55`

And in the success/materialization path it can call the already-known tails:

- `D8D1`
- `D7C4`

which is exactly the kind of side effect expected from a controller that turns selector-control results into live head-slot state changes.

### Strongest safe reading
The pass does **not** claim the final gameplay noun of every field in that state machine.
But it is now stronger than “service helper.”

Safest upgraded reading:

> `C1:8CF9` = **run the current tail lane’s selector-control stream, materialize or update the resulting head-slot assignment/state, and maintain the saved continuation pointer**

That is the right structural level for future passes.

---

## 7. Re-reading global `9C` with those helpers in hand upgrades it from vague controller to a real tail-lane service/reseat controller
This is the main top-level promotion in the pass.

### Tail-lane loop is now direct
The `8461` handler clearly loops the current tail partition:

- uses `B315` / `B252` / `B18B = current + 3`
- scans tail lanes `3..10`
- maps them through `B179/B163`

That alone already makes “general lane controller” too loose.
It is specifically walking the **tail lane band**.

### What it does for eligible occupied tail lanes
For eligible mapped tail lanes, it:

- requires an occupied lane through `AEFF`
- checks state bytes like `AFAB`, `B247`, and `5E0A`
- invokes `C1:8CF9`
- on the follow-up path:
  - mirrors `B158 -> AFAB`
  - calls `BD6F` to apply status modifiers to the lane readiness increment
  - sets `B03A = 1`

That is no longer just “some service-side work.”
It is explicit **tail-lane service / readiness-shadow refresh** work.

### What it does after the per-tail pass
After the tail loop, it runs the already-hardened reconciler/export helpers:

- `B575`
  - canonical record / lane-pair reconciliation
- `B725`
  - visible active-time/readiness gauge export init
- plus the nearby commit/cleanup helpers:
  - `AC5E`
  - `AC46`
  - `FD:ACEE`
  - `FD:AC6E`

That makes the outer routine’s role much tighter:

- service eligible tail lanes
- run their selector-control / materialization stream
- refresh readiness-shadow state
- reconcile canonical/head-visible state
- refresh/export the visible readiness gauge layer

### Strongest safe reading
This is now strong enough to promote the global label one tier.

Best structural reading:

> global `9C` is the **service-7 tail-lane admission/reseat and readiness-refresh controller**

The word “admission/reseat” is the safest phrasing because:

- `8CF9` clearly drives head-slot materialization/update
- the outer loop clearly services tail lanes
- the downstream helpers clearly reconcile canonical/head-visible state

That is materially stronger than the old “lane controller in the neighborhood of active-time.”

---

## Net result of pass 73
This pass makes three real upgrades:

1. it converts the `AD9C/AD9E/EBF8/EC7F` chain from vague helper glue into a concrete
   **pending signed stat-delta packet system**
2. it upgrades `C1:8CF9` into a real
   **tail selector-control interpreter / materialization controller**
3. it upgrades global `9C` from a generic service-side controller into the stronger structural read:
   **service-7 tail-lane admission/reseat and readiness-refresh controller**

That is enough to promote `9C` and its local selector twin out of the fuzzy bucket.

---

## Honest cautions that still remain
Even after this pass, a few things should stay explicit:

- the exact fourth byte in each 4-byte packet record is still unresolved here
- the final gameplay-facing noun of the `5E34/5E36` pair is still slightly below fully frozen, even though MP-side is the best fit
- `C1:8CF9` is now structurally much stronger, but the exact human-facing names of fields like `B242`, `AE55`, and some continuation bits still need more proof

So the upgrade is real,
but it should stay structural and not pretend every subfield is solved.

---

## Best next seam after this pass
The cleanest next move is now:

1. re-open the packet-record callers around `91 / 98 / 99` and promote their front-end nouns using the new packet-system proof
2. tighten the `5E34/5E36` pair to a fully locked MP/current-cap read if a cleaner direct spend/check path is found
3. continue through the still-loose helper tails touched by `9C` / `8CF9`, especially the remaining commit/continuation bytes around:
   - `AE55`
   - `B242`
   - `FD:ABA2`
   - `FD:AC6E`
