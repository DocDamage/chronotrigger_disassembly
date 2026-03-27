# Pass 173 — C3:13FC..C3:15E8

## Objective
Keep advancing through the higher `C3` lane without forcing a fake monolithic owner where the bytes still behave like mixed content.

## Result
Closed:
- `C3:13FC..C3:15E3`
- `C3:15E4..C3:15E8`

Next live seam:
- `C3:15E9..C3:1816`

## What changed
### `C3:13FC..C3:15E3`
Treated as:
- `ct_c3_inline_mixed_control_table_and_helper_blob_before_c302dd_wrapper`

Why:
- the region keeps breaking under linear sweep instead of settling into one convincing owner/helper family
- there are repeated stretches that look like embedded register setup, control words, table-like material, and partial helper fragments rather than one stable callable body
- the bytes immediately before the next clean split still do not give a trustworthy contiguous decode, so freezing them as a mixed blob is safer than inventing a fake function

### `C3:15E4..C3:15E8`
Treated as:
- `ct_c3_tiny_long_wrapper_calling_c302dd_then_returning`

Why:
- this subrange resolves cleanly as a tiny veneer
- decode is simply `JSL $C302DD ; RTS`
- unlike the preceding blob, this is structurally crisp enough to take as real code

## Practical interpretation
This lane is still behaving like a mixed-content island with small clean executable splinters inside it.
The honest move was to keep freezing the unstable blob and only peel out the tiny wrapper that is clearly real.

## Next-pass caution
The next live seam starts at `C3:15E9`.
That boundary looks more code-like than `13FC..15E3`, so the next pass should test whether a real owner begins there before classifying more bytes as mixed data.
