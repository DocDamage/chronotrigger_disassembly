#!/usr/bin/env python3
"""Analyze Bank DD clusters and generate report"""
import json
import subprocess
import sys

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
    except json.JSONDecodeError:
        return []

def main():
    regions = [
        ('DD:0000..DD:3FFF', 'DD:0000-4000'),
        ('DD:4000..DD:7FFF', 'DD:4000-8000'),
        ('DD:8000..DD:BFFF', 'DD:8000-C000'),
        ('DD:C000..DD:FFFF', 'DD:C000-FFFF'),
    ]
    
    all_score6_plus = []
    all_score8_plus = []
    
    print("=" * 70)
    print("BANK DD - REMAINING SCORE-6+ CLUSTER ANALYSIS")
    print("=" * 70)
    
    for range_text, name in regions:
        print(f"\n## {name}")
        clusters = run_scan(range_text)
        
        score6_plus = [c for c in clusters if c.get('score', 0) >= 6]
        score8_plus = [c for c in clusters if c.get('score', 0) >= 8]
        
        all_score6_plus.extend(score6_plus)
        all_score8_plus.extend(score8_plus)
        
        print(f"  Total clusters: {len(clusters)}")
        print(f"  Score-6+ clusters: {len(score6_plus)}")
        print(f"  Score-8+ clusters: {len(score8_plus)}")
        
        # Sort by score descending
        sorted_clusters = sorted(score6_plus, key=lambda x: x.get('score', 0), reverse=True)
        
        print(f"\n  Top clusters:")
        for c in sorted_clusters[:10]:
            start = c.get('start', '')[3:]  # Remove DD:
            end = c.get('end', '')[3:]
            score = c.get('score', 0)
            width = c.get('byte_width', 0)
            returns = c.get('returns', 0)
            calls = c.get('calls', 0)
            print(f"    Score {score:2d}: DD:{start}..{end} ({width:3d} bytes, {returns:2d} ret, {calls} call)")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total score-6+ clusters across Bank DD: {len(all_score6_plus)}")
    print(f"Total score-8+ clusters across Bank DD: {len(all_score8_plus)}")
    
    # Score distribution
    score_counts = {}
    for c in all_score6_plus:
        s = c.get('score', 0)
        score_counts[s] = score_counts.get(s, 0) + 1
    
    print("\nScore distribution:")
    for score in sorted(score_counts.keys(), reverse=True):
        print(f"  Score {score:2d}: {score_counts[score]} clusters")
    
    # Output JSON for further processing
    output = {
        'score6_plus': all_score6_plus,
        'score8_plus': all_score8_plus,
        'summary': {
            'total_score6_plus': len(all_score6_plus),
            'total_score8_plus': len(all_score8_plus),
            'score_distribution': score_counts
        }
    }
    
    with open('dd_remaining_clusters.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\nResults saved to dd_remaining_clusters.json")

if __name__ == '__main__':
    main()
