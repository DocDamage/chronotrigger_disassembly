# Chrono Trigger Disassembly — Raw Seam Report for C3:AB00..B4FF

This file preserves the seam-facing evidence for the next continuation after `C3:AB00..`. It is intentionally terse and page-oriented.

## C3:AB00..ABFF
- page metrics: ascii=0.42, zero=0.11, ff=0.00, repeated_pair=0.03
- cleanest outside lure:
  - `AB48` from `C3:09FD -> JSR $AB48`, caller risk=low, target risk=medium
- other outside lures:
  - `AB02` from `C3:181A -> JSR $AB02`, caller risk=medium, target risk=high
  - `ABA2` from `C3:5D51 -> JSR $ABA2`, caller risk=medium, target risk=high
- strongest local islands:
  - `ABD8..ABE4`, score=4, ascii=0.69, calls=1, branches=2, returns=2
  - `ABE8..ABF2`, score=3, ascii=0.46, branches=2, returns=1, stackish=1
- page also contains small BRA landing-pad veneers at `ABA8` and `ABE5`
- result: mixed early page with one reasonably clean single-hit lure and no defendable owner boundary

## C3:AC00..ACFF
- page metrics: ascii=0.33, zero=0.11, ff=0.01, repeated_pair=0.05
- visible outside lures:
  - `AC16` from `C3:324F -> JSR $AC16`, caller risk=medium, target risk=high, landing byte=`00`
  - `AC00` from `C3:5A44 -> JSR $AC00`, caller risk=high, target risk=high
  - `AC30` from `C3:6D5F -> JSR $AC30`, caller risk=high, target risk=high
- strongest local island:
  - `AC00..AC0B`, score=2, ascii=0.58, branches=2, returns=3
- notable tiny veneer candidates:
  - `AC2A = RTL` stub
  - `AC35 = RTL` stub
  - `AC6E` and `ACF0` as BRA landing pads
- result: noisy mixed page whose most visible outside lure still dies on a `00` landing

## C3:AD00..ADFF
- page metrics: ascii=0.29, zero=0.12, ff=0.00, repeated_pair=0.09
- strongest mid-early outside lure:
  - `AD21` from `C3:6A66 -> JSR $AD21`, caller risk=low, target risk=low, landing byte=`05`
- other outside lures:
  - `AD00` with 2 outside hits (`C3:4026 -> JSR $AD00`, `C3:18EA -> JMP $AD00`), but the landing byte is `00`
  - `ADA5` from `C3:6AE5 -> JSR $ADA5`, caller risk=medium, target risk=medium
  - `AD23` from `C3:4928 -> JSR $AD23`, caller risk=high, target risk=low, landing byte=`02`
- strongest local islands:
  - `ADB9..ADCD`, score=6, ascii=0.29, calls=2, branches=3, returns=2
  - `ADDB..ADE9`, score=4, ascii=0.47, calls=2, branches=3, returns=2
- notable veneer field:
  - `AD36 = RTL` stub
  - multiple BRA landing pads around `AD40`, `ADE5`, `ADE8`, and `ADF1`
- result: one genuinely clean single-hit lure plus one strong local cluster, still not enough to defend a caller-backed start

## C3:AE00..AEFF
- page metrics: ascii=0.30, zero=0.17, ff=0.00, repeated_pair=0.09
- strongest outside multi-hit lure:
  - `AE00` with 2 outside `JSR` hits (`C3:6A00`, `C3:8730`), caller risks high/high, target risk=medium
- other outside lures:
  - `AE04` from `C3:4B7F -> JSR $AE04`, caller risk=high, target risk=medium
  - `AE30` from `C3:5A48 -> JSR $AE30`, caller risk=high, target risk=high
- strongest local island:
  - `AE03..AE10`, score=5, ascii=0.43, calls=1, branches=7, returns=1, stackish=1
- page also contains several BRA landing-pad veneers around `AE00`, `AE08`, `AE11`, and `AE74`
- result: structurally active page with one double-hit lure and one good local pocket, still too mixed to promote honestly

## C3:AF00..AFFF
- page metrics: ascii=0.34, zero=0.07, ff=0.01, repeated_pair=0.18
- strongest outside multi-hit lure:
  - `AF48` with 2 outside `JSR` hits (`C3:0549`, `C3:6480`), best pairing medium/medium
- dirtier outside lures:
  - `AF10` from `C3:839A -> JSR $AF10`, landing byte=`00`
  - `AF00` from `C3:34FB -> JSR $AF00`, caller risk=high, target risk=high
- strongest local islands:
  - `AF57..AF60`, score=5, ascii=0.60, calls=1, branches=3, returns=3, stackish=1
  - `AF4F..AF55`, score=5, ascii=0.29, branches=1, returns=1, stackish=1
- result: one real outside double-hit lure plus several sharp local splinters, still not enough to defend a stable owner boundary

## C3:B000..B0FF
- page metrics: ascii=0.37, zero=0.06, ff=0.00, repeated_pair=0.05
- cleanest outside lure:
  - `B005` from `C3:CCE2 -> JSR $B005`, caller risk=low, target risk=high
- other outside lures:
  - `B02C` from `C3:9AAF -> JSR $B02C`, caller risk=high, target risk=medium
  - `B00A` from `C3:CBF6 -> JSR $B00A`, landing byte=`01`
  - `B092` from `C3:3E65 -> JSR $B092`, caller risk=high, target risk=high
- strongest local islands:
  - `B067..B074`, score=4, ascii=0.21, branches=2, returns=2
  - `B067..B073`, score=4, ascii=0.15, branches=2, returns=1
- notable tiny veneer candidates:
  - BRA landing pads around `B017`, `B064`, `B082`, and `B0C0`
  - `B0F8 = RTL` stub
- result: modestly cleaner page with one neat local pocket, still lacking caller-backed traction

## C3:B100..B1FF
- page metrics: ascii=0.41, zero=0.04, ff=0.01, repeated_pair=0.06
- visible outside lures:
  - `B131` from `CA:31C2 -> JML $C3B131`, caller risk=medium, target risk=medium
  - `B101` from `C3:56B4 -> JMP $B101`, caller risk=high, target risk=medium, landing byte=`00`
  - `B170` from `C3:970F -> JSR $B170`, caller risk=high, target risk=high, landing byte=`09`
- strongest local islands:
  - `B147..B159`, score=4, ascii=0.53, calls=2, branches=4, returns=2
  - `B16E..B175`, score=3, ascii=0.38, calls=1, returns=1
- page also contains BRA landing-pad veneers at `B13D` and `B1D6`
- result: cross-bank attention plus internal structure, still no defendable owner start

## C3:B200..B2FF
- page metrics: ascii=0.41, zero=0.07, ff=0.01, repeated_pair=0.02
- strongest outside multi-hit lure:
  - `B260` with 2 outside `JSR` hits (`C3:0BA9`, `C3:5FDB`), both high/high
- strongest local islands:
  - `B22B..B231`, score=3, ascii=0.57, calls=1, returns=1
  - `B29B..B2B0`, score=2, ascii=0.64, branches=3, returns=5
- notable veneer field:
  - BRA landing pads around `B204`, `B21A`, `B228`, `B26D`, and `B28C`
- result: one dirty double-hit lure and a noisy local cluster, still far short of promotion

## C3:B300..B3FF
- page metrics: ascii=0.39, zero=0.02, ff=0.01, repeated_pair=0.04
- cleanest outside lure:
  - `B305` from `C3:5B58 -> JSR $B305`, caller risk=medium, target risk=medium
- other outside lure:
  - `B3A2` from `C3:093D -> JSR $B3A2`, caller risk=medium, target risk=high
- strongest local islands:
  - `B3BF..B3D7`, score=5, ascii=0.44, calls=1, branches=1, returns=1, stackish=1
  - `B364..B37C`, score=3, ascii=0.52, branches=4, returns=2, stackish=1
- page also contains a dense late veneer field around `B389`, `B3DF`, `B3E2`, `B3E9`, and `B3EC`
- result: strongest late local cluster of the continuation, still unsupported as a caller-backed owner/helper start

## C3:B400..B4FF
- page metrics: ascii=0.29, zero=0.13, ff=0.00, repeated_pair=0.04
- cleanest late outside lures:
  - `B409` from `C3:BC42 -> JSR $B409`, caller risk=medium, target risk=low
  - `B414` from `C3:600C -> JSR $B414`, caller risk=medium, target risk=low
- no local islands survived strongly enough to matter
- only notable veneer candidate:
  - `B4A9 = RTL` stub
- result: quiet late page with two decent single-hit lures, still no stable owner boundary

## Bottom line
Across `C3:AB00..B4FF`, the seam produced five main temptations and rejected all of them honestly:
- `AD21` plus `ADB9..ADCD` as the strongest early outside/local near-miss combination
- `AE00` and `AF48` as the main early outside multi-hit false dawns
- `A28B` as the prior continuation’s busiest outside-call page was not followed by a breakout here; the seam stayed mixed and uneven
- `B3BF..B3D7` as the strongest late local island cluster of the continuation
- `B409 / B414` as the cleanest late single-hit outside lures, still short of a defendable owner boundary

No new defendable owner/helper promotions survived.
