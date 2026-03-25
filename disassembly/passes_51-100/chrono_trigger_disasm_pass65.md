# Chrono Trigger Disassembly — Pass 65

## Scope of this pass
This pass continued straight from the pass-64 seam, but it also did one supporting job first:

1. continue the early master-opcode band at:
   - `0C -> 925D`
   - `0D -> 92A3`
   - `0E -> 9314`
   - `0F -> 938D`
   - `10 -> 93E6`
   - `11 -> 942A`
   - `12 -> 9474`
2. re-open the relation-query engine entries they depend on, because `0C/0D/0E/0F/10` were still carrying older pass-30/31 assumptions
3. separate the relation-query wrappers from the **next direct current-slot record gate family** at `11/12`

The highest-value result of the pass is this cleanup:

> `0C/0D/0E/0F/10` still belong to the relation-query wrapper family.
>
> `11/12` do **not**.
>
> They are direct gates over a current-slot quad record rooted at `B19E + 4*B252`.

That means the old “continuous relation-query block through `12`” framing is now too broad.

---

## Method
1. Dumped the raw ROM bytes for `925D..94D1` directly from the live ROM using the toolkit xref cache PC offsets.
2. Re-decoded each opcode body instruction-by-instruction.
3. Re-opened the supporting relation-query mode entries at:
   - `2B37` (mode `04`)
   - `2BBC` (mode `05`)
   - `2BDA` (mode `06`)
   - `2CA7` / `2CBA` / `2CCD` / `2CE0` (modes `09..0C`)
4. Promoted only what the wrapper mechanics prove directly.
5. Kept one explicit caution on `0D/0E`: both bodies still have a real unresolved post-`AE21` dependency on the residual value left in `9872` by the final loop iteration.

---

## 1. Supporting relation-query results needed for this band

### Mode `04` (`C1:2B37`) is a fixed squared-distance threshold test that leaves `9872 = 00` on success and `FF` on failure
The entry at `2B37`:
- seeds `9893/9894` to a fixed threshold package (`00/04`)
- computes the projected squared-distance between subject slot `986F` and arg slot `9870`
- writes `9872 = 00` when the metric is within threshold
- writes `9872 = FF` when the metric is outside threshold

So for wrapper purposes, mode `04` is a true zero/nonzero predicate.

This tightens pass 29, which was right about the squared-distance core but too loose about the exact shape of `9872`.

### Mode `05` (`C1:2BBC`) is an absolute Y-delta `< 0x20` test
This entry:
- loads subject slot `986F`
- loads arg slot `9870`
- computes `abs(subject_y - arg_y)` from `1D23`
- leaves `9872 = 00` when the absolute delta is below `0x20`
- leaves `9872 = FF` when the absolute delta is at or above `0x20`

So the strong carry-forward is:

> mode `05` = **same vertical band / close-Y test** using the live object Y byte stream at `1D23`

### Mode `06` (`C1:2BDA`) is a vertical ordering test
This entry compares:
- `subject_y = 1D23[986F]`
- `arg_y     = 1D23[9870]`

and leaves:
- `9872 = 00` when `subject_y < arg_y`
- `9872 = FF` when `subject_y >= arg_y`

### Modes `09..0C` are coarse row/column band predicates over the current slot
These turned out to be much simpler than the older pass-30 wrapper description implied.

- `2CA7` (mode `09`) uses `1D23[subject] >> 4` and leaves `9872 = FF` when `< 0x08`
- `2CBA` (mode `0A`) uses `1D23[subject] >> 4` and leaves `9872 = FF` when `>= 0x08`
- `2CCD` (mode `0B`) uses `1D0C[subject] >> 4` and leaves `9872 = FF` when `< 0x0B`
- `2CE0` (mode `0C`) uses `1D0C[subject] >> 4` and leaves `9872 = FF` when `>= 0x05`

Since opcode `10` succeeds only when `9872 == 0`, its effective success regions are:
- mode `09` -> `subject_y_high_nibble >= 0x08`
- mode `0A` -> `subject_y_high_nibble < 0x08`
- mode `0B` -> `subject_x_high_nibble >= 0x0B`
- mode `0C` -> `subject_x_high_nibble < 0x05`

---

## 2. Global opcode `0C` is a relation-query mode-04 gate on current subject vs selection head, with operand-controlled polarity
Handler bytes:

```text
C1:925D  20 14 AC
C1:9260  AD CB AE F0 38
C1:9265  AD 52 B2 18 69 03 8D 6F 98
C1:926E  A9 04 8D 6E 98
C1:9273  AD CC AE 8D 70 98
C1:9279  A9 05 20 03 00
C1:927E  AE D2 B1 BF 01 00 CC
C1:9285  F0 07 AD 72 98 F0 11 80 05
C1:928E  AD 72 98 D0 0A
C1:9293  A9 01 8D CB AE
C1:9298  20 3E 8C
C1:929B  80 05
C1:929D  A9 01 8D 24 AF
C1:92A2  60
```

### What it does
1. calls `AC14`
2. empty selection -> failure
3. seeds relation-query workspace:
   - `986F = B252 + 3`  (current subject slot)
   - `986E = 04`        (relation-query mode 04)
   - `9870 = AECC[0]`   (selection head / first selected entry)
4. calls service `5` through `JSR $0003`, which lands in the relation-query dispatcher
5. reads operand `+1` from the CC stream as a polarity byte
6. final gate:
   - operand `+1 == 0`  -> success only when `9872 == 0`
   - operand `+1 != 0`  -> success only when `9872 != 0`
7. on success:
   - `AECB = 1`
   - `JSR $8C3E`
8. on failure:
   - `AF24 = 1`

### Strongest safe interpretation
Global opcode `0C` is best carried forward as:

> **gate tail replay on the relation-query mode-04 result between the current subject slot (`B252 + 3`) and `AECC[0]`, with operand-controlled zero/nonzero polarity**

### Important correction to older carry-forward
The old pass-30 family note that treated this only as a vague “run relation query mode 04 with AECC” is now too weak.
The replay-gate contract is clear here.

---

## 3. Global opcode `0D` marks non-subject selected entries whose mode-05 result is zero, then reduces them
Handler bytes:

```text
C1:92A3  20 14 AC
C1:92A6  AD CB AE F0 68
C1:92AB  AD 52 B2 18 69 03 8D 6F 98 85 0E
C1:92B6  64 0F
C1:92B8  A9 05 8D 6E 98
C1:92BD  7B AA 86 0A 86 0C
C1:92C3  A6 0A BD CC AE C5 0E F0 19
C1:92CC  8D 70 98
C1:92CF  A9 05 20 03 00
C1:92D4  AD 72 98 D0 0C
C1:92D9  A6 0A BD CC AE 09 80 9D CC AE
C1:92E2  E6 0C
C1:92E4  E6 0A A5 0A CD CB AE 90 D5
C1:92EE  A5 0C 8D CB AE
C1:92F3  20 21 AE
C1:92F6  AD 24 AF D0 18
C1:92FB  AE D2 B1 BF 01 00 CC
C1:9302  F0 07 AD 72 98 F0 0A 80 05
C1:930B  AD 72 98 D0 03
C1:9310  20 3E 8C
C1:9313  60
```

### What it does
1. calls `AC14`
2. empty selection -> return/failure path
3. seeds the current subject slot:
   - `986F = B252 + 3`
   - cached in `$0E`
4. sets `986E = 05`
5. loops the selected entries in `AECC`
6. skips the entry when it is the same as the subject slot
7. otherwise:
   - writes that selected entry to `9870`
   - runs relation-query mode `05`
   - when `9872 == 0`, it marks that entry with bit 7 inside `AECC`
   - increments marked-count `$0C`
8. after the scan:
   - `AECB = marked_count`
   - `JSR $AE21`
9. if `AF24 == 0`, it performs one more operand-`+1` / `9872` gate before `8C3E`

### What mode `05` means here
From the supporting decode of `2BBC`, the candidates that get marked are exactly the non-subject selected entries whose absolute Y delta from the current subject slot is **below `0x20`**.

So the strong part is:

> opcode `0D` builds a marked candidate subset of non-subject selected entries in the same close-Y / same-vertical-band region as the current subject slot

### What is still unresolved
There is still one real ambiguity after the `AE21` reduction:
- the body re-uses operand `+1` and the residual value left in `9872`
- but it does **not** re-run the relation query on the final reduced entry

So the wrapper is mechanically clear, but the exact intended higher-level contract of that final post-`AE21` gate is still not fully pinned.

### Strongest safe interpretation
Global opcode `0D` is best carried forward as:

> **mark non-subject selected entries whose relation-query mode-05 result against the current subject slot is zero, reduce them through `AE21`, then conditionally replay through a residual `9872` / operand-`+1` gate**

This is strong structural, but the final human-facing noun should stay provisional.

---

## 4. Global opcode `0E` is the parameterized sibling of `0D`, using relation mode `06 + operand2`
Handler bytes:

```text
C1:9314  20 14 AC
C1:9317  AD CB AE F0 70
C1:931C  AE D2 B1 BF 02 00 CC 18 69 06 8D 6E 98
C1:9328  AD 52 B2 18 69 03 8D 6F 98 85 0E
C1:9334  64 0F 7B AA 86 0A 86 0C
C1:933C  A6 0A BD CC AE C5 0E F0 19
C1:9345  8D 70 98
C1:9348  A9 05 20 03 00
C1:934D  AD 72 98 D0 0C
C1:9352  A6 0A BD CC AE 09 80 9D CC AE
C1:935B  E6 0C
C1:935D  E6 0A A5 0A CD CB AE 90 D5
C1:9367  A5 0C 8D CB AE
C1:936C  20 21 AE
C1:936F  AD 24 AF D0 18
C1:9374  AE D2 B1 BF 01 00 CC
C1:937B  F0 07 AD 72 98 F0 0A 80 05
C1:9384  AD 72 98 D0 03
C1:9389  20 3E 8C
C1:938C  60
```

### What it does
This is the same skeleton as `0D`, except the relation-query mode is not fixed.

1. calls `AC14`
2. empty selection -> failure path
3. loads operand `+2` from the CC stream
4. writes:

> `986E = operand2 + 0x06`

5. sets `986F = B252 + 3` as the current subject slot
6. loops non-subject selected entries
7. runs the chosen relation-query mode against each candidate in `9870`
8. marks entries whose query leaves `9872 == 0`
9. reduces the marked subset through `AE21`
10. then hits the same unresolved final operand-`+1` / residual-`9872` replay gate as `0D`

### What this corrects
Older carry-forward phrasing from passes 30/31 treated `0E` too much like a fixed “mode 06 wrapper.”
That is not the direct code shape.

The real code is:

> **parameterized relation mode `06 + operand2`**

### Strongest safe interpretation
Global opcode `0E` is best carried forward as:

> **mark non-subject selected entries whose parameterized relation-query mode `(0x06 + operand2)` result against the current subject slot is zero, reduce them through `AE21`, then conditionally replay through a residual `9872` / operand-`+1` gate**

This should remain provisional structural for now.

---

## 5. Global opcode `0F` is a direct mode-08 relation-query gate on current subject vs selection head
Handler bytes:

```text
C1:938D  20 14 AC
C1:9390  AD CB AE F0 4B
C1:9395  AD 52 B2 18 69 03 8D 6F 98
C1:939E  AD CC AE 8D 70 98
C1:93A3  A9 08 8D 6E 98
C1:93A8  A9 01 85 0E
C1:93AC  AE D2 B1 BF 02 00 CC 0A 0A 05 0E 8D 71 98
C1:93B7  A9 05 8D 72 98
C1:93BC  20 03 00
C1:93BF  AE D2 B1 BF 01 00 CC
C1:93C6  F0 0A AD 72 98 F0 0F 20 3E 8C 80 0F
C1:93D5  AD 72 98 D0 05 20 3E 8C 80 05
C1:93DF  A9 01 8D 24 AF
C1:93E4  60
```

### What it does
1. calls `AC14`
2. empty selection -> failure
3. seeds:
   - `986F = B252 + 3`
   - `9870 = AECC[0]`
   - `986E = 08`
4. computes a packed arg byte for `9871` from operand `+2`:

> `9871 = (operand2 << 2) | 0x01`

5. writes `9872 = 05` **before** calling the relation-query service
6. calls service `5`
7. reads operand `+1` as a polarity byte
8. final gate:
   - operand `+1 == 0`  -> success only when `9872 == 0`
   - operand `+1 != 0`  -> success only when `9872 != 0`

### Important supporting correction
The pre-write:

```text
A9 05
8D 72 98
```

is a dead setup write for normal relation-query flow, because `C1:2986` clears `9872` before dispatching on `986E`.

So the live inputs here are the subject slot, selection head, and the packed `9871` byte — not a pre-seeded `9872` threshold.

### Strongest safe interpretation
Global opcode `0F` is best carried forward as:

> **gate tail replay on the relation-query mode-08 result between the current subject slot (`B252 + 3`) and `AECC[0]`, using packed operand-`+2` bits in `9871` and operand-`+1` as the final zero/nonzero polarity selector**

The wrapper contract is strong even though the final human-facing gameplay noun for mode `08` is still open.

---

## 6. Global opcode `10` is a preset picker for relation modes `09..0C`, which collapse to coarse row/column band gates
Handler bytes:

```text
C1:93E6  AE D2 B1
C1:93E9  BF 03 00 CC F0 0E
C1:93F0  BF 02 00 CC F0 04 A9 0B 80 10
C1:93F9  A9 0C 80 0C
C1:93FD  BF 02 00 CC F0 04 A9 0A 80 02
C1:9407  A9 09
C1:9409  8D 6E 98
C1:940C  AD 52 B2 18 69 03 8D 6F 98
C1:9417  A9 05 20 03 00
C1:941C  AD 72 98 D0 05 20 3E 8C 80 05
C1:9426  A9 01 8D 24 AF
C1:942B  60
```

### What it does
This body does not call `AC14` at all.
It is a pure current-subject relation-query gate.

The operand mapping is:
- if operand `+3 == 0` and operand `+2 == 0` -> mode `09`
- if operand `+3 == 0` and operand `+2 != 0` -> mode `0A`
- if operand `+3 != 0` and operand `+2 != 0` -> mode `0B`
- if operand `+3 != 0` and operand `+2 == 0` -> mode `0C`

Then it sets:
- `986F = B252 + 3`
- `986E = chosen_mode`
- calls relation-query service `5`
- succeeds only when `9872 == 0`

### Effective success tests
Because the supporting mode decodes are now stronger, the effective replay gates are:
- mode `09` -> current subject `Y>>4 >= 0x08`
- mode `0A` -> current subject `Y>>4 < 0x08`
- mode `0B` -> current subject `X>>4 >= 0x0B`
- mode `0C` -> current subject `X>>4 < 0x05`

### Strongest safe interpretation
Global opcode `10` is best carried forward as:

> **gate tail replay on one of four preset coarse row/column band tests over the current subject slot, selected by operands `+2/+3` through relation-query modes `09..0C`**

This is now strong structural, and materially sharper than the older “selects between modes 09 and 0A / 0B and 0C” wording.

---

## 7. Global opcode `11` is a direct current-slot quad-record upper-nibble gate over `B19E + 4*B252`
Handler bytes:

```text
C1:942A  7B
C1:942B  AE D2 B1 BF 03 00 CC 85 02
C1:9433  BF 01 00 CC C9 00 D0 04 A9 40 80 06
C1:943F  C9 01 D0 2A A9 50 85 00
C1:9447  AD 52 B2 0A 0A AA
C1:944D  A5 02 D0 0E
C1:9451  BD 9E B1 29 F0 C5 00 D0 13
C1:945A  20 3E 8C 80 13
C1:945F  BD 9E B1 29 F0 C5 00 F0 05 20 3E 8C 80 05
C1:946D  A9 01 8D 24 AF
C1:9472  60
```

### What it does
1. reads operand `+3` into `$02`
2. reads operand `+1`
   - `0` -> target class byte `0x40`
   - `1` -> target class byte `0x50`
   - anything else -> failure path
3. computes:

> `X = B252 * 4`

4. reads the current slot record byte at:

> `B19E[X]`

5. masks its high nibble with `AND #$F0`
6. final gate:
   - operand `+3 == 0` -> success only when high nibble equals target class (`0x40` or `0x50`)
   - operand `+3 != 0` -> success only when high nibble does **not** equal target class

### Strongest safe interpretation
Global opcode `11` is best carried forward as:

> **gate tail replay on whether the current slot quad-record byte `B19E + 4*B252` has upper nibble `0x40` or `0x50`, with operand `+3` selecting equality vs inequality**

### Important structural correction
This is not part of the relation-query wrapper family.
It is the start of a new direct current-slot record gate band.

---

## 8. Global opcode `12` is the paired current-slot quad-record gate over `B19E/B19F + 4*B252`
Handler bytes:

```text
C1:9474  7B
C1:9475  AE D2 B1 BF 03 00 CC 85 04
C1:947D  BF 02 00 CC 85 02
C1:9484  BF 01 00 CC C9 00 D0 04 A9 40 80 06
C1:9490  C9 01 D0 38 A9 50 85 00
C1:9498  AD 52 B2 0A 0A AA
C1:949D  A5 04 D0 15
C1:94A1  BD 9E B1 29 F0 C5 00 D0 21
C1:94AA  BD 9F B1 C5 02 D0 1A
C1:94B1  20 3E 8C 80 1A
C1:94B6  BD 9E B1 29 F0 C5 00 F0 0C
C1:94BF  BD 9F B1 C5 02 F0 05 20 3E 8C 80 05
C1:94CB  A9 01 8D 24 AF
C1:94D0  60
```

### What it does
1. reads operand `+3` into `$04`
2. reads operand `+2` into `$02`
3. reads operand `+1`
   - `0` -> target high nibble `0x40`
   - `1` -> target high nibble `0x50`
   - anything else -> failure path
4. computes `X = B252 * 4`
5. reads two bytes from the current slot quad record:
   - `B19E[X]` high nibble
   - `B19F[X]` full byte
6. final gate:
   - operand `+3 == 0` -> success only when **both** comparisons match:
     - `B19E[X] & 0xF0 == target_high_nibble`
     - `B19F[X] == operand+2`
   - operand `+3 != 0` -> success only when **both** comparisons differ:
     - `B19E[X] & 0xF0 != target_high_nibble`
     - `B19F[X] != operand+2`

### Strongest safe interpretation
Global opcode `12` is best carried forward as:

> **gate tail replay on a two-byte current-slot quad-record test over `B19E/B19F + 4*B252`, where operand `+1` selects the high-nibble class (`0x40` vs `0x50`), operand `+2` selects the exact second-byte value, and operand `+3` selects both-match vs both-differ mode**

Like `11`, this is a direct record gate, not a relation-query wrapper.

---

## 9. Corrections forced by this pass

### Retire the over-broad “relation-query wrapper block through opcode `12`” phrasing
That was good enough at pass 30/31 time, but it is not the cleanest current model.

The more accurate split is now:
- `0C/0D/0E/0F/10` -> relation-query wrappers / gates
- `11/12` -> direct current-slot quad-record gates

### Retire the fixed-mode phrasing for opcode `0E`
The direct code shape is parameterized:

> `986E = operand2 + 0x06`

So the strongest honest wording has to preserve that.

### Tighten opcode `10`
It is no longer just “selects between relation-query modes `09..0C`.”
Because the underlying mode bodies are now decoded strongly enough, opcode `10` can be carried forward as a real **coarse row/column band gate**.

---

## Provisional labels to carry forward
- `C1:925D..C1:92A2`
  - `ct_global_opcode_0C_gate_tail_replay_on_relation_mode04_current_subject_vs_selection_head`
- `C1:92A3..C1:9313`
  - `ct_global_opcode_0D_mark_non_subject_selected_entries_by_relation_mode05_zero_then_reduce`
- `C1:9314..C1:938C`
  - `ct_global_opcode_0E_mark_non_subject_selected_entries_by_parameterized_relation_mode_zero_then_reduce`
- `C1:938D..C1:93E5`
  - `ct_global_opcode_0F_gate_tail_replay_on_relation_mode08_current_subject_vs_selection_head`
- `C1:93E6..C1:9429`
  - `ct_global_opcode_10_gate_tail_replay_on_current_subject_row_column_band_query`
- `C1:942A..C1:9473`
  - `ct_global_opcode_11_gate_tail_replay_on_current_b19e_upper_nibble_class`
- `C1:9474..C1:94D1`
  - `ct_global_opcode_12_gate_tail_replay_on_current_b19e_b19f_pair_mode`

---

## What remains open right next to this seam
The next adjacent unresolved block is now:

- `13 -> 94D2`
- `14 -> 9514`
- `15 -> 959A`
- `16 -> 95D6`
- `17 -> 95DA`
- `18 -> 95FA`
- `19 -> 9652`
- `1A -> 9656`
- `1B -> 96A5`
- `1C -> 96D4`
- `1D -> 9728`
- `1E -> 975C`
- `1F -> 9765`
- `22 -> 97D5`

The cleanest next move is:
1. stay on the now-obvious direct-record band at `13/14/15`
2. then follow the adjacent opcode family through `16..1F`
3. fold `22 -> 97D5` back in, because it sits immediately after the already-solved `20/21` pair and clearly belongs to the same local neighborhood
