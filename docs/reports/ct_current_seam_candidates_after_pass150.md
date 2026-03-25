# Chrono Trigger Seam Candidates — After Pass 150

## Live seam

- `C2:F2F3..C2:F360`

## Strongest callable starts

1. `C2:F2F3`
   - many exact direct bank-local callers already active across bank `C2`
   - clean owner prologue `PHP ; SEP #$20 ; REP #$10`

2. `C2:F333`
   - exact short helper start immediately after the exact `F2F3` owner tail
   - tiny exact `5B -> 61` base-copy helper ending at exact `RTS`

3. `C2:F338`
   - clean sibling owner prologue `PHB ; PHP ; PEA $0000 ; PLB ; PLB`
   - follows the exact short helper `F333..F337`

## Notes

- the old seam stop at `C2:F24A` was too short because the exact sibling writer / formatter / wrapper chain continues cleanly through exact `C2:F2F2`
- the new seam starts at the first uncovered hot owner entry at exact `C2:F2F3`
- immediate lookahead just past this seam still shows additional callable heat at exact `C2:F378`
