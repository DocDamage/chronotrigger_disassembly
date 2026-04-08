#!/usr/bin/env python3
"""
Generate comprehensive coverage report for Bank C0 of Chrono Trigger disassembly.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

BANK_SIZE = 0x10000  # 64KB bank
PAGE_SIZE = 256  # 256-byte pages
REGION_SIZE = 0x1000  # 4KB regions

def parse_range(range_str: str) -> Tuple[int, int]:
    """Parse range string like 'C0:86DD..C0:86F6' into (start, end)."""
    match = re.match(r'C0:([0-9A-Fa-f]+)\.\.C0:([0-9A-Fa-f]+)', range_str)
    if match:
        start = int(match.group(1), 16)
        end = int(match.group(2), 16)
        return (start, end)
    return (0, 0)

def load_all_manifests(manifest_dir: str) -> List[dict]:
    """Load all pass manifests from directory."""
    manifests = []
    for filename in os.listdir(manifest_dir):
        if filename.endswith('.json') and filename.startswith('pass'):
            filepath = os.path.join(manifest_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    manifest = json.load(f)
                    manifests.append(manifest)
            except Exception as e:
                print(f"Warning: Could not load {filename}: {e}")
    return sorted(manifests, key=lambda x: x.get('pass_number', 0))

def calculate_coverage(manifests: List[dict]) -> Dict:
    """Calculate coverage statistics from manifests."""
    # Track covered bytes as a set of individual addresses
    covered_bytes = set()
    all_ranges = []
    total_functions = 0
    
    for manifest in manifests:
        for closed_range in manifest.get('closed_ranges', []):
            range_str = closed_range.get('range', '')
            if range_str.startswith('C0:'):
                start, end = parse_range(range_str)
                if start < end:
                    for addr in range(start, end + 1):
                        covered_bytes.add(addr)
                    all_ranges.append({
                        'start': start,
                        'end': end,
                        'label': closed_range.get('label', ''),
                        'kind': closed_range.get('kind', ''),
                        'pass': manifest.get('pass_number', 0)
                    })
                    if closed_range.get('kind') == 'owner':
                        total_functions += 1
    
    return {
        'covered_bytes': covered_bytes,
        'all_ranges': all_ranges,
        'total_functions': total_functions
    }

def calculate_page_coverage(covered_bytes: Set[int]) -> List[Tuple[int, int, float]]:
    """Calculate coverage per 256-byte page. Returns list of (page_num, covered, percentage)."""
    pages = []
    for page in range(256):  # 256 pages of 256 bytes each = 64KB
        page_start = page * PAGE_SIZE
        page_end = page_start + PAGE_SIZE
        page_bytes = set(range(page_start, page_end))
        covered_in_page = len(page_bytes & covered_bytes)
        percentage = (covered_in_page / PAGE_SIZE) * 100
        pages.append((page, covered_in_page, percentage))
    return pages

def calculate_region_coverage(covered_bytes: Set[int]) -> List[Dict]:
    """Calculate coverage per 4KB region. Returns list of region info dicts."""
    regions = []
    for region in range(16):  # 16 regions of 4KB each = 64KB
        region_start = region * REGION_SIZE
        region_end = region_start + REGION_SIZE
        region_bytes = set(range(region_start, region_end))
        covered_in_region = len(region_bytes & covered_bytes)
        percentage = (covered_in_region / REGION_SIZE) * 100
        regions.append({
            'region_num': region,
            'start': region_start,
            'end': region_end - 1,
            'covered': covered_in_region,
            'total': REGION_SIZE,
            'percentage': percentage
        })
    return regions

def find_gaps(covered_bytes: Set[int], min_gap_size: int = 16) -> List[Tuple[int, int]]:
    """Find the largest uncovered gaps in the bank."""
    gaps = []
    current_gap_start = None
    
    for addr in range(BANK_SIZE):
        if addr not in covered_bytes:
            if current_gap_start is None:
                current_gap_start = addr
        else:
            if current_gap_start is not None:
                gap_size = addr - current_gap_start
                if gap_size >= min_gap_size:
                    gaps.append((current_gap_start, addr - 1, gap_size))
                current_gap_start = None
    
    # Handle gap at end of bank
    if current_gap_start is not None:
        gap_size = BANK_SIZE - current_gap_start
        if gap_size >= min_gap_size:
            gaps.append((current_gap_start, BANK_SIZE - 1, gap_size))
    
    return sorted(gaps, key=lambda x: x[2], reverse=True)

def generate_visual_map(covered_bytes: Set[int], width: int = 64) -> str:
    """Generate ASCII visual coverage map."""
    lines = []
    lines.append("\n### Visual Coverage Map (64x256 grid = 64KB)")
    lines.append("Legend: █ = Covered | ░ = Uncovered")
    lines.append("")
    
    for row in range(256):
        row_start = row * width
        row_bytes = set(range(row_start, row_start + width))
        covered_in_row = len(row_bytes & covered_bytes)
        
        # Create a simpler representation - one row per 256 bytes
        if covered_in_row == width:
            char = "#"  # Fully covered
        elif covered_in_row == 0:
            char = "."  # Fully uncovered
        elif covered_in_row > width / 2:
            char = "+"  # Mostly covered
        else:
            char = "-"  # Partially covered
        
        if row % 16 == 0:
            lines.append(f"C0:{row_start:04X} ", end="")
        lines.append(char)
        if row % 16 == 15:
            lines.append(f"  ({row_start+width-1:04X})")
    
    return "\n".join(lines)

def generate_coverage_bar(percentage: float, width: int = 30) -> str:
    """Generate ASCII bar for coverage percentage."""
    filled = int((percentage / 100) * width)
    bar = "#" * filled + "." * (width - filled)
    return f"[{bar}] {percentage:.1f}%"

def main():
    # Paths
    manifest_dir = Path("passes/manifests")
    report_path = Path("reports/c0_coverage_report.md")
    
    # Ensure reports directory exists
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load all manifests
    print("Loading manifests...")
    manifests = load_all_manifests(manifest_dir)
    print(f"Loaded {len(manifests)} manifests")
    
    # Calculate coverage
    print("Calculating coverage...")
    coverage = calculate_coverage(manifests)
    covered_bytes = coverage['covered_bytes']
    total_functions = coverage['total_functions']
    all_ranges = coverage['all_ranges']
    
    total_covered = len(covered_bytes)
    coverage_percentage = (total_covered / BANK_SIZE) * 100
    
    # Calculate by page
    page_coverage = calculate_page_coverage(covered_bytes)
    
    # Calculate by 4KB region
    region_coverage = calculate_region_coverage(covered_bytes)
    
    # Find gaps
    gaps = find_gaps(covered_bytes, min_gap_size=32)
    
    # Generate report
    report_lines = []
    report_lines.append("# Bank C0 Coverage Report")
    report_lines.append("")
    report_lines.append(f"**Generated:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    # Summary section
    report_lines.append("## Summary")
    report_lines.append("")
    report_lines.append(f"| Metric | Value |")
    report_lines.append(f"|--------|-------|")
    report_lines.append(f"| Total Functions | {total_functions} |")
    report_lines.append(f"| Total Manifests | {len(manifests)} |")
    report_lines.append(f"| Covered Bytes | {total_covered:,} / {BANK_SIZE:,} |")
    report_lines.append(f"| Coverage | {coverage_percentage:.1f}% |")
    report_lines.append(f"| Documented Ranges | {len(all_ranges)} |")
    report_lines.append("")
    
    # Overall coverage bar
    report_lines.append(f"**Overall Coverage:** {generate_coverage_bar(coverage_percentage)}")
    report_lines.append("")
    
    # Coverage by 4KB region
    report_lines.append("## Coverage by Region (4KB)")
    report_lines.append("")
    report_lines.append("| Region | Start | End | Covered | Coverage |")
    report_lines.append("|--------|-------|-----|---------|----------|")
    
    for region in region_coverage:
        bar = generate_coverage_bar(region['percentage'], width=20)
        report_lines.append(
            f"| {region['region_num']:02d} | "
            f"C0:{region['start']:04X} | "
            f"C0:{region['end']:04X} | "
            f"{region['covered']:,} / {region['total']:,} | "
            f"{region['percentage']:.1f}% |"
        )
    report_lines.append("")
    
    # Visual map
    report_lines.append("## Visual Coverage Map")
    report_lines.append("")
    report_lines.append("```")
    # Generate a 64x64 character map representing the full 64KB
    for block in range(16):  # 16 blocks of 4KB
        block_start = block * REGION_SIZE
        report_lines.append(f"\nRegion {block:02d} (C0:{block_start:04X}):")
        
        for row in range(16):  # 16 rows of 256 bytes per region
            row_start = block_start + (row * 256)
            row_covered = 0
            for offset in range(256):
                if (row_start + offset) in covered_bytes:
                    row_covered += 1
            
            row_pct = (row_covered / 256) * 100
            if row_covered == 256:
                char_line = "################"
            elif row_covered == 0:
                char_line = "................"
            elif row_pct > 75:
                char_line = "++++++++++++++++"
            elif row_pct > 25:
                char_line = "----------------"
            else:
                char_line = ".......####....."
            
            report_lines.append(f"  C0:{row_start:04X}: {char_line} ({row_covered}/256)")
    report_lines.append("```")
    report_lines.append("")
    
    # Largest gaps
    report_lines.append("## Largest Gaps (Top 20)")
    report_lines.append("")
    report_lines.append("| Rank | Start | End | Size | Visual |")
    report_lines.append("|------|-------|-----|------|--------|")
    
    for i, (start, end, size) in enumerate(gaps[:20], 1):
        bar = "." * min(30, size // 32)
        report_lines.append(f"| {i} | C0:{start:04X} | C0:{end:04X} | {size:,} bytes | {bar} |")
    report_lines.append("")
    
    # Recommended targets
    report_lines.append("## Recommended Next Scanning Targets")
    report_lines.append("")
    report_lines.append("Based on gap analysis and proximity to known code regions:")
    report_lines.append("")
    
    # Find regions with partial coverage (likely to have more code nearby)
    partial_regions = [r for r in region_coverage if 0 < r['percentage'] < 90]
    partial_regions.sort(key=lambda x: x['percentage'], reverse=True)
    
    report_lines.append("### High-Priority Regions (Partial Coverage)")
    report_lines.append("")
    for region in partial_regions[:5]:
        report_lines.append(f"- **Region {region['region_num']:02d}** (C0:{region['start']:04X}-C0:{region['end']:04X}): "
                          f"{region['percentage']:.1f}% covered - extend existing analysis")
    report_lines.append("")
    
    report_lines.append("### Large Uncovered Regions")
    report_lines.append("")
    for gap in gaps[:10]:
        start, end, size = gap
        report_lines.append(f"- **C0:{start:04X}-C0:{end:04X}**: {size:,} bytes "
                          f"(~{size//256} pages)")
    report_lines.append("")
    
    # Coverage by range type
    report_lines.append("## Coverage by Type")
    report_lines.append("")
    type_counts = {}
    for r in all_ranges:
        kind = r['kind']
        size = r['end'] - r['start'] + 1
        if kind not in type_counts:
            type_counts[kind] = {'count': 0, 'bytes': 0}
        type_counts[kind]['count'] += 1
        type_counts[kind]['bytes'] += size
    
    report_lines.append("| Type | Count | Bytes | Percentage |")
    report_lines.append("|------|-------|-------|------------|")
    for kind, stats in sorted(type_counts.items()):
        pct = (stats['bytes'] / BANK_SIZE) * 100
        report_lines.append(f"| {kind} | {stats['count']} | {stats['bytes']:,} | {pct:.1f}% |")
    report_lines.append("")
    
    # Recent additions
    report_lines.append("## Recent Additions (Last 10 Passes)")
    report_lines.append("")
    recent_manifests = sorted(manifests, key=lambda x: x.get('pass_number', 0), reverse=True)[:10]
    report_lines.append("| Pass | Range | Label |")
    report_lines.append("|------|-------|-------|")
    for manifest in recent_manifests:
        pass_num = manifest.get('pass_number', 0)
        for closed_range in manifest.get('closed_ranges', []):
            range_str = closed_range.get('range', '')
            label = closed_range.get('label', '')
            if range_str.startswith('C0:'):
                report_lines.append(f"| {pass_num} | `{range_str}` | {label} |")
    report_lines.append("")
    
    # Write report
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"\nReport generated: {report_path}")
    print(f"Coverage: {coverage_percentage:.1f}% ({total_covered:,} / {BANK_SIZE:,} bytes)")
    print(f"Total functions: {total_functions}")
    print(f"Total manifests: {len(manifests)}")
    print(f"\nTop 5 gaps:")
    for i, (start, end, size) in enumerate(gaps[:5], 1):
        print(f"  {i}. C0:{start:04X}-C0:{end:04X} ({size:,} bytes)")

if __name__ == "__main__":
    from datetime import datetime
    main()
