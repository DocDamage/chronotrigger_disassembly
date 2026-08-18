"""Range interval modeling, conflict/overlap detection, and coverage union."""

from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from .manifest_models import ClosedRange

@dataclass
class RangeConflict:
    conflict_id: str
    bank: str
    left_range: ClosedRange
    right_range: ClosedRange
    left_pass: int
    right_pass: int
    left_path: str
    right_path: str
    relationship: str  # "exact_duplicate", "containment", "partial_overlap", "code_data_overlap"
    overlap_start: int
    overlap_end: int
    suggested_resolution: str

    @property
    def overlap_range_str(self) -> str:
        return f"{self.bank}:{self.overlap_start:04X}..{self.bank}:{self.overlap_end:04X}"


def detect_range_conflicts(
    ranges_with_metadata: List[Tuple[ClosedRange, int, str]],
    waiver_registry: Optional[Dict[str, Any]] = None
) -> List[RangeConflict]:
    """Detect all range conflicts across a collection of (ClosedRange, pass_number, source_path)."""
    # Group by bank
    by_bank: Dict[str, List[Tuple[ClosedRange, int, str]]] = {}
    for r, p_num, src in ranges_with_metadata:
        # Superseded records are retained for provenance but are not active
        # ownership claims and therefore cannot participate in conflicts.
        if r.kind == "superseded":
            continue
        by_bank.setdefault(r.bank, []).append((r, p_num, src))

    conflicts: List[RangeConflict] = []
    conflict_counter = 0

    for bank, items in by_bank.items():
        # Sort by start_addr, then end_addr
        items_sorted = sorted(items, key=lambda x: (x[0].start_addr, x[0].end_addr, x[1]))
        n = len(items_sorted)

        for i in range(n):
            r1, p1, src1 = items_sorted[i]
            for j in range(i + 1, n):
                r2, p2, src2 = items_sorted[j]

                # If r2 starts after r1 ends, no more overlaps with r1 in sorted order
                if r2.start_addr > r1.end_addr:
                    break

                # Overlap exists: compute intersection
                inter_start = max(r1.start_addr, r2.start_addr)
                inter_end = min(r1.end_addr, r2.end_addr)

                if inter_start > inter_end:
                    continue

                # Determine relationship
                if r1.start_addr == r2.start_addr and r1.end_addr == r2.end_addr:
                    rel = "exact_duplicate"
                    res = "Mark duplicate as superseded or combine labels"
                elif (r1.start_addr <= r2.start_addr and r1.end_addr >= r2.end_addr) or \
                     (r2.start_addr <= r1.start_addr and r2.end_addr >= r1.end_addr):
                    rel = "containment"
                    res = "Model helper as child with parent_range or refine boundaries"
                elif (r1.kind in ("data", "text_marker") and r2.kind not in ("data", "text_marker")) or \
                     (r2.kind in ("data", "text_marker") and r1.kind not in ("data", "text_marker")):
                    rel = "code_data_overlap"
                    res = "Reclassify boundaries between code and data"
                else:
                    rel = "partial_overlap"
                    res = "Re-disassemble boundary to eliminate intersecting bytes"

                # Check if waived
                cid = f"conf_{bank}_{inter_start:04X}_{inter_end:04X}_{min(p1, p2)}_{max(p1, p2)}"
                
                # Check for explicit parent-child exception
                if rel == "containment":
                    if r2.parent_range == r1.range_str or r1.parent_range == r2.range_str:
                        continue

                conflict_counter += 1
                conflicts.append(RangeConflict(
                    conflict_id=cid,
                    bank=bank,
                    left_range=r1,
                    right_range=r2,
                    left_pass=p1,
                    right_pass=p2,
                    left_path=src1,
                    right_path=src2,
                    relationship=rel,
                    overlap_start=inter_start,
                    overlap_end=inter_end,
                    suggested_resolution=res
                ))

    return conflicts


def compute_byte_union(ranges: List[ClosedRange]) -> Dict[str, Any]:
    """Compute non-overlapping byte union per bank and global coverage statistics."""
    by_bank: Dict[str, List[Tuple[int, int]]] = {}
    total_raw_range_count = len(ranges)

    for r in ranges:
        if r.kind == "superseded":
            continue
        by_bank.setdefault(r.bank, []).append((r.start_addr, r.end_addr))

    bank_unions: Dict[str, List[Tuple[int, int]]] = {}
    bank_covered_bytes: Dict[str, int] = {}
    total_covered_bytes = 0

    for bank, intervals in sorted(by_bank.items()):
        intervals.sort()
        merged: List[Tuple[int, int]] = []
        for start, end in intervals:
            if not merged:
                merged.append((start, end))
            else:
                prev_start, prev_end = merged[-1]
                if start <= prev_end + 1:
                    merged[-1] = (prev_start, max(prev_end, end))
                else:
                    merged.append((start, end))
        bank_unions[bank] = merged
        b_bytes = sum(e - s + 1 for s, e in merged)
        bank_covered_bytes[bank] = b_bytes
        total_covered_bytes += b_bytes

    return {
        "total_covered_bytes": total_covered_bytes,
        "total_raw_ranges": total_raw_range_count,
        "bank_covered_bytes": bank_covered_bytes,
        "bank_unions": {
            b: [f"{b}:{s:04X}..{b}:{e:04X}" for s, e in u]
            for b, u in bank_unions.items()
        }
    }
