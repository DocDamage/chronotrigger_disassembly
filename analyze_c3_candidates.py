#!/usr/bin/env python3
import os
import re
import yaml

def analyze_candidates():
    candidates = []
    for f in os.listdir('labels/c3_candidates'):
        if 'SCORE4' in f or 'SCORE5' in f or 'SCORE6' in f:
            try:
                filepath = f'labels/c3_candidates/{f}'
                with open(filepath) as fp:
                    content = fp.read()
                    # Extract start address using regex
                    m = re.search(r'start:\s*"(C3:[0-9A-F]{4})"', content)
                    if m:
                        start = m.group(1)
                        addr = int(start.split(':')[1], 16)
                        # Extract score
                        score_m = re.search(r'score:\s*(\d+)', content)
                        score = int(score_m.group(1)) if score_m else 0
                        candidates.append((addr, score, f))
            except Exception as e:
                pass
    
    candidates.sort()
    print(f"Total candidates found: {len(candidates)}")
    print("\nCandidates by address:")
    for addr, score, name in candidates:
        print(f"  C3:{addr:04X} (score {score}) - {name}")
    
    # Group by region
    print("\n\nBy region:")
    regions = {
        "0000-1FFF": [],
        "2000-3FFF": [],
        "4000-5FFF": [],
        "6000-7FFF": [],
        "8000-9FFF": [],
        "A000-BFFF": [],
        "C000-DFFF": [],
        "E000-FFFF": []
    }
    
    for addr, score, name in candidates:
        for region, items in regions.items():
            start, end = region.split('-')
            if int(start, 16) <= addr < int(end, 16):
                items.append((addr, score, name))
                break
    
    for region, items in regions.items():
        if items:
            print(f"\n  Region {region}: {len(items)} candidates")
            for addr, score, name in items:
                print(f"    C3:{addr:04X} score-{score}")

if __name__ == "__main__":
    analyze_candidates()
