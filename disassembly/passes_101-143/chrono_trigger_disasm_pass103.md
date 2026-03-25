# Chrono Trigger Disassembly — Pass 103

## Scope
Pass 102 froze the late CD-side tail driver at `CD:8978..89CB`, but the owner block that seeds `CE13 = 0x03` and `CE0E = 0x80` was still being described too loosely.

This pass stayed inside that local CD/CE owner chain and decoded the exact blocking helper family rooted at:

- `CD:0D62`
- `CD:0D93`
- `CD:0DB1`
- `CD:0DD8`
- `CD:0DFA`
- `CD:0E05`

## Starting point
- previous top-of-stack: **pass 102**
- live seam from the note: **`CD:0DB1..0DFB`**

## Work performed
- decoded the ROM bytes from PC `0x0D0D62..0x0D0E22` instruction-for-instruction
- separated the real helper boundaries inside the old seam instead of treating it as one monolithic blob
- rechecked the local WRAM contracts around `5D9B`, `CCEA`, `CE0E`, and `CE13`
- cross-checked the nearby clean caller neighborhood around PC `0x0D03ED..0x0D040D` to confirm that `CD:0D93` and `CD:0DB1` are sibling blocking helpers selected by a later chooser block

## 1. `CD:0D62..0D92` is an exact restart/reinit helper, not generic setup noise
The exact body is:

```text
CD:0D62  PHX
CD:0D63  LDA #$80
CD:0D65  STA $1E00
CD:0D68  STZ $1E01
CD:0D6B  LDA #$FF
CD:0D6D  STA $1E02
CD:0D70  JSL C7:0004
CD:0D74  JSR $3E7D
CD:0D77  LDA #$10
CD:0D79  STA $1E00
CD:0D7C  LDA #$3A
CD:0D7E  STA $1E01
CD:0D81  JSL C7:0004
CD:0D85  PLX
CD:0D86  JSR $0EBD
CD:0D89  STZ $5D9B
CD:0D8C  JSR $0D33
CD:0D8F  INC $5D9B
CD:0D92  RTS
```

That means this block is doing two exact things, in a fixed order:

1. submit two fixed `C7:0004` sound/APU packets through the `1E00..` workspace
2. rebuild/rearm the auxiliary-stage machinery under the caller-supplied selector in `X`

So the strongest safe reading is:

> exact restart/reinit helper that submits fixed low-bank sound/APU packets, reinitializes the auxiliary stage by selector, rebuilds the descriptor work tables, and leaves the stage active.

## 2. `CD:0D93..0DB0` is an exact blocking selector-`0x87` launcher
The exact body is:

```text
CD:0D93  STZ $99D2
loop_idle:
CD:0D96  JSR $039E
CD:0D99  JSR $3E7D
CD:0D9C  LDA.l $002141
CD:0DA0  BNE loop_idle
CD:0DA2  LDX #$0087
CD:0DA5  JSR $0D62
wait_stage_clear:
CD:0DA8  JSR $3E7D
CD:0DAB  LDA $5D9B
CD:0DAE  BNE wait_stage_clear
CD:0DB0  RTS
```

That closes an important local distinction:
- `0D93` is a blocking helper
- it launches selector `0x87` through `0D62`
- then it waits only on `5D9B`

So this is not the same helper as `0DB1`; it is the simpler sibling.

## 3. `CD:0DB1..0DD7` is the exact owner block behind the old `CE13/CE0E` seam
The exact body is:

```text
loop_idle:
CD:0DB1  JSR $039E
CD:0DB4  JSR $3E7D
CD:0DB7  LDA.l $002141
CD:0DBB  BNE loop_idle

CD:0DBD  LDA #$03
CD:0DBF  STA $CE13
CD:0DC2  LDA #$80
CD:0DC4  STA $CE0E
CD:0DC7  JSR $0DD8

CD:0DCA  LDA #$80
loop_delay:
CD:0DCC  JSR $3E7D
CD:0DCF  DEC A
CD:0DD0  BNE loop_delay

CD:0DD2  LDX #$0084
CD:0DD5  JSR $0D62
```

and then execution falls directly into `CD:0DD8`.

This is the pass that finally turns the old handoff bullet into exact structure:
- `CE13 = 0x03` is seeded here intentionally
- `CE0E = 0x80` is seeded here intentionally
- those writes are immediately followed by a blocking drain helper
- then a fixed `0x80`-tick delay
- then a fresh auxiliary-stage launch under selector `0x84`

So the strongest safe reading is:

> exact owner-side transition helper that waits for APU idleness, forces the local CD/D1 control bytes into a masked signed-target state, drains current work to quiescence, burns a fixed delay, launches selector `0x84`, and continues blocking through the shared drain loop.

## 4. `CD:0DD8..0DFF` is the real drain/quiescence helper
This was the most important structural split of the pass.

The exact body is:

```text
repeat:
CD:0DD8  JSR $3E7D
CD:0DDB  JSR $3E7D
CD:0DDE  JSL $CD04AA
CD:0DE2  LDA $CE0B
CD:0DE5  CMP #$02
CD:0DE7  BCS repeat
CD:0DE9  LDA $CE0A
CD:0DEC  ORA $CCEA
CD:0DEF  ORA $A013
CD:0DF2  ORA $5D9B
CD:0DF5  BNE repeat
CD:0DF7  RTS
```

This means the helper returns only when **both** conditions are satisfied:

1. `CE0B < 0x02`
2. `CE0A | CCEA | A013 | 5D9B == 0`

That is the exact answer to the old seam question.
The loop over `CE0A | CCEA | A013 | 5D9B` is not decorative; it is the owner-side quiescence test.

And because pass 100 already proved the D1 side is palette-profile maintenance, the local reading here is now much better grounded:

- `CE0B` is the D1-side target/selector byte the owner cares about here
- `CE0A`, `CCEA`, `A013`, and `5D9B` are treated as outstanding local busy/progress flags
- `CD:04AA` is the service step repeatedly called while that work drains

## 5. `CD:0DFA..0E04` and `CD:0E05..0E22` close the blocking-wrapper side of `5D9B`
The tiny helper at `0DFA` is exact:

```text
CD:0DFA  LDA $5D9B
CD:0DFD  BEQ done
CD:0DFF  JSR $3E75
CD:0E02  BRA $0DFA
CD:0E04  RTS
```

And the wrapper at `0E05` is exact:

```text
CD:0E05  PHA
CD:0E06  JSR $0DFA
CD:0E09  PLA
CD:0E0A  TAX
CD:0E0B  JSR $0EBD
CD:0E0E  JSR $0D33
CD:0E11  INC $5D9B
loop:
CD:0E14  LDA $5D9B
CD:0E17  BEQ done
CD:0E19  JSR $3E75
CD:0E1C  JSL $CD04AA
CD:0E20  BRA loop
CD:0E22  RTL
```

This is a nice semantic cleanup:
- `0D28` is the already-frozen nonblocking coordinator
- `0E05` is the exact blocking sibling that waits for any previous stage to clear, starts the new one, and services it until the active flag clears

## 6. What pass 103 changes about the WRAM nouns
### `5D9B`
Earlier passes already had the right broad noun: active flag for the optional auxiliary stage.
Pass 103 makes that much tighter:
- `0D62` clears it before rebuilding the stage, then increments it to mark the rebuilt stage active
- `0D93`, `0DFA`, and `0E05` busy-wait on it directly
- `0DD8` ORs it into the owner-side quiescence test

So this is now a real blocking-owner contract, not just a general “active while running” guess.

### `CCEA`
Pass 79 had the right neighborhood noun but not the clean owner-side consumer.
Pass 103 adds that:
- `0DD8` refuses to return while `CCEA != 0`

So `CCEA` is now materially tighter as a stage progress/busy byte that blocks owner-side completion.

### `CE0E`
Pass 98 proved the clean D1-side consumer path.
Pass 103 adds the exact owner-side write:
- `0DBD..0DC6` seeds `CE0E = 0x80` immediately before the blocking drain helper

So `CE0E` is no longer just “token-era staging plus D1-side reader.”
It is also an exact owner-side preseed byte for this blocking transition path.

### `CE13`
Pass 102 already proved the `7C & CE13` mask gate before `D1:EA4B`.
Pass 103 now places the clean owner-side write into a real exact helper:
- `0DBD..0DC1` seeds `CE13 = 0x03` immediately before the owner-side drain path

That makes the local control neighborhood around `CE13` much less hypothetical.

## 7. strongest keepable conclusions
1. `CD:0DB1..0DFB` is no longer a fuzzy owner blob; it is an exact blocking transition helper built from two real pieces: a seeded prelude and the shared drain loop at `0DD8`.
2. `CE13 = 0x03` and `CE0E = 0x80` are exact owner-side transition inputs, not stray writes.
3. `CD:0DD8` is the exact quiescence loop that answers the old seam question: it waits for `CE0B < 2` and for `CE0A | CCEA | A013 | 5D9B` to all clear.
4. `CD:0D62` is a real restart/reinit helper with two fixed `C7:0004` packet submits before stage rebuild.
5. `CD:0D93` and `CD:0E05` are exact blocking siblings around the same auxiliary-stage family, one hardwired to selector `0x87`, the other driven by caller `A`.

## Honest caution
Even after this pass:

- I have **not** frozen the final higher-level noun of `CD:039E`, `CD:04AA`, `CD:3E75`, or `CD:3E7D`.
- I have **not** frozen the final gameplay-facing noun of `A013`.
- I have **not** frozen the exact higher-level noun of the chooser block around `CD:83ED..840D` that decides between `0D93` and `0DB1`.
- I have **not** frozen a clean direct static reader of `CE0F`.

## Next recommended target
The cleanest next static move is now:

1. stay in the same local CD owner chain
2. decode the chooser block around **`CD:83ED..840D`**
3. specifically freeze:
   - why `2A21 & 0x11` matters here
   - why `7F:01EC` selects between the `0D93` and `0DB1` blocking helpers
   - how that chooser feeds the already-frozen owner helpers from this pass
