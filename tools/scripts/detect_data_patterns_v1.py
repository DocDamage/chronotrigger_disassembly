#!/usr/bin/env python3
"""Detect data patterns vs code patterns in ROM regions.

Identifies:
- Repeating structural patterns (like C6:CC00-D000 PHP/SED/PLP/BRK)
- Zero-filled dead zones
- ASCII/text regions
- Jump vector tables (like C4:C0C0)
"""

import argparse
from pathlib import Path

def hirom_to_file_offset(bank, addr):
    """Convert HiROM SNES address to file offset."""
    return ((bank - 0xC0) * 0x10000) + addr

def detect_repeating_pattern(data, pattern_length=4, min_repeats=4):
    """Detect repeating byte patterns."""
    if len(data) < pattern_length * min_repeats:
        return None
    
    patterns = {}
    for i in range(0, len(data) - pattern_length, pattern_length):
        pattern = tuple(data[i:i+pattern_length])
        patterns[pattern] = patterns.get(pattern, 0) + 1
    
    # Find patterns that repeat significantly
    significant = {p: c for p, c in patterns.items() if c >= min_repeats}
    return significant

def detect_zero_fill(data, threshold=0.9):
    """Detect zero-filled regions."""
    zero_count = sum(1 for b in data if b == 0)
    return zero_count / len(data) >= threshold

def detect_ascii_text(data, threshold=0.7):
    """Detect ASCII text regions."""
    printable = sum(1 for b in data if 32 <= b < 127 or b in (0x0A, 0x0D, 0x00))
    return printable / len(data) >= threshold

def analyze_region(rom_path, bank, start, end):
    """Analyze a ROM region for data patterns."""
    rom = Path(rom_path).read_bytes()
    
    file_start = hirom_to_file_offset(bank, start)
    file_end = hirom_to_file_offset(bank, end)
    
    data = rom[file_start:file_end]
    
    results = {
        'bank': f"{bank:02X}",
        'range': f"{bank:02X}:{start:04X}-{bank:02X}:{end:04X}",
        'size': len(data),
        'is_zero_fill': detect_zero_fill(data),
        'is_ascii': detect_ascii_text(data),
        'repeating_patterns': detect_repeating_pattern(data),
        'php_count': data.count(0x08),  # PHP
        'plp_count': data.count(0x28),  # PLP
        'sed_count': data.count(0xF8),  # SED
        'brk_count': data.count(0x00),  # BRK
        'rts_count': data.count(0x60),  # RTS
        'rtl_count': data.count(0x6B),  # RTL
    }
    
    return results

def classify_region(results):
    """Classify region as code, data, or structural."""
    
    # Check for C6:CC00-D000 style pattern (PHP/SED...PLP/BRK)
    if (results['php_count'] > 50 and 
        results['sed_count'] > 40 and 
        results['plp_count'] > 20 and
        results['brk_count'] > 20):
        return "DATA_ENCODED_CONTROL", "PHP/SED/PLP/BRK structural pattern (bytecode/state machine)"
    
    # Check for zero fill
    if results['is_zero_fill']:
        return "DEAD_ZONE", "Zero-filled (exclude from mapping)"
    
    # Check for ASCII
    if results['is_ascii']:
        return "TEXT_DATA", "ASCII text region"
    
    # Check for jump vector table (RTS/RTL heavy with regular spacing)
    if results['rts_count'] + results['rtl_count'] > 50:
        return "VECTOR_TABLE", "Likely jump vector table"
    
    # Low opcode density suggests data
    if results['rts_count'] + results['rtl_count'] < 5 and results['php_count'] < 10:
        return "DATA_TABLE", "Low opcode density, likely data"
    
    return "CODE_CANDIDATE", "Standard code region"

def main():
    parser = argparse.ArgumentParser(description='Detect data patterns in ROM regions')
    parser.add_argument('--rom', required=True, help='Path to ROM file')
    parser.add_argument('--bank', type=lambda x: int(x, 16), required=True, help='Bank (hex)')
    parser.add_argument('--start', type=lambda x: int(x, 16), required=True, help='Start address (hex)')
    parser.add_argument('--end', type=lambda x: int(x, 16), required=True, help='End address (hex)')
    
    args = parser.parse_args()
    
    results = analyze_region(args.rom, args.bank, args.start, args.end)
    classification, reason = classify_region(results)
    
    print(f"Region: {results['range']} ({results['size']} bytes)")
    print(f"Classification: {classification}")
    print(f"Reason: {reason}")
    print()
    print(f"Statistics:")
    print(f"  PHP (08): {results['php_count']}")
    print(f"  PLP (28): {results['plp_count']}")
    print(f"  SED (F8): {results['sed_count']}")
    print(f"  BRK (00): {results['brk_count']}")
    print(f"  RTS (60): {results['rts_count']}")
    print(f"  RTL (6B): {results['rtl_count']}")
    
    if results['repeating_patterns']:
        print()
        print("Repeating patterns:")
        for pattern, count in list(results['repeating_patterns'].items())[:5]:
            hex_str = ' '.join(f'{b:02X}' for b in pattern)
            print(f"  [{hex_str}]: {count} times")

if __name__ == '__main__':
    main()
