#!/usr/bin/env python3
"""Generate manifest recommendations for C0:8000-FFFF mapping."""
import json
import re
from pathlib import Path
from datetime import datetime

def load_json(path):
    with open(path, encoding='utf-8-sig') as f:
        return json.load(f)

def load_existing_labels(repo_root):
    """Load existing C0 label addresses to avoid overlap."""
    labels_dir = repo_root / "labels"
    existing = []
    pattern = re.compile(r'[Cc]0[_:]?([0-9A-Fa-f]{4})')
    
    for f in labels_dir.glob("*.asm"):
        match = pattern.search(f.name)
        if match:
            addr = int(match.group(1), 16)
            existing.append((addr, f.name))
    return sorted(existing)

def parse_range(r):
    """Parse 'C0:XXXX..C0:YYYY' to (start, end)"""
    parts = r.split('..')
    start = int(parts[0].split(':')[1], 16)
    end = int(parts[1].split(':')[1], 16)
    return (start, end)

def overlaps_existing(start, end, existing):
    """Check if range overlaps with any existing label."""
    for addr, name in existing:
        # Assume documented ranges are small, roughly 10-100 bytes
        # This is a heuristic - real ranges would be parsed from manifest files
        est_end = addr + 100  # conservative estimate
        if not (end < addr or start > est_end):
            return True, name
    return False, None

def generate_manifest(candidate, repo_root, pass_num):
    """Generate a manifest file for a candidate."""
    manifests_dir = repo_root / "passes" / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)
    
    if 'candidate_start' in candidate:
        # Backtrack format
        addr_str = candidate['candidate_start']
        addr = int(addr_str.split(':')[1], 16)
        end_addr = int(candidate['target'].split(':')[1], 16) + 16
        score = candidate['score']
        start_byte = candidate['start_byte']
        method = "backtrack"
    else:
        # Island format
        start, end = parse_range(candidate['range'])
        addr_str = f"C0:{start:04X}"
        addr = start
        end_addr = end
        score = candidate['score']
        start_byte = "??"
        method = "island"
    
    manifest = {
        "pass": pass_num,
        "source": "c0_8000_ffff_mapping",
        "timestamp": datetime.now().isoformat(),
        "target_bank": "C0",
        "method": method,
        "score": score,
        "range": {
            "start": f"C0:{addr:04X}",
            "end": f"C0:{end_addr:04X}"
        },
        "label_name": f"ct_c0_{addr:04x}_score{score}_{method}",
        "start_byte": start_byte,
        "metadata": {
            "rom": "rom/Chrono Trigger (USA).sfc",
            "notes": f"Auto-generated from {method} analysis"
        }
    }
    
    filename = f"pass{pass_num}.json"
    path = manifests_dir / filename
    with open(path, 'w') as f:
        json.dump(manifest, f, indent=2)
    return filename

def main():
    repo_root = Path(__file__).parent.parent.parent
    
    # Load data
    islands_8000 = load_json(repo_root / "reports" / "c0_8000_bfff_islands.json")
    islands_c000 = load_json(repo_root / "reports" / "c0_c000_ffff_islands.json")
    back_8000 = load_json(repo_root / "reports" / "c0_8000_bfff_backtrack.json")
    back_c000 = load_json(repo_root / "reports" / "c0_c000_ffff_backtrack.json")
    
    existing = load_existing_labels(repo_root)
    print(f"Found {len(existing)} existing C0 labels")
    
    # Collect all candidates
    candidates = []
    
    # Process islands
    for i in islands_8000['islands'] + islands_c000['islands']:
        if i['score'] >= 6:
            start, end = parse_range(i['range'])
            if not overlaps_existing(start, end, existing)[0]:
                candidates.append(('island', i))
    
    # Process backtracks
    for b in back_8000['candidates'] + back_c000['candidates']:
        if b['score'] >= 6:
            addr = int(b['candidate_start'].split(':')[1], 16)
            end_addr = int(b['target'].split(':')[1], 16) + 16
            if not overlaps_existing(addr, end_addr, existing)[0]:
                candidates.append(('backtrack', b))
    
    print(f"\nFound {len(candidates)} non-overlapping score-6+ candidates")
    
    # Sort by score, then by address
    def sort_key(c):
        if c[0] == 'island':
            start, _ = parse_range(c[1]['range'])
            return (-c[1]['score'], start)
        else:
            addr = int(c[1]['candidate_start'].split(':')[1], 16)
            return (-c[1]['score'], addr)
    
    candidates.sort(key=sort_key)
    
    # Find next pass number
    manifests_dir = repo_root / "passes" / "manifests"
    existing_passes = [int(f.stem.replace('pass', '')) for f in manifests_dir.glob("pass*.json") if f.stem.replace('pass', '').isdigit()]
    next_pass = max(existing_passes) + 1 if existing_passes else 1
    
    # Generate top 20 manifests
    print("\n" + "=" * 70)
    print("TOP 20 CANDIDATES (Non-overlapping)")
    print("=" * 70)
    
    generated = []
    for i, (method, c) in enumerate(candidates[:20]):
        if method == 'island':
            start, end = parse_range(c['range'])
            range_str = f"C0:{start:04X}..C0:{end:04X}"
            print(f"\n{i+1}. {range_str} (score={c['score']}, method={method})")
            print(f"   width={c['width']}, calls={c['call_count']}, rets={c['return_count'] if isinstance(c['return_count'], int) else len(c['return_count'])}")
        else:
            start = int(c['candidate_start'].split(':')[1], 16)
            end = int(c['target'].split(':')[1], 16) + 16
            range_str = f"{c['candidate_start']}..C0:{end:04X}"
            print(f"\n{i+1}. {range_str} (score={c['score']}, method={method})")
            print(f"   target={c['target']}, start_byte={c['start_byte']}, start_class={c['start_class']}")
        
        # Generate manifest
        filename = generate_manifest(c, repo_root, next_pass + i)
        generated.append(filename)
        print(f"   -> {filename}")
    
    print(f"\n\nGenerated {len(generated)} manifests: {', '.join(generated[:5])}...")
    
    # Summary by region
    print("\n" + "=" * 70)
    print("REGION SUMMARY")
    print("=" * 70)
    
    region_8000 = [c for c in candidates if parse_range(c[1]['range'])[0] < 0xC000 if c[0] == 'island'] + \
                  [c for c in candidates if int(c[1]['candidate_start'].split(':')[1], 16) < 0xC000 if c[0] == 'backtrack']
    region_c000 = [c for c in candidates if parse_range(c[1]['range'])[0] >= 0xC000 if c[0] == 'island'] + \
                  [c for c in candidates if int(c[1]['candidate_start'].split(':')[1], 16) >= 0xC000 if c[0] == 'backtrack']
    
    print(f"C0:8000-BFFF: {len(region_8000)} candidates")
    print(f"C0:C000-FFFF: {len(region_c000)} candidates")

if __name__ == "__main__":
    main()
