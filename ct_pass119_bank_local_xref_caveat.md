# Chrono Trigger Pass 119 — Bank-Local Absolute Xref Caveat

## What got corrected

Raw absolute-xref output for `$8820` was previously treated as if every hit targeted one shared cross-bank routine.

That is wrong for 65816 absolute `JSR` / `JMP`.

## Exact rule

- `JSR $xxxx` is bank-local
- `JMP $xxxx` is bank-local
- they do **not** switch program bank

So a hit like:

- `C2:A1C3  JSR $8820`

targets:

- `C2:8820`

not:

- `C0:8820`

Likewise hits in:

- `C4`
- `D0`
- `D4`
- `D5`
- `D7`
- `E5`

are only same-offset local calls inside those banks unless there is an explicit long-call/veneer proof.

## Why this mattered here

The settlement/search subsystem caller family frozen in passes 117–118 lives in bank `C2`.

The correct owner band is:

- `C2:8820..C2:991F`

not:

- `C0:8820..C0:991F`

## Carry-forward rule

For future seam work:

- treat raw absolute-xref hits across different banks as **potential same-offset false positives**
- only promote cross-bank ownership when there is:
  - `JSL`
  - `JML`
  - exact veneer proof
  - or another explicit bank-changing path
