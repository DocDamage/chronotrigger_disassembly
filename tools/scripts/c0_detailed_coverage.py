#!/usr/bin/env python3
"""
Detailed Bank C0 Coverage Analysis with Heatmap
"""

import json
import re
from pathlib import Path
from collections import defaultdict

def parse_range(range_str):
    m = re.match(r'([0-9A-Fa-f]{2}):([0-9A-Fa-f]{4})\.\.([0-9A-Fa-f]{2}):([0-9A-Fa-f]{4})', range_str)
    if not m:
        return None
    bank = int(m.group(1), 16)
    start = int(m.group(2), 16)
    end = int(m.group(4), 16)
    return (bank, start, end)

def coverage_char(pct):
    """Return a character representing coverage level"""
    if pct == 0:
        return '.'  # Empty
    elif pct < 25:
        return '-'  # Light
    elif pct < 50:
        return '+'  # Medium
    elif pct < 75:
        return '*'  # Heavy
    else:
        return '#'  # Full

def main():
    c0_ranges = []
    manifest_dir = Path('../../passes/manifests')
    
    print("Loading manifests...")
    for manifest_file in sorted(manifest_dir.glob('pass*.json')):
        try:
            with open(manifest_file, 'r') as f:
                data = json.load(f)
            
            pass_num = data.get('pass_number', 0)
            closed_ranges = data.get('closed_ranges', [])
            
            for entry in closed_ranges:
                range_str = entry.get('range', '')
                parsed = parse_range(range_str)
                if parsed and parsed[0] == 0xC0:
                    c0_ranges.append({
                        'pass': pass_num,
                        'start': parsed[1],
                        'end': parsed[2],
                        'range': range_str,
                        'kind': entry.get('kind', 'unknown'),
                        'label': entry.get('label', 'unknown')
                    })
        except Exception as e:
            pass
    
    # Calculate coverage
    PAGE_SIZE = 256
    TOTAL_PAGES = 256
    
    page_coverage = [0] * TOTAL_PAGES
    
    for r in c0_ranges:
        start_page = r['start'] // PAGE_SIZE
        end_page = r['end'] // PAGE_SIZE
        
        for page in range(start_page, min(end_page + 1, TOTAL_PAGES)):
            page_start = page * PAGE_SIZE
            page_end = page_start + PAGE_SIZE - 1
            overlap_start = max(r['start'], page_start)
            overlap_end = min(r['end'], page_end)
            overlap_bytes = max(0, overlap_end - overlap_start + 1)
            page_coverage[page] += overlap_bytes
    
    page_coverage_pct = [(page_coverage[i] / PAGE_SIZE) * 100 for i in range(TOTAL_PAGES)]
    
    # Print heatmap (16 rows of 16 pages = 256 pages)
    print("\n" + "="*80)
    print("BANK C0 COVERAGE HEATMAP (256 pages of 256 bytes each)")
    print("Legend: .=0%  -<25%  +<50%  *<75%  #=<100%")
    print("="*80)
    print("       0 1 2 3 4 5 6 7 8 9 A B C D E F")
    
    for row in range(16):
        row_addr = row * 16 * 256  # Starting address for this row
        chars = []
        for col in range(16):
            page = row * 16 + col
            chars.append(coverage_char(page_coverage_pct[page]))
        print(f"C0:{row_addr:04X} {' '.join(chars)}")
    
    # Coverage statistics
    print("\n" + "="*80)
    print("COVERAGE STATISTICS")
    print("="*80)
    
    total_bytes = sum(page_coverage)
    bank_size = 64 * 1024
    
    print(f"\nTotal Coverage: {total_bytes:,} / {bank_size:,} bytes ({(total_bytes/bank_size)*100:.2f}%)")
    print(f"Total Functions: {len(c0_ranges)}")
    
    # Coverage buckets
    zero_pages = sum(1 for p in page_coverage_pct if p == 0)
    low_pages = sum(1 for p in page_coverage_pct if 0 < p < 25)
    med_pages = sum(1 for p in page_coverage_pct if 25 <= p < 75)
    high_pages = sum(1 for p in page_coverage_pct if p >= 75)
    
    print(f"\nCoverage Distribution:")
    print(f"  0%    (empty):  {zero_pages:3d} pages ({(zero_pages/256)*100:.1f}%)")
    print(f"  1-25%  (low):    {low_pages:3d} pages ({(low_pages/256)*100:.1f}%)")
    print(f"  25-75% (med):    {med_pages:3d} pages ({(med_pages/256)*100:.1f}%)")
    print(f"  75-100%(high):   {high_pages:3d} pages ({(high_pages/256)*100:.1f}%)")
    
    # Best covered 1KB regions
    print("\n" + "="*80)
    print("TOP 5 BEST COVERED 1KB REGIONS")
    print("="*80)
    
    region_cov = []
    for i in range(64):
        start_page = i * 4
        cov = sum(page_coverage_pct[p] for p in range(start_page, start_page + 4)) / 4
        addr = i * 1024
        region_cov.append((addr, cov))
    
    region_cov.sort(key=lambda x: -x[1])
    for i, (addr, cov) in enumerate(region_cov[:5]):
        print(f"{i+1}. C0:{addr:04X}-{addr+0x3FF:04X}: {cov:.1f}%")
    
    # Worst covered 1KB regions
    print("\n" + "="*80)
    print("TOP 5 LEAST COVERED 1KB REGIONS")
    print("="*80)
    
    region_cov.sort(key=lambda x: x[1])
    for i, (addr, cov) in enumerate(region_cov[:5]):
        print(f"{i+1}. C0:{addr:04X}-{addr+0x3FF:04X}: {cov:.1f}%")
    
    # Coverage by 4KB sectors (typical for ROM organization)
    print("\n" + "="*80)
    print("COVERAGE BY 4KB SECTORS (16 sectors)")
    print("="*80)
    
    for i in range(16):
        start_page = i * 16
        sector_cov = sum(page_coverage_pct[p] for p in range(start_page, start_page + 16)) / 16
        addr = i * 4096
        bar_len = int(sector_cov / 5)
        bar = "#" * bar_len + "-" * (20 - bar_len)
        print(f"C0:{addr:04X}-{addr+0xFFF:04X}: {bar} {sector_cov:5.1f}%")
    
    # Find all pages with <10% coverage
    print("\n" + "="*80)
    print("ALL PAGES WITH <10% COVERAGE (for detailed scanning)")
    print("="*80)
    
    low_cov_pages = [(i, page_coverage_pct[i]) for i in range(256) if page_coverage_pct[i] < 10]
    
    print(f"Total: {len(low_cov_pages)} pages")
    print("\nPages by section:")
    
    # Group by 1KB region
    kb_groups = defaultdict(list)
    for page, pct in low_cov_pages:
        kb_region = (page // 4) * 1024
        kb_groups[kb_region].append((page, pct))
    
    for kb_addr in sorted(kb_groups.keys()):
        pages = kb_groups[kb_addr]
        page_nums = [f"{p[0]*256:02X}" for p in pages]
        print(f"  C0:{kb_addr:04X}: pages at offsets {', '.join(page_nums[:8])}")

if __name__ == '__main__':
    main()
