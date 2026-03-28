# Chrono Trigger Disassembly — Raw Seam Report for C3:5100..5AFF

This file preserves the seam-facing evidence for the fifth continuation of session 13. It is intentionally terse and page-oriented.

## C3:5100..51FF
- page metrics: ascii=0.26, zero=0.09, ff=0.01, repeated_pair=0.03
- strongest visible local/control target: `5196` with 2 branch-fed hits and low-risk target-side bytes
- strongest true outside pressure: `5100` with 2 dirty external `JSR` hits (`C3:2C08`, `C3:5B7D`)
- other notable outside landings: `51F4` from `C3:2DFC`, `5168` from `C3:50C9`, `51B5` from `C3:4B48`
- top local islands:
  - `51E8..51F0 (RTI)`, score=5, ascii=0.22, calls=1, branches=0
  - `51DD..51E3 (RTI)`, score=3, ascii=0.57, calls=1, branches=0
- result: mixed control page with a tempting late pocket, no caller-backed owner

## C3:5200..52FF
- page metrics: ascii=0.29, zero=0.08, ff=0.00, repeated_pair=0.08
- strongest page-top false dawn: `5200` with 2 hits (`C3:3E86 JSR`, `C3:51FE BPL`)
- other notable outside landings: `5249` with 2 hits (`C3:43EE`, `C3:502E`), `5247` with 2 dirty hits (`C3:0E9F`, `C3:0EE6`)
- page also contains several low-risk local branch-fed landings: `520A`, `5213`, `52BE`, `52C7`, `52F5`
- top local islands:
  - `5273..5284 (RTS)`, score=4, ascii=0.67, calls=4, branches=2
  - `5221..5226 (RTS)`, score=4, ascii=0.17, calls=0, branches=0
  - `52D8..52DC (RTS)`, score=4, ascii=0.20, calls=0, branches=1
- result: strongest page-top bait of the continuation, still no defendable owner

## C3:5300..53FF
- page metrics: ascii=0.37, zero=0.15, ff=0.00, repeated_pair=0.07
- visible targets are sparse and mostly local branch/control traffic
- cleanest outside landing: `531B` from `C3:52F8 -> BRA $531B`, caller risk=medium, target risk=low
- dirtier outside lures: `537C` from `C3:4F95`, `53A5` from `C3:100B`, `53DA` from `C3:4577 BRL`
- top local island:
  - `5364..5375 (RTS/RTS)`, score=5, ascii=0.28, branches=2, returns=2
- result: sparse mixed branch/control page, no credible outside ownership

## C3:5400..54FF
- page metrics: ascii=0.33, zero=0.09, ff=0.00, repeated_pair=0.05
- strongest true external target: `54A5` with 2 medium-risk `JSR` hits (`C3:009D`, `C3:026D`)
- other visible outside landings: `544C` from `C3:6A52` (low/high), `5437` from `C3:51B7`, `54EA` from `C3:2FE6`
- xref-noisy local/control targets include `5445`, `545E`, `5462`, `5479`
- top local islands:
  - `5450..5455 (RTS/RTS/RTS)`, score=4, ascii=0.67, calls=1, branches=1
  - `54AB..54B3 (RTI)`, score=3, ascii=0.44, calls=1, branches=0
- result: active mixed page with a real-looking double-`JSR` false dawn, still no defendable owner

## C3:5500..55FF
- page metrics: ascii=0.32, zero=0.12, ff=0.01, repeated_pair=0.03
- strongest visible landing: `557B` with 2 medium-risk branch-fed hits
- strongest dirty outside pressure: `55A5` with 2 high-risk `JSR` hits (`C3:1002`, `C3:105E`)
- other outside lures: `552A` from `C3:54D7`, `55FB` from `C3:5609`, `5550` from `C3:54DB BRL`
- top local islands:
  - `559F..55B1 (RTS)`, score=5, ascii=0.32, calls=1, branches=2
  - `55D3..55D8 (RTS)`, score=4, ascii=0.33, calls=1, branches=1
- result: mixed branch-heavy page with one medium-quality local cluster and no stable external owner

## C3:5600..56FF
- page metrics: ascii=0.36, zero=0.21, ff=0.00, repeated_pair=0.20
- cleanest-looking individual landing: `56DD` from `C3:5757 -> BMI $56DD`, caller risk=low, target risk=low
- other outside lures: `5654` from `C3:6A53 JMP`, `56B4` from `C3:6758 JMP`, `56D1` from `C3:3243 JSR`
- busiest visible target: `5605` with 2 high-risk hits (`C3:55B3`, `C3:561B`)
- no local islands survived scoring strongly enough to matter
- result: ugly page-level density with one clean late branch-fed lure, still not owner-worthy

## C3:5700..57FF
- page metrics: ascii=0.33, zero=0.07, ff=0.00, repeated_pair=0.06
- busiest visible targets: `57FF` and `57C5`, each with 2 hits
- strongest outside `JSR` lure: `5777` with hits from `C3:3059` and `C3:5BEE`, still high-risk on target side
- other outside/control landings: `579F` from `C3:339B`, `57C5` from `C3:5823`, `57FF` from `C3:5833`
- top local islands:
  - `57BF..57D7 (RTI)`, score=4, ascii=0.40, calls=2, branches=3
  - `572B..5731 (RTS)`, score=3, ascii=0.57, calls=2, branches=0
- result: mixed control page with clustered late traffic and one broad unsupported local island

## C3:5800..58FF
- page metrics: ascii=0.25, zero=0.05, ff=0.00, repeated_pair=0.00
- cleanest-looking page of the continuation overall
- busiest visible landing: `5872` with 2 hits, best pairing medium/medium
- several low-risk local branch-fed landings exist: `581C`, `581D`, `5827`, `587E`, `5890`
- top local islands:
  - `582B..5840 (RTI)`, score=4, ascii=0.23, calls=0, branches=2
  - `5898..58AB (RTS)`, score=4, ascii=0.40, calls=2, branches=2
  - `587A..5886 (RTI)`, score=4, ascii=0.15, calls=0, branches=4
- result: feels executable, but mostly as self-contained local control rather than caller-backed ownership

## C3:5900..59FF
- page metrics: ascii=0.33, zero=0.08, ff=0.01, repeated_pair=0.05
- cleanest visible lure: `596F` from `C3:5958 -> BVS $596F`, caller risk=medium, target risk=low
- dirtier late bait: `59DA` with 2 high/high hits
- other outside landings: `5903` from `C3:58E0`, `5927` from `C3:58A8`, `5902` from `C3:190D`
- top local island:
  - `59D0..59D5 (RTS)`, score=2, ascii=0.67, calls=0, branches=1
- result: sparse mixed page with one cleaner mid-page lure, no owner boundary

## C3:5A00..5AFF
- page metrics: ascii=0.33, zero=0.10, ff=0.00, repeated_pair=0.03
- clustered early bait: `5A1D` and `5A4C`, each with 2 high-risk hits
- cleaner late control endpoints: `5AAA` and `5ABA`, both low-risk but branch-fed and local
- other outside lures: `5A06` from `C3:8ADA`, `5A40` from `C3:59E0`, `5A6D` from `C3:6A22`, `5ABA` from `C3:5B17`
- top local island:
  - `5A67..5A75 (RTS)`, score=3, ascii=0.33, calls=0, branches=1
- result: page ends cleaner than it begins, but still no caller-backed owner start

## Bottom line
Across `C3:5100..5AFF`, the seam produced three main temptations and rejected all of them honestly:
- `5200` as the strongest page-top false dawn
- `54A5` as the strongest true external multi-hit false dawn
- `5800` as the cleanest-looking page overall, still only as local control structure

No new defendable owner/helper promotions survived.
