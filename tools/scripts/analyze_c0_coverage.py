#!/usr/bin/env python3
"""
Bank C0 Coverage Analysis Tool
Analyzes coverage of C0:0000-FFFF across all pass manifests.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

def parse_range(range_str):
    """Parse SNES range like 'C0:231B..C0:2329'"""
    m = re.match(r'([0-9A-Fa-f]{2}):([0-9A-Fa-f]{4})\.\.([0-9A-Fa-f]{2}):([0-9A-Fa-f]{4})', range_str)
    if not m:
        return None
    bank = int(m.group(1), 16)
    start = int(m.group(2), 16)
    end = int(m.group(4), 16)
    return (bank, start, end)

def main():
    # Load all manifests and extract C0 ranges
    c0_ranges = []
    manifest_dir = Path('../../passes/manifests')
    
    print("Loading manifests...")
    manifest_count = 0
    for manifest_file in sorted(manifest_dir.glob('pass*.json')):
        try:
            with open(manifest_file, 'r') as f:
                data = json.load(f)
            manifest_count += 1
            
            pass_num = data.get('pass_number', 0)
            closed_ranges = data.get('closed_ranges', [])
            
            for entry in closed_ranges:
                range_str = entry.get('range', '')
                parsed = parse_range(range_str)
                if parsed and parsed[0] == 0xC0:  # Bank C0
                    c0_ranges.append({
                        'pass': pass_num,
                        'start': parsed[1],
                        'end': parsed[2],
                        'range': range_str,
                        'kind': entry.get('kind', 'unknown'),
                        'label': entry.get('label', 'unknown')
                    })
        except Exception as e:
            print(f'Error reading {manifest_file}: {e}')
    
    print(f"\n{'='*60}")
    print("BANK C0 COVERAGE ANALYSIS REPORT")
    print(f"{'='*60}")
    print(f"Manifests scanned: {manifest_count}")
    print(f"Total C0 ranges found: {len(c0_ranges)}")
    
    # Calculate total bytes covered
    total_bytes = sum(r['end'] - r['start'] + 1 for r in c0_ranges)
    bank_size = 64 * 1024  # 64KB
    coverage_pct = (total_bytes / bank_size) * 100
    print(f"Total bytes covered: {total_bytes} / {bank_size} ({coverage_pct:.1f}%)")
    
    # Calculate by 256-byte pages (C0:0000-FFFF = 256 pages of 256 bytes each)
    PAGE_SIZE = 256
    TOTAL_PAGES = 256
    
    page_coverage_bytes = [0] * TOTAL_PAGES
    page_functions = [[] for _ in range(TOTAL_PAGES)]
    
    for r in c0_ranges:
        start_page = r['start'] // PAGE_SIZE
        end_page = r['end'] // PAGE_SIZE
        
        for page in range(start_page, min(end_page + 1, TOTAL_PAGES)):
            page_start = page * PAGE_SIZE
            page_end = page_start + PAGE_SIZE - 1
            
            overlap_start = max(r['start'], page_start)
            overlap_end = min(r['end'], page_end)
            overlap_bytes = max(0, overlap_end - overlap_start + 1)
            
            page_coverage_bytes[page] += overlap_bytes
            page_functions[page].append(r['label'])
    
    # Convert to percentages
    page_coverage_pct = [(page_coverage_bytes[i] / PAGE_SIZE) * 100 for i in range(TOTAL_PAGES)]
    
    # Count completely uncovered pages
    uncovered_pages = sum(1 for p in page_coverage_pct if p == 0)
    low_coverage_pages = [(i, page_coverage_pct[i]) for i in range(TOTAL_PAGES) if 0 < page_coverage_pct[i] < 10]
    
    print(f"\n{'='*60}")
    print("PAGE COVERAGE SUMMARY")
    print(f"{'='*60}")
    print(f"Pages with 0% coverage: {uncovered_pages} / {TOTAL_PAGES}")
    print(f"Pages with 1-10% coverage: {len(low_coverage_pages)} / {TOTAL_PAGES}")
    
    # Calculate 1KB region coverage
    REGIONS_1KB = 64
    print(f"\n{'='*60}")
    print("COVERAGE BY 1KB REGIONS")
    print(f"{'='*60}")
    
    region_data = []
    for i in range(REGIONS_1KB):
        start_page = i * 4
        end_page = start_page + 3
        total_cov = sum(page_coverage_pct[p] for p in range(start_page, min(end_page + 1, TOTAL_PAGES)))
        avg_cov = total_cov / 4
        addr_start = i * 1024
        addr_end = addr_start + 1023
        region_data.append((i, addr_start, addr_end, avg_cov))
        print(f"C0:{addr_start:04X}-{addr_end:04X}: {avg_cov:5.1f}%")
    
    # Find top 5 most under-covered regions
    print(f"\n{'='*60}")
    print("TOP 10 MOST UNDER-COVERED 256-BYTE PAGES")
    print(f"{'='*60}")
    
    page_data = [(i, i * PAGE_SIZE, page_coverage_pct[i]) for i in range(TOTAL_PAGES)]
    page_data.sort(key=lambda x: x[2])
    
    for i, (page, addr, cov) in enumerate(page_data[:10]):
        funcs = page_functions[page]
        func_str = f" ({len(funcs)} funcs)" if funcs else " (0 funcs)"
        print(f"{i+1:2d}. C0:{addr:04X}-{addr+0xFF:04X}: {cov:5.1f}% covered{func_str}")
    
    # Identify gaps (consecutive uncovered/low coverage regions)
    print(f"\n{'='*60}")
    print("LARGEST GAPS (CONSECUTIVE LOW/NO COVERAGE)")
    print(f"{'='*60}")
    
    gaps = []
    gap_start = None
    
    for i in range(TOTAL_PAGES):
        if page_coverage_pct[i] < 10:
            if gap_start is None:
                gap_start = i
        else:
            if gap_start is not None:
                gap_size = i - gap_start
                if gap_size >= 2:  # At least 2 consecutive pages
                    gaps.append((gap_start, i - 1, gap_size))
                gap_start = None
    
    # Handle gap at end
    if gap_start is not None:
        gap_size = TOTAL_PAGES - gap_start
        if gap_size >= 2:
            gaps.append((gap_start, TOTAL_PAGES - 1, gap_size))
    
    gaps.sort(key=lambda x: -x[2])
    
    for i, (start, end, size) in enumerate(gaps[:10]):
        start_addr = start * PAGE_SIZE
        end_addr = end * PAGE_SIZE + 0xFF
        print(f"{i+1:2d}. C0:{start_addr:04X}-{end_addr:04X}: {size} pages ({size*256} bytes)")
    
    # Function kind breakdown
    print(f"\n{'='*60}")
    print("FUNCTION TYPES BREAKDOWN")
    print(f"{'='*60}")
    
    kind_counts = defaultdict(int)
    kind_bytes = defaultdict(int)
    for r in c0_ranges:
        kind = r['kind']
        kind_counts[kind] += 1
        kind_bytes[kind] += r['end'] - r['start'] + 1
    
    for kind in sorted(kind_counts.keys()):
        count = kind_counts[kind]
        bytes_cov = kind_bytes[kind]
        print(f"{kind:20s}: {count:4d} functions, {bytes_cov:5d} bytes")
    
    # Scanning recommendations
    print(f"\n{'='*60}")
    print("SCANNING PRIORITY RECOMMENDATIONS")
    print(f"{'='*60}")
    
    # Find top 5 largest gaps as recommendations
    for i, (start, end, size) in enumerate(gaps[:5]):
        start_addr = start * PAGE_SIZE
        end_addr = end * PAGE_SIZE + 0xFF
        print(f"{i+1}. Scan C0:{start_addr:04X}..C0:{end_addr:04X}")
        print(f"   Size: {size*256} bytes ({size} pages), estimated {size//4 + 1} functions")
    
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
