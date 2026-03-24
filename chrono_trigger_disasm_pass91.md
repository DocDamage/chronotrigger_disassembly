# Chrono Trigger Disassembly — Pass 91

## Scope of this pass
Pass 90 finally froze the caller-side D1 contract, but it still left the downstream tail as three raw addresses:

- `CE:EE6E`
- `CD:0235`
- `C0:0008`

This pass closes that seam materially by freezing the first exact CE stage, the exact CD-side workspace clear behind its veneer, and the exact C0-side veneer plus its real target routine.

The strongest keepable result is:

> `CE:EE6E..EF0D` is a real selector/side-driven **nine-record template seeder** into `C867..C9EC`.
>
> `CD:0235..0238` is just an exact veneer, and `CD:0239..025D` is the exact **eight-strip `B400..B7FF` workspace clear** behind it.
>
> `C0:0008..000A` is just an exact veneer to `C0:1BAB`, and `C0:1BAB..1BE5` is a real **conditional one-packet `C7:0004` submit helper** selected by `2A1F.bit6`.

That is enough to materially tighten the four-stage follow-up chain pass 90 identified.

---

## 1. `CE:EE6E..EF0D` is the first exact external follow-up stage
The entry is exact and small enough to freeze structurally without bluffing:

```text
PHB
ASL A
TAX
REP #$20
LDA CE:F24E,X
TAX
```

So entry `A` is doubled and used to index the exact word table at `CE:F24E`, and the fetched word becomes an exact byte offset into a second flat record family.

### 1a. exact source-record shape
The second table family begins at `CE:F58E`.

The copy logic proves one source record is exactly **10 words** (`0x14` bytes) wide, because the routine consumes the following exact fields from `CE:F58E + offset`:

- `+0x00`
- `+0x02`
- `+0x04`
- `+0x06`
- `+0x08`
- `+0x0A`
- `+0x0C` **or** `+0x12`, chosen by `2A21.bit0`
- `+0x0E`
- `+0x10`

That is 9 copied source offsets taken from one 10-word record.

### 1b. exact copy pattern
The routine pushes the later source offsets on stack, loads the first live source offset into `X`, and then performs 9 exact block copies using `MVN` from bank `CE` to bank `7E`.

Each copy is seeded with:

```text
LDA #$001D
MVN 7E, CE
```

So each transfer copies exactly **`0x1E` bytes**.

The exact destination roots are:

- `C867`
- `C894`
- `C8C1`
- `C8EE`
- `C91B`
- `C948`
- `C975`
- `C9A2`
- `C9CF`

Those roots are spaced by an exact stride of `0x2D` bytes.

### strongest safe reading
> `CE:EE6E..EF0D` is an exact **selector/side-driven template-record seeder** for the 9-record `C867..C9EC` workspace.

That is the first exact external stage behind pass 90’s D1 orchestrator.

---

## 2. `CD:0235` is only a veneer; `CD:0239` is the real workspace clear
Pass 90 knew `D1:F331..F410` hit `CD:0235`, but the exact body was still open.

### 2a. exact veneer body
`CD:0235..0238` is just:

```text
JSR $0239
RTL
```

So the real work begins at `CD:0239`.

### 2b. exact body at `CD:0239..025D`
This helper is fully frozen from raw bytes:

```text
REP #$20
TDC
LDX #$0080
loop:
  STA $B3FE,X
  STA $B47E,X
  STA $B4FE,X
  STA $B57E,X
  STA $B5FE,X
  STA $B67E,X
  STA $B6FE,X
  STA $B77E,X
  DEX
  DEX
  BNE loop
SEP #$20
RTS
```

Because `A` is zeroed by `TDC`, this is an exact zero-fill.

The exact spans cleared are:

- `B400..B47F`
- `B480..B4FF`
- `B500..B57F`
- `B580..B5FF`
- `B600..B67F`
- `B680..B6FF`
- `B700..B77F`
- `B780..B7FF`

So the helper clears one exact contiguous `0x0400`-byte workspace expressed as 8 adjacent `0x80`-byte strips.

### strongest safe reading
> `CD:0239..025D` is the exact **contiguous eight-strip `B400..B7FF` workspace clear helper** immediately upstream of the final low-bank follow-up stage.

---

## 3. `C0:0008` is only a veneer to `C0:1BAB`
The low-bank entry itself is exact and tiny:

```text
C0:0008  BRL $1BA0
```

So `C0:0008` lands at exact target `C0:1BAB`.

That means the pass-90 tail is not “JSL some giant C0 blob.”
It is a direct branch veneer to one specific low-bank helper.

---

## 4. `C0:1BAB..1BE5` is a conditional one-packet `C7:0004` submit helper
The target routine is exact enough to freeze structurally.

### 4a. exact prologue
It begins with:

```text
PHB
PHD
REP #$20
LDA #$0100
TCD
SEP #$20
PHA
PLB
```

So it saves `B/D`, sets `D = 0x0100`, and sets `DB = 0x00`.

### 4b. exact branch condition
Then it reads the exact live state byte `7E:2A1F` and branches on bit `0x40`:

```text
LDA.l $7E2A1F
BIT #$40
BNE alt
```

### 4c. exact packet when bit 6 is clear
If `2A1F.bit6 == 0`, it writes the following exact packet fields before calling `C7:0004`:

```text
LDA #$FF
STA $1E10
LDA $FA
STA $1E01
LDA #$14
STA $1E00
JSL C7:0004
```

I am keeping the noun of `$FA` conservative here: it is the exact direct-page byte read after `D = 0x0100`.

### 4d. exact packet when bit 6 is set
If `2A1F.bit6 != 0`, it instead does:

```text
LDA #$01
STA $1E01
LDA #$70
STA $1E00
JSL C7:0004
```

### 4e. exact epilogue
Then it restores `D` and `B` and returns via `RTL`.

### strongest safe reading
> `C0:1BAB..1BE5` is an exact **conditional one-packet `C7:0004` submit helper** behind the `C0:0008` veneer.

That is enough to materially tighten the last stage of the pass-90 follow-up chain without pretending we already know the final engine-facing noun of `C7:0004`.

---

## 5. What this pass changes in the larger chain
Pass 90 had this exact tail:

```text
CE:EE6E -> D1:F83D -> CD:0235 -> C0:0008
```

Pass 91 tightens that into:

```text
CE:EE6E = seed 9 exact template records into C867..C9EC
D1:F83D = seed exact C030..C14F quartet family
CD:0235 = clear exact contiguous B400..B7FF eight-strip workspace
C0:0008 = branch to exact conditional one-packet C7:0004 submit helper
```

That is a real upgrade in caller-contract fidelity even though the final presentation/effect noun is still one step away.

---

## Honest cautions still kept explicit
Even after this pass:

- I have **not** frozen the final gameplay-facing noun of the broader pass-88/89 lane+raster workspace.
- I have **not** frozen the final gameplay-facing noun of the `C867..C9EC` template-record workspace.
- I have **not** frozen the exact role of `C7:0004`; this pass only freezes the exact packet-submit helper behind `C0:0008`.
- I have **not** returned to the first exact clean-code external reader of `CE0F` yet.

---

## Best next move after pass 91
Do **not** go broad.

The best next seam now is:

1. **Freeze `CD:025E..028F` next**
   - it sits immediately after the newly-frozen `B400..B7FF` clear helper
   - it seeds exact `020C / 0210 / 0212 / 0214` locals and immediately calls `C2:0003 / C2:0009 / 3E7D`
   - that is now the shortest route to turning the CD follow-up side into a stronger noun

2. **Freeze `C0:000B` / `C0:1BE6` as the sibling low-bank follow-up**
   - `C0:0008` is now pinned as a veneer to `1BAB`
   - the sibling veneer at `000B` lands at `1BE6` and is clearly part of the same low-bank packet/submit cluster

3. **Only after those are tighter, return to `CE0F`**
   - the downstream tail is now a cleaner bottleneck than the remaining `CE0F` ambiguity
