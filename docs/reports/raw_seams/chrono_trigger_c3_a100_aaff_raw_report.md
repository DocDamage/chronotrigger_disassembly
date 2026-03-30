# Chrono Trigger Disassembly — Raw Seam Report for C3:A100..AAFF

This file preserves the seam-facing evidence for the next continuation after `C3:A100..`. It is intentionally terse and page-oriented.

## C3:A100..A1FF
- page metrics: ascii=0.27, zero=0.20, ff=0.01, repeated_pair=0.07
- only visible outside lure:
  - `A100` from `C3:4A8E -> JSR $A100`, caller risk=medium, target risk=medium
- no outside multi-hit pressure survived into the page
- strongest local island:
  - `A1A1..A1A6 (RTS/RTS)`, score=2, ascii=0.67, branches=1
- page also contains several small BRA landing-pad style veneers around `A13C`, `A179`, `A1D7`, `A1EB`, and `A1FC`
- result: quiet transition page with one middling outside landing and no defendable owner boundary

## C3:A200..A2FF
- page metrics: ascii=0.41, zero=0.11, ff=0.01, repeated_pair=0.06
- busiest outside-call page of the continuation
- strongest raw outside multi-hit lure:
  - `A28B` with 3 outside `JSR` hits (`C3:1977`, `C3:3B7F`, `C3:4D1D`)
- cleaner paired lure on the same page:
  - `A28A` with 2 outside `JSR` hits (`C3:0CBA`, `C3:0CCF`), best pairing medium/medium and low/medium
- both still fail because the page stays ASCII-heavy and the landings sit inside wider mixed material rather than a stable routine boundary
- other outside lures: `A200`, `A204`, `A208`, `A20A`, `A221`
- no local islands survived strongly enough to matter
- result: most xref-active page of the run, still mixed and unsupported

## C3:A300..A3FF
- page metrics: ascii=0.38, zero=0.09, ff=0.01, repeated_pair=0.02
- cleanest outside lures of the continuation:
  - `A3A5` from `C3:6CD1 -> JSR $A3A5`, caller risk=medium, target risk=low
  - `A3B8` from `C3:6864 -> JSR $A3B8`, caller risk=low, target risk=medium
  - `A3BD` from `C3:6867 -> JSR $A3BD`, caller risk=low, target risk=medium
- dirtier outside lures: `A318` from `C3:463B -> JSR $A318` and `A3EE` from `C3:0202 -> JSR $A3EE`
- strongest local islands:
  - `A345..A351 (RTS)`, score=4, ascii=0.69, calls=2
  - `A3D4..A3D9 (RTS)`, score=4, ascii=0.17, branches=1
  - `A3B0..A3B4 (RTS)`, score=4, ascii=0.20, branches=2
- result: cleanest single-hit outside-call page of the continuation, still no caller-backed owner start

## C3:A400..A4FF
- page metrics: ascii=0.40, zero=0.05, ff=0.01, repeated_pair=0.04
- only visible outside lures:
  - `A401` from `C3:2EA0 -> JSR $A401`, caller risk=high, target risk=high
  - `A458` from `C3:3735 -> JSR $A458`, caller risk=high, target risk=high
- strongest local islands:
  - `A400..A410 (RTS/RTS)`, score=4, ascii=0.41, calls=2, branches=2
  - `A400..A406 (RTS)`, score=4, ascii=0.43, calls=1, branches=1
- page also contains a later noisy pocket at `A4BB..A4C9`, but it is too ASCII-heavy to matter
- result: page has local structure but outside pressure is dirty and unconvincing

## C3:A500..A5FF
- page metrics: ascii=0.38, zero=0.05, ff=0.00, repeated_pair=0.02
- strongest outside multi-hit lure:
  - `A521` with 2 outside `JSR` hits (`C3:55A6`, `C3:7589`)
- that still fails because one caller is low/high, the other is high/medium, and the landing bytes do not defend a stable owner boundary
- other outside lures:
  - `A500` from `C3:47C7 -> JSR $A500`, landing byte=`01`
  - `A531` from `C3:3849 -> JSR $A531`, caller risk=high, target risk=medium
- no local islands survived strongly enough to matter
- result: real outside pressure exists, but the page still reads as mixed material rather than recoverable code

## C3:A600..A6FF
- page metrics: ascii=0.38, zero=0.16, ff=0.00, repeated_pair=0.08
- visible outside pressure is narrow and dirty:
  - `A600` with 2 outside `JSR` hits (`C3:2261`, `C3:7FD5`), both high/high
  - `A620` from `C3:393A -> JSR $A620`, caller risk=high, target risk=medium, landing byte=`09`
- strongest local island cluster:
  - `A688..A697`, score=4, ascii=0.69, calls=2, branches=5, returns=2
  - `A688..A693`, score=4, ascii=0.75, calls=2, branches=4
- result: one dirty page-top false dawn plus a noisy internal cluster, still far short of promotion

## C3:A700..A7FF
- page metrics: ascii=0.32, zero=0.15, ff=0.00, repeated_pair=0.17
- only visible outside lure:
  - `A780` from `C3:58A0 -> JSR $A780`, caller risk=high, target risk=medium
- no local islands survived strongly enough to matter
- page also contains a small BRA landing-pad veneer at `A7DE`
- result: thin page with one dirty outside landing and no caller-backed traction

## C3:A800..A8FF
- page metrics: ascii=0.25, zero=0.17, ff=0.01, repeated_pair=0.11
- cleanest outside lure on the page:
  - `A8A2` from `C3:5DE4 -> JSR $A8A2`, caller risk=medium, target risk=low, landing byte=`03`
- other outside lures:
  - `A810` from `C3:2D01 -> JSR $A810`, caller risk=medium, target risk=medium
  - `A800` from `C3:5A32 -> JSR $A800`, caller risk=high, target risk=medium
  - `A8BB` from `C3:4A50 -> JSR $A8BB`, caller risk=high, target risk=medium
- strongest local helper-like island of the continuation:
  - `A847..A855`, score=5, ascii=0.40, calls=2, branches=2, stackish=1, returns=2
- additional local pockets:
  - `A847..A852`, score=5, ascii=0.42, calls=2, branches=1, stackish=1
  - `A8C0..A8C8`, score=4, ascii=0.67, calls=1, branches=1
- result: best local helper-like page of the continuation, still lacking a caller-backed true start

## C3:A900..A9FF
- page metrics: ascii=0.36, zero=0.14, ff=0.02, repeated_pair=0.06
- strongest outside multi-hit lure:
  - `A90B` with 3 outside `JSR` hits (`C3:1C67`, `C3:3500`, `C3:464C`)
- next lure:
  - `A960` with 2 outside `JSR` hits (`C3:37A1`, `C3:48CF`)
- both still fail because target-side bytes stay high-risk and the page remains unevenly mixed
- other visible lures:
  - `A905` from `C3:3830 -> JSR $A905`, landing byte=`00`
  - `A90A` from `C3:1C60 -> JSR $A90A`
  - `A914` from `C3:21B4 -> JSR $A914`
- only surviving local island:
  - `A979..A97D (RTS/RTS)`, score=2, ascii=1.00
- result: busiest late dirty page of the continuation, still pure false pressure

## C3:AA00..AAFF
- page metrics: ascii=0.36, zero=0.13, ff=0.00, repeated_pair=0.09
- cleanest late outside lure:
  - `AAA0` from `C3:5B14 -> JSR $AAA0`, caller risk=medium, target risk=medium
- dirtier outside lures:
  - `AA00` from `C3:033E -> JSR $AA00`, high/high
  - `AA01` from `C3:572E -> JMP $AA01`, high/high
  - `AA3F` from `C3:1EC9 -> JSR $AA3F`, high/high
  - `AA40` from `C3:2EA8 -> JSR $AA40`, high/high
- strongest local island:
  - `AA99..AAA2`, score=2, ascii=0.50, branches=2, returns=1
- notable tiny veneer candidate:
  - `AAA2 = RTL` stub
- result: late block cools off with one middling single-hit lure and no owner-worthy support

## Bottom line
Across `C3:A100..AAFF`, the seam produced five main temptations and rejected all of them honestly:
- `A28B` as the strongest raw outside multi-hit false dawn, with `A28A` as the cleaner paired lure on the same page
- `A3A5 / A3B8` as the cleanest single-hit outside lures of the continuation
- `A521` as the first true outside multi-hit lure after the early rebound pages
- `A847..A855` as the strongest local helper-like island of the run
- `A90B` as the busiest late outside-call lure, with `AAA0` the cleanest late single-hit landing

No new defendable owner/helper promotions survived.
