#!/usr/bin/env python3
"""Generate comprehensive C0 mapping report."""
import json
from pathlib import Path
from datetime import datetime

def load_json(path):
    with open(path, encoding='utf-8-sig') as f:
        return json.load(f)

def main():
    repo_root = Path(__file__).parent.parent.parent
    
    # Load data
    islands_8000 = load_json(repo_root / "reports" / "c0_8000_bfff_islands.json")
    islands_c000 = load_json(repo_root / "reports" / "c0_c000_ffff_islands.json")
    back_8000 = load_json(repo_root / "reports" / "c0_8000_bfff_backtrack.json")
    back_c000 = load_json(repo_root / "reports" / "c0_c000_ffff_backtrack.json")
    
    # Count by score
    def count_by_score(items, key=None):
        counts = {}
        for item in items:
            score = item['score']
            counts[score] = counts.get(score, 0) + 1
        return counts
    
    print("=" * 70)
    print("BANK C0 MAPPING REPORT - UPPER REGIONS (8000-FFFF)")
    print("=" * 70)
    print(f"Generated: {datetime.now().isoformat()}")
    print()
    
    print("REGION: C0:8000-BFFF")
    print("-" * 70)
    print(f"  Islands found: {islands_8000['island_count']} total")
    print(f"  Score distribution: {dict(sorted(count_by_score(islands_8000['islands']).items(), reverse=True))}")
    
    score6plus = [i for i in islands_8000['islands'] if i['score'] >= 6]
    print(f"  Score-6+ islands: {len(score6plus)}")
    
    print(f"\n  Backtrack candidates: {back_8000['candidate_count']} total")
    bt_score6plus = [c for c in back_8000['candidates'] if c['score'] >= 6]
    print(f"  Score-6+ backtracks: {len(bt_score6plus)}")
    
    print()
    print("REGION: C0:C000-FFFF")
    print("-" * 70)
    print(f"  Islands found: {islands_c000['island_count']} total")
    print(f"  Score distribution: {dict(sorted(count_by_score(islands_c000['islands']).items(), reverse=True))}")
    
    score6plus_c = [i for i in islands_c000['islands'] if i['score'] >= 6]
    print(f"  Score-6+ islands: {len(score6plus_c)}")
    
    print(f"\n  Backtrack candidates: {back_c000['candidate_count']} total")
    bt_score6plus_c = [c for c in back_c000['candidates'] if c['score'] >= 6]
    print(f"  Score-6+ backtracks: {len(bt_score6plus_c)}")
    
    print()
    print("=" * 70)
    print("TOP CANDIDATES SUMMARY")
    print("=" * 70)
    
    all_islands = [('C0:8000-BFFF', i) for i in score6plus] + [('C0:C000-FFFF', i) for i in score6plus_c]
    all_islands.sort(key=lambda x: (-x[1]['score'], x[1]['range']))
    
    print("\nTop 15 Score-6+ Islands:")
    for region, i in all_islands[:15]:
        print(f"  {i['range']} ({region}): score={i['score']}, width={i['width']}, calls={i['call_count']}")
    
    all_bt = [('C0:8000-BFFF', c) for c in bt_score6plus] + [('C0:C000-FFFF', c) for c in bt_score6plus_c]
    all_bt.sort(key=lambda x: (-x[1]['score'], x[1]['candidate_start']))
    
    print("\nTop 15 Score-6+ Backtrack Candidates:")
    for region, c in all_bt[:15]:
        print(f"  {c['candidate_start']} ({region}): score={c['score']}, target={c['target']}, start={c['start_byte']}")
    
    print()
    print("=" * 70)
    print("MANIFESTS GENERATED")
    print("=" * 70)
    
    manifests_dir = repo_root / "passes" / "manifests"
    new_manifests = sorted([f for f in manifests_dir.glob("pass*.json") if int(f.stem.replace('pass', '')) >= 882])
    print(f"Total new manifests: {len(new_manifests)}")
    print(f"Range: {new_manifests[0].name} to {new_manifests[-1].name}")
    
    print()
    print("Generated manifests:")
    for m in new_manifests:
        with open(m) as f:
            data = json.load(f)
        print(f"  {m.name}: {data['range']['start']}..{data['range']['end']} (score={data['score']}, method={data['method']})")

if __name__ == "__main__":
    main()
