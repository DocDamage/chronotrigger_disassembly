# Session 13 toolkit upgrade — batch seam reporting and owner-boundary triage

## Why this upgrade exists

The current `C3` seam has been dominated by a repetitive manual cost:
- pages that *feel* cleaner than their neighbors but still fail owner promotion
- false dawns where the visible landing is inside a local `RTS` / `RTL` / `RTI` island instead of at its true start
- stretches where the right answer is really "this page is text-heavy mixed", "this page is local-control blob", or "this page is pointer-table risk", but that classification still had to be handwritten every time
- repeated hand assembly of 10-page raw seam reports after the actual byte review was already done

The earlier seam-shape upgrade helped score raw xrefs and surface local islands.
This upgrade adds **page-level mixedness labeling**, **owner-boundary failure triage**, and **batch seam reporting** so the next `C3` runs can be summarized faster and more consistently.

## New scripts

### `tools/scripts/page_range_mixedness_v1.py`
Scores each page in a SNES range and assigns a coarse page-shape label.

What it adds:
- page-level ASCII ratio
- zero / `FF` density
- repeated little-endian pair score
- branch / return / call density
- page labels such as:
  - `text_heavy_mixed`
  - `text_table_mixed`
  - `pointer_table_risk`
  - `local_control_blob`
  - `mixed_executable_looking`
  - `register_write_mixed`
  - `padding_or_data_mixed`
  - `mixed_unknown`

Practical use:
- faster coarse classification of ugly seams
- easier identification of pages that only *look* executable compared to worse neighbors
- better page-by-page framing for raw seam reports and handoffs

### `tools/scripts/score_owner_boundary_risk_v1.py`
Scores *why* visible target landings fail owner-boundary review.

What it adds:
- keeps raw visible landings grouped page-by-page
- scores caller-side and target-side risk around each landing
- tags landings as:
  - `page_top_bait`
  - `late_tail_bait`
  - `interior_island_landing`
  - `island_start_candidate`
  - `mid_blob_landing`
- correlates visible targets with local return-anchored islands

Practical use:
- much faster explanation of false dawns like:
  - "good caller, but interior island landing"
  - "clean page-top lure, but still page-top bait"
  - "late clean landing, but only tail bait"
- reduces manual rereads when the page already failed for boundary reasons

### `tools/scripts/run_c3_seam_batch_v1.py`
Runs a batch seam summary over a multi-page range.

What it runs:
1. `page_range_mixedness_v1.py`
2. `score_owner_boundary_risk_v1.py`

What it outputs:
- JSON summary for downstream tooling
- or a Markdown seam report suitable for direct note-writing / raw report drafting

Practical use:
- faster 5-page / 10-page seam reviews
- easier generation of consistent raw seam reports for branch write-back
- better visibility into which pages are text-heavy vs local-control vs genuinely executable-looking

### `tools/scripts/run_c3_candidate_flow_v4.py`
Lightweight upgraded wrapper for page-level seam triage.

What it adds over the older wrappers:
- page mixedness labels
- owner-boundary failure counts
- total visible hit counts and island counts across the requested range

Practical use:
- quick sanity pass before deeper manual review
- easier comparison between neighboring pages that are all "mixed", but mixed in different ways

## Validation completed locally

These scripts were syntax-checked and smoke-tested locally against the Chrono Trigger ROM.

Validated locally on:
- `C3:5100..C3:52FF`

Observed output shape:
- `C3:5100..C3:51FF` classified as `local_control_blob`
- `C3:5200..C3:52FF` classified as `mixed_executable_looking`
- owner-boundary reporting surfaced the strongest visible lures and tagged why they still failed owner review

## Recommended workflow now

For forward `C3` seam work:

1. run `run_c3_candidate_flow_v4.py` for the immediate range
2. if the seam spans several ugly pages, run `run_c3_seam_batch_v1.py`
3. inspect page labels first:
   - text-heavy mixed
   - pointer-table risk
   - local-control blob
   - mixed executable-looking
4. inspect strongest boundary-failure lures second:
   - page-top bait
   - interior island landing
   - late tail bait
   - island-start candidate
5. only promote code when caller quality, page shape, and boundary position all still agree
6. if they do not agree, freeze the page honestly and move the seam

## Honest limitation

These additions still do **not** replace semantic disassembly, CFG recovery, or assembler-backed verification.
They are triage tools.
Their job is to make the next ugly seam easier to explain and reject correctly — not to auto-promote code.
