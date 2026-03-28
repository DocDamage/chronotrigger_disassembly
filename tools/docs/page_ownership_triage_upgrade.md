# Page-ownership triage upgrade

## Why this upgrade exists

The current high-bank `C3` seam is no longer failing because we cannot find xrefs.
It is failing because the xrefs are often the **wrong kind** of xrefs:

- branch-fed local control traffic that makes a page feel more executable than it really is
- interior landings into return-anchored splinters
- page-top bait that looks promising until you separate true outside ownership from same-page self-noise
- blocks where several pages look equally ugly and still need a quick way to rank which one deserves the next deep read

The earlier seam-shape upgrade already improved:
- caller/target neighborhood risk scoring
- local return-island discovery
- one-shot seam triage with `run_c3_candidate_flow_v2.py`

This upgrade adds the missing **page-ownership layer** on top of that work.

## New scripts

### `tools/scripts/score_seam_page_ownership_v1.py`
Scores whether a page is receiving real outside ownership or just local branch-fed traffic.

What it adds:
- separates external direct hits from same-page branch/control noise
- flags page-top landings vs interior landings
- penalizes targets that land inside a surfaced local island instead of at its true start
- emits a simple page class:
  - `high_attention_external_owner_candidate`
  - `medium_attention_external_owner_candidate`
  - `local_control_blob`
  - `interior_landing_bait`
  - `mixed_no_owner`

Practical use:
- faster rejection of pages like `C3:5800..58FF` that feel executable but are mostly self-contained local control
- faster identification of false dawns like `4C3F` where the visible hit lands inside a good local island instead of at the island start
- clearer explanation for why `5200`-style page-top bait still fails ownership

### `tools/scripts/run_c3_seam_block_report_v1.py`
Batch-runs ownership triage across a consecutive block of pages.

What it adds:
- scans every `0x100` page in a block
- ranks pages by external-owner signal
- separately ranks pages by local-control density
- gives a quick answer to:
  - “which page in this block deserves the next hard read?”
  - “which pages are mostly just self-fed control blobs?”

Practical use:
- run once on a ten-page span before manual review
- cut down on deep-reading pages that only look busy because of internal branch traffic
- produce a cleaner no-BS summary for handoffs and README updates

### `tools/scripts/run_c3_candidate_flow_v3.py`
Wrapper that combines the earlier seam triage with the new page-ownership layer.

What it runs:
1. `run_c3_candidate_flow_v2.py`
2. `score_seam_page_ownership_v1.py`

Practical use:
- preserve the existing seam-shape workflow
- add page-class output without replacing the earlier evidence
- keep one command as the default first pass for ugly forward `C3` pages

## Recommended workflow now

For mixed forward seams:

1. run `run_c3_seam_block_report_v1.py` on the next block
2. pick the strongest external-owner page first, not just the busiest page
3. run `run_c3_candidate_flow_v3.py` on that page
4. inspect downgraded xrefs and surfaced local islands
5. only promote code when caller quality, target structure, and page ownership all agree
6. if they disagree, freeze the page honestly and move the seam

## Honest limitation

These helpers still do **not** prove code automatically.
They are triage tools, not semantic disassembly.

Their job is narrower and useful:
- reduce wasted time on local branch-fed bait
- separate page-top / interior false dawns from true owner candidates
- make block-level seam review faster and more explicit
