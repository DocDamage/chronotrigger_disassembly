# Chrono Trigger (USA) — Disassembly Pass 3

## What this pass focused on

This pass pushed past the earliest boot scaffolding into the first real **descriptor-driven initialization path**.

The important change is that the code at **`$C0:0082`** is no longer just “some startup calls.” It is now clearly a staged initialization chain that:

1. resets a large block of runtime state,
2. selects a **14-byte descriptor** from a table in bank **`F6`**,
3. runs a group of resource/data loaders based on that descriptor,
4. clears low WRAM working buffers,
5. initializes and services a **VRAM DMA queue**.

---

## Previously confirmed anchors still in play

From prior passes, these remain solid:

- **`$00:FF00`** — emulation-mode reset stub
- **`$FD:C000`** — low-level CPU / hardware bootstrap
- **`$C0:000E`** — first main boot stage
- **`$C0:0B4E`** — blank screen / disable interrupts / DMA / HDMA
- **`$C0:0B64`** — install NMI RAM trampoline at `$00:0500`
- **`$C0:0B75`** — install IRQ RAM trampoline at `$00:0504`
- **`$C0:2DF1`** — WRAM zero-fill via DMA using the Mode 7 multiplier result register as a constant-zero source

---

## New confirmed routine meanings

## `$C0:0B86` — Reset_MainRuntimeState

This routine is the first real state initializer after the boot chain switches into the `$0100` direct page.

Confirmed behavior:

- copies incoming values from `$00/$02/$04` into working state at `$0A/$0C/$0E`
- clears a large set of direct-page globals (`$10`, `$11`, `$17`, `$18`, `$38`, `$0F`, `$19`, `$BC`, `$53`, `$26`, `$29`, `$2F`, `$2D`, `$30`, `$44`, `$45`, `$46`, `$5F`, `$78`, `$BB`, `$62`, `$39`, `$54`, `$2B`, etc.)
- seeds several working pointers / limits:
  - `$7D = $0900`
  - `$7F = $0770`
  - `$7B = $08A0`
- seeds repeated default bytes:
  - `$B1/$B4/$B7/$BA = $E4`
- seeds runtime flags:
  - `$1F = $01`
  - `$20 = $01`
  - `$68 = $05`
  - `$28 = $5F`
- loads 16-bit values from bank **`E4:FFE0+`** into `$AF/$B2/...`

Best current name:

**`Reset_MainRuntimeState`**

That name is grounded: this routine is absolutely a global state reset / seed step, not a renderer or gameplay loop.

---

## `$C0:092B` — Select_InitDescriptor_14Byte

This routine computes the selector used by the next loader group.

Confirmed behavior:

- uses DP values **`$00`** and **`$01`**
- multiplies the low selector (`$00`) by **`0x0E`** using the SNES hardware multiplier (`$4202/$4203`, result at `$4216`)
- if bit 0 of `$01` is set, it adds **`$0E00`**
- stores the final 16-bit result in **`$FE`**

So the formula is effectively:

```text
FE = (0x0E * $00) + (($01 & 1) ? 0x0E00 : 0)
```

That makes **`$FE`** a descriptor offset into a table whose entries are **14 bytes each**.

Best current name:

**`Select_InitDescriptor_14Byte`**

This is a concrete, not speculative, finding.

---

## `$C0:00F4` — Run_InitDescriptorLoaders

This routine is the first clearly structured **descriptor-driven init group**.

Confirmed call sequence:

```asm
$C0:00F4  JSR $092B
$C0:00F7  JSR $1B53
$C0:00FA  JSR $0960
$C0:00FD  JSR $6DCF
$C0:0100  JSR $7084
$C0:0103  JSR $7F7E
$C0:0106  JSR $A33B
$C0:0109  JSR $09DD
$C0:010C  JSR $0A14
$C0:010F  JSR $56D4
$C0:0112  JSL $FD:FFFA
$C0:0116  JSL $FD:FFF4
$C0:011A  RTS
```

This is not a random chain. It is a compact loader phase driven by the descriptor selected into `$FE`.

Best current name:

**`Run_InitDescriptorLoaders`**

---

## `$C0:B192` — Clear_1B00_WordTable_ThenBranchE935

This routine was previously unlabeled. It is now much clearer.

Confirmed behavior:

- sets **direct page = `$1B00`**
- switches A/X/Y to 8-bit where needed
- reads a count from **`$7F:2000`**
- zeroes a sequence of **2-byte entries** starting at DP base (`STX $00,Y`, then `INY`, `INY`)
- repeats until the count is exhausted
- restores 16-bit index state
- branches to **`$C0:E935`**

Best current name:

**`Clear_1B00_WordTable_ThenBranchE935`**

What is still unknown is the semantic identity of the table itself, but the mechanics are now clear: it is a counted word-table clear.

---

## `$C0:B1B2` — Process_VramDmaQueue

This routine is now strong enough to name with confidence.

Confirmed behavior:

- sets **direct page = `$0900`**
- configures **DMA channel 7** for **VRAM transfer**
  - `$2115 = $80`
  - `$4371 = $18` (B-bus target = `$2118` / VRAM data)
  - `$4370 = $01`
  - `$4374 = $7F`
- loops over queue entries indexed by X in 2-byte steps
- tests **`$A0,X`** as the active/terminator flag
- for each active entry, performs **two DMA transfers** using the per-entry arrays:
  - VRAM dest 1: `$50,X`
  - source addr 1: `$40,X`
  - length 1: `$80,X`
  - VRAM dest 2: `$70,X`
  - source addr 2: `$60,X`
  - length 2: `$90,X`
- triggers each transfer with `$420B = $80`
- when done, clears `$A0` and returns

Best current name:

**`Process_VramDmaQueue`**

This is now one of the strongest routine IDs in the project.

---

## `$C0:7F7E` — Clear_LowWram_1D00_1DFF

This routine is short and fully confirmed.

Behavior:

- sets direct page to `$0100`
- programs the zero-fill helper
- clears:
  - **`$00:1D00-$00:1DFF`**

Because low bank addresses `$0000-$1FFF` are WRAM mirrors on SNES, this is a low-WRAM working-buffer clear.

Best current name:

**`Clear_LowWram_1D00_1DFF`**

---

## Descriptor-driven loader group: what is solid vs what is still provisional

These routines all depend on the descriptor offset in `$FE` and pull selector bytes from bank `F6`:

- **`$C0:0960`** uses **`F6:0001`**
- **`$C0:6DCF`** uses **`F6:0002`**
- **`$C0:7084`** uses **`F6:0003`**
- **`$C0:A33B`** uses **`F6:0004`**
- **`$C0:56D4`** uses **`F6:0008`**
- **`$C0:0A14`** also uses **`F6:0002`**

What is confirmed:

- these are **descriptor-indexed loaders**
- several of them build a source pointer into `$0300-$0302` and destination pointer into `$0303-$0305`
- then call **`$C3:0002`**, which is almost certainly a generic transfer / decompression / block-load dispatcher
- **`$C0:7084`** repeatedly copies **`0x001D`**-byte chunks from a table near **`F6:24C0+`** into WRAM starting around **`$7E:2022`**
- **`$C0:A33B`** loads data to **`$7E:B500+`** and immediately interprets bytes there as runtime flags / metadata
- **`$C0:56D4`** loads from bank **`FC:F9F0+`** into WRAM at **`$7F:2000+`**

What is *not* yet safe to claim:

- exact semantic names like “map loader,” “battle setup,” “location header,” “sprite metadata,” etc.

So the honest takeaway is:

**the structure is now real, but some content names are still provisional.**

---

## Strong new control-flow picture

The startup path now looks like this:

```text
Reset_Stub_Emu
 -> HwInit_Bootstrap
 -> MainBoot_Stage1
 -> Reset_MainRuntimeState
 -> Run_InitDescriptorLoaders
 -> Process_VramDmaQueue
 -> additional runtime init / loop setup
```

That is a meaningful improvement over the previous pass.

---

## Best current labels after this pass

- `$C0:0B86` — `Reset_MainRuntimeState`
- `$C0:092B` — `Select_InitDescriptor_14Byte`
- `$C0:00F4` — `Run_InitDescriptorLoaders`
- `$C0:B192` — `Clear_1B00_WordTable_ThenBranchE935`
- `$C0:B1B2` — `Process_VramDmaQueue`
- `$C0:7F7E` — `Clear_LowWram_1D00_1DFF`

Provisional / guarded labels:

- `$C3:0002` — `Generic_BlockTransferDispatcher` *(provisional)*
- `$C0:0960` — `DescriptorLoader_Group_0001` *(provisional)*
- `$C0:6DCF` — `DescriptorLoader_Group_0002A` *(provisional)*
- `$C0:0A14` — `DescriptorLoader_Group_0002B` *(provisional)*
- `$C0:7084` — `DescriptorLoader_Group_0003_RecordCopy` *(provisional)*
- `$C0:A33B` — `DescriptorLoader_Group_0004_Metadata` *(provisional)*
- `$C0:56D4` — `DescriptorLoader_Group_0008` *(provisional)*

---

## What the next pass should do

1. Disassemble enough of **`$C3:0002`** to prove whether it is plain block copy, decompression, or a command dispatcher.
2. Follow **`$C0:7084`** and the **`F6:24C0`** records far enough to identify what those 0x1D-byte repeated records actually are.
3. Resolve **`$C0:E935`** well enough to rename the table cleared by **`$C0:B192`**.
4. Decide whether **`$C0:1B53`** is event/script/UI dispatch or another resource-loader front end.

That is the cleanest next cut.
