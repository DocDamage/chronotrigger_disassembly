# Current Session Packet

- Latest pass: **150**
- Source note: `notes/next_session_start_here.md`
- Extracted seam targets: **1**

## Live seam text

C2:F2F3..C2:F360

## Target packet

### C2:F2F3..C2:F360

- Span: `C2:F2F3 .. C2:F360` (110 bytes)
- Start bytes ±8: `00 7D A8 A9 0B CC 28 60 08 E2 20 C2 10 2C 78 0D`
- End bytes ±8: `00 90 85 61 99 02 00 28 AB 60 C2 10 08 A9 FF 48`
- Overlapping labels:
  - none
- Nearby labels:
  - `C2:F2E2..C2:F2F2`
- Xref summary:
  - hot direct entry `F2F3` with many bank-local callers
  - short base-copy helper `F333` immediately follows the owner tail
  - sibling exact owner `F338` begins after the short helper
  - immediate lookahead just past the seam already shows live callable heat at `F378`
- Note mentions:
  - `chrono_trigger_disasm_pass150.md`
  - `chrono_trigger_labels_pass150.md`
