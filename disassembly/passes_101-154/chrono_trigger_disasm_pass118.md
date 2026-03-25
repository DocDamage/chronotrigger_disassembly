# Chrono Trigger Disassembly — Pass 118

## Purpose

Pass 117 structurally closed the whole `C0:8820..991F` candidate-offset settlement pipeline, but the final ownership gap moved into the broad caller family in bank `C2`.

This pass stayed on that exact caller seam and only promoted what the bytes justify.

---

## Biggest closure

`C0:8820` is no longer just an internally solved `C0` pipeline waiting for a noun.

Representative `C2` callers now prove that bank `C2` consumes it in **three exact grammars**:

1. an **iterative current-slot sweep** with optional per-axis export/clamp
2. a **selective accepted-slot list builder** over those exported bands
3. a **one-shot settlement-driven materialization wrapper** that commits/mirrors the resulting block and fans it into downstream table writers

That is enough to promote `C0:8820` from “isolated internal solver” to an exact **bank-`C2` current-slot settlement service** with multiple distinct caller contracts.

I am still intentionally **not** bluffing the final gameplay-facing noun of the whole subsystem yet.

---

## 1. `C2:8E2D..8E81` is the exact iterative current-slot settlement sweep with optional per-axis export and clamp

This band is now closed strongly enough to promote as one caller contract.

### Exact top shape

```text
C2:8E2D  PHP
C2:8E2E  REP #$30
C2:8E30  LDA #$FFFF
C2:8E33  STA $0F63
C2:8E36  LDX #$0F63
C2:8E39  LDY #$0F65
C2:8E3C  LDA #$0009
C2:8E3F  MVN $7E,$7E
C2:8E42  SEP #$20
C2:8E44  JSR $8ECC
C2:8E47  LDA $0DBE
C2:8E4A  STA $71
C2:8E4C  LDA #$01
C2:8E4E  STA $00
C2:8E50  LDA $0DBD
C2:8E53  BIT #$08
C2:8E55  BEQ +6
C2:8E57  LDA $73
C2:8E59  STA $00
C2:8E5B  STZ $71
loop:
C2:8E5D  JSR $8820
...
C2:8E7A  INC $71
C2:8E7C  DEC $00
C2:8E7E  BNE loop
C2:8E80  PLP
C2:8E81  RTS
```

### Exact behavior now frozen

- seeds `0F63` with `FFFF`
- uses the overlapping `MVN` to propagate that sentinel fill across the whole six-word scratch export band at `0F63..0F6E`
- runs exact precompute/setup helper `8ECC`
- seeds local loop index `71` from `0DBE`
- seeds local loop count `00 = 1`
- if `0DBD.bit3` is set:
  - switches to `71 = 0`
  - and `00 = 73`

Then for each iteration it runs the exact current-slot settlement service at `C0:8820`.

After each settlement pass:

- if `0DBD.bit7` is set:
  - runs `8E82`
  - exports a settled word into `0F63 + 2*71`
  - and clamps current-slot word `0003,Y` against `003F,Y`

- if `0DBD.bit6` is set:
  - runs `8EAB`
  - exports a settled word into `0F69 + 2*71`
  - and clamps current-slot word `0007,Y` against `0009,Y`

### Exact helper shape now strong enough

`8E82` and `8EAB` are not free-floating math now. In this caller they are exact masked export helpers:

- `8E82` uses the settled local word lane rooted at direct-page `22`
- `8EAB` uses the settled local word lane rooted at direct-page `28`
- both are gated by `0DBF`
- both write into the prefilled `0F63..0F6E` export band
- both update current-slot per-axis words through `Y = 6F`

So the strongest safe reading is now:

> **`C2:8E2D..8E81` is the exact iterative current-slot settlement sweep that repeatedly runs `C0:8820` and conditionally exports/clamps one or both settled axis words into the six-word scratch band at `0F63..0F6E`, under `0DBD/0DBF` control.**

---

## 2. `C2:8F6C..8FC8` is the exact selective accepted-slot list builder over the exported settlement bands

This is the second exact caller grammar.

### Exact front structure

```text
C2:8F6C  PHP
C2:8F6D  SEP #$20
C2:8F6F  JSL $F7D922
C2:8F73  LDX #$FC5A
C2:8F76  JSR $8385
C2:8F79  LDA $0DBE
C2:8F7C  STA $71
C2:8F7E  INC $0D15
C2:8F81  REP #$30
C2:8F83  STZ $0F53
C2:8F86  STZ $0F5D
C2:8F89  STZ $71
C2:8F8B  STZ $00
C2:8F8D  STZ $04
loop:
C2:8F8F  JSR $8FCB
C2:8F92  JSR $8FEF
...
C2:8FB6  CMP $73
C2:8FB8  BCC loop
...
C2:8FC8  RTS
```

### Exact behavior now frozen

This band is now exact enough to describe without bluffing the gameplay noun:

- clears:
  - `0F53`
  - `0F5D`
  - local `71`
  - local `00`
  - local `04`
- loops over the exported settlement bands through `71`
- calls two exact precheck helpers:
  - `8FCB` for the band rooted at `0F63`
  - `8FEF` for the band rooted at `0F69`

### Exact precheck helper behavior

`8FCB`:

- reads word `0F63 + 2*71`
- skips on negative sentinel
- sets `92 = 2`
- calls `F13F`
- stores resulting word `8A` into `0F63 + 2*00`
- sets `0F5D.bit0`
- increments `04`

`8FEF`:

- reads word `0F69 + 2*71`
- skips on negative sentinel
- sets `92 = 1`
- calls `F13F`
- stores resulting word `8A` into `0F69 + 2*00`
- ORs `0F5D` with `0x0002`
- increments `04`

So:

- `04` is the local accepted-axis-hit count for the current slot
- `0F5D.bit0/bit1` is an exact per-axis accepted-hit mask for that same slot pass

### Exact selective re-entry and list append

If `04 != 0`, the caller then:

- reruns `C0:8820`
- loads `C2:9A90`
- calls `F626`
- uses `X = 00`
- reads current-slot word `180E,Y`
- appends that word into `0F57 + X`
- increments accepted-slot count `0F53`
- advances `00` by two bytes

Strongest safe reading:

> **`C2:8F6C..8FC8` is the exact selective accepted-slot list builder over the exported settlement bands: it probes the `0F63/0F69` axis-export bands, records which axes accepted for the current slot into `0F5D`, and appends current-slot word `180E` into the packed accepted-slot list at `0F57..` when either axis hits.**

This is the first honest caller-side closure that makes `0F53`, `0F57`, and `0F5D` strong enough to promote structurally.

---

## 3. `C2:9137..916D` is the exact template-block commit/mirror helper fed by the settlement caller family

This helper matters because the one-shot wrapper below uses it immediately after `8820`.

### Exact body shape

```text
C2:9137  PHP
C2:9138  JSR $916E
C2:913B  SEP #$20
C2:913D  LDA $9ABA
C2:9140  CMP #$A8
C2:9142  BNE +3
C2:9144  ASL $9B21
C2:9147  REP #$30
C2:9149  LDY $6F
C2:914B  LDA $9A93
C2:914E  STA $0003,Y
C2:9151  LDX #$9B1C
C2:9154  TYA
C2:9155  CLC
C2:9156  ADC #$0036
C2:9159  TAY
C2:915A  LDA #$000A
C2:915D  MVN $7E,$7E
C2:9160  LDX #$9B1C
C2:9163  LDY #$9AC6
C2:9166  LDA #$000A
C2:9169  MVN $7E,$7E
C2:916C  PLP
C2:916D  RTS
```

### Exact behavior now frozen

- runs preparatory helper `916E`
- conditionally shifts `9B21` when `9ABA == A8`
- writes word `9A93 -> 0003,Y`
- copies the exact `0x0B`-byte template block rooted at `9B1C` into:
  - current-slot record at `Y + 0x36`
  - mirror block `9AC6`

So the strongest safe reading is now:

> **`C2:9137..916D` is the exact template-block commit/mirror helper that writes one settled control word into the current slot and copies the exact `9B1C` template block both into the current-slot record and into mirror block `9AC6`.**

That is stronger than “misc downstream helper” and now proven directly from bytes.

---

## 4. `C2:A22F..A26F` is the exact one-shot settlement-driven materialization wrapper

This is the third distinct caller grammar.

### Exact body shape

```text
C2:A22F  PHP
C2:A230  SEP #$20
C2:A232  LDX #$3390
C2:A235  LDY #$0402
C2:A238  JSR $F28D
C2:A23B  LDA $0412
C2:A23E  CLC
C2:A23F  ADC $0413
C2:A242  STA $71
C2:A244  JSR $8820
C2:A247  JSR $9137
C2:A24A  LDX #$BE1C
C2:A24D  JSR $31ED
C2:A250  LDX #$30A2
C2:A253  JSR $A6F0
C2:A256  LDA #$0E
C2:A258  STA $01
C2:A25A  LDA $9A90
C2:A25D  STA $0D46
C2:A260  LDX #$2EDE
C2:A263  STX $61
C2:A265  JSR $EC38
C2:A268  JSR $A273
C2:A26B  LDX #$FBE3
C2:A26E  JSR $8385
C2:A271  PLP
C2:A272  RTS
```

### Exact behavior now frozen

This wrapper is no longer vague:

- runs fixed front helper `F28D` with `X = 3390`, `Y = 0402`
- seeds current-slot loop/input byte `71 = 0412 + 0413`
- runs exact current-slot settlement service `8820`
- immediately commits/mirrors the settled template block through exact helper `9137`
- then runs exact downstream materializers:
  - `31ED` with `X = BE1C`
  - `A6F0` with `X = 30A2`
  - `EC38` after seeding:
    - `01 = 0x0E`
    - `0D46 = 9A90`
    - `61 = 2EDE`
  - `A273`
- finishes with common service call `8385` through `X = FBE3`

Strongest safe reading:

> **`C2:A22F..A26F` is the exact one-shot settlement-driven materialization wrapper that launches `8820`, commits/mirrors the resulting template block, then fans that settled state into the downstream `31ED / A6F0 / EC38 / A273` materializer chain under fixed work-pointer seeds.**

That is enough to call it a distinct caller contract rather than just “another wrapper.”

---

## 5. `C2:A273..A2C5` is the exact selector-driven staircase-and-block materializer used by the one-shot wrapper

This is the most downstream strong promotion in this pass.

### Exact body facts now frozen

- increments `0D15`
- uses 8-bit selector `9A90`
- uses byte table rooted at `C2:A2C6`
- uses word tables rooted at:
  - `FF:CE88`
  - `FF:CE92`

From those selector-derived tables it then:

- materializes an incrementing 12-word staircase into:
  - `2EEC`
  - `2EEE`
  - `2EF0`
  - `2EF2`
  - `2EF4`
  - `2EF6`
  - `2F2C`
  - `2F2E`
  - `2F30`
  - `2F32`
  - `2F34`
  - `2F36`

and then:

- performs an exact `0x20`-byte banked block move using the selector-derived second table word

Strongest safe reading:

> **`C2:A273..A2C5` is the exact selector-driven staircase-and-block materializer used by the one-shot settlement wrapper, owning the twelve-word incrementing export into `2EEC..2F36` and an additional selector-derived `0x20`-byte block move.**

I am intentionally **not** freezing the final gameplay-facing noun of that exported block yet.

---

## 6. What this pass actually proves about caller ownership

This pass is enough to stop treating `C0:8820` like an isolated internal solver.

Representative `C2` callers now prove:

- bank `C2` owns a real caller family around `8820`
- that family uses **multiple distinct contracts**, not one repeated wrapper:
  1. iterative export/clamp sweep
  2. selective accepted-slot list build
  3. one-shot materialization
- the first exact downstream structurally promoted outputs are now:
  - `0F53`
  - `0F57..`
  - `0F5D`
  - `9B1C -> current-slot + mirror` commit path
  - `2EEC..2F36` selector-driven staircase export

That is the strongest honest caller-side ownership closure so far.

---

## Honest limits after this pass

I still did **not** freeze the final gameplay-facing noun of the whole subsystem.

What is now solved:
- the internal `C0` settlement pipeline
- three exact `C2` caller grammars around it
- the first exact caller-side export / list / materialization paths

What is still unresolved:
- the higher-level family name tying together:
  - `A1C3`
  - `A2D2`
  - `A31C`
  - outer-bank callers like `D4:CE8A`, `D5:8B4E`, `E5:C1AA`
- the final noun of the selector-driven export blocks rooted at:
  - `9B1C`
  - `0F57..`
  - `2EEC..2F36`

So the next pass should stay on sibling caller families and one outer-bank caller, not reopen `C0:8820` itself.

---

## Completion estimate after pass 118

This pass improved caller ownership and promoted the first exact caller-side outputs, but it still did not expand source-bank coverage or rebuild readiness.

Updated honest estimate:

- previous: **71.0%**
- current: **71.4%**

Why it went up:
- caller ownership is materially tighter now
- several formerly anonymous downstream scratch/export bands now have exact structural roles

Why it did **not** jump more:
- no new bank separation win
- no rebuild readiness gain
- no runtime-backed proof yet

---

## Best next move

Do **not** reopen the internal `C0:8820..991F` solver band.

The clean next seam is now:

1. sibling `C2` callers:
   - `C2:A1C3..A1E8`
   - `C2:A2D2..A319`
   - `C2:A31C..A388`

2. one outer-bank representative caller:
   - `D4:CE8A`
   - or `E5:C1AA`

3. first exact downstream consumers of:
   - `0F53`
   - `0F57..`
   - `0F5D`
   - `2EEC..2F36`

That is where the final gameplay-facing noun now lives.
