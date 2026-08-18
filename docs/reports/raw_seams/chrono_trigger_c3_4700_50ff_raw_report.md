# Chrono Trigger Disassembly — Raw Seam Report for C3:4700..50FF

This file preserves the seam-facing evidence for the fourth continuation of session 13. It is intentionally terse and page-oriented.

## C3:4700..47FF
- page metrics: ascii=0.25, zero=0.13, ff=0.02, repeated_pair=0.06
- visible targets: `4709`, `4738`, `4788`, `47B8`
- strongest target-side look: `4738`, but its only visible caller is dirty (`C3:DADD -> JSR $4738`)
- `4709` lands on a tiny top-of-page `RTS` pocket, but both caller and target side still read high-risk
- top local islands:
  - `47D6..47E5 (RTS)`, score=5, ascii=0.12, branches=1, calls=0
  - `4700..4709 (RTS)`, score=3, ascii=0.60, branches=0, calls=2

## C3:4800..48FF
- page metrics: ascii=0.33, zero=0.10, ff=0.01, repeated_pair=0.02
- strongest visible target: `4843` with 2 external `JSR` hits (`C3:3E95`, `C3:7720`), both high-risk
- other visible targets: `4800`, `4802`, `480A`, `480C`, `4814`, `483A`, `4840`, `48F4`
- no caller-backed owner boundary survived
- top local islands:
  - `489B..489F (RTS)`, score=4, ascii=0.20, branches=3, calls=0
  - `487C..4883 (RTS)`, score=2, ascii=0.38, branches=2, calls=0

## C3:4900..49FF
- page metrics: ascii=0.37, zero=0.08, ff=0.00, repeated_pair=0.05
- strongest visible target: `4920` with 2 external `JSR` hits (`C3:4A16`, `C3:73AF`), both high-risk
- other visible targets: `4942`, `494E`, `4994`
- `494E` had the cleanest target-side neighborhood, but still only one dirty caller
- top local island:
  - `49BB..49C4 (RTS)`, score=2, ascii=0.30, branches=2, calls=0

## C3:4A00..4AFF
- page metrics: ascii=0.41, zero=0.07, ff=0.00, repeated_pair=0.04
- visible targets: `4A0E`, `4A3C`, `4A48`, `4A52`, `4A60`, `4A62`, `4AA5`, `4AF0`
- least-awful risk pairings on paper: `4AA5` and `4AF0`, still only single-hit and still embedded in ASCII-heavy mixed material
- top local islands:
  - `4A34..4A4C (RTI)`, score=5, ascii=0.60, branches=2, calls=2
  - `4A3B..4A53 (RTI)`, score=5, ascii=0.52, branches=2, calls=2
  - `4A2B..4A43 (RTS)`, score=4, ascii=0.64, branches=3, calls=3
  - `4A5F..4A77 (RTS)`, score=4, ascii=0.44, branches=2, calls=4

## C3:4B00..4BFF
- page metrics: ascii=0.39, zero=0.08, ff=0.01, repeated_pair=0.05
- visible targets: `4B00`, `4B30`, `4B3A`, `4BCB`
- most tempting landing: `4BCB` from `C3:28EA -> JMP $4BCB`, caller risk=medium, target risk=low
- even so, `4BCB` lands too late and too deep inside mixed material to defend ownership
- top local islands:
  - `4B20..4B33 (RTS)`, score=3, ascii=0.50, branches=3, calls=0
  - `4BED..4BF1 (RTS)`, score=3, ascii=0.60, branches=0, calls=1

## C3:4C00..4CFF
- page metrics: ascii=0.31, zero=0.08, ff=0.01, repeated_pair=0.04
- visible targets: `4C00`, `4C3F`, `4C50`, `4CA5`, `4CD0`
- strongest false-dawn target: `4C3F` from `C3:28F4 -> JSR $4C3F`, caller risk=medium, target risk=low
- strongest local island of the continuation: `4C3A..4C49 (RTS)`, score=7, ascii=0.25, branches=1, calls=1
- the visible hit lands at interior `4C3F`, not at the local pocket’s true beginning
- other local islands:
  - `4C8B..4C92 (RTS)`, score=3, ascii=0.12, branches=0, calls=0
  - `4C5A..4C67 (RTS)`, score=2, ascii=0.57, branches=1, calls=0

## C3:4D00..4DFF
- page metrics: ascii=0.31, zero=0.09, ff=0.01, repeated_pair=0.05
- visible targets: `4D3A`, `4D3C`, `4D40`, `4D44`, `4D4E`, `4D80`, `4DA5`, `4DB5`, `4DC5`
- cleanest-looking target: `4D80` from `C3:42A4 -> JSR $4D80`, caller risk=medium, target risk=medium
- late `4DB5` and `4DC5` had lower target risk but dirty caller neighborhoods
- top local islands:
  - `4D49..4D51 (RTL)`, score=4, ascii=0.67, branches=0, calls=1
  - `4D1C..4D23 (RTI)`, score=3, ascii=0.38, branches=0, calls=2

## C3:4E00..4EFF
- page metrics: ascii=0.26, zero=0.09, ff=0.00, repeated_pair=0.04
- strongest visible target by count: `4E7D` with 2 hits from the same dirty `2A7x` neighborhood (`C3:2A79`, `C3:2A83`)
- other visible targets: `4E00`, `4E03`, `4E06`, `4E0D`, `4E12`, `4E41`, `4E45`, `4E49`, `4E60`, `4EE6`, `4EF2`
- `4EE6` had the cleanest caller-side risk of the page, but target risk remained high
- top local island:
  - `4E2C..4E36 (RTS)`, score=5, ascii=0.45, branches=1, calls=1

## C3:4F00..4FFF
- page metrics: ascii=0.39, zero=0.16, ff=0.01, repeated_pair=0.09
- clustered double-hit targets: `4F41`, `4F46`, `4F4B`
- all three clusters are backed only by high-risk callers and sit in a page with elevated zero/repeated-pair density
- other visible targets: `4F34`, `4F52`, `4F53`, `4F57`, `4F59`
- top local islands:
  - `4F1D..4F2A (RTI)`, score=4, ascii=0.71, branches=2, calls=1
  - `4F13..4F1B (RTI)`, score=4, ascii=1.00, branches=1, calls=1

## C3:5000..50FF
- page metrics: ascii=0.25, zero=0.16, ff=0.02, repeated_pair=0.08
- visible targets: `5008`, `5016`, `5018`, `5028`, `5035`, `503F`, `5047`, `50A5`, `50E1`, `50E7`, `50F1`
- page is less text-heavy than `4A00` / `4B00` / `4F00`, but still zero/repeated-pair heavy and structurally mixed
- `5016`, `5018`, and `50F1` had the least-awful target-side neighborhoods, still with dirty single-hit caller support
- top local island:
  - `50B8..50C3 (RTI)`, score=2, ascii=0.42, branches=1, calls=0

## Bottom line
Across `C3:4700..50FF`, the seam produced three main temptations and rejected all of them honestly:
- `4BCB` as a comparatively cleaner late landing
- `4C3F` plus local island `4C3A..4C49` as the strongest false-dawn combination of the run
- `4D80` as the next cleanest single-hit mid-page landing

None survived caller quality plus local boundary review together.
