#!/usr/bin/env python3
"""
Auto-promote high-caller targets from seam block scan JSON.
Creates pass manifests automatically with conflict detection and boundary adjustment.
"""

import json
import glob
import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional

MANIFESTS_DIR = Path('../../passes/manifests')
ROM_PATH = Path('../../rom/Chrono Trigger (USA).sfc')


def addr_to_int(addr: str) -> int:
    """Convert C0:1234 to integer."""
    bank, offset = addr.split(':')
    return int(bank, 16) * 0x10000 + int(offset, 16)


def int_to_addr(val: int) -> str:
    """Convert integer to C0:1234 format."""
    bank = val // 0x10000
    offset = val % 0x10000
    return f"C{bank}:{offset:04X}"


def parse_range(r: str) -> Tuple[str, int, int]:
    """Parse 'C0:1234..C0:5678' into (bank, start, end)."""
    start, end = r.split('..')
    bank = start.split(':')[0]
    return (bank, addr_to_int(start), addr_to_int(end))


def ranges_overlap(r1: str, r2: str) -> bool:
    """Check if two ranges overlap (same bank only)."""
    b1, s1, e1 = parse_range(r1)
    b2, s2, e2 = parse_range(r2)
    if b1 != b2:
        return False
    return not (e1 < s2 or e2 < s1)


def find_next_pass_number() -> int:
    """Find the next available pass number."""
    max_num = 0
    for mf in MANIFESTS_DIR.glob('pass*.json'):
        try:
            num = int(mf.stem.replace('pass', ''))
            max_num = max(max_num, num)
        except:
            pass
    return max_num + 1


def get_existing_ranges() -> List[Tuple[str, str]]:
    """Load all existing pass ranges."""
    ranges = []
    for mf in MANIFESTS_DIR.glob('pass*.json'):
        try:
            with open(mf) as f:
                data = json.load(f)
            for r in data.get('closed_ranges', []):
                ranges.append((mf.name, r['range']))
        except:
            pass
    return ranges


def check_conflicts(new_range: str, existing: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Check for conflicts with existing passes."""
    conflicts = []
    for name, existing_range in existing:
        if ranges_overlap(new_range, existing_range):
            conflicts.append((name, existing_range))
    return conflicts


def adjust_boundary(start: str, end: str, conflicts: List[Tuple[str, str]]) -> Optional[str]:
    """Adjust boundary to avoid conflicts. Returns new range or None."""
    bank = start.split(':')[0]
    start_int = addr_to_int(start)
    end_int = addr_to_int(end)
    
    # Try to shrink from end first
    for conflict_pass, conflict_range in conflicts:
        cb, cs, ce = parse_range(conflict_range)
        if start_int <= ce and cs <= end_int:
            # Overlapping - try to end before conflict starts
            new_end = cs - 1
            if new_end > start_int + 10:  # Minimum 10 bytes
                return f"{start}..{bank}:{new_end:04X}"
    
    return None


def extract_targets_from_scan(scan_data: Dict) -> List[Dict]:
    """Extract high-caller targets from scan JSON."""
    targets = []
    
    for page in scan_data.get('pages', []):
        page_range = page.get('range', '')
        
        for target_info in page.get('best_targets', []):
            target_addr = target_info.get('target', '')
            callers = target_info.get('callers', [])
            strength = target_info.get('best_strength', '')
            hit_count = target_info.get('hit_count', 0)
            
            # Skip invalid targets unless they have massive caller counts
            if strength == 'invalid' and hit_count < 10:
                continue
            
            # Find best backtrack candidate
            best_backtrack = None
            best_score = -100
            
            for bt in page.get('top_backtracks', []):
                if bt.get('target') == target_addr:
                    score = bt.get('score', 0)
                    if score > best_score:
                        best_score = score
                        best_backtrack = bt
            
            # Use target address if no good backtrack
            if best_backtrack:
                start_addr = best_backtrack.get('candidate_start', target_addr)
                start_class = best_backtrack.get('start_class', '')
            else:
                start_addr = target_addr
                start_class = ''
            
            targets.append({
                'target': target_addr,
                'start': start_addr,
                'callers': callers,
                'caller_count': len(callers),
                'strength': strength,
                'score': best_score,
                'start_class': start_class,
                'page': page_range,
                'backtrack': best_backtrack
            })
    
    return targets


def suggest_boundary(target: Dict, min_size: int = 20, max_size: int = 50) -> str:
    """Suggest a boundary range for a target."""
    start = target['start']
    bank = start.split(':')[0]
    start_int = addr_to_int(start)
    
    # Estimate end based on backtrack candidate range if available
    if target['backtrack']:
        candidate_range = target['backtrack'].get('candidate_range', '')
        if candidate_range:
            try:
                parts = candidate_range.split('..')
                if len(parts) == 2:
                    end_int = addr_to_int(parts[1])
                    return f"{start}..{int_to_addr(end_int)}"
            except:
                pass
    
    # Default size based on caller count
    if target['caller_count'] >= 5:
        size = 35
    elif target['caller_count'] >= 3:
        size = 30
    else:
        size = 25
    
    end_int = start_int + size
    return f"{start}..{bank}:{end_int:04X}"


def create_pass_manifest(pass_num: int, range_str: str, target: Dict) -> Dict:
    """Create a pass manifest dictionary."""
    label = f"ct_c0_{target['start'].replace(':', '').lower()}_function_{target['caller_count']}callers"
    
    confidence = "high" if target['strength'] == 'weak' and target['caller_count'] >= 3 else "medium"
    
    reason = f"{target['caller_count']} callers ({target['strength']})"
    if target['start_class']:
        reason += f", {target['start_class']}"
    if target['score'] > 0:
        reason += f", score {target['score']}"
    
    return {
        "pass_number": pass_num,
        "closed_ranges": [{
            "range": range_str,
            "kind": "owner",
            "label": label,
            "confidence": confidence
        }],
        "promotion_reason": reason
    }


def main():
    parser = argparse.ArgumentParser(description='Auto-promote high-caller targets from scan JSON')
    parser.add_argument('--scan-file', '-f', required=True, help='Path to scan JSON file')
    parser.add_argument('--min-callers', '-c', type=int, default=2, help='Minimum caller count (default: 2)')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Dry run - do not create files')
    parser.add_argument('--auto-fix', '-a', action='store_true', help='Auto-adjust boundaries to avoid conflicts')
    
    args = parser.parse_args()
    
    # Load scan data (handle UTF-16 encoding)
    import codecs
    with open(args.scan_file, 'rb') as f:
        raw = f.read()
        if raw.startswith(codecs.BOM_UTF16_LE):
            content = raw.decode('utf-16-le')
            content = content.lstrip('\ufeff')  # Strip BOM if present
        elif raw.startswith(codecs.BOM_UTF16_BE):
            content = raw.decode('utf-16-be')
            content = content.lstrip('\ufeff')
        else:
            content = raw.decode('utf-8-sig')
        scan_data = json.loads(content)
    
    # Extract targets
    targets = extract_targets_from_scan(scan_data)
    
    # Filter by caller count
    targets = [t for t in targets if t['caller_count'] >= args.min_callers]
    
    if not targets:
        print(f"No targets with {args.min_callers}+ callers found.")
        return
    
    print(f"Found {len(targets)} targets with {args.min_callers}+ callers:\n")
    
    # Get existing ranges for conflict checking
    existing_ranges = get_existing_ranges()
    
    # Process each target
    next_pass = find_next_pass_number()
    created = []
    skipped = []
    adjusted = []
    
    for target in sorted(targets, key=lambda x: -x['caller_count']):
        suggested_range = suggest_boundary(target)
        
        print(f"Target: {target['target']}")
        print(f"  Callers: {target['caller_count']} ({target['strength']})")
        print(f"  Suggested range: {suggested_range}")
        
        # Check for conflicts
        conflicts = check_conflicts(suggested_range, existing_ranges)
        
        if conflicts:
            print(f"  [WARN]  CONFLICTS found:")
            for name, r in conflicts:
                print(f"      {name}: {r}")
            
            if args.auto_fix:
                adjusted_range = adjust_boundary(
                    suggested_range.split('..')[0],
                    suggested_range.split('..')[1],
                    conflicts
                )
                if adjusted_range:
                    print(f"  [OK]  Auto-adjusted to: {adjusted_range}")
                    suggested_range = adjusted_range
                    adjusted.append(target)
                else:
                    print(f"  [FAIL] Cannot auto-fix, skipping")
                    skipped.append((target, "conflict"))
                    print()
                    continue
            else:
                print(f"  Use --auto-fix to attempt boundary adjustment")
                skipped.append((target, "conflict"))
                print()
                continue
        
        # Create pass
        manifest = create_pass_manifest(next_pass, suggested_range, target)
        
        if not args.dry_run:
            output_path = MANIFESTS_DIR / f"pass{next_pass}.json"
            with open(output_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            print(f"  [OK] Created pass{next_pass}.json")
        else:
            print(f"  [DRY RUN] Would create pass{next_pass}.json")
        
        created.append((next_pass, target, suggested_range))
        existing_ranges.append((f"pass{next_pass}.json", suggested_range))
        next_pass += 1
        print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Targets found: {len(targets)}")
    print(f"Passes created: {len(created)}")
    print(f"Adjusted boundaries: {len(adjusted)}")
    print(f"Skipped (conflicts): {len(skipped)}")
    
    if created:
        print("\nCreated passes:")
        for num, target, range_str in created:
            print(f"  pass{num}.json: {target['target']} ({target['caller_count']} callers) -> {range_str}")


if __name__ == '__main__':
    main()
