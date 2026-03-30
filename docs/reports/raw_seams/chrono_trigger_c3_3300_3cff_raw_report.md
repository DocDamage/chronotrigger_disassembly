# Chrono Trigger Disassembly — Raw Seam Report for C3:3300..3CFF

This file preserves the raw seam-facing evidence for the second continuation of session 13. It is intentionally terse and page-oriented.

## C3:3300..33FF
- page metrics: ascii=0.22, zero=0.10, ff=0.00, repeated_pair=0.01
- strongest visible target: `33D6` with 2 same-bank hits
- caller picture: one cleaner caller (`C3:22C5`) plus one ASCII-side caller (`C3:6615`)
- result: still failed because the landing sits inside a mixed control/data blob
- notable local islands: `3358..3363 (RTS)`, `3321..3340 (RTI)`, `3398..33AF (RTS)`

## C3:3400..34FF
- page metrics: ascii=0.27, zero=0.15, ff=0.00, repeated_pair=0.01
- strongest visible target: `3461` with one cleaner caller and one ASCII-side caller
- result: target bytes immediately read like little-endian pointer/table material rather than callable structure
- notable local islands: `34BD..34DC (RTS)`, `3404..3423 (RTS)`, `3407..3426 (RTS)`

## C3:3500..35FF
- page metrics: ascii=0.27, zero=0.11, ff=0.02, repeated_pair=0.02
- strongest visible target: `350E` with one comparatively clean caller from `C3:2FB0`
- `357B` drew three visible jumps, but all were dirty
- result: looked structured but not clean; no defendable owner boundary
- notable local islands: `3598..35B7 (RTS)`, `35D3..35F2 (RTS)`, `3575..3594 (RTI)`

## C3:3600..36FF
- page metrics: ascii=0.35, zero=0.12, ff=0.01, repeated_pair=0.02
- strongest visible target: `3691` with one cleaner caller from `C3:1BAB`
- `36E9` looked like late tail bait rather than a real owner start
- result: local bytes were more code-like than average, but still collapsed under boundary review
- notable local islands: `3699..36B8 (RTS)`, `3692..36B1 (RTS)`, `3612..3621 (RTI)`

## C3:3700..37FF
- page metrics: ascii=0.34, zero=0.07, ff=0.02, repeated_pair=0.02
- strongest visible target: `377E` with 3 same-bank callers, including two comparatively cleaner ones
- early target field `370C..3716` was heavily polluted by ASCII-side callers
- result: `377E` still failed because the landing did not defend a true start and continued to read like mixed command/data material
- notable local islands: `3700..371E (RTS)`, `37B2..37D1 (RTS)`, `37BC..37D3 (RTS)`

## C3:3800..38FF
- page metrics: ascii=0.32, zero=0.06, ff=0.01, repeated_pair=0.02
- strongest visible target by count: `3800` with 4 same-bank jumps
- all visible `3800` callers came from dirty neighborhoods
- `3870` had the cleanest single hit, but only as a tiny unsupported pocket
- result: another xref-rich false-positive page
- notable local islands: `3854..3873 (RTI)`, `3876..3895 (RTS)`, `38CE..38ED (RTI)`

## C3:3900..39FF
- page metrics: ascii=0.25, zero=0.27, ff=0.00, repeated_pair=0.04
- strongest visible targets: `395E`, `39A7`, `39B1`, `39DE`, `39F5`
- caller picture was the cleanest of the continuation, especially around `395E`, `39A7`, and `39DE`
- result: despite cleaner xrefs, the target neighborhoods themselves resolved as repeated command/pointer-table style material, not defendable code starts
- notable local islands: `3900..3912 (RTS)`, `39D3..39EA (RTL)`, `394B..3962 (RTS)`

## C3:3A00..3AFF
- page metrics: ascii=0.27, zero=0.18, ff=0.00, repeated_pair=0.06
- strongest visible dirty cluster: `3A20` with 3 hits, all from comically ASCII-heavy text-side neighborhoods
- cleaner-looking callers existed for `3A01`, `3A3A`, and `3AA9`
- result: page remained dominated by table/command-stream behavior; `3AA9` stayed a false jump target
- notable local islands: `3ADE..3AFD (RTS)`, `3ADD..3AF4 (RTI)`

## C3:3B00..3BFF
- page metrics: ascii=0.35, zero=0.07, ff=0.01, repeated_pair=0.01
- strongest visible target: `3B46` with 2 hits, both from heavily ASCII-contaminated low addresses
- `3B24` had only a weak dirty jump caller
- result: sparse page, no owner/helper promotion survived
- notable local islands: `3B00..3B1B (RTS)`, `3B8A..3BA1 (RTI)`, `3B03..3B12 (RTI)`

## C3:3C00..3CFF
- page metrics: ascii=0.28, zero=0.09, ff=0.00, repeated_pair=0.02
- strongest visible targets: `3C5E` and `3C80`
- `3C5E` was the most interesting external hit of the continuation because it received a long call from bank `E9`
- `3C80` also had a cleaner same-bank jump from `C3:2917`
- result: both still failed because they land inside a wider mixed blob made of setup/store-like structure, tail jumps, and command/data contamination
- notable local islands: `3CDA..3CF9 (RTI)`, `3C6D..3C84 (RTS)`, `3C61..3C70 (RTS)`

## Bottom line
Across `C3:3300..3CFF`, the seam kept producing better-looking caller evidence without producing defendable owners. The strongest false dawns were `33D6`, `377E`, `395E/39A7/39DE`, and finally `3C5E/3C80`.
