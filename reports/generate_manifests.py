#!/usr/bin/env python3
"""Generate manifest recommendations for Bank DB."""
import sys
sys.path.insert(0, 'tools/scripts')

import json
from pathlib import Path
from collections import OrderedDict
from snes_utils_hirom_v2 import parse_snes_address

def deduplicate_candidates(candidates):
    """Remove duplicate addresses, keeping highest score."""
    seen = {}
    for c in candidates:
        addr = c['addr']
        if addr not in seen or seen[addr]['score'] < c['score']:
            seen[addr] = c
    return list(seen.values())

def estimate_end(rom, bank, start_addr):
    """Estimate function end by looking for return or barrier."""
    from snes_utils_hirom_v2 import hirom_to_file_offset
    offset = hirom_to_file_offset(bank, start_addr)
    RETURNS = {0x60, 0x6B, 0x40}  # RTS, RTL, RTI
    BARRIERS = {0x00, 0x02, 0xFF}
    
    # Look for return within first 256 bytes
    for i in range(min(256, len(rom) - offset)):
        b = rom[offset + i]
        if b in RETURNS:
            return start_addr + i + 1  # Include the return instruction
        if b in BARRIERS and i > 8:
            return start_addr + i
    return start_addr + 32  # Default

def main():
    rom = Path('rom/Chrono Trigger (USA).sfc').read_bytes()
    
    # Load verified candidates
    with open('reports/db_verified_candidates.json') as f:
        verified = json.load(f)
    
    # Load cross-bank callers
    with open('reports/db_cross_bank_callers.json') as f:
        xcall = json.load(f)
    cross_bank_targets = set(xcall['targets'].keys())
    
    # Deduplicate
    unique = deduplicate_candidates(verified)
    unique.sort(key=lambda x: (-int(x['is_cross_bank']), -x['score'], x['addr']))
    
    print("=" * 70)
    print("BANK DB MANIFEST RECOMMENDATIONS")
    print("=" * 70)
    print(f"\nTotal unique verified candidates: {len(unique)}")
    print(f"Cross-bank targets: {sum(1 for v in unique if v['is_cross_bank'])}")
    print()
    
    # Generate manifest entries
    manifests = []
    for i, v in enumerate(unique[:15], 1):  # Top 15
        addr_str = v['addr']
        bank, addr = parse_snes_address(addr_str)
        end = estimate_end(rom, bank, addr)
        
        is_xcall = addr_str in cross_bank_targets
        xcall_marker = "_XCALL" if is_xcall else ""
        
        label = f"CT_DB_{addr:04X}_SCORE{v['score']}{xcall_marker}"
        
        manifest = {
            'label': label,
            'addr': addr_str,
            'range': f"{addr_str}..DB:{end:04X}",
            'score': v['score'],
            'is_cross_bank': is_xcall,
            'kind': 'owner',
            'confidence': 'high' if v['score'] >= 6 else 'medium',
        }
        manifests.append(manifest)
        
        print(f"{i}. {label}")
        print(f"   Range: {manifest['range']}")
        print(f"   Score: {v['score']}, Cross-bank: {is_xcall}")
        print()
    
    # Save manifest recommendations
    with open('reports/db_manifest_recommendations.json', 'w') as f:
        json.dump(manifests, f, indent=2)
    
    print("=" * 70)
    print("Manifest recommendations saved to:")
    print("  reports/db_manifest_recommendations.json")
    print()
    print("Summary:")
    print(f"  - Generated {len(manifests)} manifest entries")
    print(f"  - Score 6+ candidates: {len([m for m in manifests if m['score'] >= 6])}")
    print(f"  - Cross-bank targets: {len([m for m in manifests if m['is_cross_bank']])}")

if __name__ == '__main__':
    main()
