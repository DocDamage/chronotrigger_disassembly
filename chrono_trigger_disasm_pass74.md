# Chrono Trigger Disassembly — Pass 74

## Scope of this pass
This pass continues directly from the pass-73 seam.

Pass 73 left three useful cleanup targets inside the late packet / materialization neighborhood:

- re-open globals `91 / 98 / 99` with the now-proved pending stat-delta packet system
- tighten the shared helper tail around:
  - `C1:895B`
  - `C1:AC57`
  - `C1:AC85`
  - `FD:ACEE`
- stop treating `AE55` and `B2C0` as anonymous continuation bytes

This pass does exactly that.

The biggest upgrade is this architectural cleanup:

> globals `91` and `99` are **not** just “lane geometry seeders.”
> They are **dual-path packet callers**:
> they populate a transient `AD9C` workspace,
> queue a live signed stat-delta packet through `EBF8`,
> then run a shared fixed-`7F` follow-up tail that ends in packet apply and workspace clear.

By contrast, global `98` is the stripped-down fast path:

> it skips the transient `AD9C` workspace entirely
> and directly queues + applies one packet through `EBF8 -> EC7F`.

That also gives two state fields much cleaner roles:

- `B2C0` = armed alternate continuation-pointer flag
- `AE55` = descriptor/option flags for materialization and continuation behavior

---

## 1. `C1:895B` is a fixed follow-up-context seeder, not random scratch
Direct bytes:

```text
C1:895B  8D 93 AE
C1:895E  9C 91 AE
C1:8961  A9 02
C1:8963  8D 92 AE
C1:8966  9C 94 AE
C1:8969  9C 95 AE
C1:896C  A9 80
C1:896E  8D 96 AE
C1:8971  20 57 AC
C1:8974  60
```

Whatever arrives in `A` is copied into `AE93`, then the helper seeds a fixed context:

- `AE91 = 0`
- `AE92 = 2`
- `AE94 = 0`
- `AE95 = 0`
- `AE96 = 0x80`
- then `JSR AC57`

That is not generic cleanup.
It is a real **follow-up-context seed + dispatch tail**.

The important pass-74 observation is that both globals `91` and `99` call this helper with:

- `A = 0x7F`

So they share one fixed follow-up packet / context kind after their packet write path.

Safest upgraded reading:

> `C1:895B` = **seed fixed follow-up context from `A` into `AE91..AE96` and run the common `AC57` tail**

---

## 2. `C1:AC57` and `C1:AC85` are the common tail that bridges follow-up handling into packet apply
Direct bytes:

```text
C1:AC57  20 A4 BF
C1:AC5A  20 85 AC
C1:AC5D  60

C1:AC85  20 7F EC
C1:AC88  60
```

This is straightforward:

- `AC57` calls `BFA4`
- then calls `AC85`
- `AC85` is just `JSR EC7F ; RTS`

So the structural split is now safe:

- `AC57` = common follow-up tail
- `AC85` = tiny packet-apply wrapper

The part that should stay explicit is that `BFA4` is **not** fully solved here.
But the tail role is no longer vague:

> `AC57` is the shared bridge from follow-up-context handling into **pending stat-delta packet application**.

That matters because `91` and `99` both end by entering this exact tail through `895B`.

---

## 3. `FD:ACEE` is a real workspace clearer for the transient `AD9C` packet records
Direct bytes:

```text
FD:ACEE  7B
FD:ACEF  AA
FD:ACF0  8D 9B AD
FD:ACF3  9D 9C AD
FD:ACF6  E8
FD:ACF7  E0 B0 00
FD:ACFA  90 F7
FD:ACFC  6B
```

This loop is much cleaner than the old “late helper cleanup” wording.

What it does:

1. zero `A` (`TDC`)
2. zero `X` (`TAX`)
3. clear `AD9B`
4. clear `AD9C + X`
5. increment `X`
6. repeat until `X == 0x00B0`
7. `RTL`

That means it clears exactly:

- `AD9B`
- `AD9C..AE4B` (`0xB0` bytes)

This is a hard structural size proof.
And because pass 73 already proved the packet indexing formula:

- `0x2C * record + 4 * slot`

`0xB0 = 4 * 0x2C` means the cleared block is a transient:

- **4 records**
- each record = **11 slots**
- each slot = **4 bytes**

So the safest promoted reading is now:

> `FD:ACEE` = **clear the transient 4-record `AD9C` packet workspace and reset `AD9B`**

That is a real memory-model upgrade, not just another helper nickname.

---

## 4. Global `91` is a dual-path packet caller, not just a geometry seeder
Handler body: `C1:88C5..C1:8974`

Pass 72 had already pinned the lane gating.
Pass 74 tightens what the gated success path actually *does*.

### The already-solid front end
It still does the same proven setup:

- choose lane from `B179[1]`, or `AEC7` if zero
- map through `B163`
- require:
  - `5E4A[lane_block].bit7 = 1`
  - `5E4B[lane_block].bit6 = 0`
- set `AFC1[lane] = 1`
- compute `AF32[lane] = B0DF[lane] + 5E64[lane_block]`

### What the packet path proves now
After that front end, the code does three distinct things:

1. seeds `DP28/29` from `5E32/33`
2. seeds `DP2A` from a `5E64`-derived scale
3. runs `JSR C92A`

Then it uses the result in a dual path:

- **transient workspace path**
  - computes `0x2C * AD9B + 4 * lane` through `E89F`
  - stores the 16-bit result into `AD9C[offset]`
  - stores mode `3` into `AD9E[offset]`
- **live queued packet path**
  - clears `B202`
  - runs `JSR EBF8`

And after that it immediately runs the shared follow-up/apply tail:

- `A = 0x7F`
- `JSR 895B`
- `JSL FD:ACEE`

### Strongest safe reading
This is materially stronger than pass 72’s wording.
The command is not just “seed geometry scratch.”
It is doing all of the following:

- computing a scaled stat-delta amount from lane-state inputs
- mirroring that amount into the transient `AD9C` workspace in mode `3`
- queuing a live signed packet through `EBF8`
- running the shared fixed-`7F` follow-up/apply tail
- clearing the transient workspace afterward

Safest upgraded reading:

> **global `91` conditionally computes a scaled lane-derived primary-stat delta, mirrors it into transient packet workspace mode `3`, queues the live packet, and runs the shared `7F` follow-up/apply tail**

### Important caution
The exact consumer of the transient `AD9C/AD9E` write inside the shared `7F` tail is still not fully locked.
So this pass upgrades the command from “geometry seeder” to **dual-path packet caller**, but it does **not** fake the final gameplay noun yet.

---

## 5. Global `98` is the direct fast path: queue + apply one primary-stat packet immediately
Handler body: `C1:8A9F..C1:8B0F`

Pass 72 already had the front-end lane mapping and the `AF7F` side of the opcode.
Pass 74 tightens the optional packet tail.

### The proven direct packet tail
When `5E4B[lane_block].bit4` is set, the code does:

```text
LDX #$0001
STX AD89
TYA
STA B1FD
LDA #$00
STA B202
JSR EBF8
JSR EC7F
```

With pass 73’s packet proof in hand, that means:

- `AD89 = 1`
- target slot = current mapped lane (`B1FD = lane`)
- no sign-flip bit
- no secondary-route bit
- queue packet through `EBF8`
- immediately apply it through `EC7F`

And because `EC7F` subtracts the queued amount from the primary current pair when the secondary-route bit is clear, this is not a neutral helper call.
It is a real **one-point primary-stat decrement fast path**.

### Strongest safe reading
So the old wording “optionally runs `EBF8 -> EC7F`” is no longer enough.
The meaningful structural contract is:

> **global `98` captures the lane-derived `B12C` variant into `AF7F`, and when `5E4B.bit4` is set, directly queues and immediately applies a 1-point primary-stat decrement packet**

This is the stripped-down fast path counterpart to the more elaborate `91` / `99` tails.

---

## 6. Global `99` is the timed secondary-route packet caller with the same shared `7F` tail as `91`
Handler body: `C1:8B10..C1:8BB8`

Pass 72 already locked the countdown behavior.
Pass 74 tightens the expiry helper path.

### The proven expiry path
On countdown expiry, once the lane/block gates pass, the code does:

1. `AD89 = 5`
2. `B1FD = lane`
3. `JSR E89F`
4. store `AD89` into `AD9C[offset]`
5. store mode `2` into `AD9E[offset]`
6. `B202 = 0xC0`
7. `JSR EBF8`
8. `A = 0x7F ; JSR 895B ; JSL FD:ACEE`

The packet bits here matter:

- `B202.bit7` forces signed negation before queue write in `EBF8`
- `B202.bit6` routes the packet into the secondary-stat side in `EC7F`

So this is not just another generic helper seed.
It is a concrete signed secondary-route packet path.

And because the signed amount starts at `5`, the queued live packet becomes the secondary-route **+5** case after the `EBF8` sign flip and `EC7F` subtract semantics are combined.

### Strongest safe reading
This is the strongest upgraded reading that stays honest:

> **global `99` updates its timer/state front end, and on expiry conditionally builds transient packet workspace mode `2`, queues a signed secondary-route `+5` packet for the mapped lane, and runs the shared `7F` follow-up/apply tail**

That is much tighter than “conditionally seeds `AD9C` through a helper path.”

### Important caution
Like `91`, the exact final gameplay-facing noun of the transient mode byte still wants another pass.
So mode `2` and mode `3` should stay structural rather than over-flavored.

---

## 7. `B2C0` is now strong enough to promote as an armed alternate continuation-pointer flag
This is the cleanest state-field win from the `8CF9` tail.

### Entry-side proof
At `8D29`, `8CF9` first checks `B2C0`.

If `B2C0 != 0`, it does **not** resume from the saved per-tail pointer pair in `B1D4/B1E4`.
Instead it uses the alternate continuation pointer in `B273`.

### Exit-side proof
At the tail end of `8CF9`:

- if `AECC < 3`, it returns through `8C3E`
- if `AECC == FF`, it also does not arm continuation
- otherwise, when `AE55.bit3` is clear:
  - `B2C0 = 1`
  - `AE55 = 0`

That is a clean arm/use pattern.

Strongest safe reading:

> `B2C0` is the **armed alternate continuation-pointer flag** for the `8CF9` materialization controller.

That is materially stronger than the old “saved continuation state somewhere around `B273`” wording.

---

## 8. `AE55` is no longer anonymous; it is a descriptor/option flag byte consumed by the `8CF9` continuation tail
Pass 73 correctly left `AE55` loose.
Pass 74 tightens it one level.

### Producer-side proof
At `C1:D879`, the code loads a byte from `CC:6FCC,...` and stores it into `AE55`.
That is table-driven descriptor behavior, not scratch arithmetic.

### Consumer-side proof
At `C1:8E97`, the `8CF9` tail checks:

- `AE55.bit3`

If that bit is clear, it arms `B2C0`.
If that bit is set, it does **not** arm the alternate continuation pointer.

### Strongest safe reading
That is enough to stop calling `AE55` “mystery continuation byte.”

Safest upgraded reading:

> `AE55` is a **materialization descriptor / option-flag byte**, with bit `3` acting as a continuation-arm suppressor for the `8CF9` tail.

The rest of the bits still need more proof.
So this should stay structural and slightly cautious.

---

## 9. The transient packet workspace is now strong enough for real state labels
Pass 73 proved the addressing formula.
Pass 74 adds the hard clear size from `FD:ACEE`.
Together they support a safer state model:

- `AD9B` = current transient packet-workspace record index
- `AD9C..AE4B` = transient 4-record packet workspace
- `AD89` = current signed packet amount seed before queue write
- `B202` = current packet flag byte controlling sign/route/persistence
- `B1FD` = current target slot index for queue write

That is the first point where these bytes are stable enough to promote as a coherent state bundle.

---

## Net result of pass 74
This pass makes five real upgrades:

1. it upgrades globals `91` and `99` from vague “geometry/helper seeders” into **dual-path packet callers**
2. it upgrades global `98` into the direct **queue + apply one-point primary-stat packet** fast path
3. it pins `895B -> AC57 -> AC85` as the shared **follow-up-context -> packet-apply** tail
4. it proves `FD:ACEE` is the clearer for the transient **4-record `AD9C` packet workspace**
5. it promotes `B2C0` and tightens `AE55` as real continuation/materialization control bytes

That is enough to update the late packet caller labels without pretending the final gameplay nouns are finished.

---

## Honest cautions that still remain
A few things should stay explicit even after this pass:

- the exact consumer inside the shared fixed-`7F` follow-up tail is still not fully pinned
- the exact human-facing meanings of transient packet workspace modes `2` and `3` are still open
- `AE55` is now a real descriptor/option byte, but only bit `3` is materially pinned here
- `FD:ABA2` and `FD:AC6E` are still worth a dedicated pass; they are clearly downstream side-effect helpers, but this pass does not force their final nouns

So the gain here is real,
but it stays structural where the proof is still partial.

---

## Best next seam after this pass
The cleanest next move is now:

1. decode the shared fixed-`7F` follow-up tail more tightly by reopening:
   - `C1:BFA4`
   - `C1:BF79`
   - the related `AE91..AE96` consumers
2. then take the remaining downstream side-effect helpers that still touch the same neighborhood:
   - `FD:ABA2`
   - `FD:AC6E`
3. keep `AE55` on the shortlist until more of its table-driven bits are explained
