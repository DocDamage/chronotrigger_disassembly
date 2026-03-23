# Chrono Trigger Disassembly — Pass 76

## Scope of this pass
This pass continues directly from the pass-75 seam.

Pass 75 proved that the fixed follow-up tail is:

- `AC57 = service-04 hook`
- then packet apply through `AC85 -> EC7F`

But that still left one real blind spot:

- what **service 04** actually is
- how `AE91 / AE92 / AE93` steer it
- whether the two proven callers are really using the same body or different submodes

This pass closes that gap.

The biggest upgrade is simple and real:

> service `04` is **not** one monolithic helper body.
> It is a local **mode dispatcher keyed by `AE92`**.
>
> And the two already-proved late callers split cleanly across two different service-04 modes:
>
> - `BFAA` seeds `AE92 = 1` and therefore routes into **mode 1**
> - `895B` seeds `AE92 = 2` and therefore routes into **mode 2**

That matters because it stops collapsing the current-tail runner and the fixed-`7F` follow-up runner into the same vague “service-04 blob.”
They share the service family and the common emit/finalize tail, but they do **not** share the same profile-loader front end.

---

## 1. `C1:431D` is the real service-04 mode dispatcher, and `AE92` is the mode byte
Direct bytes:

```text
C1:431D  AD 92 AE
C1:4320  C9 04
C1:4322  90 01
C1:4324  7B
C1:4325  0A
C1:4326  AA
C1:4327  FC 63 7A
C1:432A  60
```

This is exact:

1. load `AE92`
2. if `AE92 >= 4`, clamp/fallback to `0` by zeroing `A`
3. `ASL A`
4. `JSR (7A63,x)`
5. `RTS`

So `AE92` is no longer fuzzy context scratch.
It is the **service-04 submode selector**.

And the local jump table at `C1:7A63` resolves directly as:

```text
mode 0 -> C1:475A
mode 1 -> C1:432C
mode 2 -> C1:45A0
mode 3 -> C1:475B
AE92 >= 4 -> fallback to mode 0
```

That immediately sharpens the already-proved late callers:

- `C1:BFAA` seeds `AE92 = 1`
- `C1:895B` seeds `AE92 = 2`

So the two callers are using:

- **mode 1** for the current-tail/current-occupant follow-up path
- **mode 2** for the fixed-`7F` follow-up path

Safest upgraded reading:

> `C1:431D` = **service-04 mode dispatcher keyed by `AE92`**

---

## 2. Mode 1 (`C1:432C`) is the current-tail / current-context profile-loader front end, with separate head-slot and tail-slot branches
Mode 1 begins here:

```text
C1:432C  AD 91 AE
C1:432F  C9 03
C1:4331  90 03
C1:4333  4C 97 44
```

So the first split is immediate:

- `AE91 < 3`  -> head-slot branch at `432C`
- `AE91 >= 3` -> tail-slot branch at `4497`

That is already a concrete noun improvement:

> `AE91` is the **service-04 source/current slot selector**, and mode 1 treats `0..2` and `3..10` as distinct profile families.

### 2a. Mode-1 head-slot branch (`432C..4496`)
The front half does this:

- calls setup helpers (`JSL CCF110`, `JSR 49FF`)
- transforms `AE91` through `CC:F83F[...] -> 1C48[...]`
- computes a **15-stride index**
- then chooses one of **three parallel table families** in bank `CD`

The three family packs are selected by:

- sign of `AE9B`
- and later `9930`

The actual table groups are:

- `CD:4000 / 4015`
- `CD:4007 / 401A`
- `CD:400E / 401F`

Across those families, mode 1 loads the working profile bytes into:

- `9877`
- `987A`
- `987B`
- `987E`
- `9881`
- `9884`

Then it derives secondary working values through shared bank-`D1/CD/CE` lookup helpers and falls into the common runner at `4833`.

This is not yet enough to freeze a gameplay-facing noun like “animation,” “formation,” or “projectile.”
But it is enough to pin the structure:

> mode-1 head-slot handling = **table-driven current-context profile loader using three alternate head-slot table families, then common emit/finalize**

### 2b. Mode-1 tail-slot branch (`4497..459F`)
This branch is much cleaner structurally.

Direct front-half shape:

- reduce the slot to tail-local form via `AE91 - 3`
- use `9853[tail_local]`
- build a **6-stride** profile index
- choose between two bank-`CD` table families based on `AE93`

Those two families are:

- `CD:4926...` when `AE93 == 0`
- `CD:4F26...` when `AE93 != 0`

The loaded working bytes are again pushed into the same `9877 / 987A / 987B / 987E / 9881 / 9884` neighborhood, then the branch converges into the same shared runner at `4833`.

So mode 1 is now clearly one service-04 family with two source-slot partitions:

- head-slot profile families
- tail-slot profile families

Safest upgraded reading:

> `C1:432C..459F` = **service-04 mode-1 current-context profile loader and emitter front end, split by `AE91` into head-slot and tail-slot profile families**

---

## 3. Mode 2 (`C1:45A0`) is the fixed-follow-up profile-loader front end, and it is the exact mode reached by the pass-74/75 fixed-`7F` tail
Pass 74 already proved:

- `895B` stores incoming `A` into `AE93`
- seeds `AE91 = 0`
- seeds `AE92 = 2`
- then runs `AC57`

Pass 75 proved:

- `AC57` first invokes service `04`

Pass 76 closes the loop:

- `AE92 = 2` lands in `C1:45A0`

So the fixed-`7F` path from globals `91` and `99` is now structurally exact:

```text
A = 0x7F
-> 895B   (AE93 = 0x7F, AE91 = 0, AE92 = 2)
-> AC57
-> service 04 mode 2 at 45A0
-> common runner at 4833
-> packet apply tail continues
```

### 3a. Mode-2 head-slot branch (`45A0..4681`)
The front-half computation is straightforward:

```text
X = 7 * AE93
```

Then it loads a real **7-byte profile record** from bank `CD`:

- `CD:45A6 + 7*AE93`

into working bytes:

- `9877`
- `987A`
- `987B`
- `987E`
- `9881`
- `9884`
- `987C`

Then it derives secondary working values through the same shared `D1/CD/CE` lookup family and converges to the common runner at `4833`.

### 3b. Mode-2 tail-slot branch (`4682..4758`)
This is the tail-slot sibling of the head branch.

It uses the same:

- `X = 7 * AE93`
- same working-byte destinations
- same shared derivation chain
- same convergence into `4833`

But its primary record base moves to:

- `CD:5526 + 7*AE93`

So mode 2 is now strongly pinned as a real profile-record family, not generic scratch logic.

Safest upgraded reading:

> `C1:45A0..4758` = **service-04 mode-2 fixed-follow-up profile loader and emitter front end, split by `AE91` into head-slot and tail-slot record families**

This is the most important architectural gain in the pass because it turns the pass-74/75 fixed-`7F` tail into a real path rather than a blob of chained helpers.

---

## 4. `C1:4833` is the shared service-04 emit/finalize runner used by both mode 1 and mode 2
Both mode 1 and mode 2 converge into:

```text
C1:4833
```

This routine is still too large to freeze every last internal noun, but its outer contract is now strong enough to stop calling it generic cleanup.

The provable top-level structure is:

1. consume working bytes already loaded into the `9877..9885` neighborhood
2. run two fixed bank-`CD` long calls:
   - `JSL CD:0015`
   - `JSL CD:002A`
3. optionally run `JSL CD:0018` only when:
   - `AE93 != 0x37`
   - `AE94 == 0`
   - `987C != 0xFF`
4. run `JSR 48EC`
5. prepare a `C3:0002` call using `7E:2D00..` workspace pointers
6. run `JSR 4943` exactly eight times
7. emit sixteen 6-byte output records into the `5D00..` family while setting `A07B[...] = 1`

That is enough to pin the shared role:

> `C1:4833` = **common service-04 output materialization / emit-finalize runner**

Two small but useful follow-ups also become visible here:

- `AE94` is not random scratch; it is a real suppress/override gate for the optional `CD:0018` stage
- `48EC` and `4943` are both service-04-local output builders, not unrelated helpers

I am keeping those helper nouns structural for now because the final emitted object/data type still needs one more pass.

---

## 5. Resulting cleaned-up service-04 picture
After this pass, the proven service-04 architecture is:

### dispatcher
- `431D` = dispatch on `AE92`
- mode table at `7A63`

### proven active modes used by the current late seam
- mode `1` (`432C`) = current-tail/current-context front end
- mode `2` (`45A0`) = fixed-follow-up front end

### shared steering bytes
- `AE91` = source/current slot selector used to split head vs tail profile families
- `AE92` = service-04 mode selector
- `AE93` = profile/pattern index used directly as the record selector in mode 2 and as a family selector/gate in mode 1
- `AE94` = suppress/override gate for the optional `CD:0018` stage inside the shared runner

### shared tail
- `4833` = common emit/finalize runner

This is a real architectural gain:

- pass 74 proved the packet callers
- pass 75 proved the service-04 entry wrapper
- pass 76 proves that service 04 itself is a **small mode-driven profile/emitter subsystem**

That is a lot tighter than the old “service-04 hook” wording.

---

## Honest caution
Three things should stay explicit even after this pass:

1. I have **not** frozen a final gameplay-facing noun for the things emitted by `4833 / 48EC / 4943`.
   The subsystem is clearly profile-driven and output-producing, but whether the best final noun is “effect,” “follow-up object,” “overlay,” or something adjacent still wants another pass.

2. I have **not** finished modes `0` and `3` at `475A / 475B`.
   The dispatcher proof is real, but those two entries should stay outside the solved bucket for now.

3. I have **not** finished the per-byte field semantics of the 17-byte `CC:213F` descriptor records copied into `AEE6..AEF6`.
   This pass proved the live service-04 mode structure first; the per-byte descriptor nouns are still the next better target.

---

## Best next targets after pass 76
1. crack `48EC` and `4943` so the common service-04 tail gets a final output noun
2. finish service-04 modes `0` and `3` at `475A / 475B`
3. return to the `CC:213F -> AEE6..AEF6` 17-byte record fields with the now-cleaner service-04 mode picture in hand
