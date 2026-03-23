# Chrono Trigger Disassembly — Pass 66

## Scope of this pass
This pass continued directly from the pass-65 seam inside the early master-opcode band and covered:

- `13 -> C1:94D2`
- `14 -> C1:9514`
- `15 -> C1:959A`
- `16 -> C1:95D6`
- `17 -> C1:95DA`
- `18 -> C1:95FA`
- `19 -> C1:9652`
- `1A -> C1:9656`
- `1B -> C1:96A5`
- `1C -> C1:96D4`
- `1D -> C1:9728`
- `1E -> C1:975C`
- `1F -> C1:9765`
- sibling `22 -> C1:97D5`

The biggest cleanup from this pass is:

> `13/14/15` really are the continuation of the **direct current-slot record gate band**.
>
> `16/19` are plain replay aliases.
>
> `17/1A/22` are simple threshold/count gates.
>
> `18/1C/1F` still need caution, but their structural skeletons are much better now.

A second useful result is that a few branches that looked content-heavy are actually much simpler than they first appear:
- opcode `14` has a whole branch where the low-nibble compare chain is effectively dead noise
- opcode `1A` has a dead `LDA $B252` just before `TDC/TAX`
- the later master-table alias run `23..28` all points back to `95FA`, so solving opcode `18` matters again later

---

## 1. Global opcode `13` is a current-`B19E` bit-4 gate with equality/inequality control
Handler bytes:

```text
C1:94D2  7B AE D2 B1 BF 03 00 CC 85 02 BF 01 00 CC 29 01
C1:94E2  0A 0A 0A 0A 85 00 AD 52 B2 0A 0A AA A5 02 D0 0E
C1:94F2  BD 9E B1 29 10 45 00 D0 13 20 3E 8C 80 13 BD 9E
C1:9502  B1 29 10 45 00 F0 05 20 3E 8C 80 05 A9 01 8D 24
C1:9512  AF 60
```

### What it does
1. reads:
   - operand `+1`, masks it to bit `0`, then shifts it to `0x00` or `0x10`
   - operand `+3` as a branch-polarity byte
2. computes the current slot quad-record index:
   - `X = B252 * 4`
3. reads:
   - `B19E[X] & 0x10`
4. XORs that against the derived target bit (`0x00` or `0x10`)
5. success behavior:
   - operand `+3 == 0` -> success when the XOR result is zero
   - operand `+3 != 0` -> success when the XOR result is nonzero
6. success continues through `8C3E`
7. failure writes `AF24 = 1`

### Strongest safe interpretation
Global opcode `13` is best carried forward as:

> **gate tail replay on whether current `B19E[current*4]` bit 4 matches the target bit derived from operand `+1`, with operand `+3` selecting equality vs inequality**

This is a clean sibling to the current-record gates from pass 65.

---

## 2. Global opcode `14` is a two-form current-`B19E` gate, and one branch collapses much harder than it first looks
Handler bytes:

```text
C1:9514  7B AE D2 B1 BF 03 00 CC 85 04 BF 02 00 CC 85 02
C1:9524  BF 01 00 CC 85 00 AD 52 B2 0A 0A AA A5 02 D0 30
C1:9534  A5 04 D0 16 BD 9E B1 89 10 D0 55 29 0F AA BD 0A
C1:9544  AF C5 00 D0 4B 20 3E 8C 80 4B BD 9E B1 29 10 D0
C1:9554  3F 29 0F AA BD 0A AF C5 00 F0 35 20 3E 8C 80 35
C1:9564  BD 9E B1 89 10 D0 29 A5 04 D0 10 29 0F C9 01 F0
C1:9574  1A C9 02 F0 16 C9 05 F0 12 80 15 29 0F C9 01 D0
C1:9584  0A C9 02 D0 06 C9 05 D0 02 80 05 20 3E 8C 80 05
C1:9594  A9 01 8D 24 AF 60
```

### What it does
This handler has two top-level forms selected by operand `+2`.

#### A. operand `+2 == 0`
1. current slot record index:
   - `X = B252 * 4`
2. require current `B19E[X]` bit 4 clear
3. use the low nibble of current `B19E[X]` as an index into:
   - `AF0A[...]`
4. compare that byte against operand `+1`
5. operand `+3 == 0` -> success on equality
6. operand `+3 != 0` -> success on inequality

#### B. operand `+2 != 0`
This branch looks more complex than it really is.

The actual effect is:
1. require current `B19E[X]` bit 4 clear
2. if operand `+3 == 0`, fail
3. if operand `+3 != 0`, succeed

The apparent low-nibble compare chain against `01/02/05` does not change the real top-level truth table in the nonzero-operand-`+3` branch.

### Why this matters
Without writing this down, it is easy to keep over-claiming a fake “subtype family” here.

The strong thing proved is simpler:

- one branch is a real indexed compare through `AF0A[...]`
- the other branch collapses to a much blunter bit4-clear / operand3-nonzero gate

### Strongest safe interpretation
Global opcode `14` is best carried forward as:

> **two-form current-`B19E` gate: either compare `AF0A[B19E_low_nibble]` against operand `+1` under equality/inequality control, or in the alternate mode reduce to a blunt current-bit4-clear plus operand-`+3` nonzero gate**

This is structurally strong, but the final gameplay-facing noun should stay provisional.

---

## 3. Global opcode `15` is a current-`B1A0` mask gate
Handler bytes:

```text
C1:959A  7B AE D2 B1 BF 03 00 CC 85 04 BF 01 00 CC 85 02
C1:95AA  AD 52 B2 0A 0A AA A5 04 D0 0E BD A0 B1 25 02 C5
C1:95BA  02 D0 13 20 3E 8C 80 13 BD A0 B1 25 02 C5 02 F0
C1:95CA  05 20 3E 8C 80 05 A9 01 8D 24 AF 60
```

### What it does
1. reads:
   - operand `+1` as a bitmask
   - operand `+3` as equality/inequality selector
2. computes:
   - `X = B252 * 4`
3. reads:
   - `current_masked = B1A0[X] & operand1`
4. operand `+3 == 0` -> success only when `current_masked == operand1`
5. operand `+3 != 0` -> success only when `current_masked != operand1`
6. success continues through `8C3E`
7. failure writes `AF24 = 1`

### Strongest safe interpretation
Global opcode `15` is best carried forward as:

> **gate tail replay on whether the current `B1A0[current*4]` byte contains all bits from operand `+1`, with operand `+3` selecting full-mask match vs non-match**

---

## 4. Global opcodes `16` and `19` are plain unconditional replay aliases
Handlers:

```text
C1:95D6  20 3E 8C 60
C1:9652  20 3E 8C 60
```

### What this means
These are not distinct semantic bodies.
They are both just:

- `JSR $8C3E`
- `RTS`

So they are opcode-table aliases of the same replay/controller step already solved at opcode `00`.

### Strongest safe interpretation
- `16` = unconditional tail replay step alias
- `19` = unconditional tail replay step alias

---

## 5. Global opcode `17` is a simple RNG percentage gate
Handler bytes:

```text
C1:95DA  7B AE D2 B1 BF 01 00 CC 85 00 7B AA A9 64 20 22
C1:95EA  AF C5 00 B0 05 20 3E 8C 80 05 A9 01 8D 24 AF 60
```

### What it does
1. reads operand `+1` as a threshold byte
2. calls the already-known RNG helper:
   - `JSR $AF22`
   - with `A = 0x64`
3. compares the returned value against operand `+1`
4. success only when:

> RNG result `< operand1`

5. failure writes `AF24 = 1`

### Strongest safe interpretation
Global opcode `17` is best carried forward as:

> **gate tail replay on RNG percent-like value being below the immediate threshold**

The exact RNG range wording can stay slightly cautious, but structurally this is a probability gate.

---

## 6. Global opcode `18` is an indirect-table selected-entry compare reducer, but its base-pointer setup still needs caution
Handler bytes:

```text
C1:95FA  AE D2 B1 E8 8E D2 B1 BF 00 00 CC 85 08 20 14 AC
C1:960A  AD CB AE F0 3D AE D2 B1 BF 01 00 CC 85 0A 7B AA
C1:961A  86 0E BD CC AE C2 20 0A AA BF 0B A8 FD A8 7B E2
C1:962A  20 B1 0A C5 08 F0 0B E6 0E A5 0E CD CB AE 90 E2
C1:963A  80 10 20 21 AE AD 24 AF D0 08 20 FD AE 20 3E 8C
C1:964A  80 05 A9 01 8D 24 AF 60
```

### What it does
1. advances the CC stream pointer by one byte
2. reads operand `+1` into `$08`
3. calls `AC14`
4. empty selection -> failure
5. reads operand `+2` into `$0A`
6. scans the selected entries in `AECC`
7. for each selected entry:
   - resolves its `FD:A80B` record-rooted value
   - uses that value as the `Y` component of an indirect indexed byte read:
     - `LDA ($0A),Y`
   - compares the resulting byte against operand `+1`
8. on the first equality hit:
   - `JSR $AE21`
   - if `AF24 == 0`, `AEFD` then `8C3E`
9. if the scan completes with no equality hit, failure writes `AF24 = 1`

### What is still unresolved
Unlike opcodes `09/0B`, this handler does **not** explicitly zero the high byte beside `$0A` before using `($0A),Y`.

So the mechanics are clear, but the final phrasing for the base table source should stay cautious until the pointer setup is re-checked harder.

### Strongest safe interpretation
Global opcode `18` is best carried forward as:

> **scan selected entries for an indirect-table byte, indexed by their `FD:A80B` record-rooted value, equal to the immediate byte, then reduce through `AE21`**

This is structurally useful already, and it matters again later because master opcodes `23..28` all alias back to this same handler body.

---

## 7. Global opcode `1A` searches the live-tail occupant submap for an immediate occupant byte, with an alternate “ignore current slot” mode
Handler bytes:

```text
C1:9656  AE D2 B1 E8 8E D2 B1 BF 00 00 CC 85 08 BF 01 00
C1:9666  CC 85 0A BF 02 00 CC 85 0C AD 52 B2 7B AA BD 02
C1:9676  AF C9 FF F0 04 C5 08 D0 0D E8 8A CD C6 AE D0 EE
C1:9686  A5 0A F0 10 80 13 A5 0A F0 06 8A CD 52 B2 F0 E9
C1:9696  A5 0C F0 05 20 3E 8C 80 05 A9 01 8D 24 AF 60
```

### What it does
1. advances the CC stream pointer by one byte
2. reads:
   - operand `+1` -> target occupant byte
   - operand `+2` -> mode byte A
   - operand `+3` -> mode byte B
3. scans:
   - `AF02[0 .. AEC6-1]`
4. ignores `FF` entries
5. on a matching occupant byte:
   - if operand `+2 != 0` and the hit is the current slot (`X == B252`), it skips that hit and keeps scanning
   - otherwise it exits to a final success/failure gate controlled by operand `+3`
6. on no match at all:
   - operand `+2 == 0` -> success
   - operand `+2 != 0` -> failure

### Important cleanup
The leading `LDA $B252` before `TDC/TAX` is dead in this body.
So the real scan starts from `X = 0`, not from the current slot.

### Strongest safe interpretation
Global opcode `1A` is best carried forward as:

> **gate tail replay on a live-tail occupant-byte search through `AF02`, with an alternate mode that skips current-slot hits and requires another matching live-tail entry**

The exact human-facing noun for the operand-mode pair should stay a little cautious, but the search mechanics are strong.

---

## 8. Global opcode `1B` is a visible-head live-count gate
Handler bytes:

```text
C1:96A5  AE D2 B1 E8 8E D2 B1 BF 00 00 CC 1A 85 08 7B AA
C1:96B5  A8 BD FF AE C9 FF F0 01 C8 E8 E0 03 00 90 F2 98
C1:96C5  C5 08 B0 05 20 3E 8C 80 05 A9 01 8D 24 AF 60
```

### What it does
1. advances the CC stream pointer by one byte
2. reads operand `+1`, increments it, stores to `$08`
3. counts non-`FF` entries in:
   - `AEFF[0..2]`
4. success only when:

> visible-head live count `< (operand1 + 1)`

which is equivalent to:

> visible-head live count `<= operand1`

5. failure writes `AF24 = 1`

### Strongest safe interpretation
Global opcode `1B` is best carried forward as:

> **gate tail replay on visible-head live occupant count at or below the immediate threshold**

---

## 9. Global opcode `1C` optionally replays based on selected-byte membership in the canonical head map, then always aborts
Handler bytes:

```text
C1:96D4  20 14 AC AD CB AE F0 46 7B AE D2 B1 E8 8E D2 B1
C1:96E4  BF 00 00 CC 85 08 BF 01 00 CC 85 0A 7B AA AD CC
C1:96F4  AE DD 0A AF F0 08 E8 E0 03 00 90 F5 80 17 A5 0A
C1:9704  C9 01 F0 1A A5 08 C9 01 F0 11 BD FF AE C9 FF F0
C1:9714  02 80 08 80 09 A5 0A C9 00 F0 03 20 3E 8C A9 01
C1:9724  8D 24 AF 60
```

### What it does
1. calls `AC14`
2. empty selection -> failure path
3. advances the stream pointer by one byte
4. reads operands `+1/+2`
5. searches the canonical head map:
   - `AF0A[0..2]`
   - for a byte equal to `AECC[0]`
6. if no match is found:
   - success only when operand `+2 != 0`
7. if a match is found:
   - operand `+2 == 1` -> fail
   - otherwise:
     - operand `+1 == 1` -> success
     - else require corresponding live head entry `AEFF[x] != FF`
8. on success it runs `8C3E`
9. after that, and also on failure, it writes:
   - `AF24 = 1`

### Why this should stay provisional
This handler clearly is **not** a normal replay-gate wrapper, because it always exits with `AF24 = 1` even after the replay call.

The structural mechanics are real, but the final gameplay-facing contract needs more caller/context work.

### Strongest safe interpretation
Global opcode `1C` is best carried forward as:

> **conditionally replay based on whether the selected byte is represented in the canonical visible-head map, with an optional live-head presence requirement, then force abort**

---

## 10. Global opcode `1D` is a selected tail-live presence/absence gate
Handler bytes:

```text
C1:9728  20 14 AC AE D2 B1 E8 E8 8E D2 B1 BF 00 00 CC 85
C1:9738  0A 7B AA 7B AD CC AE AA BD 02 AF C9 FF D0 06 A5
C1:9748  0A D0 06 80 09 A5 0A D0 05 20 3E 8C 80 05 A9 01
C1:9758  8D 24 AF 60
```

### What it does
1. calls `AC14`
2. advances the stream pointer by two bytes
3. reads operand `+2` into `$0A`
4. loads:
   - `X = AECC[0]`
5. reads:
   - `AF02[X]`
6. success behavior:
   - if `AF02[X] == FF`, success only when operand `+2 != 0`
   - if `AF02[X] != FF`, success only when operand `+2 == 0`
7. success continues through `8C3E`
8. failure writes `AF24 = 1`

### Strongest safe interpretation
Global opcode `1D` is best carried forward as:

> **gate tail replay on presence vs absence in the tail live-occupant submap for the selected entry index**

This is the clean selected-entry sibling to opcode `04`'s broader live-tail presence gate.

---

## 11. Global opcode `1E` is an unconditional replay-then-abort step
Handler bytes:

```text
C1:975C  20 3E 8C A9 01 8D 24 AF 60
```

### What it does
1. runs `8C3E`
2. then unconditionally writes:
   - `AF24 = 1`
3. returns

### Strongest safe interpretation
Global opcode `1E` is best carried forward as:

> **unconditional tail replay step that always forces abort/short-circuit afterward**

This is a real structural sibling of the pure replay aliases, but with the extra forced-failure flag.

---

## 12. Global opcode `1F` is the real master-table home of the old mode-`0E` relation-query wrapper
Handler bytes:

```text
C1:9765  20 14 AC AD CB AE F0 38 AD 52 B2 18 69 03 8D 6F
C1:9775  98 A9 0E 8D 6E 98 AD CC AE 8D 70 98 A9 05 20 03
C1:9785  00 AE D2 B1 BF 01 00 CC F0 07 AD 72 98 F0 11 80
C1:9795  05 AD 72 98 D0 0A A9 01 8D CB AE 20 3E 8C 80 05
C1:97A5  A9 01 8D 24 AF 60
```

### What it does
1. calls `AC14`
2. empty selection -> failure
3. seeds the relation-query service with:
   - `986F = B252 + 3`   (current subject slot)
   - `986E = 0E`
   - `9870 = AECC[0]`
4. calls local service `5` through `JSR $0003`
5. operand `+1` selects the final zero/nonzero gate over `9872`
6. on success:
   - `AECB = 1`
   - `JSR $8C3E`
7. on failure:
   - `AF24 = 1`

### What this corrects
Passes 30–31 already knew this wrapper family existed, but after the master-table unification it is now clear that:

> `1F` is the real master-opcode slot for the old mode-`0E` relation-query wrapper

### What is still open
The wrapper contract is now clear, but the final human-facing semantics of relation-query mode `0E` are still not fully frozen.

The underlying mode body at `2CF3` looks much more like a value-producing projected-distance-delta path than a trivial compare, so future work should decode that body directly instead of pretending the noun is already done.

### Strongest safe interpretation
Global opcode `1F` is best carried forward as:

> **gate tail replay on the mode-`0E` relation-query result between the current subject slot and `AECC[0]`, with operand-controlled zero/nonzero polarity**

---

## 13. Global opcode `22` is a selected-entry `B158` threshold gate
Handler bytes:

```text
C1:97D5  20 14 AC AE D2 B1 BF 01 00 CC 85 08 BF 02 00 CC
C1:97E5  85 09 D0 0E 7B AD CC AE AA BD 58 B1 C5 08 90 0E
C1:97F5  80 11 7B AD CC AE AA BD 58 B1 C5 08 90 05 20 3E
C1:9805  8C 80 05 A9 01 8D 24 AF 64 09 60
```

### What it does
1. calls `AC14`
2. reads:
   - operand `+1` -> threshold byte
   - operand `+2` -> compare-mode byte
3. uses:
   - `X = AECC[0]`
4. reads:
   - `B158[X]`
5. success behavior:
   - operand `+2 == 0` -> success when `B158[X] < operand1`
   - operand `+2 != 0` -> success when `B158[X] >= operand1`
6. success continues through `8C3E`
7. failure writes `AF24 = 1`
8. final scratch cleanup:
   - `STZ $09`

### Strongest safe interpretation
Global opcode `22` is best carried forward as:

> **gate tail replay on the selected entry’s `B158` value being below or at/above an immediate threshold, depending on operand `+2`**

Given passes 50–51, this likely touches the readiness/active-time seed family, but the opcode label should stay anchored to the byte-level proof for now.

---

## 14. What this pass changes about the local seam
The early master-opcode band is now much less muddy.

### Newly solid
- `13/15` = clean current-record gates
- `16/19` = unconditional replay aliases
- `17` = RNG gate
- `1B` = visible-head live-count gate
- `1D` = selected tail-live presence/absence gate
- `1E` = replay-then-abort step
- `22` = selected-entry `B158` threshold gate

### Strong but still cautious
- `14` = two-form current-`B19E` gate with one collapsed branch
- `18` = indirect-table selected-entry compare reducer
- `1C` = canonical-head/live-head conditional replay then abort
- `1F` = mode-`0E` relation-query wrapper whose underlying mode semantics still need direct decoding

---

## 15. Best next seam
The cleanest continuation after this pass is:

1. the master-table alias cluster:
   - `23..28`
   - all of which reuse `95FA`
2. then:
   - `29 -> 9810`
   - `2A/2B -> 983A`
   - `2C -> 98C4`
   - `2D -> 98C5`
   - `2E -> 9960`
   - `2F -> 9961`
3. and separately:
   - decode relation-query mode `0E` at `2CF3` hard enough to upgrade opcode `1F`
   - re-check whether opcode `18`'s indirect base should freeze as a true zero-page base offset or a caller-fed pointer pair
