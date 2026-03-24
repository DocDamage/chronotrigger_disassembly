# Chrono Trigger Disassembly — Pass 92

## Scope of this pass
Pass 91 froze the four-stage downstream tail enough to stop treating it like three raw addresses, but it still left the next two exact follow-up helpers open:

- `CD:025E..`
- `C0:000B / C0:1BE6..`

This pass closes that seam materially.

The strongest keepable result is:

> `CD:025E..0295` is an exact shared **selector/workspace setup helper** that seeds the `020C..0214` call packet, clears the exact `B400..B7FF` workspace through `0239`, then runs the exact pair `C2:0003 -> C2:0009`, double-runs local helper `3E7D`, and finally arms `CCEC` and `CA24`.
>
> `C0:000B..000D` is just an exact veneer to `C0:1BE6`.
>
> `C0:1BE6..1CFB` is an exact gated **multi-packet `C7:0004` submit helper** whose default 5-packet body has one exact alternate second packet selected only when `7F:01EC == 1` and `2A1F.bit5` is clear; if `2A1F.bit6` is set it collapses to the same one-packet `0x70` path already seen at `1BAB`.

That materially tightens the remaining downstream bottleneck without pretending the final engine-facing noun of `C2:0003`, `C2:0009`, or `C7:0004` is solved.

---

## 1. `CD:025E..0295` is the shared CD-side setup helper behind the newly-frozen clear stage
Pass 91 froze `CD:0235..025D`, but the immediately-following helper at `025E` was still just a target note.

This pass freezes it exactly enough to stop calling it a raw address.

### 1a. exact entry-side writes
The helper begins by seeding an exact local call/workspace packet:

```text
STA $020C
STZ $CCED
STZ $02A1
LDX #$B400
STX $0210
LDA #$007E
STA $0212
STZ $0214
```

So the exact live packet/workspace family touched at entry is:

- `020C`
- `0210`
- `0212`
- `0214`
- plus local clears of `CCED` and `02A1`

### 1b. exact clear + external pair
It then runs the exact clear helper pass 91 already froze and immediately calls the exact C2 pair:

```text
JSR $0239
JSL C2:0003
LDA #$6040
STA $0213
JSL C2:0009
```

So `CD:025E` is not incidental cleanup after `0239`.
It is the exact setup helper that:

- seeds the packet/workspace family
- clears `B400..B7FF`
- invokes `C2:0003`
- then seeds `0213 = 0x6040`
- then invokes `C2:0009`

### 1c. exact local tail
After the two external calls it runs the same local helper twice and arms the local state bytes before returning:

```text
JSR $3E7D
JSR $3E7D
LDA #$0010
STA $CCEC
INC $CA24
RTS
```

### 1d. exact call-site shape
This helper is shared, not one-off.
The clean in-bank callsites include:

- `CD:01D2`
- `CD:0222`
- `CD:02AD`
- `CD:02FF`
- `CD:032F`

That is enough to promote it beyond “the helper after `0239`.”

### strongest safe reading
> `CD:025E..0295` is a shared **selector/workspace setup helper** that seeds the `020C..0214` call packet, clears `B400..B7FF`, runs the exact `C2:0003 -> C2:0009` pair, double-runs local helper `3E7D`, then arms `CCEC` and `CA24`.

---

## 2. `C0:000B` is only a veneer to `C0:1BE6`
The sibling low-bank entry is exact and tiny.

Its full body is just:

```text
BRL $1BD8
```

So `C0:000B..000D` lands at exact target:

- `C0:1BE6`

That means pass 91’s guess was right: `000B` really is the sibling veneer in the same low-bank packet/submit cluster as `0008 -> 1BAB`.

---

## 3. `C0:1BE6..1CFB` is a gated multi-packet `C7:0004` submit helper
This sibling helper is not another tiny one-packet wrapper.
It is a real gated packet sequence builder.

### 3a. exact shared prologue
Like `1BAB`, it saves state, sets `D = 0x0100`, and sets `DB = 0x00`:

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

### 3b. exact special-case gate before the main packet path
The first gate reads exact live byte `7F:01EC` and only treats the exact value `1` specially:

```text
LDA.l $7F01EC
BEQ main
DEC A
BEQ special_check
DEC A
BRA main
```

Only when the original value was exactly `1` does execution reach the extra check:

```text
LDA.l $7E2A1F
BIT #$20
BNE main
BRL $1C90
```

So the exact alternate packet body at `1C90` is selected **only when**:

- `7F:01EC == 1`
- and `2A1F.bit5 == 0`

All other cases fall through to the default packet path at `1C09`.

### 3c. exact default main-path gate on `2A1F.bit6`
The default path begins with:

```text
LDA.l $7E2A1F
BIT #$40
BNE one_packet_70
```

So this sibling helper shares the same `bit6` split already seen at `1BAB`.

If `2A1F.bit6 != 0`, it collapses to the exact one-packet path:

```text
LDA #$00 : STA $1E01
LDA #$70 : STA $1E00
JSL C7:0004
```

then restores `B/D` and returns.

### 3d. exact default 5-packet sequence when `2A1F.bit6 == 0`
If `bit6` is clear and the special-case branch was not taken, `1BE6` submits the following exact 5-packet sequence through repeated `JSL C7:0004`:

1. packet A
   - `1E10 = 0x00`
   - `1E01 = 0x00`
   - `1E02 = 0x00`
   - `1E03 = 0xFF`
   - `1E00 = 0x81`

2. packet B (default form)
   - `1E01 = [7E:29AE]`
   - `1E00 = 0x11`

3. packet C
   - `1E01 = 0x40`
   - `1E02 = 0xFF`
   - `1E03 = 0xFF`
   - `1E00 = 0x81`

4. packet D
   - `1E01 = 0x00`
   - `1E02 = 0xFF`
   - `1E00 = 0x82`

5. packet E
   - `1E01 = 0x00`
   - `1E02 = 0xFF`
   - `1E00 = 0x83`

Then it restores `B/D` and returns.

### 3e. exact alternate 5-packet sequence at `1C90`
When the exact special-case gate fires (`7F:01EC == 1` and `2A1F.bit5 == 0`), the same surrounding structure is kept, but the second packet changes.

The exact alternate sequence is:

1. packet A
   - `1E10 = 0x00`
   - `1E01 = 0x00`
   - `1E02 = 0x00`
   - `1E03 = 0xFF`
   - `1E00 = 0x81`

2. packet B (alternate form)
   - `1E01 = 0x26`
   - `1E00 = 0x14`

3. packet C
   - `1E01 = 0x80`
   - `1E02 = 0xFF`
   - `1E03 = 0xFF`
   - `1E00 = 0x81`

4. packet D
   - `1E01 = 0x00`
   - `1E02 = 0xFF`
   - `1E00 = 0x82`

5. packet E
   - `1E01 = 0x00`
   - `1E02 = 0xFF`
   - `1E00 = 0x83`

Then it restores `B/D` and returns.

### strongest safe reading
> `C0:1BE6..1CFB` is a gated **multi-packet `C7:0004` submit helper** whose default 5-packet sequence has one exact alternate second packet selected only when `7F:01EC == 1` and `2A1F.bit5` is clear; if `2A1F.bit6` is set it collapses to the same one-packet `0x70` path already seen at `1BAB`.

---

## 4. What this changes structurally
Before pass 92, the project had:

- exact D1-side local orchestrator / build helpers
- exact CE template-record seeder
- exact CD clear veneer + clear body
- exact C0 one-packet submit helper behind `0008`

After pass 92, the remaining downstream bottleneck is much narrower:

- `CD:025E` is no longer a raw address after `0239`; it is a shared exact setup helper with a real packet/workspace contract
- `C0:000B` is no longer a guessed sibling entry; it is an exact veneer to `1BE6`
- `C0:1BE6` is no longer an unknown low-bank neighbor; it is a real gated multi-packet submit helper with one exact special-case path

That means the tail is now bottlenecked much more directly by the still-unfrozen engine-facing nouns of:

- `C2:0003`
- `C2:0009`
- `C7:0004`

rather than by the local staging addresses themselves.

---

## Honest caution kept explicit
Even after this pass:

- I have **not** frozen the final gameplay-facing noun of the broader pass-88/89 lane+raster workspace.
- I have **not** frozen the exact engine-facing role of `C2:0003`.
- I have **not** frozen the exact engine-facing role of `C2:0009`.
- I have **not** frozen the exact engine-facing role of `C7:0004`; pass 91 + pass 92 now freeze the local packet builders and submit sequences around it, not the final subsystem noun.
- I have **not** returned to the first exact clean-code external reader of `CE0F` yet.

---

## Best next seam after pass 92
Do **not** go broad.

The cleanest next move now is:

1. **Freeze `C2:0003` and `C2:0009` next**
   - `CD:025E` now proves they sit directly behind an exact shared packet/workspace setup helper
   - that makes them the cleanest remaining external bottleneck on the CD side

2. **Freeze `C7:0004` from the packet-consumer side**
   - pass 91 and pass 92 now prove multiple exact packet builders around it
   - the next win is turning “packet submitter” into the actual subsystem noun if the downstream body permits it

3. **Only after that, revisit `CE0F`**
   - the external bottleneck around the lane/raster tail is now cleaner than the remaining `CE0F` ambiguity
