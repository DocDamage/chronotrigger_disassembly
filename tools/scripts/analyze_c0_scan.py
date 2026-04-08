#!/usr/bin/env python3
import json
from pathlib import Path

def analyze_islands(path, name):
    with open(path, encoding='utf-8-sig') as f:
        data = json.load(f)
    islands = [i for i in data['islands'] if i['score'] >= 6]
    islands.sort(key=lambda x: -x['score'])
    print(f"\n{name}: {len(islands)} score-6+ islands out of {data['island_count']} total")
    print("-" * 60)
    for i in islands[:25]:
        ret_count = i['return_count'] if isinstance(i['return_count'], int) else len(i['return_count'])
        print(f"  {i['range']}: score={i['score']}, width={i['width']}, calls={i['call_count']}, rets={ret_count}")
    return islands

def analyze_backtrack(path, name):
    with open(path, encoding='utf-8-sig') as f:
        data = json.load(f)
    items = [i for i in data['candidates'] if i['score'] >= 6]
    items.sort(key=lambda x: (-x['score'], x['candidate_start']))
    print(f"\n{name}: {len(items)} score-6+ candidates")
    print("-" * 60)
    for i in items[:20]:
        print(f"  {i['candidate_start']} -> {i['target']} (score={i['score']}, start={i['start_byte']})")
    return items

if __name__ == "__main__":
    import sys
    repo_root = Path(__file__).parent.parent.parent
    
    islands_8000 = analyze_islands(repo_root / "reports" / "c0_8000_bfff_islands.json", "C0:8000-BFFF Islands")
    islands_c000 = analyze_islands(repo_root / "reports" / "c0_c000_ffff_islands.json", "C0:C000-FFFF Islands")
    
    back_8000 = analyze_backtrack(repo_root / "reports" / "c0_8000_bfff_backtrack.json", "C0:8000-BFFF Backtrack")
    back_c000 = analyze_backtrack(repo_root / "reports" / "c0_c000_ffff_backtrack.json", "C0:C000-FFFF Backtrack")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"C0:8000-BFFF: {len(islands_8000)} island candidates, {len(back_8000)} backtrack candidates")
    print(f"C0:C000-FFFF: {len(islands_c000)} island candidates, {len(back_c000)} backtrack candidates")
    print(f"Total score-6+ candidates: {len(islands_8000) + len(islands_c000) + len(back_8000) + len(back_c000)}")
