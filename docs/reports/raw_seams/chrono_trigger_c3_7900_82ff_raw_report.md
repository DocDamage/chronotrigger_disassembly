# Chrono Trigger Disassembly — Raw Seam Report for C3:7900..82FF

This file preserves the seam-facing evidence for the next continuation after `C3:7900..`. It is intentionally terse and page-oriented.

## C3:7900..79FF
- page metrics: ascii=0.55, zero=0.03, ff=0.00, repeated_pair=0.00
- page is still strongly ASCII-heavy / mixed-content
- only visible outside lures are:
  - `7910` from `C3:A377 -> JMP $7910`
  - `795F` from `C3:7471 -> JSR $795F`
- both landings stay high-risk on both caller and target side
- top local island:
  - `7910..7928 (RTS)`, score=3, ascii=0.56, branches=1, stackish=1
- notable tiny veneer candidate:
  - `79B7..79B7 = RTL` stub
- result: dirty mixed page with two outside lures and no defendable owner

## C3:7A00..7AFF
- page metrics: ascii=0.09, zero=0.84, ff=0.00, repeated_pair=0.82
- page turns sharply into zero-heavy / repeated-pair-heavy material
- visible outside lures:
  - `7A00` from `C3:6FD1 -> JSR $7A00`
  - `7AC8` from `C3:70F7 -> JSR $7AC8`
- `7AC8` dies immediately because the landing byte is `00`
- result: obvious zero-heavy transition page, not a recoverable code page

## C3:7B00..7BFF
- page metrics: ascii=0.00, zero=1.00, ff=0.00, repeated_pair=0.99
- page is effectively a zero field
- only visible outside landing:
  - `7B37` from `C3:9308 -> JSR $7B37`
- the landing byte is `00`, so the hit is pure false pressure into dead zero space
- result: fully contaminated zero-fill page, not executable territory

## C3:7C00..7CFF
- page metrics: ascii=0.00, zero=1.00, ff=0.00, repeated_pair=0.99
- strongest zero-field false dawn of the continuation:
  - `7C13` with 5 outside `JSR` hits (`C3:8BDB`, `C3:9827`, `C3:9FAF`, `C3:BFCB`, `C3:C850`)
- other raw lures:
  - `7C83` from `EC:7751 -> JML $C37C83`
  - `7C8F` from `C3:2C5E -> JSR $7C8F`
  - `7CA5` from `C3:2732 -> JMP $7CA5`
- every landing still sits on `00`
- result: xref-rich but obviously fake zero-field pressure, no owner candidate

## C3:7D00..7DFF
- page metrics: ascii=0.00, zero=1.00, ff=0.00, repeated_pair=0.99
- only visible outside landing:
  - `7D12` from `D5:EEEE -> JSL $C37D12`
- the page is still all zeros; the landing is pure false pressure
- result: dead zero-fill page, nothing to recover

## C3:7E00..7EFF
- page metrics: ascii=0.00, zero=1.00, ff=0.00, repeated_pair=0.99
- strongest visible false dawn:
  - `7E4E` with 4 outside `JSR` hits (`C3:9476`, `C3:A29C`, `C3:BBAB`, `C3:CDB9`)
- other lures:
  - `7E20` from `C3:3C61`
  - `7E45` from `C3:5162`
  - `7E8D` from `C3:1AAB`
- all visible landings still sit on `00`
- result: another zero sea with raw-caller contamination, not code

## C3:7F00..7FFF
- page metrics: ascii=0.00, zero=1.00, ff=0.00, repeated_pair=0.99
- strongest visible false dawn:
  - `7F8C` with 3 outside `JSR` hits (`C3:9619`, `C3:A165`, `C3:A8BA`)
- other lures:
  - `7F08` from `C3:8F1D`
  - `7F12` from `C3:B4A2 -> JMP $7F12`
  - `7F40` from `C3:87C8`
- every visible landing still sits on `00`
- result: final zero-field page of the run, still pure false pressure

## C3:8000..80FF
- page metrics: ascii=0.22, zero=0.20, ff=0.02, repeated_pair=0.04
- first post-zero page and the most interesting real seam page of the continuation
- strongest true external multi-hit lure:
  - `800C` with 8 outside `JSR` hits, best pairings medium/medium
- cleanest-looking outside lure:
  - `8089` with 3 hits, best from `C3:1B1D -> JSR $8089`, caller risk=low, target risk=low
- other notable lures:
  - `8000` with 2 outside hits, but the page starts on `RTS`
  - `8034` with 2 high/high hits and a `00` landing byte
  - `80DE` from `C3:3E36`, caller risk=low, target risk=medium
- top local island:
  - `8072..807B (RTI)`, score=4, ascii=0.30, call_count=1, stackish=1
- result: best post-zero rebound page, still reading as packed mixed command/control material rather than a defendable owner lane

## C3:8100..81FF
- page metrics: ascii=0.27, zero=0.14, ff=0.00, repeated_pair=0.05
- no raw outside callable landings survived into this page
- page instead shows only small local-control / landing-pad style behavior
- top local island:
  - `81B7..81BB (RTS)`, score=3, ascii=0.40
- notable tiny veneer candidates:
  - `8125..8126 = BRA landing pad -> 8157`
  - `817C..817D = BRA landing pad -> 81AB`
  - `81D5..81D6 = BRA landing pad -> 81A5`
- result: transitional local-control page, still no caller-backed owner

## C3:8200..82FF
- page metrics: ascii=0.29, zero=0.12, ff=0.00, repeated_pair=0.03
- strongest late-block outside lure:
  - `8207` with 2 outside `JSL` hits (`E5:8EA7`, `EC:3F40`), caller risk=medium, target risk=medium
- other visible lures:
  - `8278` from `C3:4D94 -> JSR $8278`, caller risk=medium, target risk=low, but the landing byte is `02`
  - `8200` from `C3:DBAC -> JSR $8200`
  - `829C` from `C3:1C76 -> JSR $829C`
- strongest local island:
  - `82E0..82EE`, score=4, ascii=0.20, branches=3, returns=2
- page also contains several small BRA-style landing pads around `8263`, `82AB`, `82D9`, and `82E0`
- result: cleaner late mixed page with one cross-bank double-hit lure and one decent local island, still no defendable owner/helper start

## Bottom line
Across `C3:7900..82FF`, the seam produced four main truths and rejected the bait honestly:
- `7A00..7FFF` is overwhelmingly zero-filled territory, and the many raw callers into it are false pressure landing on `00`
- `7C13` is the strongest zero-field multi-hit false dawn of the continuation and still lands inside dead zero space
- `8000` is the first real post-zero rebound page; `800C` and especially `8089` look much cleaner than the surrounding run, but the page still does not defend a stable owner boundary
- `8207` is the strongest late-block outside multi-hit lure, while `82E0..82EE` is the strongest local island, and neither is enough to justify promotion

No new defendable owner/helper promotions survived.
