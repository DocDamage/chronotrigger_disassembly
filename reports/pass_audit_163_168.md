# Pass Audit — 163 through 168

This is the first structured audit pass using the repo-native manifest layer.
It is not a full re-disassembly. It identifies likely revisit candidates.

## High-confidence keepers
These passes look structurally strong and should remain closed unless new xref evidence appears.
- pass 164 — `C3:0307..C3:0528`
- pass 167 — `C3:0EFA..C3:1024`, `C3:1025..C3:10BF`, `C3:10C0..C3:10CF`
- pass 168 — `C3:10D0..C3:12FF`

## Revisit candidates
### Pass 163
- `C3:01E4..C3:02DC`
- `C3:02DD..C3:0306`
Reason: early seam split that established the pattern for later cleanup; worth a spot-check with the newer call-anchor/classifier flow.

### Pass 165
- `C3:08A9..C3:08B2`
Reason: explicitly marked tail fragment pending backward reattachment.

- `C3:09E9..C3:0A8F`
Reason: shared runtime-code emitter is high-impact and worth a second xref-oriented audit.

### Pass 166
- `C3:0B03..C3:0C91`
Reason: stream interpreter / dispatcher logic is a high-complexity owner and deserves a modern audit.

- `C3:0CB1..C3:0CB7`
Reason: externally called helper; exact split should be preserved and verified by xref scan.

## Audit conclusion
A sweep of older passes is beneficial, but it should be targeted.
The highest-value revisit set right now is:
1. `C3:09E9..C3:0A8F`
2. `C3:0B03..C3:0C91`
3. `C3:08A9..C3:08B2`
4. `C3:01E4..C3:0306`
