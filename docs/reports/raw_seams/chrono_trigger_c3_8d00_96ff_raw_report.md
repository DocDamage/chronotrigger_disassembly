# Chrono Trigger Disassembly — Raw Seam Report for C3:8D00..96FF

This file preserves the seam-facing evidence for the next continuation after `C3:8D00..`. It is intentionally terse and page-oriented.

## C3:8D00..8DFF
- page metrics: ascii=0.28, zero=0.16, ff=0.00, repeated_pair=0.09
- strongest early outside multi-hit lure:
  - `8D80` with 2 outside `JSR` hits (`C3:07DF`, `C3:08A1`)
- this is the cleanest early double-hit target of the continuation, but target-side bytes still stay only medium-risk and the page never stabilizes into a defendable owner boundary
- other outside lures:
  - `8D00` with 2 outside `JSR` hits from `C3:3937` and `C3:3C95`, but target-side risk stays high
  - `8DAD` from `C3:0928 -> JSR $8DAD`, caller risk=medium, target risk=low
  - `8D0A` from `C3:3FFC -> JMP $8D0A`
- no local islands survived strongly enough to matter
- result: modestly cleaner early page with one real double-hit lure, still no caller-backed owner

## C3:8E00..8EFF
- page metrics: ascii=0.34, zero=0.14, ff=0.01, repeated_pair=0.08
- outside callable traffic is all single-hit and mixed:
  - `8E20` from `C3:091E -> JSR $8E20`, caller risk=medium, target risk=low
  - `8E09` from `C3:13EB -> JSR $8E09`, caller risk=medium, target risk=medium
  - `8E8E` from `C3:42C7 -> JSR $8E8E`, caller risk=medium, target risk=medium
- obvious false landing:
  - `8E14` from `C3:22A8 -> JSR $8E14`, but the landing byte is `00`
- page also contains several tiny BRA landing-pad style veneers around `8E27`, `8E29`, `8E37`, `8E43`, `8EC2`, and `8ED9`
- result: xref-light mixed page with one cleaner single-hit lure and no owner-worthy start

## C3:8F00..8FFF
- page metrics: ascii=0.35, zero=0.09, ff=0.00, repeated_pair=0.05
- visible outside lures are sparse:
  - `8FCE` from `C3:161D -> JSR $8FCE`, caller risk=low, target risk=high
  - `8FE4` from `C3:44EC -> JSR $8FE4`, caller risk=medium, target risk=high
  - `8F00` from `C3:59BC -> JSR $8F00`, caller risk=high, target risk=high, landing byte=`01`
- strongest local island:
  - `8F10..8F1C (RTS)`, score=4, ascii=0.15
- other local pockets exist late in the page, but they are either highly ASCII-heavy or tiny return clusters without caller-backed starts
- result: sparse mixed page with one clean-looking local splinter, still no defendable owner boundary

## C3:9000..90FF
- page metrics: ascii=0.42, zero=0.03, ff=0.00, repeated_pair=0.05
- busiest outside-call page of the continuation
- strongest outside multi-hit lure:
  - `90A7` with 2 outside `JSR` hits (`C3:301A`, `C3:57A9`)
- other outside lures:
  - `9000` from `C3:4800 -> JSR $9000`, caller risk=low, target risk=high
  - `90FC` from `C3:5FF3 -> JSR $90FC`, caller risk=medium, target risk=medium
  - `9079` from `C3:6929 -> JSR $9079`
- strongest local islands:
  - `906B..9083`, score=4, calls=2, branches=6
  - `9075..908D`, score=4, calls=1, branches=7, returns=3
- result: xref-busy page with multiple real temptations, still too mixed and uneven to promote code

## C3:9100..91FF
- page metrics: ascii=0.38, zero=0.03, ff=0.00, repeated_pair=0.06
- outside callable pressure is very thin:
  - `9127` from `C3:B39C -> JSR $9127`, caller risk=medium, target risk=medium
  - `9195` from `C3:6302 -> JMP $9195`, caller risk=high, target risk=high
- strongest local island cluster of the continuation:
  - `9199..91B1`, score=5, ascii=0.20, branches=3, returns=2
  - `91E0..91F7`, score=5, ascii=0.38, calls=2, branches=5
- the page feels structured locally, but almost all of that structure is self-contained and unsupported by caller-backed starts
- result: best internal-control page of the run so far, still no true owner/helper start

## C3:9200..92FF
- page metrics: ascii=0.33, zero=0.05, ff=0.00, repeated_pair=0.08
- no visible outside callable landings survived into this page
- no local islands survived scoring strongly enough to matter
- the page reads more like packed mixed command/control material than a recoverable callable lane
- result: quiet mid-block page with no caller-backed traction at all

## C3:9300..93FF
- page metrics: ascii=0.38, zero=0.04, ff=0.01, repeated_pair=0.04
- only visible outside lure:
  - `935F` from `C3:B7D7 -> JSR $935F`, caller risk=high, target risk=medium
- strongest local islands:
  - `93BF..93C7 (RTS)`, score=4, ascii=0.44, calls=1, branches=2
  - `9334..933A (RTS)`, score=4, ascii=0.57, calls=1, branches=3
- notable tiny BRA landing-pad style veneers cluster around `930D`, `9322`, `932B`, `932E`, `9332`, and `9339`
- result: sparse page with one dirty outside lure and several noisy internal splinters, still not owner-worthy

## C3:9400..94FF
- page metrics: ascii=0.41, zero=0.08, ff=0.00, repeated_pair=0.05
- no visible outside callable landings survived into this page
- cleanest isolated local pocket:
  - `94BA..94C4 (RTS)`, score=4, ascii=0.09
- despite that unusually clean local island, the page still lacks any caller-backed true start
- page also contains tiny BRA landing pads around `9461` and `94B0`
- result: no outside pressure and one neat local splinter, still not enough to promote code

## C3:9500..95FF
- page metrics: ascii=0.29, zero=0.14, ff=0.00, repeated_pair=0.04
- cleanest-looking page of the continuation overall
- strongest local helper-like island of the run:
  - `957B..958B (RTS)`, score=7, ascii=0.29, calls=1, branches=2, returns=2
- outside lures are all single-hit:
  - `9585` from `C3:1379 -> JSR $9585`, caller risk=medium, target risk=medium
  - `9590` from `C3:6334 -> JSR $9590`, caller risk=medium, target risk=medium
  - `95F2` from `C3:4C44 -> JSR $95F2`, caller risk=medium, target risk=medium
  - `9522` from `C3:765C -> JSR $9522`, caller risk=high, target risk=low
- the page feels cleaner and more structured than most of the block, but the best evidence is still local-island evidence rather than caller-backed ownership
- result: strongest local-helper false dawn of the continuation, still no defendable owner start

## C3:9600..96FF
- page metrics: ascii=0.35, zero=0.07, ff=0.01, repeated_pair=0.05
- strongest late-block outside multi-hit lure:
  - `960A` with 2 outside `JSR` hits (`C3:8AE6`, `C3:8AEB`)
- cleanest late outside single-hit lure:
  - `9613` from `C3:5866 -> JSR $9613`, caller risk=medium, target risk=low
- other outside lures:
  - `96A2` from `C3:5827 -> JSR $96A2`, caller risk=low, target risk=high
  - `9618` from `C3:AFD3 -> JSR $9618`, landing byte=`01`
  - `96AD` from `C3:0AA4 -> JSR $96AD`, caller risk=high, target risk=high
- strongest local islands:
  - `960C..9624`, score=6, ascii=0.24, calls=1, branches=3, returns=2
  - `9609..961F`, score=4, ascii=0.30, calls=1, branches=2, returns=2
- result: late block ends with one real double-hit lure and one strong local cluster, still short of a defendable owner/helper promotion

## Bottom line
Across `C3:8D00..96FF`, the seam produced five main temptations and rejected all of them honestly:
- `8D80` as the cleanest early double-hit outside lure
- `90A7` as the busiest outside-call lure on the most xref-active page
- `9199..91B1` plus `91E0..91F7` as the strongest internal-control island cluster of the continuation
- `957B..958B` as the strongest local helper-like island of the run
- `960A` plus `960C..9624` as the cleanest late-block outside/local combination, still not enough to justify promotion

No new defendable owner/helper promotions survived.
