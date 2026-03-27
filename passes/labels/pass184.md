# Pass 184 — New Labels

- `ct_c3_inline_mixed_xref_bait_with_untrusted_single_call_targets_and_unsupported_local_helper_pocket_before_2200_candidate`
  - Range: `C3:2100..C3:21FF`
  - Kind: `data`
  - Confidence: `medium-high`
  - Notes: conservative upgraded-flow freeze; all visible raw targets in the page are single-hit and fail local sanity checks, the only tiny veneer-looking signatures at `2109` and `214D` are false positives, and the strongest locally coherent pocket begins around `2191` but lacks caller support while the visible `21A0` target lands inside it rather than at its true start
