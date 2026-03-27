# Xref and Anchor Validation Upgrade

This upgrade exists because raw byte-pattern hits were no longer good enough.

## Why this was added

Recent `C3` work exposed three recurring failure modes:

- same-bank `JSR/JMP` hits were being over-trusted across bank boundaries
- caller evidence from unresolved mixed-content ranges was being treated too much like real anchor proof
- tiny wrappers, landing pads, and single-byte return stubs were easy to miss unless they were found manually
- the old HiROM mapper rejected low addresses like `C3:1817`, which is exactly where recent `C3` work has been happening

The new scripts address those exact problems.

## New scripts

- `tools/scripts/snes_utils_hirom_v2.py`
  - full-bank HiROM mapping helper
  - accepts low addresses like `C3:1817`
- `tools/scripts/manifest_xref_utils.py`
  - shared helpers for loading closed manifest ranges and classifying caller context
- `tools/scripts/build_call_anchor_report_v3.py`
  - target-first anchor report
  - bank-aware validation
  - caller-confidence scoring
- `tools/scripts/scan_range_entry_callers_v1.py`
  - range-first scan for incoming caller targets
  - useful when a wide seam contains many tempting raw targets
- `tools/scripts/detect_tiny_veneers_v1.py`
  - detects tiny `JSR/JSL ... ; RTS` wrappers
  - detects `RTL` stubs
  - detects tiny `BRA` landing pads

## Anchor strength model

### Strong
A valid caller exists and the caller sits inside a previously closed executable range.

### Weak
A valid caller exists, but the caller still sits in unresolved bytes.

### Suspect
A valid-looking caller exists, but it sits inside a closed data range.

### Invalid
A same-bank `JSR/JMP` hit does not actually resolve to the requested bank, or the hit otherwise fails bank-aware validation.

## Recommended workflow

When a seam looks executable but the proof is shaky:

1. run `detect_tiny_veneers_v1.py` on the seam
2. run `scan_range_entry_callers_v1.py` on the seam
3. for any especially tempting target, run `build_call_anchor_report_v3.py`
4. only treat a target as strongly anchored when the caller survives bank-aware validation and comes from resolved executable context

## Example commands

```bash
python tools/scripts/detect_tiny_veneers_v1.py \
  --rom "/path/to/Chrono Trigger (USA).sfc" \
  --range C3:1817..C3:18FF

python tools/scripts/scan_range_entry_callers_v1.py \
  --rom "/path/to/Chrono Trigger (USA).sfc" \
  --range C3:1817..C3:18FF \
  --manifests-dir passes/manifests

python tools/scripts/build_call_anchor_report_v3.py \
  --rom "/path/to/Chrono Trigger (USA).sfc" \
  --target C3:17BD \
  --manifests-dir passes/manifests
```

## Intended use

These scripts do not replace real disassembly reasoning.
They are there to prevent avoidable mistakes:

- fake cross-bank same-bank anchors
- promoting unresolved caller hits into strong evidence
- missing tiny executable splinters inside mixed-content islands
- rejecting valid low-address `C3` ranges because of an overly strict mapper
