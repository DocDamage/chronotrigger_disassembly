# Chrono Trigger Disassembly — Raw Seam Report for C3:6F00..78FF

This file preserves the seam-facing evidence for the next continuation after `C3:6F00..`. It is intentionally terse and page-oriented.

## C3:6F00..6FFF
- page metrics: ascii=0.27, zero=0.13, ff=0.05, repeated_pair=0.27
- most interesting visible outside landing: `6F50` from `C3:6697 -> JSR $6F50`
- that matters because `6697..669A` was already a tiny `JSR/RTS` wrapper candidate in the prior block, but the target still does not defend a stable owner boundary here
- other outside lure: `6F1D` from `C3:D54D -> JMP $6F1D`, caller risk=medium, target risk=medium
- top local island:
  - `6FDC..6FE3 (RTS)`, score=2, ascii=0.50, branches=1
- result: low-traffic transitional page; the carried-over wrapper target still does not make the page recoverable code

## C3:7000..70FF
- page metrics: ascii=0.29, zero=0.12, ff=0.02, repeated_pair=0.10
- busiest raw-xref page of the continuation, but every visible landing is only single-hit outside pressure
- cleaner-looking individual lures: `70E0` from `C3:88C9 -> JMP $70E0`, plus `7078`, `707E`, and `70E6` with low target-side risk but dirty callers
- page-top bait `7000` still grades high/high and does not stabilize
- top local island:
  - `706A..7072 (RTS)`, score=2, ascii=0.44, branches=1
- result: xref-noisy page with no defendable owner start

## C3:7100..71FF
- page metrics: ascii=0.15, zero=0.07, ff=0.00, repeated_pair=0.28
- visually cleaner than the surrounding pages, but the outside landings still collapse on inspection
- `7157` is the clearest example because it takes an outside `JSR` from `C3:7767` and still lands directly on `00`
- other outside lures: `7141`, `71AA`, `71AC`; all are single-hit and caller-dirty
- no local islands survived strongly enough to matter
- result: low-ascii false-dawn page, still no caller-backed ownership

## C3:7200..72FF
- page metrics: ascii=0.62, zero=0.09, ff=0.00, repeated_pair=0.08
- page turns sharply more text/mixed-content heavy again
- cleanest visible outside lure: `724E` from `C3:A8C5 -> JSR $724E`, caller risk=medium, target risk=low
- other outside lure: `7210` from `C3:4AAC -> JSR $7210`, caller risk=medium, target risk=medium
- top local islands:
  - `7297..72A9 (RTS)`, score=4, ascii=0.79, calls=1, branches=2
  - `721D..722F (RTS)`, score=3, ascii=0.37, stackish=3, branches=2
- notable tiny veneer candidate:
  - `72FE..72FE = RTL` stub
- result: heavily ASCII-tainted page with one deceptively clean outside landing and no recoverable owner

## C3:7300..73FF
- page metrics: ascii=0.69, zero=0.09, ff=0.00, repeated_pair=0.07
- overtly mixed/text-heavy page
- visible outside lures: `7385` from `C3:2489 -> JSR $7385` and `7316` from `C3:4843 -> JSR $7316`
- `7316` fails immediately because the landing byte is `02`
- strongest local island:
  - `7305..7311 (RTS)`, score=4, ascii=0.85, calls=2, branches=1
- result: obvious mixed-content contamination, not a believable code breakout

## C3:7400..74FF
- page metrics: ascii=0.55, zero=0.02, ff=0.00, repeated_pair=0.01
- strongest true external multi-hit lure of the continuation: `7420` with two outside `JSR` hits (`C3:2E32`, `C3:4B6C`)
- it still fails instantly because the landing byte is `01`, and the surrounding page stays highly contaminated
- other outside lures: `7408` from `C3:581A`, `74F5` from `C3:466C`, `7453` from `C3:441D`, `74DD` from `C3:4B60`
- top local islands:
  - `7415..7429 (RTS/RTS)`, score=4, ascii=0.52, calls=1, branches=1
  - `743D..7451 (RTS)`, score=3, ascii=0.62, calls=1
- result: best raw outside pressure in the block and still a textbook false dawn

## C3:7500..75FF
- page metrics: ascii=0.48, zero=0.02, ff=0.01, repeated_pair=0.01
- only visible outside callable landing: `7534` from `C3:8E66 -> JSR $7534`, caller risk=medium, target risk=high
- strongest local islands:
  - `7572..7578 (RTS)`, score=4, ascii=0.29, branches=2
  - `7500..7508 (RTS)`, score=3, ascii=0.89, calls=1
- page also contains several small branch-fed landing-pad style veneers around `7522`, `7537`, and `7593`
- result: sparse mixed page with one outside lure and multiple tiny local-control splinters

## C3:7600..76FF
- page metrics: ascii=0.50, zero=0.00, ff=0.04, repeated_pair=0.01
- outside callable traffic exists, but none of it stabilizes
- strangest visible lure: `76C3` from `FC:BA5A -> JML $C376C3`, caller risk=low, target risk=high
- same page also takes outside hits at `7600`, `762E`, `7649`, and `76C7`, all still mixed and unsupported
- top local island:
  - `76EC..76F0 (RTS)`, score=2, ascii=0.80, branches=1
- result: cross-bank attention does not rescue the page; it remains mixed-content bait

## C3:7700..77FF
- page metrics: ascii=0.53, zero=0.02, ff=0.00, repeated_pair=0.00
- strongest local helper-like island of the continuation:
  - `771C..7734 (RTS)`, score=5, ascii=0.76, calls=4, branches=3, stackish=2
- that island still fails promotion because it is buried in an obviously ASCII-heavy mixed page, not a stable callable lane
- visible outside lures: `77AB` from `C3:57FD -> JSR $77AB` and `7774` from `C3:4B6D -> JSR $7774`
- result: best local splinter of the run, still too contaminated to own itself

## C3:7800..78FF
- page metrics: ascii=0.50, zero=0.04, ff=0.01, repeated_pair=0.01
- outside callable lures stay thin and dirty: `78F0`, `783C`, `7852`, `78BF`
- `78F0` is the clearest late false landing because it gets an outside `JSR` from `C3:12D4` and still lands on `FF`
- top local islands:
  - `7845..7850 (RTS)`, score=3, ascii=0.33, stackish=1, branches=1
  - `78F3..78FE (RTS)`, score=2, ascii=0.33, branches=2
- result: late block stays mixed and never turns into a recoverable owner page

## Bottom line
Across `C3:6F00..78FF`, the seam produced four main temptations and rejected all of them honestly:
- `6F50` as the carried-over tiny-wrapper target that still does not defend a real start
- `7420` as the strongest true external multi-hit false dawn, killed immediately by landing on `01`
- `724E` as the cleanest-looking single-hit outside lure on a very dirty page
- `771C..7734` as the strongest local helper-like island of the continuation, still too ASCII-heavy to promote

No new defendable owner/helper promotions survived.
