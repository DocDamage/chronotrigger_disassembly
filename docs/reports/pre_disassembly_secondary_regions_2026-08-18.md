# Secondary-region pre-disassembly review — 2026-08-18

This report records the requested Phase 3 review of D1–D9, CF:C000–CFFF, C5:9000–9FFF and D000–DFFF, and the active DA–FF upper-ROM pool. Historical scores were treated as search leads, not executable evidence.

## Outcome

- New executable owners promoted: **0**
- Active historical code claims corrected to data: **89**
- Active historical owner claims corrected to executable fragments: **7**
- Score-qualified scanner findings dispositioned: **261** raw findings (including overlapping and already-active windows)
- D1–D9 active claims left pending: **0**
- DA–FF active claims left pending: **0**
- Unique covered bytes: **59,050 before and after**
- Executable bytes since the original baseline: **38,079 → 33,710**
- Classified-data bytes since the original baseline: **20,971 → 25,340**
- Ownership conflicts: **0**

The 4,369-byte movement is a classification correction. It does not claim new ROM coverage.

## D4 and D6 deep scans

The repaired seam workflow scanned all 256 pages of each bank.

- D4 page families: 164 branch-fed pockets, 86 mixed-command/data pages, and 6 nominal candidate-code lanes. All 16 active historical “functions” were bitplane or mask records. Repeated headers and mirrored plane rows disproved even the score-nine claims.
- D6 page families: 114 nominal candidate-code lanes, 110 branch-fed pockets, 26 mixed pages, and 6 zero-fill pages. The compact review retained 173 owner-backtrack candidates and 70 score-qualified clusters. All 24 active historical claims and the broader score pool were compressed-graphics false positives. D6:BE65, historically score ten, is asset data rather than a handler.

The raw scorer's high candidate density in these banks is therefore a property of graphics bytes that coincide with 65816 opcode values, not code density.

## D1 and broader D2–D9

D2, D3, D5, D7, D8, and D9 contained 18 active score claims. Every range was a graphics, mask, or compressed-asset record and is now reviewed data.

D1 required a mixed classification:

- Twelve active ranges from D1:0350 through D1:3AE2 are graphics records. D1:3A8F is an especially clear mirrored bitplane sequence. D1:0D28's score twelve arose because mask bytes were counted as eight returns.
- Seven upper-bank ranges contain genuine aligned instructions locally but cannot own the historical boundaries. D1:E90F begins at a backward-loop tail; D1:E721 ends mid-instruction; D1:F8F1 combines portions of two routines; and D1:FA67 begins on the preceding routine's `RTS`. These ranges are retained as reviewed `tail_fragment` evidence pending complete owner and caller reconstruction.

## CF:C000–CFFF

The 16-page rerun classified 12 pages as text/ASCII-heavy and four as mixed command/data. Three score-qualified windows survived compact filtering:

- CF:C0B0 was reclassified as tilemap/graphics-index data, including both adjudicated canonical pieces.
- CF:C396 (score seven) and CF:CD30 (score eight) were rejected. Both are slices of regular little-endian word tables.

No executable owner was promoted.

## C5 requested windows

- C5:9000–9FFF retained nine score-six-plus windows in compact output. All sample dense graphics or compressed-asset data; no active canonical owner existed in this window.
- C5:D000–DFFF retained six score-six-plus windows. The active C5:DB2B and C5:DC49 score clusters were corrected to compressed graphics data. The other windows were rejected without promotion.

## Upper ROM DA–FF

Only DA, DB, DD, DE, and DF contained active canonical claims; E0–FF had none. All 59 active claims were data:

- DA, DB, and DF contain compressed graphics and mask records.
- DD and DE contain highly regular little-endian word/tilemap tables, frequently alternating a value with `40`. Those table bytes produced historical scores up to nineteen and several false “cross-bank hubs.”

The correction registry now supports schema-validated bulk corrections with deterministic labels. Migration, conservation, adjudication validation, and report comparison expand the same batch representation, avoiding duplicated evidence while preserving every original pass/range/label identity.

## Durable evidence

- Candidate pool decisions: `tools/config/candidate_dispositions.json`
- Reproducible legacy-to-canonical corrections: `tools/config/manifest_corrections.json`
- D6 compact full-bank scan: `reports/pre_disassembly_d6_compact_scan.json`
- CF compact scan: `reports/pre_disassembly_cf_c000_cfff_compact_scan.json`
- C5 compact scans: `reports/pre_disassembly_c5_9000_9fff_compact_scan.json` and `reports/pre_disassembly_c5_d000_dfff_compact_scan.json`

Historical reports remain unchanged. Where they claim completion or executable promotion from score alone, this report and the canonical correction ledger are the current authority.

## Final whole-repository reconciliation — 2026-08-19

The same instruction-alignment standard was subsequently applied to every remaining active canonical range, not only the named Phase 3 windows.

- C4, C5, C6, and C7 contributed **112 additional false executable claims**, all corrected to graphics or compressed-asset data.
- CF below E000 contributed **35 table/asset false positives**; its coherent E000–FFFF snippets remain reviewed executable fragments.
- The 398 C0, 55 C1, and 12 C2 active windows contain genuine executable material, but score-derived boundaries were conservatively recorded as `tail_fragment` rather than asserted as independent owners.
- The 292 active C3 ranges retain their authoritative semantic classifications after overlap adjudication and evidence review.
- Across the repository, **771 historical `code_owner` records were corrected**: 282 to data and 489 to executable fragments. No new owner was promoted.
- Final classification totals are 137 code owners, 11 helpers, 8 veneers, 1 wrapper, 489 executable fragments, 413 data ranges, and 2 text markers.
- Unique coverage remains **59,050 bytes (1.4079%)**. Executable coverage is **28,189 bytes** and classified-data coverage is **30,861 bytes**.
- The readiness gate is **READY**: 1,061/1,061 active ranges reviewed, with zero missing evidence, provenance, ownership conflicts, or deferred candidate dispositions.
