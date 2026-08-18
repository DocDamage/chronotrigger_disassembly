# Chrono Trigger Disassembly — Raw Seam Report for C3:8300..8CFF

This file preserves the seam-facing evidence for the next continuation after `C3:8300..`. It is intentionally terse and page-oriented.

## C3:8300..83FF
- page metrics: ascii=0.30, zero=0.13, ff=0.00, repeated_pair=0.02
- visible outside lures are sparse and all stay dirty:
  - `8328` from `C3:B8F4 -> JSR $8328`
  - `8330` from `C3:A37A -> JMP $8330`
  - `8300` from `C3:D067 -> JSR $8300`
- strongest local island:
  - `8302..830A (RTS/RTS/RTS)`, score=4, ascii=0.67, calls=1, branches=2
- page also contains several tiny BRA landing-pad style veneers around `830F`, `833C`, `8354`, `836F`, and `83B3`
- result: mixed transitional page with a busy early local-control splinter, still no caller-backed owner

## C3:8400..84FF
- page metrics: ascii=0.29, zero=0.13, ff=0.01, repeated_pair=0.05
- strongest true outside multi-hit lure:
  - `8440` with 2 outside `JSR` hits (`C3:2EAF`, `C3:D055`)
- both callers stay high-risk, and the page never stabilizes into a defendable routine boundary
- other outside lures: `8402`, `842A`, `84DC`
- top local island:
  - `8452..845E (RTS)`, score=2, ascii=0.38, branches=4
- result: modestly cleaner page with one real multi-hit lure, still mixed and unsupported

## C3:8500..85FF
- page metrics: ascii=0.21, zero=0.09, ff=0.03, repeated_pair=0.09
- strongest true external multi-hit lure of the continuation:
  - `8500` with 3 outside `JSR` hits (`C3:0520`, `C3:38D9`, `C3:4368`)
- that still fails because the landing byte stream starts `DF 12 ED 30 00 ...`, which reads like packed mixed command/data material rather than a stable owner boundary
- cleanest single outside lure on the page:
  - `857E` from `C3:4E57 -> JSR $857E`, caller risk=medium, target risk=low
- strongest local islands:
  - `8569..8574 (RTS)`, score=4, ascii=0.25
  - `852A..8533 (RTS)`, score=4, ascii=0.40, calls=1, branches=1
- result: lowest-ascii page of the continuation and still only a false dawn; outside pressure exists, but the page does not own itself

## C3:8600..86FF
- page metrics: ascii=0.49, zero=0.14, ff=0.00, repeated_pair=0.04
- cleanest outside lures:
  - `860C` from `C3:1C0F -> JSR $860C`, caller risk=medium, target risk=low
  - `862B` from `C3:832D -> JSR $862B`, caller risk=medium, target risk=low
- both are still single-hit and embedded inside a page that stays heavily ASCII/mixed-content contaminated
- strongest local island:
  - `86D8..86E3 (RTS)`, score=4, ascii=0.75, calls=2
- notable tiny veneer candidate:
  - `8685..8685 = RTL` stub
- result: page produces a couple of cleaner individual landings, but they still do not defend ownership

## C3:8700..87FF
- page metrics: ascii=0.37, zero=0.09, ff=0.02, repeated_pair=0.01
- outside callable traffic is thin:
  - `8772` from `C3:584A -> JSR $8772`
  - `8752` from `C3:579F -> JSR $8752`
- strongest local helper-like island of the continuation:
  - `87A4..87AE (RTS)`, score=5, ascii=0.18, branches=2, stackish=1
- the same page also contains a wider noisy splinter around `87BA..87E1`, but it is too ASCII-heavy and internally fragmented to promote
- notable tiny veneer candidates:
  - `87BC..87BF = JSR $7020 / RTS`
  - `87BD..87C0 = JSR $6070 / RTS`
- result: best local helper-like pocket of the run, still lacking a caller-backed true start

## C3:8800..88FF
- page metrics: ascii=0.29, zero=0.11, ff=0.01, repeated_pair=0.02
- strongest outside multi-hit lure:
  - `88AD` with 2 outside `JSR` hits (`C3:09A5`, `C3:0BE3`)
- this is the cleanest multi-hit target in the continuation, with one low-risk caller and low target-side risk, but the target bytes still do not defend a stable owner boundary
- other outside lures: `8800`, `880B`, `8880`, `88E6`
- strongest local island:
  - `8868..8871 (RTS)`, score=4, ascii=0.10
- page also contains multiple BRA landing-pad style veneers around `8823`, `885A`, `885C`, `88A8`, `88AA`, `88B2`, `88CC`, and `88CE`
- result: most interesting page of the block after `8500`, still mixed command/control material rather than recoverable standalone code

## C3:8900..89FF
- page metrics: ascii=0.33, zero=0.12, ff=0.02, repeated_pair=0.06
- strongest outside multi-hit lure:
  - `89ED` with 2 outside `JSR` hits (`C3:1D95`, `C3:4CD6`)
- cleaner single-hit lure:
  - `8921` from `C3:6637 -> JMP $8921`, caller risk=medium, target risk=low
- neither survives because the page stays mixed and the late hits pile into dirtier target-side bytes
- top local island:
  - `8978..897D (RTS)`, score=3, ascii=0.17
- notable tiny veneer candidates:
  - `8913 = RTL` stub
  - `89F5 = RTL` stub
  - `89F6 = RTL` stub
- result: mixed late-block page with one decent single-hit lure and one dirtier double-hit lure, still no owner boundary

## C3:8A00..8AFF
- page metrics: ascii=0.32, zero=0.10, ff=0.02, repeated_pair=0.06
- strongest clean outside lure:
  - `8A8D` from `C3:1867 -> JSR $8A8D`, caller risk=low, target risk=medium
- other outside lures: `8A40`, `8A03`, `8A06`, `8AF0`
- strongest local island cluster of the continuation:
  - `8A10..8A26`, score=4, ascii=0.35, calls=2, branches=5, returns=6
- that whole cluster still behaves like an internal control pocket rather than a caller-backed true start
- result: structurally busy page with the densest local island cluster of the run, still not enough to promote code

## C3:8B00..8BFF
- page metrics: ascii=0.33, zero=0.09, ff=0.02, repeated_pair=0.02
- only visible outside lure:
  - `8B00` from `C3:D15B -> JSR $8B00`, caller risk=high, target risk=high
- strongest local island:
  - `8BE8..8BF2 (RTS)`, score=4, ascii=0.45, calls=1, branches=1
- notable tiny veneer candidate:
  - `8BDB..8BDE = JSR $7C13 / RTS`
- result: sparse page whose most interesting feature is a tiny wrapper back into the already-proven zero field at `7C13`

## C3:8C00..8CFF
- page metrics: ascii=0.32, zero=0.14, ff=0.00, repeated_pair=0.09
- strongest outside multi-hit lure:
  - `8C80` with 2 outside `JSR` hits (`C3:065A`, `C3:071D`), both with low caller-side risk and medium target-side risk
- other visible lures:
  - `8C02` from `C3:B41D`
  - `8C0A` from `C3:588E`
  - `8C8F` from `C3:B191`
  - `8C90` from `C3:8EF6`
  - `8CAD` from `C3:08FC`
- strongest local island:
  - `8C9F..8CA5 (RTS)`, score=3, ascii=0.57, calls=2
- result: late-block page with the cleanest outside double-hit lure of the continuation, still not enough to defend a real owner start

## Bottom line
Across `C3:8300..8CFF`, the seam produced five main temptations and rejected all of them honestly:
- `8440` as the first real multi-hit lure of the continuation
- `8500` as the strongest true external multi-hit false dawn of the run
- `87A4..87AE` as the strongest local helper-like island of the continuation
- `88AD` as the cleanest-looking outside multi-hit lure in the block
- `8C80` as the cleanest late-block double-hit lure, still short of a defendable owner boundary

No new defendable owner/helper promotions survived.
