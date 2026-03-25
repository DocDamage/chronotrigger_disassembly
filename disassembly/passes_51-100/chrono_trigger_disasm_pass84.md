# Chrono Trigger Disassembly — Pass 84

## Scope of this pass
Pass 83 closed the **local behavior** of the `D1:F427 / F431 / F457` gate,
but one of the biggest remaining open questions was still external:

- who actually writes `7E:CFFF`
- whether `CFFF` is just a boolean or a wider selector byte
- how much of `CDC8 / CE0F / CE12` is real local phase state versus vague "pending" wording

This pass closes the first half of that gap.

The honest result is:

> `CFFF` is no longer an unmapped mystery selector.
> It has **exact mapped writers** in both runtime script systems.
>
> The auxiliary `CD:0018` VM has a direct immediate-write token at **`0xE6`**:
> `CD:18C2..18C7 = LDA [$40] ; STA $CFFF ; RTS`.
>
> The older primary slot-script VM also has exact tiny helpers that **force** the byte to
> `0x01` or `0x00`.
>
> And inside D1, the only local consumer is still the same one from pass 83:
> `D1:F426` treats `CFFF` strictly as a **zero vs nonzero mode byte**.

That means the strongest safe reading can now be tightened:

> `CFFF` is a **suspend/restore mode byte** for the D1 descriptor-header gate,
> not just a hypothetical abstract flag.
>
> Zero selects restore.
> Any nonzero value selects suspend.

This pass also tightens the neighboring control bytes:

- `CDC8` is now more clearly the **seed/promote phase-side byte** of the `E984 <-> E91A` half-cycle
- `CE0F` is now more clearly a **seed-side arm/epoch byte**, reset by init and incremented only by `E984` inside D1
- `CFFF / CE0F / CE12` are all explicitly cleared by the larger D1 reset cluster around `F220..F29C`

I am still **not** freezing the final gameplay-facing noun of the `2040/20A0/.../23A0` palette-band families,
and I am still **not** claiming that every nonzero `CFFF` value has a distinct live-mode meaning.
The code only proves **zero vs nonzero** so far.

---

## 1. `CFFF` now has an exact auxiliary-VM writer: token `0xE6`
The auxiliary token table at `CD:16B5` is a flat 16-bit pointer table.
Parsing the entries shows:

- table index `0x66`
- token `0x80 + 0x66 = 0xE6`
- handler address `CD:18C2`

The exact handler body at `CD:18C2..18C7` is:

```text
LDA [$40]
STA $CFFF
RTS
```

This is not a fuzzy wrapper and not a local side effect.
It is a direct streamed immediate write into the D1 gate byte.

### strongest safe reading
The strongest safe reading is:

> auxiliary token `0xE6` is the **direct stream-write token for `CFFF`**.
>
> Whatever byte follows in the auxiliary command stream is copied straight into `7E:CFFF`.

That is the first exact mapped runtime writer the project needed.

---

## 2. `CFFF` also has exact primary-script writers: hard set vs hard clear
The older primary slot-script VM has two exact tiny handlers in the `58D* / 58E*` cluster.

### 2a. `C1:58DB..58E3` forces `CFFF = 1`
The exact body is:

```text
LDA #$01
STA $CFFF
JMP $75BB
```

So this path unconditionally sets the mode byte nonzero and then returns through the standard VM tail.

### 2b. `C1:58E4..58EB` forces `CFFF = 0`
The exact body is:

```text
STZ $CFFF
LDA #$01
JMP $75BB
```

So this sibling unconditionally clears the mode byte and returns the same success code.

### strongest safe reading
The strongest safe reading is:

> the primary slot-script VM has explicit **set-suspend** and **clear-restore** helpers for `CFFF`.

That matters because it means `CFFF` is not owned by only one script language.
Both runtime VMs can drive it.

---

## 3. pass 83’s local D1 reading can now be tightened from “selector” to “mode byte”
Pass 83 already proved the local consumer:

```text
D1:F426
  LDA $CFFF
  BEQ restore_path
  JMP $F431   ; suspend/shadow path
restore_path:
  JMP $F457   ; restore path
```

With the new mapped writers in hand, three things are now exact enough to say plainly.

### 3a. the D1 code does **not** distinguish among nonzero values
The D1 branch is a plain `BEQ` test.
That means:

- `00` -> restore path
- any nonzero byte -> suspend path

So even though the auxiliary token can write any immediate value, the local D1 gate only consumes it as a **zero/nonzero mode**.

### 3b. the primary VM’s hardcoded `1` and `0` are clean convenience shorthands
The older VM helpers fit perfectly:

- `58DB` -> force nonzero -> suspend path
- `58E4` -> force zero -> restore path

### 3c. the auxiliary token is the more general writer
Because token `0xE6` writes the raw streamed byte,
it is the more general form of the same control.

### strongest safe reading
The strongest safe reading is:

> `CFFF` is a **D1 suspend/restore mode byte**.
>
> It is externally writable by both script systems,
> but locally consumed only as **zero = restore, nonzero = suspend**.

That is stronger and more honest than the old “some selector” wording.

---

## 4. `CFFF`, `CE0F`, and `CE12` are all explicitly cleared by the D1 reset cluster
The pass-83 discussion mostly focused on the active helpers.
But the larger D1 reset cluster around `F220..F29C` gives an important state-anchor.

The exact writes in the `F260..F297` subsection include:

```text
STX $CE0A
STX $CE0C
STX $CE19
STZ $CE0E
STZ $CE0F
STZ $CE10
STZ $CE15
STZ $CE12
...
STZ $CFFF
```

This is important for two reasons.

### 4a. these bytes are part of one real control family
They are not random globals.
They are explicitly grouped in one reset pass.

### 4b. `CFFF` is not persistent across this D1 reset/init step
Any runtime script that wants the suspend path later has to write it again.

### strongest safe reading
The strongest safe reading is:

> `CFFF`, `CE0F`, and `CE12` belong to the same real D1-side control cluster,
> and all three are explicitly reset by the larger D1 cluster initializer.

---

## 5. `CDC8` can now be tightened one notch further
Inside D1, the exact opcode references are now small enough to reason about safely.

For `CDC8`, the only exact D1-side touches are:

- `D1:E984` -> `INC $CDC8`
- `D1:E97D` -> `STZ $CDC8`

And pass 82 already proved the surrounding high-level behaviors:

- `E984` is the **seed-and-snapshot** half
- `E91A` is the **promote-and-restore** half

So locally, `CDC8` is not a vague generic latch anymore.
It is attached specifically to the **seed side** of that half-cycle and cleared by the promote side.

### strongest safe reading
The strongest safe reading is:

> `CDC8` is the local **seed-vs-promote phase byte** for the first 48-color palette-band half-cycle.

I am still avoiding a final gameplay-facing noun because I do **not** yet have the exact external reader.
But the local phase relationship is now strong.

---

## 6. `CE0F` can also be tightened locally, but more cautiously than `CDC8`
For `CE0F`, the exact D1-side touches are:

- `D1:E987` -> `INC $CE0F`
- `D1:F26E` -> `STZ $CE0F`

That is more limited than `CE12`, because there is still no exact D1-side reader in the current pass set.

But it is still enough to say something tighter than the old wording.

### 6a. `CE0F` is strictly on the seed side locally
Within D1, it is only raised by `E984`, not by `E91A`.

### 6b. it is part of the same reset cluster as `CFFF` and `CE12`
So it is definitely a real sibling state byte, not detached scratch.

### strongest safe reading
The strongest safe reading is:

> `CE0F` is a **seed-side arm/epoch byte** in the same D1 control cluster.
>
> It is reset by the cluster initializer and incremented by the seed/snapshot helper,
> but its exact external consumer is still open.

That is more grounded than “generic count or latch,” but still honest about the missing reader.

---

## 7. what this pass actually closes
This pass closes three real unknowns from the pass-83 handoff.

### closed now
1. the project now has an **exact mapped runtime writer** for `CFFF`:
   - auxiliary token `0xE6` at `CD:18C2`
2. the project also has exact **hard set / hard clear** writers in the primary slot VM:
   - `C1:58DB`
   - `C1:58E4`
3. `CFFF` can now be called a **mode byte** rather than a vague selector
4. `CDC8` can now be treated locally as the **seed/promote phase-side byte**
5. `CE0F` can now be treated locally as the **seed-side arm/epoch byte**
6. the reset/init cluster explicitly groups and clears `CFFF / CE0F / CE12`

### still open
- whether auxiliary token `0xE6` ever uses distinct nonzero meanings at runtime, or only `00/01`
- the final human-facing noun of the `2040/20A0/2120/21A0/2240/22A0/2320/23A0` families
- the exact external consumer(s) of `CDC8` and `CE0F`
- why the suspend path spares signed `0x8x` descriptor headers while clearing positive `0x1x`
- the final live role of `A101`, `2A21.bit1`, and the `0575.bit6` toggle around `D1:E70A`

---

## Best next move after this pass
The best next seam is no longer “find *any* writer for `CFFF`.”
That part is done.

The best next move is:

1. confirm whether token `0xE6` uses only `00/01` in real runtime streams or can carry multiple live nonzero modes
2. find the actual external reader(s) of `CDC8` and `CE0F`
3. explain the intentional split between positive `0x1x` and signed `0x8x` descriptor headers in the suspend path
4. continue freezing the late auxiliary token band around `0xE3..0xE8`, since that cluster is now clearly part of the same control neighborhood
