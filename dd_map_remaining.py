#!/usr/bin/env python3
"""Map remaining Bank DD clusters and generate manifests"""
import json
import subprocess
import sys
from pathlib import Path

def run_scan(range_text):
    """Run find_local_code_islands_v2.py and return clusters"""
    cmd = [
        'python', 'tools/scripts/find_local_code_islands_v2.py',
        '--rom', 'rom/Chrono Trigger (USA).sfc',
        '--range', range_text,
        '--max-back', '48',
        '--json'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error scanning {range_text}: {result.stderr}", file=sys.stderr)
        return []
    try:
        data = json.loads(result.stdout)
        return data.get('clusters', [])
    except json.JSONDecodeError as e:
        print(f"JSON error for {range_text}: {e}", file=sys.stderr)
        return []

def format_addr(addr_str):
    """Format address string like DD:1234"""
    return addr_str.replace('0x', '').upper()

def main():
    regions = [
        ('DD:0000..DD:3FFF', 'DD:0000-4000'),
        ('DD:4000..DD:7FFF', 'DD:4000-8000'),
        ('DD:8000..DD:BFFF', 'DD:8000-C000'),
        ('DD:C000..DD:FFFF', 'DD:C000-FFFF'),
    ]
    
    all_clusters = []
    
    print("=" * 80)
    print("BANK DD REMAINING CLUSTER MAPPING")
    print("=" * 80)
    
    for range_text, name in regions:
        print(f"\n## Scanning {name}")
        clusters = run_scan(range_text)
        
        score6_plus = [c for c in clusters if c.get('score', 0) >= 6]
        score8_plus = [c for c in clusters if c.get('score', 0) >= 8]
        
        all_clusters.extend(clusters)
        
        print(f"  Total clusters found: {len(clusters)}")
        print(f"  Score-6+ clusters: {len(score6_plus)}")
        print(f"  Score-8+ clusters: {len(score8_plus)}")
        
        if score6_plus:
            print(f"\n  Score-6+ clusters (sorted by score):")
            sorted_clusters = sorted(score6_plus, key=lambda x: x.get('score', 0), reverse=True)
            for c in sorted_clusters:
                start = format_addr(c.get('start', '??'))
                end = format_addr(c.get('end', '??'))
                score = c.get('score', 0)
                width = c.get('byte_width', 0)
                returns = c.get('returns', 0)
                calls = c.get('calls', 0)
                branches = c.get('branches', 0)
                print(f"    Score {score:2d}: {start}..{end} ({width:3d}b, {returns:2d}ret, {calls}call, {branches}branch)")
    
    # Overall summary
    all_score6 = [c for c in all_clusters if c.get('score', 0) >= 6]
    all_score8 = [c for c in all_clusters if c.get('score', 0) >= 8]
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total clusters found: {len(all_clusters)}")
    print(f"Score-6+ clusters: {len(all_score6)}")
    print(f"Score-8+ clusters: {len(all_score8)}")
    
    # Score distribution
    score_dist = {}
    for c in all_score6:
        s = c.get('score', 0)
        score_dist[s] = score_dist.get(s, 0) + 1
    
    print("\nScore-6+ distribution:")
    for score in sorted(score_dist.keys(), reverse=True):
        count = score_dist[score]
        print(f"  Score {score:2d}: {count} clusters")
    
    # Generate recommended manifests for score-8+
    print("\n" + "=" * 80)
    print("RECOMMENDED MANIFESTS (Score-8+)")
    print("=" * 80)
    
    # Get next available pass number
    manifests_dir = Path('passes/manifests')
    existing_passes = []
    for p in manifests_dir.glob('pass*.json'):
        try:
            # Only extract numeric part from standard pass names like pass123.json
            if p.stem.startswith('pass') and p.stem[4:].isdigit():
                existing_passes.append(int(p.stem[4:]))
        except (ValueError, IndexError):
            pass
    next_pass = max(existing_passes) + 1 if existing_passes else 1
    print(f"\nNext available pass number: {next_pass}")
    
    score8_sorted = sorted(all_score8, key=lambda x: x.get('score', 0), reverse=True)
    
    manifests = []
    for i, c in enumerate(score8_sorted[:25], start=next_pass):
        start = c.get('start', '')
        end = c.get('end', '')
        score = c.get('score', 0)
        width = c.get('byte_width', 0)
        
        # Extract hex addresses
        start_hex = start.split(':')[1] if ':' in start else '0000'
        end_hex = end.split(':')[1] if ':' in end else '0000'
        
        manifest = {
            "pass_number": i,
            "closed_ranges": [
                {
                    "range": f"DD:{start_hex}..DD:{end_hex}",
                    "kind": "owner",
                    "label": f"ct_dd_{start_hex.lower()}_score{score}_cluster",
                    "confidence": "high" if score >= 10 else "medium"
                }
            ],
            "promotion_reason": f"Score-{score} cluster, {width} bytes. Bank DD remaining function candidate."
        }
        manifests.append(manifest)
        print(f"\npass{i}.json:")
        print(json.dumps(manifest, indent=2))
    
    # Save results
    output = {
        'all_clusters': all_clusters,
        'score6_plus': all_score6,
        'score8_plus': all_score8,
        'recommended_manifests': manifests,
        'summary': {
            'total_clusters': len(all_clusters),
            'score6_plus_count': len(all_score6),
            'score8_plus_count': len(all_score8),
            'score_distribution': score_dist
        }
    }
    
    with open('dd_mapping_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n\nResults saved to dd_mapping_results.json")
    print(f"Recommended manifests: pass{next_pass}.json to pass{next_pass + len(manifests) - 1}.json")

if __name__ == '__main__':
    main()
