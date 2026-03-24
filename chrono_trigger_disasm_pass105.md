# Chrono Trigger Disassembly — Pass 105

## Scope
Pass 104 proved that `CD:840D..8449` installs `0501/0503 -> D1:F4C0` and that the installed target clears `$47`, but it deliberately stopped short of freezing the full higher-level role of that trampoline target.

This pass stayed on that exact seam and decoded the full installed target body at:

- `D1:F4C0..F55A`

It also tightened the local payload bytes that the trampoline flushes into PPU registers:

- `00:0045`
- `7E:BB00`
- `7E:2C70..2C7B`

## Starting point
- previous top-of-stack: **pass 104**
- live seam from the note: **`D1:F4C0..`**

## Work performed
- decoded the full exact instruction stream at PC `0x11F4C0..0x11F55A`
- proved the installed `0501/0503 -> D1:F4C0` target is an **interrupt body**, not a generic callable helper, because it terminates with exact `RTI`
- froze the exact front-edge machine-state work: save registers, set `D = 0`, disable HDMA, acknowledge NMI through `$4210`, re-arm `$4200 = 0xA1`, clear `$47`
- froze the exact flush path from the caller-staged byte `BB00 -> $45 -> $2100`
- froze the exact 12-byte flush path from `7E:2C70..2C7B` into `BG1/BG2/BG3` scroll registers `$210D..$2112`
- tightened the next seam around the return value of `JSL C0:0005`, because `D1:F4C0` writes that returned byte straight into `$420C`

## 1. `D1:F4C0..F55A` is the installed RAM NMI trampoline body
The exact body is:

```text
D1:F4C0  REP #$30
D1:F4C2  PHA
D1:F4C3  PHX
D1:F4C4  PHY
D1:F4C5  PHB
D1:F4C6  PHD
D1:F4C7  LDA #$0000
D1:F4CA  TCD
D1:F4CB  TDC
D1:F4CC  SEP #$20
D1:F4CE  STA.l $00420C
D1:F4D2  LDA.l $004210
D1:F4D6  LDA #$A1
D1:F4D8  STA.l $004200
D1:F4DC  STZ $47
D1:F4DE  JSL $CD09CE
D1:F4E2  JSL $C00005
D1:F4E6  STA $420C
D1:F4E9  LDA.l $000045
D1:F4ED  STA.l $002100
D1:F4F1  LDA #$7E
D1:F4F3  PHA
D1:F4F4  PLB
D1:F4F5  LDA $2C70
D1:F4F8  STA.l $00210D
D1:F4FC  LDA $2C71
D1:F4FF  STA.l $00210D
D1:F503  LDA $2C72
D1:F506  STA.l $00210E
D1:F50A  LDA $2C73
D1:F50D  STA.l $00210E
D1:F511  LDA $2C74
D1:F514  STA.l $00210F
D1:F518  LDA $2C75
D1:F51B  STA.l $00210F
D1:F51F  LDA $2C76
D1:F522  STA.l $002110
D1:F526  LDA $2C77
D1:F529  STA.l $002110
D1:F52D  LDA $2C78
D1:F530  STA.l $002111
D1:F534  LDA $2C79
D1:F537  STA.l $002111
D1:F53B  LDA $2C7A
D1:F53E  STA.l $002112
D1:F542  LDA $2C7B
D1:F545  STA.l $002112
D1:F549  JSL $CD0C89
D1:F54D  JSL $FDFFF7
D1:F551  REP #$30
D1:F553  PLD
D1:F554  PLB
D1:F555  PLY
D1:F556  PLX
D1:F557  PLA
D1:F558  RTI
```

The decisive fact is the ending:
- this target returns with **`RTI`**, not `RTL` or `RTS`
- so `0501/0503 -> D1:F4C0` is not pointing at a generic helper
- it is pointing at an installed **RAM interrupt-trampoline payload**

So the strongest safe reading is:

> exact installed RAM NMI trampoline body that acknowledges/re-arms the interrupt side, clears the local completion latch, refreshes PPU-visible display/scroll shadow bytes, runs two exact follow-up helpers plus one exact HDMA-mask helper, then returns with `RTI`.

## 2. The old `$47` seam is now fully closed
Pass 104 already proved the local waiter:

```text
CD:044A  LDA #$01
CD:044C  STA $47
wait:
CD:044E  LDA $47
CD:0450  BNE wait
CD:0452  RTS
```

Pass 105 completes the other side of that contract:

```text
D1:F4DC  STZ $47
```

Because the installed target is now proven to be the actual RAM NMI trampoline body, the helper meaning is no longer tentative at all:

- `CD:044A` waits for one installed trampoline / NMI cycle
- `D1:F4C0` clears `$47` on entry to signal that the cycle has started and reached the committed interrupt body

So the strongest safe reading is now:

> `$47` is the exact one-shot completion latch for this installed RAM NMI trampoline contract.

## 3. `$45 -> $2100` is an exact INIDISP flush path
Pass 104 froze the wrapper-side staging:

```text
CD:8423  LDA $BB00
CD:8426  STA $45
```

Pass 105 freezes the exact trampoline-side consumer:

```text
D1:F4E9  LDA.l $000045
D1:F4ED  STA.l $002100
```

That means the exact local path is:

```text
7E:BB00 -> 00:0045 -> PPU $2100
```

Since `$2100` is the SNES `INIDISP` register, this is not just an arbitrary forwarded byte anymore.

The strongest safe reading is:

> exact staged display-control / `INIDISP` shadow byte path, with `BB00` as the source staged by the CD-side wrapper and `$45` as the direct-page trampoline handoff byte consumed by the installed NMI body.

I am still being careful about the final gameplay-facing subsystem noun of `BB00`, but the hardware-facing role in this local chain is now exact.

## 4. `7E:2C70..2C7B` is an exact BG1/BG2/BG3 scroll-shadow flush band
The installed trampoline writes these 12 bytes in exact order:

- `2C70,2C71 -> $210D,$210D`  (`BG1HOFS` pair)
- `2C72,2C73 -> $210E,$210E`  (`BG1VOFS` pair)
- `2C74,2C75 -> $210F,$210F`  (`BG2HOFS` pair)
- `2C76,2C77 -> $2110,$2110`  (`BG2VOFS` pair)
- `2C78,2C79 -> $2111,$2111`  (`BG3HOFS` pair)
- `2C7A,2C7B -> $2112,$2112`  (`BG3VOFS` pair)

That makes this band materially sharper than before:

> exact 12-byte WRAM shadow band for the committed `BG1/BG2/BG3` horizontal/vertical scroll register writes performed by the installed RAM NMI trampoline body.

This is now good enough to stop treating `2C70..2C7B` as anonymous WRAM.

## 5. `D1:F4C0` also proves the local machine-state contract around the wrapper
The front edge matters:

- `REP #$30` then full `A/X/Y/B/D` save
- `D = 0`
- `A = 0` (8-bit) then `STA.l $420C`
- `LDA.l $4210`
- `LDA #$A1 ; STA.l $4200`
- `STZ $47`

Even without naming the two helper calls yet, this already freezes the exact local contract:

- HDMA is disabled first via `$420C = 0`
- the interrupt side is acknowledged/read through `$4210`
- `$4200` is re-seeded to exact value `0xA1`
- only after that does the trampoline clear `$47` and continue into the helper/flush tail

So the strongest safe reading is:

> exact interrupt-entry stabilization prelude for the installed NMI body before the helper/flush tail runs.

## 6. The next seam is now obvious: `C0:0005 -> C0:0AFF..`
This pass did **not** overreach into the called helpers.

But it did freeze one very strong new dependency:

```text
D1:F4E2  JSL $C00005
D1:F4E6  STA $420C
```

And the low-bank bytes at `C0:0005` are exact:

```text
C0:0005  BRL $0AF7   ; lands at C0:0AFF
```

So the shortest next move is now:
1. follow `C0:0005 -> C0:0AFF`
2. freeze what exact byte comes back in `A`
3. settle the exact HDMA-enable-mask role behind `D1:F4C0 -> $420C`

That is cleaner than jumping sideways to `CD:09CE` or `CD:0C89` first.

## Completion-score correction
You were right to call out the percentage wobble.

The pass-104 **next-session note** said `~68.5%`, but the toolkit-generated weighted score report said `~68.3%`.

For pass 105, the toolkit-generated **`reports/ct_completion_score.md`** is the source of truth.
I am treating that generated report as authoritative and keeping the handoff note aligned to it from here forward.
