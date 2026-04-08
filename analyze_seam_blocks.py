#!/usr/bin/env python3
import json

def analyze_seam_block(filepath):
    with open(filepath, 'r', encoding='utf-16') as f:
        data = json.load(f)
    
    range_name = data.get('range', 'Unknown')
    print(f"\n{'='*60}")
    print(f"SEAM BLOCK: {range_name}")
    print(f"{'='*60}")
    
    # Summary
    summary = data.get('summary', {})
    print(f"\nTotal pages: {summary.get('page_count', 0)}")
    print(f"Status: {summary.get('final_status', 'N/A')}")
    
    # Raw xrefs
    raw_xrefs = data.get('raw_xrefs', {})
    print(f"\n--- Raw XRefs ---")
    print(f"Total targets: {raw_xrefs.get('target_count', 0)}")
    print(f"Strong hits: {raw_xrefs.get('strong_hit_count', 0)}")
    print(f"Weak hits: {raw_xrefs.get('weak_hit_count', 0)}")
    
    # Page results
    print(f"\n--- Page Results ---")
    for page in data.get('pages', []):
        page_addr = page.get('range', 'Unknown')
        status = page.get('review_posture', 'N/A')
        family = page.get('page_family', 'N/A')
        print(f"\n  {page_addr}: {status} ({family})")
        
        # Show top owner backtrack candidates
        if 'owner_backtrack' in page:
            ob = page['owner_backtrack']
            candidates = sorted(ob.get('candidates', []), key=lambda x: x.get('score', 0), reverse=True)[:3]
            for c in candidates:
                if c.get('score', 0) >= 5:
                    print(f"    -> {c['target']}: score={c['score']}, start={c['candidate_start']}")
        
        # Show tiny veneers
        if 'tiny_veneers' in page:
            tv = page['tiny_veneers']
            for v in tv.get('candidates', [])[:3]:
                print(f"    -> VENEER {v['range']}: {v['pattern']} -> {v['target']}")

if __name__ == "__main__":
    files = [
        'reports/c3_2900_seam_block.json',
        'reports/c3_3000_seam_block.json',
        'reports/c3_3100_seam_block.json',
        'reports/c3_3700_seam_block.json',
    ]
    
    for f in files:
        try:
            analyze_seam_block(f)
        except Exception as e:
            import traceback
            print(f"Error processing {f}: {e}")
            traceback.print_exc()
