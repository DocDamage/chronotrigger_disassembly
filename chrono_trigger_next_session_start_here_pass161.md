# Chrono Trigger — Next Session Start Here (Pass 161)

## What pass 161 actually closed

Pass 161 proved that exact low-bank `C3` is real mapped ROM at exact payload/file offset `0x030000`, not one exact fake unmapped seam, and closed the exact bank-head veneer/data cluster plus the exact launcher immediately after it.

### Exact new closures now frozen

- `C3:0000..C3:0001`
  - exact branch-over wrapper `BRA $0014`

- `C3:0005..C3:0007`
  - exact embedded raw long constant `C2:DECE`

- `C3:0008..C3:000A`
  - exact direct-entry veneer `JMP $0077`
  - exact `JSL C3:0008` appears at **11** exact call sites

- `C3:000B..C3:000D`
  - exact second embedded raw long constant `C2:DECE`

- `C3:000E..C3:0010`
  - exact direct-entry veneer `JMP $01E4`
  - exact `JSL C3:000E` appears at **3** exact call sites

- `C3:0011..C3:0013`
  - exact direct-entry veneer `JMP $0EFA`
  - exact `JSL C3:0011` appears at **1** exact call site

- `C3:0014..C3:0076`
  - exact bank-head launcher that:
    - installs exact RAM trampolines `0500 = JML C3:0548` and `0504 = JML C3:0529`
    - conditionally seeds exact `$2100/$4200/$4209` state
    - loads one exact source word from exact `FE:0003 -> 0300`
    - stages exact unpack core `C3:0557` for exact destination `7E:3000`
    - exits through exact `JML 7E:3000`

- `C3:0529..C3:0547`
  - exact temporary RAM-trampoline body that polls exact `$4212`, writes exact `80 -> $2100`, and exits exact `RTI`

- `C3:0548..C3:0556`
  - exact temporary RAM-trampoline body that reads exact `$4210`, writes exact `0F -> $2100`, and exits exact `RTI`

## Important correction/state change

- do **not** keep treating exact `C3:0000` as "non-ROM-mapped"
- the exact toolkit warning is the blind spot here, not the exact bytes
- exact `C3:0000..0013` is now split into:
  - one exact branch-over wrapper
  - one already-proven exact unpack veneer at `0002`
  - two exact embedded raw long constants
  - three exact live direct-entry veneers

## What not to reopen

- do not reopen exact `C3:0005..0007` or exact `C3:000B..000D` as code without brand-new proof; they are exact raw constant spans right now
- do not flatten exact `C3:0000..0013` into one exact monolithic "startup blob"
- do not forget that exact `0014` is now closed through its exact `JML 7E:3000` tail

## The real next seam now

1. exact next manual/raw target:
   - `C3:0077..C3:01E3`

2. exact reasons this is the right next place:
   - exact `C3:0008` is one exact live veneer with **11** exact call sites
   - exact `C3:0077` is the exact first downstream worker body that veneer lands in
   - exact `C3:01E4` is already anchored by one exact second veneer at exact `000E`, so the clean first split stops right before it

3. exact safest next move:
   - inspect exact raw bytes `C3:0077..C3:01FF` manually
   - split the exact `0077` worker from the exact follow-on owner at exact `01E4`
   - keep the exact low-bank tooling caveat explicit instead of pretending the default exact HiROM inspector has been fixed already
