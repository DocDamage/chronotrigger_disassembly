#!/usr/bin/env python3
"""Generate comprehensive Bank DD report with recommended manifests"""
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
    return json.loads(result.stdout)

def get_closed_ranges():
    """Load closed ranges from snapshot"""
    try:
        with open('tools/cache/closed_ranges_snapshot_v1.json') as f:
            data = json.load(f)
        return data.get('ranges', [])
    except:
        return []

def overlaps_closed_range(start, end, closed_ranges, bank=0xDD):
    """Check if a range overlaps with any closed range"""
    for r in closed_ranges:
        if r.get('bank') == bank:
            closed_start = r.get('start', 0)
            closed_end = r.get('end', 0)
            # Check overlap
            if not (end < closed_start or start > closed_end):
                return True
    return False

def main():
    regions = [
        ('DD:0000..DD:3FFF', 'DD:0000-4000'),
        ('DD:4000..DD:7FFF', 'DD:4000-8000'),
        ('DD:8000..DD:BFFF', 'DD:8000-C000'),
        ('DD:C000..DD:FFFF', 'DD:C000-FFFF'),
    ]
    
    all_clusters = []
    closed_ranges = get_closed_ranges()
    
    print("=" * 80)
    print("BANK DD - REMAINING SCORE-6+ CLUSTER REPORT")
    print("=" * 80)
    print(f"Closed ranges in Bank DD: {len([r for r in closed_ranges if r.get('bank') == 0xDD])}")
    
    for range_text, name in regions:
        print(f"\n{'='*80}")
        print(f"REGION: {name}")
        print("=" * 80)
        
        data = run_scan(range_text)
        clusters = data.get('clusters', [])
        
        # Filter for score-6+ and not overlapping with closed ranges
        score6_plus = []
        for c in clusters:
            if c.get('cluster_score', 0) >= 6:
                # Parse range
                range_str = c.get('range', '')
                parts = range_str.replace('DD:', '').split('..')
                if len(parts) == 2:
                    start = int(parts[0], 16)
                    end = int(parts[1], 16)
                    if not overlaps_closed_range(start, end, closed_ranges):
                        score6_plus.append(c)
        
        print(f"Score-6+ clusters (not yet documented): {len(score6_plus)}")
        
        for c in sorted(score6_plus, key=lambda x: x.get('cluster_score', 0), reverse=True):
            range_str = c.get('range', '')
            score = c.get('cluster_score', 0)
            width = c.get('width', 0)
            returns = c.get('return_count', 0)
            calls = c.get('call_count', 0)
            children = c.get('child_count', 0)
            print(f"  Score {score:2d}: {range_str} ({width:3d}b, {returns:2d}ret, {calls}call, {children}children)")
        
        all_clusters.extend(score6_plus)
    
    # Summary
    print("\n" + "=" * 80)
    print("OVERALL SUMMARY")
    print("=" * 80)
    print(f"Total score-6+ clusters waiting: {len(all_clusters)}")
    
    # Score distribution
    score_dist = {}
    for c in all_clusters:
        s = c.get('cluster_score', 0)
        score_dist[s] = score_dist.get(s, 0) + 1
    
    print("\nScore distribution:")
    for s in sorted(score_dist.keys(), reverse=True):
        print(f"  Score {s:2d}: {score_dist[s]} clusters")
    
    # Regional breakdown
    regions_breakdown = {
        'DD:0000-4000': [],
        'DD:4000-8000': [],
        'DD:8000-C000': [],
        'DD:C000-FFFF': [],
    }
    
    for c in all_clusters:
        range_str = c.get('range', '')
        addr = int(range_str.replace('DD:', '').split('..')[0], 16)
        if addr < 0x4000:
            regions_breakdown['DD:0000-4000'].append(c)
        elif addr < 0x8000:
            regions_breakdown['DD:4000-8000'].append(c)
        elif addr < 0xC000:
            regions_breakdown['DD:8000-C000'].append(c)
        else:
            regions_breakdown['DD:C000-FFFF'].append(c)
    
    print("\nRegional breakdown:")
    for region, clusters in regions_breakdown.items():
        score8_plus = len([c for c in clusters if c.get('cluster_score', 0) >= 8])
        print(f"  {region}: {len(clusters)} score-6+, {score8_plus} score-8+")
    
    # Get next pass number
    manifests_dir = Path('passes/manifests')
    existing_passes = []
    for p in manifests_dir.glob('pass*.json'):
        try:
            if p.stem.startswith('pass') and p.stem[4:].isdigit():
                existing_passes.append(int(p.stem[4:]))
        except:
            pass
    next_pass = max(existing_passes) + 1 if existing_passes else 1
    
    # Generate manifests for score-8+ (priority)
    score8_plus = [c for c in all_clusters if c.get('cluster_score', 0) >= 8]
    score8_sorted = sorted(score8_plus, key=lambda x: x.get('cluster_score', 0), reverse=True)
    
    print("\n" + "=" * 80)
    print("RECOMMENDED MANIFESTS (Score-8+)")
    print("=" * 80)
    print(f"Starting from pass {next_pass}\n")
    
    manifests = []
    for i, c in enumerate(score8_sorted[:25], start=next_pass):
        range_str = c.get('range', '')
        score = c.get('cluster_score', 0)
        width = c.get('width', 0)
        
        parts = range_str.replace('DD:', '').split('..')
        start_hex = parts[0]
        end_hex = parts[1]
        
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
            "promotion_reason": f"Score-{score} cluster, {width} bytes. Bank DD function candidate."
        }
        manifests.append(manifest)
        
        print(f"pass{i}.json:")
        print(json.dumps(manifest, indent=2))
        print()
    
    # Also list score-6 and score-7 for next session
    score6_7 = [c for c in all_clusters if 6 <= c.get('cluster_score', 0) <= 7]
    score6_7_sorted = sorted(score6_7, key=lambda x: x.get('cluster_score', 0), reverse=True)
    
    print("\n" + "=" * 80)
    print("SCORE-6/7 CLUSTERS (For next session)")
    print("=" * 80)
    for c in score6_7_sorted:
        range_str = c.get('range', '')
        score = c.get('cluster_score', 0)
        width = c.get('width', 0)
        returns = c.get('return_count', 0)
        calls = c.get('call_count', 0)
        print(f"  Score {score}: {range_str} ({width}b, {returns}ret, {calls}call)")
    
    # Save results
    output = {
        'timestamp': '2026-04-08',
        'bank': 'DD',
        'summary': {
            'total_score6_plus': len(all_clusters),
            'total_score8_plus': len(score8_plus),
            'score_distribution': score_dist,
            'regional_breakdown': {k: len(v) for k, v in regions_breakdown.items()}
        },
        'score8_plus_clusters': score8_sorted,
        'score6_7_clusters': score6_7_sorted,
        'recommended_manifests': manifests,
        'next_pass_number': next_pass + len(manifests)
    }
    
    with open('BANK_DD_SCORE6_PLUS_REPORT.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "=" * 80)
    print(f"Report saved to BANK_DD_SCORE6_PLUS_REPORT.json")
    print(f"Recommended manifests: pass{next_pass}.json to pass{next_pass + len(manifests) - 1}.json")
    print(f"Next session should start at pass {next_pass + len(manifests)}")

if __name__ == '__main__':
    main()
