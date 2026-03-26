# Confidence Levels

Each pass closure should keep three separate confidence signals.

## Structural confidence
How certain we are about:
- entry boundaries
- helper splits
- terminal boundaries
- code vs data classification

## Semantic confidence
How certain we are about:
- what the routine actually does
- whether a label describes engine behavior correctly
- whether a range is presentation logic, math, graphics, audio, etc.

## Rebuild confidence
How certain we are that:
- the range could be reconstructed faithfully in source
- all helper/data relationships are captured
- the current interpretation supports byte-accurate rebuild planning

## Suggested levels
- `high`
- `medium-high`
- `medium`
- `low`

Structural confidence may be high while semantic confidence is still medium.
