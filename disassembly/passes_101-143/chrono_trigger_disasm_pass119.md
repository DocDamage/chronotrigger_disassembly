# Chrono Trigger Disassembly — Pass 119

## Purpose

Pass 118 closed representative caller-side ownership around the settlement/search subsystem, but it carried one real banking mistake forward: several bank-`C2` absolute `JSR $8820` callsites were being described as if they targeted `C0:8820`.

This pass fixes that ownership bug first, then closes the sibling `C2` caller cluster rooted at `A1B2`, `A2CE`, and `A321`.

---

## Biggest closure

The settlement/search subsystem and its caller family are now bank-corrected.

The exact pipeline previously carried forward as `C0:8820..991F` must be read as:

> **`C2:8820..991F` = exact DP=`$1D00` current-slot candidate-offset settlement/search pipeline**

Why that correction is mandatory:

- on 65816, `JSR abs` is bank-local
- the caller family at:
  - `C2:8E5D`
  - `C2:8F99`
  - `C2:A1C3`
  - `C2:A244`
  - `C2:A2DE`
  - `C2:A336`
  all uses plain absolute `JSR $8820`
- therefore those calls target **`C2:8820`**, not `C0:8820`
- direct byte check confirms the banks differ:
  - `C0:8820` begins `8D EB 01 0B ...`
  - `C2:8820` begins `DA 5A 08 E2 30 ...`

So the structural work from passes 115–118 survives, but the **bank prefix was wrong**. The real owner band is bank `C2`, and the old “outer-bank caller” seam suggested from raw absolute-xref output was bogus.

---

## 1. Bank-local xref correction: the real caller family is bank `C2`

The raw absolute-xref list for `$8820` contains entries in `C4/D0/D4/D5/D7/E5`, but those are only same-offset local calls inside those banks.

They are **not** callers of the settlement/search service in bank `C2`.

So the safe carry-forward correction is:

- `C2:8820..C2:991F` owns the settlement/search pipeline
- the representative caller family closed in passes 117–118 belongs to bank `C2`
- the suggested next seam from pass 118:
  - `D4:CE8A`
  - `E5:C1AA`
  is no longer safe as “outer-bank caller ownership” evidence for this subsystem

That correction is now frozen.

---

## 2. `C2:A1B2..A1E8` is the exact full-span linear settlement sweep with twin post-settlement tail dispatchers

### Exact body

```text
C2:A1B2  PHP
C2:A1B3  SEP #$20
C2:A1B5  LDA $0413
C2:A1B8  STA $71
C2:A1BA  STZ $72
C2:A1BC  REP #$30
C2:A1BE  LDA #$2E00
C2:A1C1  STA $61
loop:
C2:A1C3  JSR $8820
C2:A1C6  ORA $51
C2:A1C8  BEQ use_A216
C2:A1CA  JSR $A1E9
C2:A1CD  BRA +3
use_A216:
C2:A1CF  JSR $A216
C2:A1D2  INC $71
C2:A1D4  LDA $71
C2:A1D6  CMP $85
C2:A1D8  BCS done
C2:A1DA  LDA $61
C2:A1DC  CLC
C2:A1DD  ADC #$0180
C2:A1E0  STA $61
C2:A1E2  CMP #$3280
C2:A1E5  BCC loop
done:
C2:A1E7  PLP
C2:A1E8  RTS
```

### Exact behavior now frozen

- seeds local slot/index byte `71 = 0413`
- clears `72`
- seeds work pointer/base word `61 = 2E00`
- repeatedly runs exact settlement/search service `C2:8820`
- then tests exact post-settlement local byte `51`
  - `51 != 0` -> runs `A1E9`
  - `51 == 0` -> runs `A216`
- after each pass:
  - increments `71`
  - advances `61 += 0x0180`
- exits when either:
  - `71 >= 85`
  - or `61 >= 3280`

Strongest safe reading:

> **`C2:A1B2..A1E8` is the exact full-span linear settlement sweep over `61/71`, repeatedly calling the bank-`C2` settlement/search service and choosing one of two post-settlement tail dispatchers from local result byte `51`.**

That is much stronger than “another caller.”

---

## 3. `C2:A1E9..A215` and `C2:A216..A22E` are the exact twin post-settlement tail family

This range closes the two exact tails selected by `A1B2`.

### `A1EF..A215` exact common gate

```text
C2:A1EF  PHP
C2:A1F0  REP #$30
C2:A1F2  STZ $0D5D
C2:A1F5  LDA $9A90
C2:A1F8  AND #$0007
C2:A1FB  STA $0D4D
C2:A1FE  ASL A
C2:A1FF  TAX
C2:A200  LDA $0D38,X
C2:A203  CMP $9A93
C2:A206  BCC +6
C2:A208  LDA #$0004
C2:A20B  STA $0D5D
C2:A20E  LDA #$0020
C2:A211  TSB $0D4D
C2:A214  PLP
C2:A215  RTS
```

### Twin tail bodies

```text
C2:A1E9  LDX #$BE15
C2:A1EC  JMP $ED31

C2:A216  JSR $A1EF
C2:A219  LDX #$BE0E
C2:A21C  JMP $ED31

C2:A21F  PHP
C2:A220  REP #$30
C2:A222  JSR $A22F
C2:A225  LDA #$2E00
C2:A228  STA $61
C2:A22A  JSR $A216
C2:A22D  PLP
C2:A22E  RTS
```

### Exact behavior now frozen

- `A1EF`:
  - clears `0D5D`
  - copies low three bits of `9A90` into `0D4D`
  - indexes exact compare table `0D38`
  - compares that selector-derived threshold against `9A93`
  - if table value is **not below** `9A93`, then:
    - forces `0D5D = 4`
    - sets bit `0x20` in `0D4D`

- `A1E9`:
  - exact direct tail jump to common downstream service `ED31` with `X = BE15`

- `A216`:
  - runs the exact common gate `A1EF`
  - exact direct tail jump to `ED31` with `X = BE0E`

- `A21F`:
  - runs the already-closed one-shot settlement wrapper `A22F`
  - resets `61 = 2E00`
  - then runs `A216`

Strongest safe reading:

> **`A1E9/A216` are exact twin post-settlement tail dispatchers sharing selector/threshold gate `A1EF`, and `A21F` is the exact wrapper that chains the one-shot settlement materializer into the `A216` tail.**

---

## 4. `C2:A2CE..A2EC` is the exact one-shot settlement tail that feeds `A6F0` and `ED31`

This is the first sibling caller body after the pass-118 one-shot wrapper family.

### Exact body

```text
C2:A2CE  SEP #$20
C2:A2D0  STZ $0D22
C2:A2D3  LDA $0412
C2:A2D6  STA $54
C2:A2D8  CLC
C2:A2D9  ADC $0413
C2:A2DC  STA $71
C2:A2DE  JSR $8820
C2:A2E1  LDX #$30A2
C2:A2E4  JSR $A6F0
C2:A2E7  LDX #$BDEF
C2:A2EA  JSR $ED31
```

### Exact behavior now frozen

- clears exact local/state word `0D22`
- seeds selector/index byte `54 = 0412`
- seeds `71 = 0412 + 0413`
- runs exact settlement/search service `C2:8820`
- immediately fans into downstream materializer/service pair:
  - `A6F0` with `X = 30A2`
  - `ED31` with `X = BDEF`

Strongest safe reading:

> **`C2:A2CE..A2EC` is the exact one-shot settlement tail that seeds `54/71`, runs the bank-`C2` settlement/search service once, then fans the settled state into `A6F0` and the `ED31` common service through fixed `X` selectors.**

---

## 5. `C2:A2ED..A320` is the exact static block-seed and common-service tail after `A170`

### Exact body

```text
C2:A2ED  JSR $A170
C2:A2F0  REP #$30
C2:A2F2  LDA #$969A
C2:A2F5  STA $9694
C2:A2F8  LDA #$9300
C2:A2FB  STA $9696
C2:A2FE  LDA #$0013
C2:A301  STA $9698
C2:A304  LDA #$61FF
C2:A307  STA $5D42
C2:A30A  LDX #$5D42
C2:A30D  LDY #$5D44
C2:A310  LDA #$0015
C2:A313  MVN $7E,$7E
C2:A316  JSR $9E76
C2:A319  LDX #$FBE3
C2:A31C  JSR $8385
C2:A31F  PLP
C2:A320  RTS
```

### Exact behavior now frozen

- runs front helper `A170`
- seeds exact `9694/9696/9698` triplet:
  - `9694 = 969A`
  - `9696 = 9300`
  - `9698 = 0013`
- seeds `5D42 = 61FF`
- uses overlapping `MVN` to propagate that fill across `5D42..5D58`
- runs exact helper `9E76`
- finishes through common service call `8385` with `X = FBE3`

Strongest safe reading:

> **`C2:A2ED..A320` is the exact static block-seed and common-service tail after `A170`, owning the `9694/9696/9698` seed triplet and the `5D42..5D58` propagated fill.**

This range is now no longer generic filler between two bigger callers.

---

## 6. `C2:A321..A388` is the exact settlement-driven quad-block materializer with service fanout

This is the strongest new sibling closure in the cluster.

### Exact body

```text
C2:A321  PHP
C2:A322  REP #$30
C2:A324  LDX #$BE6D
C2:A327  JSR $ED31
C2:A32A  LDA $0412
C2:A32D  CLC
C2:A32E  ADC $0413
C2:A331  AND #$00FF
C2:A334  STA $71
C2:A336  JSR $8820
C2:A339  LDA #$2E00
C2:A33C  STA $61
C2:A33E  JSR $A216
C2:A341  LDA #$40FF
C2:A344  STA $5CC2
C2:A347  LDX #$5CC2
C2:A34A  LDY #$5CC4
C2:A34D  LDA #$0015
C2:A350  MVN $7E,$7E
C2:A353  LDA #$969A
C2:A356  STA $9694
C2:A359  LDA #$9300
C2:A35C  STA $9696
C2:A35F  LDA #$0025
C2:A362  STA $9698
C2:A365  SEP #$20
C2:A367  STZ $54
C2:A369  JSR $A38B
C2:A36C  INC $0D15
C2:A36F  DEC $0D9A
C2:A372  LDX #$FBE3
C2:A375  JSR $8385
C2:A378  LDX #$FBFF
C2:A37B  JSR $8385
C2:A37E  LDX #$FC45
C2:A381  JSR $8385
C2:A384  LDA #$C5
C2:A386  STA $0D13
C2:A389  PLP
C2:A38A  RTS
```

### Exact behavior now frozen

- runs common front service `ED31` with `X = BE6D`
- seeds `71 = (0412 + 0413) & 00FF`
- runs exact settlement/search service `C2:8820`
- resets `61 = 2E00`
- runs exact post-settlement tail `A216`
- seeds `5CC2 = 40FF`
- uses overlapping `MVN` to propagate that fill across `5CC2..5CD8`
- seeds exact `9694/9696/9698` triplet:
  - `9694 = 969A`
  - `9696 = 9300`
  - `9698 = 0025`
- clears selector byte `54`
- runs exact helper `A38B`
- updates state/count bytes:
  - `INC 0D15`
  - `DEC 0D9A`
- fans out through three exact common service calls:
  - `8385` with `X = FBE3`
  - `8385` with `X = FBFF`
  - `8385` with `X = FC45`
- forces `0D13 = C5`

Strongest safe reading:

> **`C2:A321..A388` is the exact settlement-driven quad-block materializer and service-fanout caller, pairing one settlement/search pass with the `A216` tail, a propagated `5CC2..5CD8` fill, a selector-zeroed `A38B` table helper, and a fixed three-service fanout.**

---

## 7. `C2:A38B..A418` is the exact selector-indexed block helper cluster behind `A321`

This helper cluster is strong enough to promote now.

### `A38B..A3B8`

```text
C2:A38B  PHP
C2:A38C  SEP #$20
C2:A38E  TDC
C2:A38F  LDA $54
C2:A391  STA $0077
C2:A394  REP #$30
C2:A396  ASL A
C2:A397  STA $00
C2:A399  ASL A
C2:A39A  ASL A
C2:A39B  ADC $00
C2:A39D  ADC #$A3BA
C2:A3A0  TAY
C2:A3A1  STZ $7D
C2:A3A3  LDX #$3086
C2:A3A6  LDA #$C20A
C2:A3A9  JSR $EF65
C2:A3AC  LDX #$3040
C2:A3AF  LDY #$3840
C2:A3B2  SEC
C2:A3B3  LDA #$007F
C2:A3B6  MVN $7E,$7E
C2:A3B7  PLP
C2:A3B8  RTS
```

### `A3BA..A3E1`

- exact four-entry table
- exact entry size = `0x0A` bytes
- selected by exact formula:
  - `Y = A3BA + 10 * 54`

### `A3E2..A418`

```text
C2:A3E2  PHP
C2:A3E3  REP #$30
C2:A3E5  LDX #$3062
C2:A3E8  JSR $A3ED
C2:A3EB  PLP
C2:A3EC  RTS
C2:A3ED  STX $61
C2:A3EF  LDA $0077
C2:A3F2  AND #$00FF
C2:A3F5  STA $00
C2:A3F7  STZ $02
loop:
C2:A3F9  LDA #$1C0B
C2:A3FC  LDX $00
C2:A3FE  CPX $02
C2:A400  BNE +3
C2:A402  LDA #$000B
C2:A405  JSR $ECAC
C2:A408  INC $02
C2:A40A  LDA $61
C2:A40C  CLC
C2:A40D  ADC #$0080
C2:A410  STA $61
C2:A412  LDA $02
C2:A414  CMP #$0004
C2:A417  BCC loop
C2:A418  RTS
```

### Exact behavior now frozen

- `A38B`:
  - latches selector `54 -> 77`
  - computes exact table entry base `A3BA + 10*54`
  - clears `7D`
  - runs helper `EF65` with:
    - `X = 3086`
    - `A = C20A`
    - `Y = selector-derived table entry`
  - then copies exact `0x80`-byte block from `3040` to `3840`

- `A3E2/A3ED`:
  - starts at `61 = 3062`
  - walks four exact `0x80`-spaced bands
  - for each band writes default word `1C0B` through `ECAC`
  - but for the single selector-matched band (`02 == 77`) writes exact override word `000B`

Strongest safe reading:

> **`C2:A38B..A418` is the exact selector-indexed block helper cluster behind `A321`, owning the 4-entry `0x0A`-byte selector table, the `3040 -> 3840` `0x80`-byte block copy, and the four-band `1C0B`/`000B` marker writer keyed by latched selector `77`.**

---

## Honest remaining gap

This pass fixed a real bank-ownership bug and closed the sibling `C2` caller cluster strongly enough to stop using the old “outer-bank caller” seam.

What still remains open is the **higher-level noun** tying together the broader bank-`C2` family beyond the representative callers frozen so far.

The best next targets are now same-bank and bank-correct:

- `C2:9DB9..9ED0`
- `C2:A046..A0BA`
- `C2:A886..A8??`
- `C2:B002`
- `C2:BA32`
- `C2:BEEF`

And the next hygiene task is explicit:

- relabel the old carry-forward wording from `C0:8820..991F` to `C2:8820..991F`
- treat raw absolute-xref hits across other banks as **same-offset local calls**, not proof of cross-bank subsystem ownership
