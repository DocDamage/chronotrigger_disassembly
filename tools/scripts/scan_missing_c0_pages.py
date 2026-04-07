#!/usr/bin/env python3
"""Scan all missing C0 pages to find functions for disassembly."""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROM_PATH = "rom/Chrono Trigger (USA).sfc"

def run_seam_block(start, pages=1):
    """Run seam block scan on a range of pages."""
    cmd = [
        sys.executable, str(SCRIPT_DIR / "run_seam_block_v1.py"),
        "--rom", ROM_PATH,
        "--start", start,
        "--pages", str(pages),
        "--json"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"Error scanning {start}: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception scanning {start}: {e}")
        return None


def main():
    # Read missing pages
    with open(SCRIPT_DIR / "missing_c0_pages.txt") as f:
        missing_pages = [line.strip() for line in f if line.strip()]
    
    print(f"Scanning {len(missing_pages)} missing C0 pages...")
    
    # Results tracking
    has_code_pages = []
    data_pages = []
    errors = []
    
    # Scan each missing page individually
    for i, page in enumerate(missing_pages):
        print(f"\n[{i+1}/{len(missing_pages)}] Scanning {page}...")
        
        result = run_seam_block(page, 1)
        if not result:
            errors.append(page)
            continue
        
        page_info = result.get('pages', [{}])[0]
        page_family = page_info.get('page_family', 'unknown')
        posture = page_info.get('review_posture', 'unknown')
        
        print(f"  Family: {page_family}, Posture: {posture}")
        
        # Check if page has code
        if page_family in ('local-code-only', 'local-code-with-candidates', 'has-candidates'):
            has_code_pages.append({
                'page': page,
                'family': page_family,
                'posture': posture,
                'summary': page_info.get('summary', {}),
                'best_targets': page_info.get('best_targets', []),
                'local_clusters': page_info.get('local_clusters', [])
            })
        elif page_family == 'data-only':
            data_pages.append({
                'page': page,
                'family': page_family
            })
    
    # Save results
    results = {
        'scanned_count': len(missing_pages),
        'has_code_pages': has_code_pages,
        'data_pages': data_pages,
        'errors': errors
    }
    
    output_file = SCRIPT_DIR / "c0_scan_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n\n{'='*60}")
    print(f"SCAN COMPLETE")
    print(f"{'='*60}")
    print(f"Total missing pages scanned: {len(missing_pages)}")
    print(f"Pages with code: {len(has_code_pages)}")
    print(f"Data-only pages: {len(data_pages)}")
    print(f"Errors: {len(errors)}")
    
    if has_code_pages:
        print(f"\n--- Pages with code (potential new passes) ---")
        for p in has_code_pages:
            print(f"  {p['page']}: {p['family']} / {p['posture']}")
    
    print(f"\nResults saved to: {output_file}")


if __name__ == '__main__':
    main()
