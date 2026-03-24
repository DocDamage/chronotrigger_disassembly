# Next Session Start Here

Latest completed pass: **105**

## What pass 105 actually closed
Pass 105 stayed on the installed RAM-trampoline seam opened by pass 104 and froze the full exact body at `D1:F4C0..F55A`.

The strongest keepable results are:

- `D1:F4C0..F55A` is now exact
  - saves `A/X/Y/B/D`
  - sets `D = 0`
  - disables HDMA via exact zero write to `$420C`
  - reads `$4210`
  - writes exact `0xA1` to `$4200`
  - clears `$47`
  - calls `CD:09CE`
  - calls `C0:0005` and writes its return byte directly to `$420C`
  - flushes `$45 -> $2100`
  - flushes `7E:2C70..2C7B -> $210D..$2112`
  - calls `CD:0C89`
  - calls `FD:FFF7`
  - restores state and returns with exact `RTI`
- strongest safe reading: exact installed RAM NMI trampoline body for this local launcher contract

- `00:0045` is now exact enough to stop calling it anonymous DP scratch
  - pass 104 froze `BB00 -> $45`
  - pass 105 froze `$45 -> $2100`
- strongest safe reading: exact direct-page handoff byte for the trampoline-side `INIDISP` flush

- `7E:BB00` is now materially tighter
  - exact local path is `BB00 -> $45 -> $2100`
- strongest safe reading: staged source byte for the display-control / `INIDISP` flush path in this chain

- `7E:2C70..7E:2C7B` is now exact enough for a real noun
  - this 12-byte band is flushed in exact order to `BG1/BG2/BG3` scroll regs `$210D..$2112`
- strongest safe reading: exact BG1/BG2/BG3 scroll-shadow byte band committed by the installed trampoline body

- `C0:0005..0007` is now exact as a veneer
  - `BRL $0AF7`
  - lands at exact target `C0:0AFF`
  - its return value is written directly to `$420C` by `D1:F4C0`
- strongest safe reading: low-bank helper veneer whose returned byte is the next unresolved exact `$420C` mask/value seam

## What this means semantically
The honest static picture is now:

- `0501/0503 -> D1:F4C0` does **not** point at a generic helper
- it points at the actual installed RAM **NMI trampoline body** in this launcher path
- `$47` is no longer just “a latch the wrapper waits on”
  - it is the exact one-shot completion latch cleared by entry into the installed trampoline body
- `$45 -> $2100` is now a real hardware-facing display-control flush path
- `2C70..2C7B` is now a real committed BG scroll-shadow band

## Best next seam
Do **not** reopen `D1:F4C0` itself unless new evidence appears.

The cleanest next move is:

1. stay on the exact trampoline body we just froze
2. follow **`C0:0005 -> C0:0AFF..`**
3. specifically freeze:
   - what exact byte comes back in `A`
   - why `D1:F4C0` writes that byte directly to `$420C`
   - whether this is the exact HDMA-enable mask/value producer for the installed NMI body

That is cleaner than jumping sideways to `CD:09CE` or `CD:0C89` first, because `C0:0005` is now the shortest unresolved exact edge inside the trampoline itself.

## Completion estimate after pass 105
Use the toolkit-generated weighted report as the source of truth.

Conservative project completion estimate: **~68.7%**

Still true:
- semantic/control coverage is ahead of rebuild readiness
- the expensive endgame is still bank separation, decompressor/data grammar work, runtime-backed WRAM proof, source lift, and rebuild validation
