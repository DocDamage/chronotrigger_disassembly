# Chrono Trigger Disassembly — Raw Seam Report for C3:3D00..46FF

This file preserves the seam-facing evidence for the third continuation of session 13. It is intentionally terse and page-oriented.

## C3:3D00..3DFF
- page metrics: ascii=0.29, zero=0.08, ff=0.01, repeated_pair=0.03
- strongest external-looking target: `3DE5` with one comparatively cleaner cross-page `BRA` from `C3:3E54`
- dirtier external pressure also existed into `3DF0`, `3DD2`, `3DC9`, and `3DB9`
- best local islands: `3DE2..3DEA (RTS)`, `3D35..3D42 (RTI)`, `3D23..3D2C (RTS)`
- result: mixed branch/control blob, no defendable owner boundary

## C3:3E00..3EFF
- page metrics: ascii=0.33, zero=0.14, ff=0.00, repeated_pair=0.04
- strongest external target on paper: `3ED3` with 2 external `JSR` hits (`C3:1C1E`, `C3:597A`), both dirty
- cleaner single-hit branch pressure existed into `3EE5`, `3ECE`, `3ECD`, and `3E2F`
- best local island: `3E5E..3E69 (RTS)`
- result: mixed init/control material, no stable owner start

## C3:3F00..3FFF
- page metrics: ascii=0.35, zero=0.04, ff=0.00, repeated_pair=0.02
- strongest external target: `3F90` with one comparatively cleaner `JSR` from `C3:62A5`
- other visible external targets: `3FD1`, `3FB0`, `3F05`
- strongest local islands: `3F24..3F43 (RTI)`, `3F57..3F6D (RTI)`, `3F0E..3F20 (RTS)`
- result: more executable-looking than nearby pages, but still no defendable owner

## C3:4000..40FF
- page metrics: ascii=0.29, zero=0.14, ff=0.03, repeated_pair=0.05
- heaviest external target field of the continuation: `4000`, `4018`, `4019`, `4008`, `405F`, `40F0`, `40A0`, `4025`
- strongest count target: `4000` with 6 external hits, all dirty enough to fail promotion
- best local island: `4028..4035 (RTS)`
- result: xref-saturated dispatch/table-like material, not a defendable owner lane

## C3:4100..41FF
- page metrics: ascii=0.34, zero=0.08, ff=0.01, repeated_pair=0.02
- cleanest external target: `4109` with one cleaner `JSR` from `C3:51DF`
- noisier external pressure also existed into `4159`, `41B5`, `41A5`, `4181`, and `4160`
- strongest local island: `41C0..41DF (RTS)`
- result: mixed control/data page, visible late hits still resolve as interior/tail bait

## C3:4200..42FF
- page metrics: ascii=0.34, zero=0.07, ff=0.00, repeated_pair=0.00
- cleanest external target: `4274` with one comparatively cleaner `JSR` from `C3:68EF`
- `424F` drew 2 external `JSR` hits (`C3:0E4F`, `C3:0E69`), both dirty
- best local island: `42C2..42D0 (RTL)`
- result: mixed script/command-control page, no owner survives

## C3:4300..43FF
- page metrics: ascii=0.43, zero=0.09, ff=0.01, repeated_pair=0.04
- strongest false-dawn target: `4309` with 2 comparatively clean direct external hits (`C3:2193 JSR`, `C3:24A1 JMP`)
- `4300` also received one cleaner external `JSR` from `C3:65B7`
- the page degrades later into obvious name/text-style material around the `43B0` zone
- result: strongest caller-side false dawn of the continuation, but still no defendable owner

## C3:4400..44FF
- page metrics: ascii=0.63, zero=0.10, ff=0.00, repeated_pair=0.06
- visible external targets: `44A5`, `44C2`, `44B0`, `44AA`, `4441`, `4435`
- `44A5` had 2 external `JSR` hits, but caller quality and target-side bytes both fail immediately
- page body is overwhelmingly credits/text-heavy
- result: obvious text page, no code promotion possible

## C3:4500..45FF
- page metrics: ascii=0.28, zero=0.06, ff=0.00, repeated_pair=0.04
- strongest count target: `4544` with 3 external `JSR` hits (`C3:0EEE`, `C3:442F`, `C3:72B5`), still dirty/noisy overall
- late branch-fed bait clustered at `45DE`, `45E0`, `45EB`, and `45EF`
- strongest local island by shape: `45A2..45C1 (RTS)`
- result: mixed command/control page with a tempting late pocket, still not owner-worthy

## C3:4600..46FF
- page metrics: ascii=0.30, zero=0.07, ff=0.01, repeated_pair=0.02
- strongest external target on paper: `4631` with 2 dirty external `JSR` hits (`C3:D828`, `C3:DC30`)
- cleaner single-hit branch pressure existed into `461E` and `46E3`
- local return pockets: `46BF..46C6 (RTS)`, `46E3..46F0 (RTI)`
- result: mixed control/script tail page, no defendable owner boundary

## Bottom line
Across `C3:3D00..46FF`, the seam produced four main temptations and rejected all of them honestly:
- `3F90` as the cleanest lone external `JSR` landing
- `4309` as the strongest clean double-caller false dawn
- `4544` / `45DE` as the late mixed-control temptation
- `4631` as the strongest late dirty multi-`JSR` landing

The two clearest structural conclusions of the run are:
1. `4300` still fails even with real-looking direct caller support.
2. `4400` is straight credits/text-heavy material and is not recoverable as callable code.
