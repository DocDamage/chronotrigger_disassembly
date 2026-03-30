# Chrono Trigger Disassembly — Raw Seam Report for C3:5B00..64FF

This file preserves the seam-facing evidence for the first continuation after session 13. It is intentionally terse and page-oriented.

## C3:5B00..5BFF
- page metrics: ascii=0.36, zero=0.04, ff=0.02, repeated_pair=0.02
- strongest visible outside `JSR` lure: `5BB6` from `C3:4A36`, but both caller-side and target-side bytes stay high-risk
- cleaner outside branch/control landings: `5B5D` from `C3:5ADC -> BPL $5B5D`, `5B76` from `C3:504B -> BRL $5B76`
- top local islands:
  - `5B22..5B3A (RTS)`, score=5, ascii=0.40, calls=2, branches=2
  - `5B5A..5B72 (RTS)`, score=2, ascii=0.32, calls=0, branches=3
- result: mixed control page with one wider local splinter, no caller-backed owner

## C3:5C00..5CFF
- page metrics: ascii=0.35, zero=0.05, ff=0.00, repeated_pair=0.01
- strongest outside `JSR` lures: `5C8D` from `C3:6A30` and `5CAE` from `C3:6A29`; target-side bytes are cleaner, but caller-side risk stays high
- busiest visible target: `5C8D`, with one outside `JSR` plus branch-fed followthrough from `C3:5CBD` and `C3:5D05`
- top local islands:
  - `5C4D..5C65 (RTS)`, score=5, ascii=0.56, calls=1, branches=1
  - `5C6C..5C76 (RTS)`, score=3, ascii=0.36, calls=1, branches=0
- result: active mixed page with a cleaner target-side pocket, still no defendable owner boundary

## C3:5D00..5DFF
- page metrics: ascii=0.29, zero=0.09, ff=0.01, repeated_pair=0.01
- strongest true outside `JSR` lure: `5D95` from `C3:4AD8`, but target-side bytes still stay high-risk
- cleaner visible late control endpoint: `5DB4` from `C3:5E2D -> BCC $5DB4`
- top local islands:
  - `5DAC..5DB4 (RTS/RTS)`, score=4, ascii=0.22, branches=1
  - `5DBF..5DC7 (RTS)`, score=2, ascii=0.33, branches=2
- result: less text-heavy than the earlier pages, but still only as mixed branch/control structure

## C3:5E00..5EFF
- page metrics: ascii=0.32, zero=0.12, ff=0.01, repeated_pair=0.05
- strongest early-block false dawn: `5E3C` with two outside `JSR` hits (`C3:34CE`, `C3:5C3E`)
- that lure still fails ownership because the callers are dirty and the landing sits inside a wider mixed command-style lane
- other outside lures: `5E54` from `C3:3886`, `5E80` from `C3:A68A`
- top local islands:
  - `5E28..5E40 (RTS)`, score=4, ascii=0.20, branches=2
  - `5E00..5E17 (RTS)`, score=4, ascii=0.46, calls=4, branches=1
  - `5E87..5E90 (RTS/RTS)`, score=4, ascii=0.50, calls=2, branches=1
- result: most xref-active early page of the run, still mixed and unsupported

## C3:5F00..5FFF
- page metrics: ascii=0.20, zero=0.18, ff=0.01, repeated_pair=0.04
- no true outside `JSR`/`JMP` ownership survived
- strongest visible traffic is branch-fed: `5F24` with two hits, plus `5F39` with two local hits
- a tiny `RTL` stub appears at `5F58`, but it is isolated and not owner-worthy
- top local island:
  - `5F00..5F08 (RTS)`, score=3, ascii=0.89, branches=1
- result: lower-ascii page that still behaves more like packed control/data than callable code

## C3:6000..60FF
- page metrics: ascii=0.20, zero=0.12, ff=0.04, repeated_pair=0.02
- strongest true external multi-hit lure of the whole continuation: `60AB` with two low-risk outside `JSR` callers (`C3:30BC`, `C3:591D`)
- it still fails immediately because the landing byte is `02` (`COP` / barrier-style start), not a defendable routine boundary
- next strongest lure: `6010` with two outside hits (`C3:2F41 -> JSR $6010`, `C3:68CE -> JMP $6010`), but the surrounding bytes still read like packed command/table material
- other outside lures: `6060`, `6069`, `60A0`
- top local island:
  - `6040..6047 (RTS)`, score=4, ascii=0.12, branches=1
- result: lowest-ascii page in the block and still a false dawn; the outside-call pressure is real, but the landings do not own themselves

## C3:6100..61FF
- page metrics: ascii=0.19, zero=0.14, ff=0.03, repeated_pair=0.05
- outside `JSR` lures are sparse: `6108` from `C3:7368`, `6151` from `C3:B1DA`, `6178` from `C3:A149`
- cleaner visible control endpoint: `616E` from `C3:1B8B -> BRL $616E`
- top local island:
  - `6121..6129 (RTS)`, score=4, ascii=0.11, branches=1
- result: cleaner-looking page, but still only as local control splinters rather than caller-backed ownership

## C3:6200..62FF
- page metrics: ascii=0.21, zero=0.11, ff=0.01, repeated_pair=0.04
- strongest outside `JSR` lures: `6244` from `C3:B0F3` and `62D1` from `C3:CC4A`
- `62D1` is especially telling because the hit lands directly on `RTS` (`60`), which makes it return-stub bait rather than a recoverable owner
- busiest visible target: `621F`, with two branch-fed hits and one outside source
- top local island:
  - `62CC..62D1 (RTS)`, score=4, ascii=0.17, calls=0, branches=0
- result: mixed control page with one tiny late return-stub lure, no true owner

## C3:6300..63FF
- page metrics: ascii=0.25, zero=0.07, ff=0.02, repeated_pair=0.01
- strongest outside callable lure: `6360` from `C3:4708 -> JMP $6360`
- strongest local island of the whole continuation:
  - `6334..6345 (RTS)`, score=6, ascii=0.17, calls=1, branches=2
- that island still fails owner promotion because it is a self-contained splinter inside a wider mixed page, not a caller-backed true start
- other outside lures: `6390` from `C3:3BD3`, `631C` from `C3:D3BC`
- result: best local helper-like pocket of the run, still unsupported as a real owner/helper start

## C3:6400..64FF
- page metrics: ascii=0.22, zero=0.11, ff=0.03, repeated_pair=0.01
- strongest outside lures: `64AD` from `C3:65F2`, `64CA` from `C3:3D24 -> JMP $64CA`, `64DD` from `C3:3DB1 -> JMP $64DD`
- `64CA` is another obvious false landing because the first byte is `02`, not a stable callable start
- the page contains a short code-looking splinter around `6430..643F`, but it remains embedded inside wider mixed material and does not defend ownership
- top local islands:
  - `648A..6490 (RTS)`, score=3, ascii=0.29
  - `6445..6449 (RTS)`, score=2, ascii=0.40
- result: late-block page with a few tempting internal splinters, still not enough to promote code

## Bottom line
Across `C3:5B00..64FF`, the seam produced four main temptations and rejected all of them honestly:
- `5E3C` as the strongest early-block multi-hit external false dawn
- `60AB` as the strongest true external multi-hit lure of the continuation, still dead on arrival because it starts on `02`
- `6010` as the next-cleanest outside-call lure, still resolving as packed mixed command/table material
- `6334..6345` as the strongest local helper-like island, still not a defendable owner/helper start

No new defendable owner/helper promotions survived.
