# Next Session Start Here

Latest completed pass: **109**

## What pass 109 actually closed
Pass 109 reopened the old low-bank `0128 -> $420C` seam from the raw ROM bytes and corrected a misleading assumption that had been hiding in the old continuity wording.

The strongest keepable results are:

- the old `AE2B/AE33` seam is now **closed**
  - it sits inside an exact forced-blank shutdown loop
  - that loop clears:
    - `$4200`
    - `$420B`
    - `$420C`
    - `0128`
    - `$212C`
    - `$212D`
    - `$2121`
  - then seeds a CGRAM color from `X`, restores `$4200 = 0x81` and `$2100 = 0x0F`, unmasks IRQs, and spins forever
  - so that path is a **forced-zero mirror**, not the general nonzero owner of `0128`

- `EC00..EC5D` is now exact as the low-bank interrupt/service tail that:
  - calls selected helper families from `7B`
  - sets `D = 0x0100`
  - `JSL FD:C1EE`
  - `STZ 52`
  - `JSL C2:8002`
  - flushes:
    - `0BD9 -> $2123`
    - `0BDA -> $2124`
    - `0BDB -> $2125`
    - `0BDC -> $2128`
    - `0BDD -> $2129`
    - `0BDE -> $2130`
    - `0121 -> $2132`
    - `0128 -> $420C`
  - conditionally forces `$2100 = 0x80`
  - returns by `RTI`

- `EC74..ECA3` is now exact as a channel-7 VRAM DMA helper
  - source: `7E:D800`
  - destination VRAM address: `0BE5`
  - length: `0BE7`

- `ECA4..ECCB` is now exact as a channel-7 OAM DMA helper
  - zeroes OAM address
  - uploads `0x0220` bytes from `000700` to OAM

- `ECCC..ED13` is now exact as the IRQ-side HBlank wait / force-blank / HDMA-off wrapper
  - gates on `010F` and `$4211`
  - waits for HBlank through `$4212.bit6`
  - force-blanks via `$2100 = 0x80`
  - disables HDMA via `$420C = 0`
  - branches on `0153.bit0`
    - clear -> `JSR ED15`
    - set -> `JSL FD:FFFD`
  - restores registers and `RTI`

## What this means semantically
The direct low-bank `0128` picture is now cleaner:

- `0128` is still the HDMA-enable shadow byte
- `EC00..EC5D` is the exact low-bank **commit tail**
- the old `AE2B/AE33` pair is only a **forced-zero shutdown path**
- so the live seam is no longer “what is `0128`?” or “does AE33 own it?”
- the live seam is now:

> which exact branch body between `ED15` and `FD:FFFD -> FD:E022` rebuilds or mutates the nonzero display/HDMA shadow state before the next `EC00..EC5D` flush tail commits it?

## Best next seam
Go directly to the split just proven in pass 109:

### Preferred continuation
- decode `C0:ED15..`
- decode `FD:FFFD -> FD:E022`
- compare what each side updates
- determine whether the split is:
  - two buffer-side implementations
  - two transfer methods
  - or two distinct render/update modes

### Secondary continuation
After `ED15 / FD:E022` are harder:
- revisit the contiguous shadow block:
  - `0BD9..0BDE`
  - `0121`
- and decide whether its broader subsystem noun can be safely promoted beyond “PPU shadow block”

## Address continuity note
The old handoff wording around the C0 seam uses address spellings that are still useful for continuity, but the actual byte proof in pass 109 came from the raw ROM windows directly.
So keep following the pass-109 writeup rather than the old “AE2B owner seam” wording.

## Completion estimate after pass 109
Conservative project completion estimate: **~68.2%**

Why it dipped:
- this pass added real exact closures
- but it also corrected one misleading seam interpretation instead of pretending the older wording was still good
- that honesty reduces fake semantic certainty while improving the actual map of what is left
