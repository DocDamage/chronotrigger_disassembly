# Chrono Trigger Disassembly — Raw Seam Report for C3:9700..A0FF

This file preserves the seam-facing evidence for the next continuation after `C3:9700..`. It is intentionally terse and page-oriented.

## C3:9700..97FF
- page metrics: ascii=0.34, zero=0.07, ff=0.00, repeated_pair=0.02
- cleanest outside lure on the page:
  - `97B5` from `C3:64CB -> JSR $97B5`, caller risk=low, target risk=low
- other outside lures:
  - `9745` from `C3:646A -> JSR $9745`, caller risk=medium, target risk=medium
  - `9710` from `C3:A682 -> JSR $9710`, caller risk=high, target risk=high
  - `9700` from `C3:A686 -> JSR $9700`, caller risk=high, target risk=high
- strongest local island:
  - `97B1..97C9 (RTS)`, score=7, ascii=0.28, calls=2, branches=3, stackish=2
- page also contains small BRA landing-pad style veneers around `9712` and `97DE`
- result: strongest early page of the continuation, but the best evidence is still split between one clean outside hit and one strong local splinter rather than one caller-backed true start

## C3:9800..98FF
- page metrics: ascii=0.34, zero=0.14, ff=0.00, repeated_pair=0.10
- only visible outside lure:
  - `9897` from `C3:6454 -> JSR $9897`, caller risk=high, target risk=low
- strongest local islands:
  - `9830..9838 (RTS)`, score=3, ascii=0.44, stackish=2
  - `98D6..98DC (RTS)`, score=3, ascii=0.29
- page also contains small BRA landing-pad style veneers around `984A` and `9893`
- result: structurally mixed page with one interesting outside landing, still nowhere near a defendable owner boundary

## C3:9900..99FF
- page metrics: ascii=0.29, zero=0.12, ff=0.00, repeated_pair=0.07
- strongest outside multi-hit lure:
  - `9900` with 2 outside `JSR` hits (`C3:627D`, `C3:6C91`)
- that still fails because the landing byte is `09`, target-side bytes stay high-risk, and the page never resolves into a stable callable boundary
- strongest local islands:
  - `998A..999E`, score=4, ascii=0.52, calls=2, branches=3, returns=2
  - `99AC..99C4`, score=3, ascii=0.40, branches=5, returns=1, stackish=1
- result: first real double-hit outside pressure of the continuation, still mixed and unsupported

## C3:9A00..9AFF
- page metrics: ascii=0.30, zero=0.11, ff=0.01, repeated_pair=0.05
- cleanest outside lure:
  - `9AFF` from `C3:31A0 -> JSR $9AFF`, caller risk=low, target risk=medium
- dirtier outside lures:
  - `9A70` from `C3:2CB1 -> JSR $9A70`, caller risk=high, target risk=high
  - `9ABA` from `C3:4A49 -> JSR $9ABA`, caller risk=high, target risk=high
- strongest local islands:
  - `9A60..9A68`, score=4, ascii=0.44, calls=1, branches=1, returns=2
  - `9A37..9A3C`, score=2, ascii=0.33, branches=1, returns=1
- page also contains small BRA landing-pad style veneers around `9A48` and `9A6D`
- result: modestly cleaner page with one decent late single-hit lure, still no honest owner start

## C3:9B00..9BFF
- page metrics: ascii=0.32, zero=0.11, ff=0.01, repeated_pair=0.06
- cleanest outside lure:
  - `9B80` from `C3:6671 -> JMP $9B80`, caller risk=low, target risk=medium
- other outside lure:
  - `9B0B` from `C3:5891 -> JSR $9B0B`, caller risk=medium, target risk=high
- strongest local islands:
  - `9B76..9B80`, score=5, ascii=0.45, calls=2, branches=1, stackish=1
  - `9B95..9BA8`, score=4, ascii=0.55, calls=1, branches=6
- page also contains small BRA landing-pad style veneers around `9B04` and `9B07`
- result: one good late landing plus one good local splinter, still not enough to defend a true owner/helper start

## C3:9C00..9CFF
- page metrics: ascii=0.36, zero=0.10, ff=0.00, repeated_pair=0.04
- visible outside lures are busy but dirty:
  - `9C00` with 2 outside `JSR` hits (`C3:2FBA`, `C3:37CC`), landing byte=`00`
  - `9C2C` from `C3:A3C2 -> JSR $9C2C`, caller risk=high, target risk=high
  - `9C18` from `C3:D767 -> JSR $9C18`, caller risk=high, target risk=high
- strongest local pockets:
  - `9CAA..9CC2`, score=3, ascii=0.36, branches=3, returns=2, stackish=4
  - `9CA7..9CB9`, score=3, ascii=0.42, branches=2, returns=1, stackish=2
- page also contains a BRA landing pad at `9C60` and an `RTL` stub at `9C6F`
- result: busiest dirty page of the continuation, still pure false pressure rather than a recoverable code page

## C3:9D00..9DFF
- page metrics: ascii=0.32, zero=0.06, ff=0.01, repeated_pair=0.05
- only visible outside lure:
  - `9D6A` from `C3:6C9B -> JSR $9D6A`, caller risk=medium, target risk=high, landing byte=`02`
- strongest local islands:
  - `9DC7..9DDF`, score=2, ascii=0.32, branches=5, returns=1
  - `9DBB..9DC6`, score=2, ascii=0.50, branches=1, returns=1
- page also contains small BRA landing-pad style veneers around `9DDA` and `9DFA`
- result: thin page with one obvious false landing and no caller-backed traction

## C3:9E00..9EFF
- page metrics: ascii=0.35, zero=0.04, ff=0.00, repeated_pair=0.06
- cleanest single outside lure of the continuation:
  - `9E1C` from `C3:4510 -> JSR $9E1C`, caller risk=low, target risk=low
- strongest local islands:
  - `9E67..9E6E`, score=4, ascii=0.25, branches=3, returns=1
  - `9E81..9E99`, score=3, ascii=0.40, branches=9, returns=2, stackish=1
- page also contains a dense veneer field of small BRA landing pads, including `9E07` and `9E63`
- result: probably the cleanest single outside landing in the whole continuation, but still only one hit inside a page that stays mixed and branch-fed

## C3:9F00..9FFF
- page metrics: ascii=0.28, zero=0.10, ff=0.02, repeated_pair=0.05
- outside callable pressure is split across three weak lures:
  - `9F59` from `C3:6BAD -> JSR $9F59`, caller risk=medium, target risk=medium
  - `9F10` from `C3:370B -> JSR $9F10`, caller risk=medium, target risk=high
  - `9F68` from `C3:0C73 -> JSR $9F68`, caller risk=high, target risk=low, landing byte=`00`
- strongest local island:
  - `9F30..9F3B`, score=4, ascii=0.50, calls=1, branches=1, returns=1
- page also contains small BRA landing-pad style veneers around `9F5C` and `9F77`
- result: no real owner candidate; the page stays split between middling outside pressure and one modest internal splinter

## C3:A000..A0FF
- page metrics: ascii=0.34, zero=0.12, ff=0.00, repeated_pair=0.08
- strongest outside-call page of the continuation
- strongest outside multi-hit lure:
  - `A03D` with 2 outside hits (`C3:68BB -> JSR $A03D`, `C3:6963 -> JMP $A03D`), caller risks low/medium, target risk=medium
- other outside lures:
  - `A009` from `C3:0912 -> JSR $A009`, caller risk=medium, target risk=high
  - `A007` from `C3:5B0F -> JSR $A007`, caller risk=medium, target risk=high
  - `A05A` from `C3:1E42 -> JSR $A05A`, caller risk=low, target risk=medium, landing byte=`01`
  - `A0B5` from `C3:6AE7 -> JSR $A0B5`, caller risk=medium, target risk=medium
  - `A0BF` from `C3:7D97 -> JSL $C3A0BF`, caller risk=very_high, target risk=low
- strongest local islands:
  - `A0ED..A0FB`, score=4, ascii=0.40, calls=1, branches=3, returns=3
  - `A0ED..A0F5`, score=4, ascii=0.33, calls=1, branches=2, returns=2
- page also contains small BRA landing-pad style veneers around `A056` and `A0B3`
- result: busiest page of the run with the cleanest outside multi-hit lure at `A03D`, still not enough to justify a defendable owner/helper promotion

## Bottom line
Across `C3:9700..A0FF`, the seam produced five main temptations and rejected all of them honestly:
- `97B5` plus `97B1..97C9` as the strongest early outside/local near-miss combination
- `9900` as the first true outside multi-hit false dawn of the continuation
- `9E1C` as the cleanest single outside lure in the block
- `9B80` and its nearby `9B76..9B80` local splinter as the best mid-block outside/local pairing
- `A03D` as the cleanest late-block outside multi-hit lure, still short of a defendable owner boundary

No new defendable owner/helper promotions survived.
