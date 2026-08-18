# ADR 0002: Range Ownership and Coverage Model

## Status
Accepted

## Context
Previous tooling merged closed ranges before checking for collisions or overlaps. This concealed exact duplicate ranges, boundary touches, code/data overlaps, and helper/owner nestings. In addition, coverage denominators and metrics were inconsistently calculated across different scripts.

## Decision

### 1. Ownership Classes
Each closed range in a manifest MUST specify a `kind` from the following controlled vocabulary:
- `code_owner`: Top-level executable function/subroutine. May not overlap any other active top-level owner.
- `code_helper`: Independently callable function nested within or helper to an owner. Must either be disjoint or specify `parent_range` / `parent_label`.
- `wrapper` / `veneer`: Callable dispatch wrappers with same ownership constraints as helpers.
- `data` / `text_marker`: Non-executable data tables or text segments. May not overlap executable code without an approved mixed-content waiver.
- `tail_fragment`: Temporary fragment requiring resolution.
- `superseded`: Historical record retained for provenance, excluded from active coverage.

### 2. Conflict and Overlap Taxonomy
1. **Exact Duplicate**: Same bank and endpoints ($[start, end]$ identical). Resolved by retaining primary owner and setting duplicate as superseded or reaffirmation.
2. **Containment**: One range is a strict subset of another. Permitted only if the contained range is `code_helper`/`wrapper` referencing the containing `code_owner`.
3. **Partial Overlap**: Intersecting intervals without containment. Strictly forbidden and considered a blocking error.
4. **Code vs Data Overlap**: Strictly forbidden without explicit waiver.

### 3. Coverage Calculation Semantics
- Coverage MUST be computed via interval union per bank over active, non-superseded ranges.
- Coverage MUST report distinct metrics:
  - Total closed bytes (interval union length).
  - Executable code bytes (`code_owner`, `code_helper`, `wrapper`).
  - Classified data/text bytes (`data`, `text_marker`).
  - Total bank denominator (e.g. 64 KiB per HiROM bank).
- Raw conflicts and overlaps MUST be evaluated and reported BEFORE applying interval union.

## Consequences
- Coverage calculations are deterministic and cannot mask hidden boundary conflicts.
- Parent-child helper relationships are formally modeled without double-counting bytes.
