#!/usr/bin/env python3
"""Verify DB candidates by examining ROM bytes."""
import sys
sys.path.insert(0, 'tools/scripts')

import json
from pathlib import Path
from collections import defaultdict
from snes_utils_hirom_v2 import parse_snes_address

# Likely prologue opcodes
LIKELY_PROLOG = {0xA9, 0xA2, 0xA0, 0x08, 0x48, 0xDA, 0x5A, 0x20, 0x22, 0x0B, 0x4B, 0x8B, 0xC2}
RETURNS = {0x60, 0x6B, 0x40}
BARRIERS = {0x00, 0x02, 0xFF}

def hirom_to_offset(bank, addr):
    return ((bank - 0xC0) * 0x10000) + addr

def read_bytes(rom, bank, addr, count):
    off = hirom_to_offset(bank, addr)
    return rom[off:off+count]

def analyze_function(rom, bank, addr, lookahead=32):
    """Analyze potential function at address."""
    off = hirom_to_offset(bank, addr)
    bytes_data = rom[off:off+lookahead]
    
    if not bytes_data:
        return None
    
    first = bytes_data[0]
    has_return = any(b in RETURNS for b in bytes_data)
    has_call = any(b in {0x20, 0x22} for b in bytes_data)
    has_branch = any(b in {0x10, 0x30, 0x50, 0x70, 0x80, 0x90, 0xB0, 0xD0, 0xF0} for b in bytes_data)
    barrier_count = sum(1 for b in bytes_data if b in BARRIERS)
    
    return {
        'first_byte': f'{first:02X}',
        'is_prolog': first in LIKELY_PROLOG,
        'has_return': has_return,
        'has_call': has_call,
        'has_branch': has_branch,
        'barrier_count': barrier_count,
        'hex_preview': ' '.join(f'{b:02X}' for b in bytes_data[:16]),
    }

def main():
    rom = Path('rom/Chrono Trigger (USA).sfc').read_bytes()
    
    # Load backtrack candidates
    with open('reports/db_0000_4000_backtrack.json', encoding='utf-8-sig') as f:
        bt1 = json.load(f)
    with open('reports/db_4000_8000_backtrack.json', encoding='utf-8-sig') as f:
        bt2 = json.load(f)
    
    # Load cross-bank callers
    with open('reports/db_cross_bank_callers.json') as f:
        xcall = json.load(f)
    
    cross_bank_targets = set(xcall['targets'].keys())
    
    print("=" * 70)
    print("BANK DB CANDIDATE VERIFICATION")
    print("=" * 70)
    print()
    
    # Prioritize candidates that are cross-bank targets
    all_candidates = []
    for c in bt1['candidates'] + bt2['candidates']:
        if c['score'] >= 6:
            all_candidates.append(c)
    
    # Sort: cross-bank targets first, then by score
    def sort_key(c):
        is_xcall = c['candidate_start'] in cross_bank_targets
        return (-int(is_xcall), -c['score'], c['candidate_start'])
    
    all_candidates.sort(key=sort_key)
    
    print("TOP 20 PRIORITY CANDIDATES (cross-bank targets marked with *)")
    print("-" * 70)
    
    verified = []
    for c in all_candidates[:20]:
        addr_str = c['candidate_start']
        bank, addr = parse_snes_address(addr_str)
        analysis = analyze_function(rom, bank, addr)
        
        is_xcall = addr_str in cross_bank_targets
        marker = "*" if is_xcall else " "
        
        prolog_ok = "OK" if analysis['is_prolog'] else "--"
        return_ok = "OK" if analysis['has_return'] else "--"
        
        print(f"{marker} {addr_str} score={c['score']:2d} | "
              f"prolog={prolog_ok} return={return_ok} | "
              f"{analysis['hex_preview']}")
        
        if analysis['is_prolog'] and analysis['has_return']:
            verified.append({
                'addr': addr_str,
                'score': c['score'],
                'is_cross_bank': is_xcall,
                'analysis': analysis
            })
    
    print()
    print("=" * 70)
    print(f"VERIFIED CANDIDATES (prolog + return): {len(verified)}")
    print("-" * 70)
    for v in verified[:15]:
        marker = "*" if v['is_cross_bank'] else " "
        print(f"{marker} {v['addr']} score={v['score']}")
    
    # Save results
    with open('reports/db_verified_candidates.json', 'w') as f:
        json.dump(verified, f, indent=2)
    print()
    print("Results saved to reports/db_verified_candidates.json")

if __name__ == '__main__':
    main()
