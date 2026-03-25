# Chrono Trigger Disassembly — Pass 67

## Scope of this pass
This pass continued directly from the pass-66 seam and covered the next exposed part of the
master bank-`C1` opcode table:

- alias cluster `23..28`
- global `29..2F`

The main job in this pass was not inventing new logic families from scratch.
It was to consolidate table ownership now that pass 61 already proved:

- `C1:B80D` is the master opcode table
- the old `B85F` “group-1” table is just the global slice starting at opcode `29`

That means the work here is half **exact alias mapping** and half **promoting old local group-1 results into proper global-master labels**.

The biggest useful structural result is:

> global `29`, `2A`, and `2B` are not isolated curiosities.
>
> They are **setup / persistence commands** that feed the later seeded group-2 families:
>
> - `29` and the `AEE3 != 2` path in `2A` write the saved seed/state pair at `5E0D[current] / 5E15[current]`
> - the `AEE3 == 2` path in `2B` writes the alternate saved seed at `B16E[current]`

So this pass materially tightens the bridge between the old group-1 and group-2 command families.

---

## 1. Exact master-table map for `23..2F`
Direct pointer-table bytes at `C1:B853..C1:B86B`:

```text
23 -> C1:95FA
24 -> C1:95FA
25 -> C1:95FA
26 -> C1:95FA
27 -> C1:95FA
28 -> C1:95FA

29 -> C1:9810
2A -> C1:983A
2B -> C1:983A
2C -> C1:98C4
2D -> C1:98C5
2E -> C1:9960
2F -> C1:9961
```

What this proves:

- `23..28` are an exact six-opcode alias run onto the same handler already solved at global `18`
- `29..2F` are the first seven entries of the old `B85F` slice, now promoted to their correct role as master-table globals

---

## 2. Global opcodes `23..28` are exact aliases of opcode `18`
These entries all point to:

```text
C1:95FA
```

That is the same handler body already decoded in pass 66 for global opcode `18`.

### What this means
There is no wrapper distinction here.
At the byte level these are exact table aliases.

So the safest carry-forward is:

- `23` = alias of global `18`
- `24` = alias of global `18`
- `25` = alias of global `18`
- `26` = alias of global `18`
- `27` = alias of global `18`
- `28` = alias of global `18`

### Strongest safe interpretation
All six are:

> **reduce selected entries by indirect-table byte equals immediate**

with the same pass-66 caution preserved about the exact base-pointer wording for the indirect read through `($0A),Y`.

This is useful because the table is now honest:
the apparent “new cluster” after `22` is mostly not new behavior at all.

---

## 3. Global opcode `29` resolves a selector and persists its head plus one inline byte into current-slot saved state
Handler bytes:

```text
C1:9810  AE D2 B1 E8 8E D2 B1 20 14 AC AE D2 B1 E8 8E D2
C1:9820  B1 BF 00 00 CC 8D E5 AE 7B AD 52 B2 AA AD E5 AE
C1:9830  9D 0D 5E AD CC AE 9D 15 5E 60
```

### What it does
1. advances the CC stream pointer by one byte
2. calls `AC14`
3. advances the CC stream pointer by one more byte
4. reads that inline byte into `AEE5`
5. computes:
   - `X = B252`
6. stores:
   - `AEE5 -> 5E0D[X]`
   - `AECC[0] -> 5E15[X]`
7. returns

### Why this matters
Pass 34 already proved that later group-2 opcode `01` seeds its one-entry selected list from:

- `5E15[current]`

and also uses the paired parameter path built from:

- `AEE5`

So opcode `29` is not random bookkeeping.
It is a concrete **selector-head persistence command** feeding that later seeded family.

### Strongest safe interpretation
Global opcode `29` is best carried forward as:

> **resolve selector and persist the selected head plus one inline parameter into current-slot `5E15/5E0D` saved state**

Keep the exact gameplay-facing noun for `5E15` / `5E0D` cautious, but the persistence role is strong.

---

## 4. Global opcodes `2A` and `2B` share one body, but the body intentionally splits on `AEE3`
Handler bytes:

```text
C1:983A  AE D2 B1 E8 8E D2 B1 20 14 AC AD CB AE F0 6B C9
C1:984A  01 F0 22 7B AA A8 BD 3A B2 D9 CC AE F0 11 C8 98
C1:985A  CD CB AE 90 F1 7B A8 E8 8A C9 08 90 E9 80 4B B9
C1:986A  CC AE 8D CC AE AD E3 AE C9 02 F0 23 AE D2 B1 E8
C1:987A  8E D2 B1 BF 00 00 CC 8D E5 AE 7B AD 52 B2 AA 86
C1:988A  0C AD E5 AE 9D 0D 5E AD CC AE 9D 15 5E 80 2A 7B
C1:989A  AD 52 B2 AA AD CC AE 9D 6E B1 AE D2 B1 E8 8E D2
C1:98AA  B1 AE D2 B1 E8 8E D2 B1 80 0F 7B AD 52 B2 AA A9
C1:98BA  FF 9D 42 B2 A9 02 8D 24 AF 60
```

### Shared front half
Both opcodes do the same early selection logic:

1. advance the CC stream pointer by one byte
2. call `AC14`
3. if `AECB == 0`, fail
4. if `AECB == 1`, keep that one entry
5. if `AECB > 1`, choose the first selected entry according to the external priority order in:
   - `B23A[0..7]`
6. copy the chosen entry into:
   - `AECC[0]`

This is not a reducer through `AE21`.
It is its own **ordered-first-choice collapse** driven by `B23A`.

### Split point
After choosing the winning entry, the handler checks:

- `AEE3`

Pass 31 already proved `AEE3` is the current group-1/group-2 opcode-class byte tracked by the dispatcher.
That lets the shared entrypoint separate the real opcode behaviors.

---

## 5. Global opcode `2A` (`AEE3 == 1`) persists the chosen entry into `5E15[current]` with one inline parameter in `5E0D[current]`
For the `AEE3 != 2` branch reached by global `2A`, the handler:

1. advances the CC stream pointer by one more byte
2. reads one inline byte into `AEE5`
3. computes:
   - `X = B252`
4. stores:
   - `AEE5 -> 5E0D[X]`
   - `AECC[0] -> 5E15[X]`
5. returns success

### Strongest safe interpretation
Global opcode `2A` is best carried forward as:

> **resolve selector, collapse it to the first entry by `B23A` priority, then persist that chosen entry plus one inline parameter into current-slot `5E15/5E0D` saved state**

This is a stronger sibling of opcode `29`:
- `29` simply stores the current selected head
- `2A` first imposes the explicit `B23A` ordering rule, then stores the chosen result

---

## 6. Global opcode `2B` (`AEE3 == 2`) persists the chosen entry into `B16E[current]` and skips two inline bytes
For the `AEE3 == 2` branch reached by global `2B`, the handler instead:

1. computes:
   - `X = B252`
2. stores:
   - `AECC[0] -> B16E[X]`
3. advances the CC stream pointer twice more
4. returns success

### Why this matters
Pass 34 already proved that later group-2 opcode `02` seeds its one-entry selected list from:

- `B16E[current]`

So `2B` is the alternate saved-seed writer feeding that second seeded family.

### Strongest safe interpretation
Global opcode `2B` is best carried forward as:

> **resolve selector, collapse it to the first entry by `B23A` priority, then persist the chosen entry into current-slot `B16E` saved state**

The extra two stream-pointer increments strongly suggest this opcode reserves two inline bytes in the stream even though this body does not otherwise consume them locally.

### Shared failure behavior for `2A/2B`
If selection fails, the handler:

- sets `B242[current] = FF`
- sets `AF24 = 2`
- returns

That is a stronger failure signature than the ordinary `AF24 = 1` gate family.

---

## 7. Global opcode `2C` is an exact no-op alias
Handler:

```text
C1:98C4  60
```

### Strongest safe interpretation
Global opcode `2C` is just:

> **RTS no-op alias**

---

## 8. Global opcode `2D` is the old group-1 random 4-way stream-advance command, now promoted to master-table global status
Handler entry:

```text
C1:98C5
```

This body was already the strongest semantic win from pass 32.

### Carry-forward result
Global opcode `2D` is best treated as:

> **random 4-way stream-advance / branch-style command**

Its core structure remains:

- request random value with `A = #$64`
- split the result into four ranges
- consult `FD:BA4A`
- advance the current command-stream pointer by command-sized boundaries
- resume execution from the new stream location

### Why this matters now
This is no longer merely “group-1 opcode `04`”.
It is now pinned in the real master table as:

- global `2D`

That is a table-ownership correction worth carrying forward in all later docs.

---

## 9. Global opcodes `2E` and `2F` are exact no-op aliases
Handlers:

```text
C1:9960  60
C1:9961  60
```

### Strongest safe interpretation
- `2E` = `RTS` no-op alias
- `2F` = `RTS` no-op alias

These are distinct table entries but not distinct behaviors.

---

## 10. Working interpretation of this whole cluster
After pass 67 the first global slice after `22` is no longer a mystery blob.

It is now:

- `23..28` = six-opcode alias run onto global `18`
- `29` = persist selector head + inline param into `5E15/5E0D`
- `2A` = ordered-first-choice persist into `5E15/5E0D`
- `2B` = ordered-first-choice persist into `B16E`
- `2C` = no-op
- `2D` = random 4-way stream-advance
- `2E/2F` = no-op

That is a real cleanup because it exposes the intended bridge:

- early global/master opcodes here are preparing **saved seed state**
- later seeded group-2 families consume that saved state

---

## 11. Best next seam after this pass
The next clean continuation is:

- `30..3F` to finish promoting the rest of the old group-1 slice into master-global labels
- then `40..52` to do the same promotion / cleanup for the old group-2 slice
- with special attention on whether the `9967` / `9981` bodies can now be renamed more strongly in global terms

---

## Confidence / guardrails
### Strong enough to keep
- exact alias mapping for `23..28`
- `29` as selector-head persistence into `5E15/5E0D`
- `2A/2B` as ordered-first-choice persistence commands split by `AEE3`
- `2C`, `2E`, `2F` as literal `RTS` aliases
- `2D` as the already-solved random 4-way stream-advance command promoted to global status

### Still intentionally cautious
- exact gameplay-facing nouns for `5E0D`, `5E15`, and `B16E`
- whether the two skipped bytes in `2B` are operand placeholders, reserved fields, or something higher-level
- whether `B23A` should be named as initiative/order/rank without stronger caller-side proof
