# Chrono Trigger Disassembly Pass 107

## What this pass focused on

Pass 106 closed the return-value seam at `C0:0AFF` and proved that the installed NMI trampoline ultimately commits the current `7E:0128` shadow byte to `$420C`.

That left one obvious question:

> what exact job does `FD:C1EE..C2C0` perform inside that family?

This pass closes that exact body.

The key result is that `FD:C1EE..C2C0` is **not** the place where the HDMA-enable shadow byte itself is directly read or written.
Instead, it is the exact **HDMA channel-register programming/finalization** step that loads all eight indirect HDMA channel slots from one of two paired WRAM table bundles in bank `7F`.

That matters because it narrows the remaining live seam again:
- `FD:C1EE` is now exact enough to stop babysitting
- the still-open producer side is further upstream in the paired builder families reached through `FD:C2C1`

---

## What I did

- fully decoded `FD:C1EE..C2C0`
- mapped its direct-page setup and proved it is writing the HDMA register blocks at `$4300..$437A`
- froze the two exact 8-table WRAM bundles selected by this routine
- froze the exact local role of `7E:013C.bit0` inside this body
- checked for direct `7E:0128` accesses inside bank `FD` to see whether this body itself mutates the HDMA-enable shadow

---

## 1. `FD:C1EE..C2C0` is the exact eight-channel indirect-HDMA programming/finalization body

Exact decoded structure:

```asm
FD:C1EE  PHD
FD:C1EF  REP #$20
FD:C1F1  LDA #$4300
FD:C1F4  TCD
FD:C1F5  SEP #$20

; channel control bytes
FD:C1F7  LDA #$44 : STA $00
FD:C1FB  LDA #$43 : STA $10
FD:C1FF  LDA #$43 : STA $20
FD:C203  LDA #$43 : STA $30
FD:C207  LDA #$44 : STA $40
FD:C20B  LDA #$41 : STA $50
FD:C20F  LDA #$41 : STA $60
FD:C213  LDA #$40 : STA $70

; channel B-bus targets
FD:C217  LDA #$07 : STA $01
FD:C21B  LDA #$0D : STA $11
FD:C21F  LDA #$0F : STA $21
FD:C223  LDA #$11 : STA $31
FD:C227  LDA #$2C : STA $41
FD:C22B  LDA #$26 : STA $51
FD:C22F  LDA #$31 : STA $61
FD:C233  LDA $013C
FD:C236  BIT #$01
FD:C238  BNE +4
FD:C23A  LDA #$28
FD:C23C  BRA +2
FD:C23E  LDA #$29
FD:C240  STA $71

; set all channel source-bank and indirect-bank bytes to 7F
FD:C242  LDA #$7F
FD:C244  STA $04,$14,$24,$34,$44,$54,$64,$74
FD:C254  STA $07,$17,$27,$37,$47,$57,$67,$77

; choose one of two exact 8-table bundles
FD:C264  LDA $0153
FD:C267  AND #$0F
FD:C269  BEQ first_bundle
FD:C26B  BRA second_bundle

first_bundle:
  X -> 0F80,0FD7,102E,1085,10DC,1133,118A,11E1

second_bundle:
  X -> 1238,128F,12E6,133D,1394,13EB,1442,1499

FD:C2BE  PLD
FD:C2BF  RTL
```

This is now exact enough to say:

> `FD:C1EE..C2C0` is the local finalization body that programs all eight indirect HDMA channel register blocks from one of two paired WRAM table bundles in `7F`.

That is a materially stronger reading than the old vague “HDMA-shadow/materialization path” wording.

---

## 2. The routine proves the exact two WRAM table bundles it can install

The source-address halfwords written into `$4302/$4303`, `$4312/$4313`, ... `$4372/$4373` are now exact.

### First bundle selected when `($0153 & 0x0F) == 0`
- `7F:0F80`
- `7F:0FD7`
- `7F:102E`
- `7F:1085`
- `7F:10DC`
- `7F:1133`
- `7F:118A`
- `7F:11E1`

### Second bundle selected when `($0153 & 0x0F) != 0`
- `7F:1238`
- `7F:128F`
- `7F:12E6`
- `7F:133D`
- `7F:1394`
- `7F:13EB`
- `7F:1442`
- `7F:1499`

The spacing is exact in both families:
- every start address is separated by `0x57`
- the first bundle therefore spans `7F:0F80..7F:1237`
- the second bundle therefore spans `7F:1238..7F:14EF`

So the routine is not choosing random pointers. It is installing one of two exact, tightly packed 8-entry WRAM HDMA table bundles.

---

## 3. `7E:013C.bit0` is an exact local selector for channel 7's B-bus target

This body contains the only clean local read needed to freeze a useful exact role for `7E:013C` here:

```asm
FD:C233  LDA $013C
FD:C236  BIT #$01
FD:C238  BNE use_29
FD:C23A  LDA #$28
FD:C23C  BRA store
FD:C23E  LDA #$29
FD:C240  STA $71
```

Because the direct page is `0x4300`, `$71` is the B-bus target byte for channel 7.

So the exact local truth is:
- `013C.bit0 == 0` -> channel 7 B-bus target byte is `0x28`
- `013C.bit0 != 0` -> channel 7 B-bus target byte is `0x29`

That is the strongest safe claim here.
I am still **not** pretending to know the final broader gameplay/UI noun of `013C`, but its local contract in this body is now exact.

---

## 4. `FD:C1EE` does not directly touch `7E:0128`, which narrows the producer seam again

I checked for direct `7E:0128` reads/writes inside bank `FD`.

Result:
- no clean direct `AD 28 01`
- no clean direct `8D 28 01`
- no clean long `AF/8F 28 01 00`
- no raw word hit for `7E:0128` in bank `FD`

That matters because pass 106 proved that:
- `C0:0AFF` runs `FD:C1EE`
- then returns `7E:0128`
- then the installed NMI trampoline commits that returned byte to `$420C`

Pass 107 now sharpens the causal chain:

- `FD:C1EE` is the exact **channel-register programming/finalization** body
- but it is **not** the direct `0128` writer
- so the still-open producer side is further upstream in the paired builder families behind `FD:C2C1`

This is a real narrowing of the seam, not just renaming.

---

## 5. What this changes semantically

Before this pass, the whole `FD:C1EE..C2C0` body still had the risk of being treated as a fuzzy “does some HDMA stuff” block.

That is no longer necessary.

The strongest safe reading after pass 107 is:

- `FD:C2C1` chooses one of six exact local builder families
- those builders prepare one of two paired WRAM table bundles in `7F`
- `FD:C1EE` is the exact finalizer that installs one of those two 8-channel bundles into `$4300..$437A`
- `C0:0AFF` then returns the already-prepared `7E:0128` HDMA enable shadow byte
- the installed `D1:F4C0` RAM NMI trampoline commits that shadow byte to `$420C`

So `FD:C1EE` is now exact enough to classify as **installer/finalizer**, not producer.

---

## 6. Strongest safe reading after pass 107

The exact grounded reading is now:

- `FD:C1EE..C2C0` = program all eight indirect HDMA channel register blocks from one of two exact 8-table WRAM bundles in `7F`
- `7F:0F80..1237` = first exact 8-table WRAM bundle installed when `($0153 & 0x0F) == 0`
- `7F:1238..14EF` = second exact 8-table WRAM bundle installed when `($0153 & 0x0F) != 0`
- `7E:013C.bit0` = exact local selector choosing channel 7 B-bus target byte `0x28` vs `0x29`
- the real still-open seam is **not** `FD:C1EE` anymore; it is the paired upstream builder families reached through `FD:C2C1`

---

## Honest caution

Even after this pass:

- I have **not** frozen the final broader subsystem noun of `7E:013C`; only its exact local bit0 contract in `FD:C1EE`.
- I have **not** frozen the final broader noun of `7E:0153`; only that `FD:C1EE` uses its low nibble as a zero-vs-nonzero bundle selector in addition to the already-frozen local `bit7` and `bit0` contracts.
- I have **not** frozen which of the six builder targets behind `FD:C2C1` is the direct owner of the final `7E:0128` shadow value.

---

## Best next move

Do **not** stay on `FD:C1EE`.
That body is now exact enough.

The right next move is:

1. stay inside the same family
2. move one layer upstream into the exact paired builder targets behind `FD:C2C1`
3. prioritize the paired families by selector index:
   - `0126 = 0` -> `FD:C2EB / FD:C847`
   - `0126 = 1` -> `FD:C995 / FD:CD0C`
   - `0126 = 2` -> `FD:CFCF / FD:D27E`
4. specifically find:
   - which builder family writes or finalizes `7E:0128`
   - whether the two tables chosen by `0153.bit0` are true double-buffer siblings or mode siblings
   - whether `0126` is just a local 3-way builder-family index or a wider display/state selector byte

That is the real next seam now.
