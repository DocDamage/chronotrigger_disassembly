# Chrono Trigger Disassembly — Raw Seam Report for C3:B500..BEFF

This file preserves the seam-facing evidence for the next continuation after `C3:B500..`. It is intentionally terse and page-oriented.

## C3:B500..B5FF
- page metrics: ascii=0.41, zero=0.03, ff=0.00, repeated_pair=0.02
- strongest true outside multi-hit lure:
  - `B574` with 2 outside `JSR` hits (`C3:2E33`, `C3:552E`)
- that still fails immediately because the landing byte at `B574` is `60` (`RTS`), making it classic return-stub bait rather than a defendable owner start
- cleaner cross-bank lure:
  - `B563` from `DF:2716 -> JML $C3B563`, caller risk=medium, target risk=medium, but the landing byte is `01`
- strongest local islands:
  - `B5D9..B5E6`, score=4, ascii=0.50, calls=3, branches=1, returns=2
  - `B5D9..B5E9`, score=4, ascii=0.53, calls=3, branches=1, returns=3
- page also contains several small BRA landing-pad veneers around `B50B`, `B52A`, `B530`, `B555`, `B559`, and `B597`
- result: active early page with one real outside multi-hit false dawn and one busy local splinter, still no defendable owner boundary

## C3:B600..B6FF
- page metrics: ascii=0.34, zero=0.03, ff=0.01, repeated_pair=0.03
- only visible outside lure:
  - `B6BF` from `C3:42AA -> JSR $B6BF`, caller risk=high, target risk=high
- strongest local islands:
  - `B6A0..B6B8`, score=4, ascii=0.44, calls=1, branches=2, returns=1
  - `B6C6..B6CF`, score=2, ascii=0.60, branches=5, returns=1
- notable veneer field:
  - BRA landing pads around `B635`, `B6B4`, `B6C6`, and `B6EC`
  - `B6EF = RTL` stub
- result: one dirty outside hit and one better local pocket, still no caller-backed traction

## C3:B700..B7FF
- page metrics: ascii=0.39, zero=0.06, ff=0.01, repeated_pair=0.00
- no outside callable landings survived into this page
- strongest local islands:
  - `B769..B772`, score=5, ascii=0.20, branches=2, returns=1, stackish=1
  - `B7A2..B7AF`, score=5, ascii=0.43, calls=2, branches=2, returns=1, stackish=1
  - `B7A2..B7B8`, score=5, ascii=0.48, calls=2, branches=2, returns=2, stackish=1
- veneer activity stays local only, with BRA landing pads around `B740`, `B76A`, `B7CE`, and `B7EB`
- result: strongest pure local-control page of the early continuation, still no caller-backed true start

## C3:B800..B8FF
- page metrics: ascii=0.41, zero=0.07, ff=0.01, repeated_pair=0.06
- only visible outside lure:
  - `B8EE` from `CA:31D8 -> JSL $C3B8EE`, caller risk=medium, target risk=high
- no local islands survived strongly enough to matter beyond one tiny late pocket:
  - `B831..B836`, score=2, ascii=0.50, branches=2, returns=1
- only visible veneer candidate:
  - `B848 = BRA` landing pad into nearby local control
- result: quiet page with one cross-bank lure and almost no support for promotion

## C3:B900..B9FF
- page metrics: ascii=0.32, zero=0.05, ff=0.01, repeated_pair=0.07
- no outside callable landings survived into this page
- strongest local helper-like islands of the continuation:
  - `B994..B9AC`, score=5, ascii=0.28, branches=2, returns=2, stackish=1
  - `B979..B991`, score=5, ascii=0.28, branches=1, returns=1, stackish=2
  - `B986..B99E`, score=5, ascii=0.32, calls=1, branches=1, returns=2, stackish=2
- veneer activity is minimal, with a single BRA landing pad around `B9A0`
- result: structurally convincing local-control page with zero outside traction, still not owner-worthy

## C3:BA00..BAFF
- page metrics: ascii=0.29, zero=0.14, ff=0.00, repeated_pair=0.05
- visible outside lures:
  - `BA45` from `C3:8841 -> JSR $BA45`, caller risk=medium, target risk=high
  - `BA4C` from `C3:88B8 -> JMP $BA4C`, caller risk=low, target risk=high
  - `BA56` from `C3:79D0 -> JMP $BA56`, caller risk=high, target risk=high
  - `BAC6` from `C3:276D -> JSR $BAC6`, caller risk=medium, target risk=medium, landing byte=`02`
- strongest local island:
  - `BA6F..BA79`, score=4, ascii=0.18, branches=1, returns=1
- notable veneer candidates:
  - BRA landing pads around `BA16`, `BA3D`, and `BA56`
  - `BAB9 = RTL` stub
- result: several visible outside lures, but every one still collapses on target quality or bad-start bytes

## C3:BB00..BBFF
- page metrics: ascii=0.29, zero=0.17, ff=0.01, repeated_pair=0.09
- cleanest single outside lure of the continuation:
  - `BBDA` from `C3:0A01 -> JSR $BBDA`, caller risk=low, target risk=low
- other outside lures:
  - `BB81` from `C3:4457 -> JSR $BB81`, caller risk=high, target risk=medium
  - `BB00` from `C3:35C1 -> JSR $BB00`, caller risk=high, target risk=high, landing byte=`80`
- strongest local islands:
  - `BB04..BB15`, score=5, ascii=0.50, calls=1, branches=2, returns=5, stackish=2
  - `BB04..BB0D`, score=5, ascii=0.50, calls=1, branches=1, returns=3, stackish=2
- veneer field includes BRA landing pads around `BB00`, `BB18`, `BB86`, and `BBB9`
- result: one unusually clean single-hit lure plus a noisy early return cluster, still not enough to defend an owner/helper start

## C3:BC00..BCFF
- page metrics: ascii=0.29, zero=0.08, ff=0.01, repeated_pair=0.08
- only visible outside lure:
  - `BC1B` from `C3:387B -> JSR $BC1B`, caller risk=high, target risk=low
- strongest local island of the continuation:
  - `BC5C..BC74`, score=5, ascii=0.16, branches=6, returns=1, stackish=3
- secondary local pocket:
  - `BCBF..BCC6`, score=4, ascii=0.25, branches=2, returns=1
- only visible veneer candidate:
  - `BC48 = BRA` landing pad into nearby control flow
- result: best late local splinter of the run, still unsupported by any caller-backed true start

## C3:BD00..BDFF
- page metrics: ascii=0.42, zero=0.08, ff=0.00, repeated_pair=0.04
- visible outside lures:
  - `BD12` from `C3:389B -> JSR $BD12`, caller risk=medium, target risk=medium
  - `BD00` from `C3:1E45 -> JSR $BD00`, caller risk=medium, target risk=high, landing byte=`30`
  - `BD88` from `C3:D7A9 -> JSR $BD88`, caller risk=high, target risk=high
- strongest local islands:
  - `BDE7..BDF2`, score=4, ascii=0.50, calls=1, branches=2, returns=2
  - `BDE7..BDEE`, score=4, ascii=0.50, calls=1, branches=1, returns=1
- veneer field includes BRA landing pads around `BD34`, `BD56`, `BD85`, `BD99`, and `BDEA`
- result: active late page with one middling clean outside hit and a noisy tail cluster, still no defendable boundary

## C3:BE00..BEFF
- page metrics: ascii=0.49, zero=0.04, ff=0.00, repeated_pair=0.06
- visible outside lures:
  - `BEA2` from `C3:B807 -> JSR $BEA2`, caller risk=high, target risk=high
  - `BEF0` from `C3:12C7 -> JSR $BEF0`, caller risk=high, target risk=high
- strongest local islands:
  - `BE58..BE67`, score=5, ascii=0.69, calls=3, branches=3, returns=1, stackish=1
  - `BEB2..BEBD`, score=4, ascii=0.50, calls=1, branches=4, returns=2
  - `BECA..BED5`, score=3, ascii=0.33, branches=2, returns=1, stackish=1
- only visible veneer candidate:
  - `BE4A = BRA` landing pad
- result: loud, ASCII-heavy end page with dirty outside pressure and no honest owner/helper start

## Bottom line
Across `C3:B500..BEFF`, the seam produced five main temptations and rejected all of them honestly:
- `B574` as the strongest early outside multi-hit false dawn, killed immediately by landing on `RTS`
- `B769..B772` and especially `B994..B9AC` as the strongest early pure local-control splinters
- `BBDA` as the cleanest single outside lure of the continuation
- `BC5C..BC74` as the strongest late local island of the run
- `BD12` plus the surrounding late-page cluster as the cleanest late outside/local near-miss, still short of a defendable owner boundary

No new defendable owner/helper promotions survived.
