# Chrono Trigger Disassembly — Raw Seam Report for C3:6500..6EFF

This file preserves the seam-facing evidence for the next continuation after `C3:6500..`. It is intentionally terse and page-oriented.

## C3:6500..65FF
- page metrics: ascii=0.23, zero=0.12, ff=0.00, repeated_pair=0.07
- cleanest visible outside landing: `6505` from `C3:BC90 -> JMP $6505`, caller risk=medium, target risk=low
- other outside lures: `6500` from `C3:660A -> JSR $6500`, `65AE` from `C3:3DD9 -> JSR $65AE`, `651A` from `C3:C2CC -> JSR $651A`
- none of the landings defend a routine boundary; `651A` starts on `00`, and `6500/6505` still read like embedded mixed material rather than stable page-top ownership
- top local island:
  - `65D5..65DA (RTS)`, score=3, ascii=0.17
- result: cleaner-looking page than some earlier seam pages, still no caller-backed owner

## C3:6600..66FF
- page metrics: ascii=0.32, zero=0.11, ff=0.01, repeated_pair=0.03
- strongest true external multi-hit lure: `66B0` with two outside `JSR` hits (`C3:3B44`, `C3:577B`)
- that still fails because both callers are high-risk and the landing sits inside wider mixed material
- strongest local island of the continuation:
  - `6641..6649 (RTS)`, score=6, ascii=0.22, calls=1, branches=1
- notable tiny veneer candidate:
  - `6697..669A = JSR $6F50 / RTS`
- result: active mixed page with the best local helper-like splinter of the run, still no defendable owner/helper start

## C3:6700..67FF
- page metrics: ascii=0.23, zero=0.10, ff=0.00, repeated_pair=0.05
- only visible outside callable landing: `6709` from `C3:BC7D -> JSR $6709`
- strongest local pocket:
  - `6730..6740 (RTS)`, score=4, ascii=0.53, calls=1, branches=2
- the page stays mostly local-control and mixed-content despite the lower page-level ASCII
- result: sparse page with one outside lure and no stable owner boundary

## C3:6800..68FF
- page metrics: ascii=0.19, zero=0.11, ff=0.01, repeated_pair=0.02
- page looks cleaner at first glance, but the outside landings stay weak or dirty
- notable outside lures: `6808` from `C3:53E9`, `68AA` from `C3:4BB1`, `68D4` from `C3:4D4A`, `6860` from `C3:1EC6`
- `6808` dies immediately as a start because it lands on `00`
- top local islands:
  - `684E..6857 (RTS/RTS)`, score=3, ascii=0.40
  - `683A..683E (RTS)`, score=2, ascii=0.60
- result: low-ASCII false-dawn page, still mixed and unsupported

## C3:6900..69FF
- page metrics: ascii=0.32, zero=0.12, ff=0.00, repeated_pair=0.08
- outside callable lures are thin: `6918`, `69A5`, `69AA`
- both `69A5` and `69AA` start on `00`, which kills them as defendable routine starts
- top local island:
  - `6931..6939 (RTS)`, score=4, ascii=0.22
- result: sparse mixed page with no real owner candidate

## C3:6A00..6AFF
- page metrics: ascii=0.25, zero=0.09, ff=0.00, repeated_pair=0.07
- busiest visible page of the continuation by raw outside pressure
- strongest cleaner-looking outside callable lures:
  - `6A95` from `C3:89E8 -> JMP $6A95`, caller risk=medium, target risk=low
  - `6AAB` from `C3:3FBA -> JSR $6AAB`, caller risk=medium, target risk=low
- strongest page-top pressure: `6A00` from `C3:FC6B -> JSR $6A00`, but the target-side bytes still grade high-risk
- obvious false landing inside the same page: `6A45` starts on `02`
- several other outside lures (`6A53`, `6ACD`, `6AF6`) never stabilize into owner-worthy boundaries
- top local islands:
  - `6AA9..6AB2 (RTS)`, score=4, ascii=0.20, branches=2
  - `6A2F..6A34 (RTS)`, score=3, ascii=0.67, calls=3
- result: xref-busy mixed page that feels executable in spots but still reads more like packed command/control material than recoverable standalone code

## C3:6B00..6BFF
- page metrics: ascii=0.30, zero=0.09, ff=0.00, repeated_pair=0.00
- cleanest visible lure: `6B15` from `C3:AD34 -> JSR $6B15`, caller risk=medium, target risk=low
- other outside landing: `6BF9` from `C3:423D -> JSR $6BF9`, target risk=high
- top local island:
  - `6BDA..6BEB (RTS)`, score=4, ascii=0.11
- result: one reasonably clean landing plus one decent late local pocket, still not enough to promote code

## C3:6C00..6CFF
- page metrics: ascii=0.30, zero=0.14, ff=0.00, repeated_pair=0.05
- cleanest outside lure: `6C71` from `C3:42B6 -> JSR $6C71`, caller risk=medium, target risk=low
- dirtier page-top-style lure: `6C20` from `C3:8F33 -> JSR $6C20`, caller risk=high, target risk=high
- strongest local islands:
  - `6CAF..6CB5 (RTS)`, score=5, ascii=0.29, calls=1
  - `6C61..6C70 (RTS)`, score=4, ascii=0.19, branches=3
- result: another page with code-looking splinters, but the outside landings still do not defend true ownership

## C3:6D00..6DFF
- page metrics: ascii=0.47, zero=0.21, ff=0.00, repeated_pair=0.20
- this is the dirtiest page of the continuation by far
- only visible outside landing: `6D8B` from `C3:5765 -> JSR $6D8B`, caller risk=medium, target risk=high
- local islands exist, but they are all embedded in an overwhelmingly text/data-heavy page
- result: obvious mixed-content contamination, not a recoverable code page

## C3:6E00..6EFF
- page metrics: ascii=0.23, zero=0.14, ff=0.05, repeated_pair=0.11
- strongest late-block false dawn: `6E1B` with two outside `JSR` hits (`C3:DB25`, `C3:DC78`)
- even that fails because both callers are high-risk and the landing still sits in mixed bytes rather than a defendable boundary
- other outside lure: `6E42` from `C3:4B68 -> JSR $6E42`
- no local islands survived strongly enough to matter
- result: late block ends with another multi-hit false dawn and still no owner promotion

## Bottom line
Across `C3:6500..6EFF`, the seam produced four main temptations and rejected all of them honestly:
- `66B0` as the strongest true external multi-hit lure of the early continuation
- `6641..6649` as the strongest local helper-like island of the run
- `6A95 / 6AAB` as the cleanest-looking single-hit outside callable lures on the busiest page
- `6E1B` as the strongest late-block multi-hit false dawn

No new defendable owner/helper promotions survived.
