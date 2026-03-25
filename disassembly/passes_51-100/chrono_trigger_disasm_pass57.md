# Chrono Trigger Disassembly Pass 57

## Scope of this pass
This pass continued from pass 56's open seam, but the cleaner structural win did **not** come from the readiness arithmetic side first.

While tracing the live/canonical tail-slot consumers, the stronger new seam turned out to be the **withheld-tail materialization path** around:

- `C1:AB03..AB49`
- `C1:AED3..AEFB`
- `C1:8C0A..8C37`
- `C1:9012..9043`

The goals for this pass were:

1. determine whether `AF15.bit7` is only a passive “not live” flag, or whether it participates in an active deferred-selection/materialization flow
2. determine whether there is a direct routine that converts a canonical-but-not-live tail entry into a live tail entry
3. determine whether the live/unwithheld tail count is consumed explicitly by later gate logic
4. decide whether pass 56's `AF15.bit7` wording can now be strengthened again

The main result is:

> `AF15.bit7` is no longer best read as only “canonical but not live.”
>
> It now participates in a real **deferred tail-entry selection + materialization** flow:
>
> - flagged tail entries are enumerated into a candidate list
> - if multiple candidates exist, the flow randomly reduces them to **one** selected candidate
> - a later routine materializes that canonical entry back into the live tail map by writing `AF02[x] = AF0D[x]` and clearing bit 7
>
> So bit 7 is now best treated as a **deferred / withheld-from-live tail materialization flag**.

That is materially stronger than the pass-56 wording.

---

## Method
1. Re-scan all bank-`C1` references to `AF15`
2. Re-read the tail-map producer from pass 56:
   - `FD:B2A3..B2DD`
3. Decode the consumer clusters that explicitly test bit `7`:
   - `C1:8C0A..8C37`
   - `C1:9012..9043`
   - `C1:AB03..AB49`
   - `C1:AED3..AEFB`
4. Cross-check whether these routines are working over:
   - `AF02..AF09` = live tail occupant submap
   - `AF0D..AF14` = canonical tail occupant submap
5. Upgrade labels only where the bytes prove an active state transition, not just a static gate

---

## 1. `C1:AB03..AB49` builds a candidate list of **withheld tail slots**, and if needed reduces it to **one random choice**
Relevant bytes:

```text
C1:AB03  7B AA A8
C1:AB06  BD 15 AF 89 80 F0 05
C1:AB0D  8A 99 CC AE
C1:AB11  C8
C1:AB12  E8 E0 08 00 90 EE
C1:AB18  C0 00 00 D0 06
C1:AB1E  7B 8D CB AE 80 2A
C1:AB24  98 8D CB AE
C1:AB27  C9 02 90 22
C1:AB2B  7B AA
C1:AB2D  AD CB AE
C1:AB30  20 22 AF
C1:AB33  AA
C1:AB34  BD CC AE
C1:AB37  8D CC AE
C1:AB3A  A2 01 00
C1:AB3D  A9 FF
C1:AB3F  9D CC AE
C1:AB42  E8 E0 0B 00 90 F7
C1:AB48  A9 01 8D CB AE 60
```

### Structural read
This routine starts with `A = 0`, `X = 0`, `Y = 0` and scans all 8 tail entries.

For each `X`:

```text
LDA $AF15,X
AND #$80
BEQ skip
TXA
STA $AECC,Y
INY
```

So this is **not** scanning live occupants directly.
It is scanning the tail entries whose `AF15.bit7` is set.

Then:

- if `Y == 0`, it stores `0` to `AECB` and returns
- otherwise it stores `Y` to `AECB`

That alone already upgrades the role of bit 7: flagged entries are being collected into a dedicated candidate list.

### The important second half
If `AECB >= 2`, the routine does **not** keep the full list intact.
Instead it does:

1. `LDA AECB`
2. `JSR $AF22`
3. uses the returned value as an index into `AECC`
4. copies the chosen entry into `AECC[0]`
5. fills the rest of `AECC[1..]` with `FF`
6. forces `AECB = 1`

Pass 36 already identified `AF22` as an RNG helper.
So this routine is now strong enough to describe as:

> **enumerate withheld tail-slot indices, and if multiple exist, randomly reduce the candidate list to a single chosen slot index**

That is much stronger than pass 56's static “withheld from live” wording.
This is an active deferred-selection path.

---

## 2. `C1:AED3..AEFB` is the direct **materialize withheld canonical tail entry into live map** helper
Relevant bytes:

```text
C1:AED3  7B AA
C1:AED5  8D 24 AF
C1:AED8  A5 0E
C1:AEDA  DD 0D AF D0 05
C1:AEDF  DD 02 AF D0 0D
C1:AEE4  E8 E0 08 00 90 F0
C1:AEEA  A9 01 8D 24 AF 80 0B
C1:AEF1  9D 02 AF
C1:AEF4  BD 15 AF 29 7F
C1:AEF9  9D 15 AF
C1:AEFC  60
```

### Strong structural read
The routine does:

1. clear `AF24`
2. scan tail entries `X = 0..7`
3. compare target occupant ID in `$0E` against `AF0D[x]`
4. if canonical occupant does **not** match, continue
5. if canonical occupant matches but live occupant `AF02[x]` already matches too, continue
6. otherwise:
   - `STA $AF02,X`
   - `LDA $AF15,X`
   - `AND #$7F`
   - `STA $AF15,X`
   - `RTS`
7. if no match is found, set `AF24 = 1`

### What this proves
This is the direct state transition we needed.
A tail entry with:

- canonical occupant present in `AF0D[x]`
- but absent/different in `AF02[x]`

can be restored into the live map by:

- copying the canonical occupant ID into `AF02[x]`
- clearing `AF15.bit7`

That is not just a gate check.
It is an explicit **reveal / materialize** transition.

So pass 56's wording can now be upgraded from:

> canonical present, but not live

into:

> canonical present, withheld from live until materialized by the deferred-tail helper flow

---

## 3. `C1:8C0A..8C37` iterates only **live and unwithheld** tail entries for downstream dispatch
Relevant bytes:

```text
C1:8C09  9C 52 B2
C1:8C0C  7B 8D CF B1
C1:8C10  AD 52 B2 AA 9E 4A B2 9E 63 B2
C1:8C1A  BD 15 AF 89 80 D0 07
C1:8C21  BD 02 AF C9 FF F0 0B
C1:8C28  BD B6 B2 D0 06
C1:8C2D  BD 02 AF 20 D2 AF
C1:8C31  EE 52 B2
C1:8C34  AD 52 B2 C9 08 90 CF
C1:8C3B  60
```

### Strong structural read
For each tail slot `X = 0..7`, the routine first clears a pair of scratch arrays at `B24A[x]` and `B263[x]`, then gates the slot with three tests:

1. `AF15.bit7` must be clear
2. `AF02[x]` must not be `FF`
3. `B2B6[x]` must be zero

Only then does it pass `AF02[x]` to `JSR $AFD2` and increment the local count at `B252`.

### What this proves
This routine is not consuming canonical tail entries indiscriminately.
It only consumes entries that are:

- live in the tail map
- not currently withheld/deferred
- not blocked by the separate `B2B6[x]` per-tail gate

That lines up perfectly with the `AB03` / `AED3` pair:

- `AB03` deals with withheld candidates
- `AED3` materializes a chosen withheld entry
- `8C0A` consumes only the entries that are already live and not withheld

So the bit-7 model is no longer hypothetical. It is now integrated into the live consumer path.

---

## 4. `C1:9012..9043` explicitly counts **live, unwithheld** tail entries and gates downstream flow on that count
Relevant bytes:

```text
C1:9012  AE D2 B1
C1:9015  BF 01 00 CC 85 08
C1:901B  7B AA 86 0A
C1:9020  BD 02 AF C9 FF F0 07
C1:9027  BD 15 AF D0 02
C1:902C  E6 0A
C1:902E  E8 E0 08 00 90 EC
C1:9034  A5 08 C5 0A 90 05
C1:9039  20 3E 8C 80 05
C1:903E  A9 01 8D 24 AF
C1:9043  60
```

### What is directly proved
This routine:

1. loads a descriptor byte from `CC:[B1D2 + 1]` into `$08`
2. scans all 8 tail slots
3. increments `$0A` only when:
   - `AF02[x] != FF`
   - and `AF15[x] == 0`
4. compares `$08` against the resulting count `$0A`
5. if the compare falls through the `BCC` path, it dispatches to `JSR $8C3E`
6. otherwise it sets `AF24 = 1`

### Safe interpretation
The exact human-facing noun for the descriptor byte in `$08` is still open.
But the branch condition itself is no longer vague.
This routine is using the count of **currently live, unwithheld tail entries** as an explicit gate for downstream processing.

The safest carry-forward wording is:

> **descriptor-controlled gate on the number of currently live, unwithheld tail entries**

This is stronger than pass 56 because it proves the bit-7 state is not merely recorded; it is actively counted and compared by later control flow.

---

## 5. This materially upgrades the meaning of `AF15.bit7`
Pass 56 was already strong enough to say:

- canonical tail entry exists
- but it is withheld from the live tail map

Pass 57 adds the missing dynamic proof:

1. flagged entries are enumerated into a dedicated candidate list (`AB03`)
2. multiple flagged entries are reduced to a single random chosen candidate (`AB03 + AF22`)
3. a chosen entry can be reinserted into the live map by occupant ID (`AED3`)
4. ordinary tail consumers ignore flagged entries (`8C0A`)
5. ordinary tail-count gates ignore flagged entries too (`9012`)

So the strongest safe reading now is:

> `AF15.bit7` marks a **deferred tail entry** that remains canonically present but is withheld from ordinary live-tail dispatch and counting until it is explicitly materialized.

That is stronger than “not live” and still more cautious than over-flavored words like “reserve monster,” “queued enemy,” or “hidden combatant.”

---

## 6. What this changes about pass 56's open questions
Pass 56 left open:

1. the exact outward meaning of `AF15.bit7`
2. why some canonical tail entries are withheld from the live map

Pass 57 does **not** completely solve the gameplay-facing reason yet, but it solves the mechanics much harder.

### What is now solved mechanically
- the withheld entries form a special candidate pool
- only one candidate may be selected from that pool in this flow
- ordinary live-tail consumers do not see the withheld entries
- the chosen candidate can later be materialized into the live map

### What remains open
- which higher-level caller contexts feed `$0E` before `AED3`
- what exact gameplay/event condition chooses when the deferred candidate is materialized
- whether the random reduction in `AB03` is always used for the same gameplay-facing phenomenon, or whether several wrapper modes reuse it

---

## 7. Labels safe to strengthen after this pass
### `AF15.bit7`
Best strengthened noun now:

> **deferred / withheld-from-live tail materialization flag**

### `C1:AB03..AB49`
Best new label now:

> **build withheld-tail candidate list and randomly reduce it to one selected slot**

### `C1:AED3..AEFB`
Best new label now:

> **materialize deferred tail entry from canonical occupant map into live tail map**

### `C1:8C0A..8C37`
Best current structural label:

> **iterate live, unwithheld tail entries for downstream dispatch**

### `C1:9012..9043`
Best current structural label:

> **gate downstream tail dispatch on the descriptor-controlled count of live, unwithheld tail entries**

---

## 8. Cautions still in force
Do **not** over-freeze the following yet:

1. `AECC/AECB` globally as “withheld-tail list”
   - this pass proves that `AB03` reuses them that way
   - earlier passes already proved they are more general selection/candidate scratch in other paths
2. the descriptor byte at `CC:[B1D2 + 1]` as specifically “minimum count” or “maximum count”
   - the compare direction is proved
   - the final human-facing noun still wants more wrapper context
3. `AF15.bit7` as a heavily flavored gameplay term
   - the mechanics are now strong
   - the exact narrative/gameplay role still wants caller proof

---

## 9. Suggested next seam
The cleanest next continuation point after this pass is:

1. trace the caller paths that populate `$0E` before `C1:AED3`
2. trace which wrappers invoke `C1:AB03` and whether they always use the same descriptor/mode family
3. return to the earlier readiness seam afterward, now with the stronger proof that the tail-slot state machine itself is split between:
   - live/unwithheld entries
   - deferred/withheld canonical entries
