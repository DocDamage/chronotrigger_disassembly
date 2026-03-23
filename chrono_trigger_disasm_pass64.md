# Chrono Trigger Disassembly — Pass 64

## Scope of this pass
This pass stayed on the same live seam left by pass 63, but it also cracked the helper that all of those early-band handlers depend on:

1. continue the early global-opcode band inside the master `C1:B80D` table
2. decode the next contiguous handlers:
   - `08 -> 90BE`
   - `09 -> 9130`
   - `0A -> 918E`
   - `0B -> 91F9`
3. resolve the real contract of `AE21`
4. correct any pass-63 carry-forward that treated `AE21` as a vague finalize helper instead of a concrete marked-entry reducer

The highest-value result of this pass is not just four more opcode bodies.

It is this architectural correction:

> `AE21` is not a generic “finalize” box.
>
> It is a **selected-entry reduction helper** that collapses `AECC/AECB` down to **one chosen entry**,
> requiring a high-bit mark on the chosen byte and raising `AF24` on failure.
>
> That means the high-bit OR operations in opcodes `01/02/03/08` are not incidental.
> They are how those handlers **mark candidate survivors for `AE21` to choose from**.

That immediately sharpens pass 63 and changes how `09` and `0B` should be read:

- `08` is a real marked-survivor builder
- `0A` is a direct single-entry gate that bypasses `AE21`
- `09` and `0B` do **not** mark entries themselves, so they are scan/gate wrappers into `AE21`, not simple list-compaction bodies

---

## Method
1. Re-opened the next contiguous master-table entries after pass 63:
   - `08 -> 90BE`
   - `09 -> 9130`
   - `0A -> 918E`
   - `0B -> 91F9`
2. Decoded `AE21..AE6F` directly, because it is the choke point for the whole early-band family.
3. Re-read the caller bodies with the now-known `AE21` contract in mind.
4. Kept three distinctions explicit:
   - does the handler mark survivors with bit 7?
   - does it call `AE21`?
   - does it go directly to `8C3E` instead?

---

## 1. `AE21` is a marked-entry reducer that collapses `AECC/AECB` to one chosen entry or fails
Helper bytes:

```text
C1:AE21  AD CB AE F0 46
C1:AE26  C9 01 F0 26
C1:AE2A  7B AA A8
C1:AE2D  BD CC AE 29 0F D9 63 B1 F0 10
C1:AE37  C8 98 C9 0B 90 F0
C1:AE3D  7B A8 E8 8A C9 0B 90 E8
C1:AE45  80 25
C1:AE47  B9 CC AE 89 80 F0 E9
C1:AE4E  80 10
C1:AE50  7B AA
C1:AE52  BD CC AE 89 80 D0 07
C1:AE59  E8 8A CD CB AE D0 F2
C1:AE60  29 7F 8D CC AE
C1:AE65  A9 01 8D CB AE
C1:AE6A  80 03
C1:AE6C  EE 24 AF
C1:AE6F  60
```

### What it does
This helper is no longer vague.

#### empty selection
- if `AECB == 0`
- it increments `AF24`
- then returns

So empty input selection is a hard failure.

#### single-entry path
- if `AECB == 1`, it scans the selected bytes looking for one with bit 7 set
- if it finds one:
  - it clears bit 7
  - writes that byte to `AECC[0]`
  - sets `AECB = 1`
- if no marked entry is found:
  - it increments `AF24`

#### multi-entry path
When `AECB > 1`, it:
1. scans the selected bytes in `AECC`
2. compares their low nibble against the byte stream at `C1:B163 + Y`
3. requires the finally chosen entry byte to have bit 7 set
4. on success:
   - strips bit 7
   - stores the chosen entry in `AECC[0]`
   - sets `AECB = 1`
5. if no acceptable marked entry is found:
   - increments `AF24`

### Strongest safe interpretation
`AE21` is best carried forward as:

> **reduce marked selected entries to one chosen entry or fail**

### Important caution
The exact higher-level rule behind the multi-entry ranking step is still open.
This pass proves the mechanics:
- low-nibble comparison against the `C1:B163` byte stream
- requirement that the chosen byte be bit-7 marked
- collapse to one unmarked entry in `AECC[0]`

That is enough to sharpen the surrounding opcode family even before the final gameplay noun is known.

---

## 2. Global opcode `08` marks record-threshold survivors for `AE21` to reduce
Handler bytes:

```text
C1:90BE  20 14 AC
C1:90C1  AD CB AE F0 64
C1:90C6  AE D2 B1 E8 8E D2 B1 BF 00 00 CC 85 08
C1:90D3  BF 01 00 CC 85 09
C1:90D9  7B AA 86 0A 86 0C
C1:90DF  7B A6 0A BD CC AE
C1:90E5  C2 20 0A AA
C1:90E9  BF 0B A8 FD AA
C1:90EE  BD 03 00 C5 08 F0 02 B0 0E
C1:90F8  E2 20 A6 0A BD CC AE 09 80 9D CC AE
C1:9101  E6 0C
C1:9103  E2 20 7B E6 0A
C1:9108  A5 0A CD CB AE 90 CE
C1:910E  64 09
C1:9110  A5 0C F0 13
C1:9114  8D CB AE
C1:9117  20 21 AE
C1:911A  AD 24 AF D0 08
C1:9120  20 FD AE
C1:9123  20 3E 8C
C1:9128  80 05
C1:912A  A9 01 8D 24 AF
C1:912F  60
```

### What it does
1. calls `AC14`
   - so operand `+1` is an inline selector-control byte
2. empty selection -> failure
3. reads the next two CC bytes as a 16-bit immediate threshold in `$08/$09`
4. iterates the current selected entries in `AECC`
5. for each entry:
   - resolves a structured-record base through `FD:A80B`
   - reads the 16-bit field at record offset `+3`
   - if `record_word_+3 <= immediate_word`, it:
     - sets bit 7 on that entry byte in `AECC`
     - increments the marked-count `$0C`
6. after the scan:
   - zero marked entries -> failure
   - otherwise:
     - `AECB = marked_count`
     - `JSR $AE21`
     - if `AF24 == 0`, then `AEFD` and `8C3E`

### What this proves
Opcode `08` is the clearest new beneficiary of the `AE21` solution.

The OR-`0x80` operation is not “increment” or vague in-place mutation.
It is the **candidate mark** that `AE21` later requires.

### Strongest safe interpretation
Global opcode `08` is best carried forward as:

> **mark selected entries whose `FD:A80B` record word at offset `+3` is at or below an immediate 16-bit threshold, then reduce to one chosen entry through `AE21`**

---

## 3. Global opcode `09` scans selected entries for a record-byte `>=` threshold hit, then hands control to `AE21`
Handler bytes:

```text
C1:9130  20 14 AC
C1:9133  AD CB AE F0 50
C1:9138  7B AE D2 B1 E8 8E D2 B1 BF 00 00 CC 85 0A
C1:9145  64 0B
C1:9147  E8 8E D2 B1 BF 00 00 CC 85 08
C1:9151  7B AA 86 0E
C1:9155  BD CC AE
C1:9158  C2 20 0A AA
C1:915C  BF 0B A8 FD A8
C1:9161  7B E2 20
C1:9165  B1 0A C5 08 B0 0D
C1:916B  E6 0E
C1:916D  A6 0E A5 0E CD CB AE 90 E0
C1:9176  80 10
C1:9178  20 21 AE
C1:917B  AD 24 AF D0 08
C1:9180  20 FD AE
C1:9183  20 3E 8C
C1:9188  A9 01 8D 24 AF
C1:918D  60
```

### What it does
This body:
1. calls `AC14`
2. empty selection -> failure
3. reads:
   - operand `+1` as a byte offset into the `FD:A80B` record
   - operand `+2` as a compare byte
4. scans the selected entries one by one
5. for each entry:
   - loads `record_byte = *(record_base + operand1)`
   - if `record_byte >= operand2`, it immediately breaks out to `AE21`
6. if the whole selected list is scanned with no hit, it fails

### Why this is **not** just a simple survivor filter
Unlike opcodes `01/02/03/08`, this body does **not** set bit 7 on entries in `AECC` before calling `AE21`.

That means the strong thing proved here is:

> opcode `09` is a **scan/gate wrapper** that reaches `AE21` on the first
> `record_byte >= immediate` hit.

Its exact final chosen-entry behavior still depends on:
- the incoming selected-entry mark state
- the now-solved `AE21` reducer

### Strongest safe interpretation
Global opcode `09` is best carried forward as:

> **scan selected entries for an `FD:A80B` record byte at immediate offset meeting `>= immediate`, then attempt chosen-entry reduction through `AE21`**

This is mechanically stronger than the old vague read, but still honest about the unresolved mark-state question.

---

## 4. Global opcode `0A` is a direct chosen-entry bit-clear gate, not an `AE21` body
Handler bytes:

```text
C1:918E  20 14 AC
C1:9191  AD CB AE F0 5D
C1:9196  C9 01 F0 22
C1:919A  7B AA A8
C1:919D  BD 3A B2 D9 CC AE F0 11
C1:91A5  C8 98 CD CB AE 90 F1
C1:91AC  7B A8 E8 8A C9 08 90 E9
C1:91B4  80 3D
C1:91B6  B9 CC AE 8D CC AE
C1:91BC  7B AE D2 B1 E8 8E D2 B1 BF 00 00 CC 85 0A
C1:91CA  64 0B
C1:91CC  AD CC AE
C1:91CF  C2 20 0A AA
C1:91D3  BF 0B A8 FD A8
C1:91D8  7B E2 20
C1:91DB  B1 0A 85 08
C1:91DF  AE D2 B1 E8 8E D2 B1 BF 00 00 CC
C1:91EA  24 08 F0 05
C1:91EE  20 3E 8C
C1:91F3  A9 01 8D 24 AF
C1:91F8  60
```

### What it does
1. calls `AC14`
2. empty selection -> failure
3. if exactly one entry is selected, uses it directly
4. if more than one entry is selected:
   - scans WRAM vector `B23A[0..7]`
   - looks for the first selected entry that appears in that vector
   - copies that chosen entry into `AECC[0]`
   - if no selected entry matches, fails
5. then:
   - operand `+1` is a record-byte offset
   - loads the chosen entry's record byte through `FD:A80B`
   - operand `+2` is an immediate mask
   - `BIT $08` decides the outcome

Success occurs when:

> `(operand2 & chosen_record_byte) == 0`

### What this proves
Opcode `0A` is cleanly **not** part of the marked-entry `AE21` family.

It is a direct chosen-entry replay gate:
- choose one entry
- test one mask-clear condition
- success -> `8C3E`
- failure -> `AF24 = 1`

### Strongest safe interpretation
Global opcode `0A` is best carried forward as:

> **gate tail replay on a priority-chosen selected entry whose `FD:A80B` record byte at immediate offset has no overlap with an immediate mask**

### Important caution
The final human-facing noun for `B23A` is still open.
But this pass makes its structural role here very clear:
it provides the order used when opcode `0A` must reduce a multi-entry selected list to one entry.

---

## 5. Global opcode `0B` is the `<=` scan sibling of opcode `09`
Handler bytes:

```text
C1:91F9  64 0A 64 0B
C1:91FD  20 14 AC
C1:9200  AD CB AE F0 52
C1:9205  7B AE D2 B1 E8 8E D2 B1 BF 00 00 CC 85 0A
C1:9213  64 0B
C1:9215  E8 8E D2 B1 BF 00 00 CC 85 08
C1:921F  7B AA 86 0E
C1:9223  BD CC AE
C1:9226  C2 20 0A AA
C1:922A  BF 0B A8 FD A8
C1:922F  7B E2 20
C1:9232  B1 0A C5 08 F0 0F 90 0D
C1:923A  E6 0E
C1:923C  A6 0E A5 0E CD CB AE 90 DE
C1:9245  80 10
C1:9247  20 21 AE
C1:924A  AD 24 AF D0 08
C1:924F  20 FD AE
C1:9252  20 3E 8C
C1:9257  A9 01 8D 24 AF
C1:925C  60
```

### What it does
This is the structural sibling of `09` with the opposite compare sense.

It:
1. calls `AC14`
2. empty selection -> failure
3. reads:
   - operand `+1` as record-byte offset
   - operand `+2` as compare byte
4. scans the selected entries
5. on the first entry where:

> `record_byte <= operand2`

it breaks out to `AE21`

6. if the scan completes with no such hit, it fails

### Why the old “greater-than filter” read should be retired
The critical compare bytes are:

```text
CMP operand2
BEQ success
BCC success
```

So this is the `<=` sibling, not the `>` sibling.

And like opcode `09`, it does **not** mark `AECC` entries itself before calling `AE21`.

### Strongest safe interpretation
Global opcode `0B` is best carried forward as:

> **scan selected entries for an `FD:A80B` record byte at immediate offset meeting `<= immediate`, then attempt chosen-entry reduction through `AE21`**

---

## 6. Correction to pass-63 carry-forward
Pass 64 forces one important cleanup.

### Retire the old wording that implied `AE21` was just a generic finalize step
That phrasing was too weak once the helper itself was decoded.

The stronger and now more correct framing is:

- `01/02/03/08` mark candidate survivor entries with bit 7
- `AE21` reduces marked candidates to one chosen entry or raises `AF24`
- then `AEFD` / `8C3E` continue the replay path

### Retire the old wording that treated the OR-`0x80` writes as “increments”
Those are mark operations, not arithmetic increments.

That correction matters because it is exactly what makes the early record-filter family coherent.

---

## Provisional labels to carry forward
- `C1:AE21..C1:AE6F`
  - `ct_reduce_marked_selected_entries_to_single_choice_or_fail`
- `C1:90BE..C1:912F`
  - `ct_global_opcode_08_mark_selected_entries_by_fd_record_word3_le_immediate_then_reduce`
- `C1:9130..C1:918D`
  - `ct_global_opcode_09_scan_selected_entries_for_fd_record_byte_offset_gte_immediate_then_reduce`
- `C1:918E..C1:91F8`
  - `ct_global_opcode_0A_gate_tail_replay_on_priority_selected_entry_record_mask_clear`
- `C1:91F9..C1:925C`
  - `ct_global_opcode_0B_scan_selected_entries_for_fd_record_byte_offset_lte_immediate_then_reduce`

---

## What remains open right next to this seam
The next adjacent unresolved block is still:

- `0C -> 925D`
- `0D -> 92A3`
- `0E -> 9314`
- `0F -> 938D`
- `10 -> 93E6`
- `11 -> 942A`
- `12 -> 9474`

The strongest next move now is even clearer than before:

1. continue straight into `0C/0D/0E`
2. keep the new `AE21` contract in view while reading them
3. then crack the short direct gate trio `10/11/12`
